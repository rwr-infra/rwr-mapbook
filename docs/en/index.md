---
title: "Rat Book"
description: "The handbook for the Running With Rifles map editor: what every panel does, the model and wall inventories, key bindings and common workflows."
source_sha256: 4bf67b4d22d8c524f2f904e2b76ed8e1863e74fb7afc6a25ff8a1a123e73509e
translated: 2026-09-25
nav_label: "Home"
icon: lucide/house
nav: ["prepare", "editor", "tables", "settings", "about"]
# ⚠️ 由 tools/docsgen.py 从 content/index.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

# Rat Book

<p class="kicker">RWR MAP EDITING GROUP · INTERNAL NOTES</p>

What to do before you start making a map — mostly to make the editor less painful to use.

|  |  |
| --- | --- |
| Edited | 20260922 |
| Editor version | 0101 |
| Current editor | HamSter |

!!! warning "First, what this is"
    These are the editing group's **internal working notes**, not an official manual.
    Where the original says "untested" or "not recorded", it still says that — it means
    **the group has not tried it**, which is not the same as "it works" or "it does not".

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

    Five inventories, seven hundred objects, with previews and the group's own notes.

    [:octicons-arrow-right-24: Model inventories](tables/index.md)

-   :material-cog-outline:{ .lg .middle } __Three configuration files__

    ---

    mapSettings for the map itself; 3rdParSettings and RefpM for outside resources.

    [:octicons-arrow-right-24: Configuration files](settings/index.md)

</div>

## This site has two axes

**Version** decides which release of the editor you are reading about; **language**
decides which script you read it in. The two do not touch: switching version keeps your
language, and switching language keeps your version.

| Axis | Which side of the header | What changes |
| --- | --- | --- |
| Version | the tag icon on the left | only the version; language stays |
| Language | the translate icon on the right | only the language; version stays |

[Start with getting ready](prepare/index.md){ .md-button .md-button--primary }
[Go straight to the inventories](tables/index.md){ .md-button }

*[template]: the name an object is referred to by in `template = …`; that is how you look it up
