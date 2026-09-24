---
title: "Previous versions"
description: "Complete archives of every editor version, plus the two companion files: one click fetches the parts, checks them, and joins them into a single package."
source_sha256: 3513a772d32e258d86122fcc4e0f3ccdc9b99c0b774dcd957b25b76a965c4b39
translated: 2026-09-25
nav_label: "Previous versions"
icon: lucide/archive
tags: [Setup]
# ⚠️ 由 tools/docsgen.py 从 content/download/index.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

# Previous version archives { #download }

<p class="kicker">DOWNLOAD · the full package of every editor version</p>

Complete archives of every editor version, from 060 to 0101. Each one holds the whole
set of files for that version, exactly as it was posted in the group files.

One click is all it takes: the page fetches the parts, checks every hash, and joins them
into a single package **under the original file name**. No manual joining, and no extra
tool to merge them.

| Version | Archive | Download |
| --- | --- | --- |
| Editor 060 | `060.zip`<br><span data-dl-size="060">—</span> | <button type="button" class="md-button md-button--primary" data-dl="060">Download</button> <span class="dl-status" data-dl-status="060"></span> |
| Editor 070 | `070.rar`<br><span data-dl-size="070">—</span> | <button type="button" class="md-button md-button--primary" data-dl="070">Download</button> <span class="dl-status" data-dl-status="070"></span> |
| Editor 080 | `080.rar`<br><span data-dl-size="080">—</span> | <button type="button" class="md-button md-button--primary" data-dl="080">Download</button> <span class="dl-status" data-dl-status="080"></span> |
| Editor 081 | `081.rar`<br><span data-dl-size="081">—</span> | <button type="button" class="md-button md-button--primary" data-dl="081">Download</button> <span class="dl-status" data-dl-status="081"></span> |
| Editor 090 | `090.rar`<br><span data-dl-size="090">—</span> | <button type="button" class="md-button md-button--primary" data-dl="090">Download</button> <span class="dl-status" data-dl-status="090"></span> |
| Editor 091 | `091.rar`<br><span data-dl-size="091">—</span> | <button type="button" class="md-button md-button--primary" data-dl="091">Download</button> <span class="dl-status" data-dl-status="091"></span> |
| Editor 0100 | `0100.rar`<br><span data-dl-size="0100">—</span> | <button type="button" class="md-button md-button--primary" data-dl="0100">Download</button> <span class="dl-status" data-dl-status="0100"></span> |
| Editor 0101 | `0101.rar`<br><span data-dl-size="0101">—</span> | <button type="button" class="md-button md-button--primary" data-dl="0101">Download</button> <span class="dl-status" data-dl-status="0101"></span> |

!!! warning "Check which version you are looking at"
    The archives are **frozen**: each one is that version's complete file set, and it will
    not change afterwards. The handbook itself describes the current version; against an
    older editor the interface and the inventories may not line up.

## The two companion files { #materials }

The other two things modelling and configuration call for. [Getting ready](../prepare/index.md)
covers how they are used: the template goes into the editor's `templates` folder, and the
OgreSDK is only needed once `3rdParSettings` comes into play.

| Item | File | Download |
| --- | --- | --- |
| Template (inventory version vao0822) | `vao0822.svg`<br><span data-dl-size="vao0822">—</span> | <button type="button" class="md-button md-button--primary" data-dl="vao0822">Download</button> <span class="dl-status" data-dl-status="vao0822"></span> |
| OgreSDK | `OgreSDK_vc10_v1-7-4.zip`<br><span data-dl-size="OgreSDK_vc10_v1-7-4">—</span> | <button type="button" class="md-button md-button--primary" data-dl="OgreSDK_vc10_v1-7-4">Download</button> <span class="dl-status" data-dl-status="OgreSDK_vc10_v1-7-4"></span> |

!!! note "Why the packages are split"
    The host caps how large a single file may be, so archives bigger than that cap are
    stored as several parts. That happens **on the server side only**: the page fetches
    every part, checks each hash, and hands you one joined package. If any part fails its
    check it stops and reports the error rather than giving you half a package.
