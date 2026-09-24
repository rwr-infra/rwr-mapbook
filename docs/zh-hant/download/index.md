---
nav_label: "歷史版本"
title: "歷史版本"
icon: "lucide/archive"
description: "歷次地編版本的完整歸檔與兩份配套材料：點一次下載，分包自動取回、校驗並拼成一個整包。"
tags: [安裝與配置]
# ⚠️ 由 tools/docsgen.py 從 content/download/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [navigation]
---

# 歷史版本歸檔 { #download }

<p class="kicker">DOWNLOAD · 每一版地編的整包</p>

這裡是歷次地編版本的完整歸檔，從 060 到 0101。每個包就是那一版地編的全套文件，
與當時發在群文件裡的一致。

「下載」有兩種走法。沒超過部署上限的整包是**一個普通文件**，按鈕就是直鏈——瀏覽器
能下，下載器也能下。超過上限的會存成若干片段，那種由頁面把分片取回、逐片核對哈希，
拼成一個**與原文件同名**的整包。兩種情況落到下載文件夾裡的都是一個整包，
不會出現 `.partNNN`，也不需要手工合併。

| 版本 | 歸檔 | 下載 |
| --- | --- | --- |
| 地編 060 | `060.zip`<br><span data-dl-size="060">—</span> | <button type="button" class="md-button md-button--primary" data-dl="060">下載</button> <span class="dl-status" data-dl-status="060"></span> |
| 地編 070 | `070.rar`<br><span data-dl-size="070">—</span> | <button type="button" class="md-button md-button--primary" data-dl="070">下載</button> <span class="dl-status" data-dl-status="070"></span> |
| 地編 080 | `080.rar`<br><span data-dl-size="080">—</span> | <button type="button" class="md-button md-button--primary" data-dl="080">下載</button> <span class="dl-status" data-dl-status="080"></span> |
| 地編 081 | `081.rar`<br><span data-dl-size="081">—</span> | <button type="button" class="md-button md-button--primary" data-dl="081">下載</button> <span class="dl-status" data-dl-status="081"></span> |
| 地編 090 | `090.rar`<br><span data-dl-size="090">—</span> | <button type="button" class="md-button md-button--primary" data-dl="090">下載</button> <span class="dl-status" data-dl-status="090"></span> |
| 地編 091 | `091.rar`<br><span data-dl-size="091">—</span> | <button type="button" class="md-button md-button--primary" data-dl="091">下載</button> <span class="dl-status" data-dl-status="091"></span> |
| 地編 0100 | `0100.rar`<br><span data-dl-size="0100">—</span> | <button type="button" class="md-button md-button--primary" data-dl="0100">下載</button> <span class="dl-status" data-dl-status="0100"></span> |
| 地編 0101 | `0101.rar`<br><span data-dl-size="0101">—</span> | <button type="button" class="md-button md-button--primary" data-dl="0101">下載</button> <span class="dl-status" data-dl-status="0101"></span> |

!!! warning "先看清是哪一版"
    歸檔是**凍結的**：哪一版就是當時那一版的全部文件，之後不會再改。
    手冊正文講的是當前版；拿舊版地編對着看，界面與清單可能對不上。

## 兩份配套材料 { #materials }

建模與配置要用到的另外兩樣東西。用法見[準備工作](../prepare/index.md)：
模板放進地編的 `templates` 文件夾，OgreSDK 則是 `3rdParSettings` 要用到時才裝。

| 材料 | 文件 | 下載 |
| --- | --- | --- |
| 模板（清單版本 vao0822） | `vao0822.svg`<br><span data-dl-size="vao0822">—</span> | <button type="button" class="md-button md-button--primary" data-dl="vao0822">下載</button> <span class="dl-status" data-dl-status="vao0822"></span> |
| OgreSDK | `OgreSDK_vc10_v1-7-4.zip`<br><span data-dl-size="OgreSDK_vc10_v1-7-4">—</span> | <button type="button" class="md-button md-button--primary" data-dl="OgreSDK_vc10_v1-7-4">下載</button> <span class="dl-status" data-dl-status="OgreSDK_vc10_v1-7-4"></span> |

!!! note "直鏈，還是由頁面拼"
    本站部署在 EdgeOne Pages，**單個文件最大 25 MB**，而地編的整包是 26–84 MB，
    塞不進一個文件裡。所以：

    * 沒超上限的（比如那份 441 kB 的模板）就是一個**普通文件**，按鈕是直鏈：
      瀏覽器能下，下載器也能下（右鍵就能交給它）；
    * 超了上限的存成若干片段，那種**只能由頁面拼**。分片是倉庫裡的真實地址沒錯，
      但那是幾段，交給下載器只會拿到幾段 `.partNNN`，還得自己合併。頁面把全部片段
      取回、逐片核對哈希、拼成一個整包再交給你；任何一片對不上就停下報錯，
      不會把半個包塞過來。
