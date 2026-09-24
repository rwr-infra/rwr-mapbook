---
nav_label: "mapSettings 說明（待試）"
title: "mapSettings 說明（待試）"
description: "地圖自身的設置項。這一頁標註「待試」，尚未逐項驗證。"
status: "partial"
tags: [配置文件, 未驗證]
# ⚠️ 由 tools/docsgen.py 從 content/settings/map-settings.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [toc]
---

# mapSettings 說明 { #map-settings }

<p class="kicker">SETTINGS · 地圖自己的那份配置</p>

!!! warning "這一頁是**待試**的"
    下面每一行的「說明」列都照原樣留着，其中好幾條直接標着「沒試」「不知道這是啥」。
    照原樣留着——**沒試過就是沒試過**，不要照着猜。

| 字段 | 示例 | 備註 | 說明 |
| --- | --- | --- | --- |
| `ambience_alert_day_sound` | `ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | 沒試，不知道這是啥 |
| `ambience_day_sound` | `ambient_daytime.wav`<br>`ambient_lightrain.wav` |  | 白天的背景音效 |
| `ambience_night_sound` | `ambient_lightrain_night.wav` |  | 晚上的背景音效 |
| `day_color` | `#e5c685ff`<br>`fill` | 任意 16 進制顏色 | 白天的顏色 |
| `description` | `16 bases`<br>`2 faction king of the hill map`<br>`assault map - 11 bases`<br>`conquest map - 10 bases`<br>`pure pvp map` | 隨便填，但最好按格式來 | 地圖描述 |
| `flip` | `-1` |  | 不知道這是啥，沒試 |
| `global_effect` | `ambience_alert_day_sound`<br>`ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | 全局效果 |
| `name` | `Route 666` | 隨便填 | 地圖名 |
| `night_color` | `#136395`<br>`#5f5fc0ff`<br>`stroke` | 任意 16 進制顏色 | 晚上的顏色 |
| `randomize_faction_index` | `0`<br>`1` |  | 沒試，不知道這是啥 |
| `show_base_names_in_map_view` | `0` |  | 不知道這是啥，沒試 |
| `starting_day_phase` | `0.1`<br>`6` |  | 戰役開始的時間 |
| `visible_in_menu` | `0`<br>`1` |  | 是否在列表可見 |

!!! tip "顏色那兩行的第三種寫法"
    `day_color` 與 `night_color` 的示例裡除了色值還有一個 `fill` / `stroke`——
    這裡沒寫這是什麼，也沒試過。照填色值即可。
