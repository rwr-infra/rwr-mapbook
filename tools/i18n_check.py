#!/usr/bin/env python3
"""翻译度检查器：默认语言与各语种之间的对照体检。

它回答四个问题：

1. **有没有漏翻** —— 默认语言有的篇目，某个语种有没有；
2. **有没有过期** —— 该语种是不是照着当前的默认语言版做的；
3. **结构对不对得上** —— 各语种的章节、表格、提示框、链接是否与默认语言一一对应
   （漏掉一段、少一行表格，光看字符数是看不出来的）；
4. **派生语种有没有跟上** —— 繁体不是翻译，是从简体**脚本转换**出来的，
   所以它必须**逐字节等于**对当前简体原文做一次转换的结果。

两种语种，两套判据
------------------
* **手写语种**（英文）：在该语种文件的前置元数据里记下所依据的默认语言原文指纹
      source_sha256: 3f9c…      # content/guide/index.zh-hans.md 当时的 sha256
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

import yaml

from docsgen import depth_of, rewrite_shared
from hant import to_hant
from langs import CONTENT, DEFAULT_LANG, DERIVATIONS, LANG_RE, ROOT, other_languages

DOCS = ROOT / "docs"
REPORT_JSON = ROOT / "i18n-report.json"
REPORT_MD = ROOT / "i18n-report.md"

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
PLACEHOLDER_RE = re.compile(r"^\s*(?:<!--.*?-->\s*)*TODO\s*$", re.S | re.I)
BANNER_RE = re.compile(r"^# ⚠️ 由 tools/docsgen\.py .*$\n?", re.M)

#: 正文里 CJK 占比超过这个值，基本可以断定没翻
CJK_UNTRANSLATED = 0.08


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
    """默认语言的源文件，按路径排序。"""
    return sorted(CONTENT.rglob(f"*.{DEFAULT_LANG}.md"))


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


def inspect_derived(source: Path, lang: str) -> dict:
    """派生语种：产物必须逐字节等于「对当前原文做一次转换」的结果。"""
    target = DOCS / lang / source.relative_to(CONTENT).with_name(
        source.name[: -len(f".{DEFAULT_LANG}.md")] + ".md").relative_to(".")
    record: dict = {
        "source": source.relative_to(ROOT).as_posix(),
        "target": target.relative_to(ROOT).as_posix(),
        "lang": lang,
        "kind": "derived",
    }

    if not target.exists():
        record["status"] = "missing"
        record["next"] = f"产物的 {lang} 版缺失；跑 make gen（docsgen 会从简体转换生成）"
        return record

    # 期望值要按 docsgen 的同一条流水线算：先补共享资产的相对层级，再转换
    base = source.parent.relative_to(CONTENT).as_posix()
    base = "" if base == "." else base
    expected = strip_banner(to_hant(rewrite_shared(
        source.read_text(encoding="utf-8"), base, depth_of(lang))))
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
]
#: 逐语言各取一页样例。语言清单来自 tools/langs.py，加一种语言不必回来改这里；
#: 样例页指向模版自带的示例内容（content/guide/），换掉示例内容时同步改这里。
for _lang in [DEFAULT_LANG, *other_languages()]:
    _prefix = "" if _lang == DEFAULT_LANG else f"{_lang}/"
    SMOKE += [
        (f"{_prefix}guide/index.html", "md-path__link", f"{_lang} 的面包屑"),
        (f"{_prefix}guide/writing/index.html", "md-footer__link--next", f"{_lang} 页脚的「下一页」"),
        (f"{_prefix}guide/writing/index.html", 'rel="prev"', f"{_lang} 的 <link rel=prev>"),
    ]

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
            fs = site / target.lstrip("/")
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

    pages: list[dict] = []
    for source in source_pages():
        for lang in languages:
            if lang in declared:
                pages.append(inspect_translation(source, lang, sync=args.sync))
            else:
                pages.append(inspect_derived(source, lang))
    pages.append(inspect_rendered_output())

    counts: dict[str, int] = {}
    for page in pages:
        counts[page["status"]] = counts.get(page["status"], 0) + 1

    todolist = [p for p in pages if p["status"] not in ("ok", "created")]

    report = {
        "generated": date.today().isoformat(),
        "languages": {"default": DEFAULT_LANG, "others": languages,
                      "derived": sorted(DERIVATIONS)},
        "summary": {
            "total": len(pages),
            "counts": {k: counts.get(k, 0) for k in ORDER if k in counts},
            "complete": not todolist,
        },
        "todo": [
            {"lang": p["lang"], "source": p["source"], "target": p["target"],
             "status": p["status"], "next": p["next"]}
            for p in todolist
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
    lines += ["", "## 待办", ""]
    if todolist:
        lines += ["| 语种 | 状态 | 文件 | 来源 | 下一步 |", "| --- | --- | --- | --- | --- |"]
        for p in todolist:
            cell = re.sub(r"\s+", " ", p["next"]).replace("|", "\\|")
            lines.append(f"| `{p['lang']}` | {LABEL[p['status']]} | `{p['target']}` | `{p['source']}` | {cell} |")
    else:
        lines.append("各语种与默认语言完全同步。")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    if not args.quiet:
        for page in todolist:
            print(f"[{page['lang']} · {LABEL[page['status']]}] {page['target']}\n    {page['next']}")

    summary = "　".join(f"{LABEL[s]} {counts[s]}" for s in ORDER if s in counts)
    print(f"\n翻译度：{summary}")
    print(f"报告：{REPORT_JSON.relative_to(ROOT)}　{REPORT_MD.relative_to(ROOT)}")

    return 0 if not todolist else 1


if __name__ == "__main__":
    raise SystemExit(main())
