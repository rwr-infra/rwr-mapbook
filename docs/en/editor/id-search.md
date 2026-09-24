---
title: "ID search"
description: "Locating an object by ID when an error is thrown."
source_sha256: bf8f25bb1b7ac8e6dc9ca61cd8c6d22f4959ae876e0f39abf9c1ce18fd7507b8
translated: 2026-09-25
nav_label: "ID search"
icon: lucide/search
tags: [Troubleshooting, Tools]
# ⚠️ 由 tools/docsgen.py 从 content/editor/id-search.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# ID search { #id-search }

<p class="kicker">EDITOR · what that number in the error is</p>

An editor error usually gives you an ID. With that ID you can find the matching object on
the map — this is the method you will use most when fixing a map.

1. First read the ID in the error message (or look at where the ID appears in the
   "finding problems" images below).

    ![ID in an error](../../assets/editor/050.png)

2. Put the ID into the search box and search.

    ![Searching by ID in the search box](../../assets/editor/051.png)

## Some uses for finding problems

The images below are examples; in each one you get the ID first, then go back to the map
to locate it:

![Locating an object by ID (1)](../../assets/editor/052.png)

![Locating an object by ID (2)](../../assets/editor/053.png)

![Locating an object by ID (3)](../../assets/editor/054.png)

!!! tip "IDs change"
    The editor re-numbers every ID each time it saves, so the number may differ from the
    last one. So **what you wrote down is the ID at that moment**; after one more save,
    searching again may not find it.
