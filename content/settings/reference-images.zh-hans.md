---
nav_label: "RefpM 说明"
title: "RefpM 说明"
icon: "lucide/image"
description: "用来加参考图。"
tags: [配置文件, 参考图]
---

# RefpM 说明（用来加参考图） { #reference-images }

<p class="kicker">SETTINGS · 把底图垫在地编里</p>

做地图时把一张卫星图或手绘稿垫在下面，照着摆物件。用 **Import** 导入参考图，
**Clear** 移除。

| 控件 | 作用 | 填什么 |
| --- | --- | --- |
| `ScaleX` | 横向压缩或拉长参考图 | 倍率。填 `0.5` 就是横向压到一半 |
| `ScaleY` | 纵向压缩或拉长参考图 | 倍率 |
| `OffsetX` | 横向偏移参考图 | 距离。X 轴向右增长 |
| `OffsetY` | 纵向偏移参考图 | 距离。Y 轴向上增长 |
| `Alpha` | 更改参考图透明度 | 向左淡化，向右实体化 |

??? note "编者原话"
    原样写的是「OffsetX 与 OffsetX 其实是 Y 的作用」「向右躯体化」——
    从上下文看是笔误，这里按 `OffsetY` 与「实体化」写。需要改回原样请告知。
