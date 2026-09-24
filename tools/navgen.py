#!/usr/bin/env python3
"""从文件树生成导航文件（.nav.yml）。

设计前提
--------
导航的唯一来源是内容本身，不再手工维护一份导航配置：

* **顺序**来自各目录 index.md 的 `nav:` 列表（列出该目录的子项名字）；
* **显示名**优先取该页的 `nav_label`，其次 `title`，再次首个一级标题；
* 顶层目录的顺序来自 `docs/index.md` 的 `nav:`。

也就是说：一个文件夹的全部导航元数据，就写在它自己的 index.md 里。

生成物
------
每个含内容的目录下写一个 `.nav.yml`（以点开头，不会被当成页面构建）。
**不要手改这些文件**，改 index.md 后重跑本脚本即可。

    uv run python tools/navgen.py           # 生成
    uv run python tools/navgen.py --check   # 只检查是否有过期，不写盘
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from langs import DEFAULT_LANG, other_languages

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
#: 默认语言在 docs/ 根，其余语言各占一个子目录（docs/en、docs/zh-hant …）。
#: 这些目录不出现在默认语言的导航里，改由 build_nav 统一挂在末尾。
#: ⚠️ 只能按语言代码识别——docs/ 下每个内容分区（guide、reference…）也有 index.md，
#: 用「有 index.md」当判据会把所有分区都当成语言目录。
OTHER_LANG_DIRS = tuple(DOCS / lang for lang in other_languages() if (DOCS / lang).is_dir())

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


# ── 文件树 ────────────────────────────────────────────────────────────────

def discover(directory: Path, *, root: bool) -> list[Path]:
    """目录的直接子项：带 index.md 的子目录、以及除 index.md 外的 .md 文件。

    下划线或点开头的名字视为不参与导航（草稿、片段、生成物）。
    英文分区在根目录被排除，改由 build_nav 单独挂在末尾——
    它的显示名与显示时机由模板按页面语言决定。
    """
    found: list[Path] = []
    for entry in sorted(directory.iterdir()):
        if entry.name.startswith((".", "_")):
            continue
        if entry.is_dir():
            if root and entry in OTHER_LANG_DIRS:
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


def order_children(directory: Path, fm: dict, *, root: bool) -> tuple[list[Path], list[str]]:
    """按 index.md 的 `nav:` 排序，未列出的按文件名排在后面。"""
    available = {key_of(e): e for e in discover(directory, root=root)}
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

def build_nav(directory: Path, *, root: bool) -> tuple[list, list[str]]:
    """构造一个目录的 nav 列表。"""
    index = directory / "index.md"
    fm = read_front_matter(index)
    children, warnings = order_children(directory, fm, root=root)

    nav: list = []
    if index.exists():
        # 目录自身的入口页；被 navigation.indexes 折叠成分区标题后通常不显示
        nav.append({nav_label(index): "index.md"})

    for child in children:
        if child.is_dir():
            nav.append({nav_label(child / "index.md"): child.name})
        else:
            nav.append({nav_label(child): child.name})

    # 其它语言分区挂在默认语言树的末尾，具体显示哪一支由模板按页面语言决定
    # （见 overrides/partials/nav.html）。
    # ⚠️ 标题带 LANG_MARKER 前缀：overrides/partials/nav.html 与 path.html 靠它
    # 认出语言分区（nav 里只渲染当前语言那一支，面包屑里跳过这一层）。
    if root:
        for directory in OTHER_LANG_DIRS:
            nav.append({LANG_MARKER + directory.name: directory.name})

    if not nav:
        warnings.append(f"{rel(directory)}: 没有可导航的内容")

    return nav, warnings


def render(nav: list) -> str:
    body = yaml.safe_dump(
        {"nav": nav},
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=4096,
    )
    return BANNER + body


def targets() -> list[tuple[Path, bool]]:
    """需要生成 .nav.yml 的目录：docs 本体、docs/en，以及它们下面每个含 index.md 的目录。"""
    out: list[tuple[Path, bool]] = []
    roots = [(DOCS, True), *((d, False) for d in OTHER_LANG_DIRS)]
    for base, root in roots:
        if not base.is_dir():
            continue
        out.append((base, root))
        for index in sorted(base.rglob("index.md")):
            directory = index.parent
            if directory != base:
                out.append((directory, False))
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

    for directory, root in targets():
        nav, warns = build_nav(directory, root=root)
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
    print(f"{verb} {len(changed)} 个 .nav.yml" + (f"（共检查 {len(targets())} 个目录）" if changed else ""))
    for path in changed:
        print(f"  {rel(path)}")
    if stale:
        print(f"已删除 {len(stale)} 个失效的 .nav.yml")
        for path in stale:
            print(f"  {rel(path)}")

    return 1 if (args.check and (changed or stale)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
