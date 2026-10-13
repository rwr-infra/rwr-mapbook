---
nav_label: "Building E"
title: "Building E"
description: "可放置的房子。"
icon: "lucide/box"
---

# Building E { #building }
!!! warning "注意事项"
    注：由于建筑物只是材质之间互相组合排列，因此本页面只说明相关代码，请自行组合尝试。

!!! note "暂无已校验内容。"

???+ example "**待校验内容。**（展开以查看）"
    | 代码 | 值 | 说明 | 备注 |
    | --- | --- | --- | --- |
    | name | 字符串 | 建筑名 | 通常与外层 rect 的 id（material_XXX）保持一致；地图上建筑 rect 通过 material=XXX 引用它。模板不用展示，直接默认一样就行。 |
    | color | fill<br>stroke<br>0~1的透明度、R、G、B数值 | 墙面颜色 | 例如0.8 0.8 0.8 1.0。模板给几个常用的固定值吧，然后再加一个自定义的选项，当然只有第一个也不是不行。 |
    | color_variance | 0~1的R、G、B数值 | 墙面颜色随机偏移范围 | 让共用同一材质的不同实例产生轻微色差，例如0.0 0.0 0.3。模板应该给俩选项一个是0偏移，一个是自定义偏移选项，当然只给第一个也不是不行。 |
    | detail_texture | wall_atlas1.png<br>自己自定义的图集文件名 | 墙面纹理图集 | 正常情况就是wall_atlas1.png。模板不用展示，固定纹理就行感觉。 |
    | detail_texture_atlas_cell | 列、行、总列数、总行数、边距、边距数值 | 要使用的墙面纹理在图集中的单元位置 | 数据中并存 5 个数与 6 个数两种写法，例如0 1 8 8 0.0078125 0.0078125，貌似只写前面的边距不写后面的那个就默认是正方形？大部分都只写了第一个边距，甚至有一个还没写。这个模板给几个具体名字吧，选了就把属性转成对应的位置，到时候我图鉴去列举这几个都长啥样。 |
    | detail_texture_scale | X缩放、Y缩放倍数数值 | 墙面纹理的缩放 | 以 3 3 最常见。模板根据选的纹理是啥用预设值就行，不展示。 |
    | detail_cutout_texture | cutout.png | 墙面镂空图 | 一共就这一个值，还没试。模板直接固定值得了，不展示。 |
    | detail_cutout_texture_channel | 1 | 墙面镂空图读取的颜色通道 | 一共就这一个值，还没试。模板直接固定值得了，不展示。 |
    | detail_cutout_texture_scale | X缩放、Y缩放数值 | 墙面镂空图缩放 | 模板按相应的预设固定得了。 |
    | atlas_texture | building_atlas2.png<br>building_atlas3.png<br>building_atlas4.png<br>自己自定义的图集文件名 | 墙体主图集大图 | 模板给选择栏？然后我这边图鉴弄下这几个都是啥样。 |
    | 1st_floor_1 | 引用的style样式名称 | 一层正面墙体贴图 | 模板可以一个选项是默认所有面都是一样的，点有差异的再展开成四个面，给预设就行，之后在图鉴看，下同。 |
    | 1st_floor_2 | 引用的style样式名称 | 一层右面墙体贴图 |  |
    | 1st_floor_3 | 引用的style样式名称 | 一层背面墙体贴图 |  |
    | 1st_floor_4 | 引用的style样式名称 | 一层左面墙体贴图 |  |
    | other_floor_1 | 引用的style样式名称 | 其它层正面墙体贴图 |  |
    | other_floor_2 | 引用的style样式名称 | 其它层右面墙体贴图 |  |
    | other_floor_3 | 引用的style样式名称 | 其它层背面墙体贴图 |  |
    | other_floor_4 | 引用的style样式名称 | 其它层左面墙体贴图 |  |
    | roof_texture | wall_atlas1.png<br>自己自定义的图集文件名 | 屋顶纹理图集 | 模板固定得了。 |
    | roof_texture_atlas_cell | 列、行、总列数、总行数、边距、边距数值 | 要使用的屋顶纹理在图集中的单元位置 | 格式同 detail_texture_atlas_cell。这个模板给几个具体名字吧，选了就把属性转成对应的位置，到时候我图鉴去列举这几个都长啥样。 |
    | roof_texture_scale | X缩放、Y缩放倍数数值 | 屋顶纹理的缩放 | 模板根据选的纹理是啥用预设值就行，不展示。 |
    | roof_scale | X缩放、Y缩放倍数数值 | 屋顶贴图整体缩放 | 没试。模板应该还是根据选的给预设吧。 |
    | roof_color | fill<br>stroke<br>0~1的透明度、R、G、B数值 | 屋顶颜色 | 取值规则与 color 相同。模板给几个常用的固定值吧，然后再加一个自定义的选项，当然只有第一个也不是不行。 |
    | roof_color_variance | 0~1的R、G、B数值 | 屋顶颜色随机偏移范围 | 取值规则与color_variance相同。模板应该给俩选项一个是0偏移，一个是自定义偏移选项，当然只给第一个也不是不行。 |
    | roof_cutout_texture | cutout.png<br>自己自定义的镂空图文件名 | 屋顶镂空图 | 一共就这俩值，还没试。模板不展示。 |
    | roof_cutout_texture_channel | 1 | 屋顶镂空图读取的颜色通道 | 一共就这一个值，还没试。模板不展示。 |
    | roof_cutout_texture_scale | X缩放、Y缩放倍数数值 | 屋顶镂空图缩放 | 模板按相应的预设固定得了。 |
    | climbable | 0<br>1 | 是否可攀爬 | 0=不可攀爬，1=可攀爬。模板给个选项？ |
