---
title: 命令與體檢
icon: lucide/terminal
description: make 目標一覽，以及三條構建後體檢各自守什麼。
tags: ["build"]
# ⚠️ 由 tools/docsgen.py 從 content/reference/commands.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 命令與體檢

<p class="kicker">COMMANDS & CHECKS</p>

```bash
make gen      # content/ → docs/，並重新生成導航
make check    # 只跑翻譯度體檢
make links    # 只跑產物鏈接體檢（需先構建）
make build    # 生成 → 構建 → 標簽過濾 → 鏈接體檢 → 翻譯度體檢
make serve    # 本地預覽
make sync     # 為缺失的譯文建立骨架，然後重新生成
make clean    # 刪掉 site/
```

## 三條體檢各自守什麼

| 腳本 | 守的是 | 為什麼源的校驗看不到 |
| --- | --- | --- |
| `tools/linkcheck.py` | 站內引用、目錄尾斜槓、跳轉樁目標 | 這些都是構建後才定型的鏈接 |
| `tools/tagfilter.py` | 標簽頁只列本語言的篇目 | tags 插件按整個 `docs/` 掃描，沒有語言概念 |
| `tools/i18n_check.py` | 漏翻 / 過期 / 結構對不上 / 產物缺件 | 需要同時看內容與產物 |

`i18n_check.py` 還會對構建產物做一組「該有的東西真的在」的斷言（SMOKE）：
模板裡的條件一旦恆為假，輸出會**靜默**少一塊——不報錯、不警告。
