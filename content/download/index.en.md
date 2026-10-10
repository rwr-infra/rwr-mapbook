---
title: "File downloads"
description: "Complete archives of every editor version, the three templates and the prefabs, hosted outside the repository as direct links."
source_sha256: f33988a54cd7da3a7a3d8e2622990afa768936cac33abc9097d602f91a24105e
translated: 2026-10-10
nav_label: "File downloads"
icon: lucide/archive
---

<!--
  译文同步提醒（2026-10-10）：这次简中页改了三处——
    1. 模板下载由一种拆成三种（普通 / 沙漠 / 雪地），三种并列；
    2. 新加「组件下载」一节（三个 .asmb 预制件，带页内搜索）；
    3. 校验用哈希多了五条（vdao.svg、vwao.svg 与三个 .asmb）。
  组件那三行的**预览图与备注简中原文也还空着**，这里同样留了位置；
  等原文补上再跟一次即可。source_sha256 由 _refingerprint.js 重算，不用手改。
-->

This page is for downloading the editor, the templates and the prefabs. The editor's latest
version is 0101; there are three templates now: the normal-mode template vao0822, the
desert-mode template vdao and the winter-mode template vwao.

## Editor downloads { #download .section-title }

Complete archives of every editor version, from 060 to 0101. Each one holds the whole
set of files for that version, exactly as it was posted in the group files.

The archives are **not in this site's repository**. These eight alone are 234 MB, and carrying
them there would mean everyone who wants to edit the text downloads several hundred megabytes
first — while what actually changes in that repository is the text. They live in object
storage elsewhere (Cloudflare R2), and every entry below is **a direct link**: a browser can
fetch it, and so can a download manager (IDM, aria2, Thunder) — right-click hands it over.

<div class="ts-plain" markdown="1">

**Latest version:**

| Version | Archive | Download |
| --- | --- | --- |
| Editor 0101 | `0101.rar`　26.2 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/0101.rar){ .md-button .md-button--primary } |

**Previous versions:**

??? note "Expand for every earlier version (060 to 0100)"
    | Version | Archive | Download |
    | --- | --- | --- |
    | Editor 0100 | `0100.rar`　31.2 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/0100.rar){ .md-button .md-button--primary } |
    | Editor 091 | `091.rar`　26.2 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/091.rar){ .md-button .md-button--primary } |
    | Editor 090 | `090.rar`　30.7 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/090.rar){ .md-button .md-button--primary } |
    | Editor 081 | `081.rar`　30.7 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/081.rar){ .md-button .md-button--primary } |
    | Editor 080 | `080.rar`　30.7 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/080.rar){ .md-button .md-button--primary } |
    | Editor 070 | `070.rar`　26.2 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/070.rar){ .md-button .md-button--primary } |
    | Editor 060 | `060.zip`　32.1 MB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/060.zip){ .md-button .md-button--primary } |

</div>

!!! warning "Check which version you are looking at"
    The archives are **frozen**: each one is that version's complete file set, and it will
    not change afterwards. The handbook itself describes the latest version; against an
    older editor the interface and the inventories may not line up.

## Template downloads { #materials .section-title }

The template you need in order to make maps. Download it and drop it into the editor's
`templates` folder (**only one template in that folder takes effect, so rename the extension
of the others first to keep the editor from reading the wrong one**). A template supplies a
fairly complete library of Mesh, Wall and other assets, and its kind (normal, desert, winter)
decides how the ground is rendered on the map.

The three templates are listed **side by side** — take the one you want.

<div class="ts-plain ts-align" markdown="1">

**Original template (based on map8)**

| Item | File | Download |
| --- | --- | --- |
| Normal-mode template (inventory version vao0822) | `vao0822.svg`　441 kB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary download="vao0822.svg" } |

**Desert template**

| Item | File | Download |
| --- | --- | --- |
| Desert-mode template | `vdao.svg`　431 kB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/vdao.svg){ .md-button .md-button--primary download="vdao.svg" } |

**Winter template**

| Item | File | Download |
| --- | --- | --- |
| Winter-mode template | `vwao.svg`　426 kB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/vwao.svg){ .md-button .md-button--primary download="vwao.svg" } |

</div>

## Prefab downloads { #prefabs .section-title }

A prefab (`.asmb`) is **a group of objects already laid out**: drop it into the folder the
editor reads prefabs from (`assaumbles`) and you can use the whole group at once instead of
placing objects one by one.

<div class="ts-search">
  <div class="ts-search__box">
    <span class="ts-search__icon" aria-hidden="true"></span>
    <input class="ts-search__input" type="search" autocomplete="off" spellcheck="false" placeholder="Search prefab names…" aria-label="Search prefabs">
    <kbd class="ts-search__kbd">Ctrl K</kbd>
  </div>
  <p class="ts-search__meta">3 items · searchable by name</p>
</div>

| Preview | Name | Notes | Download |
| --- | --- | --- | --- |
| <span class="ts-shot"></span><span class="ts-shot"></span> | Hangar on the island<br>`HangarOnIsland_objects.asmb`　5.8 kB | To be filled in | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/HangarOnIsland_objects.asmb){ .md-button .md-button--primary download="HangarOnIsland_objects.asmb" } |
| <span class="ts-shot"></span><span class="ts-shot"></span> | Stash<br>`Stash_vao0822.asmb`　4.2 kB | To be filled in | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/Stash_vao0822.asmb){ .md-button .md-button--primary download="Stash_vao0822.asmb" } |
| <span class="ts-shot"></span><span class="ts-shot"></span> | Armory<br>`Armory_vao0822.asmb`　2.7 kB | To be filled in | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/Armory_vao0822.asmb){ .md-button .md-button--primary download="Armory_vao0822.asmb" } |

!!! note "Previews and notes are still empty"
    The preview images and the notes for these three rows are not in yet: the slots are
    already there (two frames per row) and will be replaced once the images arrive.
    The file names and the checksums are final, so the downloads work as they are.

## Related notes { .section-title }

??? quote "Checksums (sha256)"
    To confirm you got the original file:

    ```
    35c9560e78566d0e7c8139e9f8b43f15a7932cf1a20139eea2930710f0c4bddb  060.zip
    eff018db8027e2327a36a45ac0fb2167fb30d593afe987d8cf889b3ae16ecb70  070.rar
    a2b47f4896ea760da64b8ee99a01152a37734e213bf27cee10896a968a1cb3ed  080.rar
    303e30c4d0796aa4bc3a6f85729d5ed9d97efd7d7b434021673406c63651af96  081.rar
    e2b670c0db6156e2414801fdd5167a9a2eff75c62d6f773aa37f45e164eb0446  090.rar
    2479c531f4576e8c5751e15637c422f6ff2ce3654e8c4c4aa3fd5263c1b6eade  091.rar
    84d18efd2fe7de947efe9f44374662961f2a4d5f7e09cb65e4165aafcddd742a  0100.rar
    49de6d2c0175f6a6a01f0f6eaaab93c4f0af394d82151576ad9b36c33c849a55  0101.rar
    e4ec1869d92fc802d8760e8898eba9953b55a2face1c39e74dffee850f1bfc31  vao0822.svg
    67a34f77b43b1520dde8515e83c1b6e78413a14293938a85479aa1de3aa0dc48  vdao.svg
    d6959ab114a5ef17d628449a882e019e1ad7d1dd245adad40a0db80f27a9657f  vwao.svg
    42b39c0476684493dcafb7d0a4fd4954f55f960b034591f3dcf1a614c9047d19  HangarOnIsland_objects.asmb
    c1228e7973441ee118e15f31dd0fd4babdcbe1b3d09035022cd8284c493353f5  Stash_vao0822.asmb
    ccbdcdb74b362ddbc559fd66c10d3d9aeaee1b7423907997326ae79c3404ba5c  Armory_vao0822.asmb
    ```

    The archives are **frozen**, so these do not change; if a file is ever replaced, this
    block changes with it. These are the same numbers as the tables above — if the two ever
    disagree, one of them was missed. The numbers are taken from the file as it sits on the
    storage (not recomputed locally), with the `sha256` command in `_r2_cunchu`.

??? quote "Where these files live"
    On the `assets.rwr-infra.uk` domain (Cloudflare R2 object storage). The repository keeps
    no copy and the site's deployment does not carry them — so the built site has no
    hundreds-of-megabytes of binaries in it, and cloning this repository downloads text,
    not archives.
