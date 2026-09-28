---
title: "Feature guide"
description: "The editor's features: every toolbar tool in turn, the key bindings, ID search, and the mapSettings / 3rdParSettings / RefpM configuration files."
source_sha256: 045cb90469a604c9312407becdb6e58580fd290983b098965fbe9e475d24dcda
translated: 2026-09-27
nav_label: "Feature guide"
icon: lucide/layout-grid
tags: [Interface, Tools, Config files]
---

# Feature guide { #overview }

Fourteen buttons sit on the editor's toolbar, one job each. They are listed below
in left-to-right order; each one leads to its own section.

![](../assets/editor/016.png)

/// caption
The editor's main panel. That row on the toolbar is the tools below.
///

## The toolbar tools

<div class="grid cards cards--stack" markdown>

-   __Save__

    ---

    Save the map

    [:octicons-arrow-right-24: Read](#save)

-   __ViewMap__

    ---

    Generate the tactical preview image

    [:octicons-arrow-right-24: Read](#viewmap)

-   __Select__

    ---

    Select, move, rotate

    [:octicons-arrow-right-24: Read](#select)

-   __PinMan__

    ---

    Place reference objects

    [:octicons-arrow-right-24: Read](#pinman)

-   __WallE__

    ---

    Draw walls

    [:octicons-arrow-right-24: Read](#walle)

-   __BuildingE__

    ---

    Place houses

    [:octicons-arrow-right-24: Read](#buildinge)

-   __PlatformE__

    ---

    Draw platforms, change heights

    [:octicons-arrow-right-24: Read](#platforme)

-   __FuncObjects__

    ---

    Ladders, crates, spawn points, bases

    [:octicons-arrow-right-24: Read](#funcobjects)

-   __MeshE__

    ---

    Place models, power poles

    [:octicons-arrow-right-24: Read](#meshe)

-   __HeightMap__

    ---

    Paint terrain height

    [:octicons-arrow-right-24: Read](#heightmap)

-   __TerrainBash__

    ---

    Paint ground texture

    [:octicons-arrow-right-24: Read](#terrainbash)

-   __offroadbuilder__

    ---

    Mark driving routes for the AI

    [:octicons-arrow-right-24: Read](#offroadbuilder)

-   __Decal__

    ---

    Ground decals

    [:octicons-arrow-right-24: Read](#decal)

-   __Assaum__

    ---

    Ready-made assemblies

    [:octicons-arrow-right-24: Read](#assaum)

-   __A few extra notes__

    ---

    Stacking order, ID reordering — the traps you cannot dodge

    [:octicons-arrow-right-24: Read](#extra)

-   __How do you draw a platform?__

    ---

    From high ground down a gentle slope into the water, drawn through once step by step

    [:octicons-arrow-right-24: Read](#platform)

</div>

### Save { #save }

Saves the map; when it is done you get a sound.

### ViewMap { #viewmap }

Generates the tactical preview image of the map — the map you look at in RWR by pressing Tab.

!!! question "Not verified"
    The file name has to be adjusted by hand (not verified item by item).

### Select { #select }

- Left click to select a single object, Ctrl+left click or left-drag to select several.
- Press Esc to deselect.
- Press Delete to delete the selected target.
- Press G to switch on move mode; moving the mouse then drags the selected objects away.
- Press R to switch on rotate mode; moving the mouse then rotates the selected objects to some angle.
- In any other tool mode, the Shift+1 shortcut jumps quickly back to the Select tool.
- You cannot select several platforms at once.
- In top-down view (orthographic) some platforms will not display or select properly; you have to switch to free camera (perspective) to select them.
- Moving and rotating in free camera (perspective) is not recommended; the interaction is poor.

### PinMan { #pinman }

Used to place a virtual reference object at the point you click.

There are three options, but only the tank works.

### WallE { #walle }

- Used to pick the kind of wall from the list, and to draw nodes with PathBush and then press space to join them into a line in placement order. You can pick the wall kind first and then draw, or draw first and then pick the wall kind — once you have picked, click the wall you already drew and the replacement is done.
- The search bar finds an object quickly by name, and for what each wall does see [Model inventories · Wall E](../tables/wall.md).
- With it selected by Select, you can edit the coordinates on this panel (the first field grows along X to the right, the second grows along Y downwards; the values are twice the coordinates of the current mouse position), use Add Point to add a connected segment in the drawing direction, and use the cross to delete that node.
- With several selected by Select, you can delete the specified objects on this panel; the same goes for Buiding, Mesh and the rest.
- With it selected by Select, you can see the id, the current layer and the wall kind on this panel, and set a custom height and whether to Merge.
- Marge is ticked by default, to stop the AI getting stuck on the wall and failing to climb over it.
- With ReHeight ticked you can type in the wall's height yourself.

![](../assets/editor/017.png)

/// caption
Main panel 1
///

![](../assets/editor/018.png)

/// caption
Main panel 2
///

![](../assets/editor/019.png)

/// caption
Main panel 3
///

![](../assets/editor/020.png)

/// caption
Main panel 4
///

### BuildingE { #buildinge }

- Used to pick the kind of building from the list, and to draw buildings with DrawBush by holding the left button and dragging. You can pick the building kind first and then draw, or draw first and then pick the building kind — once you have picked, click the building you already drew and the replacement is done.
- The search bar finds an object quickly by name, and for what each building looks like see [Model inventories · Building E](../tables/building.md).
- At the very top, HeightDown and HeightUp change the height of the Building at the clicked spot, by 2 each time (6).
- RoofSwitch turns the roof into a pitched/flat roof; the pitched direction is fixed, so you have to select the building and press R to rotate it yourself.
- It is best to finish adjusting Height first and then stack new objects on top: the height of the objects above does not follow changes in the height of the Building below.
- With it selected by Select, you can see the id, the current layer, whether the roof is pitched and the building kind on this panel.
- Offset sets a custom offset (the first field grows along X to the right, the second grows along Z towards the top, the third grows along Y downwards).
- Right now the X axis cannot be changed.

!!! warning "Needs fixing"
    In free camera (perspective), the perspective has serious problems depending on the direction; see the example image on the right above.

![](../assets/editor/021.png)

/// caption
Main panel 5
///

![](../assets/editor/022.png)

/// caption
Main panel 6
///

![](../assets/editor/023.png)

/// caption
Main panel 7
///

### PlatformE { #platforme }

- Used to pick the kind of platform from the list and draw with pathBush; like Wall, so no more detail here.
- For a worked example see below: How do you draw a platform?
- The search bar is like Wall's, so no more detail here.
- At the very bottom, TypeChange switches the Platform at the clicked spot between no special property, the deck property and the bridge property. (This section is not finished yet.)
- ChangeHei works by setting the height and then pressing Enter to put the tool into use; it changes the height of the Platform at the clicked spot.
- With it selected by Select, you can edit the coordinates on this panel; the method is like Wall's, so no more detail here.
- With it selected by Select, you can see the type, id, current layer, top material, the kind of wall on the platform's sides, the kind of wall added on top of the platform and the wall height on this panel.
- The kind of wall added on top of the platform can be changed with the WallE tool.
- The value added in SetMaterial can be wood, grass, pavement, terrian. (This section is not finished yet.)

![](../assets/editor/026.png)

/// caption
Main panel 10
///

![](../assets/editor/027.png)

/// caption
Main panel 11
///

![](../assets/editor/028.png)

/// caption
Main panel 12
///

![](../assets/editor/029.png)

/// caption
Main panel 13
///

### FuncObjects { #funcobjects }

LadderScatter and LadderEraser place ladders and delete ladders. A placed ladder snaps
automatically to nearby buildings, platforms and anything else with fixed collision.

!!! warning "Needs optimisation"
    The ladders' automatic snapping is currently unreliable.

    <span class="redact" tabindex="0">Right now the snapping is about as well-behaved as a cat, and there are problems.</span>

- ItemSupplyScatter places the trigger area of a stash or an armory: stash is the stash, weapon_rack is the armory; once selected, click ChangeType below to switch.
- CrateScatter and CrateEraser place wooden crates and delete wooden crates; the items inside are random and cannot be specified.
- SpawnScatter and SpawnEraser create spawn points and delete spawn points; a spawn point should not sit too close to the map edge.
- BaseScatter creates a base by left-dragging. With it selected by Select, you can change the base's displayed name and specify which faction captured this base first; fill in 0, 1 or 2, <span class="redact" tabindex="0">which one is which I honestly do not know either haha XD</span>

![](../assets/editor/030.png)

/// caption
Main panel 14
///

![](../assets/editor/031.png)

/// caption
Main panel 15
///

### MeshE { #meshe }

- Used to pick the kind of model from the list.
- The search bar is like Wall's, so no more detail here.
- StoneEraser and StoneScatter delete a random rock or place a random rock; for what the rocks look like see [Model inventories · MESH E](../tables/mesh.md).
- TreeEraser and TreeScatter delete a random tree or place a random tree; for what the trees look like see [Model inventories · MESH E](../tables/mesh.md).
- The tool at the very bottom is used like Wall: it places power poles as nodes, and once they are placed you press space to run wires in order between each pair — the wires are decoration only, with no collision.
- With it selected by Select, you can see the id, the kind and the collision box on this panel (not shown if it is the default).
- With ReCollision ticked you can change length, height and width in the window above (measured from the centre).
- offset sets a custom offset (the first field grows along X to the right, the second grows along Z towards the top, the third grows along Y downwards).

![](../assets/editor/032.png)

/// caption
Main panel 16
///

![](../assets/editor/033.png)

/// caption
Main panel 17
///

![](../assets/editor/034.png)

/// caption
Main panel 18
///

![](../assets/editor/035.png)

/// caption
Main panel 19
///

### HeightMap { #heightmap }

- HeightBush is the terrain brush. In the panel at the bottom left, SetHardness is the hardness, which decides how steep the transition is between the height you are painting and the background height, range 0 to 1; SerRange is the terrain brush's range; SetHeight is the terrain brush's height, range 0 to 1. Press X to lock the brush horizontally, Y to lock it vertically.
- HeightSmudge drags the height within a certain range under the mouse and, following the direction the mouse moves, makes the nearby terrain deform as a transition.
- Smooth flattens the terrain over the whole map.
- Noise adds noise to the terrain over the whole map, so that the map is not a big flat plain at a single height value but has some tiny bumps.
- heightPath is the path terrain brush; it is used like the Wall tool, the top left explains the relevant values and you can try it yourself.

![](../assets/editor/036.png)

/// caption
Main panel 20
///

![](../assets/editor/037.png)

/// caption
Main panel 21
///

### TerrainBash { #terrainbash }

- Pathpainter is the path ground-texture brush; it is used like the Wall tool, the top left explains the relevant values and you can try it yourself.
- The decay exponent is adjusted with [ and ]; it is not a description typed twice that turned into [[/]].
- painter is the ground-texture brush: Chg Index is the material kind, a number; Chg Rng is the range; Chg Har is the hardness.
- In version 0101, when you use this tool there may be a spare adjustment bar in the bottom left; it has no effect at all.
- Smooth flattens the ground texture over the whole map.

![](../assets/editor/038.png)

/// caption
Main panel 22
///

![](../assets/editor/039.png)

/// caption
Main panel 23
///

### offroadbuilder { #offroadbuilder }

Used to tell the AI that this route is a driving route.

It is used like the Wall tool.

### Decal { #decal }

- Used to pick the kind of decal from the list; you can think of it as printing another layer of material on top of the ground texture. Once picked, left click to place it.
- deleteDecals deletes the decals inside the marquee you drag.
- Once Select has picked it, you can use Length to change this decal's size, that is its scale.

![](../assets/editor/040.png)

/// caption
Main panel 24
///

### Assaum { #assaum }

Used to pick assemblies from the list, an armory with its collision box and trigger area already built for example. Once picked, left click to place it.

Add and Name are unavailable for now, with no effect.

### A few extra notes { #extra }

1. If you want to put a Wall, Building, Platform or the like on top of a Building, then once you have thought it through you should draw from the bottom up; when drawing you have to make sure the start point is inside the previous element. That way all the objects stack one by one as layer1, layer2…, pick up the height of the previous one automatically, and climbing and other checks work properly too.

2. Every time the editor saves it re-sorts the IDs, so the numbers may change.

### How do you draw a platform? { #platform }

Take a transition cliff platform as the example:

The goal here is to get from the high ground on the left down a gentle slope into the water
at the bottom of the valley. To the left of the arrow direction there is a slope that is not
all that gentle, and to the right a sheer cliff, so the transition cliff should take the
height of the slope on the left as its baseline.

![](../assets/editor/041.png)

/// caption
Main panel 25
///

![](../assets/editor/042.png)

/// caption
Main panel 26
///

Because when drawing a platform you have to make sure the end edge is to the right of the direction the start edge travels in, and the start edge is the edge that decides the height, we should first draw on the gentle slope to the left of the arrow, following the arrow direction of figure 1.

(Eight points were drawn; if you want the change to be more even you can place a few more.) Then press space, place the other corresponding eight points to the right of the arrow, and press space a second time to finish drawing.

![](../assets/editor/043.png)

/// caption
Main panel 27
///

![](../assets/editor/044.png)

/// caption
Main panel 28
///

Then fine-tune the platform to make it reasonable.

(The blue points are the reference points, that is the points generated by the first line drawn; the line between a blue point and a pink point is the terrain's transition.)

(If your platform is that purple-and-black broken render colour, <span class="redact" tabindex="0">then congratulations, you placed it the wrong way round</span> — please note once more that when drawing a platform you have to make sure the end edge is to the right of the direction the start edge travels in.)

(The images are not compressed, so the details can be zoomed in on.)

![](../assets/editor/045.png)

/// caption
Main panel 29
///

Looking at it in game, the terrain still came out poorly; adding a few more anchors and
polishing the terrain matters.

??? note "The author's aside"
    Sure enough it came out a total mess — which shows how important it is to add a few more
    anchors and polish the terrain. Let this be a warning to you all :(

![](../assets/editor/046.png)

/// caption
Main panel 30
///

## Key bindings { #keys }

!!! question "Is this table complete?"
    This page originally left a line blank, "(is it really complete?)" — meaning the table is
    **not verified item by item**. If you find something missing while using it, add it to
    the table below.

| Key | Action |
| --- | --- |
| ++f5++ | Refresh the editor interface, and clean up illegal elements |
| ++tab++ | Toggle between top-down view and free camera |
| ++w++ ++a++ ++s++ ++d++ | Directional control |
| Mouse wheel | In top-down view, adjusts the zoom; in free camera, adjusts the camera's movement speed |
| ++q++ ++e++ | In free camera, adjusts the camera height |
| ++esc++ | Deselect; lock the camera to the mouse / release the mouse |
| ++shift+1++ | Switch to the Select tool |
| ++x++ | Brush horizontal lock |
| ++y++ | Brush vertical lock |
| ++r++ | Rotate the selected object |
| ++g++ | Move the selected object |
| ++ctrl+c++ | Copy object |
| ++ctrl+v++ | Paste object |
| ++ctrl+z++ | Undo |

!!! tip "Two that are not in this table"
    The camera mod's ++f3++–++f7++ are a separate set; see [Getting ready → 3](../prepare/index.md#camera-mod).

    And ++f5++ on this page is **refresh the editor**, while in the camera mod it is
    **turn on normals mode** — the same key, depending on which one you have open.

## ID search { #id-search }

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

### Some uses for finding problems

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

## Configuration files

Three configurations, one job each: one for the map itself, one for models and materials
that live outside the editor, and one for a reference image you lay underneath.

### mapSettings { #map-settings }

!!! warning "This page is marked **untested**"
    It has not been verified item by item. Every row below keeps its **Description** column
    exactly as written, and several rows say outright "not tried" and "no idea what this
    is" — that is the author's original record, and **not tried is not tried**: do not read
    those rows as answers.

| Field | Example | Notes | Description |
| --- | --- | --- | --- |
| `ambience_alert_day_sound` | `ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | not tried, no idea what this is |
| `ambience_day_sound` | `ambient_daytime.wav`<br>`ambient_lightrain.wav` |  | daytime ambient sound |
| `ambience_night_sound` | `ambient_lightrain_night.wav` |  | nighttime ambient sound |
| `day_color` | `#e5c685ff`<br>`fill` | any hex colour | the daytime colour |
| `description` | `16 bases`<br>`2 faction king of the hill map`<br>`assault map - 11 bases`<br>`conquest map - 10 bases`<br>`pure pvp map` | you can enter anything, but keeping to the format is better | the map description |
| `flip` | `-1` |  | no idea what this is, not tried |
| `global_effect` | `ambience_alert_day_sound`<br>`ambient_alert_daytime.wav`<br>`ambient_lightrain_alert.wav` |  | global effect |
| `name` | `Route 666` | you can enter anything | the map name |
| `night_color` | `#136395`<br>`#5f5fc0ff`<br>`stroke` | any hex colour | the nighttime colour |
| `randomize_faction_index` | `0`<br>`1` |  | not tried, no idea what this is |
| `show_base_names_in_map_view` | `0` |  | no idea what this is, not tried |
| `starting_day_phase` | `0.1`<br>`6` |  | when the campaign starts |
| `visible_in_menu` | `0`<br>`1` |  | whether it shows up in the list |

!!! tip "The third value in the two colour rows"
    Besides the colour value, the examples for `day_color` and `night_color` also carry a
    `fill` / `stroke` — the page never says what that is, and it has not been verified.
    Just fill in the colour value.

### 3rdParSettings { #third-party }

!!! info "You can skip this step"
    Without it the editor works just the same, it only shows models and materials more coarsely.
    Setting it up means downloading [OgreSDK](../download/index.md#materials) first.

Three paths have to be set; miss one and the matching resources will not load.

#### 1. Choosing the OgreXMLConverter.exe Path { #ogreref }

1. Click Select, check where `OgreSDK_vc10_v1-7-4.zip` was unzipped, and find its root folder.
2. Follow `OgreSDK_vc10_v1-7-4\bin\release` down to `OgreXMLConverter.exe` and pick it.
3. That is the first configuration done — on to steps two and three.

!!! example "Example paths, for reference only"
    ```text
    D:\RWRMap\OgreSDK_vc10_v1-7-4\bin\release
    ```

#### 2. Choosing the Mesh files path { #mesh-path }

1. Find the root folder of Running With Rifles in your Steam library. You can get there in the
   Steam client via Manage → Browse local files.

    ![](../assets/editor/047.png)

    /// caption
    Browse local files
    ///

2. Follow `RunningWithRifles\media\packages\vanilla` down to the `models` folder and pick it.
3. Click **load mesh**.

!!! example "Example paths, for reference only"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

Once it is set, the result looks like this (a Mesh, as an example):

![](../assets/editor/048.png)

/// caption
Models are no longer boxes; you can see their real shape.
///

#### 3. Choosing the textures path { #textures-path }

1. The same as step 1 of the section before.
2. Follow `RunningWithRifles\media\packages\vanilla` down to the `textures` folder and pick it.
3. Click **load textures**.

!!! example "Example paths, for reference only"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

Once it is set, the result looks like this (a Decal, as an example):

![](../assets/editor/049.png)

/// caption
Ground decals now have their real materials.
///

### RefpM { #reference-images }

When you build a map, lay a satellite image or a hand-drawn sketch underneath and place
objects against it. Use **Import** to bring in a reference image, **Clear** to remove it.

| Control | What it does | What to fill in |
| --- | --- | --- |
| `ScaleX` | Squeezes or stretches the reference image horizontally | A multiplier. `0.5` squeezes it to half width |
| `ScaleY` | Squeezes or stretches the reference image vertically | A multiplier |
| `OffsetX` | Shifts the reference image horizontally | A distance. The X axis grows to the right |
| `OffsetY` | Shifts the reference image vertically | A distance. The Y axis grows upwards |
| `Alpha` | Changes the reference image's transparency | Fades it towards the left, makes it solid towards the right |

??? note "The author's aside"
    As written it read "OffsetX and OffsetX are really Y's job" and "towards the right it
    turns 躯体化" — from the context these are typos, so this page writes `OffsetY` and
    "towards the right it turns solid". Tell me if you want them put back.
