---
nav_label: "模型清单"
title: "模型清单"
icon: "lucide/table"
description: "Mesh E、Wall E、Building E、Vehicle Scatter、Decal 五张清单。"
nav: ["mesh", "wall", "building", "vehicle", "decal"]
tags: [模型]
# ⚠️ 由 tools/docsgen.py 从 content/tables/index.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [toc]
---

# 模型清单

<p class="kicker">TABLES · 六百多个物件，能不能用</p>

五张表，**模板版本 vao0822**。每一行是一个物件：预览图、它是什么，
以及在地编里实测下来的备注。

| 页 | 内容 | 条目 |
| --- | --- | --- |
| [MESH E](mesh.md) | 石头、植物、小物件、大物件、特殊物件，以及有严重问题的物件 | 311 |
| [Wall E](wall.md) | 正常墙与特殊墙 | 76 |
| [Building E](building.md) | 可放置的房子 | 12 |
| [Vehicle Scatter](vehicle.md) | 载具散布 | 194 |
| [Decal](decal.md) | 地面贴花 | 20 |

!!! warning "预览图怎么看"
    左侧是斜向下视角，右侧是正对法线（也就是地编视角）。请以**水平线**为参考——
    垂直线是点透视，可能让物件看起来是斜的。

!!! tip "每一行的「名称」列"
    斜杠前是它是什么，斜杠后是 `template = …` 的引用名。地编里就按这个名字找它。
