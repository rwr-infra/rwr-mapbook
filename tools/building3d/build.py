# -*- coding: utf-8 -*-
"""
把地编模板 vao0822.svg 里的 Building 定义，整理成站点 3D 预览要用的数据。

模板里有两种我们关心的东西：
  1. `id="material_XXX"` 的 <desc>——每一栋建筑的属性：
       name / color / detail_texture(+cell,scale) / 1st_floor_1..4 / other_floor_1..4 /
       roof_texture(+cell,scale) / roof_color …
  2. `id="texture_groups__XXX"` 的 <desc>——「单元名 = 列,行」的图集坐标表，
     例如 apartment1_1st_floor_door = 2,0。有了它，建筑每层引用的 style 名
     才能落到图集的具体格子上（游戏资源里只存名字，不存坐标，就靠模板这张表）。

输出：docs/b3d/data.json（与 3D 预览用到的贴图放一起，页面运行时 fetch）。
"""

import os
import glob
import re
import json
import shutil

#: 这个脚本在 `<仓库>/tools/building3d/build.py`，往上两级是仓库根。
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(os.path.dirname(HERE))

TEMPLATE = r"D:\RWRMap\0100\1007_Data\templates\vao0822.svg"
GAME = r"D://steam//steamapps//common//RunningWithRifles"
GAME_TEX = os.path.join(GAME, "media", "packages", "vanilla", "textures")
#: 站点侧全在 docs/b3d/：viewer.js、data.json 与所有贴图同住一处，
#: 前端只认这一个目录（docs/b3d/viewer.js 里 BASE + "b3d/"）。
OUT_DIR = os.path.join(PROJECT, "docs", "b3d")

# 模板没写 atlas_texture 时用的默认墙体图集（参数字典里列的三种之一）
DEFAULT_ATLAS = "building_atlas2.png"
# ⚠️ normandy / provence / tropical 三张图集是跟着特定地图目录走的**极特殊素材**，
#    不进通用模板体系：相关材质、style、单元坐标与贴图全部排除在预览之外。
SPECIAL_ATLASES = {
    "building_atlas_normandy.png",
    "building_atlas_provence.png",
    "building_atlas_tropical.png",
}
# 这三个系列的名字直接出现在材质名 / style 名 / 单元名里
SPECIAL_PAT = re.compile(r"normandy|provence|tropical", re.I)
MAP_SVGS = [r"D:\RWRMap\0100\1007_Data\map\objects.svg"]
GRID = [8, 8]        # 单元坐标表是 8 列（列号 0..7）；图集 256×256 → 每格 32px
# 各图集真实的网格（换图集时前端自动匹配，不用手数）：
#   building 系都是 8×8（building_atlas4 是 512px，格子 64px）；world_atlas1 是 16×16
ATLAS_GRIDS = {
    "building_atlas.png": [8, 8],
    "building_atlas2.png": [8, 8],
    "building_atlas3.png": [8, 8],
    "building_atlas4.png": [8, 8],
    "building_atlas_desert.png": [8, 8],
    "world_atlas1.png": [16, 16],
}
# 图集「原生格」跨度（宽格, 高格）：坐标表里 1 个单位 = 1 宽 × 2 高 的基础格。
# building_atlas2/3/4 三张统一按 1×2 编号（此前只有 atlas2 标了，atlas3 被当成
# 1×1 → 窗全落在空格上，整面墙没窗；atlas4 的坐标也跟着错位）。这里做成数据，
# 让 Python 与前端 JS 走同一份配置，不再在 JS 里另写一份 DEFAULT_SPANS。
ATLAS_SPANS = {
    "building_atlas2.png": [1, 2],
    "building_atlas3.png": [1, 2],
    "building_atlas4.png": [1, 2],
}
# 个别单元的真实切分与所在图集的默认跨度不同 → 按「图集 → 单元」单独列出。
# 当前三张图集统一 1×2，没有需要回退的单元；渲染层（styleTexture）会把窗/门
# 的不透明内容竖向拉满整格（触顶触底），所以无需在此做 1×1 例外。保留结构以备
# 将来个别单元微调。
ATLAS_UNIT_SPANS = {}


def parse_kv(text):
    """`k = v; k2 = v2` → dict。带注释的 `# xxx;` 段跳过。"""
    out = {}
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk or "=" not in chunk or chunk.startswith("#"):
            continue
        k, _, v = chunk.partition("=")
        k, v = k.strip(), v.strip()
        if not k:
            continue
        if k in out:
            if isinstance(out[k], list):
                out[k].append(v)
            else:
                out[k] = [out[k], v]
        else:
            out[k] = v
    return out


def first_token(value, fallback=""):
    """取第一个 token（值里常带格子参数：`wall_atlas1.png 2 0 8 8`），空值给回退值。"""
    parts = str(value or "").split()
    return parts[0] if parts else fallback

def main():
    svg = open(TEMPLATE, encoding="utf-8", errors="replace").read()

    # 1) 图集单元坐标表：`empty = 0,0; shop1_l = 0,1 2,1 ...`
    cells = {}
    for gid, body in re.findall(r'<desc\s+id="texture_groups__([^"]+)"[^>]*>(.*?)</desc>',
                                svg, re.S):
        group = {}
        for chunk in body.split(";"):
            chunk = chunk.strip()
            if "=" not in chunk:
                continue
            name, _, val = chunk.partition("=")
            name, val = name.strip(), val.strip()
            if not name or not re.match(r"^[\d,\s]+$", val):
                continue
            # 一个单元可能有多个位置（序列），取第一个当代表
            first = val.split()[0]
            col, _, row = first.partition(",")
            try:
                group[name] = [int(col), int(row)]
            except ValueError:
                continue
        if group:
            cells[gid] = group

    # 1.5) style（一栋楼一面墙的贴图 = 一串基础单元横向拼起来）：
    #      `name = factory1_1st_floor; sequence = a; sequence = b, c; ...`
    styles = {}
    for sid, body in re.findall(r'<desc\s+id="building_style_([^"]+)"[^>]*>(.*?)</desc>',
                                svg, re.S):
        name = None
        seq = []
        for chunk in body.split(";"):
            chunk = chunk.strip()
            if not chunk or "=" not in chunk:
                continue
            k, _, v = chunk.partition("=")
            k, v = k.strip(), v.strip()
            if k == "name":
                name = v
            elif k == "sequence":
                seq.append([u.strip() for u in v.split(",") if u.strip()])
        if name and seq:
            styles[name] = seq

    # 1.6) ⚠️ BuildingBritish 等系列引用的单元（house_normandy_* 等）坐标表
    #      不在模板里、跟着别的包地图走（edelweiss 等）——扫一遍所有包的
    #      objects.svg，把 texture_groups（坐标表）与 building_style（贴图序列）
    #      都补进来。同名以先出现的为准；太大的文件跳过（防卡死）。
    for svg_path in sorted(glob.glob(os.path.join(
            GAME, "media", "packages", "*", "maps", "*", "objects.svg"))):
        try:
            if os.path.getsize(svg_path) > 15 * 1024 * 1024:
                continue
            other = open(svg_path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if "texture_groups__" not in other and "building_style_" not in other:
            continue
        for gid, body in re.findall(
                r'<desc\s+id="texture_groups__([^"]+)"[^>]*>(.*?)</desc>',
                other, re.S):
            # ⚠️ 先收进独立的组 dict 再并回 cells：直接 cells.setdefault(name, [c,r])
            #    会把 cells 的 value 从 dict 变成 list，后面 data 构造直接崩
            newgroup = cells.setdefault("extra_" + gid, {})
            for chunk in body.split(";"):
                chunk = chunk.strip()
                if "=" not in chunk:
                    continue
                name, _, val = chunk.partition("=")
                name, val = name.strip(), val.strip()
                if not name or name in newgroup:
                    continue
                first = val.split()[0] if val.split() else ""
                col, _, row = first.partition(",")
                try:
                    newgroup[name] = [int(col), int(row)]
                except ValueError:
                    continue
        for sid, body in re.findall(
                r'<desc\s+id="building_style_([^"]+)"[^>]*>(.*?)</desc>',
                other, re.S):
            name = None
            seq = []
            for chunk in body.split(";"):
                chunk = chunk.strip()
                if "=" not in chunk:
                    continue
                k, _, v = chunk.partition("=")
                k, v = k.strip(), v.strip()
                if k == "name":
                    name = v
                elif k == "sequence":
                    seq.append([u.strip() for u in v.split(",") if u.strip()])
            if name and seq and name not in styles:
                styles[name] = seq
        print("  扫描 %s：单元 %d / style %d" % (
            os.path.relpath(svg_path, GAME), len(cells), len(styles)))

    # 1.7) ⚠️ 极特殊素材（normandy/provence/tropical）相关的 style 直接剔除：
    #      名字带这三词的，以及 sequence 里引用了 normandy_* 单元的。
    #      放在所有来源扫完之后——别的包地图会把同名 style 再次塞回来。
    dropped_styles = [n for n in styles
                      if SPECIAL_PAT.search(n)
                      or any(SPECIAL_PAT.search(u) for item in styles[n] for u in item)]
    for n in dropped_styles:
        del styles[n]
    if dropped_styles:
        print("  剔除极特殊素材 style %d 个：%s" % (len(dropped_styles), ", ".join(sorted(dropped_styles))))

    # 2) 建筑定义
    materials = {}
    order = []
    # ⚠️ 扫两遍：① 模板 vao0822.svg（基础定义）；② 地图 objects.svg（带
    #    atlas_texture 与真实 fill/stroke，用来补模板缺的信息）。第二遍 override。
    sources = [svg]
    for p in MAP_SVGS:
        if os.path.exists(p):
            try:
                sources.append(open(p, encoding="utf-8", errors="replace").read())
                print("  扫描地图 %s" % p)
            except OSError:
                pass
    for src_i, src in enumerate(sources):
        override = src_i > 0
        # 先收一遍所有 material rect 的 style，拿到 fill/stroke 的实际色值——
        # desc 里的 color/roof_color 只是「fill 还是 stroke」的语义开关
        rect_styles = {}
        for tag in re.finditer(r'<rect[^>]*\bid="(material_[^"]+)"([^>]*)>', src):
            sid, attrs = tag.group(1), tag.group(2)
            f = re.search(r'fill:\s*(#[0-9a-fA-F]{3,8})', attrs)
            s = re.search(r'stroke:\s*(#[0-9a-fA-F]{3,8})', attrs)
            rect_styles[sid] = {"fill": f.group(1) if f else "",
                                "stroke": s.group(1) if s else ""}
        for mid, body in re.findall(r'<desc\s+id="material_([^"]+)"[^>]*>(.*?)</desc>',
                                    src, re.S):
            kv = parse_kv(body)
            name = kv.get("name")
            # ⚠️ 不能按 Building 前缀过滤：2020 系列等不带 Building 的也是建筑。
            #    判据用字段：有楼层/屋顶字段的才是建筑（树、桶等杂物没有）。
            if not name or ("1st_floor" not in kv and "other_floor" not in kv
                            and "roof_texture" not in kv):
                continue
            # desc id 形如 material_n_2020Busy_desc_1 → 对应 rect id material_n_2020Busy
            sty = rect_styles.get("material_" + re.sub(r"_desc_\d+$", "", mid), {})
            if name in materials:
                # 第二遍（地图 objects.svg）只补更具体的信息：图集与色值
                old = materials[name]
                if kv.get("atlas_texture"):
                    old["atlas_texture"] = first_token(kv.get("atlas_texture"),
                                                       old["atlas_texture"])
                if not old.get("fill") and sty.get("fill"):
                    old["fill"], old["stroke"] = sty["fill"], sty["stroke"]
                continue
            # 墙纹理（detail_*）与屋顶（roof_*）的格子可能带 5/6 个数
            def cell_of(prefix):
                raw = kv.get(prefix + "_atlas_cell")
                if not raw:
                    return None
                parts = str(raw).split()
                try:
                    nums = [float(x) for x in parts[:6]]
                except ValueError:
                    return None
                while len(nums) < 6:
                    nums.append(0.0)     # [列,行,总列,总行,边距u,边距v]，边距=UV 内缩防串色
                return nums
            materials[name] = {
                "color": kv.get("color", "fill"),
                "color_variance": kv.get("color_variance", ""),
                "fill": sty.get("fill", ""),
                "stroke": sty.get("stroke", ""),
                "detail_texture": first_token(kv.get("detail_texture"), "wall_atlas1.png"),
                "detail_cell": cell_of("detail_texture"),
                "detail_scale": str(kv.get("detail_texture_scale", "3 3")),
                # 墙面 detail 遮罩上再叠的 cutout（channel 指用哪条通道当遮罩，1=G）
                "detail_cutout": first_token(kv.get("detail_cutout_texture"), ""),
                "detail_cutout_channel": kv.get("detail_cutout_texture_channel", "1"),
                "detail_cutout_scale": str(kv.get("detail_cutout_texture_scale", "")),
                "atlas_texture": first_token(kv.get("atlas_texture"), DEFAULT_ATLAS),
                "floors": {
                    "1st": [kv.get(f"1st_floor_{i}", "") for i in (1, 2, 3, 4)],
                    "other": [kv.get(f"other_floor_{i}", "") for i in (1, 2, 3, 4)],
                },
                "roof": {
                    "texture": first_token(kv.get("roof_texture"), "wall_atlas1.png"),
                    "cell": cell_of("roof_texture"),
                    "scale": str(kv.get("roof_scale", kv.get("roof_texture_scale", "6 6"))),
                    "color": kv.get("roof_color", "stroke"),
                    # 屋顶遮罩上面还有一层 cutout（channel=1 走 alpha）：
                    # 遮罩决定明暗、cutout 决定斑驳，两层 alpha 相乘才是游戏里的屋顶
                    "cutout": first_token(kv.get("roof_cutout_texture"), ""),
                    "cutout_channel": kv.get("roof_cutout_texture_channel", "1"),
                    "cutout_scale": str(kv.get("roof_cutout_texture_scale", "")),
                },
            }
            order.append(name)

    # 2.5) ⚠️ 极特殊素材的材质整栋剔除：图集是这三张的，或者楼层引用了
    #      已被剔除的 style（引用链断了留着也没法画）
    dropped_mats = [n for n, m in materials.items()
                    if m["atlas_texture"] in SPECIAL_ATLASES
                    or any(s and s not in styles
                           for grp in m["floors"].values() for s in grp)]
    for n in dropped_mats:
        del materials[n]
    order = [n for n in order if n in materials]
    if dropped_mats:
        print("  剔除极特殊素材材质 %d 个：%s" % (len(dropped_mats), ", ".join(sorted(dropped_mats))))

    # 单元坐标表同样剔除 normandy_* 等极特殊单元（provence/tropical 的 style
    # 用的都是共享的 house_* 单元，跟着 style 一起走，这里按名字兜一遍）
    cells_all = {k: v for group in cells.values() for k, v in group.items()
                 if not SPECIAL_PAT.search(k)}

    data = {
        "source": os.path.basename(TEMPLATE),
        "atlas_grid": GRID,
        "atlas_grids": ATLAS_GRIDS,
        "atlas_spans": ATLAS_SPANS,
        "atlas_unit_spans": ATLAS_UNIT_SPANS,
        "default_atlas": DEFAULT_ATLAS,
        # 单元名全局唯一，直接把所有组的坐标并到一起（组 key 带 _desc_1 后缀，
        # 别按名字精确取，取不到就 0 条）
        "cells": cells_all,
        "styles": styles,
        "cell_groups": sorted(cells.keys()),
        "materials": materials,
        "order": order,
    }
    os.makedirs(OUT_DIR, exist_ok=True)

    # 3) 预览要用的贴图原图拷进站点（跟 data.json 放一起）
    needed = set([DEFAULT_ATLAS, "wall_atlas1.png", "cutout.png"])
    for m in materials.values():
        needed.add(m["atlas_texture"])
        needed.add(m["detail_texture"])
        needed.add(m["roof"]["texture"])
        if m.get("detail_cutout"):
            needed.add(m["detail_cutout"])
        if m["roof"].get("cutout"):
            needed.add(m["roof"]["cutout"])
    # 墙/建筑/平台材质体系用到的全部贴图——3D 预览的「自定义」要能任选，
    # 哪怕某个贴图暂时没被任何建筑引用（wood/pavement/grass 这类平台顶面）
    needed.update([
        "building_atlas.png", "building_atlas_desert.png", "cliff_wall1.png",
        "fence_atlas1.png", "grass.png", "none.png", "pavement.png",
        "pavement_end.png", "wood.png", "wood2.png", "world_atlas1.png",
    ])
    missing = []
    for tex in sorted(needed):
        if tex in SPECIAL_ATLASES:
            continue                # 极特殊素材不拷
        # 查找顺序：vanilla/textures → 其它包 textures → 各包地图目录
        # （building_atlas_normandy.png 这类图集只存在于特定地图目录里）
        hits = [h for h in (
            os.path.join(GAME_TEX, tex),
            os.path.join(GAME, "media", "packages", "edelweiss", "textures", tex),
        ) if os.path.exists(h)]
        if not hits:
            hits = glob.glob(os.path.join(GAME, "media", "packages", "*", "maps", "*", tex))
        if hits:
            shutil.copyfile(hits[0], os.path.join(OUT_DIR, tex))
        else:
            missing.append(tex)
    # 站点目录里若还残留上一次跑出来的极特殊图集，一并清掉
    for tex in SPECIAL_ATLASES:
        stale = os.path.join(OUT_DIR, tex)
        if os.path.exists(stale):
            os.remove(stale)
            print("  已删除残留贴图", tex)

    # 3.5) cutout 遮罩派生图：cutout.png 的 alpha 全 0、遮罩在 G 通道（R 全 255）。
    #      ⚠️ 浏览器 canvas 按**预乘 alpha** 存储，drawImage 一张全透明图会把 RGB
    #      抹成 0——前端永远读不到颜色通道（表现为「斑驳怎么调都没变化」）。
    #      所以在生成器里用 PIL 把指定通道预转成真 alpha，写成 <名>__mask.png，
    #      并把 data.json 里的引用改到派生图上。channel 约定：0=R 1=G 2=B。
    #      派生源优先用 cutout_viewable.png（用户导出的可视化版：同 RGB、
    #      alpha 全 255）；原 cutout.png 保留在站点里但不再参与合成。
    from PIL import Image as PILImage
    cut_refs = {}                          # 文件名 -> 用到的通道集合
    for m in materials.values():
        if m.get("detail_cutout"):
            cut_refs.setdefault(m["detail_cutout"], set()).add(m.get("detail_cutout_channel", "1"))
        if m["roof"].get("cutout"):
            cut_refs.setdefault(m["roof"]["cutout"], set()).add(m["roof"].get("cutout_channel", "1"))
    viewable = os.path.join(OUT_DIR, "cutout_viewable.png")
    for fname, chans in sorted(cut_refs.items()):
        if chans - {"1"}:
            print(f"  ⚠️ {fname} 用到非 G 通道 {chans}，暂按 G 处理")
        src = os.path.join(OUT_DIR, fname)
        if os.path.exists(viewable):
            src = viewable
        if not os.path.exists(src):
            continue                       # 拷贝阶段已缺失（如 cutout_2.png），前端有守卫
        im = PILImage.open(src).convert("RGBA")
        derived = fname.replace(".png", "__mask.png")       # G 通道（黄+白 = 露砖）
        derived_b = fname.replace(".png", "__maskb.png")    # B 通道（白 = 磨得最深）
        out = PILImage.new("RGBA", im.size, (0, 0, 0, 0))
        out.putalpha(im.split()[1])        # G 通道 → alpha
        out.save(os.path.join(OUT_DIR, derived))
        outb = PILImage.new("RGBA", im.size, (0, 0, 0, 0))
        outb.putalpha(im.split()[2])       # B 通道 → alpha
        outb.save(os.path.join(OUT_DIR, derived_b))
        for m in materials.values():
            if m.get("detail_cutout") == fname:
                m["detail_cutout"] = derived
            if m["roof"].get("cutout") == fname:
                m["roof"]["cutout"] = derived
                m["roof"]["cutout_b"] = derived_b
        print(f"  生成通道遮罩 {derived} / {derived_b} ← {os.path.basename(src)} (G/B→alpha)")

    # 4) 写 data.json：textures = 站点里实际有的贴图文件（下拉框全量可选；
    #    __mask*.png 是生成器派生的通道遮罩、cutout_viewable.png 是派生源，不列进去）
    data["textures"] = sorted(
        f for f in os.listdir(OUT_DIR)
        if f.lower().endswith(".png") and "__mask" not in f
        and f != "cutout_viewable.png")
    with open(os.path.join(OUT_DIR, "data.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)

    print(f"建筑 {len(order)} 条 · style {len(styles)} 个 · 单元坐标 {len(data['cells'])} 个")
    print(f"纹理：拷贝 {len(needed) - len(missing)} 个" + (f"，缺 {missing}" if missing else ""))
    print("输出：", os.path.join(OUT_DIR, "data.json"))


if __name__ == "__main__":
    main()
