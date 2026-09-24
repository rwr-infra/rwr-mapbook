#!/usr/bin/env python3
"""简体 → 繁体（脚本转换）。

这里做的是**文字转换**，不是翻译：把简体字转成繁体字，用词与句式一概不动。
语言代码用 `zh-hant`（文字），不用 `zh-TW` / `zh-HK` 这类**地区**标签——
地区标签会把词汇也改掉（激光→雷射、链接→連結、文件→檔案），
那是替读者选了某一地的用法，本站不做这个选择。

转换范围
--------
**引文（块引用）与正文一视同仁。** 简体树已把原始件的繁体用字转写为通行简体
（读者选简体就该看到简体，见 about/index 的记述原则），繁体树因此必须把同样的
文字转写回繁体——否则 `zh-hant` 的引文会停在简体，比原来更糟。

两处不转换
----------
1. **反引号内的内容**：那些是真实文件名，必须逐字保留。
   （否则 zhconv 会把 `签到表` 转成 `籤到表`——连繁体都转错了，
   因为它不知道这里该是「簽到」。）

另加一处：**链接与图片的目标**（`](…)`、`src=`、`href=`、裸 URL、参考式定义）。
目标里的中文是**路径**，磁盘上的文件名是简体，转换它等于把链接指向不存在的文件。
（曾如此：一个指向 `报告_2026年版.pdf` 的下载链接被转成了「報告_2026年版.pdf」，
文件实际仍叫原名，链接直接取不到。）

**但目标里的锚点（`#` 之后那一段）要转。** 本站的标题大多是中文，
`](settings.md#save说明)` 这个锚点是**标题的 id**（由 toc.slugify 生成），
而目标页的标题在繁体树里是要转写的——`## Save说明` 变成 `## Save說明`，
它的 id 也就成了 `save說明`。锚点若不跟着转，繁体树上每一条指向中文标题的
链接都会落空，而简体树上全都好好的。所以这里把路径与锚点分开：
路径原样保留，`#` 之后交给 convert_span。

另外把几个「古体异写」归一为现代通行的繁体写法。这些差异不是地区差异
（两岸三地都更常用右边那个），只是转换表偏古：
    爲→為  羣→群  啓→啟  祕→秘  峯→峰  衆→眾
像 裏/裡、賬/帳 这类**确实存在地区分歧**的字，保持转换表原样，不替读者选边。
"""

from __future__ import annotations

import re

import zhconv

#: 不能转换的「路径位」。中文出现在这些地方是文件名/网址，不是文案。
PROTECTED = re.compile(
    r"\]\([^)\n]*\)"                      # 行内链接与图片的目标
    r"|\b(?:src|href|poster)=\"[^\"]*\""  # HTML 属性里的路径
    r"|^\s{0,3}\[(?!\^)[^\]]+\]:\s*\S+"    # 参考式链接定义（⚠️ 脚注定义 [^x]: 不是路径，见下）
    r"|https?://\S+"                      # 裸 URL
    r"|\bdata-(?:photo|caption|original)=\"[^\"]*\"",
    re.M,
)

#: 转换表里偏古或前后不一致的写法，统一到现代通行繁体。
#: 这些都不是地区差异（两岸三地通用），只是正字法与一致性问题：
#:   古体异写  爲→為  羣→群  啓→啟  祕→秘  峯→峰  衆→眾
#:   同字混用  裏→裡（转换表对「这里/哪里」给裡，对「教室里」给裏，同一篇里混着）
NORMALIZE = str.maketrans({
    "爲": "為",
    "羣": "群",
    "啓": "啟",
    "祕": "秘",
    "峯": "峰",
    "衆": "眾",
    "裏": "裡",
})

#: 「签」作签署、签名、签到、多签用时是「簽」，不是「籤」（籤只用于抽籤一类）。
#: 转换表一律给「籤」，这里按下文改回来；「抽籤」保持不动。
SIGN_FIX = re.compile(r"(?<!抽)籤")

#: 逐字补漏时**必须跳过**的字：简繁同形、意思随上下文变，只能整词判断。
#: 照着转换表单字硬转会把它们改错：
#:     若干→若幹   公里→公裏   皇后→皇後   台北→臺北（这一处尚可，但同一个字
#:     在「台甫」里又该是「台」）  开采→開採（对）／风采→風采（错）
#: 词组表在这些词上是对的，所以交给它；逐字那一遍绕开这些字。
AMBIGUOUS = set("干里后复采斗云划冲占咸尽只面系板表松谷制卷卜舍重台")

#: 围栏行：```text title="…"
FENCE_RE = re.compile(r"^(\s*`{3,})(.*)$")

#: 行内链接与图片的目标（上面 PROTECTED 会整段保住），这里只把 `#` 之后的锚点
#: 捞出来转写，路径那一段原样不动。理由见文件开头「两处不转换」的补充说明。
LINK_TARGET = re.compile(r"\]\(([^)\n]*)\)")


def convert_anchors(line: str) -> str:
    """把链接目标里 `#` 之后的锚点转成繁体，路径保持不变。"""
    def patch(match: re.Match[str]) -> str:
        whole = match.group(1)
        head, sep, fragment = whole.partition("#")
        if not sep or not fragment:
            return match.group(0)
        return f"]({head}#{convert_span(fragment)})"

    return LINK_TARGET.sub(patch, line)


def _sweep_chars(chunk: str) -> str:
    """逐字补漏：把上一遍没跟上的简体字补上。

    转换表按词组切分，长句里会漏字——例如 `特别致谢` 整体转完 `别` 仍是简体，
    而单独转 `特别` 却是对的。这里对无歧义的字再扫一遍；
    歧义字见 AMBIGUOUS，一律不动。
    """
    return "".join(
        chunk[i] if ch in AMBIGUOUS else zhconv.convert(ch, "zh-hant")
        for i, ch in enumerate(chunk)
    )


def convert_span(text: str) -> str:
    """转换一段不含代码与路径的文本。

    两遍：先让词组表整段转换，再逐字补漏，最后才做异写归一——
    顺序不能反，否则补漏那遍会把归一好的 `群` `秘` `峰` 又打回 `羣` `祕` `峯`。
    """
    converted = _sweep_chars(zhconv.convert(text, "zh-hant")).translate(NORMALIZE)
    return SIGN_FIX.sub("簽", converted)


def convert_line(line: str) -> str:
    """转换一行：跳过后引号内容，以及落在「路径位」上的片段。"""
    fence = FENCE_RE.match(line)
    if fence:
        # 围栏行本身（```text title="…"）：反引号后面是语言短代码与代码块标题。
        # 不能交给 _convert_backticks——它按反引号左右分段，会把这一整行
        # 当成「行内代码」，于是代码块标题永远停在简体。
        return fence.group(1) + convert_span(fence.group(2))
    out: list[str] = []
    pos = 0
    for match in PROTECTED.finditer(line):
        out.append(_convert_backticks(line[pos:match.start()]))
        out.append(match.group(0))  # 路径原样保留
        pos = match.end()
    out.append(_convert_backticks(line[pos:]))
    # 路径位整个跳过了转换，锚点因此也停在了简体；这里单独把锚点补上
    return convert_anchors("".join(out))


def _convert_backticks(chunk: str) -> str:
    parts = chunk.split("`")
    return "`".join(part if i % 2 else convert_span(part) for i, part in enumerate(parts))


def to_hant(text: str) -> str:
    """整份文件转换：逐行转写，引文与代码块一并处理。

    早先这里跳过块引用与代码块，是因为简体树还保留着原始件的繁体引文，
    转写会把它们改坏。现在简体树一律呈现简体，跳过反而会让繁体树停在简体，
    所以两道豁免都去掉了；`convert_line` 仍会保住反引号里的文件名与链接目标。
    """
    return "\n".join(convert_line(line) for line in text.split("\n"))


__all__ = ["to_hant", "convert_span", "convert_line"]
