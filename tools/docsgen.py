#!/usr/bin/env python3
"""从 content/ 生成构建树 docs/。

分层
----
    content/     唯一手写层。文件名带语言后缀：guide/index.zh-hans.md、guide/index.en.md
    docs/        构建层。.md 由本脚本产出；assets/、stylesheets/、*.html 仍是手写的

同名不同语言后缀的文件是**同一篇**的不同语种：

    content/guide/index.zh-hans.md  ─┐
    content/guide/index.en.md       ─┴─ 同一篇，两个语种

产物路径
--------
    默认语言 zh-hans  →  docs/<名字>.md
    其它语言 en       →  docs/en/<名字>.md
    其它语言 zh-hant  →  docs/zh-hant/<名字>.md

于是简中在 /guide/，英文在 /en/guide/，繁中在 /zh-hant/guide/。
默认语言是哪一个，只在 tools/langs.py 的 DEFAULT_LANG 里改。

语言代码用**文字**标签（zh-hans / zh-hant），不用 zh-CN / zh-TW 这类**地区**标签：
地区标签会把用词一起改掉（激光→雷射、链接→連結），那是替读者选边。

派生语言
--------
繁体不是翻译，是简体的**脚本转换**，因此不单独手写，由本脚本从
`content/**/*.zh-hans.md` 派生（见 tools/hant.py）。派生意味着不可能出现
「简体改了、繁体没跟上」。派生关系定义在 tools/langs.py 的 DERIVATIONS。

共享资产
--------
`docs/assets/` 只有一份，三种语言共用。content/ 里的相对链接按**内容根**解析，
落点在 assets/ 之下的就是共享资产；非默认语言的产物深一层，因此这些链接要多补
一个 `../`。其余链接指向镜像页面，保持原样即可。

    uv run python tools/docsgen.py
    uv run python tools/docsgen.py --check     # 只比对，不写盘
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path
from typing import Callable

from hant import to_hant
from langs import CONTENT, DEFAULT_LANG, DERIVATIONS, LANG_RE, ROOT

DOCS = ROOT / "docs"

#: 派生语言 → 转换函数。派生关系本身定义在 tools/langs.py，
#: 那里是「本站有哪几种语言」的唯一出处；这里只负责绑定转换实现。
DERIVED_CONVERTERS: dict[str, Callable[[str], str]] = {
    "zh-hant": to_hant,
}
DERIVATIONS = [(dst, src, DERIVED_CONVERTERS[dst]) for dst, src in DERIVATIONS.items()
               if dst in DERIVED_CONVERTERS]

#: 内容根下这些前缀指向共享资产，而不是镜像页面。
SHARED_PREFIXES = ("assets/",)

BANNER_FMT = "# ⚠️ 由 tools/docsgen.py 从 {source} 生成，请勿手改；要改请改 content/ 下的源文件。"
DERIVED_BANNER = "（本页由 {source_lang} 版脚本转换而来，不是另译）"

#: 「这一份是生成物」的判据。横幅插在前置元数据里（`#` 是 YAML 注释，不会渲染成
#: 正文），它本来就写着「这是生成的、别手改」——身份与出处是同一件事。
#: 因此不再另存一份清单（原先的 .docsgen.json）来记录哪些文件是生成的：
#: 两份记录会分叉，一份不会。与 tools/i18n_check.py 的 BANNER_RE 同一前缀。
OWNED_RE = re.compile(r"^# ⚠️ 由 tools/docsgen\.py ", re.M)

_LINK = re.compile(r'(\]\(|(?:\bsrc|\bhref)=")(?P<target>[^")\s]+)')


# ── 路径 ──────────────────────────────────────────────────────────────────

def split_lang(stem: str) -> tuple[str, str] | None:
    """把 `index.zh-hans` 拆成 ('index', 'zh-hans')；不是语言后缀的文件返回 None。"""
    match = LANG_RE.match(stem)
    return (match["name"], match["lang"]) if match else None


def depth_of(lang: str) -> int:
    """产物相对 docs/ 下沉几层。默认语言 0，其余 1。"""
    return 0 if lang == DEFAULT_LANG else 1


def is_shared(target: str, base: str) -> bool:
    """该相对链接是否指向共享资产（而非镜像页面）。"""
    if not target or target.startswith(("http://", "https://", "mailto:", "/", "#", "data:")):
        return False
    path = target.split("#", 1)[0].split("?", 1)[0]
    if not path:
        return False
    return any(posixpath.normpath(posixpath.join(base, path)).startswith(p)
               for p in SHARED_PREFIXES)


def rewrite_shared(body: str, base: str, depth: int) -> str:
    """非默认语言多下沉一层，共享资产的相对链接要多补 depth 个 `../`。"""
    if depth == 0:
        return body

    def patch(match: re.Match[str]) -> str:
        target = match["target"]
        if not is_shared(target, base):
            return match.group(0)
        return f"{match.group(1)}{'../' * depth}{target}"

    return _LINK.sub(patch, body)


# ── 生成 ──────────────────────────────────────────────────────────────────

def sources() -> list[tuple[Path, str, str]]:
    """(源文件, 名字, 语言)，按路径排序。名字是相对 content/ 的路径，含子目录。"""
    found = []
    for path in sorted(CONTENT.rglob("*.md")):
        rel = path.relative_to(CONTENT)
        parts = split_lang(rel.stem)
        if not parts:
            print(f"warn: {path.relative_to(ROOT)} 没有语言后缀，已跳过", file=sys.stderr)
            continue
        stem, lang = parts
        found.append((path, (rel.parent / stem).as_posix(), lang))
    return found


def insert_banner(text: str, source: Path, note: str = "") -> str:
    banner = BANNER_FMT.format(source=source.relative_to(ROOT).as_posix()) + note
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            raise SystemExit(f"{source}: 前置元数据没有闭合")
        return f"{text[: end + 1]}{banner}\n{text[end + 1:]}"
    return f"<!-- {banner.lstrip('# ')} -->\n\n{text}"


def render(source: Path, lang: str, *, depth: int, convert: Callable[[str], str] | None = None,
           note: str = "") -> str:
    text = source.read_text(encoding="utf-8")
    base = source.parent.relative_to(CONTENT).as_posix()
    base = "" if base == "." else base
    text = insert_banner(text, source, note)
    text = rewrite_shared(text, base, depth)
    return convert(text) if convert else text


def output_of(name: str, lang: str) -> Path:
    prefix = DOCS if lang == DEFAULT_LANG else DOCS / lang
    return prefix / f"{name}.md"


def previously_generated() -> set[str]:
    """上一次生成留下的产物：带生成横幅的 docs/**/*.md。

    取代原先的 .docsgen.json 清单——那是在文件里已经写明「这是生成物」之外，
    再单独存一份「哪些文件是生成物」，两份会分叉。手写的 docs/**/*.md 不带
    横幅，因此不会被误认领、也不会被 prune 删掉。
    """
    found: set[str] = set()
    for path in DOCS.rglob("*.md"):
        if OWNED_RE.search(path.read_text(encoding="utf-8")):
            found.add(path.relative_to(ROOT).as_posix())
    return found


def prune(previous: set[str], current: set[str]) -> list[Path]:
    """删掉上一次生成、这次不再存在的文件，并清掉空目录。"""
    removed = []
    for rel in sorted(previous - current):
        path = ROOT / rel
        if path.exists():
            path.unlink()
            removed.append(path)
    for rel in sorted(previous - current, reverse=True):
        directory = (ROOT / rel).parent
        while directory not in (DOCS, ROOT) and directory.exists() and not any(directory.iterdir()):
            directory.rmdir()
            directory = directory.parent
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="从 content/ 生成构建树 docs/")
    parser.add_argument("--check", action="store_true", help="只比对，不写盘")
    args = parser.parse_args()

    previous = previously_generated()

    current: set[str] = set()
    changed: list[Path] = []
    errors: list[str] = []

    def emit(target: Path, content: str) -> None:
        current.add(target.relative_to(ROOT).as_posix())
        existing = target.read_text(encoding="utf-8") if target.exists() else None
        if existing == content:
            return
        changed.append(target)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    seen: dict[Path, Path] = {}

    for source, name, lang in sources():
        target = output_of(name, lang)
        if target in seen:
            errors.append(f"{source} 与 {seen[target]} 都要生成 {target}")
        seen[target] = source
        emit(target, render(source, lang, depth=depth_of(lang)))

        # 由这一族语言派生的其它语言（如 zh-hans → zh-hant）
        for dst_lang, src_lang, convert in DERIVATIONS:
            if lang != src_lang:
                continue
            note = " " + DERIVED_BANNER.format(source_lang=src_lang)
            emit(
                output_of(name, dst_lang),
                render(source, lang, depth=depth_of(dst_lang), convert=convert, note=note),
            )

    stale = previous - current

    if not args.check:
        prune(previous, current)

    for warning in errors:
        print(f"error: {warning}", file=sys.stderr)

    verb = "需要更新" if args.check else "已生成"
    print(f"{verb} {len(changed)} / {len(current)} 个文件")
    for path in changed[:20]:
        print(f"  {path.relative_to(ROOT)}")
    if len(changed) > 20:
        print(f"  … 另有 {len(changed) - 20} 个")
    if stale:
        print(f"{'将删除' if args.check else '已删除'} {len(stale)} 个已失效的产物")
        for rel in sorted(stale)[:10]:
            print(f"  {rel}")

    return 1 if (args.check and (changed or stale)) else (1 if errors else 0)


if __name__ == "__main__":
    raise SystemExit(main())
