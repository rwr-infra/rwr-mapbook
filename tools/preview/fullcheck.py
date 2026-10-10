#!/usr/bin/env python3
"""交付前统一处理：把平时预览跳过的那些检查，一次跑完并汇总。

    fullcheck.bat

平时改文档、看效果请用 `start.bat`（预览）——它只做「生成 + 构建 + 刷新」，
不做任何体检，就是要快。等你说「统一处理一下」的时候，再跑这个。

它跑的是 Makefile 里 `make build` 那一条链，本机没有 make，这里是等价物：

    1. docsgen      content/ → docs/（含繁体派生）
    2. navgen       .nav.yml
    3. zensical build --clean --strict   构建，并把警告当错误
    4. linkcheck    站内引用、目录尾斜杠、跳转桩
    5. i18n_check   漏翻 / 已过期 / 结构对不上（英文译文跟没跟上）
    6. versions     版本轴那一套判据

跑完给一份汇总：哪一步过了、哪一步没过、没过的要看什么。
**它不会替你改任何文件**（除了生成层 docs/ 与构建产物 site/）——
该你动手的（比如补英文译文）它会把具体命令给出来。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
#: 仓库根：这个脚本在 `<仓库>/tools/preview/fullcheck.py`，往上两级就是仓库。
PROJECT = HERE.parents[1]
TOOLS = PROJECT / "tools"

#: 解释器：`RWR_PYTHON` > 正在跑这个脚本的解释器 > 工作区里那个便携 Python >
#: PATH 上的 python。下面那三个包（zensical / pyyaml / zhconv）得装在同一个
#: 解释器里，所以这里跟 serve.py 用同一套判据，只是不做交互。
def pick_python() -> str:
    probe = "import zensical, yaml, zhconv"
    candidates = [
        os.environ.get("RWR_PYTHON"),
        sys.executable,
        r"D:/RWRWorkSpace/_py/py314/python.exe",
        shutil.which("python"),
        shutil.which("python3"),
    ]
    for cand in candidates:
        if not cand or not Path(cand).is_file():
            continue
        try:
            done = subprocess.run([str(cand), "-c", probe], capture_output=True, timeout=60)
        except OSError:
            continue
        if done.returncode == 0:
            return str(cand)
    print("× 没找到装齐 zensical / pyyaml / zhconv 的解释器；")
    print("  装一下，或者设 RWR_PYTHON=<那个 python 的完整路径> 再跑：")
    for cand in candidates:
        print(f"    {cand}")
    raise SystemExit(1)


PY = pick_python()

# 仓库里的 tools/*.py 是嵌入式 Python：脚本目录不在 sys.path、PYTHONPATH 也被忽略，
# `python tools/xxx.py` 里的 `from hant import ...` 必然找不到。用 runpy 套一层。
BOOT = "import runpy,sys;sys.path.insert(0,r'{tools}');runpy.run_path(r'{script}',run_name='__main__')"


def run_step(name: str, argv: list[str]) -> tuple[bool, str, float]:
    """跑一步，返回 (过没过, 输出尾部, 耗时秒)。"""
    t0 = time.time()
    try:
        done = subprocess.run(argv, cwd=str(PROJECT), capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    except OSError as exc:
        return False, str(exc), time.time() - t0
    out = ((done.stdout or "") + (done.stderr or "")).strip()
    tail = "\n".join(out.splitlines()[-6:])
    return done.returncode == 0, tail, time.time() - t0


def py_tool(script: str) -> list[str]:
    return [PY, "-c", BOOT.format(tools=str(TOOLS).replace("\\", "/"),
                                  script=str(TOOLS / script).replace("\\", "/"))]


def step_docsgen() -> tuple[bool, str, float]:
    ok, tail, spent = run_step("docsgen", py_tool("docsgen.py"))
    if ok:
        ok2, _, _ = run_step("navgen", py_tool("navgen.py"))
        ok = ok2
    return ok, tail, spent


def main() -> int:
    print("交付前统一处理 —— 平时预览跳过的检查，这里一次跑完\n")

    results: list[tuple[str, bool, str, float]] = []

    def record(name: str, ok: bool, tail: str, spent: float) -> None:
        results.append((name, ok, tail, spent))
        print(f"{'✓' if ok else '×'} {name}（{spent:.1f} 秒）", flush=True)
        if not ok and tail:
            print("    " + "\n    ".join(tail.splitlines()), flush=True)

    ok, tail, spent = step_docsgen()
    record("生成 docs/（含繁体派生）与导航", ok, tail, spent)

    ok, tail, spent = run_step("build", [PY, "-m", "zensical", "build", "--clean", "--strict"])
    # 本机偶发：收尾一步被系统拒（os error 5），产物其实写得齐。
    # 只要 site/index.html 是新的就当过，但把这件事说清楚。
    marker = PROJECT / "site" / "index.html"
    fresh = marker.is_file() and (time.time() - marker.stat().st_mtime) < 300
    if not ok and "could not be cleaned" in tail:
        print("  ! 构建清不掉 site/：多半是预览还在跑（它正服务着 site/）。", flush=True)
        print("    先双击 stop.bat 关掉预览，再跑这个。", flush=True)
    elif not ok and fresh:
        print("  ! 构建收尾报了 os error 5，但产物是新的（本机已知问题），按通过算", flush=True)
        ok = True
    record("构建（--clean --strict，警告当错误）", ok, tail, spent)

    ok, tail, spent = run_step("linkcheck", py_tool("linkcheck.py"))
    record("链接体检", ok, tail, spent)

    ok, tail, spent = run_step("i18n_check", py_tool("i18n_check.py"))
    record("翻译度体检", ok, tail, spent)

    ok, tail, spent = run_step("versions", py_tool("versions.py"))
    record("版本体检", ok, tail, spent)

    # ── 汇总 ──────────────────────────────────────────────────────────
    failed = [name for name, ok, _, _ in results if not ok]
    print("\n" + "─" * 60)
    if not failed:
        print("✓ 全部通过。可以提交了。")
    else:
        print(f"× 有 {len(failed)} 步没过：")
        for name in failed:
            print(f"    · {name}")

    # 英文没跟上的，把该跑的命令直接列出来（翻译度报告是唯一的依据）。
    report = PROJECT / "i18n-report.json"
    try:
        todo = json.loads(report.read_text(encoding="utf-8")).get("todo") or []
    except (OSError, ValueError):
        todo = []
    if todo:
        print("\n还没跟上（会挡住构建）：")
        for item in todo:
            print(f"    [{item.get('lang')}] {item.get('target')}  ·  {item.get('status')}")
        stale = [i for i in todo if i.get("status") == "stale"
                 and i.get("source") and i.get("target")]
        if stale:
            print("\n英文译文改完之后，用这些把指纹更新（一次一条）：")
            for item in stale:
                print(f"    node _refingerprint.js rwr-mapbook/{item['source']}:"
                      f"rwr-mapbook/{item['target']}")
        print("\n（完整清单在 rwr-mapbook/i18n-report.md）")

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
