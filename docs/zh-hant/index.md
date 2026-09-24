---
nav_label: "首頁"
icon: "lucide/house"
description: "小兵步槍地圖編輯器手冊：地編界面逐項說明、模型與牆體清單、交互按鍵與常用流程。"
nav: ["prepare", "editor", "tables", "settings", "about"]
# ⚠️ 由 tools/docsgen.py 從 content/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [navigation]
---

# RWR 地圖編輯器手冊

<p class="kicker">RWR · 做地圖之前先看這一頁</p>

做地圖之前的準備工作——主要是把地編的交互體驗調順。

|  |  |
| --- | --- |
| 編輯日期 | 20260922 |
| 地編版本 | 0101 |
| 當前編輯者 | HamSter |

!!! warning "先說清楚這是什麼"
    這是**做圖的人寫給做圖的人看的**工作記錄，不是官方說明書。
    標着「待試」「沒試，不知道這是啥」的地方照原樣留着——那表示**還沒人試過**，
    不代表能用，也不代表不能用。

## 從哪裡開始

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } __剛拿到地編__

    ---

    解壓、配置、與 RWR 的文件夾同步，再把自帶的相機 mod 打開。

    [:octicons-arrow-right-24: 準備工作](prepare/index.md)

-   :material-cursor-default-click:{ .lg .middle } __界面上都是什麼__

    ---

    主界面各工具、交互按鍵、按 ID 找物件。

    [:octicons-arrow-right-24: 地編界面](editor/index.md)

-   :material-cube-outline:{ .lg .middle } __有哪些模型能擺__

    ---

    五張清單、七百多個物件，帶預覽圖與實測備註。

    [:octicons-arrow-right-24: 模型清單](tables/index.md)

-   :material-cog-outline:{ .lg .middle } __三個配置文件__

    ---

    mapSettings 管地圖本身，3rdParSettings 與 RefpM 管外部資源。

    [:octicons-arrow-right-24: 設置文件](settings/index.md)

</div>

## 這個站有兩條軸

**版本**決定你看到哪一份內容，**語言**決定用哪種文字讀。兩者互不幹涉：
換版本不會換語言，換語言也不會回版本。

| 軸 | 在頁眉哪一側 | 切換之後 |
| --- | --- | --- |
| 版本 | 左側的標簽圖標 | 只換版本，語言留着 |
| 語言 | 右側的翻譯圖標 | 只換語言，版本留着 |

版本這一格現在只有兩項：**地編版本 0101**（就是你在看的這份）與**彩蛋**。
彩蛋不是歷史版，是砍版機制的試用品——那一支裡凍着一份 060 版的構建數據。

[從準備工作開始](prepare/index.md){ .md-button .md-button--primary }
[直接翻模型清單](tables/index.md){ .md-button }

*[模板]: 物件在 `template = …` 裡引用的名字，地編裡按這個名字找它
