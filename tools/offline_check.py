#!/usr/bin/env python3
"""离线包体检：站内引用与锚点在 file:// 下是不是都落在真实文件上。

为什么不能直接用 tools/linkcheck.py
-----------------------------------
linkcheck 假定的是**线上那份产物**：directory-style 地址（`…/page/`）、跳转桩在
`<目录>/index.html`、链接以 `/` 或相对路径拼。而 `make offline` 出来的整站是
`.html` 式地址（file:// 下浏览器不会把 `guide/` 解析到 `guide/index.html`，
所以 offline 插件把 use_directory_urls 关掉了）。拿线上那套判据去量离线版，
只会满屏假警报——所以这里另写一遍，**判据只有一条且与线上相同：每条站内引用都得落地**。

它同时补上 linkcheck 没有的那一半：**锚点**。离线包里页内跳转很多（目录、脚注、
「回到顶部」），锚点落空在浏览器里表现为「点了没反应」，不明显，也不报错。

    uv run python tools/offline_check.py            # 默认查 site-offline/
    uv run python tools/offline_check.py <目录>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

#: href/src 的取值。HTML 里的引号都是双引号（主题与本模版都这么写），
#: 单引号那一支不值得为它把正则放宽——放宽之后会把正文里的引号也当链接。
REF = re.compile(r'(?:href|src)="([^"]+)"')
ID = re.compile(r'\sid="([^"]+)"')

#: 不归本脚本管的引用：外部地址、数据、脚本伪协议、以及页内锚点。
SKIP = ("http:", "https:", "//", "data:", "mailto:", "javascript:", "blob:")


def check(root: Path) -> tuple[list[str], list[str], int, int]:
    """返回（落空的引用，落空的锚点，页面数，引用总数）。"""
    pages = sorted(root.rglob("*.html"))
    missing: list[str] = []
    anchors: list[str] = []
    total = 0

    for page in pages:
        html = page.read_text(encoding="utf-8", errors="replace")
        for raw in REF.findall(html):
            if not raw.strip() or raw.startswith(SKIP):
                continue
            total += 1
            path, _, frag = raw.partition("#")
            # `#top` 是 HTML 规范里的特例：页面上没有 id="top" 也照样滚到顶部，
            # 主题的「回到顶部」用的就是它。线上版同样如此，不是离线版的问题。
            if path == "" and frag == "top":
                continue
            target = Path(page if not path else page.parent / unquote(path))
            if not target.exists():
                missing.append(f"{page.relative_to(root)} → {raw}")
                continue
            if frag and target.is_file():
                text = target.read_text(encoding="utf-8", errors="replace")
                if frag not in set(ID.findall(text)):
                    anchors.append(f"{page.relative_to(root)} → {raw}")
    return missing, anchors, len(pages), total


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "site-offline").resolve()
    if not root.is_dir():
        print(f"error: {root} 不存在——先跑 `make offline`", file=sys.stderr)
        return 1

    missing, anchors, pages, total = check(root)
    for label, rows in (("找不到的引用", missing), ("找不到的锚点", anchors)):
        if rows:
            head = sorted(set(rows))
            print(f"\n{label}：{len(rows)} 条")
            for row in head[:25]:
                print("  ", row)
            if len(head) > 25:
                print(f"   … 另有 {len(head) - 25} 种")

    print(f"\n离线包体检：{pages} 个页面、{total} 处引用，"
          f"落地的 {total - len(missing)} 处；锚点落空 {len(anchors)} 处")
    if missing or anchors:
        print("离线包里有打不开的东西，先修再发。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
