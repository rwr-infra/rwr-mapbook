#!/usr/bin/env python3
"""把发布用的归档切成不超过上限的分片，并写一份清单让浏览器端拼回去。

为什么要有分片
--------------
仓库要托管历史版本的地编归档（060、070……），而 **GitHub 网页上传的单文件上限是
25 MB**：比它大的文件在浏览器里根本传不上去。所以归档一分为若干片，每片不超上限，
随站点一起发布；读者那边由 docs/javascripts/downloads.js 一次取回全部片段、
逐片校验、拼成一个**与原文件同名**的整包存下来。

读者不该看见分片
----------------
分片是**托管方的限制**，不是内容的一部分。页面上只出现版本、文件名与总大小，
拼接与命名都在浏览器里做完，落到下载文件夹里的是 `060.zip`，不是一堆 `.partNNN`。
手工合并、命令行工具都不需要。

清单是唯一出处
--------------
本脚本产出两样东西，都在 docs/downloads/ 下：

    manifest.json        分片的名单：路径、字节数、每片与整文件的 sha256
    <名字>.partNNN       分片本体

页面（content/download/*.md）只写「哪一版、什么文件、一个按钮」——大小与状态由
docs/javascripts/downloads.js 从清单里读出来摆在按钮旁边。所以**大小只有一份**，
页面上不会出现一个手写的、源文件换掉之后就过期的数字。

    uv run python tools/chunker.py --src ~/Downloads 060.zip 070.rar 0101.rar
    uv run python tools/chunker.py --check      # 只对账，不切分；CI 跑这个
    uv run python tools/chunker.py --selftest   # 切一遍再拼回来，不碰仓库

`--check` 不需要源文件：源归档在群文件里，仓库里没有。它只看仓库里的这一份对不对——
分片还在不在、哈希对不对、页面上挂的按钮与清单是不是两边都对得上。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONTENT = ROOT / "content"

#: 分片与清单的落点。它在 docs/ 之下，因此会随站点一起发布。
#: tools/docsgen.py 只清理带生成横幅的 .md 与跳转桩，碰不到这里。
OUT = DOCS / "downloads"
MANIFEST = OUT / "manifest.json"

#: 单片上限：25 MB。用**十进制**，不用 25 MiB —— 各家说的「25 MB」都是十进制，
#: 按 MiB 切出来的 26 214 400 字节会正好贴在上限上，多半传不上去。
LIMIT = 25 * 1000 * 1000

#: 分片名。原扩展名留在中间，肉眼一看就知道它属于哪个文件。
PART_FMT = "{name}.part{n:03d}"

#: 清单里给浏览器看的路径：相对**站点根**，由脚本用自己的地址拼出来
#: （见 docs/javascripts/downloads.js 的 BASE）。
URL_PREFIX = "downloads/"

#: 分片名的判据。清理与体检都按它认人。
PART_RE = re.compile(r"^.+\.part\d{3}$")

#: 页面上挂下载按钮的地方：`<button … data-dl="060">`。清单与页面对不上时，
#: 读者点到的按钮要么没反应，要么下到别的文件——所以两边都要算一遍。
#: 注意这只扫 content/（手写层）：docs/ 里的 .md 是它的副本，扫那里等于扫两遍。
DL_RE = re.compile(r'data-dl="([^"]+)"')


# ── 切分 ──────────────────────────────────────────────────────────────────

def digest_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_one(src: Path, limit: int, out: Path) -> dict:
    """切一个文件，返回清单里的一条。

    整文件的哈希是**边切边算**的：一遍读完，不为了算哈希再读一次盘。
    """
    whole = hashlib.sha256()
    parts: list[dict] = []
    with src.open("rb") as handle:
        index = 0
        while True:
            data = handle.read(limit)
            if not data:
                break
            index += 1
            whole.update(data)
            name = PART_FMT.format(name=src.name, n=index)
            (out / name).write_bytes(data)
            parts.append({
                "path": URL_PREFIX + name,
                "bytes": len(data),
                "sha256": digest_of(data),
            })
    return {
        "id": src.stem,
        "name": src.name,
        "bytes": sum(part["bytes"] for part in parts),
        "sha256": whole.hexdigest(),
        "parts": parts,
    }


def prune(out: Path, keep: set[str]) -> list[str]:
    """删掉上一次切分留下的、这一份清单里已经没有的分片。

    上限调小一次再调回来，就会留下比现在多的分片；不清理的话它们既发布出去，
    又让读者那边多取几十兆——而 `--check` 也会因此一直报「不在清单里」。
    """
    removed: list[str] = []
    if not out.is_dir():
        return removed
    for path in sorted(out.iterdir()):
        if path.is_file() and PART_RE.match(path.name) and path.name not in keep:
            path.unlink()
            removed.append(path.name)
    return removed


def write_manifest(entries: list[dict], limit: int, manifest: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps({"limit": limit, "files": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ── 对账 ──────────────────────────────────────────────────────────────────

def content_ids() -> dict[str, list[str]]:
    """content/ 里出现过 `data-dl="…"` 的 id → 出现在哪些文件里。"""
    found: dict[str, list[str]] = {}
    for path in sorted(CONTENT.rglob("*.md")):
        for match in DL_RE.finditer(path.read_text(encoding="utf-8")):
            found.setdefault(match.group(1), []).append(str(path.relative_to(ROOT)))
    return found


def check(out: Path, manifest: Path) -> list[str]:
    """仓库里这一份自己是否成立：分片、哈希、页面与清单两边对账。"""
    if not manifest.is_file():
        return [f"{MANIFEST.relative_to(ROOT)} 不存在：先在有源归档的机器上跑一次 `make downloads`"]

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    entries = payload.get("files") or []
    problems: list[str] = []
    keep: set[str] = set()

    for entry in entries:
        total = 0
        for part in entry.get("parts") or []:
            name = str(part.get("path", "")).rsplit("/", 1)[-1]
            keep.add(name)
            path = out / name
            if not path.is_file():
                problems.append(f"{entry.get('id')}: 清单里的分片 {name} 不在 docs/downloads/ 下")
                continue
            data = path.read_bytes()
            total += len(data)
            if len(data) != part.get("bytes"):
                problems.append(
                    f"{entry.get('id')}: 分片 {name} 是 {len(data)} 字节，"
                    f"清单记的是 {part.get('bytes')} 字节"
                )
            elif digest_of(data) != part.get("sha256"):
                problems.append(f"{entry.get('id')}: 分片 {name} 的哈希与清单不符（文件被换过或传坏了）")
        if total and total != entry.get("bytes"):
            problems.append(
                f"{entry.get('id')}: 分片合计 {total} 字节，清单记的整文件是 {entry.get('bytes')} 字节"
            )
        if not entry.get("parts"):
            problems.append(f"{entry.get('id')}: 清单里一条分片都没有")

    if out.is_dir():
        for path in sorted(out.iterdir()):
            if path.is_file() and PART_RE.match(path.name) and path.name not in keep:
                problems.append(f"分片 {path.name} 不在清单里：上一次切分的残留，重跑 `make downloads`")

    declared = {str(entry.get("id")) for entry in entries}
    referenced = content_ids()
    for missing in sorted(set(referenced) - declared):
        problems.append(
            f'页面上的 data-dl="{missing}" 在清单里没有对应文件（{referenced[missing][0]}）：'
            f"按钮点了不会有反应"
        )
    for orphan in sorted(declared - set(referenced)):
        problems.append(f"清单里的 {orphan} 没有任何页面引用：读者点不到它")

    return problems


# ── 自检 ──────────────────────────────────────────────────────────────────

def selftest() -> int:
    """切一遍再拼回来，不碰仓库里的任何东西。

    这是「切分逻辑坏了就会红」的那一条：源文件在群文件里，CI 拿不到，
    所以线上能跑的只有这一段。
    """
    payload = bytes(range(256)) * 30000  # 7 680 000 字节
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        out = root / "downloads"
        out.mkdir()

        src = root / "sample.bin"
        src.write_bytes(payload)
        entry = split_one(src, 3_000_000, out)
        assert len(entry["parts"]) == 3, f"7.68 MB 按 3 MB 切，应当 3 片，实得 {len(entry['parts'])}"
        assert entry["bytes"] == len(payload), entry["bytes"]
        assert entry["sha256"] == digest_of(payload), "整文件哈希与源不符"
        merged = b"".join(
            (out / part["path"].rsplit("/", 1)[-1]).read_bytes() for part in entry["parts"]
        )
        assert merged == payload, "拼回来的字节与源不一致"

        # 不超上限的文件切成一片，内容原样——大多数归档走的就是这一条。
        small = root / "small.bin"
        small.write_bytes(payload[:100])
        one = split_one(small, 3_000_000, out)
        assert len(one["parts"]) == 1 and one["parts"][0]["bytes"] == 100, one["parts"]

        # 上限正好整除时不多切一片空的。
        exact = root / "exact.bin"
        exact.write_bytes(b"x" * 6_000_000)
        even = split_one(exact, 3_000_000, out)
        assert len(even["parts"]) == 2, f"正好两倍应切 2 片，实得 {len(even['parts'])}"

    print("自检通过：切分、拼接、整文件哈希三处都对得上")
    return 0


# ── 入口 ──────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="*", help="要切的归档（相对 --src，或绝对路径）")
    parser.add_argument("--src", default=str(Path.home() / "Downloads"),
                        help="归档所在的目录（默认 ~/Downloads）")
    parser.add_argument("--limit", type=int, default=LIMIT, help=f"单片字节上限（默认 {LIMIT}）")
    parser.add_argument("--check", action="store_true", help="只对账，不切分（CI 跑这个）")
    parser.add_argument("--selftest", action="store_true", help="自检：切一遍再拼回来")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    if args.check:
        problems = check(OUT, MANIFEST)
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        if problems:
            print(f"\n归档体检：{len(problems)} 个问题", file=sys.stderr)
            return 1
        files = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
        total = sum(entry["bytes"] for entry in files)
        print(f"归档体检：{len(files)} 个归档、{sum(len(e['parts']) for e in files)} 片，"
              f"合计 {total / 1e6:.1f} MB，页面与清单对得上")
        return 0

    if not args.files:
        parser.error("没有给要切的文件：先是哪几个由 Makefile 的 DOWNLOADS 列着")

    src_dir = Path(args.src).expanduser()
    OUT.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []
    seen: set[str] = set()
    for name in args.files:
        path = Path(name).expanduser()
        if not path.is_absolute():
            path = src_dir / name
        if not path.is_file():
            print(f"error: 找不到 {path}", file=sys.stderr)
            return 1
        if path.stat().st_size == 0:
            print(f"error: {path} 是空文件", file=sys.stderr)
            return 1
        if path.stem in seen:
            print(f"error: 两个文件的 id 都是 “{path.stem}”：页面上认不出谁是谁", file=sys.stderr)
            return 1
        seen.add(path.stem)
        entries.append(split_one(path, args.limit, OUT))

    keep = {part["path"].rsplit("/", 1)[-1] for entry in entries for part in entry["parts"]}
    removed = prune(OUT, keep)
    write_manifest(entries, args.limit, MANIFEST, OUT)

    for name in removed:
        print(f"清掉旧分片 {name}")
    for entry in entries:
        biggest = max(part["bytes"] for part in entry["parts"])
        print(f"  {entry['name']:<16} {entry['bytes']:>10} B → {len(entry['parts'])} 片，"
              f"最大一片 {biggest / 1e6:.1f} MB")

    problems = check(OUT, MANIFEST)
    for problem in problems:
        # 页面还没跟上不算「切分失败」，但必须说出来：这些是构建期就该知道的事。
        print(f"warn: {problem}", file=sys.stderr)
    print(f"切好了：{len(entries)} 个归档，"
          f"清单 {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
