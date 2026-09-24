---
title: 寫內容
icon: lucide/pen-line
description: 前置元數據各字段的含義，以及導航為什麼不需要單獨維護。
tags: ["content"]
# ⚠️ 由 tools/docsgen.py 從 content/guide/writing.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 寫內容

<p class="kicker">WRITING</p>

## 一篇內容長什麼樣

```markdown
---
title: 寫內容
description: 一到兩句，會進頁面摘要與檢索結果。
icon: lucide/pen-line
tags: ["content"]
---

# 寫內容

正文……
```

## 導航不單獨維護

導航的**唯一來源是內容本身**（見 `tools/navgen.py`）：

* **順序**來自同目錄 `index.md` 的 `nav:` 列表，列出子項的名字；
* **顯示名**優先取 `nav_label`，其次 `title`，再次首個一級標題；
* 頂層目錄的順序來自 `docs/index.md` 的 `nav:`。

也就是說，**一個文件夾的全部導航元數據，就寫在它自己的 `index.md` 裡**。
`navgen.py` 會據此為每個目錄寫一個 `.nav.yml`——那是生成物，別手改。

不想佔一格導航的頁面（例如標簽頁），在前置元數據裡寫 `nav_hidden: true`。

## 鏈接怎麼寫

* 指向**站內頁面**：寫相對路徑，例如 `[起步](getting-started.md)`。
  各語言目錄結構鏡像，所以這一條在三種語言裡都成立，不用改寫。
* 指向**共享資產**：`docs/assets/` 只有一份，三棵樹共用。寫相對路徑即可，
  `docsgen.py` 會給非默認語言的產物自動多補一個 `../`。
