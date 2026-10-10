#!/usr/bin/env python3
"""往 Cloudflare R2（`assets` 桶 · `rwrme-web-assets/` 前缀）上传／删除归档。

    r2.bat list                      列出线上都有什么
    r2.bat head 060.zip              看一个文件的大小、类型、缓存头、公开地址
    r2.bat upload D:\\pkg\\070.rar   上传（对象名默认就是文件名）
    r2.bat delete 070.rar            删除（要你手打一遍名字才肯删）
    r2.bat verify                    页面上的直链与哈希，和线上挨个对一遍
    r2.bat creds                     看凭据是从哪儿读的（值打码，不打印密钥）
    r2.bat lock                      把凭据文件的权限收紧到只有你自己

密钥不写在脚本里：按顺序找 `R2_CREDS` 指的文件 → 本目录的 `creds.env` →
`~/.r2/creds.env`；同名环境变量始终覆盖文件里的值。

⚠️ **这套工具在仓库里，密钥永远不在。** `creds.env` 只在你自己的机器上，
既不要提交、也不要发给别人。需要能上传/删除归档的凭据，联系
<https://github.com/bananaxiao2333>。

⚠️ 密钥只认「文件 + 环境变量」两种给法，且**任何输出都不打印密钥值**：
   打印不出来就抄不走、也贴不进聊天里。`creds` 打的是打码版。

约定（与 rwr-mapbook/README.md 的「历史版本归档放在站外」一节一致）
------------------------------------------------------------------
- **对象名就是原文件名**（`070.rar`、`OgreSDK_vc10_v1-7-4.zip`），不带版本目录——
  名字本身已经唯一，多套一层只会在换存储时多一处要改的地方；
- **长缓存**：`Cache-Control: public, max-age=31536000, immutable`；
- **先算 sha256 再传**：传错文件是这里唯一会静默出错的地方，所以上传前把哈希打出来
  请你对一眼，对不上就别传；
- **哈希只写一处**：传完脚本会打印 sha256，拿去更新 `content/download/index.<lang>.md`
  下面那份清单即可；存储那边不另存清单文件（两份记录会分叉，一份不会）。

⚠️ 归档是**冻结的**：同名文件永远同一个内容，所以敢上长缓存。
   真要换文件内容，请先想清楚——改了文件才动页面上的哈希，没改就别动。
"""

from __future__ import annotations

import argparse
import hashlib
import mimetypes
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
#: 仓库根。这个脚本在 `<仓库>/tools/r2/r2.py`，往上两级就是仓库；
#: `verify` 要读 `content/**/*.md`，所以这个路径得对。
PROJECT = HERE.parents[1]

#: 凭据按这个顺序找，先找到的先用：
#:   1. 环境变量 `R2_CREDS` 指的那个文件（想把密钥放在仓库外面就用它）
#:   2. 本目录的 `creds.env`（从 creds.example.env 复制一份；**永远不要提交**）
#:   3. `~/.r2/creds.env`
#: 文件里的值还可以被同名环境变量覆盖——**环境变量优先**。
_candidates = [
    Path(os.environ["R2_CREDS"]).expanduser() if os.environ.get("R2_CREDS") else None,
    HERE / "creds.env",
    Path.home() / ".r2" / "creds.env",
]
CREDS_CANDIDATES = tuple(p for p in _candidates if p is not None)
CREDS = HERE / "creds.env"  # 提示信息里默认提到的那一个
CREDS_USED: Path | None = None  # 实际读到的是哪个（creds 命令要打出来）

ENV_KEYS = ("R2_ENDPOINT", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY",
            "R2_BUCKET", "R2_PREFIX", "R2_PUBLIC_BASE")

#: 已经读进来的密钥值。任何要往外打的东西都过一遍 redact()——
#: 万一哪层库把密钥塞进异常信息里，也不会打到终端/日志里。
SECRETS: list[str] = []


def redact(text: str) -> str:
    """把密钥值从要打印的文本里抹掉。"""
    for secret in SECRETS:
        if secret:
            text = text.replace(secret, "***")
    return text


def mask(value: str) -> str:
    """打码：留头尾各 4 位，够认出来是谁，又抄不走。"""
    if not value:
        return "（空）"
    if len(value) <= 10:
        return value[:2] + "*" * max(len(value) - 2, 0)
    return f"{value[:4]}…{value[-4:]}（{len(value)} 位）"


def mask_endpoint(url: str) -> str:
    """endpoint 里的账户 ID 也算半个隐私（打一半码）。"""
    m = re.match(r"(https?://)([^./]+)(\..*)", url)
    if not m:
        return url
    head, host, tail = m.groups()
    return f"{head}{host[:6]}{'*' * max(len(host) - 6, 0)}{tail}"


#: 这几样扩展名按 README 的约定显式给，其余交给 mimetypes 猜。
CONTENT_TYPES = {
    ".zip": "application/zip",
    ".rar": "application/vnd.rar",
    ".7z": "application/x-7z-compressed",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".pdf": "application/pdf",
}
CACHE_CONTROL = "public, max-age=31536000, immutable"


# ── 连接 ──────────────────────────────────────────────────────────────────

def read_env_file(path: Path, cfg: dict) -> None:
    """把一个 KEY=VALUE 的 env 文件读进 cfg。

    ⚠️ 按 `utf-8-sig` 读：记事本存出来的 UTF-8 常带 BOM，带 BOM 时第一个键会变成
    `"\\ufeffR2_ENDPOINT"`——表现是「明明填了却说缺 R2_ENDPOINT」，很难看出为什么。
    """
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        if " #" in value:  # 行尾注释：这几样值里不会有 #，留着容易看岔
            value = value.split(" #", 1)[0].strip()
        cfg[key.strip()] = value


def load_creds() -> dict:
    """按 CREDS_CANDIDATES 的顺序找凭据文件，再让同名环境变量覆盖它。"""
    global CREDS_USED
    cfg: dict[str, str] = {}
    for path in CREDS_CANDIDATES:
        if path.is_file():
            CREDS_USED = path
            read_env_file(path, cfg)
            break
    for key in ENV_KEYS:
        if os.environ.get(key):
            cfg[key] = os.environ[key].strip()

    missing = [k for k in ("R2_ENDPOINT", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY")
               if not cfg.get(k)]
    if missing:
        print(f"× 缺 {', '.join(missing)}。", flush=True)
        print("  三种给法，挑一种：", flush=True)
        print(f"    1) 从 creds.example.env 复制一份到 {CREDS}，把值填进去", flush=True)
        print("    2) 放到仓库外面：设 R2_CREDS=D:\\某处\\r2-creds.env", flush=True)
        print("    3) 直接设环境变量 R2_ENDPOINT / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY",
              flush=True)
        raise SystemExit(1)

    cfg.setdefault("R2_BUCKET", "assets")
    cfg.setdefault("R2_PREFIX", "rwrme-web-assets")
    cfg.setdefault("R2_PUBLIC_BASE", "https://assets.rwr-infra.uk/rwrme-web-assets")
    SECRETS[:] = [cfg["R2_ACCESS_KEY_ID"], cfg["R2_SECRET_ACCESS_KEY"]]
    return cfg



def client(cfg: dict):
    try:
        import boto3
    except ImportError:
        print("× 这台机器上没装 boto3。装一下：", flush=True)
        print(f"  {sys.executable} -m pip install boto3", flush=True)
        raise SystemExit(1)
    return boto3.client(
        "s3",
        endpoint_url=cfg["R2_ENDPOINT"],
        aws_access_key_id=cfg["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=cfg["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )


def full_key(cfg: dict, name: str) -> str:
    """用户说的对象名 → 桶里的完整 key。

    约定是「对象名就是文件名，不带目录」，所以这里只认一层名字：
    传进来的若已带前缀就不再重复加，带子目录的一律拒绝——免得把文件传进
    一个谁也想不到的位置。
    """
    prefix = cfg["R2_PREFIX"].strip("/")
    name = name.replace("\\", "/").lstrip("/")
    if name == prefix or name.startswith(prefix + "/"):
        return name
    if "/" in name:
        print(f"× 对象名只认一层文件名（{name}）。归档都平铺在 {prefix}/ 下。", flush=True)
        raise SystemExit(1)
    return f"{prefix}/{name}"


def public_url(cfg: dict, name: str) -> str:
    return f"{cfg['R2_PUBLIC_BASE'].rstrip('/')}/{name.lstrip('/')}"


def ask(prompt: str) -> str:
    """问一句；没有键盘可问时（重定向、脚本里）就当是「不」。"""
    try:
        return input(prompt)
    except EOFError:
        return ""


class Progress:
    """上传进度：在同一行里刷新，最多每 0.5 秒重画一次（别把日志刷爆）。"""

    def __init__(self, total: int) -> None:
        self.total = total
        self.last = 0.0

    def __call__(self, sent: int) -> None:
        now = time.time()
        if now - self.last < 0.5 and sent < self.total:
            return
        self.last = now
        pct = 100.0 * sent / self.total if self.total else 100.0
        sys.stdout.write(f"\r     {pct:5.1f}%  {human(sent)} / {human(self.total)}")
        sys.stdout.flush()

    def done(self) -> None:
        sys.stdout.write("\r" + " " * 44 + "\r")
        sys.stdout.flush()


def human(size: int) -> str:
    """按**十进制**给大小（1 MB = 1 000 000 字节）。

    ⚠️ 这里故意不用 1024：页面 `content/download/index.<lang>.md` 上写的是十进制
    （0101.rar 写作 26.2 MB，就是 26 212 902 字节），`r2.bat list` 打出来的数字要能
    直接抄进页面。早先用 1024 时同一份文件这里显示 25.0 MB，和页面上的 26.2 MB
    对不上——`verify` 的大小核对也会因此全是假报警。
    """
    if size >= 1_000_000_000:
        return f"{size / 1e9:.1f} GB"
    if size >= 1_000_000:
        return f"{size / 1e6:.1f} MB"
    if size >= 1_000:
        return f"{size / 1e3:.1f} kB"
    return f"{size} B"


def iter_objects(cfg: dict, s3, prefix: str) -> list:
    """列出前缀下的所有对象（`list_objects_v2` 一次最多 1000 个，这里翻页翻完）。"""
    objects: list = []
    token = None
    while True:
        kwargs = {"Bucket": cfg["R2_BUCKET"], "Prefix": prefix}
        if token:
            kwargs["ContinuationToken"] = token
        out = s3.list_objects_v2(**kwargs)
        objects.extend(out.get("Contents", []))
        if not out.get("IsTruncated"):
            return objects
        token = out.get("NextContinuationToken")
        if not token:
            return objects



# ── 命令 ──────────────────────────────────────────────────────────────────

def cmd_list(cfg: dict, s3, args) -> int:
    prefix = f"{cfg['R2_PREFIX'].strip('/')}/"
    objs = [o for o in iter_objects(cfg, s3, prefix) if o["Size"] > 0]
    if not objs:
        print(f"（{prefix} 下没有东西）")
        return 0
    total = 0
    for o in sorted(objs, key=lambda x: x["Key"]):
        name = o["Key"][len(prefix):]
        total += o["Size"]
        stamp = o["LastModified"].strftime("%Y-%m-%d %H:%M")
        print(f"  {name:<34} {human(o['Size']):>10}  {stamp}")
    print(f"\n  合计 {len(objs)} 个，{human(total)}")
    return 0


def cmd_head(cfg: dict, s3, args) -> int:
    key = full_key(cfg, args.name)
    try:
        h = s3.head_object(Bucket=cfg["R2_BUCKET"], Key=key)
    except Exception as exc:
        code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
        print(f"× 取不到 {key}（{code or type(exc).__name__}）", flush=True)
        return 1
    name = args.name
    print(f"  对象名    {name}")
    print(f"  大小      {human(h['ContentLength'])}  （{h['ContentLength']} 字节）")
    print(f"  类型      {h.get('ContentType', '（没给）')}")
    print(f"  缓存头    {h.get('CacheControl', '（没有）')}")
    print(f"  最后修改  {h['LastModified'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  公开地址  {public_url(cfg, name)}")
    return 0


def put_one(cfg: dict, s3, src: Path, name: str, args, confirm: bool = True) -> tuple:
    """传一个文件。返回 `(是否传了, sha256)`——`upload` 与 `upload-dir` 共用这一段。

    `confirm=False` 用于整批上传：那时已经对整个清单确认过一次了，
    不至于每个文件再问一遍（三个文件问三次很烦）。每个文件的**同名检查**
    不受影响，照样一个一个查。
    """
    key = full_key(cfg, name)

    # 同名会直接覆盖，而归档是冻结的、覆盖找不回来——先查一遍。
    try:
        already = s3.head_object(Bucket=cfg["R2_BUCKET"], Key=key)
    except Exception:
        already = None
    if already is not None and not args.overwrite:
        print(f"  ⚠ 跳过 {name}：线上已经有同名的（"
              f"{human(already['ContentLength'])}，"
              f"{already['LastModified'].strftime('%Y-%m-%d %H:%M')}）", flush=True)
        print("    要覆盖就加 --overwrite，或者换个对象名。", flush=True)
        return False, ""

    size = src.stat().st_size
    if args.content_type:
        ctype = args.content_type
        unknown = False
    else:
        ctype = CONTENT_TYPES.get(src.suffix.lower()) or mimetypes.guess_type(src.name)[0]
        if ctype is None:
            ctype = "application/octet-stream"
            unknown = True
        else:
            unknown = False

    print(f"\n  ── {name}")
    print(f"     大小    {human(size)}  （{size} 字节）")
    print(f"     对象名  {cfg['R2_BUCKET']}/{key}")

    # 先算哈希再传：传错文件是这里唯一会静默出错的地方。
    digest = hashlib.sha256()
    with open(src, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    sha = digest.hexdigest()
    print(f"     sha256  {sha}")
    print(f"     类型    {ctype}" + ("  ← 没认出这个扩展名，可用 --content-type 指定"
                                     if unknown else ""))
    if already is not None:
        print(f"     ⚠ 线上已有同名对象（{human(already['ContentLength'])}），这次会覆盖它")

    if confirm and not args.yes:
        print("     对一眼上面的哈希，和你记的那份一致再传。", flush=True)
        if ask("     上传？[y/N] ").strip().lower() != "y":
            print("     取消了，什么都没传。")
            return False, ""

    extra = {"ContentType": ctype, "CacheControl": CACHE_CONTROL}
    # 归档几十 MB，走分段上传，断了能续；boto3 自己会切。
    from boto3.s3.transfer import TransferConfig
    tcfg = TransferConfig(multipart_threshold=8 * 1024 * 1024)
    t0 = time.time()
    # 几十 MB 的包要传一阵子，终端里一点动静都没有会让人以为卡死了。
    # 只在真的有终端时画进度（重定向/脚本里不画，免得把日志刷花）。
    ticker = Progress(size) if size >= 8 * 1024 * 1024 and sys.stdout.isatty() else None
    s3.upload_file(str(src), cfg["R2_BUCKET"], key, ExtraArgs=extra, Config=tcfg,
                   Callback=ticker)
    if ticker:
        ticker.done()

    h = s3.head_object(Bucket=cfg["R2_BUCKET"], Key=key)
    ok = h["ContentLength"] == size
    print(f"     {'✓' if ok else '×'} 传完（{time.time() - t0:.1f} 秒），线上 "
          f"{h['ContentLength']} 字节，{'与本地一致' if ok else '与本地不一致，去查一下'}")
    return True, sha


def cmd_upload(cfg: dict, s3, args) -> int:
    src = Path(args.file).expanduser()
    if not src.is_file():
        print(f"× 本地没有这个文件：{src}", flush=True)
        return 1

    name = args.name or src.name
    done, sha = put_one(cfg, s3, src, name, args, confirm=True)
    if not done:
        return 1 if not args.yes else 0

    print(f"\n  公开地址  {public_url(cfg, name)}")
    print(f"  页面要写的 sha256：{sha}")
    print("  （改 content/download/index.<lang>.md 那份清单用；存储那边不另存清单。）")
    return 0


def cmd_upload_dir(cfg: dict, s3, args) -> int:
    """把一个文件夹里的文件整批上传——对象名一律取文件名（约定：不带目录）。"""
    root = Path(args.dir).expanduser()
    if not root.is_dir():
        print(f"× 本地没有这个文件夹：{root}", flush=True)
        return 1

    wanted = [p for p in sorted(root.iterdir()) if p.is_file()]
    if args.ext:
        exts = tuple(e.lower() if e.startswith(".") else "." + e.lower() for e in args.ext)
        wanted = [p for p in wanted if p.suffix.lower() in exts]

    # 子目录里还有文件的话，说一声：按约定它们的对象名只能是文件名，
    # 硬传会把同名文件互相覆盖，所以整批上传不往下钻。
    subdirs = [p for p in sorted(root.iterdir()) if p.is_dir()]
    if subdirs and not args.recursive:
        print(f"· 下面还有 {len(subdirs)} 个子文件夹，没往里钻：{', '.join(p.name for p in subdirs[:3])}"
              f"{'…' if len(subdirs) > 3 else ''}", flush=True)
        print("  要连子文件夹一起传就加 --recursive（对象名仍只取文件名，"
              "同名会互相覆盖，慎用）。", flush=True)
    if args.recursive:
        for p in sorted(root.rglob("*")):
            if p.is_file() and p not in wanted:
                wanted.append(p)

    if not wanted:
        print("× 这个文件夹里没有可传的文件。", flush=True)
        return 1

    total = sum(p.stat().st_size for p in wanted)
    print(f"  文件夹    {root}")
    print(f"  待传 {len(wanted)} 个文件，共 {human(total)}：", flush=True)
    for p in wanted:
        print(f"     {p.name}　{human(p.stat().st_size)}", flush=True)

    if args.dry_run:
        print("\n  --dry-run，只是列一下，什么都没传。")
        return 0

    if not args.yes:
        print(f"\n  这 {len(wanted)} 个文件会传成同样名字的对象（缓存头一律长缓存）。", flush=True)
        if ask("  开始传？[y/N] ").strip().lower() != "y":
            print("  取消了，一个都没传。")
            return 0

    done_list, skipped = [], []
    for p in wanted:
        ok, sha = put_one(cfg, s3, p, p.name, args, confirm=False)
        (done_list if ok else skipped).append((p.name, sha))

    print(f"\n✓ 传完 {len(done_list)} 个" + (f"，跳过 {len(skipped)} 个" if skipped else ""), flush=True)
    if done_list:
        print("\n  页面要写的 sha256：")
        for name, sha in done_list:
            print(f"    {sha}  {name}")
        print("\n  （改 content/download/index.<lang>.md 那份清单用；存储那边不另存清单。）")
    return 0


def cmd_sha256(cfg: dict, s3, args) -> int:
    """把线上对象的 sha256 算出来（流式取，不落盘）。

    页面那份哈希表要的就是这个数——文件传完之后，与其在本地另算一遍，
    不如直接问线上：算的就是最终发出去的那些字节。
    """
    ok = True
    for name in args.name:
        key = full_key(cfg, name)
        try:
            resp = s3.get_object(Bucket=cfg["R2_BUCKET"], Key=key)
        except Exception as exc:
            code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
            print(f"× 取不到 {name}（{code or type(exc).__name__}）", flush=True)
            ok = False
            continue
        digest = hashlib.sha256()
        size = 0
        for chunk in resp["Body"].iter_chunks():
            digest.update(chunk)
            size += len(chunk)
        print(f"{digest.hexdigest()}  {name}  （{human(size)}）")
    return 0 if ok else 1


def cmd_delete(cfg: dict, s3, args) -> int:
    key = full_key(cfg, args.name)
    try:
        h = s3.head_object(Bucket=cfg["R2_BUCKET"], Key=key)
    except Exception:
        print(f"× 线上没有 {key}，不用删。", flush=True)
        return 1

    print(f"  即将删除  {cfg['R2_BUCKET']}/{key}")
    print(f"  大小      {human(h['ContentLength'])}")
    print(f"  公开地址  {public_url(cfg, args.name)}")
    if not args.yes:
        print("\n  删了就找不回来了，而且页面上的直链会当场断。", flush=True)
        typed = ask(f"  要删就手打一遍对象名（{args.name}）：").strip()
        if typed != args.name:
            print("  名字对不上，没删。")
            return 0

    s3.delete_object(Bucket=cfg["R2_BUCKET"], Key=key)
    left = s3.list_objects_v2(Bucket=cfg["R2_BUCKET"], Prefix=key).get("Contents", [])
    print(f"✓ 已删除{'' if not left else '，但好像还有残留，再查一次'}")
    return 0


# ── 凭据本身：看一眼来源、把权限收紧 ──────────────────────────────────────

def acl_note(path: Path) -> str:
    """凭据文件的权限是不是太宽。没问题就返回空串。"""
    if os.name == "nt":
        try:
            done = subprocess.run(["icacls", str(path)], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace")
        except OSError:
            return ""
        out = done.stdout or ""
        wide = [who for who in ("BUILTIN\\Users", "Authenticated Users", "Everyone")
                if who in out]
        if wide:
            return ("! 这个文件的权限偏宽（同机任何账户都能读："
                    f"{'、'.join(sorted(set(wide)))}）——跑 r2.bat lock 收紧一下。")
        return ""
    mode = path.stat().st_mode & 0o777
    if mode & 0o077:
        return "! 这个文件的权限偏宽（同机其他账户能读）——chmod 600 收紧一下。"
    return ""


def cmd_creds(cfg: dict, s3, args) -> int:
    """凭据从哪儿读的、长什么样（**值一律打码**，这个命令永远不会打印密钥）。"""
    print(f"  凭据来源  {CREDS_USED if CREDS_USED else '（没有文件：全部来自环境变量）'}")
    print(f"  endpoint  {mask_endpoint(cfg['R2_ENDPOINT'])}")
    print(f"  key id    {mask(cfg['R2_ACCESS_KEY_ID'])}")
    print(f"  secret    {mask(cfg['R2_SECRET_ACCESS_KEY'])}")
    print(f"  桶 / 前缀 {cfg['R2_BUCKET']} / {cfg['R2_PREFIX']}")
    print(f"  公开地址  {cfg['R2_PUBLIC_BASE']}")
    if CREDS_USED:
        note = acl_note(CREDS_USED)
        if note:
            print("  " + note)
    if args.check:
        try:
            probe = client(cfg)
            probe.list_objects_v2(Bucket=cfg["R2_BUCKET"],
                                  Prefix=cfg["R2_PREFIX"].strip("/") + "/", MaxKeys=1)
            print("  ✓ 密钥可用（列得到桶里的东西）")
        except SystemExit:
            pass
        except Exception as exc:
            print(f"  × 密钥用不了：{redact(f'{type(exc).__name__}: {exc}')}")
    print("\n  密钥本身任何命令都不会打印——这里看到的都是打码版。")
    print("  要确认能不能用：r2.bat creds --check（或 r2.bat list）")
    return 0


def cmd_lock(cfg: dict, s3, args) -> int:
    """把凭据文件的权限收紧到只有当前用户（别的本地账户读不到）。"""
    if CREDS_USED is None:
        print("· 凭据不是从文件读的（环境变量），没有文件要收紧。")
        return 0
    path = CREDS_USED
    if os.name == "nt":
        # USERNAME 未必在环境里（从别的地方拉起来时可能没有），拿家目录名兜一下
        who = os.environ.get("USERNAME") or Path.home().name
        if not who:
            print("× 取不到当前用户名。手动跑：")
            print(f'  icacls "{path}" /inheritance:r /grant:r "<你的用户名>:F"')
            return 1
        cmd = ["icacls", str(path), "/inheritance:r", "/grant:r", f"{who}:F"]
    else:
        cmd = ["chmod", "600", str(path)]
    done = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    if done.returncode != 0:
        out = ((done.stdout or "") + (done.stderr or "")).strip()
        print(f"× 没改成功（退出码 {done.returncode}）：{out}")
        print("  改权限要管理员/普通控制台才行——在一个正常的 cmd 窗口里手动跑：")
        print(f'    icacls "{path}" /inheritance:r /grant:r "{who}:F"')
        return 1
    print(f"✓ 已收紧 {path}：继承来的权限都去掉了，只剩你自己能读写。")
    note = acl_note(path)
    if note:
        print("  " + note)
    else:
        print("  现在同机的其他账户读不到这个文件了。")
    return 0


# ── 体检：页面上的直链与哈希，和线上对一遍 ────────────────────────────────

#: 页面里指向对象存储的链接：https://assets.rwr-infra.uk/rwrme-web-assets/<名字>
LINK_RE = re.compile(r"https?://assets\.rwr-infra\.uk/([^\s)\"'<>]+)")
#: 哈希块里的那几行：`<64 位十六进制>  <文件名>`
#: （块缩进在 `??? quote` 里，行首有空格，所以别锚死在第一列）
HASH_RE = re.compile(r"^[ \t]*([0-9a-fA-F]{64})[ \t]+(\S+)[ \t]*$", re.M)
#: 表格里的 `文件名`　26.2 MB —— 页面上的大小标签（十进制）
SIZE_RE = re.compile(r"`([^`]+?)`[\s\u3000]*([\d.]+)[\u3000 ]*(GB|MB|kB)")
UNITS = {"B": 1.0, "kB": 1e3, "MB": 1e6, "GB": 1e9}


def scan_page(path: Path, prefix: str) -> dict:
    """把一个页面里跟对象存储有关的东西读出来：链接、哈希表、大小标签。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    links = set()
    for m in LINK_RE.finditer(text):
        key = m.group(1).strip()
        if key.startswith(prefix + "/"):
            key = key[len(prefix) + 1:]
        if key:
            links.add(key)
    hashes = {m.group(2): m.group(1).lower() for m in HASH_RE.finditer(text)}
    sizes = {}
    for m in SIZE_RE.finditer(text):
        sizes.setdefault(m.group(1), float(m.group(2)) * UNITS[m.group(3)])
    return {"path": path, "links": links, "hashes": hashes, "sizes": sizes}


def sha256_online(s3, bucket: str, key: str) -> tuple:
    """把线上对象流式读一遍算 sha256（不落盘），返回 (哈希, 字节数)。"""
    body = s3.get_object(Bucket=bucket, Key=key)["Body"]
    digest = hashlib.sha256()
    size = 0
    for chunk in body.iter_chunks():
        digest.update(chunk)
        size += len(chunk)
    return digest.hexdigest(), size


def cmd_verify(cfg: dict, s3, args) -> int:
    """页面 ⇄ 线上对一遍。

    为什么要它：站外那十几条直链**不在 CI 体检范围内**（`linkcheck` 够不着别的域），
    页面上写的哈希也没人复核。手工点一遍十几条链接不现实，漏了就等读者发现。
    这里一次说清：哪条链接线上没有、哪个对象没人链、哈希对不对、大小标签有没有
    写错、各语言的页面有没有改漏。
    """
    prefix = cfg["R2_PREFIX"].strip("/")
    # 三种语言的页面都看：链接/哈希是同一批，正好用来查「英文页有没有改漏」。
    pages = sorted((PROJECT / "content").rglob("*.md"))
    scans = [scan_page(p, prefix) for p in pages]
    if not scans:
        print(f"× 在 {PROJECT / 'content'} 下没找到要看的页面。", flush=True)
        return 1

    online = {o["Key"][len(prefix) + 1:]: o
              for o in iter_objects(cfg, s3, prefix + "/") if o["Size"] > 0}

    linked: set = set()
    for scan in scans:
        linked |= scan["links"]
    linked_hash: dict = {}
    for scan in scans:
        for name, sha in scan["hashes"].items():
            linked_hash.setdefault(name, sha)

    problems = 0

    def head(title: str) -> None:
        print(f"\n  {title}", flush=True)

    print(f"  页面    {len(scans)} 个（content/ 下的 *.md）")
    print(f"  线上    {len(online)} 个对象，{human(sum(o['Size'] for o in online.values()))}")

    # 1. 链接指到线上不存在的对象 —— 读者点开就是 404，最要紧的一条
    missing = sorted(linked - set(online))
    head(f"✗ 页面链了、线上没有（点开 404）：{len(missing)} 条" if missing
         else f"✓ 页面上每条链接线上都有（{len(linked)} 条）")
    for name in missing:
        print(f"      {name}")
    problems += len(missing)

    # 2. 线上有、页面没人链（可能是漏挂，也可能是历史遗留）
    orphans = sorted(set(online) - linked)
    if orphans:
        head("! 线上有、页面里没人链（漏挂还是遗留？）：")
        for name in orphans:
            print(f"      {name:<34} {human(online[name]['Size']):>10}")

    # 3. 哈希表与链接对不上
    no_hash = sorted(linked - set(linked_hash))
    no_link = sorted(set(linked_hash) - linked)
    if no_hash:
        head("! 页面链了、但哈希表里没有这一条：")
        for name in no_hash:
            print(f"      {name}")
        problems += len(no_hash)
    if no_link:
        head("! 哈希表里有、页面里没有链接：")
        for name in no_link:
            print(f"      {name}")

    # 4. 大小标签（页面写的是十进制；差 1.5% 以上就当作写错了）
    sizes: dict = {}
    for scan in scans:
        for name, want in scan["sizes"].items():
            sizes.setdefault(name, want)
    wrong_size = []
    for name, want in sorted(sizes.items()):
        obj = online.get(name)
        if obj is None or not want:
            continue
        if abs(want - obj["Size"]) / obj["Size"] > 0.015:
            wrong_size.append((name, want, obj["Size"]))
    if wrong_size:
        head(f"! 大小标签与线上对不上（{len(wrong_size)} 条）：")
        for name, want, real in wrong_size:
            print(f"      {name:<34} 页面 {human(int(want)):>10} / 线上 {human(real):>10}")
        problems += len(wrong_size)
    else:
        head(f"✓ 页面上的大小标签与线上一致（{len(sizes)} 条，十进制）")

    # 5. 各语言的页面有没有改漏：同目录、同名页面之间比链接与哈希
    groups: dict = {}
    for scan in scans:
        stem = scan["path"].name.split(".")[0]
        groups.setdefault((scan["path"].parent, stem), []).append(scan)
    for (parent, stem), group in sorted(groups.items(), key=lambda kv: str(kv[0])):
        if len(group) < 2:
            continue
        base = group[0]
        for other in group[1:]:
            lost = base["links"] - other["links"]
            extra = other["links"] - base["links"]
            drift = [n for n, sha in base["hashes"].items()
                     if n in other["hashes"] and other["hashes"][n] != sha]
            if lost or extra or drift:
                head(f"! {parent.name}/{stem}: {base['path'].name} 与 "
                     f"{other['path'].name} 不一致")
                for name in sorted(lost):
                    print(f"      只在 {base['path'].name} 里链了：{name}")
                for name in sorted(extra):
                    print(f"      只在 {other['path'].name} 里链了：{name}")
                for name in sorted(drift):
                    print(f"      哈希两边不一样：{name}")
                problems += 1

    # 6. 哈希本身对不对（可选：要把线上文件整个读一遍）
    if args.hash:
        todo = sorted(n for n in linked if n in online and n in linked_hash)
        if args.only:
            todo = [n for n in todo if n in set(args.only)]
        total = sum(online[n]["Size"] for n in todo)
        head(f"正在核对哈希（从线上流式读 {len(todo)} 个文件，约 {human(total)}）…")
        bad = []
        for i, name in enumerate(todo, 1):
            print(f"      [{i}/{len(todo)}] {name} … ", end="", flush=True)
            try:
                sha, size = sha256_online(s3, cfg["R2_BUCKET"],
                                          f"{prefix}/{name}")
            except Exception as exc:
                print(f"× 取不到（{redact(type(exc).__name__)}）")
                bad.append((name, "取不到"))
                continue
            if sha == linked_hash[name]:
                print("✓")
            else:
                print("✗")
                bad.append((name, f"页面 {linked_hash[name][:12]}… / 线上 {sha[:12]}…"))
        if bad:
            head("✗ 哈希对不上：")
            for name, why in bad:
                print(f"      {name:<34} {why}")
            problems += len(bad)
        else:
            print(f"      ✓ {len(todo)} 个全对")

    print()
    if problems:
        print(f"× 有 {problems} 处要对一下。", flush=True)
        return 1
    print("✓ 页面上那些直链、哈希、大小标签，和线上都对得上。", flush=True)
    if not args.hash:
        print("  （哈希本身没核——加 --hash 会把线上文件流式读一遍再算一遍。"
              "十几条链接就 300 MB 左右，慢一些。）")
    return 0


# ── 入口 ──────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        prog="r2", description="R2 上的归档：上传 / 删除 / 查看")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="列出线上都有什么")
    p.set_defaults(func=cmd_list, needs_s3=True)

    p = sub.add_parser("head", help="看一个文件的大小、类型、缓存头、公开地址")
    p.add_argument("name")
    p.set_defaults(func=cmd_head, needs_s3=True)

    p = sub.add_parser("upload", help="上传一个文件（对象名默认就是文件名）")
    p.add_argument("file", help="本地文件路径")
    p.add_argument("name", nargs="?", help="对象名，默认取文件名")
    p.add_argument("--content-type", help="覆盖自动推断的 Content-Type")
    p.add_argument("--overwrite", action="store_true",
                   help="线上已有同名对象时也照传（默认会拒绝，防止误覆盖冻结的归档）")
    p.add_argument("--yes", action="store_true", help="不问直接传（脚本里用）")
    p.set_defaults(func=cmd_upload, needs_s3=True)

    p = sub.add_parser("upload-dir", help="把一个文件夹里的文件整批上传（对象名一律取文件名）")
    p.add_argument("dir", help="本地文件夹路径")
    p.add_argument("--ext", nargs="+", metavar="后缀",
                   help="只传这些后缀的，例如 --ext .asmb .svg")
    p.add_argument("--recursive", action="store_true",
                   help="连子文件夹里的文件一起传（对象名仍只取文件名，同名会覆盖）")
    p.add_argument("--dry-run", action="store_true", help="只列出要传什么，不真传")
    p.add_argument("--content-type", help="覆盖自动推断的 Content-Type（整批同一个）")
    p.add_argument("--overwrite", action="store_true", help="线上已有同名对象时也照传")
    p.add_argument("--yes", action="store_true", help="不问直接传")
    p.set_defaults(func=cmd_upload_dir, needs_s3=True)

    p = sub.add_parser("sha256", help="算线上对象的 sha256（页面那份哈希表用这个数）")
    p.add_argument("name", nargs="+")
    p.set_defaults(func=cmd_sha256, needs_s3=True)

    p = sub.add_parser("delete", help="删除一个对象（要手打一遍名字才肯删）")
    p.add_argument("name")
    p.add_argument("--yes", action="store_true", help="不问直接删（慎用）")
    p.set_defaults(func=cmd_delete, needs_s3=True)

    p = sub.add_parser("verify", help="页面上的直链、哈希、大小与线上对一遍")
    p.add_argument("--hash", action="store_true",
                   help="连哈希一起核（把线上文件流式读一遍再算，300 MB 左右，慢）")
    p.add_argument("--only", nargs="+", metavar="名字",
                   help="只核这几个（例如 --only vdao.svg，配 --hash 用来抽样）")
    p.set_defaults(func=cmd_verify, needs_s3=True)

    p = sub.add_parser("creds", help="看凭据是从哪儿读的（值打码，不打印密钥）")
    p.add_argument("--check", action="store_true", help="顺手试一下密钥能不能用")
    p.set_defaults(func=cmd_creds)

    p = sub.add_parser("lock", help="把凭据文件的权限收紧到只有你自己")
    p.set_defaults(func=cmd_lock)

    args = ap.parse_args()
    cfg = load_creds()
    s3 = client(cfg) if getattr(args, "needs_s3", False) else None
    try:
        return args.func(cfg, s3, args)
    except KeyboardInterrupt:
        print("\n停了。")
        return 130
    except Exception as exc:
        code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
        # 过一遍 redact：万一哪层库把密钥塞进了异常信息，也不会留在终端/日志里。
        print(redact(f"× 出错了：{code or type(exc).__name__}  {exc}"), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
