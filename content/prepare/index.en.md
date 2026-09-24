---
title: "Getting ready"
description: "How to configure the editor once it is downloaded, sync it with your RWR folder, switch on the built-in camera mod, and download the OgreSDK."
source_sha256: 828ccfd24088ae5e7b7e94b023537a6b457455f896bc8c1441bd446ea486d30f
translated: 2026-09-25
nav_label: "Getting ready"
icon: lucide/download
tags: [Setup, Camera mod]
---

# Getting ready { #prepare }

<p class="kicker">PREPARE · get it installed, and only then talk about drawing</p>

Four things. Do them in order and you can start. Skip the first three and every step after
this gets stuck.

<div class="grid cards" markdown>

-   __1 · Set up the editor__

    ---

    Unzip it, make two folders, drop the template and a map in.

    [:octicons-arrow-right-24: Jump to this section](#setup)

-   __2 · Sync the folders__

    ---

    One `mklink` command wires the editor straight to RWR's map folder.

    [:octicons-arrow-right-24: Jump to this section](#sync)

-   __3 · Switch on the camera mod__

    ---

    One line in the launch options, and in game you can fly free and flip to normals.

    [:octicons-arrow-right-24: Jump to this section](#camera-mod)

-   __4 · Download the OgreSDK__

    ---

    Not needed yet — come back when 3rdParSettings needs it.

    [:octicons-arrow-right-24: Jump to this section](#ogresdk)

</div>

## 1. How to configure the editor after downloading { #setup }

1. Unzip the downloaded file to whatever path you like.

    ![Unzip it to any path](../assets/editor/001.png)

2. Inside `1007_Data`, create a `templates` folder and a `map` folder.

    ![Create the two folders, templates and map](../assets/editor/002.png)

3. Download the latest template from the group files (currently `vao0822.svg`) and put it
    in the editor's `templates` folder.

    ![Put the template into templates](../assets/editor/003.png)

    !!! note "So far only vanilla maps have a template"
        The desert and winter templates are not finished yet.

4. Pick a map you like and put it in the editor's `map` folder — **only one** — and throw
    in every relevant file from that map's folder. If you are not sure, use `map7`: it is
    the basis of the template above, and it sidesteps a few problems of unclear origin.

    ![Put the map files into map](../assets/editor/004.png)

    ![How it looks once it is in place](../assets/editor/005.png)

    !!! warning "Maps come in three kinds, and the template has to match"
        RWR's vanilla maps come in three kinds: vanilla among vanilla, the desert of
        vanilla, the winter of vanilla. Whichever kind you use you have to install the
        matching template — and so far **only the "vanilla among vanilla" kind has been
        made**, so you can only use the files under `\vanilla\maps`.

        Maps from `map19`, `\vanilla.desert\maps` and `\vanilla.winter\maps` may have
        compatibility problems — opening them to look is harmless, but do not use them
        as a base.

    ??? quote "The .meta files in the example images above"
        The pile of `.meta` files in the editor folder in the example images is nothing
        to worry about, it is only an example. Just put the whole of the left side into
        the editor folder on the right.

## 2. How to sync the editor folder with RWR's { #sync }

Keeping the editor's folder and the game's folder apart is a pain, so join them with one
symbolic link. After that you can play the map you just drew straight from the game.

1. Press ++win+r++, type `cmd`, and open the command prompt.

    ![The Win+R run box](../assets/editor/006.png)

    ![Type cmd](../assets/editor/007.png)

2. Type this command:

    ```text
    mklink /J "the map folder you want to create in RWR" "the editor folder"
    ```

    !!! note "Both paths have to be your own"
        Everybody's paths differ, fill in your own. This uses `\J` — a **directory
        junction**, not the soft link of `\D`; the former does not ask for administrator
        rights, and works across drives too.

        Make sure the first path **does not exist before you run the command**, otherwise
        it reports "file already exists".

    ![Type the mklink command](../assets/editor/008.png)

3. When it is done it should look like this:

    ![Created successfully](../assets/editor/009.png)

## 3. How to switch on RWR's built-in camera mod { #camera-mod }

The camera mod ships with the game, it is just not loaded by default. Switch it on, and
you can fly free as soon as you are in a map.

1. In your Steam library, right-click RWR → Properties, and under **Launch Options**
    enter:

    ```text
    skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
    ```

    ![Fill in the launch options](../assets/editor/010.png)

2. Open the game, click "Start a new Quick Match mode", then click "Load mods".

    ![Start a quick match](../assets/editor/011.png)

3. Select Camera mod.

    ![Select Camera mod](../assets/editor/012.png)

4. Enter a map, press ++f4++ and move the mouse, and see whether anything responds.

    ![Enter a map and press F4](../assets/editor/013.png)

    | Key | What it does |
    | --- | --- |
    | ++f3++ | toggles the filter used for shooting promo footage |
    | ++f4++ | toggles the free camera |
    | ++f5++ | toggles normal mode, for looking at the [collision box](#camera-mod "an object's collision volume; in the editor it is what tells you whether you can stand on it or shoot it") |
    | ++f6++ | switches between dawn / dusk |
    | ++f7++ | toggles the GUI display |

    !!! tip "F5 is the same key, two different things"
        In the editor ++f5++ is **refresh the interface**, in the camera mod it is
        **turn on normal mode**. It depends on which window you are in right now.

## OgreSDK download { #ogresdk }

Not needed right now — come back when
[3rdParSettings](../settings/third-party.md#third-party) needs it.

![The OgreSDK package](../assets/editor/014.png)

1. Download `OgreSDK_vc10_v1-7-4.zip` from the group files and unzip it to whatever path
    you like — preferably alongside the editor folder.

    ![Unzip the OgreSDK](../assets/editor/015.png)

2. That is all. 3rdParSettings will need it later; not covered here.

*[template]: the name an object is referred to by in `template = …`; that is how you look it up
*[RWR]: Running With Rifles
