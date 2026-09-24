---
nav_label: "首页"
icon: lucide/house
description: 一个开箱即用的 Zensical 三语文档站模版：content/ 是唯一手写层，其余全部由脚本生成。
nav: ["guide", "reference", "about"]
# ⚠️ 由 tools/docsgen.py 从 content/index.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# 三语文档站模版

<p class="kicker">ZENSICAL · ZH-HANS / EN / ZH-HANT · STARTER</p>

这份模版把「一份内容、三种语言」做成了一条可维护的流水线：
**`content/` 是唯一手写层**，`docs/` 下的 `.md` 全部由脚本生成，改内容不必碰构建产物。

!!! info "它主要解决一件事"
    多语言文档站最常见的毛病是**译文会悄悄过期**：默认语言改了，译文还是旧的，
    而构建一路绿灯。这里把「译文过没过期」变成一次会以非零码退出的检查。

## 三种语言，两种来源

<div class="grid cards" markdown>

-   __默认语言：手写__

    ---

    `content/**/*.zh-hans.md`，这是唯一需要人写的东西。

    [:octicons-arrow-right-24: 从指南开始](guide/index.md)

-   __译文：手写 + 指纹__

    ---

    `content/**/*.en.md`，在前置元数据里记下它所依据的原文指纹。

    [:octicons-arrow-right-24: 翻译怎么做](guide/translating.md)

-   __派生语言：脚本转换__

    ---

    `zh-hant` 不是翻译，是由简体自动转换而来，改不动也漏不掉。

    [:octicons-arrow-right-24: 查字段与命令](reference/index.md)

</div>

## 先跑起来

```bash
uv sync --locked     # 装依赖（含 zensical 与 zhconv）
make gen             # 从 content/ 生成 docs/ 与导航
make serve           # 预览 http://127.0.0.1:8000
```

构建产物在 `site/`，是纯静态目录，交给任何静态托管即可。
