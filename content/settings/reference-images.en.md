---
title: "RefpM"
description: "Used for adding a reference image."
source_sha256: 79da6c8c9791aab8fa8d5305723b22d7dbaa7058aff5e59b8620f1b2024e992d
translated: 2026-09-25
nav_label: "RefpM"
icon: "lucide/image"
---

# RefpM { #reference-images }

<p class="kicker">SETTINGS · laying the base image under the editor</p>

When you build a map, lay a satellite image or a hand-drawn sketch underneath and place
objects against it. Use **Import** to bring in a reference image, **Clear** to remove it.

| Control | What it does | What to fill in |
| --- | --- | --- |
| `ScaleX` | Squeezes or stretches the reference image horizontally | A multiplier. `0.5` squeezes it to half width |
| `ScaleY` | Squeezes or stretches the reference image vertically | A multiplier |
| `OffsetX` | Shifts the reference image horizontally | A distance. The X axis grows to the right |
| `OffsetY` | Shifts the reference image vertically | A distance. The Y axis grows upwards |
| `Alpha` | Changes the reference image's transparency | Fades it towards the left, makes it solid towards the right |

!!! note "Two typos were sorted out in this table"
    As written it read "OffsetX and OffsetX are really Y's job" and "towards the right it
    turns 躯体化" — from the context these are typos, so this page writes `OffsetY` and
    "towards the right it turns solid". Say the word if you want them put back.
