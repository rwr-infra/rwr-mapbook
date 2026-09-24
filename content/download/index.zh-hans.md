---
nav_label: "历史版本"
title: "历史版本"
icon: "lucide/archive"
description: "历次地编版本的完整归档与两份配套材料：点一次下载，分包自动取回、校验并拼成一个整包。"
tags: [安装与配置]
---

# 历史版本归档 { #download }

<p class="kicker">DOWNLOAD · 每一版地编的整包</p>

这里是历次地编版本的完整归档，从 060 到 0101。每个包就是那一版地编的全套文件，
与当时发在群文件里的一致。

点一次「下载」即可：分包由页面自己取回、逐个核对哈希，最后拼成一个**与原文件同名**
的整包存进下载文件夹。不需要手工合并，也不需要另装合并工具。

| 版本 | 归档 | 下载 |
| --- | --- | --- |
| 地编 060 | `060.zip`<br><span data-dl-size="060">—</span> | <button type="button" class="md-button md-button--primary" data-dl="060">下载</button> <span class="dl-status" data-dl-status="060"></span> |
| 地编 070 | `070.rar`<br><span data-dl-size="070">—</span> | <button type="button" class="md-button md-button--primary" data-dl="070">下载</button> <span class="dl-status" data-dl-status="070"></span> |
| 地编 080 | `080.rar`<br><span data-dl-size="080">—</span> | <button type="button" class="md-button md-button--primary" data-dl="080">下载</button> <span class="dl-status" data-dl-status="080"></span> |
| 地编 081 | `081.rar`<br><span data-dl-size="081">—</span> | <button type="button" class="md-button md-button--primary" data-dl="081">下载</button> <span class="dl-status" data-dl-status="081"></span> |
| 地编 090 | `090.rar`<br><span data-dl-size="090">—</span> | <button type="button" class="md-button md-button--primary" data-dl="090">下载</button> <span class="dl-status" data-dl-status="090"></span> |
| 地编 091 | `091.rar`<br><span data-dl-size="091">—</span> | <button type="button" class="md-button md-button--primary" data-dl="091">下载</button> <span class="dl-status" data-dl-status="091"></span> |
| 地编 0100 | `0100.rar`<br><span data-dl-size="0100">—</span> | <button type="button" class="md-button md-button--primary" data-dl="0100">下载</button> <span class="dl-status" data-dl-status="0100"></span> |
| 地编 0101 | `0101.rar`<br><span data-dl-size="0101">—</span> | <button type="button" class="md-button md-button--primary" data-dl="0101">下载</button> <span class="dl-status" data-dl-status="0101"></span> |

!!! warning "先看清是哪一版"
    归档是**冻结的**：哪一版就是当时那一版的全部文件，之后不会再改。
    手册正文讲的是当前版；拿旧版地编对着看，界面与清单可能对不上。

## 两份配套材料 { #materials }

建模与配置要用到的另外两样东西。用法见[准备工作](../prepare/index.md)：
模板放进地编的 `templates` 文件夹，OgreSDK 则是 `3rdParSettings` 要用到时才装。

| 材料 | 文件 | 下载 |
| --- | --- | --- |
| 模板（清单版本 vao0822） | `vao0822.svg`<br><span data-dl-size="vao0822">—</span> | <button type="button" class="md-button md-button--primary" data-dl="vao0822">下载</button> <span class="dl-status" data-dl-status="vao0822"></span> |
| OgreSDK | `OgreSDK_vc10_v1-7-4.zip`<br><span data-dl-size="OgreSDK_vc10_v1-7-4">—</span> | <button type="button" class="md-button md-button--primary" data-dl="OgreSDK_vc10_v1-7-4">下载</button> <span class="dl-status" data-dl-status="OgreSDK_vc10_v1-7-4"></span> |

!!! note "为什么要分包"
    托管方对单个文件有大小上限，比它大的归档在仓库里存成若干片段。
    这件事**只发生在服务器那一侧**：页面把全部片段取回、逐片核对哈希、
    拼成一个整包再交给你。任何一片对不上就停下报错，不会把半个包塞过来。
