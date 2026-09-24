---
title: Commands and checks
description: "The make targets, and what each of the three post-build checks guards."
source_sha256: 8a134b720fd2bfec425de04620e64fec83ace2988d8891a88b710147a8af87d4
translated: 2026-01-01
icon: lucide/terminal
tags: ["build"]
# ⚠️ 由 tools/docsgen.py 从 content/reference/commands.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# Commands and checks

<p class="kicker">COMMANDS & CHECKS</p>

```bash
make gen      # content/ → docs/, and regenerate the navigation
make check    # translation coverage check only
make links    # built-output link check only (build first)
make build    # gen → build → tag filter → link check → i18n check
make serve    # local preview
make sync     # create skeletons for missing translations, then regenerate
make clean    # remove site/
```

## What each check guards

| Script | Guards | Why source validation cannot see it |
| --- | --- | --- |
| `tools/linkcheck.py` | internal references, directory trailing slashes, redirect stub targets | these links only take their final shape after the build |
| `tools/tagfilter.py` | the tag page lists only pages of its own language | the tags plugin scans all of `docs/` and has no notion of language |
| `tools/i18n_check.py` | missing, stale, or structurally mismatched translations | it needs to look at content and output at the same time |

`i18n_check.py` also asserts that certain things really are present in the built output
(SMOKE). When a template condition is permanently false, output **silently** loses a
block — no error, no warning.
