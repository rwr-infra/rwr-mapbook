/**
 * 下载链接：点了直接存成文件，而不是被浏览器打开。
 *
 * 为什么需要它
 * ------------
 * 归档与配套材料放在站外（assets.rwr-infra.uk，Cloudflare R2）上，每一条都是直链。
 * 而 `<a download>` 只对**同源**链接生效——跨域时这个属性被浏览器忽略
 * （Chrome 65+ 与 Firefox 都是这么定的），于是 zip / rar 照常下载（浏览器渲染不了
 * 它们），唯独 `vao0822.svg` 会露馅：浏览器认识 image/svg+xml，一点就把图打开，
 * 存不下来。
 *
 * 所以这里接手：标了 `download` 的跨域链接，改成 fetch 回来、做成 blob 再存。
 * blob: 是同源的，download 属性到这一步才真正管用。R2 上那条
 * `access-control-allow-origin: https://rwrme.rwr-infra.uk` 正是这条请求要用的。
 *
 * 两个判据各管一件事，别合并
 * --------------------------
 *   · `a[download]` 是**意图**——只有作者标了的才接管。站内直接链一张图给读者看的
 *     （表页那些预览）不在此列，不能顺手把它们也变成下载。
 *   · 后缀在 INLINE 里是**兜底**——浏览器本来就下载的文件不必我们插手；少了这一条，
 *     哪天有人给 318 MB 的整包也补上 download，fetch 会把整份读进内存。
 *
 * 取不到就照旧
 * ------------
 * 本地预览（127.0.0.1）与离线包都不在那条 CORS 白名单里，fetch 会被浏览器拦下。
 * 这时不去假装成功，而是退回原来的行为——跳转过去，让浏览器打开它。
 * 本地看到旧行为，好过这里静默地什么都不做。
 *
 * 用事件委托：内容页是整页替换的（主题的 instant navigation），
 * 逐条挂监听会在换页后全丢，委托到 document 就不会（同 redact.js）。
 */
(function () {
  "use strict";

  // 浏览器会**内联打开**的那几类，也就只有它们需要我们插手。
  var INLINE = ["svg", "png", "jpg", "jpeg", "gif", "webp", "avif", "bmp", "ico", "pdf"];

  function nameOf(anchor, url) {
    var hint = anchor.getAttribute("download") || "";
    // 属性裸写成 `download` 时，attr_list 给的值就是 "download"，那不是文件名。
    if (hint && hint !== "download") return hint;
    return decodeURIComponent(url.pathname.split("/").pop() || "download");
  }

  function save(blob, name) {
    var objectUrl = URL.createObjectURL(blob);
    var saver = document.createElement("a");
    saver.href = objectUrl;
    saver.download = name;
    document.body.appendChild(saver);
    saver.click();
    saver.remove();
    // 立刻 revoke 会在部分浏览器里把下载掐掉，等它起步了再放。
    setTimeout(function () { URL.revokeObjectURL(objectUrl); }, 60000);
  }

  document.addEventListener("click", function (event) {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    var anchor = event.target && event.target.closest
      ? event.target.closest("a[download][href]")
      : null;
    if (!anchor) return;
    if (anchor.target && anchor.target !== "_self") return;

    var url;
    try {
      url = new URL(anchor.href, document.baseURI);
    } catch (e) {
      return;
    }
    // 同源：download 属性本来就生效，交给浏览器。
    if (url.origin === window.location.origin) return;
    if (INLINE.indexOf(url.pathname.split(".").pop().toLowerCase()) === -1) return;

    event.preventDefault();
    fetch(url.href, { credentials: "omit" })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.blob();
      })
      .then(function (blob) {
        save(blob, nameOf(anchor, url));
      })
      .catch(function () {
        // 多半是当前源不在 R2 的 CORS 白名单里：退回原行为。
        window.location.href = anchor.href;
      });
  });
})();
