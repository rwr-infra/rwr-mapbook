---
nav_label: "Wall E"
title: "Wall E"
description: "正常墙与特殊墙，含爆炸物摧毁判定等备注。"
icon: "lucide/box"
# ⚠️ 由 tools/docsgen.py 从 content/tables/wall.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# Wall E { #wall }

<p class="kicker">EDITOR · 墙，以及能不能被打掉</p>

<div class="grid" markdown>

[:octicons-arrow-right-24: 正常墙](#normal){ .card }

[:octicons-arrow-right-24: 特殊墙](#special){ .card }

</div>

!!! tip "怎么读这张表"
    「预览」列按原文的两张图并排给：左侧斜向下视角，右侧正对法线。判断形状请以**水平线**为准，垂直线是点透视。

    两张表：正常墙与特殊墙。备注列里原文写的是待测项（能否翻越、被爆炸摧毁的阈值）。

*[模板]: 物件在 `template = …` 里引用的名字，地编里按这个名字找它


!!! note "原文标注"
    注：模板版本vao0822，视角为侧视，爆炸物摧毁判定貌似需要靠近中间，在两边可能炸不掉，如果墙是隐形的或者形状/材质奇奇怪怪的那大概率是跟平台结合使用的

## 正常墙 { #normal }

| 预览 | 名称 | 备注 |
| --- | --- | --- |
| ![](../assets/tables/wall-e/001.png) | 一号军械库墙<br>template = ArmoryWall1 | 视野（FOV）能否穿透：<br>能否翻过：<br>能否跨墙射击：<br>常规子弹能否穿过及阈值：<br>被载具碾压摧毁的阈值：<br>被爆炸摧毁的阈值： |
| ![](../assets/tables/wall-e/003.png) | 一号带刺铁丝网<br>template = BarbedWire1 |  |
| ![](../assets/tables/wall-e/005.png) | 二号带刺铁丝网<br>template = BarbedWire2 |  |
| ![](../assets/tables/wall-e/007.png) | 带刺铁丝网围栏<br>template = BarbedWireFence1 |  |
| ![](../assets/tables/wall-e/009.png) | 铁丝网墙<br>template = BarbwireWall1 |  |
| ![](../assets/tables/wall-e/011.png) | 一号砖墙<br>template = BrickWall1 |  |
| ![](../assets/tables/wall-e/013.png) | 二号砖墙<br>template = BrickWall2 |  |
| ![](../assets/tables/wall-e/015.png) | 三号砖墙<br>template = BrickWall3 |  |
| ![](../assets/tables/wall-e/017.png) | 砖墙残骸<br>template = BrickWallRuin |  |
| ![](../assets/tables/wall-e/019.png) | 一号悬崖墙<br>template = CliffWall1 |  |
| ![](../assets/tables/wall-e/021.png) | 二号悬崖墙<br>template = CliffWall2 |  |
| ![](../assets/tables/wall-e/023.png) | 一号复合墙<br>template = CompoundWall1 |  |
| ![](../assets/tables/wall-e/025.png) | 可破坏的一号复合墙<br>template = CompoundWallDestructible1 | 可破坏是指代码破坏，正常玩弄不坏 |
| ![](../assets/tables/wall-e/027.png) | 斑马纹围栏<br>template = CorrugatedFence |  |
| ![](../assets/tables/wall-e/029.png) | 一号农场围栏<br>template = FarmFence1 |  |
| ![](../assets/tables/wall-e/031.png) | 二号农场围栏<br>template = FarmFence2 |  |
| ![](../assets/tables/wall-e/033.png) | 一号花园墙<br>template = GardenWall1 |  |
| ![](../assets/tables/wall-e/035.png) | 一号绿篱墙<br>template = HedgerowWall1 |  |
| ![](../assets/tables/wall-e/037.png) | 我的三号砖墙<br>template = MyBrickWall3 |  |
| ![](../assets/tables/wall-e/039.png) | 一号尖板围栏<br>template = PicketFence1 |  |
| ![](../assets/tables/wall-e/041.png) | 二号尖板围栏<br>template = PicketFence2 |  |
| ![](../assets/tables/wall-e/043.png) | 一号平台围栏<br>template = PlatformFence1 |  |
| ![](../assets/tables/wall-e/045.png) | 二号平台围栏<br>template = PlatformFence2 |  |
| ![](../assets/tables/wall-e/047.png) | 泳池墙<br>template = PoolWall |  |
| ![](../assets/tables/wall-e/049.png) | 石头模型墙<br>template = RockMeshWall | 碰撞箱按相应的石头变动<br>![](../assets/tables/wall-e/050.jpg) |
| ![](../assets/tables/wall-e/052.png) | 一号沙袋墙<br>template = SandbagWall1 |  |
| ![](../assets/tables/wall-e/054.png) | 二号沙袋墙<br>template = SandbagWall2 |  |
| ![](../assets/tables/wall-e/056.png) | 沙袋墙残骸<br>template = SandbagWallRuin |  |
| ![](../assets/tables/wall-e/057.png) | 一号安全围栏<br>template = SecurityFence1 |  |
| ![](../assets/tables/wall-e/058.png) | 二号安全围栏<br>template = SecurityFence2 |  |
| ![](../assets/tables/wall-e/059.png) | 一号船舶围栏<br>template = ShipFence1 |  |
| ![](../assets/tables/wall-e/060.png) | 一号侧板墙<br>template = SidePanelWall1 |  |
| ![](../assets/tables/wall-e/061.png) | 一号石墙<br>template = StoneWall1 |  |
| ![](../assets/tables/wall-e/062.png) | 二号石墙<br>template = StoneWall2 |  |
| ![](../assets/tables/wall-e/063.png) | 三号石墙<br>template = StoneWall3 |  |
| ![](../assets/tables/wall-e/064.png) | 一号堡垒石墙<br>template = StoneWallCastle1 |  |
| ![](../assets/tables/wall-e/065.png) | 二号堡垒石墙<br>template = StoneWallCastle2 |  |
| ![](../assets/tables/wall-e/066.png) | 三号堡垒石墙<br>template = StoneWallCastle3 |  |
| ![](../assets/tables/wall-e/067.png) | 一号哥谭城市墙<br>template = Tan_CityWall1st |  |
| ![](../assets/tables/wall-e/068.png) | 一号哥谭城市窗户墙<br>template = Tan_CityWall1stWindow |  |
| ![](../assets/tables/wall-e/069.png) | 二号哥谭城市墙<br>template = Tan_CityWall2nd |  |
| ![](../assets/tables/wall-e/070.png) | 二号哥谭城市地板墙<br>template = Tan_CityWall2ndFloor |  |
| ![](../assets/tables/wall-e/071.png) | 二号哥谭城市窗户墙<br>template = Tan_CityWall2ndWindow |  |
| ![](../assets/tables/wall-e/072.png) | 网球围栏<br>template = TennisFence |  |
| ![](../assets/tables/wall-e/073.png) | 网球球网<br>template = TennisNet |  |
| ![](../assets/tables/wall-e/074.png) | 一号战壕墙<br>template = TrenchWall1 |  |
| ![](../assets/tables/wall-e/075.png) | 二号战壕墙<br>template = TrenchWall2 |  |
| ![](../assets/tables/wall-e/076.png) | 三号战壕墙<br>template = TrenchWall3 |  |
| ![](../assets/tables/wall-e/077.png) | 木柱围栏1<br>template = WoodPostFence1 |  |

## 特殊墙 { #special }

| 预览 | 名称 | 备注 |
| --- | --- | --- |
| ![](../assets/tables/wall-e/002.png) | 一号城堡墙<br>template = CastleWall1 |  |
| ![](../assets/tables/wall-e/004.png) | 二号城堡墙<br>template = CastleWall2 |  |
| ![](../assets/tables/wall-e/006.png) | 三号城堡墙<br>template = CastleWall3 |  |
| ![](../assets/tables/wall-e/008.png) | 一号教堂墙<br>template = ChurchWall1 |  |
| ![](../assets/tables/wall-e/010.png) | 一号虚拟墙<br>template = DummyWall1 |  |
| ![](../assets/tables/wall-e/012.png) | 灰色一号城市墙<br>template = Grey_CityWall1st |  |
| ![](../assets/tables/wall-e/014.png) | 灰色一号城市窗户墙<br>template = Grey_CityWall1stWindow |  |
| ![](../assets/tables/wall-e/016.png) | 灰色二号城市墙<br>template = Grey_CityWall2nd |  |
| ![](../assets/tables/wall-e/018.png) | 灰色二号城市地板墙<br>template = Grey_CityWall2ndFloor |  |
| ![](../assets/tables/wall-e/020.png) | 灰色二号城市窗户墙<br>template = Grey_CityWall2ndWindow |  |
| ![](../assets/tables/wall-e/022.png) | 机库墙<br>template = HangarWall |  |
| ![](../assets/tables/wall-e/024.png) | 一号隐形围栏<br>template = InvisibleFence1 |  |
| ![](../assets/tables/wall-e/026.png) | 一号城堡隐形围栏<br>template = InvisibleFenceCastle1 |  |
| ![](../assets/tables/wall-e/028.png) | 隐形墙<br>template = InvisibleWall |  |
| ![](../assets/tables/wall-e/030.png) | 一号隐形墙<br>template = InvisibleWall1 |  |
| ![](../assets/tables/wall-e/032.png) | 二号隐形墙<br>template = InvisibleWall2 |  |
| ![](../assets/tables/wall-e/034.png) | 三号隐形墙<br>template = InvisibleWall3 |  |
| ![](../assets/tables/wall-e/036.png) | 四号隐形墙<br>template = InvisibleWall4 |  |
| ![](../assets/tables/wall-e/038.png) | 隐形筒仓墙<br>template = InvisibleWallSilo |  |
| ![](../assets/tables/wall-e/040.png) | 一号隐形木柱墙<br>template = InvisibleWoodPostWall1 |  |
| ![](../assets/tables/wall-e/042.png) | 二号隐形木柱墙<br>template = InvisibleWoodPostWall2 |  |
| ![](../assets/tables/wall-e/044.png) | 一号范围墙<br>template = RangeWall1 |  |
| ![](../assets/tables/wall-e/046.png) | 二号范围墙<br>template = RangeWall2 |  |
| ![](../assets/tables/wall-e/048.png) | 三号范围墙<br>template = RangeWall3 |  |
| ![](../assets/tables/wall-e/051.png) | 一号残骸墙<br>template = RuinWall1 |  |
| ![](../assets/tables/wall-e/053.png) | 二号残骸墙<br>template = RuinWall2 |  |
| ![](../assets/tables/wall-e/055.png) | 墙模板<br>template = Wall_Template |  |
