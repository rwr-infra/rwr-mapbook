---
nav_label: "文件下载"
title: "文件下载"
icon: "lucide/archive"
description: "地编各版本的完整归档与配套模板，放在站外的对象存储上，每一条都是直链。"
# ⚠️ 由 tools/docsgen.py 从 content/download/index.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

用来下载地编与模板，地编目前最新版本为0101，模板目前有普通模式模板vao0822，雪地模式模板与沙漠模式模板正在制作中。

## 地编下载 { #download .section-title }

这里是历次地编版本的完整归档，从 060 到 0101。每个包就是那一版地编的全套文件，
与当时发在群文件里的一致。

归档**不在本站的仓库里**。单是这些归档就有 234 MB，跟着仓库走的话，每个想改文档的人
都得先下几百 MB，而这份仓库里真正会变的是正文。所以它们放在站外的对象存储上
（Cloudflare R2），下面每一条都是**直链**：浏览器能下，下载器（IDM、aria2、迅雷）
也能下，右键就能交给它们。

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

!!! warning "先看清是哪一版"
    归档是**冻结的**：哪一版就是当时那一版的全部文件，之后不会再改。
    手册正文讲的是最新版；拿旧版地编对着看，界面与清单可能对不上。

## 模板下载 { #materials .section-title }

做地图要用的模板，下载后放进地编的 `templates` 文件夹即可（**注意该文件夹中只有一个模板会生效，可以先将其它模板改下后缀防止读错**）。模板的作用是提供比较完备的Mesh、Wall等素材库，并且根据模板的种类（普通、沙漠、雪地）来对地图进行不同地面渲染。

**原版模板（以map8为基础）**

| 材料 | 文件 | 下载 |
| --- | --- | --- |
| 普通模式模板（清单版本 vao0822） | `vao0822.svg`　441 kB | [下载](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary download="vao0822.svg" } |

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
    ```

    归档是**冻结**的，哈希不会变；哪天真换了文件，这里会跟着改——
    它与上面的表格是同一批数字，两处对不上就是有人改漏了一处。

??? quote "这些东西存在哪儿"
    立在 `assets.rwr-infra.uk` 那个域上（Cloudflare R2 的对象存储），
    仓库里既没有副本、也不走本站的部署——所以整站的产物里没有几百 MB 的二进制，
    克隆这份仓库要下的是正文，不是归档。
