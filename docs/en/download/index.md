---
title: "File downloads"
description: "Complete archives of every editor version plus the companion template, hosted outside the repository as direct links."
source_sha256: 975e131ab3707ed7f1d90b00c5fb04eb19ab3f27678781f8585d31099eb9e51f
translated: 2026-09-27
nav_label: "File downloads"
icon: lucide/archive
# ⚠️ 由 tools/docsgen.py 从 content/download/index.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

<!--
  译文同步提醒（2026-09-27）：简中页新加的开头一段、以及「模板下载」一节新写的两段正文，
  都是这次跟着简中原文新译的，麻烦过一眼英文措辞。
  之后再改正文，把上面 translated 的日期顺手改掉即可；source_sha256 不用动。
-->

This page is for downloading the editor and the templates. The editor's latest version is
0101; of the templates, the normal-mode template vao0822 is ready, while the desert-mode and
winter-mode templates are still being made.

## Editor downloads { #download .section-title }

Complete archives of every editor version, from 060 to 0101. Each one holds the whole
set of files for that version, exactly as it was posted in the group files.

The archives are **not in this site's repository**. These eight alone are 234 MB, and carrying
them there would mean everyone who wants to edit the text downloads several hundred megabytes
first — while what actually changes in that repository is the text. They live in object
storage elsewhere (Cloudflare R2), and every entry below is **a direct link**: a browser can
fetch it, and so can a download manager (IDM, aria2, Thunder) — right-click hands it over.

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

**Original template (based on map8)**

| Item | File | Download |
| --- | --- | --- |
| Normal-mode template (inventory version vao0822) | `vao0822.svg`　441 kB | [Download](https://assets.rwr-infra.uk/rwrme-web-assets/vao0822.svg){ .md-button .md-button--primary download="vao0822.svg" } |

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
    ```

    The archives are **frozen**, so these do not change; if a file is ever replaced, this
    block changes with it. These are the same numbers as the tables above — if the two ever
    disagree, one of them was missed.

??? quote "Where these files live"
    On the `assets.rwr-infra.uk` domain (Cloudflare R2 object storage). The repository keeps
    no copy and the site's deployment does not carry them — so the built site has no
    hundreds-of-megabytes of binaries in it, and cloning this repository downloads text,
    not archives.
