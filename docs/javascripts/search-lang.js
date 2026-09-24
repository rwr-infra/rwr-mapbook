/**
 * 搜索面板：标签按语言分段 + 面板文案跟着语言走
 * ===========================================================================
 * 要做的事
 * ---------
 * 本站一份内容有三种语言（简体 / 繁體 / English），而搜索索引 `search.json`
 * 是**整站一份**的，面板上的标签清单也是一锅端的：三种语言的标签混在同一个
 * 列表里，看不出谁是谁的。这个脚本补两件事：
 *
 *   1. **筛选栏里的标签按语言分段**：一种语言一段，段标题就是语言名，而
 *      **当前页面的语言排在最前**——一打开搜索就先看到自己这一种。
 *      点击照旧走主题原生的标签筛选：那些条目是从原生列表里**搬**过来的，
 *      事件监听是它们自己的，这里只负责把它们归位。
 *   2. **面板界面上的文案跟着页面语言走**（主题的搜索面板写死英文）。
 *
 * 为什么写成这样
 * ---------------
 * 搜索面板是主题用 preact 渲染进一个 **shadow root** 的，本站改不到它的模板
 * （模板在 JS 里），所以这里的每一样都是**事后摆上去**的：
 *
 *   · 定位一律走**结构**（input[role=combobox] → 父 → 祖父 → …），不认它那些
 *     一个字母的类名——那是压缩产物，升级主题就会变；
 *   · 标签条目是**搬**（move）不是抄（clone）：抄出来的没有事件监听，点了没反应；
 *   · preact 每次重画都可能把新条目塞回原生列表、把文案改回英文；
 *     MutationObserver 盯着，对不上就再摆一次（写入前先比较，不会自己触发自己）；
 *   · 结构对不上就**什么都不做**：宁可没有分段，也不要半截 DOM 或报错。
 *
 * 标签属于哪种语言，是从 search.json 的 `tags` 字段反查出来的，不另立一张表；
 * 查不到的标签（刚加、还没进索引的）归到当前语言那一段。
 *
 * 加语言时要改哪里
 * -------------------
 * 只改 LANGS 与 STRINGS。判据是「网址前两段里出现了哪个语言目录名」——
 * 版本段可能排在语言段前面（`/egg/en/…`），所以看两段。
 */
(function () {
  "use strict";

  // 语言目录名与显示名。zh-hans 是默认语言，网址上没有前缀。
  var LANGS = [
    { id: "zh-hans", label: "简体" },
    { id: "zh-hant", label: "繁體" },
    { id: "en", label: "English" }
  ];

  // 面板界面上跟着语言走的那几个词。主题只给了英文，这里按页面语言换掉。
  var STRINGS = {
    "zh-hans": { search: "搜索", filters: "筛选", close: "关闭搜索", filter: "按标签筛选", results: "条结果" },
    "zh-hant": { search: "搜尋", filters: "篩選", close: "關閉搜尋", filter: "依標籤篩選", results: "條結果" },
    "en": { search: "Search", filters: "Filters", close: "Close search", filter: "Filter by tag", results: "results" }
  };

  // 脚本自己的网址：search.json 就在它上一层的站点根。
  // 必须**同步**取，之后 document.currentScript 就是 null 了。
  // ⚠️ 索引里的 location 是**相对站点根**的（`editor/keys/`），判断它属于哪种语言
  //    必须相对站点根去解——相对当前页去解就会解成 `/editor/keys/en/…`，
  //    语言段被挤到前两段之外，于是每一个标签都被判成默认语言。
  var SCRIPT_SRC = document.currentScript ? document.currentScript.src : null;
  var BASE = SCRIPT_SRC ? new URL("../", SCRIPT_SRC) : new URL("./", location.href);

  var PREFIXES = LANGS.map(function (l) { return l.id; }).filter(function (id) { return id !== "zh-hans"; });

  // 样式注进 shadow root：外面的样式表穿不过去。
  // 变量（--space-*、--color-*、--alpha-*）由面板自己的 .e 定好，跟着主题走。
  // 段标题照抄主题标签清单那一行的观感（14px、半透明、padding 8px）。
  var CSS = [
    ".dsl-h{font-size:14px;font-weight:400;opacity:.5;padding:8px;margin:4px 0 0}",
    ".dsl-list{display:flex;flex-direction:column;gap:2px;list-style:none;padding:0;margin:0}",
    ".dsl-off{display:none}"
  ].join("");

  var TAG_LANGS = null;   // { 标签名: { 语言: true } }
  var parts = null;

  /** 一条网址属于哪种语言：看路径前两段。 */
  function langOf(pathname) {
    var seg = pathname.split("/").filter(Boolean).slice(0, 2);
    for (var i = 0; i < seg.length; i++) {
      if (PREFIXES.indexOf(seg[i]) >= 0) return seg[i];
    }
    return "zh-hans";
  }

  var home = langOf(location.pathname);          // 当前页面的语言
  var S = STRINGS[home] || STRINGS.en;

  /** 当前语言排最前，其余按 LANGS 原序。 */
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

  /** 标签条目的文字：主题把它拆成「名字」和「条数」两个 span。 */
  function tagName(li) {
    var span = li.querySelector("span");
    var text = (span ? span.textContent : li.textContent) || "";
    return text.replace(/\s+/g, " ").trim().replace(/\d+$/, "").trim();
  }

  function build(root) {
    var input = root.querySelector('input[role="combobox"]');
    var controls = input && input.parentElement && input.parentElement.parentElement;
    var content = controls && controls.parentElement;
    var sidebar = content && content.nextElementSibling;
    var inner = sidebar && sidebar.querySelector("h3");
    inner = inner && inner.parentElement;
    if (!inner) return null;

    // 原生结构：[h3「Filters」, h4「Tags」, 标签清单 ol]
    var h3 = inner.querySelector("h3");
    var tagsHead = inner.querySelector("h4");
    var native = null;
    if (tagsHead) {
      for (var n = tagsHead.nextElementSibling; n; n = n.nextElementSibling) {
        if (n.tagName === "OL") { native = n; break; }
      }
    }
    if (!native) {
      var lists = inner.querySelectorAll("ol");
      if (lists.length) native = lists[lists.length - 1];
    }
    if (!native) return null;

    var style = el("style");
    style.textContent = CSS;
    root.appendChild(style);

    // 段标题就是语言名，原生的「Tags」那一行因此多余；原生清单也空掉（条目都搬走了）。
    if (tagsHead) tagsHead.classList.add("dsl-off");
    native.classList.add("dsl-off");

    var groups = order().map(function (lang) {
      var head = el("h4", "dsl-h", lang.label);
      var list = el("ol", "dsl-list");
      inner.appendChild(head);
      inner.appendChild(list);
      return { lang: lang.id, head: head, list: list };
    });

    return { root: root, inner: inner, native: native, groups: groups, h3: h3 };
  }

  /** 把标签条目归位到各自语言的段里；preact 新塞进原生清单的也一并归位。 */
  function regroup(P) {
    var loose = Array.prototype.slice.call(P.native.children);
    P.groups.forEach(function (g) {
      Array.prototype.forEach.call(g.list.children, function (li) {
        if (loose.indexOf(li) < 0) loose.push(li);
      });
    });

    loose.forEach(function (li) {
      var name = tagName(li);
      var known = TAG_LANGS && TAG_LANGS[name];
      var lang = home;
      if (known) {
        for (var i = 0; i < LANGS.length; i++) {
          if (known[LANGS[i].id]) { lang = LANGS[i].id; break; }
        }
      }
      for (var k = 0; k < P.groups.length; k++) {
        if (P.groups[k].lang !== lang) continue;
        if (!P.groups[k].list.contains(li)) P.groups[k].list.appendChild(li);
        return;
      }
    });

    // 空段（这种语言在这个查询下一个标签都没有）收起来
    P.groups.forEach(function (g) {
      var empty = g.list.children.length === 0;
      g.list.classList.toggle("dsl-off", empty);
      g.head.classList.toggle("dsl-off", empty);
    });
  }

  /** 面板上写死的英文，按页面语言换掉。 */
  function localize(P) {
    var input = P.root.querySelector('input[role="combobox"]');
    if (input && input.placeholder !== S.search) input.placeholder = S.search;

    var buttons = P.root.querySelectorAll("button");
    for (var i = 0; i < buttons.length; i++) {
      if (i === 0 && buttons[i].getAttribute("aria-label") !== S.close) buttons[i].setAttribute("aria-label", S.close);
      if (i === buttons.length - 1 && buttons[i].getAttribute("aria-label") !== S.filter) buttons[i].setAttribute("aria-label", S.filter);
    }

    if (P.h3 && P.h3.textContent.trim() !== S.filters) P.h3.textContent = S.filters;

    // 结果数那一行：「12 results」的数字由主题维护，这里只把词换掉。
    var head = P.inner.parentElement && P.inner.parentElement.parentElement;
    var nodes = (head || P.root).querySelectorAll("h3");
    for (var j = 0; j < nodes.length; j++) {
      var node = nodes[j];
      if (node === P.h3) continue;
      Array.prototype.forEach.call(node.childNodes, function (child) {
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
      var url = new URL("search.json", BASE);
      fetch(url).then(function (r) { return r.ok ? r.json() : null; }).then(function (data) {
        if (!data || !data.items) return;
        var map = Object.create(null);
        data.items.forEach(function (item) {
          if (!item.tags || !item.tags.length) return;
          var lang = langOf(new URL(item.location || "", BASE).pathname);
          item.tags.forEach(function (tag) { (map[tag] || (map[tag] = {}))[lang] = true; });
        });
        TAG_LANGS = map;
        if (done) done();
      }).catch(function () { /* 拿不到就不分段，其余照旧 */ });
    } catch (e) { /* 同上 */ }
  }

  function mount(root) {
    if (root.__dsl) return;
    parts = build(root);
    if (!parts) { parts = null; return; }
    root.__dsl = true;
    localize(parts);
    learnTags(function () { if (parts) regroup(parts); });

    var queued = false;
    new MutationObserver(function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        if (!parts) return;
        // preact 重画可能把标题改回英文、把清单换掉；换掉了就重搭一遍。
        if (!parts.native.isConnected || !parts.groups[0].head.isConnected) {
          parts = build(root);
          if (!parts) return;
        }
        localize(parts);
        regroup(parts);
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
