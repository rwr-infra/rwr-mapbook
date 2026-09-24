---
title: "About"
description: "Where this handbook comes from, and which versions it covers."
source_sha256: 4b6b9e7affd936697afcccbe0d83dfd1814e3c3c19e157876cc63c47cb496213
translated: 2026-09-25
nav_label: "About"
icon: lucide/info
# ⚠️ 由 tools/docsgen.py 从 content/about/index.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

# About

This handbook comes from *Rat Book*, the RWR map-editing group's internal document,
together with the model inventories the group maintains.

|  |  |
| --- | --- |
| Editor version | 0101 |
| Handbook edited | 20260922 |
| Current editor | HamSter |
| Inventory template version | vao0822 |

## The two originals

| Original | Form | What it became on this site |
| --- | --- | --- |
| *Rat Book* | a single HTML page with 54 embedded images | Getting ready, The editor, Configuration files |
| The inventories | an Excel workbook, 5 sheets, 705 floating images | The five pages of Model inventories |

## How the URLs are laid out

Version first, language second — so the same page has its own address in every version
and every language:

```mermaid
graph TD
  A["/ · current · Simplified"] --> B["/en/ · current · English"]
  A --> C["/zh-hant/ · current · Traditional"]
  A --> D["/archive/ · archived · Simplified"]
  D --> E["/archive/en/"]
  D --> F["/archive/zh-hant/"]
```

## What the original left unverified

Where the original says "untested", it still does, and the navigation shows an
*Incomplete* marker for it; the "it is said that…" passages are unchanged too.
**This move does not second-guess the source.**

!!! quote "How the original sounds"
    These notes were written by the group for the group, so they are blunt:
    "crashes on load", "no collision box", "whatever you do, do not file every material
    error under template meshes". All of that is kept as written — polished into formal
    prose, a reader could no longer tell how certain the author was.
