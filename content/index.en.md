---
title: "RWR Map Editor's Handbook"
description: "The handbook for the Running With Rifles map editor: what every panel does, the model and wall inventories, key bindings and common workflows."
source_sha256: 0bd45c03a508ac47daf7f82d9a83c5abae1f50f065d5d22c10b4f0f64d4962aa
translated: 2026-09-25
nav_label: "Home"
icon: lucide/house
nav: ["prepare", "editor", "tables", "settings", "about"]
---

# RWR Map Editor's Handbook

<p class="kicker">RWR · READ THIS BEFORE YOU START MAPPING</p>

What to do before you start making a map — mostly to make the editor less painful to use.

|  |  |
| --- | --- |
| Edited | 20260922 |
| Editor version | 0101 |
| Current editor | HamSter |

!!! warning "First, what this is"
    These are **notes by mappers, for mappers** — not an official manual.
    Where a line says "untested" or "not tried, no idea what this is", it still says that:
    it means **nobody has tried it yet**, which is not the same as "it works"
    or "it does not".

## Where to start

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __Just got the editor__

    ---

    Unpack it, configure it, sync it with your RWR folder, and switch on the built-in
    camera mod.

    [:octicons-arrow-right-24: Getting ready](prepare/index.md)

-   :material-cursor-default-click:{ .lg .middle } __What the buttons do__

    ---

    Every tool on the main panel, the key bindings, and finding an object by ID.

    [:octicons-arrow-right-24: The editor](editor/index.md)

-   :material-cube-outline:{ .lg .middle } __Which models you can place__

    ---

    Five inventories, seven hundred objects, with previews and notes from testing.

    [:octicons-arrow-right-24: Model inventories](tables/index.md)

-   :material-cog-outline:{ .lg .middle } __Three configuration files__

    ---

    mapSettings for the map itself; 3rdParSettings and RefpM for outside resources.

    [:octicons-arrow-right-24: Configuration files](settings/index.md)

</div>

## This site has two axes

**Version** decides which set of pages you are reading; **language** decides which
script you read it in. The two do not touch: switching version keeps your language,
and switching language keeps your version.

| Axis | Which side of the header | What changes |
| --- | --- | --- |
| Version | the tag icon on the left | only the version; language stays |
| Language | the translate icon on the right | only the language; version stays |

The version menu holds two entries right now: **地编版本 0101** (this handbook) and
**彩蛋** — not an old release but a trial run of the freeze mechanism, with a 060 build's
numbers inside it.

[Start with getting ready](prepare/index.md){ .md-button .md-button--primary }
[Go straight to the inventories](tables/index.md){ .md-button }

*[template]: the name an object is referred to by in `template = …`; that is how you look it up
