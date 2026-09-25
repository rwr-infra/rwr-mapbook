---
nav_label: "歷史版本"
title: "歷史版本"
icon: "lucide/archive"
description: "歷次地編版本的完整歸檔與兩份配套材料，放在站外的對象存儲上，每一條都是直鏈。"
tags: [安裝與配置]
# ⚠️ 由 tools/docsgen.py 從 content/download/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [navigation]
---

# 歷史版本歸檔 { #download }

<p class="kicker">DOWNLOAD · 每一版地編的整包</p>

這裡是歷次地編版本的完整歸檔，從 060 到 0101。每個包就是那一版地編的全套文件，
與當時發在群文件裡的一致。

歸檔**不在本站的倉庫裡**。單是這十份就有 318 MB，跟着倉庫走的話，每個想改文檔的人
都得先下幾百 MB，而這份倉庫裡真正會變的是正文。所以它們放在站外的對象存儲上
（Cloudflare R2），下面每一條都是**直鏈**：瀏覽器能下，下載器（IDM、aria2、迅雷）
也能下，右鍵就能交給它們。

| 版本 | 歸檔 | 下載 |
| --- | --- | --- |
| 地編 060 | `060.zip`　32.1 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/060.zip){ .md-button .md-button--primary } |
| 地編 070 | `070.rar`　26.2 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/070.rar){ .md-button .md-button--primary } |
| 地編 080 | `080.rar`　30.7 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/080.rar){ .md-button .md-button--primary } |
| 地編 081 | `081.rar`　30.7 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/081.rar){ .md-button .md-button--primary } |
| 地編 090 | `090.rar`　30.7 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/090.rar){ .md-button .md-button--primary } |
| 地編 091 | `091.rar`　26.2 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/091.rar){ .md-button .md-button--primary } |
| 地編 0100 | `0100.rar`　31.2 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/0100.rar){ .md-button .md-button--primary } |
| 地編 0101 | `0101.rar`　26.2 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/0101.rar){ .md-button .md-button--primary } |

!!! warning "先看清是哪一版"
    歸檔是**凍結的**：哪一版就是當時那一版的全部文件，之後不會再改。
    手冊正文講的是當前版；拿舊版地編對着看，界面與清單可能對不上。

## 兩份配套材料 { #materials }

建模與配置要用到的另外兩樣東西。用法見[準備工作](../prepare/index.md)：
模板放進地編的 `templates` 文件夾，OgreSDK 則是 `3rdParSettings` 要用到時才裝。

| 材料 | 文件 | 下載 |
| --- | --- | --- |
| 模板（清單版本 vao0822） | `vao0822.svg`　441 kB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary } |
| OgreSDK | `OgreSDK_vc10_v1-7-4.zip`　83.9 MB | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/OgreSDK_vc10_v1-7-4.zip){ .md-button .md-button--primary } |

??? note "校驗用哈希（sha256）"
    下完想確認拿到的是原件，可以對一下：

    ```
    35c9560e78566d0e7c8139e9f8b43f15a7932cf1a20139eea2930710f0c4bddb  060.zip
    eff018db8027e2327a36a45ac0fb2167fb30d593afe987d8cf889b3ae16ecb70  070.rar
    a2b47f4896ea760da64b8ee99a01152a37734e213bf27cee10896a968a1cb3ed  080.rar
    303e30c4d0796aa4bc3a6f85729d5ed9d97efd7d7b434021673406c63651af96  081.rar
    e2b670c0db6156e2414801fdd5167a9a2eff75c62d6f773aa37f45e164eb0446  090.rar
    2479c531f4576e8c5751e15637c422f6ff2ce3654e8c4c4aa3fd5263c1b6eade  091.rar
    84d18efd2fe7de947efe9f44374662961f2a4d5f7e09cb65e4165aafcddd742a  0100.rar
    49de6d2c0175f6a6a01f0f6eaaab93c4f0af394d82151576ad9b36c33c849a55  0101.rar
    e4ec1869d92fc802d8760e8898eba9953b55a2face1c39e74dffee850f1bfc31  vao0822.svg
    2208167d1e2214f196888b3e04b0c4924eb15e37a8de12318a83e2533d2a6a4b  OgreSDK_vc10_v1-7-4.zip
    ```

    歸檔是**凍結**的，哈希不會變；哪天真換了文件，這裡會跟着改——
    它與上面那張表是同一批數字，兩處對不上就是有人改漏了一處。

??? note "這些東西存在哪兒"
    立在 `assets.rwr-infra.uk` 那個域上（Cloudflare R2 的對象存儲），
    倉庫裡既沒有副本、也不走本站的部署——所以整站的產物裡沒有幾百 MB 的二進制，
    克隆這份倉庫要下的是正文，不是歸檔。

