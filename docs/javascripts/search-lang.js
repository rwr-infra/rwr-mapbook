/**
 * 搜索面板：标签按语言分段 + 面板文案跟着语言走
 * ===========================================================================
 * 要做的事
 * ---------
 * 本站一份内容有多种语言，而搜索索引 `search.json` 是**整站一份**的，
 * 面板上的标签清单也是一锅端的：几种语言的标签混在同一个列表里，
 * 看不出谁是谁的。这个脚本补两件事：
 *
 *   1. **筛选栏里的标签按语言分段**：一种语言一段，段标题就是语言名，而
 *      **当前页面的语言排在最前**——一打开搜索就先看到自己这一种。
 *      点击照旧走主题原生的标签筛选：我们那一列是**抄**出来的，点一下转发给
 *      主题里那一条，命中的还是它自己的逻辑。
 *   2. **面板界面上的文案跟着页面语言走**（主题的搜索面板写死英文）。
 *
 * 语言清单从哪儿来
 * -------------------
 * **不写在这个文件里。** 页面 `<head>` 里由 overrides/main.html 放了一份
 * `<script id="__rwr" type="application/json">`：
 *
 *   languages  ← config.extra.alternate（与页眉那个语言切换器**同源**），每项有
 *                name（「简体中文」）、link（网址前缀）、lang（BCP-47）
 *   ui         ← zensical.toml 里 search_text / search_filters / … 按页面语言取好的那份
 *                （后缀约定与页脚那几组文案一样）
 *
 * 所以**加一种语言只动 zensical.toml**：加一条 `[[project.extra.alternate]]`、
 * 补一组 `_<lang>` 的 search_* 文案。这个文件一行都不用改；取不到那份配置就
 * 什么都不做（宁可没有分段，也不要猜错语言名）。
 *
 * 为什么写成这样
 * ---------------
 * 搜索面板是主题用 preact 渲染进一个 **shadow root** 的，本站改不到它的模板
 * （模板在 JS 里），所以这里的每一样都是**事后摆上去**的：
 *
 *   · 定位一律走**结构**（input[role=combobox] → 父 → 祖父 → …），不认它那些
 *     一个字母的类名——那是压缩产物，升级主题就会变；
 *   · **主题的节点一个都不搬**。原先那一版把原生 <li> 搬进自己那几列里——抄是
 *     省事，但那列 DOM 是 preact 的：一搜索，主题就把标签清单按结果重算一遍
 *     （只剩命中的几个），而我们搬走的那些它既删不掉、也不知道该留，
 *     于是筛选栏越搜越空，清空关键字也回不来。现在只**加一个类**把它藏起来，
 *     自己那一列按当前的原生清单**重新派生**（抄），点一下转发给原生那一条。
 *   · preact 每次重画都可能把清单换掉、把文案改回英文；MutationObserver 盯着，
 *     对不上就再摆一次（写入前先比较，不会自己触发自己）；
 *   · 结构对不上、配置取不到，就都不做事，绝不改一半。
 *
 * ⚠️ 主题会按当前的搜索结果**过滤**标签清单（搜「墙」时只剩 5 个标签），这是它
 * 本来就有的行为，不是缺陷；我们要做的只是跟着它变，不要跟它抢 DOM。
 *
 * 标签属于哪种语言，是从 search.json 的 `tags` 字段反查出来的，不另立一张表；
 * 查不到的标签（刚加、还没进索引的）归到当前语言那一段。
 */
(function () {
  "use strict";

  // ── 配置：本站有哪几种语言、面板上那几个词怎么说 ──────────────────────

  /** 读 <head> 里那份配置。取不到返回 null —— 下面一律「不做事」。 */
  function readConfig() {
    var node = document.getElementById("__rwr");
    if (!node) return null;
    var data;
    try { data = JSON.parse(node.textContent); } catch (e) { return null; }
    if (!data || !data.ui || !Array.isArray(data.languages)) return null;

    var langs = [];
    data.languages.forEach(function (alt) {
      if (!alt || !alt.name) return;
      // alternate 的 link 是网址前缀：默认语言 "./"，其余 "zh-hant/"、"en/"。
      var prefix = String(alt.link || "./").replace("./", "").replace(/^\/+|\/+$/g, "");
      langs.push({ id: prefix, name: alt.name, code: alt.lang || prefix });
    });
    if (!langs.length) return null;
    return { langs: langs, ui: data.ui };
  }

  var CONF = readConfig();
  if (!CONF) return;                                   // 没有配置就不动手

  var LANGS = CONF.langs;
  var S = CONF.ui;
  var DEFAULT_LANG = (LANGS.filter(function (l) { return l.id === ""; })[0] || LANGS[0]).id;

  // 脚本自己网址的上一层就是站点根：search.json 在那里。
  // ⚠️ 索引里的 location 是**相对站点根**的（`editor/keys/`），判断它属于哪种语言
  //    必须相对站点根去解——相对当前页去解会解成 `/editor/keys/en/…`，
  //    语言段被挤出前两段，于是每个标签都被判成默认语言。
  var SCRIPT_SRC = document.currentScript ? document.currentScript.src : null;
  var BASE = SCRIPT_SRC ? new URL("../", SCRIPT_SRC) : new URL("./", location.href);

  // 样式注进 shadow root：外面的样式表穿不过去。
  // 变量（--space-*、--color-*、--alpha-*）由面板自己的 .e 定好，跟着主题走。
  // 段标题照抄主题标签清单那一行的观感（14px、半透明、padding 8px）。
  var CSS = [
    ".dsl-h{font-size:14px;font-weight:400;opacity:.5;padding:8px;margin:4px 0 0}",
    ".dsl-list{display:flex;flex-direction:column;gap:2px;list-style:none;padding:0;margin:0}",
    ".dsl-off{display:none}"
  ].join("");

  var TAG_LANGS = null;   // { 标签名: { 语言 id: true } }
  var shell = null;       // 我们那一列：{ inner, groups: [{lang, head, list}] }
  var lastSig = null;     // 上一次是照着哪份原生清单摆的；没变就不重摆

  /** 一条网址属于哪种语言：看路径前两段里出现了哪个语言前缀。 */
  function langOf(pathname) {
    var seg = pathname.split("/").filter(Boolean).slice(0, 2);
    for (var i = 0; i < LANGS.length; i++) {
      if (LANGS[i].id && seg.indexOf(LANGS[i].id) >= 0) return LANGS[i].id;
    }
    return DEFAULT_LANG;
  }

  var home = langOf(location.pathname);                // 当前页面的语言

  /** 当前语言排最前，其余按配置里的顺序。 */
  function order() {
    return LANGS.filter(function (l) { return l.id === home; })
      .concat(LANGS.filter(function (l) { return l.id !== home; }));
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function searchRoot() {
    var children = document.body ? document.body.children : [];
    for (var i = 0; i < children.length; i++) {
      var root = children[i].shadowRoot;
      if (root && root.querySelector('input[role="combobox"]')) return root;
    }
    return null;
  }

  /** 标签条目的文字：主题把它拆成「名字」与「条数」两个 span。 */
  function tagName(li) {
    var span = li.querySelector("span");
    var text = (span ? span.textContent : li.textContent) || "";
    return text.replace(/\s+/g, " ").trim().replace(/\d+$/, "").trim();
  }

  /** 面板现在在哪：每次都重新找一遍——preact 会把这一带的元素整个换掉。 */
  function locate() {
    var root = searchRoot();
    if (!root) return null;
    var input = root.querySelector('input[role="combobox"]');
    var controls = input && input.parentElement && input.parentElement.parentElement;
    var content = controls && controls.parentElement;
    var sidebar = content && content.nextElementSibling;
    var h3 = sidebar && sidebar.querySelector("h3");
    var inner = h3 && h3.parentElement;
    if (!inner) return null;

    // 原生清单 = 这个侧栏里**不属于我们**的第一个 ol：我们那几列都带 dsl-list。
    // 按类名认主题的 `.F` 是不行的（压缩产物），按位置找又会随主题改版而错。
    var native = null;
    var ols = inner.querySelectorAll("ol");
    for (var i = 0; i < ols.length; i++) {
      if (!ols[i].classList.contains("dsl-list")) { native = ols[i]; break; }
    }
    if (!native) return null;

    return { root: root, inner: inner, native: native, h3: h3,
             tagsHead: inner.querySelector("h4") };
  }

  /** 摆出「一种语言一列」的空壳。壳被 preact 拆掉时会再摆一次。 */
  function buildShell(P) {
    if (!P.root.querySelector("style.dsl-style")) {
      var style = el("style", "dsl-style");
      style.textContent = CSS;
      P.root.appendChild(style);
    }
    var groups = order().map(function (lang) {
      var head = el("h4", "dsl-h", lang.name);
      var list = el("ol", "dsl-list");
      P.inner.appendChild(head);
      P.inner.appendChild(list);
      return { lang: lang.id, head: head, list: list };
    });
    return { inner: P.inner, groups: groups };
  }

  /** 一条标签属于哪种语言；查不到就归当前语言（刚加、还没进索引的）。 */
  function langOfTag(name) {
    var known = TAG_LANGS && TAG_LANGS[name];
    if (!known) return home;
    for (var i = 0; i < LANGS.length; i++) {
      if (known[LANGS[i].id]) return LANGS[i].id;
    }
    return home;
  }

  /** 原生清单的「指纹」：名字、全文（含条数）、当前是否选中的那一条。 */
  function signature(items) {
    return items.map(function (li) {
      return tagName(li) + "|" + li.textContent.replace(/\s+/g, " ") + "|" + li.className;
    }).join("\n");
  }

  /** 照着当前的原生清单，把我们那一列重摆一遍。 */
  function paint(items) {
    var columns = {};
    shell.groups.forEach(function (group) {
      group.list.textContent = "";               // 只清自己那一列，主题的碰都不碰
      columns[group.lang] = group.list;
    });

    items.forEach(function (nativeItem) {
      var name = tagName(nativeItem);
      var column = columns[langOfTag(name)] || columns[home];
      var item = nativeItem.cloneNode(true);
      // 点我们自己这一条 = 点主题那一条。名字是**现查**的：主题随时会把整份
      // 清单换掉，手里攥着一个旧节点就会点空。抄出来的没有主题的事件监听，
      // 所以由这里转发过去，过滤逻辑仍旧是主题自己的那一套。
      item.addEventListener("click", function (event) {
        event.preventDefault();
        forward(name);
      });
      column.appendChild(item);
    });

    // 这种语言在这个查询下一个标签都没有，就整段收起来。
    shell.groups.forEach(function (group) {
      var empty = group.list.children.length === 0;
      group.list.classList.toggle("dsl-off", empty);
      group.head.classList.toggle("dsl-off", empty);
    });
  }

  /** 把点击交给主题里对应的那一条。 */
  function forward(name) {
    var P = locate();
    if (!P) return;
    var items = Array.prototype.slice.call(P.native.children);
    for (var i = 0; i < items.length; i++) {
      if (tagName(items[i]) === name) { items[i].click(); return; }
    }
  }

  /**
   * 主循环：看主题现在摆的是什么，跟上它。
   *
   * ⚠️ 主题会按**当前结果**过滤标签清单（搜「墙」时只剩 5 个标签），也会在
   *    每一次输入之后重摆一遍。所以这里不缓存任何主题的节点，每次都重新找、
   *    重新抄——**跟它抢 DOM 就会输**（上一版就是搬走节点，结果越搜越空）。
   */
  function sync() {
    var P = locate();
    if (!P) return;
    if (!shell || shell.inner !== P.inner || !shell.groups[0].list.isConnected) {
      shell = buildShell(P);
      lastSig = null;                            // 壳是新摆的，内容得重来
    }

    // 主题自己那一行「Tags」与原生清单都收起来：只加类，不搬它的节点。
    if (P.tagsHead) P.tagsHead.classList.add("dsl-off");
    P.native.classList.add("dsl-off");

    var items = Array.prototype.slice.call(P.native.children);
    var sig = signature(items);
    if (sig === lastSig) return;
    lastSig = sig;
    paint(items);
  }

  /** 面板上写死的英文，换成配置里这份文案。 */
  function localize() {
    var P = locate();
    if (!P) return;
    var input = P.root.querySelector('input[role="combobox"]');
    if (input && input.placeholder !== S.search) input.placeholder = S.search;

    var buttons = P.root.querySelectorAll("button");
    for (var i = 0; i < buttons.length; i++) {
      if (i === 0 && buttons[i].getAttribute("aria-label") !== S.close) buttons[i].setAttribute("aria-label", S.close);
      if (i === buttons.length - 1 && buttons[i].getAttribute("aria-label") !== S.tag) buttons[i].setAttribute("aria-label", S.tag);
    }

    if (P.h3 && P.h3.textContent.trim() !== S.filters) P.h3.textContent = S.filters;

    // 结果数那一行：「12 results」的数字由主题维护，这里只把词换掉。
    var scope = P.inner.parentElement && P.inner.parentElement.parentElement;
    var nodes = (scope || P.root).querySelectorAll("h3");
    for (var j = 0; j < nodes.length; j++) {
      if (nodes[j] === P.h3) continue;
      Array.prototype.forEach.call(nodes[j].childNodes, function (child) {
        if (child.nodeType === 3 && /results|条结果|條結果/.test(child.nodeValue)) {
          var want = " " + S.results;
          if (child.nodeValue !== want) child.nodeValue = want;
        }
      });
    }
  }

  /** 从 search.json 反查「哪个标签属于哪种语言」。 */
  function learnTags(done) {
    try {
      fetch(new URL("search.json", BASE)).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (data) {
          if (!data || !data.items) return;
          var map = Object.create(null);
          data.items.forEach(function (item) {
            if (!item.tags || !item.tags.length) return;
            var lang = langOf(new URL(item.location || "", BASE).pathname);
            item.tags.forEach(function (tag) { (map[tag] || (map[tag] = {}))[lang] = true; });
          });
          TAG_LANGS = map;
          if (done) done();
        })
        .catch(function () { /* 拿不到就不分段，其余照旧 */ });
    } catch (e) { /* 同上 */ }
  }

  function mount(root) {
    if (root.__dsl) return;
    root.__dsl = true;

    // 面板这一刻可能还没把侧栏渲染出来；不要在这里放弃收工——
    // 下面的 MutationObserver 盯着整个 shadow root，侧栏一出现就会再 sync 一次。
    sync();
    localize();
    learnTags(function () { lastSig = null; sync(); });

    var queued = false;
    new MutationObserver(function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        // preact 重画会换掉清单、把文案改回英文。sync() 里比对指纹，
        // 没变就什么也不写，所以不会自己触发自己。
        sync();
        localize();
      });
    }).observe(root, { childList: true, subtree: true, characterData: true });
  }

  function start() {
    // 面板是 bundle 初始化时才挂上来的，而且它渲染进 shadow root——
    // 那一步不会在 document.body 上冒泡出任何 mutation，所以得轮询几秒：
    // 先出现的可能只是 shadow host，里面还没有输入框。
    var tries = 0;
    var timer = setInterval(function () {
      var root = searchRoot();
      if (root) { clearInterval(timer); return mount(root); }
      if (++tries > 60) clearInterval(timer);
    }, 250);
    var root = searchRoot();
    if (root) { clearInterval(timer); mount(root); }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
