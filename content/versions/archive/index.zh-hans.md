---
nav_label: "快照首页"
title: "历史版快照（示例）"
icon: lucide/archive
description: "版本机制的一份示例快照：这一支的内容被冻结在砍版那一刻，之后不再回改。"
nav: ["prepare"]
---

# 历史版快照（示例）

<p class="kicker">ARCHIVE · 砍版那一刻的样子</p>

!!! warning "这一支是示例，不是某一版真实的说明"
    这里演示的是**版本机制**本身：历史版是砍版那一刻的一棵**冻结的树**，
    之后不再回改；读者按自己装的地编版本进来，看到的就是当时那份说明。

    编辑组砍出第一个真正的地编历史版时：把 `content/versions/archive/` 删掉，
    在 `zensical.toml` 的 `[[project.extra.version]]` 里把这一条换成真实的
    id / label / date 并新建对应目录即可。

## 这一支里有什么

只有[准备工作](../prepare/index.md)被冻进来了——其余页面在当前版里有、在这一版里没有，
`tools/docsgen.py` 会给它们各补一个跳转桩，把读者送到这一版的首页，
而不是让他点进 404。切到「地编版本 0101」再点顶栏的「地编界面」就能看到这个效果。
