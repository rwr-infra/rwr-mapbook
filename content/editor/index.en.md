---
title: "Feature guide"
description: "The editor's features: every toolbar tool in turn, the key bindings, ID search, and the mapSettings / 3rdParSettings / RefpM configuration files."
source_sha256: af3c0c99d1898afe21b5174ca8ce46bd7882a94ebd5db9c9132a5810a3af14c9
translated: 2026-10-10
nav_label: "Feature guide"
icon: lucide/layout-grid
---

# Feature guide { #overview }

![](../assets/editor/016.png)

/// caption
The editor's main panel.
///


## The toolbar tools


### Save { #save }

!!! note "Saves the map; when it is done you get a sound."

* * *
### ViewMap { #viewmap }

??? note "Generates the map's first preview image (expand for details)"
    Clicking it produces a file called map_view_ls.png — that is the first preview image. It adds some map elements automatically, base perimeters for instance; once the map is finished you can build the map thumbnail from it.

    <span class="redact" tabindex="0">Yep — every map's final thumbnail, from back then until now, has been made by hand.</span>


* * *
### Select { #select }

??? note "Used to select objects on the map (expand for details)"
    Use the ++shift+1++ shortcut to jump quickly to the Select tool.
    * * *
    Related interaction:

    - Left click selects a single object; ++ctrl+lbutton++ (click) or ++lbutton++ (hold and drag) selects several.

    - Press ++esc++ to deselect.

    - Press ++delete++ to delete the selected target.

    - Press ++g++ to switch on move mode; moving the mouse then drags the selected objects away.

    - Press ++r++ to switch on rotate mode; moving the mouse then rotates the selected objects to some angle.

    !!! warning 
        You cannot select several platforms at once.

        In top-down view (orthographic) some platforms will not display or select properly; you have to switch to free camera (perspective) to select them.

        Moving and rotating in free camera (perspective) is not recommended; the interaction is poor.

* * *
### PinMan { #pinman }

??? note "Used to place a virtual reference object at the point you click. (expand for details)"
    Use the ++shift+2++ shortcut to jump quickly to the TankPin tool inside PinMan.
    !!! warning "There are three options, but only the tank works."

* * *
### WallE { #walle }
??? note "Used to pick the kind of wall from the list, and to draw nodes with PathBush and then press space to join them into a line in placement order. You can pick the wall kind first and then draw, or draw first and then pick the wall kind — once you have picked, click the wall you already drew and the replacement is done. (expand for details)"
    Use the ++shift+7++ shortcut to jump quickly to the PathBush tool inside WallE.
    * * *    
    The search bar finds an object quickly by name, and for what each wall's model looks like see [Model inventories · Wall E](../tables/wall.md).

    ![](../assets/editor/017.png)

    * * *
    With it selected by Select, you can edit the coordinates on this panel (the first field grows along X to the right, the second grows along Y downwards; the values are twice the coordinates of the current mouse position), use Add Point to add a connected segment in the drawing direction, and use the cross to delete that node.

    ![](../assets/editor/018.png)

    * * *
    With several selected by Select, you can delete the specified objects on this panel; the same goes for Buiding, Mesh and the rest.

    ![](../assets/editor/019.png)

    * * *
    With it selected by Select, you can see the id, the current layer and the wall kind on this panel, and set a custom height and whether to Merge.

    Marge is ticked by default, to stop the AI getting stuck on the wall and failing to climb over it.

    With ReHeight ticked you can type in the wall's height yourself.
    ![](../assets/editor/020.png)



* * *
### BuildingE { #buildinge }

??? note "Used to pick the kind of building from the list, and to draw buildings with DrawBush by holding the left button and dragging. You can pick the building kind first and then draw, or draw first and then pick the building kind — once you have picked, click the building you already drew and the replacement is done. (expand for details)"
    Use the ++shift+3++ shortcut to jump quickly to the DrawBush tool inside BuildingE.

    Use the ++shift+4++ shortcut to jump quickly to the RoofSwitch tool inside BuildingE.

    Use the ++shift+5++ shortcut to jump quickly to the BuildingMaterialChanger tool inside BuildingE.

    Use the ++shift+6++ shortcut to jump quickly to the HeightUp tool inside BuildingE.

    * * *
    The search bar finds an object quickly by name, and for what each building's model looks like see [Model inventories · Building E](../tables/building.md).

    ![](../assets/editor/021.png)

    * * *
    At the very top ^^HeightDown^^ and ^^HeightUp^^ change the height of the Building at the clicked spot, by 2 each time (6). ^^RoofSwitch^^ turns the roof into a pitched/flat roof; the pitched direction is fixed, so you have to select the building and press ++r++ to rotate it yourself.

    ![](../assets/editor/022.png)

    !!! quote "It is best to finish adjusting Height first and then stack new objects on top: the height of the objects above does not follow changes in the height of the Building below."

    * * *
    With it selected by Select, you can see the id, the current layer, whether the roof is pitched and the building kind on this panel.

    Offset sets a custom offset (the first field grows along X to the right, the second grows along Z towards the top, the third grows along Y downwards).

    ![](../assets/editor/023.png)

    !!! warning 
        Right now the X axis cannot be changed.
        If you want to put a Wall, Building, Platform or the like on top of a Building, then once you have thought it through you should draw from the bottom up; when drawing you have to make sure the start point is inside the previous element. That way all the objects stack one by one as layer1, layer2…, pick up the height of the previous one automatically, and climbing and other checks work properly too.

* * *
### PlatformE { #platforme }

??? note "Used to pick the kind of platform from the list and draw with ^^pathBush^^; like Wall, so no more detail here. (expand for details)"
    Use the ++shift+8++ shortcut to jump quickly to the PathBush tool inside PlatformE.

    Use the ++shift+9++ shortcut to jump quickly to the TypeChange tool inside PlatformE.

    Use the ++shift+0++ shortcut to jump quickly to the PlatformBasewallChanger tool inside PlatformE.
    * * *
    The search bar is like Wall's, so no more detail here.
    
    ![](../assets/editor/026.png)
    * * *
    At the very bottom ^^TypeChange^^ switches the Platform at the clicked spot between "no special property", the "deck" property and the "bridge" property.

    ChangeHeight works by setting the height and then pressing Enter to put the tool into use; it changes the height of the Platform at the clicked spot.

    ![](../assets/editor/027.png)
    !!! warning "The write-up of the properties is not finished"
    * * *

    With it selected by Select, you can edit the coordinates on this panel; the method is like Wall's, so no more detail here.

    ![](../assets/editor/028.png)

    * * *
    With it selected by Select, you can see the type, id, current layer, top material, the kind of wall on the platform's sides, the kind of wall added on top of the platform and the wall height on this panel.
    The kind of wall added on top of the platform can be changed with the WallE tool.
    The value added in SetMaterial can be wood, grass, pavement, terrian.

    ![](../assets/editor/029.png)
    !!! warning "The material preview part is not finished"
    * * *
    ??? quote "How do you draw a platform?"

        Take a transition cliff platform as the example:

        The goal this time is to get from the high ground on the left down a gentle slope into the water at the bottom of the valley. You can see that to the left of the **arrow direction** there is a slope that is not all that gentle, and to the right a sheer cliff, so the transition cliff should take the height of the slope on the left as its baseline.

        ![](../assets/editor/041.png)

        Because **when drawing a platform you have to make sure the end edge is to the right of the direction the start edge travels in**, and the start edge is the edge that decides the height, we should first draw on the gentle slope to the left of the arrow, following the arrow direction of figure 1.
        ![](../assets/editor/042.png)

        (Eight points were drawn; if you want the change to be more even you can place a few more.) Then press space, place the other corresponding eight points to the right of the arrow, and press space a second time to finish drawing.
 
        ![](../assets/editor/043.png)

        ![](../assets/editor/044.png)

        Then fine-tune the platform to make it reasonable.

        (The blue points are the reference points, that is the points generated by the first line drawn; the line between a blue point and a pink point is the terrain's transition.)

        (If your platform is that purple-and-black broken render colour, then congratulations, you placed it the wrong way round — please note once more that when drawing a platform you have to make sure the end edge is to the right of the direction the start edge travels in.)

        ![](../assets/editor/045.png)

        Have a look in game~

        <span class="redact" tabindex="0">Sure enough it came out a total mess — which shows how important it is to add a few more anchors and polish the terrain. Let this be a warning to you all :(</span>
        ![](../assets/editor/046.png)


* * *
### FuncObjects { #funcobjects }
??? note "Used to place objects that have some special interaction. (expand for details)"
    ^^LadderScatter^^ and ^^LadderEraser^^ place ladders and delete ladders. A placed ladder checks forwards automatically and snaps to nearby buildings, platforms and anything else with fixed collision.

    !!! warning "If a ladder is placed the wrong way round the snapping fails and you cannot climb it, and in version 0101 ladders have no forward indicator, so try not to mix up which way a ladder faces when adjusting it."
    * * *

    ^^ItemSupplyScatter^^ places the trigger area of a stash or an armory: stash is the stash, weapon_rack is the armory; once Select has picked it, click ChangeType below to switch.

    ![](../assets/editor/030.png)
    * * *

    ^^CrateScatter^^ and ^^CrateEraser^^ place wooden crates and delete wooden crates; the items inside are random and cannot be specified.

    ^^SpawnScatter^^ and ^^SpawnEraser^^ create spawn points and delete spawn points; a spawn point should not sit too close to the map edge.

    ^^BaseScatter^^ creates a base by left-dragging. With it selected by Select, you can change the base's displayed name (Name) and specify which faction captured this base first (Faction).


    ![](../assets/editor/031.png)

    ??? quote "A note on Faction"
        If you do not use Faction the base is assigned at random; filling in an integer assigns it by that integer's category, and the player faction defaults to faction 0.
        If you have set the map so that only two factions fight, then when Faction is 2 this base becomes a blank base that no faction holds.
        map13_2 is a special case, not covered here.

* * *
### MeshE { #meshe }

??? note "Used to pick the kind of model from the list. (expand for details)"

    The search bar is like Wall's, so no more detail here.

    ![](../assets/editor/032.png)
    * * *
    ^^StoneEraser^^ and ^^StoneScatter^^ delete a random rock or place a random rock; for what the rocks look like see [Model inventories · MESH E](../tables/mesh.md).

    ^^TreeEraser^^ and ^^TreeScatter^^ delete a random tree or place a random tree; for what the trees look like see [Model inventories · MESH E](../tables/mesh.md).

    ![](../assets/editor/033.png)
    * * *
    The tool at the very bottom is used like Wall: it places power poles as nodes, and once they are placed you press space to run wires in order between each pair — the wires are decoration only, with no collision.

    ![](../assets/editor/034.png)
    * * *
    With it selected by Select, you can see the id, the kind and the collision box on this panel (not shown if it is the default).
    With ReCollision ticked you can change length, height and width in the window above (measured from the centre).
    offset sets a custom offset (the first field grows along X to the right, the second grows along Z towards the top, the third grows along Y downwards).

    ![](../assets/editor/035.png)


* * *
### HeightMap { #heightmap }

??? note "Used to lay down the terrain's curvature. (expand for details)"
    ^^HeightBush^^ is the terrain brush. In the panel at the bottom left, SetHardness is the hardness, which decides how steep the transition is between the height you are painting and the background height, range 0 to 1; SerRange is the terrain brush's range; SetHeight is the terrain brush's height, range 0 to 1. Press X to lock the brush horizontally, Y to lock it vertically.

    ![](../assets/editor/036.png)
    * * *
    ^^HeightSmudge^^ drags the height within a certain range under the mouse and, following the direction the mouse moves, makes the nearby terrain deform as a transition.
    * * *
    ^^Smooth^^ flattens the terrain over the whole map.
    * * *
    ^^Noise^^ adds noise to the terrain over the whole map, so that the map is not a big flat plain at a single height value but has some tiny bumps.
    * * *
    heightPath is the path terrain brush; it is used like the Wall tool, the top left explains the relevant values and you can try it yourself.

    ![](../assets/editor/037.png)

* * *
### TerrainBash { #terrainbash }
??? note "Used to lay down changes in the ground texture. (expand for details)"
    ^^Pathpainter^^ is the path ground-texture brush; it is used like the Wall tool, the top left explains the relevant values and you can try it yourself.
    The decay exponent is adjusted with [ and ]; it is not a description typed twice that turned into [[/]].

    ![](../assets/editor/038.png)
    * * *
    ^^painter^^ is the ground-texture brush: Chg Index is the material kind, a number; Chg Rng is the range; Chg Har is the hardness.

    ![](../assets/editor/039.png)
    !!! warning "In version 0101, when you use this tool there may be a spare adjustment bar in the bottom left; it has no effect at all."
    * * *
    Smooth flattens the ground texture over the whole map.


* * *
### offroadbuilder { #offroadbuilder }

!!! note "Used to tell the AI that this route is a driving route; when driving, the AI prefers to pathfind along it. It is laid like the Wall tool."

* * *
### Decal { #decal }

??? note "Used to pick the kind of decal from the list; you can think of it as printing another layer of material on top of the ground texture. Once picked, left click to place it. (expand for details)"
    ^^deleteDecals^^ deletes the decals inside the marquee you drag.
    * * *
    Once Select has picked it, you can use Length to change this decal's size, that is its scale.

    ![](../assets/editor/040.png)


* * *
### Assaum { #assaum }
??? note "Used to pick assemblies from the list, an armory with its collision box and trigger area already built for example. Once picked, left click to place it. (expand for details)"
    The search bar is like Wall's, so no more detail here.
    * * *
    If you want to add an assembly of your own to the list, select the objects you want to group, give it a name via Name, then click Add and the group you picked joins the assembly list.
    !!! warning
        Assemblies do not follow the template; they are on a path of their own.
        When you click Add the objects have to be multi-selected; if only one is selected nothing is saved.




* * *
### ID search { #id-search }
??? note "The steps"
    1. Read the id here.

    ![](../assets/editor/050.png)

    /// caption
    Select the object to see it, or crack open the svg and look.
    ///    

    !!! warning
        The editor re-numbers every ID each time it saves, so the number may differ from the last one.

        So **what you wrote down is the ID at that moment**; after one more save, searching again may not find it.

    2. Put the ID into the search box and then click the search button on the right.

    ![](../assets/editor/051.png)

    /// caption
    You can see small green text appear below — the search worked.
    ///

??? quote "One use for finding an id"
    Oh no! RWR crashed halfway through loading my map?!
    Look through rwr_game.log under C:\Users\user\AppData\Roaming\Running with rifles and you can see that this time RWR blew up because it could not locate crate_adjusted.mesh.

    ![](../assets/editor/052.png)

    Search the svg map for this mesh and you find there are two related static_objects.

    ![](../assets/editor/053.png)

    /// caption
    Only one is shown here
    ///

    Search for those two static_objects and — wow, the hit rate really is high — you see the related id straight away.

    ![](../assets/editor/054.png)

    /// caption
    After that you just use the id search to delete those two objects from the map and you are done
    ///

!!! tip "IDs change"
    The editor re-numbers every ID each time it saves, so the number may differ from the last one.
    So **what you wrote down is the ID at that moment**; after one more save, searching again may not find it.

* * *
### mapSettings { #map-settings }

!!! note "Nothing verified yet."

??? example "**Content still to be verified.** (expand)"
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

!!! warning "If map settings are not written the map will not run; if you really do not know what to write, paste another map's and tweak it."

* * *
### 3rdParSettings { #third-party }
Used to load detailed models and part of the materials; you can skip it.
#### 1. Choosing the OgreXMLConverter.exe Path { #ogreref }

??? info "Version 0101 has this built in already, so you can skip it — expand to see the steps that no longer matter."
    1. Click Select, check where `OgreSDK_vc10_v1-7-4.zip` was unzipped, and find its root folder.
    2. Follow `OgreSDK_vc10_v1-7-4\bin\release` down to `OgreXMLConverter.exe` and pick it.
    3. That is the first configuration done — on to steps two and three.

    !!! example "Example paths, for reference only"
        ```text
        D:\RWRMap\OgreSDK_vc10_v1-7-4\bin\release
        ```

#### 2. Choosing the Mesh files path { #mesh-path }

1. Find the root folder of Running With Rifles on Steam. You can locate it in the Steam client via Manage → Browse local files.

    ![](../assets/editor/047.png)

2. Follow `RunningWithRifles\media\packages\vanilla` down to the `models` folder and pick it.
3. Click **load mesh**.

!!! example "Example paths, for reference only"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

Once it is set the result looks like this (a Mesh, as an example):

![](../assets/editor/048.png)

#### 3. Choosing the textures path { #textures-path }

1. The same as step 1 of the section before.
2. Follow `RunningWithRifles\media\packages\vanilla` down to the `textures` folder and pick it.
3. Click **load textures**.

!!! example "Example paths, for reference only"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

Once it is set the result looks like this (a Decal, as an example):

![](../assets/editor/049.png)

* * *
### RefpM { #reference-images }

Use ^^Import^^ to bring in a reference image, ^^Clear^^ to remove it.
^^ScaleX^^ and ^^ScaleY^^ squeeze or stretch the reference image horizontally and vertically; the value is a multiplier, so ScaleX 0.5 squeezes it to half width.
^^OffsetX^^ and ^^OffsetX<span class="redact" tabindex="0">really Y</span>^^ shift the reference image horizontally and vertically; the value is a distance, the first field grows along X to the right, the second along Y upwards.
^^Alpha^^ changes the reference image's transparency, fading it towards the left and making it solid towards the right.

* * *
### Key bindings { #keys }

!!! question "Is this table really complete?"
    | Key | Action |
    | --- | --- |
    | ++f5++ | Refresh the editor interface, and clean up illegal elements |
    | ++tab++ | Toggle between top-down view and free camera |
    | ++w++ ++a++ ++s++ ++d++ | Directional control |
    | Mouse wheel | In top-down view, adjusts the zoom; in free camera, adjusts the camera's movement speed |
    | ++q++ ++e++ | In free camera, adjusts the camera height |
    | ++esc++ | Deselect; lock the camera to the mouse / release the mouse |
    | ++shift+number key++ | Switch quickly to the matching tool |
    | ++x++ | Brush horizontal lock |
    | ++y++ | Brush vertical lock |
    | ++r++ | Rotate the selected object |
    | ++g++ | Move the selected object |
    | ++ctrl+c++ | Copy object |
    | ++ctrl+v++ | Paste object |
    | ++ctrl+z++ | Undo |


*[map thumbnail]: the map that opens in RWR when you press Tab; its file name is map.png.
