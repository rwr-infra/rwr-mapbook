/**
 * 可复制的行内代码：表格里的 `code` 点一下复制它自己。
 *
 * 管哪里
 * ------
 * 表格里（正文表格与 `details`（`???`）折叠块表格）的行内代码：
 *   · 功能介绍页 mapSettings 那张「待校验」表（在折叠块里）；
 *   · 下载页「组件下载」表的文件名（`HangarOnIsland_objects.asmb` 这类）。
 * 别处（正文非表格的行内码、代码块、清单页已有的 .ts-tpl 芯片）一律不动。
 * 下载页那三张 .ts-plain 表（版本/模板）不改：那是归档名，页面本身给了下载按钮。
 *
 * ⚠️ 一格里多个示例是用 `<br>` 隔开的**多个独立 <code>**，所以天然就是
 *    「多个示例分开复制」：点了哪块就只复制哪块，不用读者手动圈选。
 *
 * 行为与回执跟 table-tools.js 的引用值芯片一致：复制成功闪「已复制」，
 * 失败退回 execCommand。用事件委托，换页不丢。
 */
(function () {
  "use strict";

  var TEXT = {
    "zh-hans": { copied: "已复制", copyfail: "复制失败" },
    "zh-hant": { copied: "已複製", copyfail: "複製失敗" },
    en: { copied: "Copied", copyfail: "Copy failed" }
  };

  var HINT = {
    "zh-hans": "点击复制",
    "zh-hant": "點擊複製",
    en: "Click to copy"
  };

  function T() {
    var lang = (document.documentElement.getAttribute("lang") || "").toLowerCase();
    if (lang.indexOf("en") === 0) return { text: TEXT.en, hint: HINT.en };
    if (lang.indexOf("hant") !== -1) return { text: TEXT["zh-hant"], hint: HINT["zh-hant"] };
    return { text: TEXT["zh-hans"], hint: HINT["zh-hans"] };
  }

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
    if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { done(true); },
        function () { done(legacyCopy(text)); }
      );
      return;
    }
    done(legacyCopy(text));
  }

  /* 复制 / 已复制 两个小图标：与清单页芯片（table-tools.js）同一组 material
     图标，观感一致——不然这块行内码看着就跟普通代码一样，没人知道能点。 */
  var SVG_NS = "http://www.w3.org/2000/svg";
  var ICON_COPY = "M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1Z";
  var ICON_CHECK = "M21 7 9 19l-5.5-5.5 1.41-1.41L9 16.17 19.59 5.59 21 7Z";

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

  function decorate(root) {
    // 表格里的行内代码都算（正文表 + 折叠块表），排除下面三类。
    var nodes = root.querySelectorAll("table code");
    var t = T();
    Array.prototype.forEach.call(nodes, function (code) {
      if (code.closest("pre")) return;                 // 代码块整段复制有主题自己的按钮
      if (code.classList.contains("ts-tpl")) return;   // 清单页的芯片已有自己的机制
      if (code.closest(".ts-plain")) return;           // 下载页版本/模板表：那是归档名
      if (code.__cpDone) return;
      code.__cpDone = true;
      code.classList.add("cp-chip");
      code.setAttribute("role", "button");
      code.setAttribute("tabindex", "0");
      code.setAttribute("aria-label", t.hint + " " + code.textContent.replace(/\s+/g, " ").trim());
      code.title = t.hint;
      code.appendChild(icon(ICON_COPY, "cp-icon cp-icon--copy"));
      code.appendChild(icon(ICON_CHECK, "cp-icon cp-icon--done"));
    });
  }

  function flash(node, ok) {
    var text = T().text;
    node.classList.remove("is-copied", "is-failed");
    node.classList.add(ok ? "is-copied" : "is-failed");
    node.setAttribute("data-cp-done", ok ? text.copied : text.copyfail);
    window.clearTimeout(node.__cpTimer);
    node.__cpTimer = window.setTimeout(function () {
      node.classList.remove("is-copied", "is-failed");
    }, 1400);
  }

  /**
   * 实际写进剪贴板的值。
   *
   * ⚠️ 组件名（`.asmb`）**不带后缀复制**：格子里显示的是完整文件名
   *    `HangarOnIsland_objects.asmb`，但复制出来是 `HangarOnIsland_objects`——
   *    `.asmb` 是组件固定的格式后缀，粘到地编里用不上（用户要求的）。
   *    别处的值原样复制，不动。
   */
  function valueOf(node) {
    var text = node.textContent.replace(/\s+/g, " ").trim();
    return text.replace(/\.asmb$/i, "");
  }

  function handleCopy(node) {
    if (!node) return false;
    copyText(valueOf(node), function (ok) { flash(node, ok); });
    return true;
  }

  document.addEventListener("click", function (event) {
    var node = event.target && event.target.closest ? event.target.closest("code.cp-chip") : null;
    if (!node) return;
    if (window.getSelection && String(window.getSelection()).length) return; // 正在选字就不抢
    handleCopy(node);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" && event.key !== " ") return;
    var node = event.target && event.target.closest ? event.target.closest("code.cp-chip") : null;
    if (!node) return;
    event.preventDefault();
    handleCopy(node);
  });

  decorate(document);

  // 主题的 document$（同 table-tools.js）：挂上来之后再补一次
  (function wait() {
    if (window.document$) {
      window.document$.subscribe(function () { decorate(document); });
      return;
    }
    window.setTimeout(wait, 100);
  })();
})();
