/**
 * 缩写注释（<abbr title="…">）：点一下就显示解释，再点一下或点别处就收。
 *
 * 为什么要有它
 * ------------
 * <abbr title> 桌面端悬停即显，手机端却要**长按**才显——长按还会顺手把文字
 * 选中，等于没有。这里把交互统一成「点按切换」：
 *   · 点 abbr → 弹出气泡显示解释；再点它一下、点页面别处、滚动或换向 → 收起；
 *   · title 属性在第一次交互时挪到 aria-label 上——长按不再触发浏览器
 *     自带的那套，桌面端也统一走这个气泡（读屏用户不受影响）。
 *
 * 用事件委托（同 redact.js / table-tools.js）：换页不丢监听。
 * 气泡只有一个实例，挂在 body 下、按视口定位（position: fixed）。
 * 样式在 docs/stylesheets/extra.css 的「缩写注释」那一段。
 */
(function () {
  "use strict";

  var tip = null;
  var current = null;
  var openedAt = 0;

  function close() {
    if (tip) { tip.remove(); tip = null; }
    if (current) { current.removeAttribute("data-tip-open"); current = null; }
  }

  // 平滑滚动/惯性滚动的 scroll 事件可能晚于 click 到达——刚弹开就被关掉。
  // 弹开后的这一小段时间里忽略 scroll，过了宽限期滚动才收气泡。
  function closeOnScroll() {
    if (Date.now() - openedAt > 300) close();
  }

  function open(abbr) {
    close();
    var text = abbr.getAttribute("title") || abbr.getAttribute("aria-label") || "";
    if (!text) return;
    // title 挪到 aria-label：手机长按不再弹浏览器自带的那份，语义还在
    abbr.removeAttribute("title");
    abbr.setAttribute("aria-label", text);

    tip = document.createElement("span");
    tip.className = "abbr-tip";
    tip.setAttribute("role", "tooltip");
    tip.textContent = text;
    document.body.appendChild(tip);

    var rect = abbr.getBoundingClientRect();
    var tw = tip.offsetWidth;
    var th = tip.offsetHeight;
    var left = rect.left + rect.width / 2 - tw / 2;
    left = Math.max(8, Math.min(left, window.innerWidth - tw - 8));
    var top = rect.top - th - 8;
    if (top < 8) top = rect.bottom + 8;
    tip.style.left = left + "px";
    tip.style.top = top + "px";

    current = abbr;
    openedAt = Date.now();
  }

  document.addEventListener("click", function (event) {
    var abbr = event.target && event.target.closest
      ? event.target.closest("abbr[title], abbr[aria-label]")
      : null;
    if (abbr) {
      if (abbr === current) close();
      else open(abbr);
    } else {
      close();
    }
  });

  window.addEventListener("scroll", closeOnScroll, true);
  window.addEventListener("resize", close);
})();
