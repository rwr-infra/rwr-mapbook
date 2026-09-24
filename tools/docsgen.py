#!/usr/bin/env python3
"""从 content/ 生成构建树 docs/。

分层
----
    content/            唯一手写层。当前版内容，文件名带语言后缀
    content/versions/   历史版的冻结树，每个版本一个子目录
    docs/               构建层。.md 与跳转桩由本脚本产出；assets/、stylesheets/ 仍是手写的

同名不同语言后缀的文件是**同一篇**的不同语种：

    content/guide/index.zh-hans.md  ─┐
    content/guide/index.en.md       ─┴─ 同一篇，两个语种

产物路径
--------
两个正交的维度，**版本在前、语言在后**：

    默认语言 zh-hans、当前版       →  docs/<名字>.md
    其它语言 en、当前版            →  docs/en/<名字>.md
    默认语言 zh-hans、0101 版      →  docs/0101/<名字>.md
    其它语言 en、0101 版           →  docs/0101/en/<名字>.md

于是当前版简中在 /guide/，它的英文在 /en/guide/；0101 版简中在 /0101/guide/，
它的英文在 /0101/en/guide/。语言的种类只在 tools/langs.py，版本清单只在
zensical.toml 的 [[project.extra.version]]（见 tools/versions.py）。

语言代码用**文字**标签（zh-hans / zh-hant），不用 zh-CN / zh-TW 这类**地区**标签：
地区标签会把用词一起改掉（激光→雷射、链接→連結），那是替读者选边。

派生语言
--------
繁体不是翻译，是简体的**脚本转换**，因此不单独手写，由本脚本从各版本的
`*.zh-hans.md` 派生（见 tools/hant.py）。派生意味着不可能出现「简体改了、
繁体没跟上」。派生关系定义在 tools/langs.py 的 DERIVATIONS。

跳转桩
------
历史版是**冻结的快照**，所以它的页面集合可能与当前版对不上：当前版新加的分区，
旧版自然没有。而版本切换器出现在每一页上，从当前版的这一页切到 0101 版时，
0101 版里未必有对应页。缺的那些页在这里补一个跳转桩（`<meta http-equiv="refresh">`），
落到该版本该语言的首页——而不是把读者送进 404。桩是**生成物**，带同样的横幅，
`tools/linkcheck.py` 会把它的 refresh 目标当成一条必须落地的引用去验。

共享资产
--------
`docs/assets/` 只有一份，全部版本与语言共用。content/ 里的相对链接按**内容根**
解析，落点在 assets/ 之下的就是共享资产；产物每深一层，这些链接就多补一个 `../`，
层数由 depth_of() 算（历史版一层 + 非默认语言一层）。其余链接指向镜像页面，保持原样。

    uv run python tools/docsgen.py
    uv run python tools/docsgen.py --check     # 只比对，不写盘
"""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from hant import to_hant
from langs import CONTENT, DEFAULT_LANG, DERIVATIONS, LANG_RE, ROOT, other_languages
from versions import ARCHIVE, Version, all_versions, audit, source_root, url_prefix

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
#: 两份记录会分叉，一份不会。跳转桩是 HTML，横幅形式不同，另立一条。
#: 两条都与 tools/i18n_check.py 的 BANNER_RE 同一前缀。
OWNED_RE = re.compile(r"^# ⚠️ 由 tools/docsgen\.py ", re.M)
STUB_OWNED_RE = re.compile(r"<!-- ⚠️ 由 tools/docsgen\.py ", re.M)

_LINK = re.compile(r'(\]\(|(?:\bsrc|\bhref)=")(?P<target>[^")\s]+)')


# ── 源 ────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Source:
    """一篇手写内容：它属于哪个版本、哪种语言、叫什么名字。"""

    path: Path
    name: str
    lang: str
    version: Version

    @property
    def content_root(self) -> Path:
        return source_root(self.version)


# ── 路径 ──────────────────────────────────────────────────────────────────

def split_lang(stem: str) -> tuple[str, str] | None:
    """把 `index.zh-hans` 拆成 ('index', 'zh-hans')；不是语言后缀的文件返回 None。"""
    match = LANG_RE.match(stem)
    return (match["name"], match["lang"]) if match else None


def lang_prefix(lang: str) -> str:
    """产物里该语言占的那一层（带尾斜杠，默认语言为空串）。"""
    return "" if lang == DEFAULT_LANG else f"{lang}/"


def depth_of(version: Version, lang: str) -> int:
    """产物相对 docs/ 下沉几层：历史版一层 + 非默认语言一层。"""
    return (0 if version.current else 1) + (0 if lang == DEFAULT_LANG else 1)


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
    """产物每深一层，共享资产的相对链接就多补一个 `../`。"""
    if depth == 0:
        return body

    def patch(match: re.Match[str]) -> str:
        target = match["target"]
        if not is_shared(target, base):
            return match.group(0)
        return f"{match.group(1)}{'../' * depth}{target}"

    return _LINK.sub(patch, body)


# ── 生成 ──────────────────────────────────────────────────────────────────

def sources() -> list[Source]:
    """全部手写内容，按（版本，路径）排序。

    当前版的根是 content/ 本身，所以要显式跳过 content/versions/——
    那是历史版的地盘，不然历史版会被当成当前版的 `versions/` 分区重复生成一遍。
    """
    found: list[Source] = []
    for version in all_versions():
        root = source_root(version)
        if not root.is_dir():
            # 声明了却没有目录，由 versions.audit() 报错；这里安静跳过，
            # 免得在体检之前先抛一个 FileNotFoundError，把真正的原因盖掉。
            continue
        for path in sorted(root.rglob("*.md")):
            if version.current and ARCHIVE in path.parents:
                continue
            rel = path.relative_to(root)
            parts = split_lang(rel.stem)
            if not parts:
                print(f"warn: {path.relative_to(ROOT)} 没有语言后缀，已跳过", file=sys.stderr)
                continue
            stem, lang = parts
            found.append(Source(path, (rel.parent / stem).as_posix(), lang, version))
    return found


def insert_banner(text: str, source: Path, note: str = "") -> str:
    banner = BANNER_FMT.format(source=source.relative_to(ROOT).as_posix()) + note
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            raise SystemExit(f"{source}: 前置元数据没有闭合")
        return f"{text[: end + 1]}{banner}\n{text[end + 1:]}"
    return f"<!-- {banner.lstrip('# ')} -->\n\n{text}"


def render(source: Source, *, out_lang: str | None = None,
           convert: Callable[[str], str] | None = None, note: str = "") -> str:
    """把一篇手写内容渲染成产物。

    `out_lang` 是**产物**这一份的语言，不是源文件的语言。两者只在派生语种上不同
    （源是 zh-hans，产物是 zh-hant），但正是这一处不同决定了共享资产的相对链接
    要补几个 `../`：补错了不会报错，只会让繁体页上的每一张图 404。
    原先这里按 source.lang 算，靠模版自带的示例内容从没引用过 assets/ 才没暴露。
    """
    lang = out_lang or source.lang
    text = source.path.read_text(encoding="utf-8")
    base = source.path.parent.relative_to(source.content_root).as_posix()
    base = "" if base == "." else base
    text = insert_banner(text, source.path, note)
    text = rewrite_shared(text, base, depth_of(source.version, lang))
    return convert(text) if convert else text


def output_of(name: str, lang: str, version: Version) -> Path:
    return DOCS / url_prefix(version) / lang_prefix(lang) / f"{name}.md"


def stub_of(name: str, lang: str, version: Version) -> Path:
    """跳转桩的落点：**页面的**那个地址，不是「名字 + .html」。

    真页 `docs/a/b.md` 的网址是 `/a/b/`、产物是 `site/a/b/index.html`，
    所以桩要落在 `docs/<前缀>/a/b/index.html`——写成 `docs/<前缀>/a/b.html`
    的话，切换器给出的 `/a/b/` 就落不到它身上，等于没补。

    末段是 `index` 的名字是例外：`docs/a/index.md` 的网址是 `/a/`、
    产物是 `site/a/index.html`，桩也就落在同名位置。
    """
    base = DOCS / url_prefix(version) / lang_prefix(lang)
    tail = name if name == "index" or name.endswith("/index") else f"{name}/index"
    return base / f"{tail}.html"


def stub_target(name: str, lang: str, version: Version, has_home: bool) -> str:
    """桩 → 该版本该语言首页，写成**相对**地址。

    不用根相对（`/0101/en/`）：站点可能挂在子路径下（GitHub Pages 的项目站就是
    `/<repo>/`），根相对会把读者送到域名根去。相对地址与站点挂在哪儿无关，
    tools/linkcheck.py 也照常逐条验它落地。

    退几层由桩自己的落点算出来，不靠数名字里的斜杠：`index` 那一层特殊，
    数斜杠会少退一层。

    `has_home=False` 时该（版本 × 语言）树下**没有自己的首页**——例如某个历史版
    只写了简体。这时再退回一层，落到该版本的**默认语言**首页：宁可把读者送到
    看得懂的上一站，也不要停在一个不存在的地址上。
    """
    base = DOCS / url_prefix(version) / lang_prefix(lang)
    depth = len(stub_of(name, lang, version).relative_to(base).parts) - 1
    if not has_home:
        depth += 1
    return "../" * depth or "./"


def render_stub(name: str, lang: str, version: Version, source_rel: str, has_home: bool) -> str:
    """缺页的跳转桩：说明这一页没有该版本，并把读者送到该版本的首页。

    用 refresh 而不是「带本站样式的说明页」，是因为桩必须**进不了导航**：
    它占着 `guide/index.md` 这种会建分区的位置，写成页面就会被 navgen 当成
    一个真的分区。HTML 桩不参与页面树，navgen 与 awesome-nav 都看不见它。
    """
    target = stub_target(name, lang, version, has_home)
    title = html.escape(f"{version.label} · 本页无此版本", quote=True)
    where = "该版本的首页" if has_home else "该版本的默认语言首页"
    note = (f"这一页在「{version.label}」的这一种语言里没有对应内容。"
            f"正在前往{where}；若没有自动跳转，请点下面的链接。")
    return (
        "<!DOCTYPE html>\n"
        f"<!-- ⚠️ 由 tools/docsgen.py 生成，请勿手改；"
        f"它补的是「{source_rel}」在「{version.label}」里缺的那一页。 -->\n"
        f'<html lang="{html.escape(lang, quote=True)}">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        f'<meta http-equiv="refresh" content="0; url={target}">\n'
        f'<link rel="canonical" href="{target}">\n'
        f"<title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"<p>{html.escape(note)}</p>\n"
        f'<p><a href="{target}">{html.escape(version.label)} · 首页</a></p>\n'
        "</body>\n"
        "</html>\n"
    )


# ── 认领与清理 ────────────────────────────────────────────────────────────

def previously_generated() -> set[str]:
    """上一次生成留下的产物：带生成横幅的 docs/**/*.md 与跳转桩。

    取代原先的 .docsgen.json 清单——那是在文件里已经写明「这是生成物」之外，
    再单独存一份「哪些文件是生成物」，两份会分叉。手写的 docs/**/*.md 与
    手写的 docs/*.html 跳转桩都不带这个前缀，因此不会被误认领、也不会被
    prune 删掉。
    """
    found: set[str] = set()
    for path in DOCS.rglob("*.md"):
        if OWNED_RE.search(path.read_text(encoding="utf-8")):
            found.add(path.relative_to(ROOT).as_posix())
    for path in DOCS.rglob("*.html"):
        if STUB_OWNED_RE.search(path.read_text(encoding="utf-8")):
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


# ── 命名冲突 ──────────────────────────────────────────────────────────────

def collisions() -> list[str]:
    """版本 id 与当前版的顶层分区名撞车。

    这一条只有在生成时才知道，所以不放进 versions.audit()：历史版的产物落在
    docs/<id>/，而当前版的分区也落在 docs/<分区名>/，两者同名就会把两棵完全
    不同的树叠在一起——生成不报错，页面悄悄互相覆盖。
    """
    problems: list[str] = []
    if not CONTENT.is_dir():
        return problems

    # 每个版本都必须有自己的首页。缺了它，下面补跳转桩时会生成
    # docs/<版本>/index.html → 指向 "./"，也就是指向它自己，读者被卡在一个
    # 无限自我跳转上；而 `index` 又正是唯一一个「桩的落点等于首页」的名字，
    # 所以这里只能报错，不能靠补桩兜住。
    for version in all_versions():
        home = source_root(version) / f"index.{DEFAULT_LANG}.md"
        if not home.exists():
            where = "content/" if version.current else f"content/versions/{version.id}/"
            problems.append(
                f"版本 “{version.id}” 没有首页：{where}index.{DEFAULT_LANG}.md 不存在。"
                f"每个版本都必须有自己的一篇首页，它也是版本切换器的落点"
            )

    top_dirs = {e.name for e in CONTENT.iterdir() if e.is_dir()}
    top_pages = {split_lang(f.stem)[0] for f in CONTENT.glob("*.md") if split_lang(f.stem)}
    for version in all_versions():
        if version.current or not version.id:
            continue
        if version.id in top_dirs:
            problems.append(
                f"版本 id “{version.id}” 与 content/ 顶层的分区目录同名："
                f"docs/{version.id}/ 会被两棵树同时写入"
            )
        if version.id in top_pages:
            problems.append(
                f"版本 id “{version.id}” 与 content/ 顶层的页面同名："
                f"docs/{version.id} 既是目录又是页面"
            )
    return problems


# ── 主流程 ────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="从 content/ 生成构建树 docs/")
    parser.add_argument("--check", action="store_true", help="只比对，不写盘")
    args = parser.parse_args()

    problems = audit(DEFAULT_LANG, tuple(other_languages())) + collisions()
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        print("\n版本清单没对齐，先修好再生成。", file=sys.stderr)
        return 1

    previous = previously_generated()

    wanted: set[str] = set()
    changed: list[Path] = []
    errors: list[str] = []

    def emit(target: Path, content: str) -> None:
        wanted.add(target.relative_to(ROOT).as_posix())
        existing = target.read_text(encoding="utf-8") if target.exists() else None
        if existing == content:
            return
        changed.append(target)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    entries = sources()
    seen: dict[Path, Path] = {}
    #: 每个页面名字对应的源文件，写进桩的注释里，方便回头查它是从哪儿补的。
    stub_sources: dict[str, str] = {}

    for source in entries:
        target = output_of(source.name, source.lang, source.version)
        if target in seen:
            errors.append(f"{source.path} 与 {seen[target]} 都要生成 {target}")
        seen[target] = source.path
        stub_sources.setdefault(source.name, source.path.relative_to(ROOT).as_posix())
        emit(target, render(source))

        # 由这一族语言派生的其它语言（如 zh-hans → zh-hant）
        for dst_lang, src_lang, convert in DERIVATIONS:
            if source.lang != src_lang:
                continue
            note = " " + DERIVED_BANNER.format(source_lang=src_lang)
            emit(
                output_of(source.name, dst_lang, source.version),
                render(source, out_lang=dst_lang, convert=convert, note=note),
            )

    # 每棵树（版本 × 语言）手里有哪些页面。派生语种跟着源语言一起记，
    # 因为它确实会产出那一棵树的页面。
    derived_of: dict[str, set[str]] = {}
    for dst_lang, src_lang, _ in DERIVATIONS:
        derived_of.setdefault(src_lang, set()).add(dst_lang)
    have: dict[tuple[str, str], set[str]] = {}
    for source in entries:
        for lang in {source.lang} | derived_of.get(source.lang, set()):
            have.setdefault((source.version.id, lang), set()).add(source.name)

    every_name = sorted({name for names in have.values() for name in names})
    languages = [DEFAULT_LANG, *other_languages()]

    # 两条切换轴都出现在每一页上，所以只要「别处有、这里没有」，
    # 就要在这里补一个桩，否则切换器会把读者送进 404：
    #   * 版本轴 —— 当前版新加的分区，历史版没有；
    #   * 语言轴 —— 还没翻的篇目（含仍在补齐的语种）。
    # 逐棵树补，判据是这一棵树自己有没有那一页，而不是整个版本有没有。
    for version in all_versions():
        for lang in languages:
            names = have.get((version.id, lang), set())
            has_home = "index" in names
            base = DOCS / url_prefix(version) / lang_prefix(lang)
            # `index` 是这棵树的首页：有就正常生成，没有就在这里补一个指向
            # 「该版本默认语言首页」的桩。绝不能按普通页那样往自己身上跳。
            if not has_home:
                emit(base / "index.html",
                     render_stub("index", lang, version,
                                 f"版本 {version.id} 的首页", has_home))
            for name in every_name:
                if name == "index" or name in names:
                    continue
                emit(stub_of(name, lang, version),
                     render_stub(name, lang, version,
                                 stub_sources.get(name, name), has_home))

    stale = previous - wanted

    if not args.check:
        prune(previous, wanted)

    for warning in errors:
        print(f"error: {warning}", file=sys.stderr)

    verb = "需要更新" if args.check else "已生成"
    print(f"{verb} {len(changed)} / {len(wanted)} 个文件")
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
