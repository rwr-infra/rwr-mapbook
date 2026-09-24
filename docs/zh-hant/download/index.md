---
nav_label: "歷史版本"
title: "歷史版本"
icon: "lucide/archive"
description: "歷次地編版本的完整歸檔：點一次下載，分包自動取回、校驗並拼成一個整包。"
tags: [安裝與配置]
# ⚠️ 由 tools/docsgen.py 從 content/download/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [navigation, toc]
---

# 歷史版本歸檔 { #download }

<p class="kicker">DOWNLOAD · 每一版地編的整包</p>

這裡是歷次地編版本的完整歸檔，從 060 到 0101。每個包就是那一版地編的全套文件，
與當時發在群文件裡的一致。

點一次「下載」即可：分包由頁面自己取回、逐個核對哈希，最後拼成一個**與原文件同名**
的整包存進下載文件夾。不需要手工合併，也不需要另裝合併工具。

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

!!! note "為什麼要分包"
    託管方對單個文件有大小上限，比它大的歸檔在倉庫裡存成若干片段。
    這件事**只發生在服務器那一側**：頁面把全部片段取回、逐片核對哈希、
    拼成一個整包再交給你。任何一片對不上就停下報錯，不會把半個包塞過來。

!!! warning "先看清是哪一版"
    歸檔是**凍結的**：哪一版就是當時那一版的全部文件，之後不會再改。
    手冊正文講的是當前版；拿舊版地編對着看，界面與清單可能對不上。
