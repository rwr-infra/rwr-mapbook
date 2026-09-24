---
nav_label: "准备工作"
title: "准备工作"
icon: "lucide/download"
description: "下载后的配置、与 RWR 文件夹同步、开启自带相机 mod，以及 OgreSDK 下载。"
tags: [安装与配置, 相机 mod]
---

# 准备工作 { #prepare }

<p class="kicker">PREPARE · 装好，然后才谈画图</p>

四件事，按顺序做完就能开工。前三件不做完，后面每一步都会卡住。

<div class="grid cards" markdown>

-   __1 · 配置地编__

    ---

    解压，建两个文件夹，把模板与地图放进去。

    [:octicons-arrow-right-24: 跳到这一节](#setup)

-   __2 · 同步文件夹__

    ---

    一条 `mklink` 命令，把地编直接接到 RWR 的地图目录上。

    [:octicons-arrow-right-24: 跳到这一节](#sync)

-   __3 · 开相机 mod__

    ---

    启动项里加一行，游戏里就能自由飞、切法线。

    [:octicons-arrow-right-24: 跳到这一节](#camera-mod)

-   __4 · 下 OgreSDK__

    ---

    现在用不上，等 3rdParSettings 要用时再回来。

    [:octicons-arrow-right-24: 跳到这一节](#ogresdk)

</div>

## 一、地编下载后如何配置 { #setup }

1. 将下载后的文件解压到你自己喜欢的路径。

    ![解压到任意路径](../assets/editor/001.png)

2. 在 `1007_Data` 中创建一个 `templates` 文件夹与 `map` 文件夹。

    ![建 templates 与 map 两个文件夹](../assets/editor/002.png)

3. 下载群内的最新模板（目前是 `vao0822.svg`），放进地编的 `templates` 文件夹中。

    ![把模板放进 templates](../assets/editor/003.png)

    !!! note "目前只有原版地图的模板"
        沙漠与雪地的模板暂未制作完成。

4. 选一个你喜欢的地图放进地编的 `map` 文件夹，**只能选一个**，并且要把那个地图
   文件夹下所有相关文件都扔进去。拿不准就用 `map7`——它就是上面那份模板的底稿，
   可以避开一些成因不明的问题。

    ![把地图文件放进 map](../assets/editor/004.png)

    ![放好之后的样子](../assets/editor/005.png)

    !!! warning "地图分三类，模板要对得上"
        RWR 原版地图分为三个类型：原版中的原版、原版中的沙漠、原版中的雪地。
        用哪个类型就要装对应的模板，而目前**只做了「原版中的原版」这一类**，
        所以只能用 `\vanilla\maps` 里的文件。

        `map19`、`\vanilla.desert\maps`、`\vanilla.winter\maps` 里的地图
        可能会有适配问题——打开看看不影响，但拿它们当底子做就算了。

    ??? quote "上面例图里的 .meta 文件"
        例图里地编文件夹中那一堆 `.meta` 不用管，只是示例。
        把左边的整个放进右边地编文件夹即可。

## 二、如何同步地编与 RWR 的文件夹 { #sync }

地编与游戏的目录分开管太麻烦，用一条符号链接把它们接在一起。之后在游戏里就能
直接玩到自己刚画的地图。

1. 按 ++win+r++，输入 `cmd`，打开命令提示符。

    ![Win+R 运行框](../assets/editor/006.png)

    ![输入 cmd](../assets/editor/007.png)

2. 输入下面这条命令：

    ```text
    mklink /J "你的小兵步枪要创建的地图文件夹" "地编的文件夹"
    ```

    !!! note "两个路径都要按自己的来"
        每个人的路径都不一样，按自己的填。这里用的是 `\J`——**目录联接**，
        不是 `\D` 的软链接；前者不要求管理员权限，跨盘符也没问题。

        第一个路径要保证**执行命令之前它不存在**，否则会报「文件已存在」。

    ![输入 mklink 命令](../assets/editor/008.png)

3. 完成后应该是这样：

    ![创建成功](../assets/editor/009.png)

## 三、如何开启 RWR 自带的相机 mod { #camera-mod }

相机 mod 是游戏自带的，只是默认不加载。开起来，进了地图就能自由飞。

1. 在 Steam 游戏库里右键 RWR → 属性，在**启动选项**里填入：

    ```text
    skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
    ```

    ![填启动选项](../assets/editor/010.png)

2. 打开游戏，点「开始新的快速比赛模式」，然后点「加载模组」。

    ![开始快速比赛](../assets/editor/011.png)

3. 选中 Camera mod。

    ![选中 Camera mod](../assets/editor/012.png)

4. 进入地图，按 ++f4++ 移动鼠标，看看有没有反应。

    ![进入地图按 F4](../assets/editor/013.png)

    | 按键 | 作用 |
    | --- | --- |
    | ++f3++ | 开关拍摄宣传片用的滤镜 |
    | ++f4++ | 开关自由视角 |
    | ++f5++ | 开关法线模式，用来查看[碰撞箱](#camera-mod "物件的碰撞体积；地编里靠它判断能不能站上去、能不能被打到") |
    | ++f6++ | 在凌晨 / 傍晚之间切换 |
    | ++f7++ | 开关 GUI 显示 |

    !!! tip "F5 是同一个键，两回事"
        在地编里 ++f5++ 是**刷新界面**，在相机 mod 里是**开法线模式**。
        取决于你现在在哪个窗口里。

## OgreSDK 下载 { #ogresdk }

现在用不到，等[3rdParSettings](../settings/third-party.md#third-party)要用的时候再回来。

![OgreSDK 包](../assets/editor/014.png)

1. 从群文件下载 `OgreSDK_vc10_v1-7-4.zip`，解压到自己喜欢的路径，
   推荐和地编文件夹放在一块。

    ![解压 OgreSDK](../assets/editor/015.png)

2. 就到这里。3rdParSettings 用到时再说。

*[模板]: 物件在 `template = …` 里引用的名字，地编里按这个名字找它
*[RWR]: Running With Rifles，小兵步枪
