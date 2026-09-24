# 三语文档站 · 构建流程
#
#   content/   唯一手写层：prepare/index.zh-hans.md、prepare/index.en.md
#   docs/      构建层：.md 由 tools/docsgen.py 生成，assets/ 等仍是手写的
#
#   make gen     从 content/ 生成 docs/，并从文件树重新生成导航
#   make check   翻译度检查：漏翻 / 过期 / 译文结构对不上，产出 agent 可读报告
#   make versions 版本清单体检：声明与 content/versions/ 是否对得上
#   make links   产物链接体检：站内引用 / 目录尾斜杠 / 跳转桩目标 / 补正脚本
#   make build   生成 → 构建站点 → 标签过滤 → 链接体检 → 翻译度检查
#   make serve   本地预览 http://127.0.0.1:8000（根域；线上带子路径，见文件末尾）
#   make serve-subpath  同上，但按线上的子路径预览
#   make sync    为缺失的译文建立骨架，然后重新生成

UV ?= uv

.PHONY: gen docs nav check versions links build serve serve-subpath sync clean

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

# 产物链接体检。构建会一页页重写 site/，所以它必须在 zensical 之后跑；
# tagfilter 又会在事后改标签索引，所以也排在 tagfilter 之后。
links: versions
	$(UV) run python tools/linkcheck.py

# 与 .github/workflows/docs.yml 用同一条命令：本地过得去就等于 CI 过得去。
# ⚠️ --clean 会清空 site/，所以 serve 还开着的时候不要跑这个目标。
build: gen
	$(UV) run zensical build --clean --strict
	$(UV) run python tools/tagfilter.py
	$(UV) run python tools/linkcheck.py
	$(UV) run python tools/i18n_check.py

# ⚠️ zensical serve 自己构建、自己服务，插不进 tagfilter 与 linkcheck，
#    所以预览里的 /tags/ 仍会列出全部三种语言的篇目（线上产物不会）。
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
