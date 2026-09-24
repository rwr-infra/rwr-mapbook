---
title: 写内容
icon: lucide/pen-line
description: 前置元数据各字段的含义，以及导航为什么不需要单独维护。
tags: ["content"]
---

# 写内容

<p class="kicker">WRITING</p>

## 一篇内容长什么样

```markdown
---
title: 写内容
description: 一到两句，会进页面摘要与检索结果。
icon: lucide/pen-line
tags: ["content"]
---

# 写内容

正文……
```

## 导航不单独维护

导航的**唯一来源是内容本身**（见 `tools/navgen.py`）：

* **顺序**来自同目录 `index.md` 的 `nav:` 列表，列出子项的名字；
* **显示名**优先取 `nav_label`，其次 `title`，再次首个一级标题；
* 顶层目录的顺序来自 `docs/index.md` 的 `nav:`。

也就是说，**一个文件夹的全部导航元数据，就写在它自己的 `index.md` 里**。
`navgen.py` 会据此为每个目录写一个 `.nav.yml`——那是生成物，别手改。

不想占一格导航的页面（例如标签页），在前置元数据里写 `nav_hidden: true`。

## 链接怎么写

* 指向**站内页面**：写相对路径，例如 `[起步](getting-started.md)`。
  各语言目录结构镜像，所以这一条在三种语言里都成立，不用改写。
* 指向**共享资产**：`docs/assets/` 只有一份，三棵树共用。写相对路径即可，
  `docsgen.py` 会给非默认语言的产物自动多补一个 `../`。
