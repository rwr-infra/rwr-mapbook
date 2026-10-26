---
title: "Building E"
description: "Placeable houses."
source_sha256: a8f97c8267fa77c5687c1069cc7292a93505e282955178258a1dacbed7099096
translated: 2026-10-26
nav_label: "Building E"
icon: lucide/box
---

# Building E { #building }

## 3D preview

Below is a building assembled from the definitions in the editor template `vao0822.svg`: each floor has its **own texture on each of the four sides** (front / right / back / left), floors are separated by a slab, and the roof has its own set of rules. Drag to rotate, scroll to zoom.

<div class="ts-b3d"></div>

## Other { #other }

!!! warning "Notes"
    Note: a building is only materials arranged against one another, so this page
    documents the relevant keys and nothing else — put the combinations together
    yourself and try.

!!! note "Nothing verified yet."

??? example "**Unverified content.** (expand to view)"
    | Key | Value | Meaning | Notes |
    | --- | --- | --- | --- |
    | name | string | Building name | Usually kept identical to the outer rect's id (`material_XXX`); a building rect refers to it with `material=XXX`. The template need not show it — defaulting them to the same thing is fine. |
    | color | fill<br>stroke<br>0–1 alpha, R, G, B | Wall colour | E.g. `0.8 0.8 0.8 1.0` (with alpha); there is also a three-number spelling without alpha, e.g. `0.52 0.50 0.41`. The template should offer a few common fixed values plus a custom option; offering only the first would do as well. |
    | color_variance | 0–1 R, G, B | Random wall-colour offset range | Gives instances sharing one material a slight colour difference, e.g. `0.0 0.0 0.3`. The template should offer two choices — zero offset, and a custom offset; offering only the first would do as well. |
    | detail_texture | wall_atlas1.png<br>your own atlas file name | Wall texture atlas | Normally `wall_atlas1.png`. The template need not show it; fixing the texture seems fine. |
    | detail_texture_atlas_cell | column, row, total columns, total rows, margin, margin value | Cell of the wall texture inside the atlas | Three spellings coexist — 4, 5 or 6 numbers: 6 numbers = both margins written (e.g. `0 1 8 8 0.0078125 0.0078125`, 31 entries); 5 numbers = one margin written (e.g. `2 0 8 8 0.0078125`, 73 entries, presumably defaulting to a square); 4 numbers = no margin at all (1 entry, BuildingRuin's `1 1 2 2`). The template should offer a few named choices — picking one turns the attribute into the matching cell; I will list what each of them looks like in the atlas later. |
    | detail_texture_scale | X scale, Y scale | Wall texture scale | `3 3` is the most common. The template can use a preset per texture; not shown. |
    | detail_cutout_texture | cutout.png | Wall cut-out texture | Only this one value, untested. The template can just fix it; not shown. |
    | detail_cutout_texture_channel | 1 | Colour channel read from the wall cut-out texture | Only this one value, untested. The template can just fix it; not shown. |
    | detail_cutout_texture_scale | X scale, Y scale | Wall cut-out texture scale | The template can fix it to the matching preset. |
    | atlas_texture | building_atlas2.png<br>building_atlas3.png<br>building_atlas4.png<br>your own atlas file name | Main wall atlas image | A picker in the template? Then I will show what these look like in the atlas. |
    | 1st_floor_1 | name of the `style` it refers to | Ground floor, front wall texture | The template can default to all four faces being alike and expand into four faces once they differ; presets are enough. Shown in the atlas afterwards. Same below. Measured: 20 of the 91 materials use different styles on some of the four faces (e.g. BuildingArmory1's `1st_floor_3/4` borrow the `other_floor` patterns), so the "alike by default, expand when different" design holds up. |
    | 1st_floor_2 | name of the `style` it refers to | Ground floor, right wall texture |  |
    | 1st_floor_3 | name of the `style` it refers to | Ground floor, back wall texture |  |
    | 1st_floor_4 | name of the `style` it refers to | Ground floor, left wall texture |  |
    | other_floor_1 | name of the `style` it refers to | Upper floors, front wall texture |  |
    | other_floor_2 | name of the `style` it refers to | Upper floors, right wall texture |  |
    | other_floor_3 | name of the `style` it refers to | Upper floors, back wall texture |  |
    | other_floor_4 | name of the `style` it refers to | Upper floors, left wall texture |  |
    | roof_texture | wall_atlas1.png<br>your own atlas file name | Roof texture atlas | The template can fix it. |
    | roof_texture_atlas_cell | column, row, total columns, total rows, margin, margin value | Cell of the roof texture inside the atlas | Same format as `detail_texture_atlas_cell`. The template should offer a few named choices — picking one turns the attribute into the matching cell; I will list what each of them looks like in the atlas later. |
    | roof_texture_scale | X scale, Y scale | Roof texture scale | The template can use a preset per texture; not shown. |
    | roof_scale | X scale, Y scale | Overall roof texture scale | Untested. The template should probably preset it from the pick as well. |
    | roof_color | fill<br>stroke<br>0–1 alpha, R, G, B | Roof colour | Same rule as `color`. The template should offer a few common fixed values plus a custom option; offering only the first would do as well. |
    | roof_color_variance | 0–1 R, G, B | Random roof-colour offset range | Same rule as `color_variance`. The template should offer two choices — zero offset, and a custom offset; offering only the first would do as well. |
    | roof_cutout_texture | cutout.png<br>your own cut-out file name | Roof cut-out texture | Only these two values, untested. The template does not show it. |
    | roof_cutout_texture_channel | 1 | Colour channel read from the roof cut-out texture | Only this one value, untested. The template does not show it. |
    | roof_cutout_texture_scale | X scale, Y scale | Roof cut-out texture scale | The template can fix it to the matching preset. |
    | climbable | 0<br>1 | Climbable or not | 0 = not climbable, 1 = climbable. An option in the template? |
