---
nav_label: "首页"
icon: "lucide/house"
description: "小兵步枪地图编辑器手册：地编界面逐项说明、模型与墙体清单、交互按键与常用流程。"
nav: ["prepare", "editor", "tables", "settings", "download", "about"]
# ⚠️ 由 tools/docsgen.py 从 content/index.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
hide: [navigation]
---

# RWR 地图编辑器手册

<p class="kicker">RWR · 做地图之前先看这一页</p>

做地图之前的准备工作——主要是把地编的交互体验调顺。

|  |  |
| --- | --- |
| 编辑日期 | 20260922 |
| 地编版本 | 0101 |
| 当前编辑者 | HamSter |

!!! warning "先说清楚这是什么"
    这是**做图的人写给做图的人看的**工作记录，不是官方说明书。
    标着「待试」「没试，不知道这是啥」的地方照原样留着——那表示**还没人试过**，
    不代表能用，也不代表不能用。

## 从哪里开始

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __刚拿到地编__

    ---

    解压、配置、与 RWR 的文件夹同步，再把自带的相机 mod 打开。

    [:octicons-arrow-right-24: 准备工作](prepare/index.md)

-   :material-cursor-default-click:{ .lg .middle } __界面上都是什么__

    ---

    主界面各工具、交互按键、按 ID 找物件。

    [:octicons-arrow-right-24: 地编界面](editor/index.md)

-   :material-cube-outline:{ .lg .middle } __有哪些模型能摆__

    ---

    五张清单、六百多个物件，带预览图与实测备注。

    [:octicons-arrow-right-24: 模型清单](tables/index.md)

-   :material-cog-outline:{ .lg .middle } __三个配置文件__

    ---

    mapSettings 管地图本身，3rdParSettings 与 RefpM 管外部资源。

    [:octicons-arrow-right-24: 设置文件](settings/index.md)

</div>

## 这个站有两条轴

**版本**决定你看到哪一份内容，**语言**决定用哪种文字读。两者互不干涉：
换版本不会换语言，换语言也不会回版本。

| 轴 | 在页眉哪一侧 | 切换之后 |
| --- | --- | --- |
| 版本 | 左侧的标签图标 | 只换版本，语言留着 |
| 语言 | 右侧的翻译图标 | 只换语言，版本留着 |

版本这一格现在只有两项：**地编版本 0101**（就是你在看的这份）与**彩蛋**。
彩蛋不是历史版，是砍版机制的试用品——那一支里只有一页话<span class="redact" tabindex="0">，想说给一些人听</span>。

[从准备工作开始](prepare/index.md){ .md-button .md-button--primary }
[直接翻模型清单](tables/index.md){ .md-button }

*[模板]: 物件在 `template = …` 里引用的名字，地编里按这个名字找它
