# Zensical 三语文档站模版

> 一个开箱即用的**三语静态文档站**骨架：简体中文手写、英文手写并带指纹、
> 繁体由脚本从简体转换而来。**`content/` 是唯一手写层**，`docs/` 下的每一篇
> 都是生成的。
>
> 它主要解决一件事：**译文会悄悄过期**。默认语言改了，译文还是旧的，构建一路绿灯。
> 这里把「译文过没过期」变成一次会以非零码退出的检查。

---

## 快速开始

```bash
# 需要 Python ≥ 3.14 与 uv
uv sync --locked

make gen      # content/ → docs/，并重新生成导航
make serve    # 预览 http://127.0.0.1:8000

make build    # 生成 → 构建 → 标签过滤 → 链接体检 → 翻译度体检
```

`make build` 的产物是**一个纯静态目录** `site/`，交给任何静态托管即可。

---

## 它长什么样

```
content/     唯一手写层。文件名带语言后缀
  index.zh-hans.md      ┐
  index.en.md           ┴─ 同一篇的两个语种
  guide/
    index.zh-hans.md    ← 这个目录的导航元数据也写在这里
    getting-started.zh-hans.md

docs/        构建层。.md 与 .nav.yml 都是生成物
  index.md              ← 默认语言，网址不带前缀
  en/index.md
  zh-hant/index.md
  assets/               ← 共享资产，三棵树共用一份
  stylesheets/          ← 手写
  javascripts/          ← 手写

tools/       生成器与体检（纯标准库 + pyyaml + zhconv）
overrides/   主题模板覆盖
site/        构建产物（不入库）
```

## 三种语言，两种来源

| | 来源 | 判据 | 手改哪里 |
| --- | --- | --- | --- |
| 简体 `zh-hans` | 手写 | —— | `content/**/*.zh-hans.md` |
| 英文 `en` | 手写译文 | 译文里记的 `source_sha256` 与原文对得上 | `content/**/*.en.md` |
| 繁体 `zh-hant` | 由简体**脚本转换** | 转换结果与产物**逐字节**一致 | 不要手改，改简体 |

派生语言不是「第二种翻译」，是同一份文字的字符转写，所以它**不可能过期**。
哪些字不转（反引号里的文件名、链接目标）、哪些古体异写要归一，
见 [`tools/hant.py`](tools/hant.py) 开头的说明。

## 加一种语言

语言清单**从 `content/` 的文件名后缀推导**（见 [`tools/langs.py`](tools/langs.py)），
没有一份需要手工维护的语言列表。所以加一种语言分两步：

1. 在 `content/` 里给它写**至少一篇**——一门语言的存在与否由文件说了算；
2. `uv run python tools/i18n_check.py --sync` 会把其余缺失篇目的骨架补齐。

> **删掉某语言的全部内容，那门语言就消失了。** 这是推导式设计的代价，
> 也是它的好处：不存在「配置里写着 en，但一篇英文也没有」这种半死状态。

再加一门**派生**语言（脚本转换，如简体 → 繁体），改 `tools/langs.py` 的
`DERIVATIONS` 与转换函数即可；其余脚本都会跟着走。

---

## 四条会挡住你的体检

前三条都跑在**构建产物**上——源的校验看不到它们。

| 脚本 | 守什么 | 为什么必须在构建之后 |
| --- | --- | --- |
| [`tools/tagfilter.py`](tools/tagfilter.py) | 标签页只列本语言的篇目 | tags 插件按整个 `docs/` 扫描，没有语言概念 |
| [`tools/linkcheck.py`](tools/linkcheck.py) | 站内引用落地、目录引用带尾斜杠、跳转桩目标存在、每页都带目录地址补正脚本 | 这些都是构建后才定型的链接 |
| [`tools/i18n_check.py`](tools/i18n_check.py) | 漏翻 / 过期 / 结构对不上 / 产物缺件（SMOKE 断言） | 要同时看内容与产物 |
| `zensical build --strict` | 断链、失效锚点 | 源级校验 |

`i18n_check` 的**结构比对**值得单独说：它不数字符，而是比标题层级序列、
表格行数、提示框数、卡片数、代码块数、图片数与链接集合。漏掉一整段、
少一行表格、把提示框写成普通段落，都拦得住——这些光看「翻译进度 100%」是看不见的。

```bash
make check    # 只跑翻译度体检
make links    # 只跑链接体检（需先构建）
```

---

## 前置元数据

写在 `content/**/*.md` 顶部。完整字段表见站点里的「参考 → 前置元数据」一页，
这里只列容易踩的几条：

* **`nav` 只写在 `index.md` 里** —— 它定义的是「本目录子项的顺序」。
  一个文件夹的全部导航元数据，就写在它自己的 `index.md` 里，
  不需要另维护一份导航配置。
* **`tags` 用语言中立的标识符**（日期、代号）。各语言各写一套标签，
  横向的线索一换语言就断。
* **译文的 `source_sha256` 是必填的**。它由 `--sync` 自动写入；
  手抄一份译文时得自己算：`shasum -a 256 content/<路径>.zh-hans.md`。

---

## 多语言文案放在哪里

Zensical 里 `site_name` / `copyright` / `site_description` 这类配置是**全站唯一**的，
而本站三种语言共用一次构建。所以其余语言的值放在 `zensical.toml` 的
`[project.extra]` 里，**键名加后缀**取用（默认语言留空）：

```toml
site_name         = "文档站模版"
site_name_en      = "Docs Template"
site_name_zh_hant = "文檔站模版"
```

模板里统一这么取：

```jinja
{% set site_name = config.extra["site_name" ~ L] | d(config.site_name, true) %}
```

`L` 由页面语言决定（默认语言 `""`、英文 `"_en"`、繁体 `"_zh_hant"`），
见 [`overrides/main.html`](overrides/main.html) 开头那三行。

> 后缀用**下划线**而不是连字符，因为语言代码里本来就有连字符
> （`zh-hant` → `_zh_hant`）。

---

## 本模板的几条硬规矩

这几条都有代价，是踩过之后才立的：

**1. `docs/` 提交进仓库，但它是生成物。**
构建直接读 `docs/`，所以改了 `content/` 却忘了 `make gen`，发出去的就是旧内容——
而且**不会有任何报错**。`make build` 与 CI 都先跑生成，就是为了堵这个缺口。

判据是文件里那行生成横幅（「由 tools/docsgen.py 生成，请勿手改」），
不另存一份清单：两份记录会分叉，一份不会。手写的 `docs/**/*.md` 不带横幅，
因此不会被误认领、也不会被 prune 删掉。

**2. 链接与路径的两种写法。**
指向**站内页面**用相对路径（各语言目录结构镜像，三语通用）；
指向**共享资产**也写相对路径，`docsgen.py` 会给非默认语言的产物多补一层 `../`。
后者容易忘，所以 `linkcheck.py` 会逐页解析每一条 `href`/`src` 验它落地。

**3. 目录地址的尾斜杠。**
「少一个斜杠」的目录地址会让页面内的相对链接全部解析错位。
站点自己只生成带斜杠的地址，同时每一页都挂一小段脚本把地址栏补正
（理由与取舍见 [`overrides/partials/trailing-slash.html`](overrides/partials/trailing-slash.html)）。
`linkcheck.py` 两条都守着。

**4. 不引任何第三方请求。**
字体、样式、脚本全部自托管，`zensical.toml` 里 `theme.font = false`，
图片灯箱用的是站内副本。同意表单因此**一个勾选项都没有**——
把不存在的东西列进同意表单，才是真正的不诚实。
代价是：灯箱与字体文件要跟着主题升级手动同步，见 `zensical.toml` 里的注释。

---

## 换成你自己的内容

1. 删掉 `content/` 下全部示例，写你自己的默认语言版本；
2. `zensical.toml` 里改 `site_url` / `site_name` / `site_description` /
   `site_author` / `copyright`，以及 `[project.extra]` 的多语言值；
3. 把 `docs/assets/` 换成你自己的图；需要的话在 `[project.theme]` 里
   打开 `logo` 与 `favicon`；
4. `tools/i18n_check.py` 里的 `SMOKE` 断言表指向**示例内容**，
   换内容时同步改（它检查的是「这几页上该有的东西真的在」）；
5. `make build` 跑绿。

`TRANSLATION-GUIDE.md` 是译文的写作与验收规范，里面标了几处 `⚠️` 要你替换的示例。

---

## 部署

`make build` 产出的 `site/` 是纯静态目录，与托管商无关。两种常见接法：

**A. 由托管商构建** —— 让它盯 `main`，构建命令填 `make gen && make build`，
输出目录填 `site`。前提是那台构建机能装 Python 与 uv（很多只预装 Node）。

**B. 在 CI 里构建，产物推一个分支** —— 构建环境你说了算，托管商只管搬运。
本模板带了这样一个工作流：

```
main ──push──► .github/workflows/deploy.yml
                 ├─ gen → zensical build → tagfilter → linkcheck → i18n_check
                 └─ 把 site/ 的成品 force-push 到 deploy 分支（永远只有一个提交）
                                    │
                                    ▼
                托管商盯 deploy 分支，编译命令与安装命令都留空
```

`.github/workflows/docs.yml` 只做校验、**不发布**，挂在 push 与 PR 上。

> 产物推分支时每次都用**一个全新的孤儿提交**再 `-f` 强推，而不是往旧分支上追加：
> 追加的话，上一版才有的文件会永远留在线上。

---

## 目录约定速查

```
content/          唯一手写层
docs/             构建层（生成）+ 手写资产
  assets/         共享资产，三棵树共用
  stylesheets/    手写
  javascripts/    手写
tools/            langs.py 是语言清单的唯一出处
overrides/        主题模板覆盖（见下）
site/             构建产物，不入库
```

`overrides/` 里每个文件开头都写明了**它与主题原版的差异**，
以及主题升级时需要同步什么。改这些文件之前先读那段注释。
