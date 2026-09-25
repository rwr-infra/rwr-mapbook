# 三语文档站 · 构建流程
#
#   content/   唯一手写层：prepare/index.zh-hans.md、prepare/index.en.md
#   docs/      构建层：.md 由 tools/docsgen.py 生成，assets/ 等仍是手写的
#
#   make gen     从 content/ 生成 docs/，并从文件树重新生成导航
#   make check   翻译度检查：漏翻 / 过期 / 译文结构对不上，产出 agent 可读报告
#   make versions 版本清单体检：声明与 content/versions/ 是否对得上
#   make links   产物链接体检：站内引用 / 目录尾斜杠 / 跳转桩目标 / 补正脚本
#   make build   生成 → 构建站点 → 链接体检 → 翻译度检查
#   make watch   盯着 content/，改了自动重新生成 docs/（配合 make serve 用）
#   make serve   本地预览 http://127.0.0.1:8000
#   make offline 打一份解压就能看的离线站（去掉 404 页、地址改成 .html 式）
#   make sync    为缺失的译文建立骨架，然后重新生成

UV ?= uv

.PHONY: gen docs nav check versions links build serve watch sync offline offline-check clean

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

# 产物链接体检。构建会一页页重写 site/，所以它必须在 zensical 之后跑。
links: versions
	$(UV) run python tools/linkcheck.py

# 与 .github/workflows/docs.yml 用同一条命令：本地过得去就等于 CI 过得去。
# ⚠️ --clean 会清空 site/，所以 serve 还开着的时候不要跑这个目标。
build: gen
	$(UV) run zensical build --clean --strict
	$(UV) run python tools/linkcheck.py
	$(UV) run python tools/i18n_check.py

# 预览时另开一个终端跑这个：`zensical serve` 只盯 docs/（生成物），
# 改 content/ 下的源文件它看不见——这一步把「content/ → docs/」自动接上。
# 两个一起开，改完存盘就能在浏览器里看到。
watch:
	$(UV) run python tools/watch.py

# ⚠️ `zensical serve` 跳过后处理链，所以**预览里没有链接体检**——它是构建之后
#    才做得了的事。标签索引不在此列：它由 docsgen 各自生成，预览与线上一致。
#
# 线上在域名根（`https://rwrme.rwr-infra.uk/`），所以预览直接用配置里的 site_url
# 就行，不需要另生成一份「只换 site_url」的预览配置——那是站点落在子路径下时
# 才要的包袱（本站以前在 GitHub Pages 的项目站上，`/rwr-mapbook/` 那一层会在
# `zensical serve` 里 302 一次，本地预览因此每次都要先跳一下）。
# 哪天真挪回子路径下，把那份 sed 生成预览配置的办法从模版仓库拿回来即可。
serve: gen
	@echo "预览入口： http://127.0.0.1:8000/"
	$(UV) run zensical serve -a 127.0.0.1:8000

sync:
	$(UV) run python tools/i18n_check.py --sync
	$(MAKE) gen

# ── 离线文件版 ────────────────────────────────────────────────────────────
# `make offline` 出一份**解压就能看**的整站，给不能上网／不想开服务器的人：
#
#     offline:  生成 → 用离线配置构建 → 补跳转桩的 .html 副本 → 体检 → 打成一个 zip
#
# 与线上版的三处不同，都在 zensical.offline.toml 里（由 zensical.toml 用 sed 生成）：
#
#   1. **site_dir 换成 site-offline/**，两版互不覆盖；
#   2. **打开 offline 插件**：它把 use_directory_urls 关掉，页面从 `editor/` 变成
#      `editor.html`。file:// 下面浏览器不会把 `editor/` 解析到 `editor/index.html`，
#      不关这一项整站的导航都点不动；
#   3. **删掉 404.html**：它的站内引用是绝对路径（`/rwr-mapbook/…`，因为它要能在
#      任意目录下被服务器拿出来用），离线版没有服务器，它永远不会被渲染出来，
#      留着只是一页断链。file:// 下打不开某个文件，浏览器给的是它自己的错误页。
#
# ⚠️ 它**不跑** linkcheck 与 i18n_check：那两条都假定目录式地址（`…/page/`），
#    离线版全是 `.html`，跑了只会满屏假警报。它跑的是 tools/offline_check.py——
#    同一套判据（每条站内引用都得落地）另写的一遍，外加锚点。
#    （此前是拿临时脚本在 /tmp 里验的，那种东西验完就没了；判据该留在仓库里。）
OFFLINE_CONFIG = zensical.offline.toml
OFFLINE_DIR = site-offline
OFFLINE_ZIP = rwr-mapbook-offline.zip

offline: gen $(OFFLINE_CONFIG)
	@rm -rf $(OFFLINE_DIR)
	$(UV) run zensical build -f $(OFFLINE_CONFIG) --strict
	$(UV) run python tools/offline_stubs.py $(OFFLINE_DIR)
	@rm -f $(OFFLINE_DIR)/404.html
	$(UV) run python tools/offline_check.py $(OFFLINE_DIR)
	@rm -f $(OFFLINE_ZIP)
	@cd $(OFFLINE_DIR) && zip -qr ../$(OFFLINE_ZIP) . && cd ..
	@printf '离线包：%s\n' "$(OFFLINE_ZIP)"
	@du -sh $(OFFLINE_DIR) $(OFFLINE_ZIP)

# 只体检现有的 site-offline/，不重打。
offline-check:
	$(UV) run python tools/offline_check.py $(OFFLINE_DIR)

# 与预览配置同一套办法：sed，只改该改的两行，其余一行不动。
# 第二行的注释尾巴是**锚点**，免得 sed 撞上别处恰好也是 `enabled = false` 的行。
#
# ⚠️ 判据用 awk 对着**那一节**看，不写 `grep -q '^enabled = true$'`：
#      · make 会把 `$'` 当成「名为 ' 的变量」吃掉，正则尾巴那个 $ 连带着收尾的引号
#        一起消失，于是 shell 收到一个不闭合的引号——报错还指不到这里；
#      · 更要紧的是**假绿灯**：search 与 tags 那两节本来就写着 `enabled = true`，
#        拿它当判据的话，offline 那一节压根没改成也会一路放行（踩过一次，
#        结果是整包生成了目录式地址，file:// 下点导航变成浏览器的目录列表）。
$(OFFLINE_CONFIG): zensical.toml
	@sed -e 's|^site_dir = .*|site_dir = "$(OFFLINE_DIR)"|' \
	     -e 's|^enabled = false.*离线|enabled = true|' zensical.toml > $@
	@grep -q '^site_dir = "$(OFFLINE_DIR)"' $@ || { echo "离线配置没换掉 site_dir"; rm -f $@; exit 1; }
	@awk '/^\[project\.plugins\.offline\]/{getline; if ($$0 == "enabled = true") ok = 1} \
	      END{exit !ok}' $@ || { echo "离线配置没打开 offline 插件（那一行的行尾锚点注释还在吗）"; rm -f $@; exit 1; }

clean:
	rm -rf site $(OFFLINE_DIR) $(OFFLINE_ZIP) $(OFFLINE_CONFIG)
