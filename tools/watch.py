#!/usr/bin/env python3
"""盯着手写层，改了就把 `docs/` 重新生成一遍。

为什么要有它
------------
`make serve`（`zensical serve`）只盯 `docs/`——那是**生成物**目录。
于是改 `content/` 下的源文件，预览一声不响：读者以为「改了没生效」，
实际是少了「content/ → docs/」这一步。以前得自己想起来再敲一次 `make gen`。

这个脚本把这一步自动接上：轮询手写层的修改时间，一变就跑 docsgen + navgen。
`zensical serve` 会看见 `docs/` 变了，自己重建、自己刷新浏览器——两边各管一段。

盯哪些
------
  content/            唯一手写内容层（命根子）
  tools/*.py          生成器自身（改了生成器要立刻看到结果）
  zensical.toml       站点配置
  overrides/          主题模板覆盖
  docs/               里**手写的那几样**：stylesheets/、javascripts/、assets/

不盯 `docs/` 下的 .md 与 .nav.yml：那是本脚本自己生成的，盯了会自己触发自己。

用法
----
    uv run python tools/watch.py            # 前台跑，Ctrl-C 停
    make watch                              # 同上
    make serve                              # 另开一个终端跑预览（推荐两个一起开）

⚠️ 它只负责「重新生成」，不负责构建与体检：预览里看到的就是 `zensical serve`
   当场构建的那一份。要跑完整流水线（构建 + 链接体检 + 翻译度体检）用 `make build`。
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: 盯梢的根：目录整个递归看，文件只看它自己。
WATCH_DIRS = (
    ROOT / "content",
    ROOT / "overrides",
    ROOT / "docs" / "stylesheets",
    ROOT / "docs" / "javascripts",
    ROOT / "docs" / "assets",
)
WATCH_FILES = (
    ROOT / "zensical.toml",
)
#: `tools/*.py`：生成器改了也得跟上（但不盯 __pycache__）。
WATCH_GLOBS = (
    (ROOT / "tools", "*.py"),
)

#: 生成链。顺序固定：先出页面，再出导航（导航要读生成后的树）。
STEPS = (
    ["python", "tools/docsgen.py"],
    ["python", "tools/navgen.py"],
)

#: 轮询间隔。生成一次不到一秒，一秒一次足够了。
INTERVAL = 1.0


def stamp() -> float:
    """手写层里最新的一个修改时间。"""
    newest = 0.0
    for directory in WATCH_DIRS:
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                newest = max(newest, path.stat().st_mtime)
    for pattern in WATCH_GLOBS:
        directory, glob = pattern
        if directory.is_dir():
            for path in directory.glob(glob):
                newest = max(newest, path.stat().st_mtime)
    for path in WATCH_FILES:
        if path.is_file():
            newest = max(newest, path.stat().st_mtime)
    return newest


def regenerate() -> None:
    for step in STEPS:
        done = subprocess.run(step, cwd=ROOT, capture_output=True, text=True)
        if done.returncode != 0:
            # 生成器报错多半是刚写坏了一页；把原因原样打出来，别吞掉。
            sys.stdout.write(done.stdout)
            sys.stderr.write(done.stderr)
            print("✗ 生成失败，等你改好再自动重试", flush=True)
            return
    print("✓ 已重新生成 docs/（预览会自己刷新）", flush=True)


def main() -> int:
    print(f"盯着手写层，改了就跑 {' + '.join(' '.join(s) for s in STEPS)}", flush=True)
    print("停止：Ctrl-C", flush=True)
    seen = stamp()
    try:
        while True:
            time.sleep(INTERVAL)
            now = stamp()
            if now != seen:
                seen = now
                regenerate()
    except KeyboardInterrupt:
        print("\n停了。", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
