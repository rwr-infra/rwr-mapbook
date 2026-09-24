# 三语文档站 · 构建流程
#
#   content/   唯一手写层：guide/index.zh-hans.md、guide/index.en.md
#   docs/      构建层：.md 由 tools/docsgen.py 生成，assets/ 等仍是手写的
#
#   make gen     从 content/ 生成 docs/，并从文件树重新生成导航
#   make check   翻译度检查：漏翻 / 过期 / 译文结构对不上，产出 agent 可读报告
#   make links   产物链接体检：站内引用 / 目录尾斜杠 / 跳转桩目标 / 补正脚本
#   make build   生成 → 构建站点 → 标签过滤 → 链接体检 → 翻译度检查
#   make serve   本地预览 http://127.0.0.1:8000
#   make sync    为缺失的译文建立骨架，然后重新生成

UV ?= uv

.PHONY: gen docs nav check links build serve sync clean

gen: docs nav

docs:
	$(UV) run python tools/docsgen.py

nav: docs
	$(UV) run python tools/navgen.py

check:
	$(UV) run python tools/i18n_check.py

# 产物链接体检。构建会一页页重写 site/，所以它必须在 zensical 之后跑；
# tagfilter 又会在事后改标签索引，所以也排在 tagfilter 之后。
links:
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
serve: gen
	$(UV) run zensical serve -a 127.0.0.1:8000

sync:
	$(UV) run python tools/i18n_check.py --sync
	$(MAKE) gen

clean:
	rm -rf site
