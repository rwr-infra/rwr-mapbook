#!/usr/bin/env python3
"""把发布用的归档放进 docs/downloads/，写一份清单，超过上限的才切开。

先别切
------
**能整份存下就整份存。** 整包是一个文件时，页面上那个按钮就是一条**直链**：
浏览器能下，下载器（IDM、aria2、迅雷）也能下，右键就交给它们了。切成分片则相反——
分片是真实地址没错，但那是几段，交给下载器只会拿到几段 `.partNNN`，还得自己合并；
说得准确一点，**分片是给「上传」省事，不是给「下载」省事**，代价全落在读者那边。

所以上限取的是「命令行 push」那一档（`git push` 单文件 100 MiB），不是网页上传那一档
（网页上传单文件 25 MB）。两者混起来就会白切一刀，见 LIMIT 处的说明。
要按网页上传那一档切：`make downloads LIMIT=25000000`。

非切不可的时候
--------------
超过上限的文件一切为若干片，随站点一起发布；读者那边由
docs/javascripts/downloads.js 一次取回全部片段、逐片校验、拼成一个
**与原文件同名**的整包存下来。落到下载文件夹里的是 `060.zip`，不是一堆 `.partNNN`。

清单是唯一出处
--------------
本脚本产出两样东西，都在 docs/downloads/ 下：

    manifest.json              名单：路径、字节数、每片与整文件的 sha256
    <名字>                     整文件（未超上限），或
    <名字>.partNNN             分片（超了上限）

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

#: 单片上限。**默认取的是「命令行 push」那一档，不是网页上传那一档。**
#:
#: 托管方对单个文件其实有两个不同的上限，混起来就会像下面这样白切一刀：
#:
#:   25 MB      GitHub **网页端**上传单个文件的上限（十进制）
#:   100 MiB    `git push` 的硬上限（超过直接被服务端拒绝）
#:
#: 按 25 MB 切出来的分片，读者那边只能由页面拼（见 docs/javascripts/downloads.js）——
#: 分片是真实地址，但那是几段，交给下载器只会得到几段 `.partNNN`。而 100 MiB 以内的
#: 整包可以**原样存一份**，按钮就是一个直链：浏览器能下，下载器也能下。
#: 所以默认值是后者：**只在必须的时候才切**。
#:
#: 要改回按网页上传那一档切：`make downloads LIMIT=25000000`（切成十进制 25 MB）。
LIMIT = 100 * 1024 * 1024

#: 读写分块。整文件的哈希是边写边算的，不为了算哈希把大文件整个读进内存。
BLOCK = 1 << 20

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

    不超上限的文件**原样存一份，还叫它本来的名字**。`060.zip` 本来就是一个整文件，
    没有任何理由把它改名成 `060.zip.part001` —— 那会白白毁掉两件事：它的地址不再
    是直链（右键交给下载器这一条就没了），以及读者要经过页面才拿得到。
    清单里仍然是「一条，含一片」，只是一个不多不少，所以上层不必分两种情况。

    整文件的哈希**边写边算**，一遍过，不为了算哈希把大文件整个读进内存。
    """
    size = src.stat().st_size
    whole = hashlib.sha256()

    if size <= limit:
        target = out / src.name
        with src.open("rb") as reader, target.open("wb") as writer:
            for block in iter(lambda: reader.read(BLOCK), b""):
                whole.update(block)
                writer.write(block)
        digest = whole.hexdigest()
        return {
            "id": src.stem,
            "name": src.name,
            "bytes": size,
            "sha256": digest,
            "parts": [{"path": URL_PREFIX + src.name, "bytes": size, "sha256": digest}],
        }

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


def known_names(manifest: Path) -> set[str]:
    """上一份清单里出现过的文件名。清理时靠它认出「这次不再需要」的那些。

    只按分片名的形状扫是不够的：改成整文件存放之后，上一次留下的
    `060.zip.part001` 和这一次的 `060.zip` 名字对不上，而整文件本身没有
    任何形状可认——所以拿上一份清单当名单，才认得全。
    """
    if not manifest.is_file():
        return set()
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    names: set[str] = set()
    for entry in payload.get("files") or []:
        for part in entry.get("parts") or []:
            names.add(str(part.get("path", "")).rsplit("/", 1)[-1])
    return names


def prune(out: Path, keep: set[str], previous: set[str]) -> list[str]:
    """删掉上一次留下的、这一份清单里已经没有的文件。

    上限调小一次再调回来，就会留下比现在多的分片；不清理的话它们既发布出去，
    又让读者那边多取几十兆——而 `--check` 也会因此一直报「不在清单里」。
    """
    removed: list[str] = []
    if not out.is_dir():
        return removed
    for path in sorted(out.iterdir()):
        if not path.is_file() or path.name in keep:
            continue
        # 两种都要清：上一次的分片（名字就是 `X.partNNN`，改了上限之后名字还在，
        # 但已经不该留），以及 JSON 与清单本身（listdir 之外的东西不动）。
        if PART_RE.match(path.name) or path.name in previous:
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

        # 不超上限的文件**原样存一份**，还叫本来的名字——直链就是这么来的。
        small = root / "small.bin"
        small.write_bytes(payload[:100])
        one = split_one(small, 3_000_000, out)
        assert len(one["parts"]) == 1 and one["parts"][0]["bytes"] == 100, one["parts"]
        assert one["parts"][0]["path"] == "downloads/small.bin", one["parts"][0]["path"]
        assert (out / "small.bin").is_file(), "整文件应当以原名落盘"
        assert not (out / "small.bin.part001").exists(), "整文件不该改名成分片"

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
        split = [entry for entry in files if len(entry.get("parts") or []) > 1]
        shape = ("全部是整文件" if not split
                 else f"{len(split)} 个切成了分片、{len(files) - len(split)} 个是整文件")
        print(f"归档体检：{len(files)} 个归档、合计 {total / 1e6:.1f} MB（{shape}），"
              f"页面与清单对得上")
        return 0

    if not args.files:
        parser.error("没有给要切的文件：先是哪几个由 Makefile 的 DOWNLOADS 列着")

    src_dir = Path(args.src).expanduser()
    OUT.mkdir(parents=True, exist_ok=True)
    previous = known_names(MANIFEST)
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
    removed = prune(OUT, keep, previous)
    write_manifest(entries, args.limit, MANIFEST, OUT)

    for name in removed:
        print(f"清掉旧的 {name}")
    for entry in entries:
        pieces = len(entry["parts"])
        shape = "整文件" if pieces == 1 else f"切 {pieces} 片"
        print(f"  {entry['name']:<24} {entry['bytes']:>10} B  {shape}")

    problems = check(OUT, MANIFEST)
    for problem in problems:
        # 页面还没跟上不算「切分失败」，但必须说出来：这些是构建期就该知道的事。
        print(f"warn: {problem}", file=sys.stderr)
    print(f"切好了：{len(entries)} 个归档，"
          f"清单 {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
