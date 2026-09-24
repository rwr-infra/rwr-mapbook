---
title: Translating
description: "The fingerprint mechanism: how a translation declares which source it follows, and why it goes stale."
source_sha256: b72a4d1d5b3da9ceaed4edb35f4ea6cc8a77ab2765b2ef7bd491057b599ac248
translated: 2026-01-01
icon: lucide/languages
tags: ["i18n"]
# ⚠️ 由 tools/docsgen.py 从 content/guide/translating.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# Translating

<p class="kicker">TRANSLATING</p>

## A fingerprint, not a manifest

No one has to register a translation. It **declares the source it follows** in its own
front matter:

```yaml
---
title: Getting started
description: ...
source_sha256: 3f9c…      # digest of content/guide/getting-started.zh-hans.md at the time
translated: 2026-01-01
---
```

Change the default-language file and the digest no longer matches; that page is
immediately marked `stale`. Nobody has to remember to tell the translator.

## Skeletons for missing translations

```bash
uv run python tools/i18n_check.py --sync    # create skeletons for missing translations
```

A skeleton records the source path and the digest to fill in, and carries a `TODO`
placeholder. The check keeps reporting it until it is finished.

!!! note "Derived languages do not use this"
    `zh-hant` has no hand-written source file; it is converted from Simplified Chinese by
    `tools/hant.py`, and the test is whether the conversion matches the output byte for byte.
    See [Reference](../reference/front-matter.md).
