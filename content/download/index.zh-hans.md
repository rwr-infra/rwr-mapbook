---
nav_label: "文件下载"
title: "文件下载"
icon: "lucide/archive"
description: "地编各版本的完整归档、三种模板与预制件组件，放在站外的对象存储上，每一条都是直链。"
---

用来下载地编、模板与预制件。地编目前最新版本为0101；模板现有三种：普通模式模板vao0822、沙漠模式模板vdao、雪地模式模板vwao。

## 地编下载 { #download .section-title }

这里是历次地编版本的完整归档，从 060 到 0101。每个包就是那一版地编的全套文件，
与当时发在群文件里的一致。

归档**不在本站的仓库里**。单是这些归档就有 234 MB，跟着仓库走的话，每个想改文档的人
都得先下几百 MB，而这份仓库里真正会变的是正文。所以它们放在站外的对象存储上
（Cloudflare R2），下面每一条都是**直链**：浏览器能下，下载器（IDM、aria2、迅雷）
也能下，右键就能交给它们。

<div class="ts-plain" markdown="1">

**最新版本：**

| 版本 | 归档 | 下载 |
| --- | --- | --- |
| 地编 0101 | `0101.rar`　26.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/0101.rar){ .md-button .md-button--primary } |

**历史版本：**

??? note "展开查看全部历史版本（060 到 0100）"
    | 版本 | 归档 | 下载 |
    | --- | --- | --- |
    | 地编 0100 | `0100.rar`　31.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/0100.rar){ .md-button .md-button--primary } |
    | 地编 091 | `091.rar`　26.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/091.rar){ .md-button .md-button--primary } |
    | 地编 090 | `090.rar`　30.7 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/090.rar){ .md-button .md-button--primary } |
    | 地编 081 | `081.rar`　30.7 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/081.rar){ .md-button .md-button--primary } |
    | 地编 080 | `080.rar`　30.7 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/080.rar){ .md-button .md-button--primary } |
    | 地编 070 | `070.rar`　26.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/070.rar){ .md-button .md-button--primary } |
    | 地编 060 | `060.zip`　32.1 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/060.zip){ .md-button .md-button--primary } |

</div>

!!! warning "先看清是哪一版"
    归档是**冻结的**：哪一版就是当时那一版的全部文件，之后不会再改。
    手册正文讲的是最新版；拿旧版地编对着看，界面与清单可能对不上。

## 模板下载 { #materials .section-title }

做地图要用的模板，下载后放进地编的 `templates` 文件夹即可（**注意该文件夹中只有一个模板会生效，可以先将其它模板改下后缀防止读错**）。模板的作用是提供比较完备的Mesh、Wall等素材库，并且根据模板的种类（普通、沙漠、雪地）来对地图进行不同地面渲染。

三种模板**并列**在这里，挑你要的那一种下载即可。

<div class="ts-plain ts-align" markdown="1">

**原版模板（以map8为基础）**

| 材料 | 文件 | 下载 |
| --- | --- | --- |
| 普通模式模板（清单版本 vao0822） | `vao0822.svg`　441 kB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary download="vao0822.svg" } |

**沙漠模板**

| 材料 | 文件 | 下载 |
| --- | --- | --- |
| 沙漠模式模板 | `vdao.svg`　431 kB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/vdao.svg){ .md-button .md-button--primary download="vdao.svg" } |

**雪地模板**

| 材料 | 文件 | 下载 |
| --- | --- | --- |
| 雪地模式模板 | `vwao.svg`　426 kB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/vwao.svg){ .md-button .md-button--primary download="vwao.svg" } |

</div>

## 组件下载 { #prefabs .section-title }

预制件（`.asmb`）是**一组摆好的物件**：下完之后放进地编读取组件的文件夹
（`assaumbles`），就能整组拿来用，不用一个个摆。

<div class="ts-search">
  <div class="ts-search__box">
    <span class="ts-search__icon" aria-hidden="true"></span>
    <input class="ts-search__input" type="search" autocomplete="off" spellcheck="false" placeholder="搜索组件名称…" aria-label="搜索组件">
    <kbd class="ts-search__kbd">Ctrl K</kbd>
  </div>
  <p class="ts-search__meta">共 3 项 · 可搜组件名称</p>
</div>

| 预览 | 名称 | 备注 | 下载 |
| --- | --- | --- | --- |
| <span class="ts-shot"></span><span class="ts-shot"></span> | 岛上的机库<br>`HangarOnIsland_objects.asmb`　5.8 kB | 待补 | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/HangarOnIsland_objects.asmb){ .md-button .md-button--primary download="HangarOnIsland_objects.asmb" } |
| <span class="ts-shot"></span><span class="ts-shot"></span> | 藏匿点<br>`Stash_vao0822.asmb`　4.2 kB | 待补 | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/Stash_vao0822.asmb){ .md-button .md-button--primary download="Stash_vao0822.asmb" } |
| <span class="ts-shot"></span><span class="ts-shot"></span> | 军械库<br>`Armory_vao0822.asmb`　2.7 kB | 待补 | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/Armory_vao0822.asmb){ .md-button .md-button--primary download="Armory_vao0822.asmb" } |

!!! note "预览图与备注还没补"
    这三行的预览图与备注都还空着：位置先占出来了（每行两个图框），
    图与说明补齐后会换掉。文件名与哈希是准的，可以先下。

## 相关说明 { .section-title }

??? quote "校验用哈希（sha256）"
    下完想确认拿到的是原件，可以对一下：

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

    归档是**冻结**的，哈希不会变；哪天真换了文件，这里会跟着改——
    它与上面的表格是同一批数字，两处对不上就是有人改漏了一处。
    哈希是从线上那份文件算出来的（不是本地另算一遍），数字取自
    `_r2_cunchu` 里的 `sha256` 命令。

??? quote "这些东西存在哪儿"
    立在 `assets.rwr-infra.uk` 那个域上（Cloudflare R2 的对象存储），
    仓库里既没有副本、也不走本站的部署——所以整站的产物里没有几百 MB 的二进制，
    克隆这份仓库要下的是正文，不是归档。
