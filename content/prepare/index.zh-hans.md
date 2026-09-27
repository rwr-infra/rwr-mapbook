---
nav_label: "准备工作"
title: "准备工作"
icon: "lucide/download"
description: "下载后的配置、与 RWR 地图文件夹的联接，以及开启自由视角。"
---

# 准备工作 { #prepare }

<div class="grid cards" markdown>

-   __1 · 配置地编__ <span class="badge badge--required">必须</span>

    ---

    解压完本体后，还需创建地编的 `templates` 与 `map` 文件夹以顺利使用。

    [:octicons-arrow-right-24: 跳到这一节](#setup)

-   __2 · 联接文件夹__ <span class="badge badge--optional">可选</span>

    ---

    使用 `mklink` 命令，让你的地图在保存时同步到 RWR 的地图路径中。

    [:octicons-arrow-right-24: 跳到这一节](#sync)

-   __3 · 开启 RWR 自由视角__ <span class="badge badge--optional">可选</span>

    ---

    使用 Debug 模式开启自由视角，让检视地图更方便。

    [:octicons-arrow-right-24: 跳到这一节](#camera-mod)

</div>

## 一、配置地编 { #setup }

1. [下载最新版本地编](../download/index.md#download)（本站可直接下载，也可从群文件下载）后，将文件解压到你自己喜欢的路径。

    ![](../assets/editor/001.png)

    /// caption
    解压到任意路径
    ///


2. 在 `1007_Data` 中创建一个 `templates` 文件夹与 `map` 文件夹。

    ![](../assets/editor/002.png)

    /// caption
    建 templates 与 map 两个文件夹
    ///

3. [选择并下载模板](../download/index.md#materials)（本站可直接下载，也可照旧从群文件拿），放进地编的 `templates` 文件夹中。

    ![](../assets/editor/003.png)

    /// caption
    把模板放进 templates
    ///

    !!! note "目前只有原版地图的模板"
        沙漠与雪地的模板暂未制作完成。

4. 选一个你喜欢的地图作为等待魔改的底图，放进地编的 `map` 文件夹。拿不准就用 `map7`（它就是模板文件的底稿，两个相统一可以避开一些神秘问题）。

    ![](../assets/editor/004.png)

    /// caption
    复制好你选的待魔改地图文件
    ///

    ![](../assets/editor/005.png)

    /// caption
    放进 map 文件夹
    ///

    !!! warning "地图分三类，模板要对得上"
        RWR 原版地图分为三个类型：普通模式、沙漠模式、雪地模式。用哪个类型就要装对应的模板，而目前**只做了「普通模式」这一类**，所以只能用 `\vanilla\maps` 里的文件。

        `map19`、`\vanilla.desert\maps`、`\vanilla.winter\maps` 里的地图可能会有适配问题（打开看看不影响，但拿它们当底子做就算了）。

        当然，你也可以把你地图文件夹中的 `.svg` 文件直接复制到 `templates` 文件夹中充当模板，虽然这个原生模板没经过人工完善，但仍然可以和你选的地图较好适配。

## 二、联接文件夹 { #sync }

地编与游戏打开的目录并不相同，在你保存完地图后需要将相关文件手动复制粘贴到 RWR 的地图路径中才能被 RWR 读取到。用这个方法就能免去这一步。

1. 按 ++win+r++，输入 `cmd`，打开命令提示符。

    ![](../assets/editor/006.png)

    /// caption
    Win+R打开运行框，输入 cmd
    ///

    ![](../assets/editor/007.png)

    /// caption
    打开的 cmd 界面
    ///

2. 输入下面这条命令：

    ```text
    mklink /J "RWR要创建的地图文件夹" "地编的文件夹"
    ```

    !!! warning "两个路径都要按自己的来"
        每个人的路径都不一样，按自己的填。

        第一个路径所指定的文件夹要保证执行命令之前它未被创建，否则会提示文件夹已存在，进而无法进行联接。

    ![](../assets/editor/008.png)

    /// caption
    输入 mklink 命令
    ///

3. 完成后应该是这样：

    ![](../assets/editor/009.png)

    /// caption
    创建成功
    ///

## 三、开启 RWR 自由视角 { #camera-mod }

1. 在 Steam 游戏库里右键 RWR → 属性，在**启动选项**里填入 debugmode、no_simulation、auto_update_tree_foliage、big_water（ skip_nat_server_usage 与本文无关，但是为方便复制就加到下面了）：

    ```text
    skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
    ```

    ![](../assets/editor/010.png)

    /// caption
    填入启动选项
    ///

    !!! warning
        添加了 debugmode 后无法加入多人服务器，如果想使用请删除 debugmode 相关代码再次运行游戏。

    ??? quote "其实只加 debugmode 这一条就行"
        加 debugmode 这一条可以正常使用 F4 开启自由视角了，剩下的启动项代码是配置游戏自带的相机 mod 的，这个 mod 可以实现扩大渲染范围或开启法线视图等功能。

2. 打开游戏，点「开始新的快速比赛模式」，然后点「加载模组」。

    ![](../assets/editor/011.png)

3. 选中 Camera mod。

    ![](../assets/editor/012.png)

    /// caption
    选中 Camera mod
    ///

4. 进入地图，按 ++f4++ 移动鼠标，看看有没有反应。

    ![](../assets/editor/013.png)

    /// caption
    进入地图按 F4
    ///

    ### 相机 mod 相关快捷键

    | 按键 | 作用 |
    | --- | --- |
    | ++f3++ | 开关拍摄宣传片用的滤镜 |
    | ++f4++ | 开关自由视角 |
    | ++f5++ | 开关法线模式，用来查看碰撞箱|
    | ++f6++ | 在清晨 / 傍晚之间切换 |
    | ++f7++ | 开关 GUI 显示 |

*[debugmode]: 用来开启Debug模式，开启后可以便使用自由视角以及相机mod。
*[no_simulation]: 取消渲染距离，所有东西都会在整张地图上计算并渲染，对性能损耗较大。
*[auto_update_tree_foliage]: 使树叶自动面向相机，防止你用各种角度查看时看到纸片树叶。
*[big_water]: 渲染整片水域，而不是只渲染相机附近的水面。
*[skip_nat_server_usage]: 这个是裸连国内服务器避免境外中转的，不用管。