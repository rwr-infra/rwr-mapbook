---
title: Writing content
description: "What each front matter field means, and why navigation needs no separate file."
source_sha256: 414f5e3f242c8157728056d2b44d43d858a2c2c2f88726df0c272fdddfaff0fb
translated: 2026-01-01
icon: lucide/pen-line
tags: ["content"]
---

# Writing content

<p class="kicker">WRITING</p>

## What a page looks like

```markdown
---
title: Writing content
description: One or two sentences; these feed the page summary and search results.
icon: lucide/pen-line
tags: ["content"]
---

# Writing content

Body text…
```

## Navigation is not maintained separately

The **only source of navigation is the content itself** (see `tools/navgen.py`):

* **Order** comes from the `nav:` list in the `index.md` of the same directory;
* **Display name** prefers `nav_label`, then `title`, then the first level-1 heading;
* The order of top-level directories comes from the `nav:` in `docs/index.md`.

In other words, **all navigation metadata for a folder lives in its own `index.md`**.
`navgen.py` then writes one `.nav.yml` per directory — that file is generated; do not edit it.

A page that should not take a navigation slot (the tag page, say) sets `nav_hidden: true`.

## How to write links

* To **another page**: a relative path, e.g. `[Getting started](getting-started.md)`.
  The per-language trees are mirrors, so this works unchanged in all three languages.
* To **shared assets**: `docs/assets/` exists once and is shared by every tree. Write a
  relative path; `docsgen.py` prepends the extra `../` for non-default languages.
