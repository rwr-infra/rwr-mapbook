---
title: "Previous versions"
description: "Complete archives of every editor version, plus the two companion files: one click fetches the parts, checks them, and joins them into a single package."
source_sha256: f86420beaecbcece92dc693c646fb6f8744c52a47cda5aeaa06cc43f0ac2649d
translated: 2026-09-25
nav_label: "Previous versions"
icon: lucide/archive
tags: [Setup]
---

# Previous version archives { #download }

<p class="kicker">DOWNLOAD · the full package of every editor version</p>

Complete archives of every editor version, from 060 to 0101. Each one holds the whole
set of files for that version, exactly as it was posted in the group files.

"Download" is usually a plain **direct link**: the package sits in the repository as an
ordinary file, so a browser can fetch it and so can a download manager. Only a package over
the host's single-file limit is split; that one the page fetches piece by piece, checks
every hash, and joins into a package **under the original file name**. Either way what lands
in your download folder is one whole package — never `.partNNN` files, and never anything
you have to join by hand.

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

!!! note "A direct link, or the page joins it"
    **A package under the limit is just an ordinary file**, and that button is a direct
    link: a browser can fetch it, and so can a download manager (right-click hands it over),
    giving you the whole package at once. Only a package over the limit is stored as several
    parts, and that one **only the page can join**: the parts are real URLs, but they are
    several pieces, so a download manager would hand you several `.partNNN` files to merge
    yourself. The page fetches every part, checks each hash, and joins them into one package;
    if any part fails its check it stops and reports the error rather than giving you half a
    package.
