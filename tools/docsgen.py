#!/usr/bin/env python3
"""从 content/ 生成构建树 docs/。

分层
----
    content/            唯一手写层，文件名带语言后缀
    docs/               构建层。.md 由本脚本产出；assets/、stylesheets/ 仍是手写的

同名不同语言后缀的文件是**同一篇**的不同语种：

    content/prepare/index.zh-hans.md  ─┐
    content/prepare/index.en.md       ─┴─ 同一篇，两个语种

产物路径
--------
语言是唯一的维度，**默认语言没有前缀**：

    默认语言 zh-hans  →  docs/<名字>.md
    其它语言          →  docs/<语言>/<名字>.md

于是简中在 /prepare/，英文在 /en/prepare/。语言的种类只在 tools/langs.py。

语言代码用**文字**标签（zh-hans / zh-hant），不用 zh-CN / zh-TW 这类**地区**标签：
地区标签会把用词一起改掉（激光→雷射、链接→連結），那是替读者选边。

派生语言
--------
繁体不是翻译，是简体的**脚本转换**，因此不单独手写，由本脚本从各版本的
`*.zh-hans.md` 派生（见 tools/hant.py）。派生意味着不可能出现「简体改了、
繁体没跟上」。派生关系定义在 tools/langs.py 的 DERIVATIONS。

跳转桩
------
不是每种语言都翻齐了：英文还差十几篇。而语言切换器出现在每一页上，
所以「别处有、这里没有」的那些页在这里补一个跳转桩
（`<meta http-equiv="refresh">`），落到该语言的首页——而不是把读者送进 404。
桩是**生成物**，带同样的横幅，`tools/linkcheck.py` 会把它的 refresh 目标
当成一条必须落地的引用去验。

共享资产
--------
`docs/assets/` 只有一份，全部版本与语言共用。content/ 里的相对链接按**内容根**
解析，落点在 assets/ 之下的就是共享资产；产物每深一层，这些链接就多补一个 `../`，
层数由 depth_of() 算。其余链接指向镜像页面，保持原样。

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


# ── 路径 ──────────────────────────────────────────────────────────────────

def split_lang(stem: str) -> tuple[str, str] | None:
    """把 `index.zh-hans` 拆成 ('index', 'zh-hans')；不是语言后缀的文件返回 None。"""
    match = LANG_RE.match(stem)
    return (match["name"], match["lang"]) if match else None


def lang_prefix(lang: str) -> str:
    """产物里该语言占的那一层（带尾斜杠，默认语言为空串）。"""
    return "" if lang == DEFAULT_LANG else f"{lang}/"


def depth_of(lang: str) -> int:
    """产物相对 docs/ 下沉几层：非默认语言一层，默认语言零层。"""
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
    """全部手写内容，按路径排序。"""
    found: list[Source] = []
    for path in sorted(CONTENT.rglob("*.md")):
        rel = path.relative_to(CONTENT)
        parts = split_lang(rel.stem)
        if not parts:
            print(f"warn: {path.relative_to(ROOT)} 没有语言后缀，已跳过", file=sys.stderr)
            continue
        stem, lang = parts
        found.append(Source(path, (rel.parent / stem).as_posix(), lang))
    return found


def has_front_matter(text: str) -> bool:
    """文件是不是以 YAML 前置元数据开头。

    ⚠️ 判据是**第一个字符**就是 `---`。文件开头多一个空行——写内容时手滑、
    或者用脚本生成时字符串带了个前导换行——前置元数据就整块不算数了：
    `nav_label` / `icon` / `description` 静默失效，页面标题退回头一个 h1，
    构建一声不吭。这一处踩过：`content/prepare/index.zh-hans.md` 因此丢了
    导航名与图标，也丢了下一条的 `hide:`（见 insert_hide）。
    """
    return text.startswith("---")


def insert_banner(text: str, source: Path, note: str = "") -> str:
    banner = BANNER_FMT.format(source=source.relative_to(ROOT).as_posix()) + note
    if has_front_matter(text):
        end = text.find("\n---", 3)
        if end == -1:
            raise SystemExit(f"{source}: 前置元数据没有闭合")
        return f"{text[: end + 1]}{banner}\n{text[end + 1:]}"
    if text[:1] in ("\n", "\r") or text.startswith("\ufeff"):
        # 只差一个空行/字节序标记：这几乎必然是意外，直接说清楚
        print(f"warn: {source.relative_to(ROOT)} 开头有空行或 BOM，"
              f"前置元数据不算数（nav_label / icon / description 都会失效）",
              file=sys.stderr)
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
    base = source.path.parent.relative_to(CONTENT).as_posix()
    base = "" if base == "." else base
    text = insert_banner(text, source.path, note)
    text = rewrite_shared(text, base, depth_of(lang))
    return convert(text) if convert else text


def output_of(name: str, lang: str) -> Path:
    return DOCS / lang_prefix(lang) / f"{name}.md"


def stub_of(name: str, lang: str) -> Path:
    """跳转桩的落点：**页面的**那个地址，不是「名字 + .html」。

    真页 `docs/a/b.md` 的网址是 `/a/b/`、产物是 `site/a/b/index.html`，
    所以桩要落在 `docs/<前缀>/a/b/index.html`——写成 `docs/<前缀>/a/b.html`
    的话，切换器给出的 `/a/b/` 就落不到它身上，等于没补。

    末段是 `index` 的名字是例外：`docs/a/index.md` 的网址是 `/a/`、
    产物是 `site/a/index.html`，桩也就落在同名位置。
    """
    base = DOCS / lang_prefix(lang)
    tail = name if name == "index" or name.endswith("/index") else f"{name}/index"
    return base / f"{tail}.html"


def stub_target(name: str, lang: str) -> str:
    """桩 → 该语言首页，写成**相对**地址。

    不用根相对（`/en/`）：站点可能挂在子路径下（GitHub Pages 的项目站就是
    `/<repo>/`），根相对会把读者送到域名根去。相对地址与站点挂在哪儿无关，
    tools/linkcheck.py 也照常逐条验它落地。

    退几层由桩自己的落点算出来，不靠数名字里的斜杠：`index` 那一层特殊，
    数斜杠会少退一层。
    """
    base = DOCS / lang_prefix(lang)
    depth = len(stub_of(name, lang).relative_to(base).parts) - 1
    return "../" * depth or "./"


def render_stub(name: str, lang: str, source_rel: str) -> str:
    """缺页的跳转桩：说明这一页还没翻，并把读者送到该语言的首页。

    用 refresh 而不是「带本站样式的说明页」，是因为桩必须**进不了导航**：
    它占着 `prepare/index.md` 这种会建分区的位置，写成页面就会被 navgen 当成
    一个真的分区。HTML 桩不参与页面树，navgen 与 awesome-nav 都看不见它。
    """
    target = stub_target(name, lang)
    title = html.escape("本页尚未翻译", quote=True)
    note = "这一页还没有这一种语言的版本。正在前往首页；若没有自动跳转，请点下面的链接。"
    return (
        "<!DOCTYPE html>\n"
        f"<!-- ⚠️ 由 tools/docsgen.py 生成，请勿手改；"
        f"它补的是「{source_rel}」缺的那一种语言的页。 -->\n"
        f'<html lang="{html.escape(lang, quote=True)}">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        f'<meta http-equiv="refresh" content="0; url={target}">\n'
        f'<link rel="canonical" href="{target}">\n'
        f"<title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"<p>{html.escape(note)}</p>\n"
        f'<p><a href="{target}">回到首页</a></p>\n'
        "</body>\n"
        "</html>\n"
    )


# ── 空侧栏 ────────────────────────────────────────────────────────────────

HIDE_NAV = "hide: [navigation]"
HIDE_TOC = "hide: [toc]"


def inert_sidebar(name: str, names: set[str]) -> bool:
    """这一页的左栏会不会是**空的**。

    左栏铺的是「当前顶层分区的其它页」。所以有两种页的左栏必然是空的：

    * 顶层页（首页，或任何直接躺在树根上的单篇）——它们没有分区；
    * **单页分区**的首页——这个分区里除它自己再没有第二篇。

    空着也是空着：左栏会实打实占掉 242px，正文被挤成 688px。
    拦掉它，正文自会铺到三分之二宽（见 partials/route.html 同款的推导思路）。

    判据放在构建层而不是各页的前置元数据里：分区里加一篇新页时，
    左栏该自己回来——写死在前置元数据里就不会，而且每加一种语言、
    每个历史版都要各写一遍。作者自己在前置元数据里写了 `hide:` 的，
    这里不覆盖（见 insert_hide）。
    """
    section, sep, _ = name.partition("/")
    if not sep:
        # 顶层页：它自己就是一颗标签，左栏没有东西可铺
        return True
    head = f"{section}/"
    return not any(n.startswith(head) and n != f"{head}index" for n in names)


def tree_names() -> dict[tuple[str, str], set[str]]:
    """每种语言里有哪几页。

    「这一页的左栏会不会是空的」要按**同一棵树**里还有没有别的页来判，
    所以这份集合是那条判据的输入。tools/i18n_check.py 复核派生语种时
    要重跑同一条流水线，也用它——判据必须只有一处，否则两边会分叉，
    而分叉的表现是构建红着、却看不出谁对。
    """
    derived_of: dict[str, set[str]] = {}
    for dst_lang, src_lang, _ in DERIVATIONS:
        derived_of.setdefault(src_lang, set()).add(dst_lang)
    found: dict[str, set[str]] = {}
    for source in sources():
        for lang in {source.lang} | derived_of.get(source.lang, set()):
            found.setdefault(lang, set()).add(source.name)
    return found


#: 一行放在**代码围栏之外**的 h2~h6。
#: 只认 `#`，不认裸 HTML 的 `<h2>`：本站的标题一律是 Markdown 写法，真写了
#: 裸 HTML 标题的页面，作者自己加 `hide: [toc]` 即可（这里不覆盖作者写的 hide）。
_SECTION_RE = re.compile(r"^#{2,6}[ \t]+\S", re.M)
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def body_without_fences(text: str) -> str:
    """去掉前置元数据与代码围栏，只留正文行。

    围栏里的 `## 这是注释` 不是标题，得排掉；否则一篇通篇代码的页面会被判成
    「有小标题」，右栏又空着占回去。前置元数据里的 `#` 是 YAML 注释，同理。
    """
    if has_front_matter(text):
        end = text.find("\n---", 3)
        text = text[end + 4:] if end != -1 else text
    kept: list[str] = []
    fence: str | None = None
    for line in text.split("\n"):
        match = _FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0] * 3
                continue
            kept.append(line)
        elif match and match.group(1).startswith(fence):
            fence = None
    return "\n".join(kept)


def has_sections(text: str) -> bool:
    """这一页有没有二级及以上标题 —— 也就是右栏有没有东西可铺。

    只靠一个 h1 成不了目录：主题的 base.html 会把唯一的 h1 剥掉
    （`{% set first = toc | first %}` 之后取 `first.children`），剩下的空目录
    照样渲染成一个「目录」标签——看着有东西，点开只有它自己，却实打实
    占掉右侧 242px。所以判据是「有没有 h2 及以下」，不是「有没有标题」。
    """
    return _SECTION_RE.search(body_without_fences(text)) is not None


def hide_sides(name: str, names: set[str], text: str) -> tuple[str, ...]:
    """这一页要收掉哪几侧栏 —— `hide:` 里那串东西的唯一判据。

    tools/i18n_check.py 复核派生语种时要重跑同一条流水线（它比对的正是产物
    逐字节相等），所以判据只能有这一处：两边各写一遍，迟早会分叉，
    而分叉的表现是构建红着、却看不出谁对。
    """
    sides: list[str] = []
    if inert_sidebar(name, names):
        sides.append("navigation")
    # 右栏是这一页的目录。没有二级及以上标题就没有目录可铺——空栏一样占地方，
    # 而且它在手机上只表现为一个点开是空的「目录」抽屉。
    if not has_sections(text):
        sides.append("toc")
    return tuple(sides)


def insert_hide(text: str, source: Path, sides: tuple[str, ...]) -> str:
    """往生成物的前置元数据里加一行，收掉会空着的侧栏。

    作者已经在源文件里写了 `hide:` 的，原样不动——那是有意为之，不是这里的推导。
    """
    if not sides:
        return text
    line = f"hide: [{', '.join(sides)}]"
    if not has_front_matter(text):
        # 没有前置元数据就加不了 hide:，这些侧栏会一直空着占地方。
        # 不在这里抛错（模版允许无前置元数据的内容），但要说出来——
        # 否则「栏怎么没藏」会变成一个找不着原因的现象。
        print(f"warn: {source.relative_to(ROOT)} 没有 YAML 前置元数据，"
              f"因此加不了 {line}（这些侧栏会是空的）", file=sys.stderr)
        return text
    end = text.find("\n---", 3)
    if end == -1:
        raise SystemExit(f"{source}: 前置元数据没有闭合")
    front = text[:end]
    if re.search(r"^hide\s*:", front, re.M):
        return text
    return f"{front}\n{line}{text[end:]}"


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
    """默认语言的首页在不在。

    缺了它，下面补跳转桩时会生成 docs/index.html → 指向 "./"，也就是指向它自己，
    读者被卡在一个无限自我跳转上；而 `index` 又正是唯一一个「桩的落点等于首页」
    的名字，所以这里只能报错，不能靠补桩兜住。
    """
    problems: list[str] = []
    if not CONTENT.is_dir():
        return problems
    home = CONTENT / f"index.{DEFAULT_LANG}.md"
    if not home.exists():
        problems.append(
            f"content/index.{DEFAULT_LANG}.md 不存在：默认语言必须有一篇首页，"
            f"它也是语言切换器的落点"
        )
    return problems


# ── 主流程 ────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="从 content/ 生成构建树 docs/")
    parser.add_argument("--check", action="store_true", help="只比对，不写盘")
    args = parser.parse_args()

    problems = collisions()
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        print("\n先把上面这些修好再生成。", file=sys.stderr)
        return 1

    previous = previously_generated()

    wanted: set[str] = set()
    changed: list[Path] = []
    errors: list[str] = []

    #: 一次算好，别在 emit 里每页重扫一遍 content/
    trees = tree_names()

    def emit(target: Path, content: str, name: str | None = None,
             lang: str | None = None, source: Source | None = None) -> None:
        if name is not None and source is not None:
            # 判据取自**源文件**：产物与源是同一份正文，而源文件在手边更直接。
            sides = hide_sides(name,
                               trees.get(source.lang, set()) | trees.get(lang or "", set()),
                               source.path.read_text(encoding="utf-8"))
            content = insert_hide(content, target, sides)
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
        target = output_of(source.name, source.lang)
        if target in seen:
            errors.append(f"{source.path} 与 {seen[target]} 都要生成 {target}")
        seen[target] = source.path
        stub_sources.setdefault(source.name, source.path.relative_to(ROOT).as_posix())
        emit(target, render(source), source.name, source.lang, source=source)

        # 由这一族语言派生的其它语言（如 zh-hans → zh-hant）
        for dst_lang, src_lang, convert in DERIVATIONS:
            if source.lang != src_lang:
                continue
            note = " " + DERIVED_BANNER.format(source_lang=src_lang)
            emit(
                output_of(source.name, dst_lang),
                render(source, out_lang=dst_lang, convert=convert, note=note),
                source.name, dst_lang, source=source,
            )

    # 每种语言手里有哪些页面。派生语种跟着源语言一起记，
    # 因为它确实会产出那一种语言的页面。
    derived_of: dict[str, set[str]] = {}
    for dst_lang, src_lang, _ in DERIVATIONS:
        derived_of.setdefault(src_lang, set()).add(dst_lang)
    have: dict[str, set[str]] = {}
    for source in entries:
        for lang in {source.lang} | derived_of.get(source.lang, set()):
            have.setdefault(lang, set()).add(source.name)

    every_name = sorted({name for names in have.values() for name in names})
    languages = [DEFAULT_LANG, *other_languages()]

    # 语言切换器出现在每一页上，所以只要「别处有、这里没有」，就要在这里补一个桩，
    # 否则切换器会把读者送进 404。逐种语言补，判据是这一种语言自己有没有那一页。
    for lang in languages:
        names = have.get(lang, set())
        base = DOCS / lang_prefix(lang)
        # `index` 是这一棵树的首页：有就正常生成，没有就在这里补一个指向
        # 「默认语言首页」的桩。绝不能按普通页那样往自己身上跳。
        if "index" not in names:
            emit(base / "index.html",
                 render_stub("index", lang, f"content/index.{DEFAULT_LANG}.md"))
        for name in every_name:
            if name == "index" or name in names:
                continue
            emit(stub_of(name, lang),
                 render_stub(name, lang, stub_sources.get(name, name)))

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
