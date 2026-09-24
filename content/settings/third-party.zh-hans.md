---
nav_label: "3rdParSettings 说明"
title: "3rdParSettings 说明"
icon: "lucide/puzzle"
description: "用来加载细致模型以及部分材质，可不用。"
---

# 3rdParSettings 说明（用来加载细致模型以及部分材质，可不用） { #third-party }

<p class="kicker">SETTINGS · 可选，但开了好看得多</p>

!!! info "这一步可以跳过"
    不配这个，地编照样能用，只是模型与材质显示得粗一些。
    配它需要先下 [OgreSDK](../prepare/index.md#ogresdk)。

三处路径要指，缺一处对应的东西就加载不出来。

## 一、OgreXMLConverter.exe Path 选择 { #ogreref }

1. 点击 Select，回想一下 `OgreSDK_vc10_v1-7-4.zip` 解压到哪了，找到它的根目录。
2. 顺着 `OgreSDK_vc10_v1-7-4\bin\release` 找到 `OgreXMLConverter.exe`，选中它。
3. 基础工作完成，继续第二、三步。

!!! example "我的路径，仅供参考"
    ```text
    D:\RWRMap\OgreSDK_vc10_v1-7-4\bin\release
    ```

## 二、Mesh files path 选择 { #mesh-path }

1. 找到你 Steam 上小兵步枪的根目录。可以在 Steam 界面里「管理 → 浏览本地文件」定位。

    ![浏览本地文件](../assets/editor/047.png)

2. 顺着 `RunningWithRifles\media\packages\vanilla` 找到 `models` 文件夹，选中它。
3. 点击 **load mesh**。

!!! example "我的路径，仅供参考"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

设好之后效果是这样（以 Mesh 为例）：

![加载 mesh 之后](../assets/editor/048.png)

/// caption
模型不再是方块，能看到原本的形体了。
///

## 三、textures path 选择 { #textures-path }

1. 与第二步的第 1 步相同。
2. 顺着 `RunningWithRifles\media\packages\vanilla` 找到 `textures` 文件夹，选中它。
3. 点击 **load textures**。

!!! example "我的路径，仅供参考"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

设好之后效果是这样（以 Decal 为例）：

![加载 textures 之后](../assets/editor/049.png)

/// caption
地面贴花有了真正的材质。
///
