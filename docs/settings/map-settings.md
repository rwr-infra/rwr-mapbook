---
nav_label: "mapSettings 说明（待试）"
title: "mapSettings 说明（待试）"
description: "地图自身的设置项。原文标注「待试」，尚未逐项验证。"
status: "partial"
# ⚠️ 由 tools/docsgen.py 从 content/settings/map-settings.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# mapSettings 说明（待试） { #map-settings }

<p class="kicker">SETTINGS · 地图自己的那份配置</p>

!!! warning "这一页是**待试**的"
    下面每一行的「说明」列都是原文写的，其中好几条直接标着「没试」「不知道这是啥」。
    照原样留着——**没试过就是没试过**，不要照着猜。

| 字段 | 示例 | 备注 | 说明 |
| --- | --- | --- | --- |
| `ambience_alert_day_sound` | `ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | 没试，不知道这是啥 |
| `ambience_day_sound` | `ambient_daytime.wav`<br>`ambient_lightrain.wav` |  | 白天的背景音效 |
| `ambience_night_sound` | `ambient_lightrain_night.wav` |  | 晚上的背景音效 |
| `day_color` | `#e5c685ff`<br>`fill` | 任意 16 进制颜色 | 白天的颜色 |
| `description` | `16 bases`<br>`2 faction king of the hill map`<br>`assault map - 11 bases`<br>`conquest map - 10 bases`<br>`pure pvp map` | 随便填，但最好按格式来 | 地图描述 |
| `flip` | `-1` |  | 不知道这是啥，没试 |
| `global_effect` | `ambience_alert_day_sound`<br>`ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | 全局效果 |
| `name` | `Route 666` | 随便填 | 地图名 |
| `night_color` | `#136395`<br>`#5f5fc0ff`<br>`stroke` | 任意 16 进制颜色 | 晚上的颜色 |
| `randomize_faction_index` | `0`<br>`1` |  | 没试，不知道这是啥 |
| `show_base_names_in_map_view` | `0` |  | 不知道这是啥，没试 |
| `starting_day_phase` | `0.1`<br>`6` |  | 战役开始的时间 |
| `visible_in_menu` | `0`<br>`1` |  | 是否在列表可见 |

!!! tip "颜色那两行的第三种写法"
    `day_color` 与 `night_color` 的示例里除了色值还有一个 `fill` / `stroke`——
    原文没写这是什么，也没试过。照填色值即可。
