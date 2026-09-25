# RWR 地编手册

> 小兵步枪（Running With Rifles）地图编辑器的手册，做成了一个**双轴**静态站：
> **版本**（你装的是哪一版地编）与**语言**（你用哪种文字读）互不干涉，各切各的。

内容只讲编辑器本身：准备工作、界面与工具、模型清单、配置文件。
事实、数字与结论一条没动：标着「待试」的地方仍然标着（导航里挂「未完成」），
作者没验证过的地方照旧写「未逐项验证」。**这份手册不替读者作判断。**

措辞按说明书的口吻统一过一遍；作者的私房话、吐槽与网络梗（原先混在正文里）
改成**点一下才展开的遮挡块**——表格里是行内黑块（`.redact`），
独立成段的是折叠框（`???`）。点开仍能看到原话，读者据此照样判断得出作者当时有多确定。

站点不署来源、不写「内部资料」：读者要的是「这个工具怎么用」，不是「这份笔记的来路」。

---

## 快速开始

```bash
uv sync --locked

make gen      # content/ → docs/，并重建导航
make serve    # 预览 http://127.0.0.1:8000/（根域）
make watch    # 另开一个终端：改 content/ 就自动重新生成（配合 make serve = 存盘即见）

make build    # 生成 → 构建 → 链接体检 → 翻译度体检
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

### 站点根在哪儿

线上是 `https://rwrme.rwr-infra.uk/`——**域名根**，网址里没有子路径那一层。
`zensical.toml` 里的 `site_url` 必须与它一致：站内绝对引用、sitemap、canonical
都按这个根拼，少了那一层或多了那一层，本地看着一切正常，一上线就是断链。
这一项不能按「本地预览方便」来取舍。

页脚底栏另有一条**文档仓库**入口（`footer_repo_url`）：页眉那个指向地编程序的
仓库（读者要下载、要提 issue 的是那个），页脚这个指向这份手册自己——
谁发现哪句话写错了、哪张表缺了一行，顺着它就能找过来改。两个入口各服务一种人。

（本站以前挂在 GitHub Pages 的项目站上，地址是 `…github.io/rwr-mapbook/`，
那时要另生成一份只换 `site_url` 的预览配置才好在本地按根域看。挪到自有域名之后
那份配置没用了，已删掉：现在 `make serve` 直接用配置里的 `site_url`，入口就是
`http://127.0.0.1:8000/`。哪天真挪回子路径下，把模版仓库里那份 sed 生成预览配置的
办法拿回来即可。）

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

> ✅ **三种语言现在都是全的。** 19 篇当前版正文都有手写英文译文，21 篇简体的
> 繁体转写逐字节对得上，全站还有两条例行抽检（产物抽样、卡片块形态）；
> 42 个条目全部 `已同步`，`translation_in_progress` 已清空，
> 判据回到全严：漏翻、过期、结构对不上，任意一条都挡构建。
>
> 这张名单是**预留的口子**，不是历史包袱。要再开一个语种、又不想一次翻完时：
> 把语种代号写进 `zensical.toml` 的 `translation_in_progress`，它的
> 「缺篇目 / 还是占位 / 刚建骨架」就只统计不挡构建，而
> **「已过期 / 派生失同步 / 未记录指纹 / 结构待核」照样挡**。
>
> 这条界线是刻意的：「还没翻」是**看得见**的（那页就是没有），
> 「翻了但原文改了」才是**看不见**的——体检存在的理由始终是后者。
> 译完把语种从那张名单里删掉，判据立刻回到全严。

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

## 历史版本归档放在站外

```
content/download/index.<lang>.md        页面：版本、文件名、大小、一条直链（手写）
assets.rwr-infra.uk/rwrme-web-assets/   归档本体（对象存储，不在仓库里）
```

十份整包一共 318 MB，**不在这个仓库里**，也不进站点的构建产物。理由很直接：
这个仓库里会变的是正文；带着归档走的话，每个想改一个字的人 `git clone`
都要先拉几百 MB。所以它们放在 **Cloudflare R2** 上，由 `assets.rwr-infra.uk`
这个域提供，页面上是直链。

公开地址的形状是固定的：

```
https://assets.rwr-infra.uk/rwrme-web-assets/<文件名>
```

三条约定：

* **对象名就是原文件名**（`060.zip`、`OgreSDK_vc10_v1-7-4.zip`），不带版本目录——
  名字本身已经唯一，多套一层只会在换存储时多一处要改的地方；
* **长缓存**：`Cache-Control: public, max-age=31536000, immutable`。归档是冻结的，
  同名文件永远同一个内容，所以能这么写；
* **哈希只写一处**：`content/download/index.<lang>.md` 那张表下面有一份 sha256 清单，
  读者下完能自己核。存储那边不另存一份「清单文件」——两份记录会分叉，一份不会。

### 为什么不用原先那套「分片 + 页面拼装」

本站原先把整包切成分片放进仓库，由页面取回、逐片校验、拼成一个整包再保存——
那是因为 EdgeOne Pages **单个文件最大 25 MB**，26–84 MB 的整包传不上去。
那条路的问题不在实现，而在位置：**把托管方的单文件上限，变成了读者的下载方式。**
拼装走的是 `blob:` 地址，那是页面进程内存里的临时句柄，别的程序拿不到——
所以超过上限的包只能挂在浏览器里下，下载器按不动。

挪到对象存储之后这个上限不存在了（R2 的单文件上限远高于这几百 MB），
于是分片、拼装脚本、清单文件、`make archives` / `make downloads` 一起删掉了：
页面上就是十条直链，浏览器能下，IDM / aria2 / 迅雷也能下，还支持断点续传
（`Range` 请求，实测返回 206）。

代价是**多了一处站外依赖**：那份存储要一直在。换域名或换存储商时，
改 `content/download/index.<lang>.md` 里那十条地址即可，其余地方不认这个域名。
（切分与拼装那两个件留在模版仓库里，真需要时能取回来。）

### 往上放新文件

走 S3 兼容接口（R2 的 endpoint + 一对 access key，`boto3` / `rclone` / `aws-cli`
都能用；密钥在 Cloudflare 面板上，**不要写进仓库**）。顺序是：

1. 先算本地文件的 sha256，与页面上写的那一份对上再传——传错文件是这里唯一
   会静默出错的地方；
2. `Content-Type` 按类型给（`.zip` → `application/zip`、`.rar` → `application/vnd.rar`、
   `.svg` → `image/svg+xml`），`Cache-Control` 按上面的长缓存给；
3. 传完 HEAD 一下：大小对不对、公开地址能不能取到；
4. 改了文件才动页面上的哈希；没改文件就别动——归档是冻结的。

---

## 加一种语言

**只需要动 `zensical.toml`。** 模板、脚本里都不再写死语言名：

1. `[[project.extra.alternate]]` 加一条：`name`（显示名，如「日本語」）、
   `link`（网址前缀，如 `ja/`）、`lang`（BCP-47，如 `ja`）。页眉的语言切换器、
   404 页的语言列表、`og:locale:alternate`、搜索面板的语言分段**全都读这一条**；
2. 给已有的那几组多语言文案补 `_<lang>` 后缀的键（页脚三段、同意按钮、
   搜索面板的 `search_*` 等）；
3. `lang_pack_<lang>`：主题的界面文案包名（`partials/languages/<包>.html`）。
   这是**唯一没有推导规则**的一处——主题把简体那一包叫 `zh` 而不是 `zh-Hans`，
   MiniJinja 的 `import` 又不支持 `ignore missing`，所以只能显式给出包名；
4. 内容层按 `content/**/*.<lang>.md` 放文件即可（`tools/langs.py` 从文件名后缀推导）；
   要脚本转换而不是手写译文的话，在 `tools/langs.py` 的 `DERIVATIONS` 里登记一条。

---

## 三条会挡住你的体检

前两条跑在**构建产物**上——源级校验看不到它们。

| 脚本 | 守什么 |
| --- | --- |
| [`tools/linkcheck.py`](tools/linkcheck.py) | 站内引用落地、目录引用带尾斜杠、跳转桩目标存在、每页都带地址补正脚本 |
| [`tools/i18n_check.py`](tools/i18n_check.py) | 漏翻 / 过期 / 结构对不上 / 派生失同步 / 产物缺件（SMOKE 断言） |
| [`tools/versions.py`](tools/versions.py) | 版本清单与 `content/versions/` 对齐、版本条目里没有混进别处的配置 |
| `zensical build --strict` | 断链、失效锚点 |

```bash
make check     # 翻译度体检
make links     # 链接体检（需先构建）
make versions  # 版本清单体检
```

站外那十条直链不在体检范围内：它们指到别的域上（`assets.rwr-infra.uk`），
构建期够不着。所以改过下载页之后要**手工点一遍**——`linkcheck` 只验站内的东西。

---

## 目录约定

```
content/              唯一手写层
  versions/<id>/      非当前版的冻结树
  download/           历史版本那一页（归档本体在站外，见上）
docs/                 构建层（.md 与跳转桩是生成物）+ 手写资产
  assets/editor/      界面与流程的 54 张图
  assets/tables/      清单里的 705 张图
  stylesheets/ javascripts/   手写
tools/                生成器、看门脚本与体检；langs.py 是语言清单的唯一出处
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

## 与模版的关系

本站基于 [`zensical-trilang-template`](https://github.com/bananaxiao2333/zensical-trilang-template)。
两边现在是**同步**的：版本轴、两条轴共用的判据 `overrides/partials/route.html`、
版本切换器、按（版本，语言）生成的标签索引、离线打包、大文件归档那套工具，
以及这份 README 之外的踩坑记录（模版仓库的 `LESSONS.md`），模版那边都有；
本站是它的一个实例——内容是本站的，配置是本站的，归档放在站外。

**当初这些东西是从五处静默缺陷上踩出来的**，它们都不报错，只是悄悄发错东西
（模版现已一并修掉，细节见 `LESSONS.md`）：

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

5. **语言树下的分栏导航一份都没生成，英文区只好按字母序排。**
   `navgen.targets()` 遍历每棵树时要剪掉「别的树根」，早先写的是「不等于自己」——
   站根因此把 `docs/en/editor/` 这类目录也当成别的树剪掉了（站根确实是它上级，
   但上级不是障碍）。于是语言树下一个 `.nav.yml` 都没写出来，awesome-nav 自己去扫目录：
   英文左栏的条目按字母序排、标题还全是中文占位符。判据改成「这个目录在别的树**下面**」。

其余几处都是「用不上就不碍事」的形状：归档那套工具（`chunker.py` 与页面拼装脚本）
现在只留在模版里，本站不用——归档搬到站外了（见「历史版本归档放在站外」）。

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

`make build` 产出的 `site/` 是一个普通静态目录，与托管商无关。线上由
**EdgeOne Pages** 托管，链路是：

```
main ──push──► .github/workflows/deploy.yml
                 ├─ 与 make build 同一条产线：gen → build → linkcheck → i18n
                 └─ 把 site/ 的成品 force-push 到 deploy 分支（永远只有一个提交）
                                    │
                                    ▼
                 EdgeOne Pages 的 Production 环境盯 deploy 分支，只管搬运
```

**EdgeOne 那侧不构建。** 项目设置里编译命令与安装命令都留空；若留空仍会去跑
`npm install`，就显式写成 `echo "产物分支，无需构建"`。输出目录留空（分支根目录
就是站点根），Production 环境的分支关联选 `deploy`。

这么分的理由：本站是 Python 站点（uv + Zensical），而 EdgeOne 的构建镜像只预装
Node，安装命令只认 npm / yarn / pnpm。在它的容器里现装 uv、再拉一个 Python 3.14
并非不行，只是把「这次能不能发出去」押在一个没有文档保证的环境上；GitHub 这边的
构建则是 `docs.yml` 每次推送都在验的那条。

`.github/workflows/docs.yml` 只做校验、**不发布**，挂在 push 与 PR 上。

**两个 workflow 的步骤都必须与 `make build` 逐条对齐**（顺序也一样）。这里出过
一次静默的错位：workflow 少了构建后的一步，于是线上发的一直与本地全绿的产物不同，
而「本地过得去就等于 CI 过得去」在当时并不成立。现在三处都是
`gen → zensical build → linkcheck → i18n_check`，
加步骤时请同时改 `Makefile`、`docs.yml` 与 `deploy.yml`。

!!! note "deploy 分支上只有文档"
    归档不在站点里（它们在 `assets.rwr-infra.uk` 上），所以 `site/` 与 `deploy` 分支
    都只有几十 MB 的文档，推起来很快。`deploy` 分支**永远只有一个提交**
    （孤儿提交 + force-push）：上一版才有的文件不会留在线上，分支自己也不会越滚越大。

> `zensical.toml` 里的 `site_url` 是 `https://rwrme.rwr-infra.uk/`。canonical / sitemap /
> 站内**绝对**引用都按它拼——换域名时要先改它再发一次，否则线上那些绝对地址指向别处。
> `linkcheck` 与 `i18n_check` 也按它解析绝对链接。
