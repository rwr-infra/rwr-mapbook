/**
 * 模型清单页工具：页内搜索 · 一键复制引用值 · 预览图统一图框
 *
 * 管哪五页
 * --------
 * MESH E / Wall E / Building E / Vehicle Scatter / Decal，也就是 /tables/ 下面
 * 那五张清单（三语同址，语言前缀与版本前缀都不影响判据）。
 * 别的页面这个文件一行都不做——`pageOf()` 认不出就直接返回。
 *
 * 为什么全从 DOM 上做，而不是改内容
 * --------------------------------
 * 内容层（content/tables/*.md）里的表格长这样，几百行都是一个格局：
 *
 *     | ![](a.png)<br>![](b.png) | 小石头<br>template = rock_s1 | 备注 |
 *
 * 名字、值、两张预览图**都在这一行里**，够脚本重建版式了；而内容一旦改成
 * 「带 div / span 的写法」，就会牵连三语结构对齐（tools/i18n_check.py 逐行比对
 * 表格行数、图片数、HTML 块）与每一篇的指纹。放在这里做，内容层一个字不动：
 * 以后往清单里加行、改名字、加一种语言，版式与搜索**自动跟上**。
 *
 * 于是这个文件干四件事：
 *   1. 预览列：拆掉图与图之间的 `<br>`，每张图套一个固定尺寸的图框（两图并排），
 *      框的大小全在 extra.css 的 `--ts-shot-*` 里调；
 *   2. 名称列：最后一行是引用值时，**值本身**换成可点的复制芯片，值前面的
 *      `template = ` 留在框外当正文（`template = [rock_s1]`，点复制得到 rock_s1；
 *      Vehicle Scatter 那种没有 `template =` 的，整行就是值）；
 *   3. 页面顶部生成搜索框：按**名称与引用值**模糊匹配，下拉列结果、按像的程度排，
 *      回车/点击跳到那一行。Ctrl+K 聚焦它（页眉那个全站搜索已经删了）；
 *   4. 每个分组标题后面补一个条目数。
 *
 * 认不出的行一律不动
 * ----------------
 * 「引用值」的判据是**名称列最后一行**：`template = xxx` 或者 `xxx.yyy` 这种
 * 单token。认不出（例如 MESH E 里「石头 / 使用工具放置」那两行）就不加芯片、
 * 也不套固定图框——那两行要按原尺寸看。搜索也照旧按名称收录它们。
 *
 * 与主题的关系
 * ------------
 * 主题把 `document$` 挂在 window 上（bundle 末尾 `window.document$=…`），而
 * extra_javascript 在 bundle **之前**执行（见 zensical.toml 的加载顺序说明），
 * 所以这里既要「马上就试一次」，也要在它出现后补订阅一次；`setup()` 靠
 * 元素上的一个标记做幂等，跑两次也无害。当前没有开 instant navigation，
 * 但那一条将来打开时这里不用改。
 */
(function () {
  "use strict";

  /* ── 认页面 ─────────────────────────────────────────────────────── */

  var PAGES = ["mesh", "wall", "building", "vehicle", "decal"];
  var PAGE_RE = /(?:^|\/)tables\/([a-z0-9_-]+)\/?(?:index\.html)?$/;

  function pageOf(pathname) {
    var m = PAGE_RE.exec(pathname || location.pathname);
    if (!m) return null;
    return PAGES.indexOf(m[1]) === -1 ? null : m[1];
  }

  /* ── 文案：按 `<html lang>` 取（三语各自一份，加语言照抄一组） ───── */

  var TEXT = {
    "zh-hans": {
      search: "搜索清单",
      placeholder: "搜索名称或引用值…",
      meta: "可搜名称与引用值",
      total: "共 {n} 项",
      count: "{n} 项",
      kicker: "TABLES · {n} 项",
      omitted: "略",
      none: "没有匹配的物件",
      more: "另有 {n} 条未列出，多打几个字缩小范围",
      copy: "点击复制",
      copied: "已复制",
      copyfail: "复制失败，请手动选中",
      nav: "↑↓ 选择 · 回车跳转 · Esc 关闭"
    },
    "zh-hant": {
      search: "搜尋清單",
      placeholder: "搜尋名稱或引用值…",
      meta: "可搜名稱與引用值",
      total: "共 {n} 項",
      count: "{n} 項",
      kicker: "TABLES · {n} 項",
      omitted: "略",
      none: "沒有符合的物件",
      more: "另有 {n} 條未列出，多打幾個字縮小範圍",
      copy: "點擊複製",
      copied: "已複製",
      copyfail: "複製失敗，請手動選取",
      nav: "↑↓ 選擇 · 回车跳轉 · Esc 關閉"
    },
    en: {
      search: "Search this list",
      placeholder: "Search name or reference…",
      meta: "Searches names and reference values",
      total: "{n} items",
      count: "{n} items",
      kicker: "TABLES · {n} items",
      omitted: "n/a",
      none: "No matching object",
      more: "{n} more not listed — type more to narrow it down",
      copy: "Click to copy",
      copied: "Copied",
      copyfail: "Copy failed — select it manually",
      nav: "↑↓ select · Enter jump · Esc close"
    }
  };

  function T() {
    var lang = (document.documentElement.getAttribute("lang") || "").toLowerCase();
    if (lang.indexOf("en") === 0) return TEXT.en;
    if (lang.indexOf("hant") !== -1) return TEXT["zh-hant"];
    return TEXT["zh-hans"];
  }

  /* ── 小工具 ─────────────────────────────────────────────────────── */

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  var SVG_NS = "http://www.w3.org/2000/svg";

  function icon(path, cls) {
    var svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    if (cls) svg.setAttribute("class", cls);
    var p = document.createElementNS(SVG_NS, "path");
    p.setAttribute("d", path);
    svg.appendChild(p);
    return svg;
  }

  // material 的 magnify / content-copy / check
  var ICON_SEARCH = "M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.52 6.52 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5Z";
  var ICON_COPY = "M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1Z";
  var ICON_CHECK = "M21 7 9 19l-5.5-5.5 1.41-1.41L9 16.17 19.59 5.59 21 7Z";

  /* ── 名称列：拆出「引用值」 ──────────────────────────────────────── */

  // 名称列最后一行的那几个节点（`<br>` 之后到单元格末尾）
  function lastLineNodes(cell) {
    var out = [];
    for (var i = cell.childNodes.length - 1; i >= 0; i--) {
      var node = cell.childNodes[i];
      if (node.nodeType === 1 && node.tagName === "BR") break;
      out.unshift(node);
    }
    return out;
  }

  function textOf(nodes) {
    return nodes.map(function (n) { return n.textContent; }).join("").trim();
  }

  /**
   * 名称列 → { name, value }
   *   `小石头<br>template = rock_s1`     → name 小石头 / value rock_s1
   *   `机枪悍马<br>humvee.vehicle`       → name 机枪悍马 / value humvee.vehicle
   *   `坦克<br>tank_denied_player`       → name 坦克 / value tank_denied_player
   *   只认「最后一行」，因为这几张清单的写法都是「名称一行、引用值一行」。
   *
   *   ⚠️ 裸值的判据只要求「一个拉丁 token」——**不再要求里面有点**：特殊载具表
   *      用的是阵营 key（`jeep`、`apc`、`tank_denied_player`），本来就没有点。
   *      认不出就不给值：MESH E 里「石头 / 使用工具放置」那两行的最后一行是
   *      「placed with a tool」，带空格，仍不会被误认。
   */
  function readName(cell) {
    var nodes = lastLineNodes(cell);
    var line = textOf(nodes);
    var out = { name: "", value: "", kind: "", nodes: nodes };
    var m = /^template\s*=\s*([\s\S]+)$/.exec(line);
    if (m) {
      out.kind = "template";
      out.value = m[1].trim();
    } else if (/^[A-Za-z0-9_.\-]+$/.test(line)) {
      out.kind = "ref";
      out.value = line;
    }
    var head = cell.cloneNode(true);
    var fresh = lastLineNodes(head);
    if (fresh.length && textOf(fresh) === line) {
      fresh.forEach(function (n) { head.removeChild(n); });
    }
    out.name = (head.textContent || "").replace(/\s+/g, " ").trim();
    return out;
  }

  /* ── 预览列：两图并排 + 固定图框 ─────────────────────────────────── */

  function decoratePreview(cell, hasValue) {
    var media = [];
    Array.prototype.forEach.call(cell.childNodes, function (node) {
      if (node.nodeType === 1 && (node.tagName === "A" || node.tagName === "IMG")) media.push(node);
    });

    if (!media.length) {
      // Vehicle Scatter 几百行都是空预览列：给一个静默的占位（居中显示），
      // 免得那一列看起来像「漏了图」。
      if (!cell.textContent.trim()) cell.appendChild(el("span", "ts-none", T().omitted));
      return;
    }

    // 图与图之间的换行靠 flex 的 gap，不靠 `<br>`——留着会把两张图上下叠起来
    Array.prototype.slice.call(cell.querySelectorAll("br")).forEach(function (br) {
      br.parentNode.removeChild(br);
    });

    var wrap = el("span", "ts-prev");
    // 认不出引用值的行（MESH E 的「使用工具放置」两行）不套固定框，按原尺寸看
    if (!hasValue) wrap.className += " ts-prev--natural";

    media.forEach(function (node) {
      var shot = el("span", "ts-shot");
      shot.appendChild(node); // appendChild 会把它从 cell 里摘走
      wrap.appendChild(shot);
    });
    cell.appendChild(wrap);
  }

  /* ── 复制 ───────────────────────────────────────────────────────── */

  function legacyCopy(text) {
    try {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.top = "-1000px";
      document.body.appendChild(area);
      area.select();
      var ok = document.execCommand("copy");
      document.body.removeChild(area);
      return ok;
    } catch (e) {
      return false;
    }
  }

  function copyText(text, done) {
    // file:// 离线包里没有 navigator.clipboard，退回 execCommand
    if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { done(true); },
        function () { done(legacyCopy(text)); }
      );
      return;
    }
    done(legacyCopy(text));
  }

  function chip(cell, info, text) {
    var nodes = info.nodes;
    var last = nodes[nodes.length - 1];
    // 引用值一定落在「最后一行」的最后一个文本节点里（前面可能还有别的节点，
    // 例如英文页里被 `*[template]: …` 包成 <abbr> 的那个 template——它留在原地）
    if (!last || last.nodeType !== 3) return;

    var value = info.value;
    var at = last.nodeValue.lastIndexOf(value);
    if (at < 0) return; // 值跨了节点（现实中不会），那就别动它

    // 复制框里**只放值**：`template = ` 留在框外当正文。
    // 这样点的是 `rock_s1` 这么一小块，一眼也知道复制的是哪一段。
    var code = el("code", "ts-tpl");
    // 值里的下划线处插 `<wbr>`：**只有在挤不下时才允许断行**，而且是断在
    // `railroad_straight_` / `element_50m` 这种自然位置。不插的话，这个 246px 宽
    // 的芯片（全站最长的引用值）会把「小物件」那张表的名称列顶到 281px 起，
    // 整张表因此比别的表宽 52px、多出一条横向滚动（见 extra.css 那段说明）。
    // 用 `<wbr>` 而不是零宽空格：它不产生字符，手动选中复制出来的值还是干净的。
    // ⚠️ 下划线本身要**自己补回去**：`split("_")` 会把它吃掉，第一版就写成
    //    `rock` + `<wbr>` + `s1`，页面上显示成 `rocks1`（复制出来的值倒是对的，
    //    更难发现）。`<wbr>` 放在下划线**之后**，断行才断成 `railroad_` / `straight_`。
    var body = el("span", "ts-tpl__text");
    value.split("_").forEach(function (part, index) {
      if (index) {
        body.appendChild(document.createTextNode("_"));
        body.appendChild(document.createElement("wbr"));
      }
      body.appendChild(document.createTextNode(part));
    });
    code.appendChild(body);
    code.setAttribute("role", "button");
    code.setAttribute("tabindex", "0");
    code.setAttribute("data-ts-value", value);
    code.setAttribute("data-ts-done", text.copied);
    code.setAttribute("aria-label", text.copy + " " + value);
    code.title = text.copy;
    code.appendChild(icon(ICON_COPY, "ts-tpl__icon ts-tpl__icon--copy"));
    code.appendChild(icon(ICON_CHECK, "ts-tpl__icon ts-tpl__icon--done"));

    var parent = last.parentNode;
    var head = last.nodeValue.slice(0, at);
    var tail = last.nodeValue.slice(at + value.length);
    if (head) parent.insertBefore(document.createTextNode(head), last);
    parent.insertBefore(code, last);
    if (tail) parent.insertBefore(document.createTextNode(tail), last);
    parent.removeChild(last);
  }

  function flash(node, ok) {
    var text = T();
    node.classList.remove("is-copied", "is-failed");
    node.classList.add(ok ? "is-copied" : "is-failed");
    node.setAttribute("data-ts-done", ok ? text.copied : text.copyfail);
    window.clearTimeout(node.__tsTimer);
    node.__tsTimer = window.setTimeout(function () {
      node.classList.remove("is-copied", "is-failed");
    }, 1400);
  }

  document.addEventListener("click", function (event) {
    var node = event.target && event.target.closest ? event.target.closest(".ts-tpl") : null;
    if (!node) return;
    if (window.getSelection && String(window.getSelection()).length) return; // 正在选字就不抢
    event.preventDefault();
    copyText(node.getAttribute("data-ts-value"), function (ok) { flash(node, ok); });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" && event.key !== " ") return;
    var node = event.target && event.target.closest ? event.target.closest(".ts-tpl") : null;
    if (!node) return;
    event.preventDefault();
    copyText(node.getAttribute("data-ts-value"), function (ok) { flash(node, ok); });
  });

  /* ── 模糊匹配 ───────────────────────────────────────────────────── */

  function norm(str) {
    return (str || "").toLowerCase().replace(/[\s_\-.,:;()（）【】「」『』、，。：；·]+/g, "");
  }

  function score(query, hay) {
    if (!query || !hay) return 0;
    if (hay === query) return 1000;
    var at = hay.indexOf(query);
    if (at === 0) return 800 - Math.min(200, hay.length);
    if (at > 0) return 600 - at * 2 - Math.min(200, hay.length);
    // 子序列：允许中间夹字（"sw4" 能命中 "rock_s4"），按跨度扣分
    var j = 0;
    var first = -1;
    var last = -1;
    for (var i = 0; i < hay.length && j < query.length; i++) {
      if (hay.charAt(i) === query.charAt(j)) {
        if (first < 0) first = i;
        last = i;
        j++;
      }
    }
    if (j < query.length) return 0;
    return 400 - (last - first + 1 - query.length) * 4 - first;
  }

  // 把命中的那一段圈出来（只做「连续子串」这一种，模糊命中不标）
  function mark(text, query) {
    var frag = document.createDocumentFragment();
    if (!query) {
      frag.appendChild(document.createTextNode(text));
      return frag;
    }
    var at = text.toLowerCase().indexOf(query);
    if (at < 0) {
      frag.appendChild(document.createTextNode(text));
      return frag;
    }
    frag.appendChild(document.createTextNode(text.slice(0, at)));
    frag.appendChild(el("mark", null, text.slice(at, at + query.length)));
    frag.appendChild(document.createTextNode(text.slice(at + query.length)));
    return frag;
  }

  /* ── 页面装配 ───────────────────────────────────────────────────── */

  function headingBefore(article, node) {
    var headings = article.querySelectorAll("h2, h3");
    var last = null;
    for (var i = 0; i < headings.length; i++) {
      // 4 = DOCUMENT_POSITION_FOLLOWING：node 在这个标题之后
      if (headings[i].compareDocumentPosition(node) & 4) last = headings[i];
      else break;
    }
    return last;
  }

  function headText(heading) {
    if (!heading) return "";
    var clone = heading.cloneNode(true);
    var link = clone.querySelector(".headerlink");
    if (link) clone.removeChild(link);
    return (clone.textContent || "").replace(/\s+/g, " ").trim();
  }

  function stickyOffset() {
    var header = document.querySelector(".md-header");
    var bar = document.querySelector(".ts-search");
    var root = document.documentElement.style;
    // 页眉实际高度：粘性搜索框贴在它下面（页眉不是固定高度，字号/语言都会影响）
    root.setProperty("--ts-sticky-top", (header ? header.offsetHeight : 0) + "px");
    // 搜索框自己的高度：表头要贴在**搜索框下面**，不是页眉下面——不然两者叠在一起
    root.setProperty("--ts-bar-h", (bar ? bar.offsetHeight : 0) + "px");
  }

  var MAX_RESULTS = 40;

  function buildSearch(article, rows, text) {
    var wrap = el("div", "ts-search");
    var box = el("div", "ts-search__box");
    box.appendChild(icon(ICON_SEARCH, "ts-search__icon"));

    var input = el("input", "ts-search__input");
    input.type = "search";
    input.autocomplete = "off";
    input.spellcheck = false;
    input.placeholder = text.placeholder;
    input.setAttribute("aria-label", text.search);
    box.appendChild(input);
    box.appendChild(el("kbd", "ts-search__kbd", "Ctrl K"));

    var meta = el("p", "ts-search__meta", text.total.replace("{n}", rows.length) + " · " + text.meta);
    var list = el("ul", "ts-search__list");
    list.setAttribute("role", "listbox");
    list.hidden = true;

    wrap.appendChild(box);
    wrap.appendChild(meta);
    wrap.appendChild(list);

    var host = article.querySelector(".kicker") || article.querySelector("h1");
    if (host && host.parentNode === article) article.insertBefore(wrap, host.nextSibling);
    else article.insertBefore(wrap, article.firstChild);

    var pool = rows.map(function (row) {
      return { row: row, name: norm(row.name), value: norm(row.value) };
    });

    var hits = [];
    var active = -1;

    function close() {
      list.hidden = true;
      list.textContent = "";
      hits = [];
      active = -1;
    }

    function goTo(row) {
      close();
      row.tr.scrollIntoView({ block: "center" });
      row.tr.classList.add("is-hit");
      window.setTimeout(function () { row.tr.classList.remove("is-hit"); }, 2000);
    }

    function draw() {
      var at = hits[active];
      Array.prototype.forEach.call(list.children, function (li, index) {
        li.classList.toggle("is-active", index === active);
        if (index === active && at && li.scrollIntoView) li.scrollIntoView({ block: "nearest" });
      });
    }

    function render(raw) {
      list.textContent = "";
      if (!hits.length) {
        list.appendChild(el("li", "ts-hit ts-hit--empty", text.none));
        list.hidden = false;
        active = -1;
        return;
      }
      var shown = hits.slice(0, MAX_RESULTS);
      shown.forEach(function (row, index) {
        var li = el("li", "ts-hit");
        li.setAttribute("role", "option");
        if (row.section) li.appendChild(el("span", "ts-hit__sec", row.section));
        var name = el("span", "ts-hit__name");
        name.appendChild(mark(row.name || "—", raw));
        li.appendChild(name);
        if (row.line) {
          var code = el("code", "ts-hit__tpl");
          code.appendChild(mark(row.line, raw));
          li.appendChild(code);
        }
        li.addEventListener("click", function () { goTo(row); });
        li.addEventListener("mousemove", function () { active = index; draw(); });
        list.appendChild(li);
      });
      if (hits.length > shown.length) {
        list.appendChild(el("li", "ts-hit ts-hit--more", text.more.replace("{n}", hits.length - shown.length)));
      }
      list.hidden = false;
      active = 0;
      draw();
    }

    function search(raw) {
      var query = norm(raw);
      if (!query) { close(); return; }
      // 名称与引用值各打一次分；引用值命中给一点加成——它是「精确找东西」的那一边。
      // ⚠️ 加成只能在**真的命中**时给：加在 0 分上会让所有行都 > 0，等于没筛。
      var found = [];
      pool.forEach(function (item, order) {
        var byValue = score(query, item.value);
        var byName = score(query, item.name);
        if (!byValue && !byName) return;
        found.push({ row: rows[order], score: Math.max(byValue + (byValue ? 30 : 0), byName), order: order });
      });
      found.sort(function (a, b) {
        if (b.score !== a.score) return b.score - a.score;
        return a.order - b.order;
      });
      hits = found.map(function (hit) { return hit.row; });
      render(raw);
    }

    input.addEventListener("input", function () { search(input.value); });
    input.addEventListener("focus", function () { if (input.value) search(input.value); });
    input.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        if (input.value) { input.value = ""; close(); }
        else input.blur();
        return;
      }
      if (list.hidden || !hits.length) return;
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        var step = event.key === "ArrowDown" ? 1 : -1;
        active = (active + step + hits.length) % hits.length;
        draw();
      } else if (event.key === "Enter") {
        event.preventDefault();
        if (hits[active]) goTo(hits[active]);
      }
    });

    document.addEventListener("click", function (event) {
      if (!wrap.contains(event.target)) close();
    });

    return { focus: function () { input.focus(); input.select(); }, wrap: wrap };
  }

  /* ── 一个页面装一次 ─────────────────────────────────────────────── */

  function setup() {
    var page = pageOf(location.pathname);
    if (!page) return;
    var article = document.querySelector("article.md-content__inner");
    if (!article || article.__tsDone) return;
    article.__tsDone = true;

    var text = T();
    article.classList.add("tables-page", "tables-page--" + page);

    var rows = [];
    var groups = [];

    Array.prototype.forEach.call(article.querySelectorAll("table"), function (table) {
      var section = headingBefore(article, table);
      var sectionName = headText(section);
      var body = table.tBodies[0];
      if (!body) return;
      var group = { heading: section, rows: [] };

      Array.prototype.forEach.call(body.rows, function (tr) {
        if (tr.cells.length < 2) return;
        var info = readName(tr.cells[1]);
        decoratePreview(tr.cells[0], !!info.value);

        var line = info.kind === "template" ? "template = " + info.value : info.value;
        if (info.value) chip(tr.cells[1], info, text);

        var row = { tr: tr, name: info.name, value: info.value, line: line, section: sectionName };
        rows.push(row);
        group.rows.push(row);
      });

      if (group.rows.length) groups.push(group);
    });

    // 分组标题后面补条目数（只给带表格的分组）
    groups.forEach(function (group) {
      if (!group.heading || group.heading.querySelector(".ts-count")) return;
      group.heading.appendChild(el("span", "ts-count", text.count.replace("{n}", group.rows.length)));
    });

    // 页顶那行 kicker 换成**这一页的条目数**（原先 /tables/ 落地页上那张汇总表
    // 撤掉之后，统计数就放在这儿）。页面自己没写 kicker 的（MESH E），在标题下面补一行。
    if (rows.length) {
      var kicker = article.querySelector(".kicker");
      var kickerText = text.kicker.replace("{n}", rows.length);
      if (kicker) {
        kicker.textContent = kickerText;
      } else {
        var heading = article.querySelector("h1");
        var node = el("p", "kicker", kickerText);
        if (heading && heading.parentNode === article) article.insertBefore(node, heading.nextSibling);
        else article.insertBefore(node, article.firstChild);
      }
    }

    var finder = rows.length ? buildSearch(article, rows, text) : null;

    stickyOffset();
    window.addEventListener("resize", stickyOffset);
    // 页眉的高度是量出来的，而且**主题自己后面还会改它**（滚动/换行/语言都可能动）。
    // 这里另外盯着它：页眉一变就重算，粘性搜索框与表头才不会错位。
    if (window.ResizeObserver) {
      var header = document.querySelector(".md-header");
      if (header) new ResizeObserver(stickyOffset).observe(header);
    }

    // Ctrl+K / 「/」聚焦页内搜索。页眉那个全站搜索已经删了，Ctrl+K 在这里接手；
    // 没装搜索框的页面什么都不做，也不吞按键。
    document.addEventListener("keydown", function (event) {
      if (!finder) return;
      if (event.key === "Escape") return;
      var key = (event.key || "").toLowerCase();
      var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((event.target && event.target.tagName) || "");
      if (event.ctrlKey && !event.altKey && !event.metaKey && key === "k") {
        event.preventDefault();
        finder.focus();
      } else if (key === "/" && !event.ctrlKey && !event.metaKey && !event.altKey && !typing) {
        event.preventDefault();
        finder.focus();
      }
    });
  }

  // ⚠️ **当场就跑**，不要等 DOMContentLoaded（踩过：五张清单点进去会「闪一下
  //    另一张页面」——kicker 还是老的、预览图还没进框，之后才变正常）。
  //    这个文件是同步 <script>、排在正文之后（见生成出来的 HTML），所以走到这里
  //    article 已经在 DOM 里，而浏览器**还没画第一帧**；等到 DOMContentLoaded 再跑，
  //    中间那一帧画的正是「没处理过的原样」，用户看到的就是那一闪。
  setup();

  // 主题的 document$ 还没挂上来（bundle 在 extra_javascript 之后初始化）。
  // 挂上之后再订阅一次兜底（instant navigation 将来打开时也靠它）；
  // setup() 幂等——元素上那个 __tsDone 标记就是为这个留的。
  (function wait() {
    if (window.document$) {
      window.document$.subscribe(function () { setup(); });
      return;
    }
    window.setTimeout(wait, 100);
  })();
})();
