/**
 * 遮挡块：`<span class="redact">…</span>` 点一下展开，再点一下收回去。
 *
 * 样式在 docs/stylesheets/extra.css 里（黑块、点开才显字），这里只管交互。
 * 为什么要有它、什么时候用它，写在 extra.css 那一段注释里。
 *
 * 用事件委托：内容页是整页替换的（主题的 instant navigation），
 * 逐块挂监听会在换页后全丢，委托到 document 就不会。
 * 同时接受键盘（Enter / 空格）——它带 tabindex，读屏与键盘用户也能打开。
 */
(function () {
  "use strict";

  function toggle(target) {
    target.classList.toggle("is-open");
  }

  document.addEventListener("click", function (event) {
    var node = event.target && event.target.closest ? event.target.closest(".redact") : null;
    if (node) toggle(node);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Enter" && event.key !== " ") return;
    var node = event.target && event.target.closest ? event.target.closest(".redact") : null;
    if (!node) return;
    event.preventDefault();
    toggle(node);
  });
})();
