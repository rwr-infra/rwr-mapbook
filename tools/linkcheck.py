#!/usr/bin/env python3
"""产物链接体检：site/ 里的每一条站内链接都要落到真实存在的页面上。

为什么需要它
------------
`zensical build --strict` 只校验**源文件**里的链接（`project.validation` 那两项），
而站内链接还有三类是在构建之后才定型的，源里看不出来：

  1. 模板拼出来的链接（面包屑、语言切换器、页脚、标签胶囊）；
  2. 手写的跳转桩（`docs/*.html` 里 `<meta http-equiv="refresh">` 的目标）；
  3. 由 `tools/tagfilter.py` 事后改过的标签索引。

这三类出问题时构建一声不吭，读者点到才发现。本脚本就在产物上兜底：
`make build` 的最后一步跑它，红了就说明这次不该发。

四条判据
--------
  1. 站内引用必须落到真实存在的文件，或含 `index.html` 的目录；
  2. **指向目录的引用必须以 `/` 收尾**——少一个斜杠，那一页就会停在错误的
     基址上，页面里所有向下的相对链接都会抬高一级（见
     `overrides/partials/trailing-slash.html` 的说明）。这条是把那个坑钉住；
  3. 每个跳转桩的 refresh 目标必须存在（桩指到没了的地方，等于把 404 藏起来）；
  4. 每一页都要带上目录地址补正脚本，产物里少了它，上面那个坑就会重新打开。
     手写的跳转桩（`docs/*.html`）除外：它们不是页面，读者立刻被 refresh 带走，
     自身的链接也全是根相对路径，补正脚本对它们没有意义。

判据 2 与 4 是同一件事的两半：2 管「本站自己不生成少斜杠的地址」，
4 管「别人拿少斜杠的地址进来也还能用」。

    uv run python tools/linkcheck.py
"""

from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

ATTR_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]*)"')
REFRESH_RE = re.compile(r"<meta[^>]*http-equiv=\"refresh\"[^>]*>", re.I)
CONTENT_RE = re.compile(r'content\s*=\s*"([^"]*)"', re.I)
URL_RE = re.compile(r"url\s*=\s*([^;\"'\s]+)", re.I)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
CANONICALIZER = 'id="__trailing-slash"'


def page_dir(path: Path) -> str:
    """页面在站点里的目录，带尾斜杠（根目录为空串）。"""
    rel = path.parent.relative_to(SITE).as_posix()
    return "" if rel == "." else rel + "/"


def resolve(page: str, ref: str) -> str:
    """引用 → 站点内的规范路径（去引号、去查询串与锚点、解码百分号）。"""
    clean = ref.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return ""
    clean = unquote(clean)
    joined = posixpath.join("/" + page, clean)
    return posixpath.normpath(joined).lstrip("/")


def is_internal(ref: str) -> bool:
    return bool(ref) and not ref.startswith("#") and not ref.startswith("//") and not SCHEME_RE.match(ref)


def target_state(site_rel: str) -> str:
    """站点内路径的状态：file / dir / missing。空串是站点根。"""
    path = SITE / site_rel.rstrip("/")
    if path.is_file():
        return "file"
    if path.is_dir():
        # 根目录本身也算「含 index.html 的目录」——`./..` 这类回到根的引用是合法的。
        return "dir" if (path / "index.html").is_file() else "missing"
    return "missing"


def check_page(path: Path) -> tuple[list[str], int]:
    """检查一个页面，返回（问题列表，引用数）。"""
    html = path.read_text(encoding="utf-8")
    rel = path.relative_to(SITE).as_posix()
    page = page_dir(path)
    problems: list[str] = []

    refs = ATTR_RE.findall(html)
    # 自检：产物里 href/src 的书写形式若变了（单引号、无引号），上面这条正则会漏读，
    # 那样本脚本会安静地放行。数目对不上就直接报错，而不是假装检查过了。
    for attr in ("href", "src"):
        seen = len(re.findall(attr + r"\s*=", html))
        parsed = len(re.findall(attr + r'\s*=\s*"', html))
        if seen != parsed:
            problems.append(
                f"{rel}: {attr}= 出现 {seen} 次，其中 {parsed} 次是双引号形式——"
                f"产物属性写法变了，本脚本会漏读，请先修检查器"
            )

    for ref in refs:
        if not is_internal(ref):
            continue
        site_rel = resolve(page, ref)
        state = target_state(site_rel)
        if state == "missing":
            problems.append(f"{rel}: 引用落空  {ref}  →  /{site_rel}")
        elif state == "dir" and site_rel and not ref.split("#", 1)[0].split("?", 1)[0].endswith("/"):
            # 站点根（site_rel 为空）不在此列：根地址本来就以 / 收尾，`./..`、`../..`
            # 这类回到根的引用是规范的。
            problems.append(
                f"{rel}: 目录引用少了尾斜杠  {ref}  →  /{site_rel}  "
                f"（这一页会停在 /{site_rel} 上，页内向下链接会整体抬高一级）"
            )

    # 跳转桩：refresh 的目标也要存在。
    refresh_tags = REFRESH_RE.findall(html)
    for tag in refresh_tags:
        content = CONTENT_RE.search(tag)
        target = URL_RE.search(content.group(1)) if content else None
        if not target:
            problems.append(f"{rel}: refresh 标签里读不到目标  {tag}")
            continue
        site_rel = resolve(page, target.group(1))
        if target_state(site_rel) == "missing":
            problems.append(f"{rel}: 跳转目标落空  {target.group(1)}  →  /{site_rel}")

    if not refresh_tags and CANONICALIZER not in html:
        problems.append(f"{rel}: 缺少目录地址补正脚本（{CANONICALIZER}）")

    # 同一处问题在页面上常重复出现（页眉、侧栏、页脚各一份），只报一次但带上次数。
    counted: dict[str, int] = {}
    for problem in problems:
        counted[problem] = counted.get(problem, 0) + 1
    unique = [p if n == 1 else f"{p}  （页面内出现 {n} 次）" for p, n in counted.items()]

    return unique, len(refs)


def main() -> int:
    pages = sorted(SITE.rglob("*.html"))
    if not pages:
        print("没有找到产物（site/**/*.html）——先构建再跑本脚本。", file=sys.stderr)
        return 1

    total_refs = 0
    all_problems: list[str] = []
    for path in pages:
        problems, refs = check_page(path)
        total_refs += refs
        all_problems.extend(problems)

    print(f"链接体检：{len(pages)} 个页面、{total_refs} 处引用")
    if all_problems:
        print(f"\n发现 {len(all_problems)} 个问题：")
        for problem in all_problems:
            print("  " + problem)
        return 1
    print("站内引用全部落地，目录引用都带尾斜杠，跳转桩目标都在，补正脚本无遗漏。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
