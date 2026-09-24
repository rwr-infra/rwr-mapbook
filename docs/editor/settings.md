---
nav_label: "主界面"
title: "主界面"
icon: "lucide/sliders-horizontal"
description: "Save / ViewMap / Select / PinMan / WallE / BuildingE 等按钮的逐项说明。"
# ⚠️ 由 tools/docsgen.py 从 content/editor/settings.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# 主界面

<p class="kicker">EDITOR · 十四个按钮，各管一件事</p>

地编的顶栏从左到右排着这些工具。下面按顺序逐项说明——每一条都是**用出来的**，不是从界面文字猜的。

<div class="grid cards" markdown>

-   __Save__

    ---

    存地图

    [:octicons-arrow-right-24: 说明](#save)

-   __ViewMap__

    ---

    生成战术预览图

    [:octicons-arrow-right-24: 说明](#viewmap)

-   __Select__

    ---

    选择、移动、旋转

    [:octicons-arrow-right-24: 说明](#select)

-   __PinMan__

    ---

    放参照物

    [:octicons-arrow-right-24: 说明](#pinman)

-   __WallE__

    ---

    画墙

    [:octicons-arrow-right-24: 说明](#walle)

-   __BuildingE__

    ---

    放房子

    [:octicons-arrow-right-24: 说明](#buildinge)

-   __PlatformE__

    ---

    画平台、改高度

    [:octicons-arrow-right-24: 说明](#platforme)

-   __FuncObjects__

    ---

    梯子、箱子、复活点、据点

    [:octicons-arrow-right-24: 说明](#funcobjects)

-   __MeshE__

    ---

    摆模型、电线杆

    [:octicons-arrow-right-24: 说明](#meshe)

-   __HeightMap__

    ---

    刷地形高度

    [:octicons-arrow-right-24: 说明](#heightmap)

-   __TerrainBash__

    ---

    刷地面质地

    [:octicons-arrow-right-24: 说明](#terrainbash)

-   __offroadbuilder__

    ---

    给 AI 标开车路线

    [:octicons-arrow-right-24: 说明](#offroadbuilder)

-   __Decal__

    ---

    地面贴花

    [:octicons-arrow-right-24: 说明](#decal)

-   __Assaum__

    ---

    现成的组件

    [:octicons-arrow-right-24: 说明](#assaum)

-   __一些额外说明__

    ---

    叠放顺序、ID 重排这些绕不开的坑

    [:octicons-arrow-right-24: 说明](#extra)

-   __如何画平台？__

    ---

    从高处缓坡下到水里，一步步画一遍

    [:octicons-arrow-right-24: 说明](#platform)

</div>


## Save 说明 { #save }

简简单单保存地图，保存完会有提示音。

## ViewMap 说明 { #viewmap }

生成地图的战术预览图，也就是 RWR 里面按 Tab 查看的地图。

!!! question "存疑"
    文件名貌似得自己调一下？

## Select 说明 { #select }

- 左键点击进行单个选择、Ctrl+左键点击或左键拖动进行多个选择。
- 按 Esc 键取消选择。
- 按 Delete 键删除选择的目标。
- 按 G 键启用移动模式，此时移动鼠标可将选择的对象拖走。
- 按 R 键启用旋转模式，此时移动鼠标可将选择的对象旋转至某个角度。
- 在其它工具模式中，按 Shift+1 快捷键可快速切换回 Select 工具。
- 无法同时选择多个平台。
- 俯视角模式（正交）下会导致部分平台无法正常显示与选择，此时需要切换到飞行模式（透视）来进行选择。
- 不建议在飞行模式（透视）下进行移动与旋转，交互有点够使。

## PinMan 说明 { #pinman }

用来在点击的位置上放置一个虚拟的参照物。

虽然有三个选项但是只有坦克能用。

## WallE 说明 { #walle }

- 用来在列表中选择各种墙的种类，并使用 PathBush 绘制节点然后按空格自动以摆放顺序连成线。既可以先选择墙的种类后绘制，也可以先绘制然后再选择墙的种类，选择后点击已经画好的墙即可完成替换。
- 在搜索栏中可搜索对应名称来快速选择对象，每种墙的作用见[模型清单 · Wall E](../tables/wall.md)。
- 在用 Select 选中后，可以在这个界面编辑坐标（第一项为 X 轴向右增长、第二项为 Y 轴向下增长，数据为鼠标当前位置坐标的二倍）、使用 Add Point 来在绘制方向增加一条相连的线段、使用叉号来删除这段节点。
- 在用 Select 选中多个后，可以在这个界面进行删除指定对象的操作，Buiding、Mesh 等同理。
- 在用 Select 选中后，可以在这个界面查看 id、当前层、墙的种类以及设置自定义高度与是否 Merge。
- Marge 默认勾选，目的是防止 AI 卡墙翻不过去。
- 勾选 ReHeight 后，可以自行输入墙的高度。

![主界面 1](../assets/editor/017.png)

![主界面 2](../assets/editor/018.png)

![主界面 3](../assets/editor/019.png)

![主界面 4](../assets/editor/020.png)

## BuildingE 说明 { #buildinge }

- 用来在列表中选择各种建筑物的种类，并使用 DrawBush 按住左键拖动来绘制建筑物。既可以先选择建筑物的种类后绘制，也可以先绘制然后再选择建筑物的种类，选择后点击已经画好的建筑物即可完成替换。
- 在搜索栏中可搜索对应名称来快速选择对象，每种建筑的外形见[模型清单 · Building E](../tables/building.md)。
- 最上方 HeightDown 与 HeightUp 的作用为改变点击位置的 Building 高度，每次变化 2（6）。
- RoofSwitch 的作用为将屋顶变为尖顶/平顶，尖顶方向固定需要选择建筑物后按 R 自行旋转。
- 建议先调整完 Height 后再在上方叠加新的对象，上方的对象高度不会随下方 Building 高度的变化而变化。
- 在用 Select 选中后，可以在这个界面查看 id、当前层、屋顶是否为尖顶、建筑物的种类。
- Offset 的作用是设置自定义偏移度（第一项为 X 轴向右增长、第二项为 Z 轴向顶部增长、第三项为 Y 轴向下增长）。
- 目前 X 轴改不了。

!!! warning "待修复"
    在飞行模式（透视）下，不同方向的透视有严重问题，见上方右侧例图。

![主界面 5](../assets/editor/021.png)

![主界面 6](../assets/editor/022.png)

![主界面 7](../assets/editor/023.png)

![主界面 8](../assets/editor/024.png)

![主界面 9](../assets/editor/025.png)

## PlatformE 说明 { #platforme }

- 用来在列表中选择各种平台的种类，并使用 pathBush 绘制，与 Wall 类似，不再赘述。
- 例子说明见下方：如何画平台？
- 搜索栏与 Wall 类似，不再赘述。
- 最下方的 TypeChange 的作用为让点击位置的 Platform 在无特殊属性、deck 属性、bridge 属性之间切换。（这一节还没写完）
- ChangeHei 的操作为在设置完成高度后按回车进入工具使用状态，作用为改变点击位置的 Platform 高度。
- 在用 Select 选中后，可以在这个界面编辑坐标，方法与 Wall 类似，不再赘述。
- 在用 Select 选中后，可以在这个界面查看 type、id、当前层、顶部材质、平台侧面墙的种类、平台上方附加墙的种类、墙的高度。
- 平台上方附加墙的种类可以使用 WallE 工具进行更改。
- SetMaterial 中添加的值可以是 wood、grass、pavement、terrian。（这一节还没写完）

![主界面 10](../assets/editor/026.png)

![主界面 11](../assets/editor/027.png)

![主界面 12](../assets/editor/028.png)

![主界面 13](../assets/editor/029.png)

## FuncObjects 说明 { #funcobjects }

LadderScatter 与 LadderEraser 的作用为放置梯子与删除梯子。放置的梯子会自动吸附在旁边建筑物、平台等等有固定碰撞的东西上。

!!! warning "待优化"
    目前吸附堪比哈基米，有点问题。

- ItemSupplyScatter 的作用为放置一个储藏室或军械库的判定区，stash 为储藏室，weapon_rack 为军械库，选中后点击下方 ChangeType 进行切换。
- CrateScatter 与 CrateEraser 的作用为放置木头箱子与删除木头箱子，里面的物品随机无法指定。
- SpawnScatter 与 SpawnEraser 的作用为创建复活点与删除复活点，复活点不宜太靠近地图边界。
- BaseScatter 的作用为左键拖动创建据点，在用 Select 选中后，可以分别更改据点的名字显示与指定该剧点最开始被哪个阵营占领，填写 0、1、2，分别为我也不知道对应哪个哈哈 XD

![主界面 14](../assets/editor/030.png)

![主界面 15](../assets/editor/031.png)

## MeshE 说明 { #meshe }

- 用来在列表中选择各种模型的种类。
- 搜索栏与 Wall 类似，不再赘述。
- StoneEraser 与 StoneScatter 的作用为删除一个随机石头或放置一个随机石头，石头的样子见[模型清单 · MESH E](../tables/mesh.md)。
- TreeEraser 与 TreeScatter 的作用为删除一个随机树或放置一个随机树，树的样子见[模型清单 · MESH E](../tables/mesh.md)。
- 最下方的工具使用方法与 Wall 类似，作用为放置电线杆子作为节点，放完后按空格进行按顺序的两两间电线连线，电线仅为装饰物，无碰撞。
- 在用 Select 选中后，可以在这个界面查看 id、种类、碰撞体积（如果是默认则不显示）。
- 勾选 ReCollision 后可在上方窗口内更改长、高、宽（以中心为基准）。
- offset 的作用是设置自定义偏移度（第一项为 X 轴向右增长、第二项为 Z 轴向顶部增长、第三项为 Y 轴向下增长）。

![主界面 16](../assets/editor/032.png)

![主界面 17](../assets/editor/033.png)

![主界面 18](../assets/editor/034.png)

![主界面 19](../assets/editor/035.png)

## HeightMap 说明 { #heightmap }

- HeightBush 的作用为地形刷，左下角界面中的 SetHardness 为硬度，决定着当前刷取地形的高度与背景高度的过渡陡缓，范围为 0 到 1、SerRange 为地形刷的范围、SetHeight 为地形刷的高度，范围为 0 到 1。按 X 横向锁定笔刷，按 Y 纵向锁定。
- HeightSmudge 的作用为拖拽鼠标下一定范围内的高度，并跟随鼠标移动方向使临近的地形产生过渡形变。
- Smooth 的作用为平缓全图的地形。
- Noise 的作用为对全图增加地形上的噪音，让整个地图不是同一个高度数值的大平地，有些微小起伏。
- heightPath 的作用为路径地形刷，使用方式类似 Wall 工具，相关数据调整左上角均有说明，可自行尝试。

![主界面 20](../assets/editor/036.png)

![主界面 21](../assets/editor/037.png)

## TerrainBash 说明 { #terrainbash }

- Pathpainter 的作用为路径地面质地刷，使用方式类似 Wall 工具，相关数据调整左上角均有说明，可自行尝试。
- 衰减指数的调成为[与]，并不是描述打重复变成[[/]] 了。
- painter 的作用为地面质地刷，Chg Index 为材质种类，填数字、Chg Rng 为范围、Chg Har 为硬度。
- 0101 版本中使用这个工具的时候左下角可能会有个多余的调节栏，实际啥用没有。
- Smooth 的作用为平缓全图的地面质地。

![主界面 22](../assets/editor/038.png)

![主界面 23](../assets/editor/039.png)

## offroadbuilder 说明 { #offroadbuilder }

用来给 AI 判定这个路线是开车路线，放飞驾驶。

使用方法类似 Wall 工具。

## Decal 说明 { #decal }

- 用来在列表中选择各种贴花的种类，可以理解为在地面质地上再印一层材质，选择后左键即可放置。
- deleteDecals 的作用为删除框选范围内的贴花。
- Select 选中后，可以使用 Length 更改这个贴花的大小，也就是缩放比例。

![主界面 24](../assets/editor/040.png)

## Assaum 说明 { #assaum }

用来在列表中选择各种组件，例如已经制作好碰撞箱和判定区的军械库等，选择后左键即可放置。

Add 与 Name 暂时不可用，无效果。

## 一些额外说明 { #extra }

1.如果你想在一个 Building 上面放 Wall、Building、Platform 之类的东西，那么应该在构思完之后从下往上绘制，绘制的时候需要保证起点在上一个元素之内，这样所有的对象就都会按照 layer1、layer2….去逐个叠加，并自动衔接上一个的高度，攀爬等判定也会正常生效。

2.地编在每次保存之后都会重新排序一遍 ID，编号可能会发生变动。

## 如何画平台？ { #platform }

以过渡的山崖平台为例：

我们这次的目的是要从左侧的高处用缓坡到达谷底的水中，可以看到在箭头方向的左侧是一个不那么平缓的坡，右侧则为陡崖，那我们就应该以左侧的坡的高度为基准制作一个过度的山崖。

![主界面 25](../assets/editor/041.png)

![主界面 26](../assets/editor/042.png)

因为绘制平台时需保证终点边在起点边行进方向右边，同时起点边为判定高度的边，所以我们应该先在箭头的左侧缓坡处，沿着图一的箭头方向绘制。

（画了八个点，如果想让变化更均匀可以多点几个）之后按空格，在箭头右侧放置另外对应的八个点，按第二空格次完成绘制。

![主界面 27](../assets/editor/043.png)

![主界面 28](../assets/editor/044.png)

之后对平台进行细致调整，使其合理。

（蓝色点为基准点，也就是第一次画线生成的点，蓝点到粉点之间的连线就是地形的过渡）

（如果你的平台是紫黑相间的错误渲染颜色，那么恭喜你你放反了，请再次注意绘制平台时需保证终点边在起点边行进方向右边）

（反正图片也没压缩，细节自行放大查看吧）

![主界面 29](../assets/editor/045.png)

进游戏看看~

果不其然做的一坨，可见多加几个锚点和完善地形的重要性，希望各位引以为戒:(

![主界面 30](../assets/editor/046.png)
