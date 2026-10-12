---
nav_label: "Decal"
title: "Decal"
description: "地面貼花清單。"
icon: "lucide/box"
# ⚠️ 由 tools/docsgen.py 從 content/tables/decal.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# Decal { #decal }
!!! quote "注意事項"
    註：模板版本為vao0822。預覽圖左側為斜向下視角，右側正對法線，也就是地編視角；判斷形狀請以水平線為參考，垂直線是點透視，可能讓物件看起來傾斜。

<p class="kicker">TABLES · 29 項</p>

<div class="ts-search">
  <div class="ts-search__box">
    <span class="ts-search__icon" aria-hidden="true"></span>
    <input class="ts-search__input" type="search" autocomplete="off" spellcheck="false" placeholder="搜索名稱或引用值…" aria-label="搜索清單">
    <kbd class="ts-search__kbd">Ctrl K</kbd>
  </div>
  <p class="ts-search__meta">共 29 項 · 可搜名稱與引用值</p>
</div>


*[模板]: 物件在 `template = …` 裡引用的名字，地編裡按這個名字找它


## 正常物件 <span class="ts-count">21 項</span> { #normal }

| 預覽 | 名稱 | 備註 |
| --- | --- | --- |
| ![](../../assets/tables/decal/001.png)<br>![](../../assets/tables/decal/002.png) | 停機坪<br>template = heliped |  |
| ![](../../assets/tables/decal/003.png)<br>![](../../assets/tables/decal/004.png) | 三葉草草坪<br>template = clover |  |
| ![](../../assets/tables/decal/005.png)<br>![](../../assets/tables/decal/006.png) | 人行道<br>template = pavement |  |
| ![](../../assets/tables/decal/009.png)<br>![](../../assets/tables/decal/010.png) | 人行道<br>template = pavement_tile1 | 正方形磚塊紋理 |
| ![](../../assets/tables/decal/011.png)<br>![](../../assets/tables/decal/012.png) | 屋頂<br>template = roof_tile1 | 長方形磚塊紋理 |
| ![](../../assets/tables/decal/013.png)<br>![](../../assets/tables/decal/014.png) | 檢修井井蓋<br>template = manhole |  |
| ![](../../assets/tables/decal/015.png)<br>![](../../assets/tables/decal/016.png) | 一號裂紋<br>template = cracks_1 |  |
| ![](../../assets/tables/decal/017.png)<br>![](../../assets/tables/decal/018.png) | 二號裂紋<br>template = cracks_2 |  |
| ![](../../assets/tables/decal/019.png)<br>![](../../assets/tables/decal/020.png) | 三號裂紋<br>template = cracks_3 |  |
| ![](../../assets/tables/decal/021.png)<br>![](../../assets/tables/decal/022.png) | 四號裂紋<br>template = cracks_4 |  |
| ![](../../assets/tables/decal/023.png)<br>![](../../assets/tables/decal/024.png) | 五號裂紋<br>template = cracks_5 |  |
| ![](../../assets/tables/decal/025.png)<br>![](../../assets/tables/decal/026.png) | 六號裂紋<br>template = cracks_6 |  |
| ![](../../assets/tables/decal/027.png)<br>![](../../assets/tables/decal/028.png) | 七號裂紋<br>template = cracks_7 |  |
| ![](../../assets/tables/decal/029.png)<br>![](../../assets/tables/decal/030.png) | 停車標線<br>template = parking_line |  |
| ![](../../assets/tables/decal/031.png)<br>![](../../assets/tables/decal/032.png) | 道路標線<br>template = roadline |  |
| ![](../../assets/tables/decal/033.png)<br>![](../../assets/tables/decal/034.png) | 停止標線<br>template = stop_line |  |
| ![](../../assets/tables/decal/035.png)<br>![](../../assets/tables/decal/036.png) | 二號停止標線<br>template = stop_line2 |  |
| ![](../../assets/tables/decal/037.png)<br>![](../../assets/tables/decal/038.png) | 燒焦地面<br>template = burned_ground |  |
| ![](../../assets/tables/decal/046.png)<br>![](../../assets/tables/decal/047.png) | 一號基礎樹蔭<br>template = tree_ground_base1 | 一個淡黑色圓 |
| ![](../../assets/tables/decal/052.png)<br>![](../../assets/tables/decal/053.png) | 一大片網球場<br>template = tennis_court |  |
| ![](../../assets/tables/decal/057.png)<br>![](../../assets/tables/decal/058.png) | 龜裂的地面<br>template = dry_terrain |  |

## 有問題的物件 <span class="ts-count">8 項</span> { #broken }

這幾件東西本身或者它的渲染有問題——名字和引用值能對上，但擺進地圖裡就是下面這個樣子，別當成正常效果去找。

| 預覽 | 名稱 | 備註 |
| --- | --- | --- |
| ![](../../assets/tables/decal/007.png)<br>![](../../assets/tables/decal/008.png) | 花<br>template = flower | 材質引用錯誤，引用成了人行道的 |
| ![](../../assets/tables/decal/039.png)<br>![](../../assets/tables/decal/040.png) | 燒焦地面面<br>template = burned_groundd | 渲染錯誤 |
| ![](../../assets/tables/decal/041.png)<br>![](../../assets/tables/decal/042.png) | 燒焦地面面2<br>template = burned_groundd2 | 渲染錯誤 |
| ![](../../assets/tables/decal/043.png)<br>![](../../assets/tables/decal/044.png) | 燒焦地面面3<br>template = burned_groundd3 | 渲染錯誤 |
| ![](../../assets/tables/decal/045.png) | 樹蔭<br>template = tree_grate | 渲染不完整 |
| ![](../../assets/tables/decal/048.png)<br>![](../../assets/tables/decal/049.png) | 二號基礎樹蔭<br>template = tree_ground_base2 | 渲染不完整 |
| ![](../../assets/tables/decal/050.png)<br>![](../../assets/tables/decal/051.png) | 三號基礎樹蔭<br>template = tree_ground_base3 | 渲染不完整 |
| ![](../../assets/tables/decal/054.png)<br>![](../../assets/tables/decal/055.png) | 神秘棕色方塊<br>template = ee_8 | 渲染錯誤<br>實際上是 KILROY WAS HERE 彩蛋圖標<br>在地圖文件內放了 ee_8 才會正常顯示<br>![](../../assets/tables/decal/056.png) |
