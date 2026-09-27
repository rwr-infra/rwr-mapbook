---
title: "Getting ready"
description: "How to configure the editor once it is downloaded, link it to your RWR map folder, and switch on the free camera."
source_sha256: 7f8a019addf29e641888e4a810e273e22eabd6437367ba15e0997912253ef9d5
translated: 2026-09-27
nav_label: "Getting ready"
icon: lucide/download
# ⚠️ 由 tools/docsgen.py 从 content/prepare/index.en.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

<!--
  译文同步提醒（2026-09-27）：本页已按 content/prepare/index.zh-hans.md 的最新改动重译过一遍，
  改动是这几处，麻烦过一眼英文措辞：
    · 两条 debugmode 提示（!!! warning 与 ??? quote）从「配置地编」第 1 步挪到了
      「开启自由视角」第 1 步；
    · 「开启自由视角」第 1 步那句启动选项重写，页尾补了 5 个启动项缩写（*[debugmode] 等），
      原来的 *[template] / *[RWR] 两个按简中一并去掉了；
    · 004 / 005 / 006 / 007 四张图的图下小字按简中改写；
    · 快捷键表里「碰撞箱」不再带链接；「F5 是同一个键，两回事」那个提示框按简中删掉了。
  之后再改正文，把上面 translated 的日期顺手改掉即可；source_sha256 不用动（它跟的是简中文件）。
-->

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

    ![](../../assets/editor/001.png)

    /// caption
    Unzip it to any path
    ///

2. Inside `1007_Data`, create a `templates` folder and a `map` folder.

    ![](../../assets/editor/002.png)

    /// caption
    Create the two folders, templates and map
    ///

3. [Pick and download a template](../download/index.md#materials) — straight from this site,
    or from the group files as before — and put it in the editor's `templates` folder.

    ![](../../assets/editor/003.png)

    /// caption
    Put the template into templates
    ///

    !!! note "So far only vanilla maps have a template"
        The desert and winter templates are not finished yet.

4. Pick a map you like as the foundation you are about to hack on, and put it in the editor's
    `map` folder. If you are not sure, use `map7` (it is the basis of the template file, and
    keeping the two in step sidesteps a few mysterious problems).

    ![](../../assets/editor/004.png)

    /// caption
    Copy the map file you picked to work on
    ///

    ![](../../assets/editor/005.png)

    /// caption
    Put it into the map folder
    ///

    !!! warning "Maps come in three kinds, and the template has to match"
        RWR's vanilla maps come in three kinds: normal mode, desert mode, winter mode.
        Whichever kind you use you have to install the matching template — and so far
        **only the "normal mode" kind has been made**, so you can only use the files under
        `\vanilla\maps`.

        Maps from `map19`, `\vanilla.desert\maps` and `\vanilla.winter\maps` may have
        compatibility problems (opening them to look is harmless, but do not use them as a
        base).

        Of course, you can also copy the `.svg` file from your map folder straight into the
        `templates` folder to serve as a template; this native template has not been polished
        by hand, but it still matches the map you picked reasonably well.

## 2. Link the folders { #sync }

The editor and the game do not open the same folder: after you save a map, you have to copy
the relevant files by hand into RWR's map path before RWR can read it. This method saves you
that step.

1. Press ++win+r++, type `cmd`, and open the command prompt.

    ![](../../assets/editor/006.png)

    /// caption
    The Win+R run box, type cmd
    ///

    ![](../../assets/editor/007.png)

    /// caption
    The cmd window that opens
    ///

2. Type this command:

    ```text
    mklink /J "the map folder you want to create in RWR" "the editor folder"
    ```

    !!! warning "Both paths have to be your own"
        Everybody's paths differ, fill in your own.

        The folder the first path points at must not have been created before you run the
        command; otherwise it reports that the folder already exists and the link cannot be
        made.

    ![](../../assets/editor/008.png)

    /// caption
    Type the mklink command
    ///

3. When it is done it should look like this:

    ![](../../assets/editor/009.png)

    /// caption
    Created successfully
    ///

## 3. Switch on RWR's free camera { #camera-mod }

1. In your Steam library, right-click RWR → Properties, and under **Launch Options** fill in
    debugmode, no_simulation, auto_update_tree_foliage and big_water (skip_nat_server_usage
    has nothing to do with this page, but it is in the line below so you can copy it in one
    go):

    ```text
    skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
    ```

    ![](../../assets/editor/010.png)

    /// caption
    Fill in the launch options
    ///

    !!! warning
        Once debugmode is added you cannot join multiplayer servers; if you want to use it,
        remove the debugmode code and run the game again.

    ??? quote "Adding the debugmode line alone is enough"
        Adding the debugmode line alone already lets you use F4 to switch on the free camera.
        The rest of the launch options configure the game's built-in camera mod, which can
        widen the render range or turn on the normal view.

2. Open the game, click "Start a new Quick Match mode", then click "Load mods".

    ![](../../assets/editor/011.png)

    /// caption
    Start a quick match
    ///

3. Select Camera mod.

    ![](../../assets/editor/012.png)

    /// caption
    Select Camera mod
    ///

4. Enter a map, press ++f4++ and move the mouse, and see whether anything responds.

    ![](../../assets/editor/013.png)

    /// caption
    Enter a map and press F4
    ///

    ### Camera mod key bindings

    | Key | What it does |
    | --- | --- |
    | ++f3++ | toggles the filter used for shooting promo footage |
    | ++f4++ | toggles the free camera |
    | ++f5++ | toggles normal mode, for looking at the collision box |
    | ++f6++ | switches between early morning / evening |
    | ++f7++ | toggles the GUI display |

*[debugmode]: turns on Debug mode, which lets you use the free camera and the camera mod
*[no_simulation]: drops the render distance — everything is computed and drawn across the whole map, which costs a lot of performance
*[auto_update_tree_foliage]: makes foliage always face the camera, so you do not see flat cardboard leaves from odd angles
*[big_water]: renders the whole body of water, not just the surface near the camera
*[skip_nat_server_usage]: this one is about connecting straight to domestic servers instead of routing abroad; ignore it
