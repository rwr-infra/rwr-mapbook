---
title: A Trilingual Docs Template
description: "A ready-to-use Zensical template for a three-language docs site: content/ is the only hand-written layer, everything else is generated."
source_sha256: c3decac83ab752cefd104194d223397101cf00fcc963f53f4787d88062e2e1e0
translated: 2026-01-01
nav_label: "Home"
icon: lucide/house
nav: ["guide", "reference", "about"]
---

# A Trilingual Docs Template

<p class="kicker">ZENSICAL · ZH-HANS / EN / ZH-HANT · STARTER</p>

This template turns “one body of content, three languages” into a maintainable
pipeline: **`content/` is the only hand-written layer**, and every `.md` under
`docs/` is produced by a script. Editing content never means touching build output.

!!! info "The one problem it solves"
    The usual failure of a multilingual docs site is that **translations quietly go
    stale**: the default language changes, the translation does not, and the build
    stays green. Here, “is the translation stale?” becomes a check that exits non-zero.

## Three languages, two sources

<div class="grid cards" markdown>

-   __Default language: hand-written__

    ---

    `content/**/*.zh-hans.md` — the only thing a human has to write.

    [:octicons-arrow-right-24: Start with the guide](guide/index.md)

-   __Translations: hand-written, with a fingerprint__

    ---

    `content/**/*.en.md`, recording in its front matter the digest of the source it follows.

    [:octicons-arrow-right-24: How translating works](guide/translating.md)

-   __Derived language: converted by script__

    ---

    `zh-hant` is not a translation; it is converted from Simplified Chinese automatically.

    [:octicons-arrow-right-24: Fields and commands](reference/index.md)

</div>

## Get it running

```bash
uv sync --locked     # install dependencies (zensical and zhconv)
make gen             # generate docs/ and the navigation from content/
make serve           # preview at http://127.0.0.1:8000
```

The build output lands in `site/` — a plain static directory you can hand to any host.
