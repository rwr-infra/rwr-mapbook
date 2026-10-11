---
nav_label: "文件下載"
title: "文件下載"
icon: "lucide/archive"
description: "地編各版本的完整歸檔、三種模板與預製件組件，放在站外的對象存儲上，每一條都是直鏈。"
# ⚠️ 由 tools/docsgen.py 從 content/download/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [navigation]
---
目前可以提供的下載項目有地編軟件、地圖模板以及組件（預製件）。

## 地編下載 { #download .section-title }

這裡是歷次地編版本的完整歸檔，從 060 到 0101 。每個包就是那一版地編的全套文件，與群裡發布的一致。

<div class="ts-plain" markdown="1">

**最新版本：**

| 版本 | 歸檔 | 備註 | 下載 |
| --- | --- | --- | --- |
| 地編 0101 | `0101.rar`　26.2 MB | 最新版本，教程正文對着它寫 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/0101.rar){ .md-button .md-button--primary } |

**歷史版本：**

??? note "展開查看全部歷史版本（060 到 0100）"
    | 版本 | 歸檔 | 備註 | 下載 |
    | --- | --- | --- | --- |
    | 地編 0100 | `0100.rar`　31.2 MB | 上一版，與 0101 差異不大 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/0100.rar){ .md-button .md-button--primary } |
    | 地編 091 | `091.rar`　26.2 MB | 舊版，界面與清單可能對不上 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/091.rar){ .md-button .md-button--primary } |
    | 地編 090 | `090.rar`　30.7 MB | 舊版，界面與清單可能對不上 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/090.rar){ .md-button .md-button--primary } |
    | 地編 081 | `081.rar`　30.7 MB | 舊版，界面與清單可能對不上 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/081.rar){ .md-button .md-button--primary } |
    | 地編 080 | `080.rar`　30.7 MB | 舊版，界面與清單可能對不上 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/080.rar){ .md-button .md-button--primary } |
    | 地編 070 | `070.rar`　26.2 MB | 更早的版本，僅供對照 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/070.rar){ .md-button .md-button--primary } |
    | 地編 060 | `060.zip`　32.1 MB | 歸檔裡最老的一版，注意是 zip | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/060.zip){ .md-button .md-button--primary } |

</div>

!!! warning "先看清是哪一版"
    手冊正文默認講的是最新版，如果不是會特殊標明；拿舊版地編對着看，界面與清單可能對不上。

## 模板下載 { #materials .section-title }

做地圖要用的模板，下載後放進地編的 `templates` 文件夾即可（**注意該文件夾中只有一個模板會生效，可以先將其它模板改下後綴防止讀錯**）。

模板的作用是提供比較完備的Mesh、Wall等素材庫，並且根據模板的種類（普通、沙漠、雪地）來對地圖進行不同地面渲染。

<div class="ts-plain ts-align" markdown="1">

**原版模板（以map7為基礎）**

| 版本 | 歸檔 | 備註 | 下載 |
| --- | --- | --- | --- |
| 普通模式模板（清單版本 vao0822） | `vao0822.svg`　441 kB | 默認環境 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary download="vao0822.svg" } |

**沙漠模板**

| 版本 | 歸檔 | 備註 | 下載 |
| --- | --- | --- | --- |
| 沙漠模式模板 | `vdao.svg`　431 kB | 環境材質為沙漠<br>該模板還未細化測試 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/vdao.svg){ .md-button .md-button--primary download="vdao.svg" } |

**雪地模板**

| 版本 | 歸檔 | 備註 | 下載 |
| --- | --- | --- | --- |
| 雪地模式模板 | `vwao.svg`　426 kB | 環境材質為雪地<br>該模板還未細化測試 | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/vwao.svg){ .md-button .md-button--primary download="vwao.svg" } |

</div>

## 組件下載 { #prefabs .section-title }

組件也稱預製件，格式為xxx.asmb，是一組已經組裝好的對象：下載之後放進地編讀取組件的文件夾`assaumbles`就能在地編中使用了，一般可以多個模板通用。

<div class="ts-search">
  <div class="ts-search__box">
    <span class="ts-search__icon" aria-hidden="true"></span>
    <input class="ts-search__input" type="search" autocomplete="off" spellcheck="false" placeholder="搜索組件名稱…" aria-label="搜索組件">
    <kbd class="ts-search__kbd">Ctrl K</kbd>
  </div>
  <p class="ts-search__meta">共 3 項 · 可搜組件名稱</p>
</div>

| 預覽 | 名稱 | 備註 | 下載 |
| --- | --- | --- | --- |
| <span class="ts-shot"></span><span class="ts-shot"></span> | 機庫<br>`HangarOnIsland_objects`<span class="ts-ext">.asmb</span>　5.8 kB |  | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/HangarOnIsland_objects.asmb){ .md-button .md-button--primary download="HangarOnIsland_objects.asmb" } |
| <span class="ts-shot"></span><span class="ts-shot"></span> | 儲藏室<br>`Stash_vao0822`<span class="ts-ext">.asmb</span>　4.2 kB |  | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/Stash_vao0822.asmb){ .md-button .md-button--primary download="Stash_vao0822.asmb" } |
| <span class="ts-shot"></span><span class="ts-shot"></span> | 軍械庫<br>`Armory_vao0822`<span class="ts-ext">.asmb</span>　2.7 kB |  | [下載](https://assets.rwr-infra.uk/rwrme-web-assets/Armory_vao0822.asmb){ .md-button .md-button--primary download="Armory_vao0822.asmb" } |

!!! note "預覽圖與備註還沒補"
    這三行的預覽圖與備註都還空着：位置先佔出來了（每行兩個圖框），圖與說明補齊後會換掉。

## 相關說明 { .section-title }

??? quote "校驗用哈希（sha256）"
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
    67a34f77b43b1520dde8515e83c1b6e78413a14293938a85479aa1de3aa0dc48  vdao.svg
    d6959ab114a5ef17d628449a882e019e1ad7d1dd245adad40a0db80f27a9657f  vwao.svg
    42b39c0476684493dcafb7d0a4fd4954f55f960b034591f3dcf1a614c9047d19  HangarOnIsland_objects.asmb
    c1228e7973441ee118e15f31dd0fd4babdcbe1b3d09035022cd8284c493353f5  Stash_vao0822.asmb
    ccbdcdb74b362ddbc559fd66c10d3d9aeaee1b7423907997326ae79c3404ba5c  Armory_vao0822.asmb
    ```

    歸檔是**凍結**的，哈希不會變；哪天真換了文件，這裡會跟着改——
    它與上面的表格是同一批數字，兩處對不上就是有人改漏了一處。
    哈希是從線上那份文件算出來的（不是本地另算一遍），數字取自
    `tools/r2/` 裡的 `sha256` 命令——那套歸檔工具的代碼在倉庫裡，密鑰不在。

??? quote "這些東西存在哪兒"
    立在 `assets.rwr-infra.uk` 那個域上（Cloudflare R2 的對象存儲），
    倉庫裡既沒有副本、也不走本站的部署——所以整站的產物裡沒有幾百 MB 的二進制，
    克隆這份倉庫要下的是正文，不是歸檔。
