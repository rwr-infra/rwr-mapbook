---
nav_label: "關於"
title: 關於這個模版
icon: lucide/info
description: 模版包含什麼、不包含什麼，以及它的取捨。
# ⚠️ 由 tools/docsgen.py 從 content/about/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 關於這個模版

<p class="kicker">ABOUT THIS TEMPLATE</p>

## 它給你什麼

* 一套**單一手寫層**的構建流水線：`content/` → `docs/` → `site/`；
* 三語骨架：默認語言手寫、譯文手寫並帶指紋、派生語言腳本轉換；
* 四條會以非零碼退出的體檢，可以直接掛在 CI 上；
* 主題覆蓋件：頁眉/頁腳/導航/麵包屑按頁面語言取文案，多語言切換器，
  同意表單，目錄尾斜槓補正。

## 它不給你什麼

* **內容**。這裡只有幾頁說明模版自身的示例，換掉即可。
* **主題配色與字體**。用的是 Zensical 默認主題；`docs/stylesheets/extra.css`
  只做了少量補充，字體與腳本全部自託管（不引任何第三方請求）。
* **部署**。`site/` 是純靜態目錄，交給你的靜態託管即可。

## 默認語言是哪一個

`tools/langs.py` 的 `DEFAULT_LANG`。默認語言的產物直接落在 `docs/` 根、
網址不帶前綴；其餘語言各佔一層子目錄。
