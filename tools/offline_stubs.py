#!/usr/bin/env python3
"""离线包：把 docsgen 的跳转桩从「目录式」补成「.html 式」。

为什么需要这一步
----------------
tools/docsgen.py 给「旧版里缺的那些页」写跳转桩，落点是

    docs/egg/settings/map-settings/index.html         ← 目录式

那是按**线上**的地址形状定的（线上 use_directory_urls 开着，页址是 `…/map-settings/`）。
而离线版必须把它关掉（file:// 下面浏览器不会把 `prepare/` 解析到 `prepare/index.html`），
页址变成 `…/map-settings.html`。于是版本切换器指向 `egg/settings/map-settings.html`，
桩却还在 `…/map-settings/index.html`——差一层，file:// 下点过去就是「文件不存在」。

桩的落点没法按构建方式分岔：两版**共用同一棵 docs/**，生成期不知道这一份要拿去做什么。
所以这一步做在**构建之后**，只动离线产物：给每个桩**补**一份同内容的 `<名字>.html`，
把里面的跳转目标由目录改写成该目录的 `index.html`。

⚠️ 是**补**，不是搬。实测两种链法都会出现，而它们要的是不同的形状：

    prepare/index.html  →  ../egg/prepare/index.html      ← 目录式（zencical 的 | url 加的）
    settings/map-settings.html  →  ../egg/settings/map-settings.html   ← .html 式

两种都留着，两种就都落地；少一份就是一处死链。多出来的那 60 个文件每个几百字节。

判据是桩自己那行生成横幅（`<!-- ⚠️ 由 tools/docsgen.py …`），不是文件名：
名字看不出哪一页是桩、哪一页是真页面。

    uv run python tools/offline_stubs.py site-offline
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

#: 与 docsgen 的 STUB_OWNED_RE 同一前缀：这一份是生成物，不是手写页面。
MARK = "<!-- ⚠️ 由 tools/docsgen.py"

REFRESH = re.compile(r'(content="0;\s*url=)(?P<target>[^"]*)(")')
CANON = re.compile(r'(<link rel="canonical" href=")(?P<target>[^"]*)(")')


def relocate(target: str, old_dir: Path, new_dir: Path) -> str:
    """把「从 old_dir 看过去是 target」改写成「从 new_dir 看过去是什么」。

    桩的目标是**目录**（`../../` 这种），换成 `.html` 式之后要落到那个目录的
    index.html 上：相对路径照旧算，尾巴补上 `index.html`。
    """
    if target.startswith(("http:", "https:", "//", "#")):
        return target
    where = os.path.normpath(os.path.join(old_dir, target))
    relative = os.path.relpath(where, new_dir)
    return ("" if relative == "." else relative + "/") + "index.html"


def convert(path: Path, root: Path) -> Path:
    """给一个桩补出 `.html` 版，返回新文件的路径。"""
    html = path.read_text(encoding="utf-8")
    old_dir, new_dir = path.parent, path.parent.parent
    for pattern in (REFRESH, CANON):
        html = pattern.sub(
            lambda m: m.group(1) + relocate(m.group("target"), old_dir, new_dir) + m.group(3),
            html,
        )
    target = new_dir / (path.parent.name + ".html")
    target.write_text(html, encoding="utf-8")
    return target


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"error: 找不到 {root}", file=sys.stderr)
        return 1

    stubs = [p for p in sorted(root.rglob("index.html"))
             if MARK in p.read_text(encoding="utf-8", errors="replace")[:400]]
    for stub in stubs:
        convert(stub, root)

    print(f"离线包跳转桩：{len(stubs)} 个各补了一份 .html 式（原来的目录式留着）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
