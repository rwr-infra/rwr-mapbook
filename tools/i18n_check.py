#!/usr/bin/env python3
"""翻译度检查器：默认语言与各语种之间的对照体检。

它回答五个问题：

1. **有没有漏翻** —— 默认语言有的篇目，某个语种有没有；
2. **有没有过期** —— 该语种是不是照着当前的默认语言版做的；
3. **结构对不对得上** —— 各语种的章节、表格、提示框、链接是否与默认语言一一对应
   （漏掉一段、少一行表格，光看字符数是看不出来的）；
4. **派生语种有没有跟上** —— 繁体不是翻译，是从简体**脚本转换**出来的，
   所以它必须**逐字节等于**对当前简体原文做一次转换的结果；
5. **非当前版有没有被回改** —— 非当前版是冻结的快照，它的派生语种同样要逐字节对得上。

两条轴
------
内容有**版本**与**语言**两条轴（见 tools/versions.py）。本检查器只管后者，
但两者的交集要说清楚：

* **当前版**（content/ 根）的每一篇都要求有译文；
* **非当前版**（content/versions/<id>/）是冻结快照，**不要求**译文——
  砍版那一刻它是什么样就永远是什么样，逼迫后人去补一版十年前的手册没有意义。
  但它的**派生**语种（繁体）照样要逐字节对得上：那一支是脚本算出来的，不花人力。

语种「还在补齐」怎么算
----------------------
一个语种从零翻到满是几个月的事，中途构建不可能一直红着。所以
`zensical.toml` 的 `[project.extra] translation_in_progress` 可以声明
**哪些语种还在补**。声明了的语种，它的「缺篇目 / 还是占位 / 刚建骨架」三种状态
只统计、不阻塞构建；**「已过期」「派生失同步」「未记录指纹」「结构待核」仍然阻塞**。

这条界线是刻意的：「还没翻」是**看得见**的（那页就是没有），
「翻了但原文改了」才是**看不见**的——本检查器存在的理由就是后者。
所以放宽的只是前者。补完一个语种，把它从那张名单里删掉，检查立刻回到全严。

两种语种，两套判据
------------------
* **手写语种**（英文）：在该语种文件的前置元数据里记下所依据的默认语言原文指纹
      source_sha256: 3f9c…      # content/prepare/index.zh-hans.md 当时的 sha256
  默认语言一改指纹就对不上，该页立刻报「已过期」，不需要人工维护清单。
* **派生语种**（繁体，见 tools/langs.py 的 DERIVATIONS）：没有手写源文件，
  由 tools/docsgen.py 从默认语言转换而来，因此判据是「转换结果是否与产物一致」。

输出
----
* 终端摘要
* `i18n-report.json` —— 机器 / agent 可读，含逐条状态与下一步动作
* `i18n-report.md`  —— 同一份内容的表格，便于人或 agent 直接读

退出码非零表示「还有活要干」，可以直接挂在构建流程上。

    uv run python tools/i18n_check.py            # 检查
    uv run python tools/i18n_check.py --sync     # 为缺失的译文建立骨架
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
from datetime import date
from pathlib import Path

import tomllib

import yaml

from docsgen import (apply_tags, depth_of, hide_sides, insert_hide, lang_prefix,
                     rewrite_shared, sources as docs_sources,
                     tag_index, tree_names)
from linkcheck import site_base
from hant import to_hant
from langs import CONTENT, DEFAULT_LANG, DERIVATIONS, LANG_RE, ROOT, other_languages
from versions import (ARCHIVE, Version, all_versions, current as current_version,
                      source_root, url_prefix)

DOCS = ROOT / "docs"
REPORT_JSON = ROOT / "i18n-report.json"
REPORT_MD = ROOT / "i18n-report.md"

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
PLACEHOLDER_RE = re.compile(r"^\s*(?:<!--.*?-->\s*)*TODO\s*$", re.S | re.I)
BANNER_RE = re.compile(r"^# ⚠️ 由 tools/docsgen\.py .*$\n?", re.M)

#: 正文里 CJK 占比超过这个值，基本可以断定没翻
CJK_UNTRANSLATED = 0.08

#: 「这一篇还没有译文」的三种状态。语种若被声明为「仍在补齐」，
#: 这三种状态只统计、不阻塞构建（理由见文件开头的说明）；其余状态一律阻塞。
PENDING = {"missing", "placeholder", "created"}


def in_progress_languages() -> set[str]:
    """仍在补齐的语种，来自 zensical.toml 的 [project.extra] translation_in_progress。"""
    with (ROOT / "zensical.toml").open("rb") as handle:
        config = tomllib.load(handle)
    raw = config.get("project", {}).get("extra", {}).get("translation_in_progress") or []
    return {str(x) for x in raw}


# ── 基础 ──────────────────────────────────────────────────────────────────

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_front_matter(text: str) -> tuple[dict, str]:
    """拆出 YAML 前置元数据与正文。"""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    data = yaml.safe_load(text[3:end])
    body = text[text.find("\n", end + 1) + 1 :]
    return (data if isinstance(data, dict) else {}), body


def strip_banner(text: str) -> str:
    """去掉生成器插在前置元数据里的横幅，便于逐字节比对。"""
    return BANNER_RE.sub("", text)


def cjk_ratio(body: str) -> float:
    stripped = re.sub(r"\s+", "", body)
    if not stripped:
        return 0.0
    return len(CJK_RE.findall(stripped)) / len(stripped)


def structure(body: str) -> dict:
    """结构比对用的骨架：只取与语言无关的形态特征。"""
    levels = []
    for line in body.splitlines():
        match = re.match(r"^(#+)\s", line)
        if match:
            levels.append(len(match.group(1)))
    return {
        "headings": levels,
        "tables": len(re.findall(r"^\s*\|.*\|\s*$", body, re.M)),
        "admonitions": len(re.findall(r"^\s*[!?]{3}\s", body, re.M)),
        "gridcards": len(re.findall(r"^\s*-\s{3}\s*__", body, re.M)),
        "codefences": len(re.findall(r"^\s*```", body, re.M)),
        "images": len(re.findall(r"!\[[^\]]*\]\(", body)),
        "links": sorted(m.group(1) for m in re.finditer(r"\]\(([^)\s]+)", body)),
        "htmlblocks": len(re.findall(r"^\s*<div", body, re.M)),
    }


def structure_diff(source: dict, target: dict) -> list[str]:
    problems = []
    if source["headings"] != target["headings"]:
        problems.append(f"标题层级对不上：原文 {source['headings']} / 译文 {target['headings']}")
    for key, label in (
        ("tables", "表格行"),
        ("admonitions", "提示框"),
        ("gridcards", "卡片"),
        ("codefences", "代码块"),
        ("images", "图片"),
        ("htmlblocks", "HTML 区块"),
    ):
        if source[key] != target[key]:
            problems.append(f"{label}数对不上：原文 {source[key]} / 译文 {target[key]}")
    if source["links"] != target["links"]:
        only_source = [x for x in source["links"] if x not in target["links"]]
        only_target = [x for x in target["links"] if x not in source["links"]]
        detail = []
        if only_source:
            detail.append(f"原文多出 {only_source[:3]}")
        if only_target:
            detail.append(f"译文多出 {only_target[:3]}")
        problems.append("链接不一致：" + "；".join(detail))
    return problems


# ── 对照 ──────────────────────────────────────────────────────────────────

def source_pages() -> list[Path]:
    """**当前版**的默认语言源文件，按路径排序。

    非当前版在 content/versions/ 下，是冻结快照，不参与「有没有译文」这一问；
    它们只走派生语种的比对（见 archived_pages）。
    """
    return sorted(path for path in CONTENT.rglob(f"*.{DEFAULT_LANG}.md")
                  if ARCHIVE not in path.parents)


def archived_pages() -> list[tuple[Path, Version]]:
    """非当前版的默认语言源文件，连同它所属的版本。"""
    out: list[tuple[Path, Version]] = []
    for version in all_versions():
        if version.current:
            continue
        root = source_root(version)
        if not root.is_dir():
            continue
        out += [(path, version) for path in sorted(root.rglob(f"*.{DEFAULT_LANG}.md"))]
    return out


def target_of(source: Path, lang: str) -> Path:
    """同一目录、同一名字、换语言后缀。"""
    stem = source.name[: -len(f".{DEFAULT_LANG}.md")]
    return source.with_name(f"{stem}.{lang}.md")


def inspect_translation(source: Path, lang: str, *, sync: bool) -> dict:
    """手写语种：查漏翻、过期、结构。"""
    target = target_of(source, lang)
    digest = sha256(source)
    record: dict = {
        "source": source.relative_to(ROOT).as_posix(),
        "target": target.relative_to(ROOT).as_posix(),
        "lang": lang,
        "kind": "translation",
        "source_sha256": digest,
    }

    if not target.exists():
        record["status"] = "missing"
        record["next"] = (
            f"翻译 {record['source']} → {record['target']}；"
            f"写完在前置元数据里加 source_sha256: {digest}"
        )
        if sync:
            create_stub(source, target, digest)
            record["status"] = "created"
            record["next"] = "骨架已建立，等待翻译正文"
        return record

    fm, body = split_front_matter(target.read_text(encoding="utf-8"))
    _, source_body = split_front_matter(source.read_text(encoding="utf-8"))
    recorded = str(fm.get("source_sha256") or "")
    ratio = cjk_ratio(body)
    is_placeholder = bool(PLACEHOLDER_RE.match(body.strip())) or not body.strip()
    record["recorded_sha256"] = recorded or None
    record["cjk_ratio"] = round(ratio, 4)

    problems: list[str] = []
    if not fm.get("title") or str(fm.get("title")).strip().upper() == "TODO":
        problems.append("译文缺少 title")
    if not fm.get("description"):
        problems.append("译文缺少 description")
    if lang != "zh-hant" and ratio > CJK_UNTRANSLATED and not fm.get("allow_cjk"):
        problems.append(f"正文中文字符占比 {ratio:.0%}，疑似未翻译")
    if not is_placeholder:
        problems.extend(structure_diff(structure(source_body), structure(body)))
    record["problems"] = problems

    if is_placeholder:
        record["status"] = "placeholder"
        record["next"] = (
            f"正文还是占位内容：读 {record['source']}，把正文译到 {record['target']}"
            f"（保留原有的章节结构、表格、提示框与链接），再补 title / description / translated，"
            f"并把 source_sha256 设为 {digest}"
        )
    elif not recorded:
        record["status"] = "untracked"
        record["next"] = (
            f"译文存在但没有记 source_sha256。核对内容与 {record['source']} 一致后，"
            f"在前置元数据里补上 source_sha256: {digest}"
        )
    elif recorded != digest:
        record["status"] = "stale"
        record["next"] = (
            f"原文 {record['source']} 已改动。重读源文件，更新 {record['target']}，"
            f"然后把 source_sha256 改为 {digest}"
        )
    elif problems:
        record["status"] = "partial"
        record["next"] = "；".join(problems)
    else:
        record["status"] = "ok"
        record["next"] = ""

    return record


_TAGS: dict[tuple[str, str], str] | None = None


def tags_of(version_id: str, lang: str) -> str:
    """docsgen 生成标签页时用的那份正文。只算一次，之后查表。"""
    global _TAGS
    if _TAGS is None:
        _TAGS = tag_index(docs_sources())
    return _TAGS.get((version_id, lang), "")


def inspect_derived(source: Path, lang: str, version: Version) -> dict:
    """派生语种：产物必须逐字节等于「对当前原文做一次转换」的结果。"""
    root = source_root(version)
    name = source.relative_to(root).with_name(source.name[: -len(f".{DEFAULT_LANG}.md")] + ".md")
    target = DOCS / url_prefix(version) / lang_prefix(lang) / name
    record: dict = {
        "source": source.relative_to(ROOT).as_posix(),
        "target": target.relative_to(ROOT).as_posix(),
        "lang": lang,
        "kind": "derived",
        "version": version.id,
    }

    if not target.exists():
        record["status"] = "missing"
        record["next"] = f"产物的 {lang} 版缺失；跑 make gen（docsgen 会从简体转换生成）"
        return record

    # 期望值要按 docsgen 的同一条流水线算：先补共享资产的相对层级，再转换
    base = source.parent.relative_to(root).as_posix()
    base = "" if base == "." else base
    expected = strip_banner(to_hant(rewrite_shared(
        apply_tags(source.read_text(encoding="utf-8"), tags_of(version.id, DEFAULT_LANG)),
        base, depth_of(version, lang))))
    # 构建层还会往空侧栏的页上补一行 hide: ——复核时要走同一条流水线，
    # 否则「派生失同步」会误报，而误报的修法是「跑 make gen」，
    # 跑完还是不一致，人就只能去改产物了。
    rel_name = name.with_suffix("").as_posix()
    sides = hide_sides(rel_name, tree_names().get((version.id, lang), set()),
                       source.read_text(encoding="utf-8"))
    expected = insert_hide(expected, source, sides)
    actual = strip_banner(target.read_text(encoding="utf-8"))
    if expected == actual:
        record["status"] = "ok"
        record["next"] = ""
        return record

    # 找出第一处差异，方便定位
    limit = min(len(expected), len(actual))
    pos = next((i for i in range(limit) if expected[i] != actual[i]), limit)
    record["status"] = "drift"
    record["first_diff"] = {
        "offset": pos,
        "expected": expected[max(0, pos - 30): pos + 30],
        "actual": actual[max(0, pos - 30): pos + 30],
    }
    record["next"] = (
        f"{record['target']} 与「{record['source']} 的脚本转换结果」不一致"
        f"（首处差异在第 {pos} 字符）。该文件是生成物，跑 make gen 覆盖即可；"
        f"若 make gen 之后仍不一致，说明有人改了 docs/ 下的生成物。"
    )
    return record


def create_stub(source: Path, target: Path, digest: str) -> None:
    """为缺失的译文建立骨架：沿用原文元数据，正文留待翻译。"""
    fm, _ = split_front_matter(source.read_text(encoding="utf-8"))
    stub = {
        "title": fm.get("title", source.stem),
        "description": fm.get("description", ""),
        "source_sha256": digest,
        "translated": None,
    }
    for key in ("nav_label", "nav", "icon"):
        if key in fm:
            stub[key] = fm[key]
    head = yaml.safe_dump(stub, allow_unicode=True, sort_keys=False, width=4096)
    target.write_text(
        f"---\n{head}---\n\n"
        f"<!-- TODO: 翻译自 {source.relative_to(ROOT).as_posix()} -->\n\nTODO\n",
        encoding="utf-8",
    )


#: 构建产物里必须真的出现的东西。模板里的条件一旦恒为假（例如把布尔渲染成
#: "True" 来比，而 MiniJinja 给的是小写 true），输出会**静默**少一块——不报错、
#: 不警告，只有肉眼看页面才发现。这一组断言就是给这类哑失败兜底。
#: 只在 site/ 存在时检查（CI 是 build 之后才跑；本地没构建就跳过）。
SMOKE: list[tuple[str, str, str]] = [
    ("index.html", "brand-footer", "首页的页脚品牌区"),
    # 两个切换器都挂在这一页上，少一个就说明对应的 partial 没渲染出来
    ("index.html", "md-select__link", "语言切换器 / 版本切换器的入口"),
]
#: 逐语言各取一页样例。语言清单来自 tools/langs.py，加一种语言不必回来改这里；
#: 样例页是本站的固定页，换掉内容结构时同步改这里。
for _lang in [DEFAULT_LANG, *other_languages()]:
    _prefix = "" if _lang == DEFAULT_LANG else f"{_lang}/"
    SMOKE += [
        (f"{_prefix}editor/index.html", "md-path__link", f"{_lang} 的面包屑"),
        (f"{_prefix}editor/keys/index.html", "md-footer__link--next", f"{_lang} 页脚的「下一页」"),
        (f"{_prefix}editor/keys/index.html", 'rel="prev"', f"{_lang} 的 <link rel=prev>"),
    ]
#: 非当前版的树也要真的生成出来：切换器指向它，它不在就等于切换器全是死链。
for _version in all_versions():
    if _version.current:
        continue
    SMOKE += [(f"{_version.id}/index.html", "brand-footer",
               f"非当前版 {_version.id} 的首页")]

CARD_BLOCK_RE = re.compile(r'class="grid cards"')


def card_blocks(html: str) -> list[str]:
    """把产物里每一个 `grid cards` 容器整段切出来（按 <div> 的嵌套深度收口）。

    正则切不了嵌套标签，数深度可以：从那个 div 的 `<` 起，遇到 `<div` 加一、
    遇到 `</div>` 减一，归零处就是它的结尾。
    """
    found: list[str] = []
    for match in CARD_BLOCK_RE.finditer(html):
        open_at = html.rfind("<div", 0, match.start())
        if open_at == -1:
            continue
        depth, i = 0, open_at
        while i < len(html):
            nxt_open = html.find("<div", i)
            nxt_close = html.find("</div>", i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + 4
            else:
                depth -= 1
                i = nxt_close + 6
                if depth == 0:
                    found.append(html[open_at:i])
                    break
    return found


def inspect_card_blocks() -> dict:
    """卡片索引页的「卡片有没有被拆散」体检。

    卡片是这么写的：

        <div class="grid cards" markdown>

        -   __标题__

            ---

            一句话

            [:octicons-arrow-right-24: 去读](xxx.md)

        </div>

    一旦中间那几行被当成**并列的**列表项（缩进写错、或者被别的脚本按行重排过），
    Markdown 会老老实实生成一堆**空卡片**：标题还在，分隔线、说明与链接全掉了。
    构建不报错、链接体检也查不到（那个链接压根没生成），页面上只是变成一整屏
    光秃秃的标题——这一处踩过。所以在这里按产物兜住。
    """
    site = ROOT / "site"
    record = {"source": "site/（卡片索引）", "target": "site/", "lang": "all", "kind": "cards"}
    if not site.is_dir():
        record["status"] = "ok"; record["next"] = ""; record["skipped"] = "site/ 不存在"
        return record

    problems: list[str] = []
    total = 0
    for page in sorted(site.rglob("*.html")):
        html = page.read_text(encoding="utf-8", errors="ignore")
        for block in card_blocks(html):
            items = re.findall(r"<li>(.*?)</li>", block, re.S)
            total += len(items)
            gutted = [i for i in items if "<a " not in i]
            if gutted:
                rel = page.relative_to(site).as_posix()
                problems.append(
                    f"{rel}: {len(gutted)}/{len(items)} 张卡片里没有链接"
                    f"（分隔线、说明与链接多半被拆成了并列的列表项）"
                )
    record["status"] = "drift" if problems else "ok"
    record["cards"] = total
    record["next"] = "；".join(problems[:6])
    return record


def inspect_rendered_output() -> dict:
    """对构建产物做一组「该有的东西真的在」的断言。"""
    site = ROOT / "site"
    record = {
        "source": "site/（构建产物）",
        "target": "site/",
        "lang": "all",
        "kind": "smoke",
    }
    if not site.is_dir():
        record["status"] = "ok"
        record["next"] = ""
        record["skipped"] = "site/ 不存在，跳过（先跑 make build）"
        return record

    missing = []
    for rel, needle, label in SMOKE:
        page = site / rel
        if not page.exists():
            missing.append(f"{rel} 不存在，无法检查{label}")
        elif needle not in page.read_text(encoding="utf-8"):
            missing.append(f"{rel} 缺少{label}（模板里的条件可能恒为假）")

    # 全站内部链接：把每一条 href/src 解析成绝对路径，看文件在不在。
    # 这一类 bug（模板里相对路径写错、`~ x | url` 少了括号、派生语种深一层…）
    # 已经出现过三次，而构建阶段一律不报错，只在读者点到时才 404，所以在这里兜住。
    broken: list[str] = []
    for page in sorted(site.rglob("*.html")):
        rel = page.relative_to(site).as_posix()
        base = "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
        for match in re.finditer(r'(?:href|src)="([^"]+)"', page.read_text(encoding="utf-8", errors="ignore")):
            raw = match.group(1)
            if not raw or raw[0] in "#?" or raw.startswith(("http://", "https://", "mailto:", "data:", "javascript:")):
                continue
            target = urllib.parse.urljoin(base, urllib.parse.unquote(raw.split("#")[0].split("?")[0]))
            # 绝对地址带着 site_url 的子路径前缀（子路径部署时），站点目录里没有那一段
            base_path = site_base()
            rel_target = target.lstrip("/")
            if base_path and (rel_target == base_path or rel_target.startswith(base_path + "/")):
                rel_target = rel_target[len(base_path):].lstrip("/")
            target = "/" + rel_target
            fs = site / rel_target
            if fs.is_dir():
                fs = fs / "index.html"
            if not fs.exists() and not (site / target.lstrip("/")).with_suffix(".html").exists():
                broken.append(f"{rel} → {raw}")

    if broken:
        shown = sorted(set(broken))[:8]
        missing.append(f"站内有 {len(broken)} 条内部链接取不到：" + "；".join(shown))

    record["status"] = "drift" if missing else "ok"
    record["next"] = "；".join(missing)
    return record


ORDER = ["missing", "placeholder", "created", "drift", "stale", "untracked", "partial", "ok"]
LABEL = {
    "missing": "缺失",
    "placeholder": "待翻译",
    "created": "已建骨架",
    "drift": "派生失同步",
    "stale": "已过期",
    "untracked": "未记录指纹",
    "partial": "结构待核",
    "ok": "已同步",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="检查各语种相对默认语言的完成度")
    parser.add_argument("--sync", action="store_true", help="为缺失的译文建立骨架")
    parser.add_argument("--quiet", action="store_true", help="只输出汇总")
    args = parser.parse_args()

    languages = other_languages()
    declared = set(languages) - set(DERIVATIONS)
    relaxing = in_progress_languages() & set(declared)

    current = current_version()
    if current is None:
        print("error: zensical.toml 里没有一个版本标了 current = true，"
              "先跑 uv run python tools/versions.py 看体检结果。", file=sys.stderr)
        return 1

    pages: list[dict] = []
    # 当前版：手写的译文要查漏翻 / 过期 / 结构，派生语种要查逐字节一致
    for source in source_pages():
        for lang in languages:
            if lang in declared:
                pages.append(inspect_translation(source, lang, sync=args.sync))
            else:
                pages.append(inspect_derived(source, lang, current))
    # 非当前版：冻结快照，不要求译文；但派生语种照样要逐字节对得上（那是脚本算的）
    for source, version in archived_pages():
        for lang in sorted(set(languages) & set(DERIVATIONS)):
            pages.append(inspect_derived(source, lang, version))
    pages.append(inspect_rendered_output())
    pages.append(inspect_card_blocks())

    counts: dict[str, int] = {}
    for page in pages:
        counts[page["status"]] = counts.get(page["status"], 0) + 1

    def blocks(page: dict) -> bool:
        """这一条要不要挡住构建。

        「已同步」「刚建骨架」不挡；「还没翻」在**声明为仍在补齐的语种**里也不挡
        ——那三种状态是看得见的（页面就是没有），而本检查器存在是为了那些
        看不见的：原文改了、译文还是旧的。补完一个语种就把它从
        translation_in_progress 里删掉，判据立刻回到全严。
        """
        if page["status"] in ("ok", "created"):
            return False
        if page["lang"] in relaxing and page["status"] in PENDING:
            return False
        return True

    todolist = [p for p in pages if blocks(p)]
    deferred = [p for p in pages if not blocks(p) and p["status"] not in ("ok", "created")]

    report = {
        "generated": date.today().isoformat(),
        "languages": {"default": DEFAULT_LANG, "others": languages,
                      "derived": sorted(DERIVATIONS),
                      "in_progress": sorted(relaxing)},
        "summary": {
            "total": len(pages),
            "counts": {k: counts.get(k, 0) for k in ORDER if k in counts},
            "complete": not todolist,
            "blocking": len(todolist),
            "deferred": len(deferred),
        },
        "todo": [
            {"lang": p["lang"], "source": p["source"], "target": p["target"],
             "status": p["status"], "next": p["next"]}
            for p in todolist
        ],
        "untranslated": [
            {"lang": p["lang"], "target": p["target"], "status": p["status"]}
            for p in deferred
        ],
        "pages": pages,
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 多语种报告",
        "",
        f"生成日期：{report['generated']}　·　默认语言 `{DEFAULT_LANG}`　·　"
        f"语种 {'、'.join('`' + x + '`' for x in languages)}　·　共 {len(pages)} 个条目　·　待办 {len(todolist)}",
        "",
        "| 状态 | 数量 |",
        "| --- | --- |",
    ]
    for status in ORDER:
        if status in counts:
            lines.append(f"| {LABEL[status]} `{status}` | {counts[status]} |")
    lines += ["", "## 待办（会挡住构建）", ""]
    if todolist:
        lines += ["| 语种 | 状态 | 文件 | 来源 | 下一步 |", "| --- | --- | --- | --- | --- |"]
        for p in todolist:
            cell = re.sub(r"\s+", " ", p["next"]).replace("|", "\\|")
            lines.append(f"| `{p['lang']}` | {LABEL[p['status']]} | `{p['target']}` | `{p['source']}` | {cell} |")
    else:
        lines.append("没有会挡住构建的条目。")

    lines += ["", "## 还在补的语种（只统计，不挡构建）", ""]
    if deferred:
        lines.append(f"已在 `translation_in_progress` 里声明的语种："
                     f"{'、'.join('`' + x + '`' for x in sorted(relaxing))}。")
        lines.append("")
        by_lang: dict[str, int] = {}
        for p in deferred:
            by_lang[p["lang"]] = by_lang.get(p["lang"], 0) + 1
        lines += ["| 语种 | 待译条目 |", "| --- | --- |"]
        for lang in sorted(by_lang):
            lines.append(f"| `{lang}` | {by_lang[lang]} |")
        lines.append("")
        lines.append("把某个语种翻完，从 `zensical.toml` 的 `translation_in_progress` "
                     "里删掉它，这一节就会消失、判据回到全严。")
    else:
        lines.append("没有声明任何「仍在补齐」的语种，所有条目都是全严判据。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    if not args.quiet:
        for page in todolist:
            print(f"[{page['lang']} · {LABEL[page['status']]}] {page['target']}\n    {page['next']}")

    summary = "　".join(f"{LABEL[s]} {counts[s]}" for s in ORDER if s in counts)
    print(f"\n翻译度：{summary}")
    if deferred:
        by_lang: dict[str, int] = {}
        for page in deferred:
            by_lang[page["lang"]] = by_lang.get(page["lang"], 0) + 1
        spread = "　".join(f"{lang} 待译 {n}" for lang, n in sorted(by_lang.items()))
        print(f"仍在补齐（不挡构建）：{spread}")
    print(f"报告：{REPORT_JSON.relative_to(ROOT)}　{REPORT_MD.relative_to(ROOT)}")

    return 0 if not todolist else 1


if __name__ == "__main__":
    raise SystemExit(main())
