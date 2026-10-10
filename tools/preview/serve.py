#!/usr/bin/env python3
"""rwr-mapbook 本地热更新预览：改 content/ 存盘，浏览器自己刷新。

    双击 start.bat                 或         python serve.py
    浏览器打开 http://127.0.0.1:8000/         停止：Ctrl-C（或关掉那个黑窗口）

它干什么
--------
  手写层（content/、overrides/、docs 下手写那几样、tools/*.py、zensical.toml）
      │  变了
      ▼
  docsgen + navgen（content/ → docs/）→ 让常驻的构建器只重建变了的那几页
      │                                   → 版本号 +1
      ▼
  页面里注入的那段 JS 常驻 SSE 连接，版本号一变就换掉 <article>

为什么是「常驻构建器」而不是每轮一次 `zensical build`
----------------------------------------------------
`zensical build` **没有增量能力**：连着跑两次、第二次什么都没改，实测一样 3.3 秒
（827 个产物、53 MB 整个重来一遍）。而 `zensical serve` 是常驻的，它记住上一轮的
状态，改一页只重写那几十个文件——实测 **0.15 秒**（site/ 里只有 42/851 个文件被重写）。
两者差 20 倍，这就是预览快慢的全部秘密。

所以这里默认：起一个 `zensical serve` 子进程当构建器（跑在一个内部端口上，只让它
写 `site/`），HTTP 服务与浏览器刷新仍归本脚本自己管——子进程只管构建，页面这一头
一个字都没让出去。子进程起不来（本机有过 `os error 5` 的记录）就自动退回原来的
「每轮跑一次 zensical build」，慢一点，但一样能用。

一轮下来各段实测（改一个 content/ 文件）：
    轮询发现改动    0～0.25 秒   （tools/watch.py 的 INTERVAL，原来 1 秒）
    等编辑器写完    0.15 秒      （原来是固定 0.8 秒）
    docsgen+navgen  0.6 秒       （本来就绕不过）
    重建            0.15 秒      （原先是全量 3.4 秒）
    ────────────────────────
    合计            ≈1.1 秒      （原来约 6.4 秒）

顺手去掉的两笔冤枉时间：
  · 每轮 `rmtree(.cache)`：清缓存只让构建更慢（实测 4.0 秒 vs 3.3 秒），且毫无收益；
  · 每轮把 docs/en、docs/zh-hant 挪出去再挪回来：实测省不下时间（3.35 vs 3.29 秒），
    却让预览里的英文页/繁体页 404。现在三种语言的产物都在，随便点。

为什么不用 `make serve` + `make watch`
--------------------------------------
这台机器上那条路走不通，几个坑分别绕开：

  1. 没有 make；`uv run` 会拉 Python 3.15，pyyaml 6.0.3 没对应 wheel、要现场编译，
     本机缺 MSVC，装不上；
  2. 可用的 `_py/py314` 是**嵌入式发行版**（带 python314._pth）：既不放脚本目录进
     sys.path，也忽略 PYTHONPATH，于是 `python tools/docsgen.py` 里的
     `from hant import ...` 必然找不到。这里用 runpy 套一层显式塞 sys.path；
  3. `zensical serve` 只盯 `docs/`，改 `content/` 它一声不响——这一步由本脚本的
     监视线程接上（清单来自 tools/watch.py，判据不另抄一份）。
     ⚠️ 另外它**不带浏览器自动刷新**（发出来的 HTML 里没有任何 livereload 代码），
     所以「服务 + 刷新」这两件仍然由本脚本自己来。

`zensical build` 在这台机器上有个怪脾气：同样的命令，有时 2.5 秒全绿，有时跑
50 多秒然后 `拒绝访问 (os error 5)`——像是杀软/索引器在扫刚写出的 850+ 个文件
时把文件锁了。常驻构建器这条路通常碰不上（它只写变了的几十个文件）；万一真退回
全量那条路，就自适应：失败就等一等再来（最多四轮），产物变新了也照常刷新。

它只读手写层、只写生成物：`docs/`（生成物）、`site/`、`.cache/` 都在 `.gitignore` 里，
正文与模板一个字都不会动。要跑构建 + 链接体检 + 翻译度体检的完整流水线，
用 `make build`，或者本目录的 `fullcheck.bat`。

⚠️ 构建这一步是省不掉的（除非退化成全量，那更慢）。改完存盘稍等一秒左右，
   页面动了才说明这一轮走完。
"""

from __future__ import annotations

import argparse
import atexit
import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import queue
import threading
import time
import webbrowser
from pathlib import Path

WORKSPACE = Path(r"D:/RWRWorkSpace")  # 只是那个便携解释器的默认落点，没有也不影响
#: 仓库根：这个脚本在 `<仓库>/tools/preview/serve.py`，往上两级就是仓库。
PROJECT = Path(__file__).resolve().parents[2]
TOOLS = PROJECT / "tools"
SITE = PROJECT / "site"

#: 解释器候选，按顺序试，第一个能 `import zensical, yaml, zhconv` 的胜出：
#:   1. `RWR_PYTHON` 环境变量（你的 venv 里那个 python）
#:   2. 正在跑这个脚本的解释器自己
#:   3. 工作区里那个便携 Python（本机默认就靠它）
#:   4. PATH 上的 python / python3
#: 为什么要有这一步：`zensical`、`pyyaml`、`zhconv` 得装在一个解释器里，
#: 而 PATH 上的 `python` 未必是那一个（这台机器上还踩过 WindowsApps 的桩）。
PYTHON_CANDIDATES = tuple(
    p for p in (
        os.environ.get("RWR_PYTHON"),
        sys.executable,
        WORKSPACE / "_py" / "py314" / "python.exe",
        shutil.which("python"),
        shutil.which("python3"),
    ) if p
)

#: 嵌入式 py314 既不认脚本目录也不认 PYTHONPATH，只能这样跑 tools/ 下的脚本。
BOOT = "import runpy,sys; sys.path.insert(0, {0!r}); runpy.run_path({1!r}, run_name='__main__')"

#: 页面这一头：**常驻**一条 SSE 连接（/__events），服务端一有动静就推过来——
#: 不用像轮询那样每 1.5 秒才问一次，存盘到刷新之间少掉这段白等。
#: 正在重建时右下角挂一条提示，免得页面毫无动静、看着像卡住。
#: EventSource 起不来（老浏览器、代理掐长连接）就退回原来的轮询。
REFRESH_JS = (
    b'<script>(function(){var c=null,tip=null;'
    b'function mark(busy){'
    b' if(busy&&!tip){tip=document.createElement("div");tip.textContent="\\u6b63\\u5728\\u91cd\\u5efa\\u2026";'
    b'  tip.style.cssText="position:fixed;right:1rem;bottom:1rem;z-index:99;padding:.4rem .75rem;'
    b'  border-radius:.3rem;background:#526cfe;color:#fff;font-size:.75rem;opacity:.92";'
    b'  document.body.appendChild(tip);}'
    b' if(!busy&&tip){tip.remove();tip=null;}}'
    b'function swap(){'
    b' fetch(location.href,{cache:"no-store"}).then(function(r){return r.text()}).then(function(t){'
    b'  var doc=new DOMParser().parseFromString(t,"text/html");'
    b'  var fresh=doc.querySelector("article.md-content__inner");'
    b'  var here=document.querySelector("article.md-content__inner");'
    b'  var y=window.scrollY;'
    b'  if(fresh&&here){here.innerHTML=fresh.innerHTML;window.scrollTo(0,y);}'
    b'  else location.reload();'
    b' }).catch(function(){location.reload()});}'
    b'function apply(d){'
    b' mark(!!d.busy);'
    b' if(c===null){c=d.v;return;}'
    b' if(d.v===c)return;'
    b' c=d.v;'
    b' /* pages with in-page search rebuild their widgets on load only: reload those */'
    b' if(document.querySelector(".ts-search")){location.reload();return;}'
    b' swap();}'
    b'var es=null;'
    b'if(window.EventSource){'
    b' es=new EventSource("/__events");'
    b' es.onmessage=function(e){try{apply(JSON.parse(e.data))}catch(x){}};'
    b' es.onerror=function(){es.close();es=null;};}'
    b'/* fallback: poll if SSE is gone */'
    b'setInterval(function(){'
    b' if(es&&es.readyState===1)return;'
    b' fetch("/__hot").then(function(r){return r.json()}).then(apply).catch(function(){})'
    b'},1500)})();</script>'
)

#: 存盘之后先等这么久再动手。等的是编辑器那些「中间状态」落定
#: （VS Code 是写临时文件再改名），一次保存只跑一轮重建。
#: 早先这里是固定的 0.8 秒——不管编辑器多快写完，每次都要白等满 0.8 秒。
#: 现在改成「静默期」：轮询到文件 0.15 秒不再动就走，最多等 0.8 秒。
QUIET = 0.15
DEBOUNCE_MAX = 0.8

#: 是否顺手跑翻译度体检。默认关——预览只管快，体检交给 fullcheck.bat。
CHECK = False

#: 常驻构建器（`zensical serve` 子进程）听的内部端口 = 预览端口 + 这个偏移。
#: 它只负责把 docs/ 构建进 site/，HTTP 服务与刷新仍归本脚本自己管。
BUILDER_PORT_GAP = 1000

#: 构建器说「这一轮构建完了」。zensical 把收尾那句写在 stderr 上，
#: 实测每完成一轮就有一行。万一那句话改版了，还有超时兜底（见 wait_build）。
BUILD_DONE = re.compile(r"no issues found|build finished", re.I)

state: dict = {"v": 0, "busy": False, "pending": False}

#: 常驻构建器（main() 里按端口建出来，见下面的 Builder）。rebuild() 用它。
builder: "Builder | None" = None

#: 页面那几条常驻的 SSE 连接。状态一变就往每个队列里塞一条，它们自己写出去。
subs: list = []


def publish() -> None:
    with lock:
        msg = json.dumps({"v": state["v"], "busy": bool(state["busy"])})
        feeds = list(subs)
    for feed in feeds:
        feed.put_nowait(msg)
lock = threading.Lock()
PY = ""


# ── 环境与命令 ────────────────────────────────────────────────────────────

def pick_python() -> str:
    """挑一个装齐依赖（zensical / yaml / zhconv）的解释器。"""
    probe = "import zensical, yaml, zhconv"
    for cand in PYTHON_CANDIDATES:
        if not cand or not Path(cand).is_file():
            continue
        try:
            done = subprocess.run([str(cand), "-c", probe], capture_output=True, timeout=60)
        except OSError:
            continue
        if done.returncode == 0:
            return str(cand)
    print("× 没找到装齐依赖的 Python。需要 zensical、pyyaml、zhconv 三个包，", flush=True)
    print("  试过这些解释器：", flush=True)
    for cand in PYTHON_CANDIDATES:
        print(f"    {cand}", flush=True)
    print("  装依赖：<上面某个 python> -m pip install zensical pyyaml zhconv", flush=True)
    print("  或者指定一个：设 RWR_PYTHON=<那个 python 的完整路径>", flush=True)
    raise SystemExit(1)


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    # 与 tools/watch.py 同一条规矩：显式按 UTF-8 收发，否则 Windows 上生成器
    # 报的中文错误会被 GBK 解码炸掉，看起来像「改了没生效」。
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(cmd, cwd=str(PROJECT), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)


def gen_steps() -> tuple[list[str], ...]:
    return tuple(
        [PY, "-c", BOOT.format(str(TOOLS), str(TOOLS / name))]
        for name in ("docsgen.py", "navgen.py")
    )


# ── 重建 ──────────────────────────────────────────────────────────────────

def mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


class Builder:
    """常驻构建器：借 `zensical serve` 的**增量**能力，只让它写 site/。

    为什么值得多起一个进程：`zensical build` 每轮都全量——827 个产物、53 MB、
    实测 3.3 秒，改没改都一样（连着跑两次、第二次什么都没改，还是 3.3 秒）。
    `zensical serve` 是常驻的，它记住上一轮的状态，改一页只重写那几十个文件：
    实测 **0.15 秒**，site/ 里只有 42/851 个文件被重写。这一个差别就是预览
    快慢的全部秘密。

    它那个 HTTP 端口我们不用（实测它发出来的 HTML 里没有任何 livereload 代码，
    指望不上它刷新页面）；只用它「起来了」和「一轮构建完了」这两个信号，
    服务与刷新仍旧由本脚本自己来。
    """

    def __init__(self, port: int) -> None:
        self.port = port
        self.proc: subprocess.Popen | None = None
        self.done = 0            # 完成的构建轮数（数日志里那句收尾）
        self.tail: list[str] = []  # 最近几行输出，起不来时打给人看
        self.disabled = False    # 起不来或超时没动静，就别再试了

    # ── 起停 ──────────────────────────────────────────────────────────────
    def alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def start(self, timeout: float = 90.0) -> bool:
        """起进程并等它第一轮构建完（起来就顺手把整个 site/ 建出来）。"""
        if self.disabled:
            return False
        if self.alive():
            return True
        print(f"· 启动常驻构建器：zensical serve（内部端口 {self.port}，只用来构建）", flush=True)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        try:
            self.proc = subprocess.Popen(
                [PY, "-m", "zensical", "serve", "-a", f"127.0.0.1:{self.port}"],
                cwd=str(PROJECT), env=env, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                errors="replace", bufsize=1,
            )
        except OSError as exc:
            print(f"  ! 构建器起不来（{exc}），退回每轮全量构建", flush=True)
            self.disabled = True
            return False
        atexit.register(self.stop)
        threading.Thread(target=self._read, daemon=True).start()
        ok = self.wait_build(0, timeout=timeout)
        if not ok:
            for line in self.tail:
                print(f"    | {line}", flush=True)
            print("  ! 构建器没起来或没建完，退回每轮全量构建", flush=True)
            self.stop()
            self.disabled = True
        return ok

    def _read(self) -> None:
        stream = self.proc.stdout if self.proc else None
        if stream is None:
            return
        try:
            for line in stream:
                line = line.strip()
                if not line:
                    continue
                self.tail.append(line)
                del self.tail[:-10]
                if BUILD_DONE.search(line):
                    self.done += 1  # 一轮构建收尾了
        except (OSError, ValueError):
            pass  # 进程没了/管道断了，wait_build 会从 poll() 看出来

    def stop(self) -> None:
        if self.proc is None or self.proc.poll() is not None:
            return
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()

    # ── 等一轮构建 ────────────────────────────────────────────────────────
    def wait_build(self, since: int, timeout: float = 30.0, settle: float = 0.3) -> bool:
        """等「又有构建收尾了」，并且再静 0.3 秒没有下一轮。

        为什么要 settle：生成器写 docs/ 不是一瞬间（docsgen 0.37 秒 + navgen
        0.25 秒），构建器可能在写到一半时就起过一轮。等它静下来，才不会把
        读到半套 docs/ 的那一轮当成最终结果推给浏览器。
        """
        t0 = time.time()
        seen = self.done
        last = time.time()
        while True:
            if self.done > seen:
                seen = self.done
                last = time.time()
            elif seen > since and time.time() - last >= settle:
                return True
            if not self.alive():
                return False
            if time.time() - t0 >= timeout:
                return seen > since
            time.sleep(0.05)


def process_name(pid: str) -> str:
    """PID 的映像名，小写（问不出来就返回空串）。"""
    try:
        done = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace")
    except OSError:
        return ""
    lines = (done.stdout or "").strip().splitlines()
    if not lines:
        return ""
    return lines[0].split(",")[0].strip('"').lower()


def kill_stale_builder(port: int) -> None:
    """清掉上次被硬杀（关窗口、taskkill）留下的构建器。

    它要是还活着，就继续占着 site/ 和那个内部端口；新的一轮会起不来。
    netstat 的状态名在中文 Windows 上也是英文 LISTENING，这儿照原样比。
    万一端口上坐着的是别的程序（名字问得出来、又不是 python），就不动它，
    构建器换个端口去。
    """
    try:
        done = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
    except OSError:
        return
    pids = set()
    for line in (done.stdout or "").splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0].upper() == "TCP" and parts[1].endswith(f":{port}"):
            pids.add(parts[4])
    for pid in pids:
        name = process_name(pid)
        if name and "python" not in name:
            print(f"! 端口 {port} 上不是 python（PID {pid}，{name}），不动它；"
                  f"构建器改用别的端口", flush=True)
            continue
        print(f"· 清掉上次留下的构建器（PID {pid}，端口 {port}）", flush=True)
        subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True)


def full_build() -> bool:
    """全量构建：只在常驻构建器起不来时才走这条路（原来每轮都是这么走的）。"""
    marker = SITE / "index.html"
    before = mtime(marker)
    # 这台机器上 zensical build 间歇性地以 os error 5 收场——像是杀软/索引器
    # 在扫刚写出的 850+ 个文件时锁住了它们：同样的命令有时 2.5 秒全绿，
    # 有时跑 56 秒然后拒绝访问。躲不开，只能重试；即便报错，产物通常也已经
    # 写得差不多齐，所以「产物变新了」也当成功，只有产物没动过才算失败。
    done = None
    after = before
    for attempt in range(1, 5):
        done = run([PY, "-m", "zensical", "build"])
        after = mtime(marker)
        if done.returncode == 0 or after > before:
            break
        wait = 5 * attempt
        print(f"… 构建没走完（第 {attempt} 次），{wait} 秒后重试", flush=True)
        time.sleep(wait)

    if done.returncode != 0 and after > before:
        print("! 构建收尾报了 os error 5，但产物已更新——照常刷新", flush=True)
        return True
    if done.returncode != 0:
        sys.stdout.write(done.stdout or "")
        sys.stderr.write(done.stderr or "")
        print("× 构建失败，改好之后会自动重试", flush=True)
        return False
    return True


def rebuild(tag: str = "") -> bool:
    """手写层变了：生成 docs/ → 让构建器重建 → 版本号 +1（页面自己刷新）。"""
    # 取「已经完成几轮」要放在生成器**之前**：构建器可能在 docsgen 写到一半时
    # 就起了一轮，那一轮的收尾也要算进来（wait_build 的 settle 会等它把后面
    # 几笔也收完）。
    since = builder.done

    for step in gen_steps():
        done = run(step)
        if done.returncode != 0:
            sys.stdout.write(done.stdout or "")
            sys.stderr.write(done.stderr or "")
            print("× 生成失败，改好之后会自动重试", flush=True)
            return False

    print(f"… 正在重建站点{tag}", flush=True)
    t_start = time.time()
    publish()  # 立刻让页面挂出「正在重建…」，别让页面看着像卡住

    if builder.alive() or builder.start():
        ok = builder.wait_build(since, timeout=30)
        if not ok:
            print("  ! 常驻构建器 30 秒没动静，改回全量构建", flush=True)
            builder.stop()
            builder.disabled = True
            ok = full_build()
    else:
        ok = full_build()
    if not ok:
        return False

    with lock:
        state["v"] += 1
        version = state["v"]
    publish()  # 构建完就推，页面马上刷新，不等下一次轮询
    spent = time.time() - t_start
    print(f"✓ 已重建（第 {version} 版，{spent:.1f} 秒，浏览器会自动刷新）", flush=True)
    if spent > 20:
        print("  · 这一轮偏慢：多半是杀软在扫刚写出的产物，或退回全量那条路了。", flush=True)

    # 默认**不体检**：预览只负责「改完立刻看见」。翻译度、链接那些留给
    # fullcheck.bat（你说要统一处理的时候再跑）。想在这里也一并看就加 --check。
    if CHECK:
        try:
            translation_todo()
        except Exception as exc:
            print(f"  （翻译度体检没跑成：{type(exc).__name__} {exc}）", flush=True)
    return True


def translation_todo() -> None:
    """重建之后跑一遍翻译度体检，把「还有谁没跟上」直接说在终端里。

    为什么要有这一步：改 `content/**.zh-hans.md` 是对的——那是唯一手写层，
    繁体由 docsgen 自己派生（改完就有，不用管）。但**英文是手写译文**，
    原文动了它不会自己变，而「已过期」是要挡构建的。光看页面看不出来：
    预览会照常显示英文页那份旧译文，看着一切正常，等发版 CI 才红。
    所以这里每次重建都点一次名，并把更新指纹的那条命令直接给出来。
    """
    done = run([PY, "-c", BOOT.format(str(TOOLS), str(TOOLS / "i18n_check.py"))])
    text = (done.stdout or "").strip()
    if text:
        print(text, flush=True)

    report = PROJECT / "i18n-report.json"
    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    todo = data.get("todo") or []
    if not todo:
        return

    print("  还没跟上（会挡住构建）：", flush=True)
    for item in todo:
        print(f"    [{item.get('lang')}] {item.get('target')}  ·  {item.get('status')}", flush=True)
    stale = [i for i in todo
             if i.get("status") == "stale" and i.get("source") and i.get("target")]
    if stale:
        print("    改完英文后，用这条把指纹更新（一次一条）：", flush=True)
        for item in stale:
            print(f"      node _refingerprint.js rwr-mapbook/{item['source']}:"
                  f"rwr-mapbook/{item['target']}", flush=True)


def wait_quiet(interval: float = 0.05, quiet: float = QUIET,
               cap: float = DEBOUNCE_MAX) -> float:
    """等编辑器把这一笔写完：手写层 0.15 秒不再动就走，最多等 0.8 秒。

    编辑器存盘往往不是「一次写完」：VS Code 默认写临时文件再改名，中间会多出
    一次变化（甚至一个 .tmp）。等它静下来，一次保存就只重建一轮。
    早先这里是固定 sleep(0.8)——不管编辑器多快写完都要白等满 0.8 秒。
    """
    t0 = time.time()
    last = watch.stamp()
    stable = time.time()
    while time.time() - t0 < cap:
        time.sleep(interval)
        now = watch.stamp()
        if now != last:
            last = now
            stable = time.time()
        elif time.time() - stable >= quiet:
            break
    return time.time() - t0


def watch_loop(interval: float) -> None:
    seen = watch.stamp()
    while True:
        try:
            time.sleep(interval)
            with lock:
                if state.pop("pending", False):
                    seen = 0.0  # 上一轮忙着重建时来的改动被跳过了，强制补一轮
            now = watch.stamp()
            if now == seen:
                continue
            seen = now
            wait_quiet()
            seen = watch.stamp()
            with lock:
                if state["busy"]:
                    state["pending"] = True
                    continue
                state["busy"] = True
            try:
                rebuild("（手写层有改动）")
            finally:
                with lock:
                    state["busy"] = False
                publish()  # 「重建中」那条提示要收掉，顺便把最终状态推一遍
        except Exception:
            # 这条线程一死，「改了不刷新」还没有任何报错——本机发生过一次，
            # 原因没抓到。宁可聒噪：出了什么异常都打出来，歇三秒接着干。
            import traceback
            traceback.print_exc()
            time.sleep(3)


# ── 静态服务 ──────────────────────────────────────────────────────────────

class Handler(http.server.SimpleHTTPRequestHandler):
    server_version = "rwr-preview/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        pass  # 正常请求一律不刷屏

    def sse(self) -> None:
        """服务端这一头：一条常驻连接，状态一变就推给页面（替代轮询）。"""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        feed: queue.Queue = queue.Queue()
        with lock:
            subs.append(feed)
            first = json.dumps({"v": state["v"], "busy": bool(state["busy"])})
        try:
            self.wfile.write(b"data: " + first.encode("utf-8") + b"\n\n")
            self.wfile.flush()
            while True:
                self.wfile.write(b"data: " + feed.get().encode("utf-8") + b"\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass  # 页面关了/刷新了，这条连接就到这儿
        finally:
            with lock:
                if feed in subs:
                    subs.remove(feed)

    def log_error(self, fmt: str, *args) -> None:
        # 404 一律静音：favicon、页面脚本探各语种树下的 sitemap.xml 之类，
        # 一进清单页就十几条，全是噪音，预览里没有任何查的价值。
        # 真值得看的只有 5xx（脚本/服务本身出了问题）。
        if "404" in (fmt % args):
            return
        sys.stderr.write(f"  ! {self.path} → {fmt % args}\n")

    def do_GET(self) -> None:
        path_only = self.path.split("?")[0]
        if path_only == "/__events":
            self.sse()
            return
        if path_only == "/__hot":
            with lock:
                body = json.dumps({"v": state["v"], "busy": bool(state["busy"])}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if path_only == "/favicon.ico":
            # 站点没有 favicon，浏览器却每加载一页都要讨一次；给它 204，
            # 免得每次开页面都攒一条 404 刷屏。
            self.send_response(204)
            self.end_headers()
            return

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            if not self.path.endswith("/"):
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return
            path = os.path.join(path, "index.html")
        if not (os.path.isfile(path) and path.endswith(".html")):
            super().do_GET()
            return

        with open(path, "rb") as fh:
            data = fh.read()
        # 自动刷新只注入 HTML；没有 </body> 就追加到末尾，总能生效。
        data = data.replace(b"</body>", REFRESH_JS + b"</body>") if b"</body>" in data else data + REFRESH_JS
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def open_browser(url: str) -> None:
    """用系统默认浏览器打开预览，打不开就把地址再说一遍。"""
    try:
        if webbrowser.open(url):
            return
        reason = "浏览器没响应"
    except Exception as exc:  # 免得这条线程把服务带塌
        reason = str(exc)
    print(f"· 没能自动打开浏览器（{reason}），手动打开：{url}", flush=True)


def port_free(port: int) -> bool:
    sock = socket.socket()
    try:
        sock.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def force_utf8_stdio() -> None:
    """把 stdout/stderr 钉死在 UTF-8。

    ⚠️ 这一条不是洁癖：Windows 控制台默认是 GBK，脚本里那些 `✓`、`…` 会
    `UnicodeEncodeError` 把**整个预览**带塌（实测：构建成功、打印那一行时崩，
    服务根本没起来）。双击 start.bat 时它 `chcp 65001` 过，所以看不出来；
    别的方式拉起来（另一个脚本、任务计划、无窗口）就会撞上。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


# ── 入口 ──────────────────────────────────────────────────────────────────

def main() -> int:
    global PY, CHECK, builder

    force_utf8_stdio()

    ap = argparse.ArgumentParser(description="rwr-mapbook 本地热更新预览")
    ap.add_argument("--port", type=int, default=8000, help="端口，默认 8000")
    ap.add_argument("--auto-port", action="store_true",
                    help="端口被占时自动顺延到下一个空着的（8000 被占就试 8001、8002…）")
    ap.add_argument("--no-build", action="store_true",
                    help="启动时先不构建，直接拿现有 site/ 开服务（构建器等第一次改动再起）")
    ap.add_argument("--no-open", action="store_true", help="不要用默认浏览器打开预览（默认会自动开）")
    ap.add_argument("--check", action="store_true",
                    help="重建后顺手跑一遍翻译度体检（默认不跑：那属于交付前统一处理的事）")
    ap.add_argument("--all-langs", action="store_true",
                    help="（已无意义，只为兼容老命令保留）现在三种语言都构建、都能看")
    args = ap.parse_args()

    if not PROJECT.is_dir():
        print(f"× 找不到项目目录 {PROJECT}", flush=True)
        return 1

    port = args.port
    if not port_free(port):
        if args.auto_port:
            for candidate in range(port + 1, port + 21):
                if port_free(candidate):
                    print(f"· 端口 {port} 被占，顺延到 {candidate}", flush=True)
                    port = candidate
                    break
            else:
                print(f"× 端口 {port}～{port + 20} 全被占了，换个远的：--port 9000", flush=True)
                return 1
        else:
            print(f"× 端口 {port} 已被占用。三选一：", flush=True)
            print(f"  1) 关掉它：双击 stop.bat（或 stop.bat {port}）", flush=True)
            print(f"  2) 换一个：python serve.py --port 8010", flush=True)
            print(f"  3) 让它自己找空位：python serve.py --auto-port", flush=True)
            return 1

    CHECK = args.check
    PY = pick_python()
    sys.path.insert(0, str(TOOLS))
    global watch
    import watch  # noqa: E402  盯梢清单与间隔的唯一出处

    # 常驻构建器那个内部端口：默认「预览端口 + 1000」，被占就往后找。
    builder_port = port + BUILDER_PORT_GAP
    kill_stale_builder(builder_port)  # 上次被硬杀留下的，先清掉
    if not port_free(builder_port):
        for candidate in range(builder_port + 1, builder_port + 21):
            if port_free(candidate):
                builder_port = candidate
                break
        else:
            print(f"· 内部端口 {port + BUILDER_PORT_GAP} 附近全被占，只能每轮全量构建", flush=True)
            builder_port = 0
    builder = Builder(builder_port)
    if not builder_port:
        builder.disabled = True

    print(f"项目：{PROJECT}", flush=True)
    print(f"解释器：{PY}", flush=True)
    if not args.no_build:
        if not builder.start():
            full_build()
    else:
        print("· 跳过启动构建（--no-build）：构建器等第一次改动再起（起来时要全量建一次）",
              flush=True)

    threading.Thread(target=watch_loop, args=(watch.INTERVAL,), daemon=True).start()
    url = f"http://127.0.0.1:{port}/"
    print("", flush=True)
    print(f"预览： {url}", flush=True)
    print("改 content/ 下的文件存盘，一秒左右自己刷新。停止：Ctrl-C（或关掉这个窗口）", flush=True)
    if builder.disabled:
        print("· 常驻构建器没起来：退回每轮全量构建（约 4 秒一轮），功能一样。", flush=True)
    else:
        print(f"· 常驻构建器在内部端口 {builder.port} 上（只用来构建，不是给你点的）。", flush=True)

    if not args.no_open:
        # 等一拍再开：socket 已经 bind 了，但要让 serve_forever 先转起来，
        # 免得浏览器的第一个请求撞在没 accept 的队列上看起来像打不开。
        threading.Timer(1.0, open_browser, args=(url,)).start()
        print("· 正在用默认浏览器打开……（不想自动开就加 --no-open）", flush=True)

    with http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n停了。", flush=True)
    builder.stop()  # 别把子进程落下（关窗口那种硬杀躲不掉，下次启动会清）
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
