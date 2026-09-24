---
nav_label: "首頁"
icon: lucide/house
description: 一個開箱即用的 Zensical 三語文檔站模版：content/ 是唯一手寫層，其餘全部由腳本生成。
nav: ["guide", "reference", "about"]
# ⚠️ 由 tools/docsgen.py 從 content/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 三語文檔站模版

<p class="kicker">ZENSICAL · ZH-HANS / EN / ZH-HANT · STARTER</p>

這份模版把「一份內容、三種語言」做成了一條可維護的流水線：
**`content/` 是唯一手寫層**，`docs/` 下的 `.md` 全部由腳本生成，改內容不必碰構建產物。

!!! info "它主要解決一件事"
    多語言文檔站最常見的毛病是**譯文會悄悄過期**：默認語言改了，譯文還是舊的，
    而構建一路綠燈。這裡把「譯文過沒過期」變成一次會以非零碼退出的檢查。

## 三種語言，兩種來源

<div class="grid cards" markdown>

-   __默認語言：手寫__

    ---

    `content/**/*.zh-hans.md`，這是唯一需要人寫的東西。

    [:octicons-arrow-right-24: 從指南開始](guide/index.md)

-   __譯文：手寫 + 指紋__

    ---

    `content/**/*.en.md`，在前置元數據裡記下它所依據的原文指紋。

    [:octicons-arrow-right-24: 翻譯怎麼做](guide/translating.md)

-   __派生語言：腳本轉換__

    ---

    `zh-hant` 不是翻譯，是由簡體自動轉換而來，改不動也漏不掉。

    [:octicons-arrow-right-24: 查字段與命令](reference/index.md)

</div>

## 先跑起來

```bash
uv sync --locked     # 裝依賴（含 zensical 與 zhconv）
make gen             # 從 content/ 生成 docs/ 與導航
make serve           # 預覽 http://127.0.0.1:8000
```

構建產物在 `site/`，是純靜態目錄，交給任何靜態託管即可。
