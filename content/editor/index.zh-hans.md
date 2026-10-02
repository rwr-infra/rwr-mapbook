---
nav_label: "功能介绍"
title: "功能介绍"
icon: "lucide/layout-grid"
description: "地编界面的功能介绍：顶栏工具逐项说明、交互按键、ID 搜索，以及 mapSettings、3rdParSettings、RefpM 三处配置。"
tags: [界面, 工具, 配置文件]
---

# 功能介绍 { #overview }

![](../assets/editor/016.png)

/// caption
地编主界面。
///

* * *
## 主界面工具

* * *
### Save 说明 { #save }

!!! note "用来保存地图，保存完成后会有提示音。"

* * *
### ViewMap 说明 { #viewmap }

??? note "生成地图的初版预览图（展开以查看详细介绍）"
    点击后会生成一个名为 map_view_ls.png 的文件，这便是初版预览图，其会自动添加一些地图上的元素，比如据点范围等，后续在地图做完后便可根据此图来进行 地图缩略图 的制作。

    <span class="redact" tabindex="0">对的，从之前到现在每个地图的最终缩略图都是手搓出来的。</span>


* * *
### Select 说明 { #select }

??? note "用来选择地图上的对象（展开以查看详细介绍）"
    使用快捷键 ++shift+1++ 以快速切换到 Select 工具。
    * * *
    相关交互：

    - 左键点击选择单个对象、++ctrl+lbutton++（点击）或 ++lbutton++（按住拖动）选择多个对象。

    - 按 ++esc++ 键取消选择。

    - 按 ++delete++ 键删除选择的目标。

    - 按 ++g++ 键启用移动模式，此时移动鼠标可将选择的对象拖走。

    - 按 ++r++ 键启用旋转模式，此时移动鼠标可将选择的对象旋转至某个角度。

    !!! warning 
        无法同时选择多个平台。

        俯视角模式（正交）下会导致部分平台无法正常显示与选择，此时需要切换到飞行模式（透视）来进行选择。

        不建议在飞行模式（透视）下进行移动与旋转，交互体验不佳。

* * *
### PinMan 说明 { #pinman }

??? note "用来在点击的位置上放置一个虚拟的参照物。（展开以查看详细介绍）"
    使用快捷键 ++shift+2++ 以快速切换到 PinMan 中的 TankPin 工具。
    !!! warning "有三个选项，但只有坦克可用。"

* * *
### WallE 说明 { #walle }
??? note "用来在列表中选择各种墙的种类，并使用 PathBush 绘制节点然后按空格自动以摆放顺序连成线。既可以先选择墙的种类后绘制，也可以先绘制然后再选择墙的种类，选择后点击已经画好的墙即可完成替换。（展开以查看详细介绍）"
    使用快捷键 ++shift+7++ 以快速切换到 WallE 中的 PathBush 工具。
    * * *    
    在搜索栏中可搜索对应名称来快速选择对象，每种墙的模型见[模型清单 · Wall E](../tables/wall.md)。

    ![](../assets/editor/017.png)

    * * *
    在用 Select 选中后，可以在这个界面编辑坐标（第一项为 X 轴向右增长、第二项为 Y 轴向下增长，数据为鼠标当前位置坐标的二倍）、使用 Add Point 来在绘制方向增加一条相连的线段、使用叉号来删除这段节点。

    ![](../assets/editor/018.png)

    * * *
    在用 Select 选中多个后，可以在这个界面进行删除指定对象的操作，Buiding、Mesh 等同理。

    ![](../assets/editor/019.png)

    * * *
    在用 Select 选中后，可以在这个界面查看 id、当前层、墙的种类以及设置自定义高度与是否 Merge。

    Marge 默认勾选，目的是防止 AI 卡墙翻不过去。

    勾选 ReHeight 后，可以自行输入墙的高度。
    ![](../assets/editor/020.png)



* * *
### BuildingE 说明 { #buildinge }

??? note "用来在列表中选择各种建筑物的种类，并使用 DrawBush 按住左键拖动来绘制建筑物。既可以先选择建筑物的种类后绘制，也可以先绘制然后再选择建筑物的种类，选择后点击已经画好的建筑物即可完成替换。（展开以查看详细介绍）"
    使用快捷键 ++shift+3++ 以快速切换到 BuildingE 中的 DrawBush 工具。

    使用快捷键 ++shift+4++ 以快速切换到 BuildingE 中的 RoofSwitch 工具。

    使用快捷键 ++shift+5++ 以快速切换到 BuildingE 中的 BuildingMaterialChanger 工具。

    使用快捷键 ++shift+6++ 以快速切换到 BuildingE 中的 HeightUp 工具。

    * * *
    在搜索栏中可搜索对应名称来快速选择对象，每种建筑的模型见[模型清单 · Building E](../tables/building.md)。

    ![](../assets/editor/021.png)

    * * *
    最上方 ^^HeightDown^^ 与 ^^HeightUp^^ 的作用为改变点击位置的 Building 高度，每次变化 2（6）。^^RoofSwitch^^ 的作用为将屋顶变为尖顶/平顶，尖顶方向固定需要选择建筑物后按 ++r++ 自行旋转。

    ![](../assets/editor/022.png)

    !!! quote "建议先调整完 Height 后再在上方叠加新的对象，上方的对象高度不会随下方 Building 高度的变化而变化。"

    * * *
    在用 Select 选中后，可以在这个界面查看 id、当前层、屋顶是否为尖顶、建筑物的种类。

    Offset 的作用是设置自定义偏移度（第一项为 X 轴向右增长、第二项为 Z 轴向顶部增长、第三项为 Y 轴向下增长）。

    ![](../assets/editor/023.png)

    !!! warning 
        目前 X 轴无法修改。
        如果你想在一个 Building 上面放 Wall、Building、Platform 之类的东西，那么应该在构思完之后从下往上绘制，绘制的时候需要保证起点在上一个元素之内，这样所有的对象就都会按照 layer1、layer2… 去逐个叠加，并自动衔接上一个的高度，攀爬等判定也会正常生效。

* * *
### PlatformE 说明 { #platforme }

??? note "用来在列表中选择各种平台的种类，并使用 ^^pathBush^^ 绘制，与 Wall 类似，不再赘述。（展开以查看详细介绍）"
    使用快捷键 ++shift+8++ 以快速切换到 PlatformE 中的 PathBush 工具。

    使用快捷键 ++shift+9++ 以快速切换到 PlatformE 中的 TypeChange 工具。

    使用快捷键 ++shift+0++ 以快速切换到 PlatformE 中的 PlatformBasewallChanger 工具。
    * * *
    搜索栏与 Wall 类似，不再赘述。
    
    ![](../assets/editor/026.png)
    * * *
    最下方的 ^^TypeChange^^ 的作用为让点击位置的 Platform 在"无特殊属性"、"deck 属性"、"bridge" 属性之间切换。

    ChangeHeight 的操作为在设置完高度后按回车进入工具使用状态，作用为改变点击位置的 Platform 高度。

    ![](../assets/editor/027.png)
    !!! warning "属性介绍这一块还没写完"
    * * *

    在用 Select 选中后，可以在这个界面编辑坐标，方法与 Wall 类似，不再赘述。

    ![](../assets/editor/028.png)

    * * *
    在用 Select 选中后，可以在这个界面查看 type、id、当前层、顶部材质、平台侧面墙的种类、平台上方附加墙的种类、墙的高度。
    平台上方附加墙的种类可以使用 WallE 工具进行更改。
    SetMaterial 中添加的值可以是 wood、grass、pavement、terrian。

    ![](../assets/editor/029.png)
    !!! warning "材质预览这一块还没写完"
    * * *
    ??? quote "如何画平台？"

        以过渡的山崖平台为例：

        我们这次的目的是要从左侧的高处用缓坡到达谷底的水中，可以看到在**箭头方向**的左侧是一个不那么平  缓的坡，右侧则为陡崖，那我们就应该以左侧的坡的高度为基准制作一个过度的山崖。

        ![](../assets/editor/041.png)

        因为**绘制平台时需保证终点边在起点边行进方向右边**，同时起点边为判定高度的边，所以我们应该先在  箭头的左侧缓坡处，沿着图一的箭头方向绘制。
        ![](../assets/editor/042.png)

        （画了八个点，如果想让变化更均匀可以多点几个）之后按空格，在箭头右侧放置另外对应的八个点，再按  一次空格完成绘制。
 
        ![](../assets/editor/043.png)

        ![](../assets/editor/044.png)

        之后对平台进行细致调整，使其合理。

        （蓝色点为基准点，也就是第一次画线生成的点，蓝点到粉点之间的连线就是地形的过渡）

        （如果你的平台是紫黑相间的错误渲染颜色，那么恭喜你你放反了，请再次注意绘制平台时需保证终点边在  起点边行进方向右边）

        ![](../assets/editor/045.png)

        进游戏看看~

        <span class="redact" tabindex="0">果不其然做的一坨，可见多加几个锚点和完善地形的重要性，希望各位引以为戒:(</span>
        ![](../assets/editor/046.png)


* * *
### FuncObjects 说明 { #funcobjects }
??? note "用来摆放一些有特殊交互的物件。（展开以查看详细介绍）"
    ^^LadderScatter^^ 与 ^^LadderEraser^^ 的作用为放置梯子与删除梯子。放置的梯子会向前自动判定并吸附在旁边建筑物、平台等等有固定碰撞的东西上。

    !!! warning "如果梯子方向放反了会导致吸附失败无法正常攀爬，并且0101版本的梯子没有正前方指示，调整时尽量别记混梯子朝向。"
    * * *

    ^^ItemSupplyScatter^^ 的作用为放置一个储藏室或军械库的判定区，stash 为储藏室，weapon_rack 为军械库，Select 选中后点击下方 ChangeType 进行切换。

    ![](../assets/editor/030.png)
    * * *

    ^^CrateScatter^^ 与 ^^CrateEraser^^ 的作用为放置木头箱子与删除木头箱子，里面的物品随机，无法指定。

    ^^SpawnScatter^^ 与 ^^SpawnEraser^^ 的作用为创建复活点与删除复活点，复活点不宜太靠近地图边界。

    ^^BaseScatter^^ 的作用为左键拖动创建据点，在用 Select 选中后，可以分别更改据点的名字显示（ Name ）与指定该据点最开始被哪个阵营占领（ Faction ）。


    ![](../assets/editor/031.png)

    ??? quote "关于 Faction 的一些说明"
        不使用Faction那这个据点将会进行随机分配，填写整数数字则会按整数的类别进行分配，玩家阵营默认为0号阵营。
        如果你设置了地图里只有两个阵营作战，那么当 Faction 的值填写为2时，这个据点将会变成没有被任何阵营占领的空白据点。
        map13_2 那种为特殊效果，不做介绍。

* * *
### MeshE 说明 { #meshe }

??? note "用来在列表中选择各种模型的种类。（展开以查看详细介绍）"

    搜索栏与 Wall 类似，不再赘述。

    ![](../assets/editor/032.png)
    * * *
    ^^StoneEraser^^ 与 ^^StoneScatter^^ 的作用为删除一个随机石头或放置一个随机石头，石头的样子见[模型清单 · MESH E](../tables/mesh.md)。

    ^^TreeEraser^^ 与 ^^TreeScatter^^ 的作用为删除一个随机树或放置一个随机树，树的样子见[模型清单 · MESH E](../tables/mesh.md)。

    ![](../assets/editor/033.png)
    * * *
    最下方的工具使用方法与 Wall 类似，作用为放置电线杆作为节点，放完后按空格进行按顺序的两两间电线连线，电线仅为装饰物，无碰撞。

    ![](../assets/editor/034.png)
    * * *
    在用 Select 选中后，可以在这个界面查看 id、种类、碰撞体积（如果是默认则不显示）。
    勾选 ReCollision 后可在上方窗口内更改长、高、宽（以中心为基准）。
    offset 的作用是设置自定义偏移度（第一项为 X 轴向右增长、第二项为 Z 轴向顶部增长、第三项为 Y 轴向下增长）。

    ![](../assets/editor/035.png)


* * *
### HeightMap 说明 { #heightmap }

??? note "用来铺设地面的弧度变化。（展开以查看详细介绍）"
    ^^HeightBush^^ 的作用为地形刷，左下角界面中的 SetHardness 为硬度，决定着当前刷取地形的高度与背景高度的过渡陡缓，范围为 0 到 1、SerRange 为地形刷的范围、SetHeight 为地形刷的高度，范围为 0 到 1。按 X 横向锁定笔刷，按 Y 纵向锁定。

    ![](../assets/editor/036.png)
    * * *
    ^^HeightSmudge^^ 的作用为拖拽鼠标下一定范围内的高度，并跟随鼠标移动方向使临近的地形产生过渡形变。
    * * *
    ^^Smooth^^ 的作用为平缓全图的地形。
    * * *
    ^^Noise^^ 的作用为对全图增加地形上的噪音，让整个地图不是同一个高度数值的大平地，有些微小起伏。
    * * *
    heightPath 的作用为路径地形刷，使用方式类似 Wall 工具，相关数据调整左上角均有说明，可自行尝试。

    ![](../assets/editor/037.png)

* * *
### TerrainBash 说明 { #terrainbash }
??? note "用来铺设地面的质地变化。（展开以查看详细介绍）"
    ^^Pathpainter^^ 的作用为路径地面质地刷，使用方式类似 Wall 工具，相关数据调整左上角均有说明，可自行尝试。
    衰减指数用 [ 以及 ] 调整，并不是描述重复打成了 [[/]]。

    ![](../assets/editor/038.png)
    * * *
    ^^painter^^ 的作用为地面质地刷，Chg Index 为材质种类，填数字、Chg Rng 为范围、Chg Har 为硬度。

    ![](../assets/editor/039.png)
    !!! warning "0101 版本中使用这个工具的时候左下角可能会有个多余的调节栏，实际没有任何作用。"
    * * *
    Smooth 的作用为平缓全图的地面质地。


* * *
### offroadbuilder 说明 { #offroadbuilder }

!!! note "用来告诉 AI 这条路是开车路线，AI会在开载具时优先往这条路进行寻路，铺设方法类似 Wall 工具。"

* * *
### Decal 说明 { #decal }

??? note "用来在列表中选择各种贴花的种类，可以理解为在地面质地上再印一层材质，选择后左键即可放置。（展开以查看详细介绍）"
    ^^deleteDecals^^ 的作用为删除框选范围内的贴花。
    * * *
    Select 选中后，可以使用 Length 更改这个贴花的大小，也就是缩放比例。

    ![](../assets/editor/040.png)


* * *
### Assaum 说明 { #assaum }
??? note "用来在列表中选择各种组件，例如已经制作好碰撞箱和判定区的军械库等，选择后左键即可放置。（展开以查看详细介绍）"
    搜索栏与 Wall 类似，不再赘述。
    * * *
    如果你想给列表添加你自己的组件，在选择要组装的对象之后，通过 Name 进行命名，之后点 Add 即可将你所选的对象组加入组件列表。
    !!! warning
        组件不跟随模板变动，是独立路径。
        在Add时需要保证对象是多选状态，如果只选了一个不会进行保存。




* * *
### ID 搜索说明 { #id-search }
??? note "相关步骤"
    1.在这看id。

    ![](../assets/editor/050.png)

    /// caption
    使用 Select 选中对象查看，或直接拆svg找。
    ///    

    !!! warning
        地编每次保存后都会重新排一遍 ID，编号可能和上一次不一样。

        所以**记下来的是当时的 ID**；隔一次保存再搜，未必还是它。

    2.把 ID 填进搜索框之后点右边的搜索按钮。

    ![](../assets/editor/051.png)

    /// caption
    可以看到下面出现小绿字，搜索成功。
    ///

??? quote "一个找id的运用"
    哎呦我去！RWR刚加载完一半我的地图就崩溃了？！
    在C:\Users\用户\AppData\Roaming\Running with rifles路径下翻翻rwr_game.log，可以看到这次是RWR因为没法定位到crate_adjusted.mesh，自爆了。

    ![](../assets/editor/052.png)

    在svg地图中搜一下这个mesh，发现有两个相关的static_object。

    ![](../assets/editor/053.png)

    /// caption
    这里只展示了一个
    ///

    再去搜索这俩static_object，哇爆率真的高一下就看到相关id了。

    ![](../assets/editor/054.png)

    /// caption
    后续就是用id搜索功能给这俩对象从地图上删了就完事了
    ///

!!! tip "ID 会变"
    地编每次保存后都会重新排一遍 ID，编号可能和上一次不一样。
    所以**记下来的是当时的 ID**；隔一次保存再搜，未必还是它。

* * *
### mapSettings 说明 { #map-settings }

!!! note "暂无已校验内容。"

??? example "**待校验内容。**（展开以查看）"
    | 字段 | 示例 | 备注 | 说明 |
    | --- | --- | --- | --- |
    | `ambience_alert_day_sound` | `ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | 没试，不知道这是啥 |
    | `ambience_day_sound` | `ambient_daytime.wav`<br>`ambient_lightrain.wav` |  | 白天的背景音效 |
    | `ambience_night_sound` | `ambient_lightrain_night.wav` |  | 晚上的背景音效 |
    | `day_color` | `#e5c685ff`<br>`fill` | 任意 16 进制颜色 | 白天的颜色 |
    | `description` | `16 bases`<br>`2 faction king of the hill map`<br>`assault map - 11 bases`<br>`conquest map - 10 bases`<br>`pure pvp map` | 可任意填写，但最  好按格式来 | 地图描述 |
    | `flip` | `-1` |  | 不知道这是啥，没试 |
    | `global_effect` | `ambience_alert_day_sound`<br>`ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | 全局效果 |
    | `name` | `Route 666` | 可任意填写 | 地图名 |
    | `night_color` | `#136395`<br>`#5f5fc0ff`<br>`stroke` | 任意 16 进制颜色 | 晚上的颜色 |
    | `randomize_faction_index` | `0`<br>`1` |  | 没试，不知道这是啥 |
    | `show_base_names_in_map_view` | `0` |  | 不知道这是啥，没试 |
    | `starting_day_phase` | `0.1`<br>`6` |  | 战役开始的时间 |
    | `visible_in_menu` | `0`<br>`1` |  | 是否在列表可见 |

!!! warning "map settings不写会导致无法运行地图，实在不知道写啥随便粘贴一个地图的改吧改吧就得了。"
* * *
### 3rdParSettings 说明 { #third-party }
用来加载细致模型以及部分材质，可不用。
#### 一、OgreXMLConverter.exe Path 选择 { #ogreref }

??? info "这一步已经在0101版本中内置了，可跳过，展开以查看没啥用的步骤。"
    1. 点击 Select，确认 `OgreSDK_vc10_v1-7-4.zip` 解压到了哪里，找到它的根目录。
    2. 顺着 `OgreSDK_vc10_v1-7-4\bin\release` 找到 `OgreXMLConverter.exe`，选中它。
    3. 基础设置完成，继续第二、三步。

    !!! example "示例路径，仅供参考"
        ```text
        D:\RWRMap\OgreSDK_vc10_v1-7-4\bin\release
        ```

#### 二、Mesh files path 选择 { #mesh-path }

1. 找到 Steam 上小兵步枪的根目录。可以在 Steam 界面里「管理 → 浏览本地文件」去定位。

    ![](../assets/editor/047.png)

2. 顺着 `RunningWithRifles\media\packages\vanilla` 找到 `models` 文件夹，选中它。
3. 点击 **load mesh**。

!!! example "示例路径，仅供参考"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

设置完成后效果如下（以 Mesh 为例）：

![](../assets/editor/048.png)

#### 三、textures path 选择 { #textures-path }

1. 与第二步的第 1 步相同。
2. 顺着 `RunningWithRifles\media\packages\vanilla` 找到 `textures` 文件夹，选中它。
3. 点击 **load textures**。

!!! example "示例路径，仅供参考"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

设置完成后效果如下（以 Decal 为例）：

![](../assets/editor/049.png)

* * *
### RefpM 说明 { #reference-images }

使用 ^^Import^^ 导入参考图， ^^Clear^^ 移除。
^^ScaleX^^ 与 ^^ScaleY^^ 的作用为横向与纵向压缩或拉长参考图，值填倍率，例如ScaleX填0.5就是横向把参考图压刀一半。
^^OffsetX^^ 与 ^^OffsetX<span class="redact" tabindex="0">其实是Y</span>^^ 的作用为横向与纵向偏移参考图，值填距离，第一项为X轴向右增长、第二项为Y轴向上增长。
^^Alpha^^ 作用为更改参考图透明度，向左淡化向右躯体化。

* * *
### 交互按键表 { #keys }

!!! question "这张表真收录全了吗"
    | 按键 | 作用 |
    | --- | --- |
    | ++f5++ | 刷新地编界面，以及清理非法元素 |
    | ++tab++ | 切换俯视角与自由视角 |
    | ++w++ ++a++ ++s++ ++d++ | 控制方向 |
    | 鼠标滚轮 | 俯视角下调整缩放；自由视角下调整摄影机移动速度 |
    | ++q++ ++e++ | 自由视角下调整摄像头高度 |
    | ++esc++ | 取消选择；摄像头锁定鼠标 / 鼠标脱锁 |
    | ++shift+数字键++ | 快速切换到对应工具 |
    | ++x++ | 笔刷横向锁定 |
    | ++y++ | 笔刷纵向锁定 |
    | ++r++ | 旋转选择的对象 |
    | ++g++ | 移动选择的对象 |
    | ++ctrl+c++ | 复制对象 |
    | ++ctrl+v++ | 粘贴对象 |
    | ++ctrl+z++ | 撤回 |


*[地图缩略图]: 这里指在RWR游戏里按Tab后展开的那个地图，文件名为map.png。
