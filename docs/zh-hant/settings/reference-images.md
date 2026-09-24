---
nav_label: "RefpM 說明"
title: "RefpM 說明"
icon: "lucide/image"
description: "用來加參考圖。"
# ⚠️ 由 tools/docsgen.py 從 content/settings/reference-images.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [toc]
---

# RefpM 說明（用來加參考圖） { #reference-images }

<p class="kicker">SETTINGS · 把底圖墊在地編裡</p>

做地圖時把一張衛星圖或手繪稿墊在下面，照着擺物件。用 **Import** 導入參考圖，
**Clear** 移除。

| 控件 | 作用 | 填什麼 |
| --- | --- | --- |
| `ScaleX` | 橫向壓縮或拉長參考圖 | 倍率。填 `0.5` 就是橫向壓到一半 |
| `ScaleY` | 縱向壓縮或拉長參考圖 | 倍率 |
| `OffsetX` | 橫向偏移參考圖 | 距離。X 軸向右增長 |
| `OffsetY` | 縱向偏移參考圖 | 距離。Y 軸向上增長 |
| `Alpha` | 更改參考圖透明度 | 向左淡化，向右實體化 |

!!! note "這張表裡改掉了兩處筆誤"
    原樣寫的是「OffsetX 與 OffsetX 其實是 Y 的作用」「向右軀體化」——
    從上下文看是筆誤，這裡按 `OffsetY` 與「實體化」寫。要改回去說一聲。
