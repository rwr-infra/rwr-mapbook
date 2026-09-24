---
nav_label: "Wall E"
title: "Wall E"
description: "正常牆與特殊牆，含爆炸物摧毀判定等備註。"
icon: "lucide/box"
# ⚠️ 由 tools/docsgen.py 從 content/tables/wall.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# Wall E { #wall }

<p class="kicker">EDITOR · 牆，以及能不能被打掉</p>

<div class="grid" markdown>

[:octicons-arrow-right-24: 正常牆](#normal){ .card }

[:octicons-arrow-right-24: 特殊牆](#special){ .card }

</div>

!!! tip "怎麼讀這張表"
    「預覽」列按兩張圖並排給：左側斜向下視角，右側正對法線。判斷形狀請以**水平線**為準，垂直線是點透視。

    兩張表：正常牆與特殊牆。備註列裡寫的多是待測項（能否翻越、被爆炸摧毀的閾值）。

*[模板]: 物件在 `template = …` 裡引用的名字，地編裡按這個名字找它


!!! note "寫這張表的時候記下的"
    註：模板版本vao0822，視角為側視，爆炸物摧毀判定貌似需要靠近中間，在兩邊可能炸不掉，如果牆是隱形的或者形狀/材質奇奇怪怪的那大概率是跟平臺結合使用的

## 正常牆 { #normal }

| 預覽 | 名稱 | 備註 |
| --- | --- | --- |
| ![](../../assets/tables/wall-e/001.png) | 一號軍械庫牆<br>template = ArmoryWall1 | 視野（FOV）能否穿透：<br>能否翻過：<br>能否跨牆射擊：<br>常規子彈能否穿過及閾值：<br>被載具碾壓摧毀的閾值：<br>被爆炸摧毀的閾值： |
| ![](../../assets/tables/wall-e/003.png) | 一號帶刺鐵絲網<br>template = BarbedWire1 |  |
| ![](../../assets/tables/wall-e/005.png) | 二號帶刺鐵絲網<br>template = BarbedWire2 |  |
| ![](../../assets/tables/wall-e/007.png) | 帶刺鐵絲網圍欄<br>template = BarbedWireFence1 |  |
| ![](../../assets/tables/wall-e/009.png) | 鐵絲網牆<br>template = BarbwireWall1 |  |
| ![](../../assets/tables/wall-e/011.png) | 一號磚牆<br>template = BrickWall1 |  |
| ![](../../assets/tables/wall-e/013.png) | 二號磚牆<br>template = BrickWall2 |  |
| ![](../../assets/tables/wall-e/015.png) | 三號磚牆<br>template = BrickWall3 |  |
| ![](../../assets/tables/wall-e/017.png) | 磚牆殘骸<br>template = BrickWallRuin |  |
| ![](../../assets/tables/wall-e/019.png) | 一號懸崖牆<br>template = CliffWall1 |  |
| ![](../../assets/tables/wall-e/021.png) | 二號懸崖牆<br>template = CliffWall2 |  |
| ![](../../assets/tables/wall-e/023.png) | 一號複合牆<br>template = CompoundWall1 |  |
| ![](../../assets/tables/wall-e/025.png) | 可破壞的一號複合牆<br>template = CompoundWallDestructible1 | 可破壞是指代碼破壞，正常玩弄不壞 |
| ![](../../assets/tables/wall-e/027.png) | 斑馬紋圍欄<br>template = CorrugatedFence |  |
| ![](../../assets/tables/wall-e/029.png) | 一號農場圍欄<br>template = FarmFence1 |  |
| ![](../../assets/tables/wall-e/031.png) | 二號農場圍欄<br>template = FarmFence2 |  |
| ![](../../assets/tables/wall-e/033.png) | 一號花園牆<br>template = GardenWall1 |  |
| ![](../../assets/tables/wall-e/035.png) | 一號綠籬牆<br>template = HedgerowWall1 |  |
| ![](../../assets/tables/wall-e/037.png) | 我的三號磚牆<br>template = MyBrickWall3 |  |
| ![](../../assets/tables/wall-e/039.png) | 一號尖板圍欄<br>template = PicketFence1 |  |
| ![](../../assets/tables/wall-e/041.png) | 二號尖板圍欄<br>template = PicketFence2 |  |
| ![](../../assets/tables/wall-e/043.png) | 一號平臺圍欄<br>template = PlatformFence1 |  |
| ![](../../assets/tables/wall-e/045.png) | 二號平臺圍欄<br>template = PlatformFence2 |  |
| ![](../../assets/tables/wall-e/047.png) | 泳池牆<br>template = PoolWall |  |
| ![](../../assets/tables/wall-e/049.png) | 石頭模型牆<br>template = RockMeshWall | 碰撞箱按相應的石頭變動<br>![](../../assets/tables/wall-e/050.jpg) |
| ![](../../assets/tables/wall-e/052.png) | 一號沙袋牆<br>template = SandbagWall1 |  |
| ![](../../assets/tables/wall-e/054.png) | 二號沙袋牆<br>template = SandbagWall2 |  |
| ![](../../assets/tables/wall-e/056.png) | 沙袋牆殘骸<br>template = SandbagWallRuin |  |
| ![](../../assets/tables/wall-e/057.png) | 一號安全圍欄<br>template = SecurityFence1 |  |
| ![](../../assets/tables/wall-e/058.png) | 二號安全圍欄<br>template = SecurityFence2 |  |
| ![](../../assets/tables/wall-e/059.png) | 一號船舶圍欄<br>template = ShipFence1 |  |
| ![](../../assets/tables/wall-e/060.png) | 一號側板牆<br>template = SidePanelWall1 |  |
| ![](../../assets/tables/wall-e/061.png) | 一號石牆<br>template = StoneWall1 |  |
| ![](../../assets/tables/wall-e/062.png) | 二號石牆<br>template = StoneWall2 |  |
| ![](../../assets/tables/wall-e/063.png) | 三號石牆<br>template = StoneWall3 |  |
| ![](../../assets/tables/wall-e/064.png) | 一號堡壘石牆<br>template = StoneWallCastle1 |  |
| ![](../../assets/tables/wall-e/065.png) | 二號堡壘石牆<br>template = StoneWallCastle2 |  |
| ![](../../assets/tables/wall-e/066.png) | 三號堡壘石牆<br>template = StoneWallCastle3 |  |
| ![](../../assets/tables/wall-e/067.png) | 一號哥譚城市牆<br>template = Tan_CityWall1st |  |
| ![](../../assets/tables/wall-e/068.png) | 一號哥譚城市窗戶牆<br>template = Tan_CityWall1stWindow |  |
| ![](../../assets/tables/wall-e/069.png) | 二號哥譚城市牆<br>template = Tan_CityWall2nd |  |
| ![](../../assets/tables/wall-e/070.png) | 二號哥譚城市地板牆<br>template = Tan_CityWall2ndFloor |  |
| ![](../../assets/tables/wall-e/071.png) | 二號哥譚城市窗戶牆<br>template = Tan_CityWall2ndWindow |  |
| ![](../../assets/tables/wall-e/072.png) | 網球圍欄<br>template = TennisFence |  |
| ![](../../assets/tables/wall-e/073.png) | 網球球網<br>template = TennisNet |  |
| ![](../../assets/tables/wall-e/074.png) | 一號戰壕牆<br>template = TrenchWall1 |  |
| ![](../../assets/tables/wall-e/075.png) | 二號戰壕牆<br>template = TrenchWall2 |  |
| ![](../../assets/tables/wall-e/076.png) | 三號戰壕牆<br>template = TrenchWall3 |  |
| ![](../../assets/tables/wall-e/077.png) | 木柱圍欄1<br>template = WoodPostFence1 |  |

## 特殊牆 { #special }

| 預覽 | 名稱 | 備註 |
| --- | --- | --- |
| ![](../../assets/tables/wall-e/002.png) | 一號城堡牆<br>template = CastleWall1 |  |
| ![](../../assets/tables/wall-e/004.png) | 二號城堡牆<br>template = CastleWall2 |  |
| ![](../../assets/tables/wall-e/006.png) | 三號城堡牆<br>template = CastleWall3 |  |
| ![](../../assets/tables/wall-e/008.png) | 一號教堂牆<br>template = ChurchWall1 |  |
| ![](../../assets/tables/wall-e/010.png) | 一號虛擬牆<br>template = DummyWall1 |  |
| ![](../../assets/tables/wall-e/012.png) | 灰色一號城市牆<br>template = Grey_CityWall1st |  |
| ![](../../assets/tables/wall-e/014.png) | 灰色一號城市窗戶牆<br>template = Grey_CityWall1stWindow |  |
| ![](../../assets/tables/wall-e/016.png) | 灰色二號城市牆<br>template = Grey_CityWall2nd |  |
| ![](../../assets/tables/wall-e/018.png) | 灰色二號城市地板牆<br>template = Grey_CityWall2ndFloor |  |
| ![](../../assets/tables/wall-e/020.png) | 灰色二號城市窗戶牆<br>template = Grey_CityWall2ndWindow |  |
| ![](../../assets/tables/wall-e/022.png) | 機庫牆<br>template = HangarWall |  |
| ![](../../assets/tables/wall-e/024.png) | 一號隱形圍欄<br>template = InvisibleFence1 |  |
| ![](../../assets/tables/wall-e/026.png) | 一號城堡隱形圍欄<br>template = InvisibleFenceCastle1 |  |
| ![](../../assets/tables/wall-e/028.png) | 隱形牆<br>template = InvisibleWall |  |
| ![](../../assets/tables/wall-e/030.png) | 一號隱形牆<br>template = InvisibleWall1 |  |
| ![](../../assets/tables/wall-e/032.png) | 二號隱形牆<br>template = InvisibleWall2 |  |
| ![](../../assets/tables/wall-e/034.png) | 三號隱形牆<br>template = InvisibleWall3 |  |
| ![](../../assets/tables/wall-e/036.png) | 四號隱形牆<br>template = InvisibleWall4 |  |
| ![](../../assets/tables/wall-e/038.png) | 隱形筒倉牆<br>template = InvisibleWallSilo |  |
| ![](../../assets/tables/wall-e/040.png) | 一號隱形木柱牆<br>template = InvisibleWoodPostWall1 |  |
| ![](../../assets/tables/wall-e/042.png) | 二號隱形木柱牆<br>template = InvisibleWoodPostWall2 |  |
| ![](../../assets/tables/wall-e/044.png) | 一號範圍牆<br>template = RangeWall1 |  |
| ![](../../assets/tables/wall-e/046.png) | 二號範圍牆<br>template = RangeWall2 |  |
| ![](../../assets/tables/wall-e/048.png) | 三號範圍牆<br>template = RangeWall3 |  |
| ![](../../assets/tables/wall-e/051.png) | 一號殘骸牆<br>template = RuinWall1 |  |
| ![](../../assets/tables/wall-e/053.png) | 二號殘骸牆<br>template = RuinWall2 |  |
| ![](../../assets/tables/wall-e/055.png) | 牆模板<br>template = Wall_Template |  |
