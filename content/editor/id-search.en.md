---
title: "ID search"
description: "Locating an object by ID when an error is thrown."
source_sha256: 16e9826e1636923b7c16405f0d085480708282e9838edcfa74e8e09c03472573
translated: 2026-09-27
nav_label: "ID search"
icon: lucide/search
tags: [Troubleshooting, Tools]
---

# ID search { #id-search }

<p class="kicker">EDITOR · what that number in the error is</p>

An editor error usually gives you an ID. With that ID you can find the matching object on
the map — this is the method you will use most when fixing a map.

1. First read the ID in the error message (or look at where the ID appears in the
   "finding problems" images below).

    ![](../assets/editor/050.png)

    /// caption
    ID in an error
    ///

2. Put the ID into the search box and search.

    ![](../assets/editor/051.png)

    /// caption
    Searching by ID in the search box
    ///

## Some uses for finding problems

The images below are examples; in each one you get the ID first, then go back to the map
to locate it:

![](../assets/editor/052.png)

/// caption
Locating an object by ID (1)
///

![](../assets/editor/053.png)

/// caption
Locating an object by ID (2)
///

![](../assets/editor/054.png)

/// caption
Locating an object by ID (3)
///

!!! tip "IDs change"
    The editor re-numbers every ID each time it saves, so the number may differ from the
    last one. So **what you wrote down is the ID at that moment**; after one more save,
    searching again may not find it.
