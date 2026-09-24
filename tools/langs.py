#!/usr/bin/env python3
"""语言清单：从 content/ 的文件名后缀推导，避免各处各写一份。

语言代码用**文字**标签（`zh-hans` / `zh-hant`），不用 `zh-CN` / `zh-TW` 这类
**地区**标签。地区标签会把用词一起改掉（激光→雷射、链接→連結），那是替读者
选定了某一地的用法；本站不做这个选择。
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

#: 默认语言，产物直接落在 docs/ 根，网址没有前缀。
DEFAULT_LANG = "zh-hans"

#: 派生语言：目标语言 → 源语言。这些语言没有手写源文件，由源语言**脚本转换**而来
#: （见 tools/hant.py），所以不算「declared」，但同样是本站的一种语言。
DERIVATIONS: dict[str, str] = {
    "zh-hant": "zh-hans",
}

#: 文件名语言后缀：index.zh-hans.md / index.zh-hant.md / index.en.md。
#: 允许连字符形式，但只到「文字」一级——`zh-hans` 可以，`zh-cn` 不该出现。
LANG_RE = re.compile(r"^(?P<name>.+)\.(?P<lang>[a-z]{2,3}(?:-[a-z]{4})?)$")


def declared_languages() -> list[str]:
    """content/ 里实际出现过的语言，默认语言排在最前，其余按名字排序。"""
    found: set[str] = set()
    if CONTENT.is_dir():
        for path in CONTENT.rglob("*.md"):
            match = LANG_RE.match(path.stem)
            if match:
                found.add(match["lang"])
    found |= set(DERIVATIONS)
    others = sorted(found - {DEFAULT_LANG})
    return ([DEFAULT_LANG] if DEFAULT_LANG in found else []) + others


def other_languages() -> list[str]:
    """除默认语言以外的语言，也是 docs/ 下各语言子目录的名字。"""
    return [lang for lang in declared_languages() if lang != DEFAULT_LANG]


__all__ = ["ROOT", "CONTENT", "DEFAULT_LANG", "LANG_RE", "DERIVATIONS",
           "declared_languages", "other_languages"]
