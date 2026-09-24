---
title: 写译文
icon: lucide/languages
description: 指纹机制：译文如何声明自己所依据的原文，以及它为什么会「过期」。
tags: ["i18n"]
# ⚠️ 由 tools/docsgen.py 从 content/guide/translating.zh-hans.md 生成，请勿手改；要改请改 content/ 下的源文件。
---

# 写译文

<p class="kicker">TRANSLATING</p>

## 指纹，而不是清单

译文不需要谁来登记。它在前置元数据里**自己声明依据的那份原文**：

```yaml
---
title: Getting started
description: ...
source_sha256: 3f9c…      # content/guide/getting-started.zh-hans.md 当时的 sha256
translated: 2026-01-01
---
```

默认语言那份一改，指纹就对不上，这一页立刻被标成 `stale`（已过期）——
不必有人记得去通知译者。

## 缺译文的骨架可以自动生成

```bash
uv run python tools/i18n_check.py --sync    # 为缺失的译文建立骨架
```

骨架里写着原文路径与待填的指纹，也会带上 `TODO` 占位。体检会一直报到它被填完为止。

!!! note "派生语种不走这套"
    `zh-hant` 没有手写源文件，由 `tools/hant.py` 从简体脚本转换而来，
    判据是「转换结果是否与产物逐字节一致」。详见[参考](../reference/front-matter.md)。
