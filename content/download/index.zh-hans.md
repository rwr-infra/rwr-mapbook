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

「下载」有两种走法。没超过部署上限的整包是**一个普通文件**，按钮就是直链——浏览器
能下，下载器也能下。超过上限的会存成若干片段，那种由页面把分片取回、逐片核对哈希，
拼成一个**与原文件同名**的整包。两种情况落到下载文件夹里的都是一个整包，
不会出现 `.partNNN`，也不需要手工合并。

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

!!! note "直链，还是由页面拼"
    本站部署在 EdgeOne Pages，**单个文件最大 25 MB**，而地编的整包是 26–84 MB，
    塞不进一个文件里。所以：

    * 没超上限的（比如那份 441 kB 的模板）就是一个**普通文件**，按钮是直链：
      浏览器能下，下载器也能下（右键就能交给它）；
    * 超了上限的存成若干片段，那种**只能由页面拼**。分片是仓库里的真实地址没错，
      但那是几段，交给下载器只会拿到几段 `.partNNN`，还得自己合并。页面把全部片段
      取回、逐片核对哈希、拼成一个整包再交给你；任何一片对不上就停下报错，
      不会把半个包塞过来。
