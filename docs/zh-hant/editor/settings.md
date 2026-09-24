---
nav_label: "主界面"
title: "主界面"
icon: "lucide/sliders-horizontal"
description: "Save / ViewMap / Select / PinMan / WallE / BuildingE 等按鈕的逐項說明。"
tags: [界面, 工具]
# ⚠️ 由 tools/docsgen.py 從 content/editor/settings.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 主界面

<p class="kicker">EDITOR · 十四個按鈕，各管一件事</p>

地編的頂欄從左到右排着這些工具。下面按順序逐項說明——每一條都是**用出來的**，不是從界面文字猜的。

<div class="grid cards" markdown>

-   __Save__

    ---

    存地圖

    [:octicons-arrow-right-24: 說明](#save)

-   __ViewMap__

    ---

    生成戰術預覽圖

    [:octicons-arrow-right-24: 說明](#viewmap)

-   __Select__

    ---

    選擇、移動、旋轉

    [:octicons-arrow-right-24: 說明](#select)

-   __PinMan__

    ---

    放參照物

    [:octicons-arrow-right-24: 說明](#pinman)

-   __WallE__

    ---

    畫牆

    [:octicons-arrow-right-24: 說明](#walle)

-   __BuildingE__

    ---

    放房子

    [:octicons-arrow-right-24: 說明](#buildinge)

-   __PlatformE__

    ---

    畫平臺、改高度

    [:octicons-arrow-right-24: 說明](#platforme)

-   __FuncObjects__

    ---

    梯子、箱子、復活點、據點

    [:octicons-arrow-right-24: 說明](#funcobjects)

-   __MeshE__

    ---

    擺模型、電線杆

    [:octicons-arrow-right-24: 說明](#meshe)

-   __HeightMap__

    ---

    刷地形高度

    [:octicons-arrow-right-24: 說明](#heightmap)

-   __TerrainBash__

    ---

    刷地面質地

    [:octicons-arrow-right-24: 說明](#terrainbash)

-   __offroadbuilder__

    ---

    給 AI 標開車路線

    [:octicons-arrow-right-24: 說明](#offroadbuilder)

-   __Decal__

    ---

    地面貼花

    [:octicons-arrow-right-24: 說明](#decal)

-   __Assaum__

    ---

    現成的組件

    [:octicons-arrow-right-24: 說明](#assaum)

-   __一些額外說明__

    ---

    疊放順序、ID 重排這些繞不開的坑

    [:octicons-arrow-right-24: 說明](#extra)

-   __如何畫平臺？__

    ---

    從高處緩坡下到水裡，一步步畫一遍

    [:octicons-arrow-right-24: 說明](#platform)

</div>


## Save 說明 { #save }

簡簡單單保存地圖，保存完會有提示音。

## ViewMap 說明 { #viewmap }

生成地圖的戰術預覽圖，也就是 RWR 裡面按 Tab 查看的地圖。

!!! question "存疑"
    文件名貌似得自己調一下？

## Select 說明 { #select }

- 左鍵點擊進行單個選擇、Ctrl+左鍵點擊或左鍵拖動進行多個選擇。
- 按 Esc 鍵取消選擇。
- 按 Delete 鍵刪除選擇的目標。
- 按 G 鍵啟用移動模式，此時移動鼠標可將選擇的對象拖走。
- 按 R 鍵啟用旋轉模式，此時移動鼠標可將選擇的對象旋轉至某個角度。
- 在其它工具模式中，按 Shift+1 快捷鍵可快速切換回 Select 工具。
- 無法同時選擇多個平臺。
- 俯視角模式（正交）下會導致部分平臺無法正常顯示與選擇，此時需要切換到飛行模式（透視）來進行選擇。
- 不建議在飛行模式（透視）下進行移動與旋轉，交互有點夠使。

## PinMan 說明 { #pinman }

用來在點擊的位置上放置一個虛擬的參照物。

雖然有三個選項但是只有坦克能用。

## WallE 說明 { #walle }

- 用來在列表中選擇各種牆的種類，並使用 PathBush 繪製節點然後按空格自動以擺放順序連成線。既可以先選擇牆的種類後繪製，也可以先繪製然後再選擇牆的種類，選擇後點擊已經畫好的牆即可完成替換。
- 在搜索欄中可搜索對應名稱來快速選擇對象，每種牆的作用見[模型清單 · Wall E](../tables/wall.md)。
- 在用 Select 選中後，可以在這個界面編輯坐標（第一項為 X 軸向右增長、第二項為 Y 軸向下增長，數據為鼠標當前位置坐標的二倍）、使用 Add Point 來在繪製方向增加一條相連的線段、使用叉號來刪除這段節點。
- 在用 Select 選中多個後，可以在這個界面進行刪除指定對象的操作，Buiding、Mesh 等同理。
- 在用 Select 選中後，可以在這個界面查看 id、當前層、牆的種類以及設置自定義高度與是否 Merge。
- Marge 默認勾選，目的是防止 AI 卡牆翻不過去。
- 勾選 ReHeight 後，可以自行輸入牆的高度。

![主界面 1](../../assets/editor/017.png)

![主界面 2](../../assets/editor/018.png)

![主界面 3](../../assets/editor/019.png)

![主界面 4](../../assets/editor/020.png)

## BuildingE 說明 { #buildinge }

- 用來在列表中選擇各種建築物的種類，並使用 DrawBush 按住左鍵拖動來繪製建築物。既可以先選擇建築物的種類後繪製，也可以先繪製然後再選擇建築物的種類，選擇後點擊已經畫好的建築物即可完成替換。
- 在搜索欄中可搜索對應名稱來快速選擇對象，每種建築的外形見[模型清單 · Building E](../tables/building.md)。
- 最上方 HeightDown 與 HeightUp 的作用為改變點擊位置的 Building 高度，每次變化 2（6）。
- RoofSwitch 的作用為將屋頂變為尖頂/平頂，尖頂方向固定需要選擇建築物後按 R 自行旋轉。
- 建議先調整完 Height 後再在上方疊加新的對象，上方的對象高度不會隨下方 Building 高度的變化而變化。
- 在用 Select 選中後，可以在這個界面查看 id、當前層、屋頂是否為尖頂、建築物的種類。
- Offset 的作用是設置自定義偏移度（第一項為 X 軸向右增長、第二項為 Z 軸向頂部增長、第三項為 Y 軸向下增長）。
- 目前 X 軸改不了。

!!! warning "待修復"
    在飛行模式（透視）下，不同方向的透視有嚴重問題，見上方右側例圖。

![主界面 5](../../assets/editor/021.png)

![主界面 6](../../assets/editor/022.png)

![主界面 7](../../assets/editor/023.png)

![主界面 8](../../assets/editor/024.png)

![主界面 9](../../assets/editor/025.png)

## PlatformE 說明 { #platforme }

- 用來在列表中選擇各種平臺的種類，並使用 pathBush 繪製，與 Wall 類似，不再贅述。
- 例子說明見下方：如何畫平臺？
- 搜索欄與 Wall 類似，不再贅述。
- 最下方的 TypeChange 的作用為讓點擊位置的 Platform 在無特殊屬性、deck 屬性、bridge 屬性之間切換。（這一節還沒寫完）
- ChangeHei 的操作為在設置完成高度後按回車進入工具使用狀態，作用為改變點擊位置的 Platform 高度。
- 在用 Select 選中後，可以在這個界面編輯坐標，方法與 Wall 類似，不再贅述。
- 在用 Select 選中後，可以在這個界面查看 type、id、當前層、頂部材質、平臺側面牆的種類、平臺上方附加牆的種類、牆的高度。
- 平臺上方附加牆的種類可以使用 WallE 工具進行更改。
- SetMaterial 中添加的值可以是 wood、grass、pavement、terrian。（這一節還沒寫完）

![主界面 10](../../assets/editor/026.png)

![主界面 11](../../assets/editor/027.png)

![主界面 12](../../assets/editor/028.png)

![主界面 13](../../assets/editor/029.png)

## FuncObjects 說明 { #funcobjects }

LadderScatter 與 LadderEraser 的作用為放置梯子與刪除梯子。放置的梯子會自動吸附在旁邊建築物、平臺等等有固定碰撞的東西上。

!!! warning "待優化"
    目前吸附堪比哈基米，有點問題。

- ItemSupplyScatter 的作用為放置一個儲藏室或軍械庫的判定區，stash 為儲藏室，weapon_rack 為軍械庫，選中後點擊下方 ChangeType 進行切換。
- CrateScatter 與 CrateEraser 的作用為放置木頭箱子與刪除木頭箱子，裡面的物品隨機無法指定。
- SpawnScatter 與 SpawnEraser 的作用為創建復活點與刪除復活點，復活點不宜太靠近地圖邊界。
- BaseScatter 的作用為左鍵拖動創建據點，在用 Select 選中後，可以分別更改據點的名字顯示與指定該劇點最開始被哪個陣營佔領，填寫 0、1、2，分別為我也不知道對應哪個哈哈 XD

![主界面 14](../../assets/editor/030.png)

![主界面 15](../../assets/editor/031.png)

## MeshE 說明 { #meshe }

- 用來在列表中選擇各種模型的種類。
- 搜索欄與 Wall 類似，不再贅述。
- StoneEraser 與 StoneScatter 的作用為刪除一個隨機石頭或放置一個隨機石頭，石頭的樣子見[模型清單 · MESH E](../tables/mesh.md)。
- TreeEraser 與 TreeScatter 的作用為刪除一個隨機樹或放置一個隨機樹，樹的樣子見[模型清單 · MESH E](../tables/mesh.md)。
- 最下方的工具使用方法與 Wall 類似，作用為放置電線杆子作為節點，放完後按空格進行按順序的兩兩間電線連線，電線僅為裝飾物，無碰撞。
- 在用 Select 選中後，可以在這個界面查看 id、種類、碰撞體積（如果是默認則不顯示）。
- 勾選 ReCollision 後可在上方窗口內更改長、高、寬（以中心為基準）。
- offset 的作用是設置自定義偏移度（第一項為 X 軸向右增長、第二項為 Z 軸向頂部增長、第三項為 Y 軸向下增長）。

![主界面 16](../../assets/editor/032.png)

![主界面 17](../../assets/editor/033.png)

![主界面 18](../../assets/editor/034.png)

![主界面 19](../../assets/editor/035.png)

## HeightMap 說明 { #heightmap }

- HeightBush 的作用為地形刷，左下角界面中的 SetHardness 為硬度，決定着當前刷取地形的高度與背景高度的過渡陡緩，範圍為 0 到 1、SerRange 為地形刷的範圍、SetHeight 為地形刷的高度，範圍為 0 到 1。按 X 橫向鎖定筆刷，按 Y 縱向鎖定。
- HeightSmudge 的作用為拖拽鼠標下一定範圍內的高度，並跟隨鼠標移動方向使臨近的地形產生過渡形變。
- Smooth 的作用為平緩全圖的地形。
- Noise 的作用為對全圖增加地形上的噪音，讓整個地圖不是同一個高度數值的大平地，有些微小起伏。
- heightPath 的作用為路徑地形刷，使用方式類似 Wall 工具，相關數據調整左上角均有說明，可自行嘗試。

![主界面 20](../../assets/editor/036.png)

![主界面 21](../../assets/editor/037.png)

## TerrainBash 說明 { #terrainbash }

- Pathpainter 的作用為路徑地面質地刷，使用方式類似 Wall 工具，相關數據調整左上角均有說明，可自行嘗試。
- 衰減指數的調成為[與]，並不是描述打重複變成[[/]] 了。
- painter 的作用為地面質地刷，Chg Index 為材質種類，填數字、Chg Rng 為範圍、Chg Har 為硬度。
- 0101 版本中使用這個工具的時候左下角可能會有個多餘的調節欄，實際啥用沒有。
- Smooth 的作用為平緩全圖的地面質地。

![主界面 22](../../assets/editor/038.png)

![主界面 23](../../assets/editor/039.png)

## offroadbuilder 說明 { #offroadbuilder }

用來給 AI 判定這個路線是開車路線，放飛駕駛。

使用方法類似 Wall 工具。

## Decal 說明 { #decal }

- 用來在列表中選擇各種貼花的種類，可以理解為在地面質地上再印一層材質，選擇後左鍵即可放置。
- deleteDecals 的作用為刪除框選範圍內的貼花。
- Select 選中後，可以使用 Length 更改這個貼花的大小，也就是縮放比例。

![主界面 24](../../assets/editor/040.png)

## Assaum 說明 { #assaum }

用來在列表中選擇各種組件，例如已經製作好碰撞箱和判定區的軍械庫等，選擇後左鍵即可放置。

Add 與 Name 暫時不可用，無效果。

## 一些額外說明 { #extra }

1.如果你想在一個 Building 上面放 Wall、Building、Platform 之類的東西，那麼應該在構思完之後從下往上繪製，繪製的時候需要保證起點在上一個元素之內，這樣所有的對象就都會按照 layer1、layer2….去逐個疊加，並自動銜接上一個的高度，攀爬等判定也會正常生效。

2.地編在每次保存之後都會重新排序一遍 ID，編號可能會發生變動。

## 如何畫平臺？ { #platform }

以過渡的山崖平臺為例：

我們這次的目的是要從左側的高處用緩坡到達谷底的水中，可以看到在箭頭方向的左側是一個不那麼平緩的坡，右側則為陡崖，那我們就應該以左側的坡的高度為基準製作一個過度的山崖。

![主界面 25](../../assets/editor/041.png)

![主界面 26](../../assets/editor/042.png)

因為繪製平臺時需保證終點邊在起點邊行進方向右邊，同時起點邊為判定高度的邊，所以我們應該先在箭頭的左側緩坡處，沿着圖一的箭頭方向繪製。

（畫了八個點，如果想讓變化更均勻可以多點幾個）之後按空格，在箭頭右側放置另外對應的八個點，按第二空格次完成繪製。

![主界面 27](../../assets/editor/043.png)

![主界面 28](../../assets/editor/044.png)

之後對平臺進行細緻調整，使其合理。

（藍色點為基準點，也就是第一次畫線生成的點，藍點到粉點之間的連線就是地形的過渡）

（如果你的平臺是紫黑相間的錯誤渲染顏色，那麼恭喜你你放反了，請再次注意繪製平臺時需保證終點邊在起點邊行進方向右邊）

（反正圖片也沒壓縮，細節自行放大查看吧）

![主界面 29](../../assets/editor/045.png)

進遊戲看看~

果不其然做的一坨，可見多加幾個錨點和完善地形的重要性，希望各位引以為戒:(

![主界面 30](../../assets/editor/046.png)
