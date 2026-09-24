---
nav_label: "3rdParSettings 說明"
title: "3rdParSettings 說明"
icon: "lucide/puzzle"
description: "用來加載細緻模型以及部分材質，可不用。"
tags: [配置文件, 材質]
# ⚠️ 由 tools/docsgen.py 從 content/settings/third-party.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 3rdParSettings 說明（用來加載細緻模型以及部分材質，可不用） { #third-party }

<p class="kicker">SETTINGS · 可選，但啟用後效果明顯更好</p>

!!! info "這一步可以跳過"
    不配這個，地編照樣能用，只是模型與材質顯示得比較粗略。
    配置前需要先下載 [OgreSDK](../prepare/index.md#ogresdk)。

三處路徑都要指定，缺一處，對應的資源就加載不出來。

## 一、OgreXMLConverter.exe Path 選擇 { #ogreref }

1. 點擊 Select，確認 `OgreSDK_vc10_v1-7-4.zip` 解壓到了哪裡，找到它的根目錄。
2. 順着 `OgreSDK_vc10_v1-7-4\bin\release` 找到 `OgreXMLConverter.exe`，選中它。
3. 基礎設置完成，繼續第二、三步。

!!! example "示例路徑，僅供參考"
    ```text
    D:\RWRMap\OgreSDK_vc10_v1-7-4\bin\release
    ```

## 二、Mesh files path 選擇 { #mesh-path }

1. 找到 Steam 上小兵步槍的根目錄。可以在 Steam 界面裡「管理 → 瀏覽本地文件」定位。

    ![瀏覽本地文件](../../assets/editor/047.png)

2. 順着 `RunningWithRifles\media\packages\vanilla` 找到 `models` 文件夾，選中它。
3. 點擊 **load mesh**。

!!! example "示例路徑，僅供參考"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

設置完成後效果如下（以 Mesh 為例）：

![加載 mesh 之後](../../assets/editor/048.png)

/// caption
模型不再是方塊，可以看到原本的形體。
///

## 三、textures path 選擇 { #textures-path }

1. 與第二步的第 1 步相同。
2. 順着 `RunningWithRifles\media\packages\vanilla` 找到 `textures` 文件夾，選中它。
3. 點擊 **load textures**。

!!! example "示例路徑，僅供參考"
    ```text
    D:\steam\steamapps\common\RunningWithRifles\media\packages\vanilla
    ```

設置完成後效果如下（以 Decal 為例）：

![加載 textures 之後](../../assets/editor/049.png)

/// caption
地面貼花有了真正的材質。
///
