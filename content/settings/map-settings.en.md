---
title: "mapSettings"
description: "The map's own settings. This page is marked \"untested\", and has not been verified item by item."
source_sha256: 25f8db77bca2783045bbffd4e8e2ac9982fe66568105148953725e831bd73b9f
translated: 2026-09-25
nav_label: "mapSettings"
status: "partial"
tags: [Config files, Unverified]
---

# mapSettings { #map-settings }

<p class="kicker">SETTINGS · the map's own copy of the config</p>

!!! warning "**Untested**"
    Every row below keeps its **Description** text exactly as written, and several of them
    say outright "not tried" and "no idea what this is".
    Kept as written — **not tried is not tried**; do not guess your way through it.

| Field | Example | Notes | Description |
| --- | --- | --- | --- |
| `ambience_alert_day_sound` | `ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | not tried, no idea what this is |
| `ambience_day_sound` | `ambient_daytime.wav`<br>`ambient_lightrain.wav` |  | daytime ambient sound |
| `ambience_night_sound` | `ambient_lightrain_night.wav` |  | nighttime ambient sound |
| `day_color` | `#e5c685ff`<br>`fill` | any hex colour | the daytime colour |
| `description` | `16 bases`<br>`2 faction king of the hill map`<br>`assault map - 11 bases`<br>`conquest map - 10 bases`<br>`pure pvp map` | anything goes, but better to keep to the format | the map description |
| `flip` | `-1` |  | no idea what this is, not tried |
| `global_effect` | `ambience_alert_day_sound`<br>`ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | global effect |
| `name` | `Route 666` | anything goes | the map name |
| `night_color` | `#136395`<br>`#5f5fc0ff`<br>`stroke` | any hex colour | the nighttime colour |
| `randomize_faction_index` | `0`<br>`1` |  | not tried, no idea what this is |
| `show_base_names_in_map_view` | `0` |  | no idea what this is, not tried |
| `starting_day_phase` | `0.1`<br>`6` |  | when the campaign starts |
| `visible_in_menu` | `0`<br>`1` |  | whether it shows up in the list |

!!! tip "The third value in the two colour rows"
    Besides the colour value, the examples for `day_color` and `night_color` also carry a
    `fill` / `stroke` — the page never says what that is, and it has not been tried.
    Just fill in the colour value.
