---
title: 寫譯文
icon: lucide/languages
description: 指紋機制：譯文如何聲明自己所依據的原文，以及它為什麼會「過期」。
tags: ["i18n"]
# ⚠️ 由 tools/docsgen.py 從 content/guide/translating.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 寫譯文

<p class="kicker">TRANSLATING</p>

## 指紋，而不是清單

譯文不需要誰來登記。它在前置元數據裡**自己聲明依據的那份原文**：

```yaml
---
title: Getting started
description: ...
source_sha256: 3f9c…      # content/guide/getting-started.zh-hans.md 當時的 sha256
translated: 2026-01-01
---
```

默認語言那份一改，指紋就對不上，這一頁立刻被標成 `stale`（已過期）——
不必有人記得去通知譯者。

## 缺譯文的骨架可以自動生成

```bash
uv run python tools/i18n_check.py --sync    # 為缺失的譯文建立骨架
```

骨架裡寫着原文路徑與待填的指紋，也會帶上 `TODO` 佔位。體檢會一直報到它被填完為止。

!!! note "派生語種不走這套"
    `zh-hant` 沒有手寫源文件，由 `tools/hant.py` 從簡體腳本轉換而來，
    判據是「轉換結果是否與產物逐字節一致」。詳見[參考](../reference/front-matter.md)。
