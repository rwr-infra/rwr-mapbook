---
title: Front matter
description: "Every field a .md under content/ may set, and who reads it."
source_sha256: b5f7f28cbe05b8baf4890408f711b7fcc0f48b85c2b916b16b624b52f27030a9
translated: 2026-01-01
icon: lucide/file-text
tags: ["content", "i18n"]
---

# Front matter

<p class="kicker">FRONT MATTER</p>

| Field | Read by | Meaning |
| --- | --- | --- |
| `title` | theme, `navgen` | Page title; also the navigation label when `nav_label` is absent |
| `description` | theme, search | One or two sentences for summaries and search results |
| `nav_label` | `navgen` | Name shown in the **parent** navigation; wins over `title` |
| `nav` | `navgen` | Only in `index.md`: the order of this directory's children |
| `nav_hidden` | `navgen` | When true, the page takes no navigation slot (e.g. the tag page) |
| `icon` | theme | Navigation icon from the bundled icon sets, e.g. `lucide/compass` |
| `tags` | tags plugin | Tags. **Use language-neutral identifiers**, see below |
| `source_sha256` | `i18n_check` | Translations only: digest of the source this page follows |
| `translated` | `i18n_check` | Translations only: the date it was translated |

## Why tags must be language-neutral

The tag page is the thread that runs across sections. If each language invented its own
tag names, the same subject would carry different names per language and the thread would
break the moment a reader switches language. So tags use identifiers that are independent
of language — dates, codenames and the like.

## Derived languages

The `zh-hant` output is converted from Simplified Chinese, so it does **not** read
translated versions of the fields above — the whole file is carried over and converted,
fields included. Which characters are left alone, and which are normalised, is described
at the top of `tools/hant.py`.
