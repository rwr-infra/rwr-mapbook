/**
 * 历史版本归档：一次点击，把分片取回来、校验、拼成一个整文件
 * ===========================================================================
 * 分片是**托管方的限制**，不是内容
 * --------------------------------
 * 仓库托管的地编归档比托管方允许的单文件上限大（GitHub 网页上传是 25 MB），
 * 所以它们在仓库里是一堆 `<名字>.partNNN`。这个脚本把这件事**对读者藏起来**：
 * 点一次「下载」，分片逐个取回、逐个校验哈希，拼成一个 Blob，
 * 以一个**与原文件同名**的文件存下去——读者的下载文件夹里出现的是 `060.zip`，
 * 不需要手工合并，也不需要命令行工具。分片名不在页面上露面。
 *
 * 校验
 * ----
 * 清单 `downloads/manifest.json`（由 tools/chunker.py 生成）记着每片与整个文件的
 * sha256。**逐片校验**：任何一片对不上就停下报错，不把半个文件塞给读者。
 * 整文件再核一次——那是最强的一条保证：拿到的东西与当初发的东西逐字节相同。
 *
 * crypto.subtle 只在安全上下文（https 或 localhost）里存在。取不到就**不校验**，
 * 照常拼接保存，并在状态行里说明——宁可少一道校验，也不要让读者以为下载坏了。
 * （本地预览在 127.0.0.1 上算安全上下文，所以这条路平时用不到。）
 *
 * 文案从哪儿来
 * ------------
 * 与搜索面板同一套：`<head>` 里的 `<script id="__rwr" type="application/json">`
 * 由 overrides/main.html 按页面语言取好 `download_*` 那几条传下来。
 * **语言清单不写在这个文件里**；取不到配置就只是没有状态文字，照常下载。
 */
(function () {
  "use strict";

  var SCRIPT = document.currentScript;
  if (!SCRIPT) return;

  // 站点根。这个脚本永远在 <站点根>/javascripts/ 下（各语言、各版本的页共用同一份，
  // 由模板按语言层级补 `../`），所以拿它自己的地址退一层就是根。
  // 清单里的分片路径是相对站点根的，两者一拼才有绝对地址。
  var BASE = new URL("../", SCRIPT.src);
  var MANIFEST_URL = new URL("downloads/manifest.json", BASE);

  var ui = readUi();
  var busy = false;

  function readUi() {
    var node = document.getElementById("__rwr");
    if (!node) return {};
    try {
      var data = JSON.parse(node.textContent);
      return (data && data.download) || {};
    } catch (e) {
      return {};
    }
  }

  /** 把 `{n}` 这类占位符换掉。取不到那一条文案就返回空串——不猜词。 */
  function say(node, template, vars) {
    if (!node) return;
    var text = template || "";
    if (vars) {
      Object.keys(vars).forEach(function (key) {
        text = text.replace("{" + key + "}", vars[key]);
      });
    }
    node.textContent = text;
  }

  /** 字节数按**十进制**换算，与 tools/chunker.py 打印的那一栏同一套口径。 */
  function human(bytes) {
    if (bytes < 1e6) return (bytes / 1e3).toFixed(0) + " kB";
    return (bytes / 1e6).toFixed(1) + " MB";
  }

  function hex(buffer) {
    return Array.prototype.map
      .call(new Uint8Array(buffer), function (byte) {
        return byte.toString(16).padStart(2, "0");
      })
      .join("");
  }

  function sha256(buffer) {
    return crypto.subtle.digest("SHA-256", buffer).then(hex);
  }

  function find(id) {
    var files = (window.__rwrDownloads || {}).files || [];
    for (var i = 0; i < files.length; i++) {
      if (files[i].id === id) return files[i];
    }
    return null;
  }

  function save(blob, name) {
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = name;
    document.body.appendChild(link);
    link.click();
    link.remove();
    // 立刻回收会让个别浏览器来不及取走数据，留一分钟。
    setTimeout(function () { URL.revokeObjectURL(url); }, 60000);
  }

  /**
   * 逐个取分片。**串行**，不并发：顺序拼接要求顺序到达，而并发只会让进度乱跳、
   * 顺带把读者的带宽切成几份。一次点一份归档，够了。
   */
  function collect(entry, status) {
    var chunks = [];
    var index = 0;
    var secure = window.isSecureContext && window.crypto && crypto.subtle;

    function next() {
      if (index >= entry.parts.length) return Promise.resolve(chunks);
      var part = entry.parts[index];
      index += 1;
      say(status, ui.progress, { n: index, m: entry.parts.length });
      return fetch(new URL(part.path, BASE), { cache: "no-store" })
        .then(function (response) {
          if (!response.ok) throw new Error(part.path + " → HTTP " + response.status);
          return response.arrayBuffer();
        })
        .then(function (buffer) {
          if (buffer.byteLength !== part.bytes) {
            throw new Error(part.path + " 长度是 " + buffer.byteLength + "，应为 " + part.bytes);
          }
          if (!secure) return buffer;
          return sha256(buffer).then(function (got) {
            if (got !== part.sha256) throw new Error(part.path + " 的哈希与清单不符");
            return buffer;
          });
        })
        .then(function (buffer) {
          chunks.push(buffer);
          return next();
        });
    }

    return next().then(function (parts) {
      return { parts: parts, secure: !!secure };
    });
  }

  function start(button, entry) {
    if (busy) return;
    busy = true;
    button.disabled = true;

    var row = button.closest("tr") || button.parentNode;
    var status = row ? row.querySelector("[data-dl-status]") : null;

    collect(entry, status)
      .then(function (result) {
        var blob = new Blob(result.parts);
        if (!result.secure || !entry.sha256) return { blob: blob, secure: result.secure };
        say(status, ui.verify);
        // 整文件再核一次。多一份内存副本，换「与当初发的逐字节相同」这条保证——
        // 三十兆级别值这个价；将来真有几百兆的文件，这里换成流式写入。
        return blob.arrayBuffer().then(function (whole) {
          return sha256(whole).then(function (got) {
            if (got !== entry.sha256) throw new Error("整文件哈希与清单不符");
            return { blob: blob, secure: true };
          });
        });
      })
      .then(function (result) {
        save(result.blob, entry.name);
        say(status, result.secure ? ui.done : ui.unchecked, { name: entry.name });
      })
      .catch(function (error) {
        console.error("[downloads]", error);
        say(status, ui.failed);
      })
      .then(function () {
        busy = false;
        button.disabled = false;
      });
  }

  function wire(manifest) {
    window.__rwrDownloads = manifest;

    document.querySelectorAll("[data-dl-size]").forEach(function (node) {
      var entry = find(node.dataset.dlSize);
      if (entry) node.textContent = human(entry.bytes);
    });

    document.querySelectorAll("[data-dl]").forEach(function (button) {
      var entry = find(button.dataset.dl);
      if (!entry) return;
      button.addEventListener("click", function () { start(button, entry); });
    });
  }

  // 页面上一个按钮都没有（别的页）就不去取清单——那是一次白跑的请求。
  if (!document.querySelector("[data-dl]")) return;

  fetch(MANIFEST_URL, { cache: "no-store" })
    .then(function (response) {
      if (!response.ok) throw new Error(MANIFEST_URL + " → HTTP " + response.status);
      return response.json();
    })
    .then(wire)
    .catch(function (error) {
      // 清单取不到就什么都不做：页面上的按钮保持原样（点了没反应），
      // 而不是把 reader 领进一个半截流程。
      console.error("[downloads]", error);
    });
})();
