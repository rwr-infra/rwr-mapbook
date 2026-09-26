---
title: "Getting ready"
description: "How to configure the editor once it is downloaded, link it to your RWR map folder, and switch on the free camera."
source_sha256: 27503f0903820d7b338d79129db7f247a90a6f5e6d82e2ca5cc2c2155c19dd5f
translated: 2026-09-26
nav_label: "Getting ready"
icon: lucide/download
---

# Getting ready { #prepare }

<div class="grid cards" markdown>

-   __1 · Set up the editor__ <span class="badge badge--required">Required</span>

    ---

    Once the editor itself is unzipped, create the editor's `templates` and `map` folders to
    use it smoothly.

    [:octicons-arrow-right-24: Jump to this section](#setup)

-   __2 · Link the folders__ <span class="badge badge--optional">Optional</span>

    ---

    Use the `mklink` command to keep your map synced to RWR's map path when you save it.

    [:octicons-arrow-right-24: Jump to this section](#sync)

-   __3 · Switch on RWR's free camera__ <span class="badge badge--optional">Optional</span>

    ---

    Turn on the free camera with Debug mode to make inspecting a map easier.

    [:octicons-arrow-right-24: Jump to this section](#camera-mod)

</div>

## 1. Configure the editor { #setup }

1. [Download the latest editor build](../download/index.md#download) — straight from this
    site, or from the group files — then unzip the file to whatever path you like.

    ![Unzip it to any path](../assets/editor/001.png)

    !!! warning
        Once debugmode is added you cannot join multiplayer servers; if you want to use it,
        remove the debugmode code and run the game again.

    ??? quote "Adding the debugmode line alone is enough"
        Adding the debugmode line alone already lets you use F4 to switch on the free camera.
        The rest of the launch options configure the game's built-in camera mod, which can
        widen the render range or turn on the normal view.

2. Inside `1007_Data`, create a `templates` folder and a `map` folder.

    ![Create the two folders, templates and map](../assets/editor/002.png)

3. [Pick and download a template](../download/index.md#materials) — straight from this site,
    or from the group files as before — and put it in the editor's `templates` folder.

    ![Put the template into templates](../assets/editor/003.png)

    !!! note "So far only vanilla maps have a template"
        The desert and winter templates are not finished yet.

4. Pick a map you like as the foundation you are about to hack on, and put it in the editor's
    `map` folder. If you are not sure, use `map7` (it is the basis of the template file, and
    keeping the two in step sidesteps a few mysterious problems).

    ![Put the map files into map](../assets/editor/004.png)

    ![How it looks once it is in place](../assets/editor/005.png)

    !!! warning "Maps come in three kinds, and the template has to match"
        RWR's vanilla maps come in three kinds: vanilla among vanilla, the desert of vanilla,
        the winter of vanilla. Whichever kind you use you have to install the matching
        template — and so far **only the "vanilla among vanilla" kind has been made**, so you
        can only use the files under `\vanilla\maps`.

        Maps from `map19`, `\vanilla.desert\maps` and `\vanilla.winter\maps` may have
        compatibility problems — opening them to look is harmless, but do not use them as a
        base.

        Of course, you can also copy the `.svg` file from your map folder straight into the
        `templates` folder to serve as a template; this native template has not been polished
        by hand, but it still matches the map you picked reasonably well.

## Link the folders { #sync }

The editor and the game do not open the same folder: after you save a map, you have to copy
the relevant files by hand into RWR's map path before RWR can read it. This method saves you
that step.

1. Press ++win+r++, type `cmd`, and open the command prompt.

    ![The Win+R run box](../assets/editor/006.png)

    ![Type cmd](../assets/editor/007.png)

2. Type this command:

    ```text
    mklink /J "the map folder you want to create in RWR" "the editor folder"
    ```

    !!! warning "Both paths have to be your own"
        Everybody's paths differ, fill in your own.

        The folder the first path points at must not have been created before you run the
        command; otherwise it reports that the folder already exists and the link cannot be
        made.

    ![Type the mklink command](../assets/editor/008.png)

3. When it is done it should look like this:

    ![Created successfully](../assets/editor/009.png)

## 3. Switch on RWR's free camera { #camera-mod }

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

    ### Camera mod key bindings

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

*[template]: the name an object is referred to by in `template = …`; that is how you look it up
*[RWR]: Running With Rifles
