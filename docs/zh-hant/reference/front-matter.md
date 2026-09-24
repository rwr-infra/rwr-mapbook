---
title: 前置元數據
icon: lucide/file-text
description: content/ 下每個 .md 可以寫的字段，以及誰在讀它。
tags: ["content", "i18n"]
# ⚠️ 由 tools/docsgen.py 從 content/reference/front-matter.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 前置元數據

<p class="kicker">FRONT MATTER</p>

| 字段 | 誰在讀 | 說明 |
| --- | --- | --- |
| `title` | 主題、`navgen` | 頁面標題。缺 `nav_label` 時也作導航顯示名 |
| `description` | 主題、檢索 | 一到兩句，進摘要與檢索結果 |
| `nav_label` | `navgen` | 在**上一級**導航裡顯示的名字，優先於 `title` |
| `nav` | `navgen` | 只寫在 `index.md` 裡：本目錄子項的順序 |
| `nav_hidden` | `navgen` | 為真時不佔導航格子（如標簽頁） |
| `icon` | 主題 | 導航圖標，取主題內置圖標集，如 `lucide/compass` |
| `tags` | tags 插件 | 標簽。**用語言中立的標識符**，見下 |
| `source_sha256` | `i18n_check` | 譯文專用：所依據的原文指紋 |
| `translated` | `i18n_check` | 譯文專用：翻譯日期 |

## 標簽為什麼要是語言中立的

標簽頁是把各分區橫着串起來的線索。若每種語言各寫一套標簽，
同一件事在不同語言裡就會掛上不同的名字，橫向的線索在換語言時斷掉。
所以標簽用日期、代號這類**與語言無關**的標識符。

## 派生語種

`zh-hant` 的產物由簡體轉換而來，因此它**不讀**上面這些字段的翻譯版——
轉換是把簡體整篇搬過去，字段一併轉。哪些字不轉、哪些要歸一，
見 `tools/hant.py` 開頭的說明。
