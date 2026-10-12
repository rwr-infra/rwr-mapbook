---
nav_label: "Decal"
title: "Decal"
description: "地面贴花清单。"
icon: "lucide/box"
---

# Decal { #decal }
!!! quote "注意事项"
    注：模板版本为vao0822。预览图左侧为斜向下视角，右侧正对法线，也就是地编视角；判断形状请以水平线为参考，垂直线是点透视，可能让物件看起来倾斜。

<p class="kicker">TABLES · <!--count--> 项</p>

<div class="ts-search">
  <div class="ts-search__box">
    <span class="ts-search__icon" aria-hidden="true"></span>
    <input class="ts-search__input" type="search" autocomplete="off" spellcheck="false" placeholder="搜索名称或引用值…" aria-label="搜索清单">
    <kbd class="ts-search__kbd">Ctrl K</kbd>
  </div>
  <p class="ts-search__meta">共 <!--count--> 项 · 可搜名称与引用值</p>
</div>


*[模板]: 物件在 `template = …` 里引用的名字，地编里按这个名字找它


## 正常物件 <span class="ts-count"><!--count--> 项</span> { #normal }

| 预览 | 名称 | 备注 |
| --- | --- | --- |
| ![](../assets/tables/decal/001.png)<br>![](../assets/tables/decal/002.png) | 停机坪<br>template = heliped |  |
| ![](../assets/tables/decal/003.png)<br>![](../assets/tables/decal/004.png) | 三叶草草坪<br>template = clover |  |
| ![](../assets/tables/decal/005.png)<br>![](../assets/tables/decal/006.png) | 人行道<br>template = pavement |  |
| ![](../assets/tables/decal/009.png)<br>![](../assets/tables/decal/010.png) | 人行道<br>template = pavement_tile1 | 正方形砖块纹理 |
| ![](../assets/tables/decal/011.png)<br>![](../assets/tables/decal/012.png) | 屋顶<br>template = roof_tile1 | 长方形砖块纹理 |
| ![](../assets/tables/decal/013.png)<br>![](../assets/tables/decal/014.png) | 检修井井盖<br>template = manhole |  |
| ![](../assets/tables/decal/015.png)<br>![](../assets/tables/decal/016.png) | 一号裂纹<br>template = cracks_1 |  |
| ![](../assets/tables/decal/017.png)<br>![](../assets/tables/decal/018.png) | 二号裂纹<br>template = cracks_2 |  |
| ![](../assets/tables/decal/019.png)<br>![](../assets/tables/decal/020.png) | 三号裂纹<br>template = cracks_3 |  |
| ![](../assets/tables/decal/021.png)<br>![](../assets/tables/decal/022.png) | 四号裂纹<br>template = cracks_4 |  |
| ![](../assets/tables/decal/023.png)<br>![](../assets/tables/decal/024.png) | 五号裂纹<br>template = cracks_5 |  |
| ![](../assets/tables/decal/025.png)<br>![](../assets/tables/decal/026.png) | 六号裂纹<br>template = cracks_6 |  |
| ![](../assets/tables/decal/027.png)<br>![](../assets/tables/decal/028.png) | 七号裂纹<br>template = cracks_7 |  |
| ![](../assets/tables/decal/029.png)<br>![](../assets/tables/decal/030.png) | 停车标线<br>template = parking_line |  |
| ![](../assets/tables/decal/031.png)<br>![](../assets/tables/decal/032.png) | 道路标线<br>template = roadline |  |
| ![](../assets/tables/decal/033.png)<br>![](../assets/tables/decal/034.png) | 停止标线<br>template = stop_line |  |
| ![](../assets/tables/decal/035.png)<br>![](../assets/tables/decal/036.png) | 二号停止标线<br>template = stop_line2 |  |
| ![](../assets/tables/decal/037.png)<br>![](../assets/tables/decal/038.png) | 烧焦地面<br>template = burned_ground |  |
| ![](../assets/tables/decal/046.png)<br>![](../assets/tables/decal/047.png) | 一号基础树荫<br>template = tree_ground_base1 | 一个淡黑色圆 |
| ![](../assets/tables/decal/052.png)<br>![](../assets/tables/decal/053.png) | 一大片网球场<br>template = tennis_court |  |
| ![](../assets/tables/decal/057.png)<br>![](../assets/tables/decal/058.png) | 龟裂的地面<br>template = dry_terrain |  |

## 有问题的物件 <span class="ts-count"><!--count--> 项</span> { #broken }

这几件东西本身或者它的渲染有问题——名字和引用值能对上，但摆进地图里就是下面这个样子，别当成正常效果去找。

| 预览 | 名称 | 备注 |
| --- | --- | --- |
| ![](../assets/tables/decal/007.png)<br>![](../assets/tables/decal/008.png) | 花<br>template = flower | 材质引用错误，引用成了人行道的 |
| ![](../assets/tables/decal/039.png)<br>![](../assets/tables/decal/040.png) | 烧焦地面面<br>template = burned_groundd | 渲染错误 |
| ![](../assets/tables/decal/041.png)<br>![](../assets/tables/decal/042.png) | 烧焦地面面2<br>template = burned_groundd2 | 渲染错误 |
| ![](../assets/tables/decal/043.png)<br>![](../assets/tables/decal/044.png) | 烧焦地面面3<br>template = burned_groundd3 | 渲染错误 |
| ![](../assets/tables/decal/045.png) | 树荫<br>template = tree_grate | 渲染不完整 |
| ![](../assets/tables/decal/048.png)<br>![](../assets/tables/decal/049.png) | 二号基础树荫<br>template = tree_ground_base2 | 渲染不完整 |
| ![](../assets/tables/decal/050.png)<br>![](../assets/tables/decal/051.png) | 三号基础树荫<br>template = tree_ground_base3 | 渲染不完整 |
| ![](../assets/tables/decal/054.png)<br>![](../assets/tables/decal/055.png) | 神秘棕色方块<br>template = ee_8 | 渲染错误<br>实际上是 KILROY WAS HERE 彩蛋图标<br>在地图文件内放了 ee_8 才会正常显示<br>![](../assets/tables/decal/056.png) |
