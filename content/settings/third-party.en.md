---
title: "3rdParSettings"
description: "Loads detailed models and some materials. Optional, but it looks far better with it."
source_sha256: b438f4baa8788d072b4bf811852e202a8926a85cde2dbaf693638b2c3a8ee997
translated: 2026-09-25
nav_label: "3rdParSettings"
icon: "lucide/puzzle"
tags: [Config files, Materials]
---

# 3rdParSettings { #third-party }

<p class="kicker">SETTINGS · optional, but it looks far better with it</p>

!!! info "You can skip this step"
    Without it the editor works just the same, it only shows models and materials more coarsely.
    Setting it up needs [OgreSDK](../prepare/index.md#ogresdk) downloaded first.

Three paths to point at; miss one and the matching thing will not load.

## 1. Choosing the OgreXMLConverter.exe Path { #ogreref }

1. Click Select, think back to where `OgreSDK_vc10_v1-7-4.zip` was unzipped, and find its root folder.
2. Follow `OgreSDK_vc10_v1-7-4\bin\release` down to `OgreXMLConverter.exe` and pick it.
3. That is the groundwork done — on to steps two and three.

!!! example "My paths, for reference only"
    ```text
    D:\RWRMap\OgreSDK_vc10_v1-7-4\bin\release
    ```

## 2. Choosing the Mesh files path { #mesh-path }

1. Find the root folder of Running With Rifles in your Steam library. You can get there in the
   Steam client via Manage → Browse local files.

    ![Browse local files](../assets/editor/047.png)

2. Follow `RunningWithRifles\media\packages\vanilla` down to the `models` folder and pick it.
3. Click **load mesh**.

!!! example "My paths, for reference only"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

Once it is set, it looks like this (a Mesh, as an example):

![After loading the mesh](../assets/editor/048.png)

/// caption
Models are no longer boxes; you can see their real shape.
///

## 3. Choosing the textures path { #textures-path }

1. The same as step 1 of the section before.
2. Follow `RunningWithRifles\media\packages\vanilla` down to the `textures` folder and pick it.
3. Click **load textures**.

!!! example "My paths, for reference only"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

Once it is set, it looks like this (a Decal, as an example):

![After loading textures](../assets/editor/049.png)

/// caption
Ground decals now have their real materials.
///
