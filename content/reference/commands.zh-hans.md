---
title: 命令与体检
icon: lucide/terminal
description: make 目标一览，以及三条构建后体检各自守什么。
tags: ["build"]
---

# 命令与体检

<p class="kicker">COMMANDS & CHECKS</p>

```bash
make gen      # content/ → docs/，并重新生成导航
make check    # 只跑翻译度体检
make links    # 只跑产物链接体检（需先构建）
make build    # 生成 → 构建 → 标签过滤 → 链接体检 → 翻译度体检
make serve    # 本地预览
make sync     # 为缺失的译文建立骨架，然后重新生成
make clean    # 删掉 site/
```

## 三条体检各自守什么

| 脚本 | 守的是 | 为什么源的校验看不到 |
| --- | --- | --- |
| `tools/linkcheck.py` | 站内引用、目录尾斜杠、跳转桩目标 | 这些都是构建后才定型的链接 |
| `tools/tagfilter.py` | 标签页只列本语言的篇目 | tags 插件按整个 `docs/` 扫描，没有语言概念 |
| `tools/i18n_check.py` | 漏翻 / 过期 / 结构对不上 / 产物缺件 | 需要同时看内容与产物 |

`i18n_check.py` 还会对构建产物做一组「该有的东西真的在」的断言（SMOKE）：
模板里的条件一旦恒为假，输出会**静默**少一块——不报错、不警告。
