---
nav_label: "快照首頁"
title: "歷史版快照（示例）"
icon: lucide/archive
description: "版本機制的一份示例快照：這一支的內容被凍結在砍版那一刻，之後不再回改。"
nav: ["prepare"]
# ⚠️ 由 tools/docsgen.py 從 content/versions/archive/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 歷史版快照（示例）

<p class="kicker">ARCHIVE · 砍版那一刻的樣子</p>

!!! warning "這一支是示例，不是某一版真實的說明"
    這裡演示的是**版本機制**本身：歷史版是砍版那一刻的一棵**凍結的樹**，
    之後不再回改；讀者按自己裝的地編版本進來，看到的就是當時那份說明。

    編輯組砍出第一個真正的地編歷史版時：把 `content/versions/archive/` 刪掉，
    在 `zensical.toml` 的 `[[project.extra.version]]` 裡把這一條換成真實的
    id / label / date 並新建對應目錄即可。

## 這一支裡有什麼

只有[準備工作](../prepare/index.md)被凍進來了——其餘頁面在當前版裡有、在這一版裡沒有，
`tools/docsgen.py` 會給它們各補一個跳轉樁，把讀者送到這一版的首頁，
而不是讓他點進 404。切到「地編版本 0101」再點頂欄的「地編界面」就能看到這個效果。
