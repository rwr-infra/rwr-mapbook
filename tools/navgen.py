#!/usr/bin/env python3
"""从文件树生成导航文件（.nav.yml）。

设计前提
--------
导航的唯一来源是内容本身，不再手工维护一份导航配置：

* **顺序**来自各目录 index.md 的 `nav:` 列表（列出该目录的子项名字）；
* **显示名**优先取该页的 `nav_label`，其次 `title`，再次首个一级标题；
* 顶层目录的顺序来自 `docs/index.md` 的 `nav:`。

也就是说：一个文件夹的全部导航元数据，就写在它自己的 index.md 里。

两种「分区」
------------
本站的导航树是**一棵**（Zensical 的 nav 是全站唯一的），而语言与版本各自需要
独立的顺序。做法是在树里挂一批**从不显示**的分区节点，标题带机器可识别的标记
前缀，由模板按当前页面决定渲染哪一支、跳过哪一支：

    __lang:en        语言分区（docs/en、docs/0101/en …）
    __ver:0101       版本分区（docs/0101 …）

两者可以嵌套：站根的版本分区里再挂该版本自己的语言分区。于是树形是

    docs/.nav.yml
      ├── 各内容分区                        ← 当前版 · 简体
      ├── __lang:en      → en/             ← 当前版 · 英文
      ├── __lang:zh-hant → zh-hant/        ← 当前版 · 繁体
      └── __ver:0101     → 0101/
            ├── 各内容分区                  ← 0101 版 · 简体
            ├── __lang:en      → 0101/en/
            └── __lang:zh-hant → 0101/zh-hant/

模板侧的对应逻辑在 overrides/partials/nav.html、tabs.html（只渲染当前那一支）
与 path.html（面包屑跳过这两层）里。

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
from versions import all_versions

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

#: 语言分区的标记名。语言分区本身**从不显示**——列表由模板按页面语言决定
#: 只渲染其中一支（overrides/partials/nav.html），面包屑也会跳过它
#: （overrides/partials/path.html）。所以这里刻意用一个可机器识别的标记前缀，
#: 而不是会随人改动的显示名：模板靠 `"__lang:" in title` 认出语言分区。
LANG_MARKER = "__lang:"
#: 版本分区同理。历史版在导航里同样不该占一格，读者靠页眉的版本切换器进去。
VER_MARKER = "__ver:"


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


def version_dirs() -> tuple[Path, ...]:
    """历史版的产物根（当前版在 docs/ 根，不是分区）。"""
    return tuple(DOCS / v.id for v in all_versions() if not v.current and (DOCS / v.id).is_dir())


def trees() -> list[tuple[Path, list[tuple[str, Path]]]]:
    """(树根, 该树根末尾要挂的分区)。

    一棵树 = 一个「导航顺序的辖区」。站根之外，每个语言目录、每个版本目录、
    每个版本的语言目录都是一棵独立的树，各自有一份 .nav.yml。
    """
    out: list[tuple[Path, list[tuple[str, Path]]]] = []
    if not DOCS.is_dir():
        return out

    root_langs = lang_dirs_under(DOCS)
    versions = version_dirs()
    out.append((DOCS, [(LANG_MARKER + d.name, d) for d in root_langs]
                       + [(VER_MARKER + d.name, d) for d in versions]))
    for directory in root_langs:
        out.append((directory, []))

    for version_dir in versions:
        langs = lang_dirs_under(version_dir)
        out.append((version_dir, [(LANG_MARKER + d.name, d) for d in langs]))
        for directory in langs:
            out.append((directory, []))

    return out


def discover(directory: Path, *, excluded: tuple[Path, ...]) -> list[Path]:
    """目录的直接子项：带 index.md 的子目录、以及除 index.md 外的 .md 文件。

    下划线或点开头的名字视为不参与导航（草稿、片段、生成物）。
    语言分区与版本分区被排除，改由 build_nav 单独挂在末尾——
    它们的显示名与显示时机由模板按页面决定。
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

    # 语言分区与版本分区挂在树末尾，具体显示哪一支由模板按页面决定
    # （见 overrides/partials/nav.html 与 tabs.html）。
    # ⚠️ 标题带标记前缀：模板靠它认出这两类分区，并在只该渲染一支时跳过其余。
    for marker, path in partitions:
        nav.append({marker: path.name})

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


def targets() -> list[tuple[Path, list[tuple[str, Path]]]]:
    """需要生成 .nav.yml 的目录：每棵树根，以及它下面每个含 index.md 的目录。

    子目录（非树根）不挂分区——分区只在树根这一层表达「语言 / 版本」的横向切换。

    两处要当心：

    1. **不能在站根的 rglob 里走进别的树。** 站根那一次遍历沿着整个 docs/ 往下，
       会顺手把 `docs/archive/`、`docs/en/` 这些**别的树根**也收进来，而且是以
       「没有分区」的样子收的——于是同一个目录被排两遍，后一遍（空分区）
       盖掉前一遍，`archive/.nav.yml` 里的语言分区就没了，而它看上去只是一份
       普通的 .nav.yml。所以遍历时要把别的树根整个剪掉。
    2. **没有页面的树不必有导航。** 历史版的某个语种可能一篇内容都没有
       （读者由跳转桩送走），那里写一份空的 .nav.yml 只是噪声，还会每次都
       warn 一行，把真正的告警淹掉。
    """
    roots = trees()
    all_roots = [base for base, _ in roots]
    out: list[tuple[Path, list[tuple[str, Path]]]] = []
    for base, partitions in roots:
        if not base.is_dir():
            continue
        if partitions or (base / "index.md").exists():
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
