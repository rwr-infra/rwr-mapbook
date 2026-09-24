# RWR 地编手册

> 小兵步枪（Running With Rifles）地图编辑器的手册，做成了一个**双轴**静态站：
> **版本**（你装的是哪一版地编）与**语言**（你用哪种文字读）互不干涉，各切各的。

内容只讲编辑器本身：准备工作、界面与工具、模型清单、配置文件。写法一个字没改——
标着「待试」的地方仍然标着（导航里挂「未完成」），「据说是这样」的说法也照原样留着。
**这份手册不替读者作判断。**

站点不署来源、不写「内部资料」：读者要的是「这个工具怎么用」，不是「这份笔记的来路」。

---

## 快速开始

```bash
uv sync --locked

make gen      # content/ → docs/，并重建导航
make serve    # 预览 http://127.0.0.1:8000/（根域）
make serve-subpath  # 同上，但按线上的子路径 /rwr-mapbook/ 预览

make build    # 生成 → 构建 → 标签过滤 → 链接体检 → 翻译度体检
make versions # 只看版本清单体检
```

`make build` 的产物是一个纯静态目录 `site/`。

---

## 两条切换轴

网址是两个正交维度的拼接，**版本在前、语言在后**：

```
/                     当前版 · 简体        /en/              当前版 · 英文
/egg/                 彩蛋 · 简体          /egg/en/          彩蛋 · 英文
/egg/zh-hant/         彩蛋 · 繁体
```

### 这个子路径是怎么回事

线上是 GitHub Pages 的**项目站**（仓库名不是 `<用户名>.github.io`），地址本来就是
`https://<用户名>.github.io/<仓库名>/`——**站点根落在那一层，不是域名根**。
所以 `zensical.toml` 里的 `site_url` 必须带着 `/rwr-mapbook/`：站内绝对引用、
sitemap、canonical 都按这个根拼；少了它，本地看着一切正常，一上线全是断链。
这一项不能按「本地预览方便」来取舍。

**但本地预览不该背这个包袱。** 默认的 `make serve` 会让预览停在根域：
它另生成一份 `zensical.preview.toml`（只把 `site_url` 换成本地根域，其余一行不动），
于是入口就是 `http://127.0.0.1:8000/`。那份文件是生成物、不入库，也改不到线上。

```bash
make serve           # http://127.0.0.1:8000/            ← 默认，根域，写文档时用这个
make serve-subpath   # http://127.0.0.1:8000/rwr-mapbook/ ← 核对线上子路径下的表现
```

要真的把站点挪到域名根（`https://<用户名>.github.io/`），得把仓库改名成
`<用户名>.github.io`，或配一个自定义域——那时 `site_url` 跟着去掉子路径即可。

页眉上有两个下拉，**各改一层前缀**：

| 切换器 | 改哪一层 | 保留哪一层 | 代码 |
| --- | --- | --- | --- |
| 版本 | `0101/` ↔ 无前缀 | 语言原样 | `overrides/partials/version.html` |
| 语言 | `en/` ↔ `zh-hant/` ↔ 无前缀 | 版本原样 | `overrides/partials/alternate.html` |

从 0101 版切到彩蛋那一支，读者留在同一种语言里；从简体切到英文，读者留在同一版里。
两层都改会一次把读者带走两格，那不是他点的。

判据只有一份：`overrides/partials/route.html`。它从 `page.url` 解析出版本与语言，
版本清单与语言目录都从配置推导，不硬编码。**十来个模板里原先各写一遍的
`here[:3] == "en/"` 已经全部收拢过去**——在 `archive/en/…` 这种网址上，
`here[:3]` 是 `arc`，那种判据会静默判错，把页面当成默认语言。

---

## 三种语言，两种来源

| | 来源 | 判据 | 手改哪里 |
| --- | --- | --- | --- |
| 简体 `zh-hans` | 手写 | —— | `content/**/*.zh-hans.md` |
| 英文 `en` | 手写译文 | 译文里记的 `source_sha256` 与原文对得上 | `content/**/*.en.md` |
| 繁体 `zh-hant` | 由简体**脚本转换** | 转换结果与产物**逐字节**一致 | 不要手改，改简体 |

繁体不是「第二种翻译」，是同一份文字的字符转写，所以它**不可能过期**。
转换规则见 [`tools/hant.py`](tools/hant.py) 开头的说明。

> ⚠️ **英文还没翻完。** 导航层（首页、五个分区首页、关于）已经译好，
> 13 篇正文还是骨架。这件事是**明说**的，不是藏着的：
> `zensical.toml` 里 `translation_in_progress = ["en"]` 声明了「这个语种还在补齐」，
> 于是它的「缺篇目 / 还是占位」只统计、不挡构建，而
> **「已过期 / 派生失同步 / 未记录指纹 / 结构待核」照样挡**。
>
> 这条界线是刻意的：「还没翻」是**看得见**的（那页就是没有），
> 「翻了但原文改了」才是**看不见**的——体检存在的理由始终是后者。
> 译完把 `en` 从那张名单里删掉，判据立刻回到全严。

---

## 版本是怎么一回事

版本是**冻结快照**，不是一份持续回改的文档：读者装的是哪一版地编，
就该看到哪一版当时的说明。

清单里现在只有两条：`0101`（当前版）与 `egg`（彩蛋）。机制留着，格子不必填满——
要放真正的历史版时按下面「加一个版本」加一条即可。

`egg` 那一支是砍版机制的**试用品**，也是本站的一枚彩蛋：里面只有一页
「谢谢」——写给做地图、试工具、记笔记的人。它同时证明这套机制是活的：
加一页、配一条 `[[project.extra.version]]`，切换器上就多一格，语言照常跟着走。

```
content/
  index.zh-hans.md          ← 当前版：就在 content/ 根下，网址没有前缀
  editor/ tables/ …
  versions/
    egg/                    ← 另一支：砍版那一刻那棵树的副本
      index.zh-hans.md        该支的首页
      egg.zh-hans.md          彩蛋页（「谢谢」）
```

对应产物：

```
docs/index.md               → /                （当前版 · 简体）
docs/en/index.md            → /en/
docs/egg/index.md           → /egg/
docs/egg/en/index.md        → /egg/en/
docs/egg/egg.md             → /egg/egg/
```

> ⚠️ **版本 id 不能长得像数字。** `0100`、`100`、`0` 这类 id 写进 `.nav.yml` 之后，
> YAML 会把光秃秃的值解析成**数字**，awesome-nav 拿到手的是一个数而不是目录名字符串，
> 于是找不到那棵树、退回成一个标量，最后以 `nav must be a list` 让整个构建失败。
> 诡异的是**只有一部分版本号中招**：`080`、`091` 里的 8、9 不是八进制数字，
> YAML 不认它是数，于是原样留着字符串、构建正常；`060`、`0100` 只含 0-7，构建就红。
> 所以 `tools/navgen.py` 的 `render()` 会把这类值**无条件加引号**再写出去，
> 并读回来比对一次。这条踩过一次，报错信息指不到原因。

### 加一个版本

1. 把当前版的内容复制成快照：`cp -r content/{index,editor,tables,…} content/versions/<id>/`
   （**不要**把 `content/versions/` 本身复制进去）；
2. 在 `zensical.toml` 的 `[[project.extra.version]]` 里加一条：

   ```toml
   [[project.extra.version]]
   id = "0102"
   label = "地编版本 0102"
   date = "2027-01-15"
   ```

3. `make build`。

判据由 `tools/versions.py` 的 `audit()` 守着：**声明了没有目录**、
**有目录没声明**、id 重复、一个 `current` 都没有、有多个 `current`——
每一条都以非零码退出，不会静默分成两家账。

> **非当前支的首页只写自己那一支里真的存在的页。** 本站的 `egg` 首页写的是
> `nav: ["egg"]`——它只列彩蛋那一页；`0101` 的那些分区它没有，写进去只会让 navgen
> 每次警告一行 `nav 中的 “about” 不存在，已跳过`（不报错，但把真告警淹掉）。
> 反过来，**首页自己不能写进 `nav:`**：`index` 是唯一一个「桩的落点等于首页」的名字，
> navgen 也把它当作页面名而不是条目名，写进去同样只会得到一行警告。
> 想让某一支的几节从导航里消失（那一支确实没有那些页），就干脆不写 `nav:`。

### 空侧栏会自己收掉

**左栏**铺的是「当前分区的其它页」。单页分区（`准备工作`、`关于`）与首页没有别的页可铺，
左栏是空的——空着也占 242px，正文被挤到 688px。

**右栏**铺的是这一页的二级标题。只有标题、没有小节的页面（`地编界面`、`交互按键表`、
那五张清单的首页）同样空着：主题会把唯一的 h1 剥掉，剩下的空目录照样渲染成一个
「目录」标签，点开只有它自己，却实打实占掉右侧那一列。

两条判据都放在构建层（`tools/docsgen.py` 的 `hide_sides()`），给该页的产物补一行
`hide: [navigation]`、`hide: [toc]` 或两者兼有。**不写在各页的前置元数据里**：
分区里加一篇新页、页里加一个小标题，侧栏该自己回来——写死在前置元数据里就不会，
而且每加一种语言、每个版本都要各写一遍。

作者自己写了 `hide:` 的，这里不覆盖——那是有意为之，不是推导的结果。
`tools/i18n_check.py` 复核派生语种时要走同一条流水线，所以它调的是同一个
`hide_sides()`，判据只有一处。

### 缺页怎么办

非当前那一支是冻结的，它的页面集合与当前版对不上是常态：当前版新加的分区，
那一支自然没有。而版本切换器出现在**每一页**上，所以缺的那些页由
`tools/docsgen.py` 补一个**跳转桩**（`<meta http-equiv="refresh">`）
落到该版本的首页——而不是把读者送进 404。`/egg/prepare/` 就是一个例子：
它没有那一页，于是桩把读者送回 `/egg/`。

桩是生成物，带生成横幅，由 `docsgen` 自己 prune；`tools/linkcheck.py` 会把它的
refresh 目标当成一条必须落地的引用去验。桩写成 HTML 而不是页面，是因为它要占住
`guide/index.md` 那种会建分区的位置，写成页面就会被 `navgen` 当成一个真的分区。

---

## 四条会挡住你的体检

前三条跑在**构建产物**上——源级校验看不到它们。

| 脚本 | 守什么 |
| --- | --- |
| [`tools/tagfilter.py`](tools/tagfilter.py) | 标签页只列本语言的篇目（tags 插件没有语言概念） |
| [`tools/linkcheck.py`](tools/linkcheck.py) | 站内引用落地、目录引用带尾斜杠、跳转桩目标存在、每页都带地址补正脚本 |
| [`tools/i18n_check.py`](tools/i18n_check.py) | 漏翻 / 过期 / 结构对不上 / 派生失同步 / 产物缺件（SMOKE 断言） |
| [`tools/versions.py`](tools/versions.py) | 版本清单与 `content/versions/` 对齐、版本条目里没有混进别处的配置 |
| `zensical build --strict` | 断链、失效锚点 |

```bash
make check     # 翻译度体检
make links     # 链接体检（需先构建）
make versions  # 版本清单体检
```

---

## 目录约定

```
content/              唯一手写层
  versions/<id>/      非当前版的冻结树
docs/                 构建层（.md 与跳转桩是生成物）+ 手写资产
  assets/editor/      界面与流程的 54 张图
  assets/tables/      清单里的 705 张图
  stylesheets/ javascripts/   手写
tools/                生成器与体检；langs.py 是语言清单的唯一出处
overrides/            主题模板覆盖
site/                 构建产物，不入库
.staging/             源文档抽取的中间产物，不入库
```

`docs/` 提交进仓库但它**是生成物**。构建直接读 `docs/`，改了 `content/` 却忘了
`make gen`，发出去的就是旧内容且**不会有任何报错**——`make build` 与 CI 都先跑生成，
就是为了堵这个缺口。

### 标题锚点钉住，别靠自动生成

需要被链接的标题（`主界面` 里那十六个小节、`准备工作` 的四节……）都写了显式 id：

```markdown
## WallE 说明 { #walle }
```

自动生成的 id 是**标题文字的变形**，靠不住：改一个空格，`#save说明` 就变成
`#save-说明`；繁体树上同一个标题还会被转写成 `#save說明`。凡是别处要链过去的标题，
都钉一个 ASCII 的 id，链接从此与排版和简繁转换都无关。

---

## 这个仓库对模版改了什么

本站基于 [`zensical-trilang-template`](https://github.com/bananaxiao2333/zensical-trilang-template)
（`content/` 是唯一手写层、四种会非零码退出的体检）。在它之上加了**版本轴**，
过程中在模版里翻出并修掉了四处**静默**缺陷——它们都不报错，只是悄悄发错东西：

1. **派生语种的共享资产链接少一层 `../`。**
   `docsgen.render()` 按**源文件**的语言算下沉层数，而源是简体（0 层）、产物是繁体（1 层）。
   模版自带的示例内容从没引用过 `assets/`，所以一直没暴露；本站第一张图就把它踩出来了。
   现在 `render()` 显式接收 `out_lang`。

2. **链接目标里的锚点不跟着简繁转写。**
   `hant.py` 为了保护路径，整段保住 `](…)`，于是 `](settings.md#save说明)` 里的锚点
   停在简体，而目标页的标题已经变成 `Save說明`、id 也就成了 `save說明`——
   繁体树上每一条指向中文标题的链接都落空，简体树上全都好好的。

3. **中文标题的锚点被整段丢掉。**
   Zensical 默认的 slugify 会把中日韩字符去掉：`## Save说明` → `#save`，
   纯中文标题 → `#_1`、`#_2`……目录锚点与 `toc.permalink` 因此形同虚设。
   已换成 `pymdownx.slugs.slugify`（Unicode 版），`## 一、地编下载后如何配置` →
   `#一地编下载后如何配置`。

4. **`linkcheck` / `i18n_check` 不认识 `site_url` 的子路径。**
   GitHub Pages 的项目站挂在 `/<repo>/` 下，模板的 `| url` 会生成
   `/repo/editor/` 这样的**绝对**地址，而它在站点目录里对应 `site/editor/index.html`。
   两个脚本原先一律按站点根去解，于是全站的绝对链接都被判成落空。子路径是部署形态，
   不是内容错误，判据现在跟着 `site_url` 走。

另外新增：`tools/versions.py`（版本清单与体检）、`overrides/partials/route.html`
（两条轴的唯一判据）、`overrides/partials/version.html`（版本切换器）、
`translation_in_progress`（语种补齐进度这条刻意的放宽）、空左栏的自动推导
（见上）、以及标题锚点的显式钉住。

---

## 换成你自己的内容

1. `content/` 下换成本站的内容，文件名带语言后缀；
2. `zensical.toml` 里改 `site_url` / `site_name` / `site_description` /
   `site_author` / `copyright`、`[project.extra]` 的多语言值、
   `[[project.extra.version]]` 的版本清单；
3. `docs/assets/` 换成本站的图；
4. `tools/i18n_check.py` 的 `SMOKE` 断言表指向**本站的固定页**
   （首页、`editor/index`、`editor/keys`），换内容结构时同步改；
5. `make build` 跑绿。

---

## 部署

!!! warning "本仓库**没有**部署"
    按需求撤掉了：GitHub Pages 站点已删除，`deploy` 分支已删除，
    `.github/workflows/deploy.yml` 也已从仓库移除。现在推 `main` 只会跑校验，
    不会发布任何东西。

`make build` 产出的 `site/` 是一个普通静态目录，与托管商无关。要重新发布时，
两件事：

1. 取回发布工作流——它在提交 `881ae35`（模版基线）里：

   ```bash
   git show 881ae35:.github/workflows/deploy.yml > .github/workflows/deploy.yml
   ```

   它在 CI 里跑完整条产线，然后把 `site/` 作为**一个全新的孤儿提交** force-push
   到 `deploy` 分支（每次都是新提交而不是追加，上一版才有的文件因此不会在线上
   阴魂不散）；
2. 在仓库设置里开启 Pages，来源选 `deploy` 分支。

也可以不用那条工作流：让托管商盯 `main`，构建命令填 `make gen && make build`、
输出目录填 `site` 即可。

`.github/workflows/docs.yml` 只做校验、**不发布**，挂在 push 与 PR 上——它一直留着。

> `zensical.toml` 里的 `site_url` 目前是 `https://bananaxiao2333.github.io/rwr-mapbook/`，
> 即带一个子路径（GitHub Pages 项目站）。换域名或换成用户站（`<user>.github.io`）时
> 要改它——`linkcheck` 与 `i18n_check` 都按它解析绝对链接。
