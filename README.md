# RWR 地编手册

> 小兵步枪（Running With Rifles）地图编辑器的手册，三种语言各一份。

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
```

`make build` 的产物是一个纯静态目录 `site/`。

---

## 语言是怎么排的

网址只有语言一层前缀，**默认语言没有前缀**：

```
/                     简体（默认）      /en/                英文
/zh-hant/             繁体
/prepare/             简体 · 准备工作   /en/prepare/        英文
```

页眉上有一个下拉切换语言；它只改「语言」这一层前缀，页内路径原样带过去——
在 `/en/editor/keys/` 上切到繁体，落点是 `/zh-hant/editor/keys/`，不是首页。

判据只有一份：`overrides/partials/route.html`。它从 `page.url` 解析出语言目录，
语言清单从 `config.extra.alternate` 推导，不硬编码。**十来个模板里原先各写一遍的
`here[:3] == "en/"` 已经全部收拢过去**——那种写法在语言目录不止两三个字符时会
静默判错，把页面当成默认语言。

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

### 空侧栏会自己收掉

**左栏**铺的是「当前分区的其它页」。单页分区（`准备工作`、`关于`）与首页没有别的页可铺，
左栏是空的——空着也占 242px，正文被挤到 688px。

**右栏**铺的是这一页的二级标题。只有标题、没有小节的页面（`地编界面`、`交互按键表`、
那五张清单的首页）同样空着：主题会把唯一的 h1 剥掉，剩下的空目录照样渲染成一个
「目录」标签，点开只有它自己，却实打实占掉右侧那一列。

两条判据都放在构建层（`tools/docsgen.py` 的 `hide_sides()`），给该页的产物补一行
`hide: [navigation]`、`hide: [toc]` 或两者兼有。**不写在各页的前置元数据里**：
分区里加一篇新页、页里加一个小标题，侧栏该自己回来——写死在前置元数据里就不会，
而且每加一种语言、每个历史版都要各写一遍。

作者自己写了 `hide:` 的，这里不覆盖——那是有意为之，不是推导的结果。
`tools/i18n_check.py` 复核派生语种时要走同一条流水线，所以它调的是同一个
`hide_sides()`，判据只有一处。

### 缺页怎么办

不是每种语言都翻齐了：英文还差十几篇。
而语言切换器出现在**每一页**上，所以缺的那些页由 `tools/docsgen.py` 补一个
**跳转桩**（`<meta http-equiv="refresh">`）落到该语言的首页——而不是把读者送进 404。

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
| `zensical build --strict` | 断链、失效锚点 |

```bash
make check     # 翻译度体检
make links     # 链接体检（需先构建）
```

---

## 目录约定

```
content/              唯一手写层
docs/                 构建层（.md 与跳转桩是生成物）+ 手写资产
  assets/editor/      界面与流程的 54 张图
  assets/tables/      清单里的 705 张图
  stylesheets/ javascripts/   手写
  assets/fonts/       自托管字体

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
（`content/` 是唯一手写层、四种会非零码退出的体检）。
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

另外新增：`overrides/partials/route.html`（语言前缀的唯一判据）、
`translation_in_progress`（语种补齐进度这条刻意的放宽）、空侧栏的自动推导
（见上）、以及标题锚点的显式钉住。

---

## 换成你自己的内容

1. `content/` 下换成本站的内容，文件名带语言后缀；
2. `zensical.toml` 里改 `site_url` / `site_name` / `site_description` /
   `site_author` / `copyright`、`[project.extra]` 的多语言值；
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
