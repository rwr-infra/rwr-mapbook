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

输出：docs/assets/tables/building/data.json（页面运行时 fetch）。
"""

import os
import glob
import re
import json
import shutil

TEMPLATE = r"D:\RWRMap\0100\1007_Data\templates\vao0822.svg"
GAME = r"D://steam//steamapps//common//RunningWithRifles"
GAME_TEX = os.path.join(GAME, "media", "packages", "vanilla", "textures")
DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
OUT_DIR = os.path.join(DOCS, "assets", "tables", "building")

# 模板没写 atlas_texture 时用的默认墙体图集（参数字典里列的三种之一）
DEFAULT_ATLAS = "building_atlas2.png"
# ⚠️ 模板 vao0822.svg 里的建筑定义**没有 atlas_texture**，而实际地图的
#    objects.svg 里每栋楼都指定了图集（normandy / provence / tropical /
#    building_atlas2/3/4）。预览必须用地图那份，否则整栋楼的墙面格子全错
#    （BuildingBritish 系列应该是 normandy，拿 building_atlas2 画就全是乱的）。
MAP_SVGS = [r"D:\RWRMap\0100\1007_Data\map\objects.svg"]
GRID = [8, 8]        # 单元坐标表是 8 列（列号 0..7）；图集 256×256 → 每格 32px


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
                    nums = [float(x) for x in parts[:4]]
                except ValueError:
                    return None
                return nums
            materials[name] = {
                "color": kv.get("color", "fill"),
                "color_variance": kv.get("color_variance", ""),
                "fill": sty.get("fill", ""),
                "stroke": sty.get("stroke", ""),
                "detail_texture": first_token(kv.get("detail_texture"), "wall_atlas1.png"),
                "detail_cell": cell_of("detail_texture"),
                "detail_scale": str(kv.get("detail_texture_scale", "3 3")),
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
                },
            }
            order.append(name)

    data = {
        "source": os.path.basename(TEMPLATE),
        "atlas_grid": GRID,
        "default_atlas": DEFAULT_ATLAS,
        # 单元名全局唯一，直接把所有组的坐标并到一起（组 key 带 _desc_1 后缀，
        # 别按名字精确取，取不到就 0 条）
        "cells": {k: v for group in cells.values() for k, v in group.items()},
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
    # 墙/建筑/平台材质体系用到的全部贴图——3D 预览的「自定义」要能任选，
    # 哪怕某个贴图暂时没被任何建筑引用（wood/pavement/grass 这类平台顶面）
    needed.update([
        "building_atlas.png", "building_atlas_desert.png", "cliff_wall1.png",
        "fence_atlas1.png", "grass.png", "none.png", "pavement.png",
        "pavement_end.png", "wood.png", "wood2.png", "world_atlas1.png",
    ])
    missing = []
    for tex in sorted(needed):
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

    # 4) 写 data.json：textures = 站点里实际有的贴图文件（下拉框全量可选）
    data["textures"] = sorted(
        f for f in os.listdir(OUT_DIR) if f.lower().endswith(".png"))
    with open(os.path.join(OUT_DIR, "data.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)

    print(f"建筑 {len(order)} 条 · style {len(styles)} 个 · 单元坐标 {len(data['cells'])} 个")
    print(f"纹理：拷贝 {len(needed) - len(missing)} 个" + (f"，缺 {missing}" if missing else ""))
    print("输出：", os.path.join(OUT_DIR, "data.json"))


if __name__ == "__main__":
    main()
