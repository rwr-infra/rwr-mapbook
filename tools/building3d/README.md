# `tools/building3d/`：Building E 页 3D 预览的数据生成器

```
build.py     从地编模板 vao0822.svg 抽出建筑定义，产出站点要的 data.json 与贴图
```

站点侧的所有东西都在 `docs/b3d/` 里，不在这里：

```
docs/b3d/viewer.js   渲染器（原生 WebGL，不引外部库；只在 building 页启动）
docs/b3d/data.json   本脚本的产物：建筑 / style / 图集坐标表
docs/b3d/*.png       产物：图集与贴图原图（含 __mask*.png 派生遮罩）
```

## 什么时候要重跑

产物是**入库的**，平时改页面、改样式都不用跑。只有下面这几种情况需要：

- 地编模板换了版本（`vao0822.svg` 里新增 / 调整了楼体定义）
- 补了新的图集或贴图
- `build.py` 里解析逻辑改了

```bat
D:\RWRWorkSpace\_py\py314\python.exe tools\building3d\build.py
```

跑完记得重记基线再提交（产物是整目录覆盖写，`data.json` 与贴图都会变）。

## 两个必须按本机改的常量

```python
TEMPLATE = r"D:\RWRMap\0100\1007_Data\templates\vao0822.svg"
GAME     = r"D://steam//steamapps//common//RunningWithRifles"
MAP_SVGS = [r"D:\RWRMap\0100\1007_Data\map\objects.svg"]
```

`TEMPLATE` 是地编模板，`GAME` 是装 RWR 的那个目录（贴图从
`media/packages/<包>/textures` 与各包地图目录里找），`MAP_SVGS` 是地图的
`objects.svg`——**模板里的楼体定义没有 `atlas_texture`**，实际地图那份才有，
所以两遍扫描缺一不可，少了它整栋楼的墙面格子会全错。

依赖：`PIL`（派生通道遮罩用）、标准库。跟站点其他工具用的是同一个解释器。

## 产物里的东西是怎么来的

```
建筑（材料 material_XXX 的 <desc>）
  ├─ 1st_floor_1..4    一层 正 / 右 / 背 / 左 四面各引用一个 style
  ├─ other_floor_1..4  其它层四面
  └─ roof_texture / roof_*_atlas_cell / roof_scale / roof_color …
style（building_style_XXX）
  └─ sequence = …      一串基础单元，横着拼起来就是这一面墙
基础单元（texture_groups__XXX）
  └─ 名字 = 列,行      图集里的坐标（游戏资源只存名字，坐标就靠模板这张表）
```

`normandy / provence / tropical` 三张图集属于「极特殊素材」，脚本会把它们以及
引用它们的材质、style、单元一律排除在预览之外，所以最后 `data.json` 里没有它们。
