---
title: About this template
description: "What the template includes, what it leaves out, and the trade-offs behind it."
source_sha256: fd6cbe1786848d0f419fe11b3d1b4a0ef3070bf7774571915c250e4db2702480
translated: 2026-01-01
nav_label: "About"
icon: lucide/info
---

# About this template

<p class="kicker">ABOUT THIS TEMPLATE</p>

## What you get

* A **single hand-written layer** build pipeline: `content/` → `docs/` → `site/`;
* A three-language skeleton: the default language written by hand, translations written
  by hand and fingerprinted, derived languages converted by script;
* Four checks that exit non-zero, ready to hang off CI;
* Theme overrides: header, footer, navigation and breadcrumbs that pick their wording per
  page language, a language switcher, a consent form, and directory trailing-slash repair.

## What you do not get

* **Content.** Only a few pages describing the template itself; replace them.
* **A colour scheme or typeface.** It uses the stock Zensical theme; `docs/stylesheets/extra.css`
  only adds a little. Fonts and scripts are entirely self-hosted (no third-party requests).
* **Deployment.** `site/` is a plain static directory; hand it to whatever host you use.

## Which language is the default

`DEFAULT_LANG` in `tools/langs.py`. The default language lands at the root of `docs/`
with no URL prefix; every other language occupies a subdirectory of its own.
