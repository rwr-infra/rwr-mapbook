---
nav_label: "模型清單"
title: "模型清單"
icon: "lucide/table"
description: "Mesh E、Wall E、Building E、Vehicle Scatter、Decal 五張清單。"
nav: ["mesh", "wall", "building", "vehicle", "decal"]
tags: [模型]
# ⚠️ 由 tools/docsgen.py 從 content/tables/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [toc]
---

# 模型清單

<p class="kicker">TABLES · 六百多個物件，能不能用</p>

五張表，**模板版本 vao0822**。每一行是一個物件：預覽圖、它是什麼，
以及地編裡實測的備註。

| 頁 | 內容 | 條目 |
| --- | --- | --- |
| [MESH E](mesh.md) | 石頭、植物、小物件、大物件、特殊物件，以及有嚴重問題的物件 | 311 |
| [Wall E](wall.md) | 正常牆與特殊牆 | 76 |
| [Building E](building.md) | 可放置的房子 | 12 |
| [Vehicle Scatter](vehicle.md) | 載具散布 | 194 |
| [Decal](decal.md) | 地面貼花 | 20 |

!!! warning "預覽圖怎麼看"
    左側是斜向下視角，右側正對法線，也就是地編裡的視角。判斷形狀以**水平線**為準——
    垂直線是點透視，可能讓物件看起來是斜的。

!!! tip "每一行的「名稱」列"
    斜槓前是它是什麼，斜槓後是 `template = …` 的引用名；地編裡按這個名字找它。
