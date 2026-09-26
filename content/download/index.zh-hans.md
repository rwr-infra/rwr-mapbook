---
nav_label: "历史版本"
title: "历史版本"
icon: "lucide/archive"
description: "历次地编版本的完整归档与两份配套材料，放在站外的对象存储上，每一条都是直链。"
tags: [安装与配置]
---

# 历史版本归档 { #download }

<p class="kicker">DOWNLOAD · 每一版地编的整包</p>

这里是历次地编版本的完整归档，从 060 到 0101。每个包就是那一版地编的全套文件，
与当时发在群文件里的一致。

归档**不在本站的仓库里**。单是这十份就有 318 MB，跟着仓库走的话，每个想改文档的人
都得先下几百 MB，而这份仓库里真正会变的是正文。所以它们放在站外的对象存储上
（Cloudflare R2），下面每一条都是**直链**：浏览器能下，下载器（IDM、aria2、迅雷）
也能下，右键就能交给它们。

| 版本 | 归档 | 下载 |
| --- | --- | --- |
| 地编 060 | `060.zip`　32.1 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/060.zip){ .md-button .md-button--primary } |
| 地编 070 | `070.rar`　26.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/070.rar){ .md-button .md-button--primary } |
| 地编 080 | `080.rar`　30.7 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/080.rar){ .md-button .md-button--primary } |
| 地编 081 | `081.rar`　30.7 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/081.rar){ .md-button .md-button--primary } |
| 地编 090 | `090.rar`　30.7 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/090.rar){ .md-button .md-button--primary } |
| 地编 091 | `091.rar`　26.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/091.rar){ .md-button .md-button--primary } |
| 地编 0100 | `0100.rar`　31.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/0100.rar){ .md-button .md-button--primary } |
| 地编 0101 | `0101.rar`　26.2 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/0101.rar){ .md-button .md-button--primary } |

!!! warning "先看清是哪一版"
    归档是**冻结的**：哪一版就是当时那一版的全部文件，之后不会再改。
    手册正文讲的是当前版；拿旧版地编对着看，界面与清单可能对不上。

## 两份配套材料 { #materials }

建模与配置要用到的另外两样东西。用法见[准备工作](../prepare/index.md)：
模板放进地编的 `templates` 文件夹，OgreSDK 则是 `3rdParSettings` 要用到时才装。

| 材料 | 文件 | 下载 |
| --- | --- | --- |
| 模板（清单版本 vao0822） | `vao0822.svg`　441 kB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary download="vao0822.svg" } |
| OgreSDK | `OgreSDK_vc10_v1-7-4.zip`　83.9 MB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/OgreSDK_vc10_v1-7-4.zip){ .md-button .md-button--primary } |

??? note "校验用哈希（sha256）"
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
    2208167d1e2214f196888b3e04b0c4924eb15e37a8de12318a83e2533d2a6a4b  OgreSDK_vc10_v1-7-4.zip
    ```

    归档是**冻结**的，哈希不会变；哪天真换了文件，这里会跟着改——
    它与上面那张表是同一批数字，两处对不上就是有人改漏了一处。

??? note "这些东西存在哪儿"
    立在 `assets.rwr-infra.uk` 那个域上（Cloudflare R2 的对象存储），
    仓库里既没有副本、也不走本站的部署——所以整站的产物里没有几百 MB 的二进制，
    克隆这份仓库要下的是正文，不是归档。

