---
nav_label: "准备工作"
title: "准备工作"
icon: "lucide/download"
description: "下载后的配置、与 RWR 文件夹同步、开启自带相机 mod，以及 OgreSDK 下载。"
# ⚠️ 由 tools/docsgen.py 从 content/prepare/index.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# 准备工作

## 一、地编下载后如何配置

1.将下载后的文件解压到你自己喜欢的路径。

![准备工作 1](../assets/shushu/001.png)

2.在1007_Data中创建一个templates文件夹与map文件夹。

![准备工作 2](../assets/shushu/002.png)

3.下载群内的最新模板，目前是vao0822.svg，放入地编的templates文件夹中。

> 注：目前只有原版正常地图模板，沙漠与雪地的模板暂未制作完成。

![准备工作 3](../assets/shushu/003.png)

4.选择你喜欢的地图放入地编的map文件夹里，注意只能选一个，并且将那个地图文件夹下所有的相关文件都扔进去，如果拿不准就扔map7，因为这就是上面模板的底稿，可以防止出现一些诡异问题。

> 注：RWR原版地图分为三个类型（原版中的原版、原版中的沙漠、原版中的雪地），用哪个类型就要装载对应的模板，目前只做了原版中的原版类型模板，所以只能使用\vanilla\maps中的文件，过于特殊的 map19与\vanilla.desert\maps路径和\vanilla.winter\maps路径中的地图可能会出现适配问题（当然不影响只是打开看看，但是以这些地图为底子去做还是算了）。

![准备工作 4](../assets/shushu/004.png)

![准备工作 5](../assets/shushu/005.png)

> *上面例子图我地编文件夹里一堆.meta文件用不着管，只是个示例，把左边的全扔右边地编文件夹里就行

## 二、如何同步地编与RWR的文件夹

1.首先Win+R，输入cmd打开命令提示符界面。

![准备工作 6](../assets/shushu/006.png)

![准备工作 7](../assets/shushu/007.png)

2.之后输入命令：

```text
mklink /J "你的小兵步枪要创建的地图文件夹" "地编的文件夹"
```

> 注：<br>每个人路径都不一样，按自己的来；<br>第一个文件夹路径需要保证输入命令前是未被创建的。

![准备工作 8](../assets/shushu/008.png)

3.完成后效果。

![准备工作 9](../assets/shushu/009.png)

## 三、如何开启RWR自带的相机mod

1.steam游戏库界面，在左侧列表找到右键RWR，打开属性，输入：

```text
skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
```

![准备工作 10](../assets/shushu/010.png)

2.打开游戏，点击开始新的快速比赛模式，然后点击加载模组。

![准备工作 11](../assets/shushu/011.png)

3.选中Camera mod。

![准备工作 12](../assets/shushu/012.png)

4.进入地图，按下F4动动鼠标看看有没有效果。

![准备工作 13](../assets/shushu/013.png)

其中：

F3是开关用于拍摄宣传片的滤镜

F4是开关自由视角

F5是开关法线模式，用于查看碰撞箱等

F6是切换到凌晨/傍晚

F7是开关GUI显示

## OgreSDK下载

![准备工作 14](../assets/shushu/014.png)

1.群文件下载OgreSDK_vc10_v1-7-4.zip，解压在自己喜欢的路径，推荐和地编文件夹一块。

![准备工作 15](../assets/shushu/015.png)

2.没了，之后3rdParSettings要用，现在先不说 :)
