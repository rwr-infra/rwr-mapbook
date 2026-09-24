---
title: 前置元数据
icon: lucide/file-text
description: content/ 下每个 .md 可以写的字段，以及谁在读它。
tags: ["content", "i18n"]
---

# 前置元数据

<p class="kicker">FRONT MATTER</p>

| 字段 | 谁在读 | 说明 |
| --- | --- | --- |
| `title` | 主题、`navgen` | 页面标题。缺 `nav_label` 时也作导航显示名 |
| `description` | 主题、检索 | 一到两句，进摘要与检索结果 |
| `nav_label` | `navgen` | 在**上一级**导航里显示的名字，优先于 `title` |
| `nav` | `navgen` | 只写在 `index.md` 里：本目录子项的顺序 |
| `nav_hidden` | `navgen` | 为真时不占导航格子（如标签页） |
| `icon` | 主题 | 导航图标，取主题内置图标集，如 `lucide/compass` |
| `tags` | tags 插件 | 标签。**用语言中立的标识符**，见下 |
| `source_sha256` | `i18n_check` | 译文专用：所依据的原文指纹 |
| `translated` | `i18n_check` | 译文专用：翻译日期 |

## 标签为什么要是语言中立的

标签页是把各分区横着串起来的线索。若每种语言各写一套标签，
同一件事在不同语言里就会挂上不同的名字，横向的线索在换语言时断掉。
所以标签用日期、代号这类**与语言无关**的标识符。

## 派生语种

`zh-hant` 的产物由简体转换而来，因此它**不读**上面这些字段的翻译版——
转换是把简体整篇搬过去，字段一并转。哪些字不转、哪些要归一，
见 `tools/hant.py` 开头的说明。
