#!/usr/bin/env python3
"""版本清单：`zensical.toml` 声明，`content/` 落内容，两边由 audit() 对齐。

为什么版本清单写在配置里而不是 content/ 里
--------------------------------------------
语言清单是从 `content/` 的**文件名后缀**推导的（见 tools/langs.py），因为一门语言的
存在与否，一篇内容就说得清楚。版本不一样：一个版本**没有任何内容也成立**——它只是
「地编还没出这一版的说明」而已。所以版本是站点的一件配置，跟 `extra.alternate`
（语言切换器的显示名）同一个去处。

代价是「声明」与「内容」成了两处，**这正是 audit() 存在的理由**：任何一边多出来、
少下去、名字对不上，都以非零码退出，不会静默分成两家账。

三个概念
--------
    current   当前版。内容就在 `content/` 根下，产物落在 docs/ 根，网址没有前缀。
    archived  非当前版。内容在 `content/versions/<id>/`，产物落在 docs/<id>/。
    语言      与版本正交。默认语言没有前缀，其余语言各自一层，所以某一页的产物在
              docs/[<版本>/][<语言>/]<名字>.md，最多两层前缀。

    版本在**前**、语言在**后**：
        /                     当前版 · 简体
        /en/                  当前版 · 英文
        /0101/                0101 版 · 简体
        /0101/en/             0101 版 · 英文

    「版本在前」是为了让当前版的简体（也就是绝大多数人看的那一支）保持在最浅的
    地址上；调过来会把它推到 /zh-hans/ 下面去。

为什么非当前版是整棵冻结的树，而不是「只写改动」
------------------------------------------------
地编的手册是**跟着工具版本走的**：读者装的是 0101，就该看到 0101 的说明。
所以砍一版就是当时那棵树的一份快照，之后再不回改。等到某一版的页面集合与
当前版对不上时，由 tools/docsgen.py 给缺失的页补一个跳转桩，而不是让切换器
把人送进 404。
"""

from __future__ import annotations

import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
CONFIG = ROOT / "zensical.toml"

#: 非当前版的落点。`content/versions/` 下的每个子目录就是一个非当前版。
#: 当前版没有目录——它就是 content/ 根，这样默认语言的网址才停在最浅处。
ARCHIVE = CONTENT / "versions"

#: 版本 id 的合法形式。它要当网址的一段目录名，所以只留 URL 里不需要转义的字符。
#: 点只允许出现在中间（`1.0` 可以，`.hidden` 不行）——末段带点的引用会被
#: overrides/partials/trailing-slash.html 当成文件而放过，那样地址补正就失效了。
VERSION_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._-]*[A-Za-z0-9_]$|^[A-Za-z0-9_]$")


@dataclass(frozen=True)
class Version:
    """一个版本。除了 id，都是给切换器与页脚看的显示信息。"""

    id: str
    label: str
    date: str = ""
    #: 当前版在清单里**不写** `current = true`——不写就是非当前版，写了才是当前版。
    #: 反过来（默认当前、显式标历史）会让「多标了一个」这种错变成静默的：
    #: 两个 current 时第一个赢，另一个悄悄降级成非当前版，网址却不是那么回事。
    current: bool = False


# ── 读取 ──────────────────────────────────────────────────────────────────

def declared() -> list[Version]:
    """读 zensical.toml 里的 [[project.extra.version]]，保持清单里的书写顺序。

    顺序就是切换器里的显示顺序：最新的排在最前。声明顺序由人决定，不排序——
    版本号不是都能比大小的（`vao0822` 与 `0101` 谁大？只有作者知道）。
    """
    with CONFIG.open("rb") as handle:
        config = tomllib.load(handle)
    raw = config.get("project", {}).get("extra", {}).get("version") or []
    versions: list[Version] = []
    for entry in raw:
        versions.append(
            Version(
                id=str(entry.get("id", "")).strip(),
                label=str(entry.get("label", "")).strip(),
                date=str(entry.get("date", "")).strip(),
                current=bool(entry.get("current", False)),
            )
        )
    return versions


#: `[[project.extra.version]]` 条目里认得的键。多出来的键是**别的配置被 TOML 收错了**。
KNOWN_KEYS = {"id", "label", "date", "current"}


def stray_keys() -> list[str]:
    """版本条目里出现了不认识的键 —— 几乎一定是被 TOML 吞进来的别处配置。

    TOML 的规矩：`[[project.extra.version]]` 一开，后面所有裸键都归**最后那一个
    版本条目**，不再回到 `[project.extra]`。于是把 `translation_in_progress` 写在
    版本清单后面，它就成了某个版本的字段，而 zensical.toml 看上去完全正常、
    构建也一声不吭——只是那条配置永远不起作用。这处踩过一次：
    `translation_in_progress` 被判成版本字段，「仍在补齐的语种」因此没生效，
    构建照样因为漏翻而红，而原因在配置里根本看不出来。
    """
    with CONFIG.open("rb") as handle:
        config = tomllib.load(handle)
    raw = config.get("project", {}).get("extra", {}).get("version") or []
    problems: list[str] = []
    for entry in raw:
        for key in sorted(set(entry) - KNOWN_KEYS):
            problems.append(
                f"[[project.extra.version]] 的条目 {entry.get('id', '(无 id)')!r} 里出现了"
                f"不认识的键 “{key}”：多半是某条配置被 TOML 收进了这张表"
                f"（子表一开，后面的裸键就归它了），挪到 [project.extra] 的裸键区去"
            )
    return problems


def current() -> Version | None:
    """当前版：清单里唯一标了 `current = true` 的那一条。"""
    found = [v for v in declared() if v.current]
    return found[0] if found else None


def archived() -> list[Version]:
    """非当前版，按声明顺序。"""
    return [v for v in declared() if not v.current and v.id]


def all_versions() -> list[Version]:
    return declared()


# ── 路径 ──────────────────────────────────────────────────────────────────

def source_root(version: Version) -> Path:
    """某个版本的手写内容根。当前版就是 content/ 本身。"""
    return CONTENT if version.current else ARCHIVE / version.id


def url_prefix(version: Version) -> str:
    """该版本的网网址前缀（带尾斜杠，当前版为空串）。"""
    return "" if version.current else f"{version.id}/"


def docs_prefix(version: Version) -> str:
    """该版本的产物相对 docs/ 的目录前缀（带尾斜杠，当前版为空串）。"""
    return url_prefix(version)


def depth(version: Version, lang: str, default_lang: str) -> int:
    """产物相对 docs/ 下沉几层。共享资产的相对链接就补这么多 `../`。"""
    return (0 if version.current else 1) + (0 if lang == default_lang else 1)


def version_of_id(version_id: str) -> Version | None:
    for version in declared():
        if version.id == version_id:
            return version
    return None


# ── 体检 ──────────────────────────────────────────────────────────────────

def audit(default_lang: str, other_lang_dirs: tuple[str, ...] = ()) -> list[str]:
    """把「声明」与「content/ 里真实存在的目录」对齐，返回问题清单。

    三类问题，每一类都是构建期就能定的，没有一类需要等到读者点到才发现：

      1. 清单本身不成立（没有当前版、当前版多于一个、id 不合法或重复）；
      2. 声明了非当前版但 `content/versions/<id>/` 不在（切换器会指向一个空目录）；
      3. `content/versions/<id>/` 在，但清单里没声明（内容写了却上不了线）。

    还有一条不在这张单子里、由 docsgen 管：版本 id 不能与当前版顶层的分区名
    或语言目录同名，否则产物路径会叠在一起。那属于「生成时才知道」，见
    tools/docsgen.py 的 collisions()。
    """
    problems: list[str] = stray_keys()
    versions = declared()

    if not versions:
        problems.append("zensical.toml 的 [[project.extra.version]] 一条都没有：没有任何版本被声明")
    currents = [v for v in versions if v.current]
    if len(currents) == 0:
        problems.append("没有版本标了 current = true：当前版必须是清单里明确的那一条")
    elif len(currents) > 1:
        names = "、".join(v.id or "(空 id)" for v in currents)
        problems.append(f"有 {len(currents)} 个版本标了 current = true（{names}）：当前版只能有一个")

    seen: set[str] = set()
    for version in versions:
        if not version.id:
            problems.append(f"版本 id 为空（label = “{version.label}”）")
            continue
        if not VERSION_RE.match(version.id):
            problems.append(f"版本 id “{version.id}” 不能当网址的一段目录名（只允许字母数字与 _ . -）")
        if version.id in seen:
            problems.append(f"版本 id “{version.id}” 重复声明")
        seen.add(version.id)
        if not version.label:
            problems.append(f"版本 “{version.id}” 没有 label：切换器上会显示不出名字")
        if version.id in other_lang_dirs:
            problems.append(f"版本 id “{version.id}” 与语言目录同名：产物会落在同一处")

    on_disk = {p.name for p in ARCHIVE.iterdir() if p.is_dir()} if ARCHIVE.is_dir() else set()
    for version in archived():
        if version.id and version.id not in on_disk:
            problems.append(
                f"声明了版本 “{version.id}”，但 content/versions/{version.id}/ 不存在："
                f"切换器会指向一个空目录"
            )
    declared_ids = {v.id for v in versions}
    for name in sorted(on_disk - declared_ids):
        problems.append(
            f"content/versions/{name}/ 有内容，但 zensical.toml 里没声明这个版本："
            f"它不会被生成，也不会出现在切换器里"
        )

    return problems


def main() -> int:
    from langs import DEFAULT_LANG, other_languages

    problems = audit(DEFAULT_LANG, tuple(other_languages()))
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)

    versions = declared()
    if problems:
        print(f"\n版本清单体检：{len(problems)} 个问题", file=sys.stderr)
        return 1

    mark = "（当前版）"
    print(f"版本清单体检：{len(versions)} 个版本")
    for version in versions:
        tail = f"　{version.date}" if version.date else ""
        print(f"  {version.id:<12} {version.label}{tail}{mark if version.current else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
