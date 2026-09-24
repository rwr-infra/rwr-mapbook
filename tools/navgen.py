#!/usr/bin/env python3
"""从文件树生成导航文件（.nav.yml）。

设计前提
--------
导航的唯一来源是内容本身，不再手工维护一份导航配置：

* **顺序**来自各目录 index.md 的 `nav:` 列表（列出该目录的子项名字）；
* **显示名**优先取该页的 `nav_label`，其次 `title`，再次首个一级标题；
* 顶层目录的顺序来自 `docs/index.md` 的 `nav:`。

也就是说：一个文件夹的全部导航元数据，就写在它自己的 index.md 里。

分区
----
本站的导航树是**一棵**（Zensical 的 nav 是全站唯一的），而每种语言需要独立的顺序。
做法是在树里挂一批**从不显示**的分区节点，标题带机器可识别的标记前缀，
由模板按当前页面决定渲染哪一支、跳过哪一支：

    __lang:en        语言分区（docs/en）

于是树形是

    docs/.nav.yml
      ├── 各内容分区                        ← 简体
      ├── __lang:en      → en/             ← 英文
      └── __lang:zh-hant → zh-hant/        ← 繁体

模板侧的对应逻辑在 overrides/partials/nav.html、tabs.html（只渲染当前那一支）
与 path.html（面包屑跳过这一层）里。

生成物
------
每个含内容的目录下写一个 `.nav.yml`（以点开头，不会被当成页面构建）。
**不要手改这些文件**，改 index.md 后重跑本脚本即可。

    uv run python tools/navgen.py           # 生成
    uv run python tools/navgen.py --check   # 只检查是否有过期，不写盘
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

from langs import DEFAULT_LANG, other_languages

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

#: 语言分区的标记名。语言分区本身**从不显示**——列表由模板按页面语言决定
#: 只渲染其中一支（overrides/partials/nav.html），面包屑也会跳过它
#: （overrides/partials/path.html）。所以这里刻意用一个可机器识别的标记前缀，
#: 而不是会随人改动的显示名：模板靠 `"__lang:" in title` 认出语言分区。
LANG_MARKER = "__lang:"


BANNER = (
    "# ⚠️ 本文件由 tools/navgen.py 自动生成，请勿手改。\n"
    "# 顺序与显示名来自同目录 index.md 的 YAML 前置元数据（nav / nav_label / title）。\n"
    "# 重新生成： uv run python tools/navgen.py\n"
)


# ── 前置元数据 ────────────────────────────────────────────────────────────

def read_front_matter(path: Path) -> dict:
    """读取 Markdown 文件的 YAML 前置元数据；没有则返回空字典。"""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        data = yaml.safe_load(text[3:end])
    except yaml.YAMLError as exc:
        raise SystemExit(f"{path}: 前置元数据不是合法 YAML：{exc}") from exc
    return data if isinstance(data, dict) else {}


def first_h1(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def nav_hidden(md: Path) -> bool:
    """该页是否声明要从导航里隐去（前置元数据 nav_hidden: true）。

    用于那些「由页面内链与页脚到达、但不占一格导航」的页，例如标签页——
    本站分区已有十一格标签，再塞一格会把标签栏挤成横向滚动。
    """
    return bool(read_front_matter(md).get("nav_hidden"))


def nav_label(md: Path) -> str:
    """该页在**上一级**导航里显示的名字。"""
    fm = read_front_matter(md)
    for key in ("nav_label", "title"):
        value = fm.get(key)
        if value:
            return str(value)
    return first_h1(md) or md.stem


# ── 树根与分区 ────────────────────────────────────────────────────────────

def lang_dirs_under(base: Path) -> tuple[Path, ...]:
    """base 下的语言目录（一个目录里不会有它自己的语言分区以外的语言目录）。"""
    return tuple(base / lang for lang in other_languages() if (base / lang).is_dir())


def trees() -> list[tuple[Path, list[tuple[str, Path]]]]:
    """(树根, 该树根末尾要挂的分区)。

    一棵树 = 一个「导航顺序的辖区」。站根之外，每个语言目录都是一棵独立的树，
    各自有一份 .nav.yml。
    """
    out: list[tuple[Path, list[tuple[str, Path]]]] = []
    if not DOCS.is_dir():
        return out

    root_langs = lang_dirs_under(DOCS)
    out.append((DOCS, [(LANG_MARKER + d.name, d) for d in root_langs]))
    for directory in root_langs:
        out.append((directory, []))
    return out


def discover(directory: Path, *, excluded: tuple[Path, ...]) -> list[Path]:
    """目录的直接子项：带 index.md 的子目录、以及除 index.md 外的 .md 文件。

    下划线或点开头的名字视为不参与导航（草稿、片段、生成物）。
    语言分区被排除，改由 build_nav 单独挂在末尾——
    它的显示名与显示时机由模板按页面决定。
    """
    found: list[Path] = []
    for entry in sorted(directory.iterdir()):
        if entry.name.startswith((".", "_")):
            continue
        if entry.is_dir():
            if entry in excluded:
                continue
            index = entry / "index.md"
            if index.exists() and not nav_hidden(index):
                found.append(entry)
        elif entry.is_file() and entry.suffix == ".md" and entry.name != "index.md":
            found.append(entry)
    return found


def key_of(entry: Path) -> str:
    """该子项在 `nav:` 列表里被引用的名字。"""
    return entry.name[:-3] if entry.is_file() else entry.name


def order_children(directory: Path, fm: dict, *,
                   excluded: tuple[Path, ...]) -> tuple[list[Path], list[str]]:
    """按 index.md 的 `nav:` 排序，未列出的按文件名排在后面。"""
    available = {key_of(e): e for e in discover(directory, excluded=excluded)}
    ordered: list[Path] = []
    warnings: list[str] = []

    for name in fm.get("nav") or []:
        key = str(name)
        if key not in available:
            warnings.append(f"{rel(directory)}: nav 中的 “{key}” 不存在，已跳过")
            continue
        ordered.append(available.pop(key))

    if available:
        warnings.append(
            f"{rel(directory)}: {'、'.join(available)} 未在 nav 中列出，已按文件名排在末尾"
        )
        ordered.extend(available.values())

    return ordered, warnings


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


# ── 生成 ──────────────────────────────────────────────────────────────────

def build_nav(directory: Path, partitions: list[tuple[str, Path]]) -> tuple[list, list[str]]:
    """构造一个目录的 nav 列表。"""
    index = directory / "index.md"
    fm = read_front_matter(index)
    excluded = tuple(path for _, path in partitions)
    children, warnings = order_children(directory, fm, excluded=excluded)

    nav: list = []
    if index.exists():
        # 目录自身的入口页；被 navigation.indexes 折叠成分区标题后通常不显示
        nav.append({nav_label(index): "index.md"})

    for child in children:
        if child.is_dir():
            nav.append({nav_label(child / "index.md"): child.name})
        else:
            nav.append({nav_label(child): child.name})

    # 语言分区挂在树末尾，具体显示哪一支由模板按页面决定
    # （见 overrides/partials/nav.html 与 tabs.html）。
    # ⚠️ 标题带标记前缀：模板靠它认出这类分区，并在只该渲染一支时跳过其余。
    for marker, path in partitions:
        nav.append({marker: path.name})

    if not nav:
        warnings.append(f"{rel(directory)}: 没有可导航的内容")

    return nav, warnings


#: 看起来像数字的版本 id（`0100`、`100`）要**加引号**再写进 YAML。
#: ⚠️ 不加会以一句 `nav must be a list` 让整个构建失败，而报错指不到这里：
#:    YAML 把光秃秃的 `0100` 解析成数字，awesome-nav 拿到手的是数字而不是
#:    「目录名」字符串，于是找不到那棵树，往回退成一个标量，
#:    校验 `nav` 时才发现它不是列表。诡异之处在于**只有一部分版本号中招**：
#:    `080`/`091` 里的 8、9 不是八进制数字，YAML 不认它是数，于是原样留着字符串、
#:    构建正常；`060`/`0100` 只含 0-7，YAML 认它是数，构建就红。
#:    「版本号换个数字就坏」是这里踩的坑，所以引号是**无条件**加的。
_NUMERIC_RE = re.compile(r"^[0-9]+[0-9_]*$")


def _quote_numeric_values(body: str) -> str:
    """把 nav 里那些「长得像数字」的值逐个加上引号。"""
    out: list[str] = []
    for line in body.split("\n"):
        match = re.match(r"^(\s*-\s*.*?:\s*)(\S+)\s*$", line)
        if match and _NUMERIC_RE.match(match.group(2)):
            line = f"{match.group(1)}'{match.group(2)}'"
        out.append(line)
    return "\n".join(out)


def render(nav: list) -> str:
    body = yaml.safe_dump(
        {"nav": nav},
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=4096,
    )
    body = _quote_numeric_values(body)
    if yaml.safe_load(body) != {"nav": nav}:
        # 加引号万一改了语义，宁可原样写出去——但那就得有人去看。
        raise SystemExit("navgen: 加引号之后 YAML 读回来不是同一份，先查 render()")
    return BANNER + body


def targets() -> list[tuple[Path, list[tuple[str, Path]]]]:
    """需要生成 .nav.yml 的目录：每棵树根，以及它下面每个含 index.md 的目录。

    子目录（非树根）不挂分区——分区只在树根这一层表达语言的横向切换。

    两处要当心：

    1. **不能在站根的 rglob 里走进别的树。** 站根那一次遍历沿着整个 docs/ 往下，
       会顺手把 `docs/en/`、`docs/zh-hant/` 这些**别的树根**也收进来，而且是以
       「没有分区」的样子收的——于是同一个目录被排两遍，后一遍（空分区）
       盖掉前一遍，`en/.nav.yml` 里的顺序就没了，而它看上去只是一份
       普通的 .nav.yml。所以遍历时要把别的树根整个剪掉。
    2. **还没有内容的语言树也必须给一份空的。** 某个语种可能一篇都没翻
       （读者由跳转桩送走），那里只剩一个 index.html 桩。⚠️ 这时候**恰恰不能跳过**：
       awesome-nav 找不到 .nav.yml 就自己去扫目录，扫到一个 html 也没有的目录，
       会把 nav 解析成非列表并以 `nav must be a list` 让整个构建失败——
       报错点在主题里，看不出是这个语种缺文件。空目录写一份空清单，
       构建才过得去（`nav: []` 是合法取值）。
    """
    roots = trees()
    all_roots = [base for base, _ in roots]
    out: list[tuple[Path, list[tuple[str, Path]]]] = []
    for base, partitions in roots:
        if not base.is_dir():
            continue
        # 有子目录（语言分区）就一定要留骨架；否则至少要有一篇内容或一个跳转桩。
        if partitions or (base / "index.md").exists() or (base / "index.html").exists():
            out.append((base, partitions))
        others = [r for r in all_roots if r != base]
        for index in sorted(base.rglob("index.md")):
            directory = index.parent
            if directory == base:
                continue
            if any(other == directory or other in directory.parents for other in others):
                continue
            out.append((directory, []))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="从文件树生成 .nav.yml")
    parser.add_argument(
        "--check",
        action="store_true",
        help="只比对，不写盘；有差异时以非零码退出（可挂在构建流程里）",
    )
    args = parser.parse_args()

    changed: list[Path] = []
    warnings: list[str] = []
    wanted: set[Path] = set()
    planned = targets()

    for directory, partitions in planned:
        nav, warns = build_nav(directory, partitions)
        warnings.extend(warns)
        content = render(nav)
        target = directory / ".nav.yml"
        wanted.add(target)
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == content:
            continue
        changed.append(target)
        if not args.check:
            target.write_text(content, encoding="utf-8")

    # 上一次生成、这次不再需要的 .nav.yml。文档树一旦挪动或合并，旧目录会
    # 留下一个没人认领的导航文件（docsgen 的 prune 只管 .md），空目录随即
    # 出现在构建树里，让人以为那个分区还在。判据与 docsgen 一致：只认带
    # 生成横幅的文件，手写的不动。
    stale: list[Path] = []
    if not args.check:
        for path in sorted(DOCS.rglob(".nav.yml")):
            if path in wanted or BANNER not in path.read_text(encoding="utf-8"):
                continue
            stale.append(path)
            path.unlink()
            directory = path.parent
            while directory not in (DOCS, ROOT) and directory.exists() and not any(directory.iterdir()):
                directory.rmdir()
                directory = directory.parent

    for warning in warnings:
        print(f"warn: {warning}", file=sys.stderr)

    verb = "需要更新" if args.check else "已更新"
    print(f"{verb} {len(changed)} 个 .nav.yml"
          + (f"（共检查 {len(planned)} 个目录）" if changed else ""))
    for path in changed:
        print(f"  {rel(path)}")
    if stale:
        print(f"已删除 {len(stale)} 个失效的 .nav.yml")
        for path in stale:
            print(f"  {rel(path)}")

    return 1 if (args.check and (changed or stale)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
