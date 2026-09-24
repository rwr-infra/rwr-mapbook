---
nav_label: "ID 搜索功能說明"
title: "ID 搜索功能說明"
icon: "lucide/search"
description: "報錯時按 ID 定位物件。"
tags: [排錯, 工具]
# ⚠️ 由 tools/docsgen.py 從 content/editor/id-search.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# ID 搜索功能說明 { #id-search }

<p class="kicker">EDITOR · 報錯裡那個數字是什麼</p>

地編報錯時通常會給出一個 ID。按這個 ID 就能把對應物件在地圖上找出來——
這是修圖時最常用的方法。

1. 先在報錯信息裡看 ID（或者看下面「找問題」那幾張圖裡 ID 出現的位置）。

    ![報錯裡的 ID](../../assets/editor/050.png)

2. 把 ID 填進搜索框搜索。

    ![在搜索框裡按 ID 搜](../../assets/editor/051.png)

## 一些找問題的運用

下面這幾張是例子，都是先拿到 ID、再回到地圖上定位：

![按 ID 定位物件（一）](../../assets/editor/052.png)

![按 ID 定位物件（二）](../../assets/editor/053.png)

![按 ID 定位物件（三）](../../assets/editor/054.png)

!!! tip "ID 會變"
    地編每次保存後都會重新排一遍 ID，編號可能和上一次不一樣。
    所以**記下來的是當時的 ID**；隔一次保存再搜，未必還是它。
