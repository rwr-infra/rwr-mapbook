# 三语文档站 · 构建流程
#
#   content/   唯一手写层：prepare/index.zh-hans.md、prepare/index.en.md
#   docs/      构建层：.md 由 tools/docsgen.py 生成，assets/ 等仍是手写的
#
#   make gen     从 content/ 生成 docs/，并从文件树重新生成导航
#   make check   翻译度检查：漏翻 / 过期 / 译文结构对不上，产出 agent 可读报告
#   make versions 版本清单体检：声明与 content/versions/ 是否对得上
#   make archives 历史版本归档体检：分片、哈希、页面上的按钮与清单是否对得上
#   make downloads 切分历史版本归档，并写清单（要有源归档；平时用不到）
#   make links   产物链接体检：站内引用 / 目录尾斜杠 / 跳转桩目标 / 补正脚本
#   make build   生成 → 构建站点 → 链接体检 → 归档体检 → 翻译度检查
#   make watch   盯着 content/，改了自动重新生成 docs/（配合 make serve 用）
#   make serve   本地预览 http://127.0.0.1:8000（根域；线上带子路径，见文件末尾）
#   make serve-subpath  同上，但按线上的子路径预览
#   make sync    为缺失的译文建立骨架，然后重新生成

UV ?= uv

.PHONY: gen docs nav check versions archives downloads links build serve serve-subpath watch sync clean

gen: docs nav

docs:
	$(UV) run python tools/docsgen.py

nav: docs
	$(UV) run python tools/navgen.py

check:
	$(UV) run python tools/i18n_check.py

# 版本清单体检。docsgen 生成前也会跑同一条判据（两边不过就别想生成），
# 这里单独留一个入口，好在只改 zensical.toml 时不必跑整条链。
versions:
	$(UV) run python tools/versions.py

# 历史版本归档体检：docs/downloads/ 下的分片与清单对不对得上、
# content/download/ 页面上挂的按钮与清单是不是两边都对得上。
# ⚠️ 它**不需要源归档**（源在群文件里，仓库里没有），所以 CI 跑得了这个，
#    跑不了 downloads。
archives:
	$(UV) run python tools/chunker.py --check

# 存整包 / 切分片。源归档放在 DOWNLOADS_SRC 下（默认 ~/Downloads），有哪几个由
# DOWNLOADS 列着。产物 docs/downloads/ 是**要进仓库**的：部署方不给传大文件，
# 所以整包与分片都是最终形态，不是中间产物。
# ⚠️ 25 MB 的上限来自 **EdgeOne Pages 的单文件限制**，不是 git 的；要调得有理由。
DOWNLOADS_SRC ?= $(HOME)/Downloads
DOWNLOADS ?= 060.zip 070.rar 080.rar 081.rar 090.rar 091.rar 0100.rar 0101.rar \
             vao0822.svg OgreSDK_vc10_v1-7-4.zip

downloads:
	$(UV) run python tools/chunker.py --src "$(DOWNLOADS_SRC)" $(DOWNLOADS)

# 产物链接体检。构建会一页页重写 site/，所以它必须在 zensical 之后跑。
links: versions
	$(UV) run python tools/linkcheck.py

# 与 .github/workflows/docs.yml 用同一条命令：本地过得去就等于 CI 过得去。
# ⚠️ --clean 会清空 site/，所以 serve 还开着的时候不要跑这个目标。
build: gen
	$(UV) run zensical build --clean --strict
	$(UV) run python tools/linkcheck.py
	$(UV) run python tools/chunker.py --check
	$(UV) run python tools/i18n_check.py

# 预览时另开一个终端跑这个：`zensical serve` 只盯 docs/（生成物），
# 改 content/ 下的源文件它看不见——这一步把「content/ → docs/」自动接上。
# 两个一起开，改完存盘就能在浏览器里看到。
watch:
	$(UV) run python tools/watch.py

# ⚠️ `zensical serve` 跳过后处理链，所以**预览里没有链接体检**——它是构建之后
#    才做得了的事。标签索引不在此列：它由 docsgen 各自生成，预览与线上一致。
#
# 为什么线上在子路径下
# ----------------------
# 线上是 GitHub Pages 的「项目站」（仓库名不是 <用户名>.github.io），
# 它的地址本来就是
#     https://<用户名>.github.io/<仓库名>/
# 也就是说**站点根落在那一层，而不是域名根**。所以 zensical.toml 里的 site_url
# 必须带着 /rwr-mapbook/：站内绝对引用、sitemap、canonical 都按这个根拼。
# 少了它，本地看着一切正常，一上线全是断链——这一项不能按「本地预览方便」来取舍。
#
# `zensical serve` 没有覆盖 site_url 的选项，于是它按配置把
# `http://127.0.0.1:8000/` 302 到 `/rwr-mapbook/`。
#
# 本地预览不该背这个包袱：**默认就让预览停在根域。** 办法是另生成一份
# zensical.preview.toml，只把 site_url 换成本地根域，其余配置一行不动；
# 那份文件是生成物、不入库，也改不到线上的 site_url。
SERVE_ROOT_URL = http://127.0.0.1:8000/
SERVE_SUBPATH_URL = http://127.0.0.1:8000/rwr-mapbook/
PREVIEW_CONFIG = zensical.preview.toml

serve: gen $(PREVIEW_CONFIG)
	@echo "预览入口： $(SERVE_ROOT_URL)"
	$(UV) run zensical serve -f $(PREVIEW_CONFIG) -a 127.0.0.1:8000

# 要核对「线上那种子路径」下的表现（绝对引用、canonical、sitemap）就用这个。
serve-subpath: gen
	@echo "预览入口： $(SERVE_SUBPATH_URL)  （带子路径，与线上一致）"
	$(UV) run zensical serve -a 127.0.0.1:8000

# 只把 site_url 换成本地根域，其余一行不动。用 sed 而不是「复制再改」，
# 是为了让「除了 site_url，两份配置完全相同」这件事一眼可见。
$(PREVIEW_CONFIG): zensical.toml
	@sed 's|^site_url = .*|site_url = "$(SERVE_ROOT_URL)"|' zensical.toml > $@
	@grep -q '^site_url = "$(SERVE_ROOT_URL)"' $@ || { echo "预览配置没换掉 site_url，先看 zensical.toml 第一行"; rm -f $@; exit 1; }

sync:
	$(UV) run python tools/i18n_check.py --sync
	$(MAKE) gen

clean:
	rm -rf site $(PREVIEW_CONFIG)
