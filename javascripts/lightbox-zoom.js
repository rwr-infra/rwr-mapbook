/**
 * 灯箱：滚轮缩放 · 按住拖动 · 单击关闭
 *
 * 为什么自己写
 * ------------
 * GLightbox 3.3.1 自带的图片交互跟本站要的不是一回事：
 *   · 桌面端**没有滚轮缩放**——整个库里 `wheel` 一次都没出现；
 *   · 图片的**单击**是「原尺寸 ⇄ 适配窗口」来回切（源码里的 q 类：
 *     点一下放大、再点一下还原），而本站的单击要用来**关闭预览**；
 *   · 它自带的拖动是「拖着换上一张 / 下一张」，放大之后没有平移手段；
 *   · 库里那套双指缩放的代码虽然在（q 类的 dragStart 里判断了 touchstart），
 *     但**没有一处给它挂触摸监听**——那 5 处 touchstart 全在换图用的滑动类
 *     与特性检测里，所以触摸设备上等于没有缩放。
 *
 * 于是这里不碰它的初始化与 DOM，只在 document 的**捕获阶段**补四条监听：
 *   wheel        以光标为原点缩放当前这张
 *   mousedown/mousemove/mouseup   放大后按住拖动平移
 *   click        图片上单击 → 关闭预览
 *   touchstart/touchmove/touchend 双指缩放（顺带双指平移）、放大后单指平移
 *
 * 当前是哪一张：认库自己的 `.gslide.current`
 * ------------------------------------------
 * ⚠️ 这一点踩过坑，别再改回「按面积挑视口里最大的那张图」。灯箱里所有 slide 都是
 * `position: absolute` 叠在一起、**宽度都是满屏**的，没轮到的那些只是 `opacity: 0`，
 * 几何上照样「在视口里」。实测打开 011 时：010（1809×1067，opacity 0）比 011
 * （971×693，opacity 1）面积大，于是滚轮缩放打在了一张**看不见的图**上——
 * 表现就是「滚轮没反应」，而且越小的图越容易中招。
 * 库自己是给活动 slide 挂 `current` 类的（`.gslide.current{opacity:1;z-index:99999}`），
 * 认它就与显示状态完全一致。当前 slide 没有图（视频 / inline）时返回 null，
 * 那几条监听自然什么都不做。
 *
 * 与 GLightbox 的分工（改这里之前先看这段）
 * ----------------------------------------
 *   · 缩放/平移写在 `<img>` 自己的 transform 上（`translate() scale()`），
 *     不碰 `.gslide-media`——库换图时是把 translate3d 写到 `.gslide-media` 上的，
 *     两者在不同元素上，谁也不盖谁。
 *   · 放大期间给 slide 挂上**库自己的 `zoomed` 类**：库的拖动类 N 与 resize()
 *     都拿这个类判断「现在处于放大状态」，于是「拖动换图」与「重算尺寸」自动
 *     让路，鼠标指针也自动变 grab（见 glightbox.min.css 的 `.zoomed` 那两条）。
 *   · 捕获阶段的监听先于 `<img>` 自己的监听触发，所以一个 stopPropagation
 *     就能让库挂在那张图上的「单击缩放」与「拖动换图」永远收不到事件；
 *     **只在真的拦下这件事时才拦**（放大时的拖动、双指），没放大时的拖动
 *     照旧交给库去换图。按下与松开都要拦：库的拖动类把收尾写在 mouseup 上，
 *     只拦 mousedown 的话，收尾那一下仍会把图上的 transform 抹掉。
 *
 * 拿不到就什么都不做
 * ----------------
 * 灯箱没开着的时候，每条监听都立刻返回、也不 preventDefault，页面照常滚动、
 * 照常点选。将来若换成别的灯箱，这个文件可以直接删掉。
 */
(function () {
  "use strict";

  var MIN = 1; // 缩不放小到适配尺寸以下——再小没有意义，只会四周留白
  var MAX = 8; // 放大上限
  var WHEEL_SENSITIVITY = 0.0016;
  var TAP_SLOP = 6; // 按下到抬起的位移超过它就算「拖了一下」，不再当单击

  var img = null; // 当前被缩放/平移的那张图（灯箱里的 <img>）
  var scale = 1; // 当前倍数
  var tx = 0; // 当前平移，屏幕像素（translate 写在 scale 外层，所以就是像素）
  var ty = 0;

  var drag = null; // 鼠标 / 单指：{ x, y, tx, ty, panning, moved }
  var pinch = null; // 双指：{ distance, x, y }

  function container() {
    return document.querySelector(".glightbox-container");
  }

  function isLightboxImage(el) {
    return !!(el && el.tagName === "IMG" && el.closest && el.closest(".glightbox-container"));
  }

  /** 库标记的活动 slide 里的那张图；灯箱没开、或当前是视频/inline 时返回 null。 */
  function activeImage() {
    var box = container();
    if (!box) return null;
    var slide = box.querySelector(".gslide.current");
    return slide ? slide.querySelector("img") : null;
  }

  /** 擦掉当前这张身上的痕迹，回到适配尺寸。 */
  function forget() {
    if (img) {
      img.style.transform = "";
      img.style.transformOrigin = "";
      img.style.willChange = "";
      var slide = img.closest(".gslide");
      if (slide) slide.classList.remove("zoomed");
    }
    img = null;
    scale = 1;
    tx = 0;
    ty = 0;
    drag = null;
    pinch = null;
  }

  /**
   * 当前这张；换图（含灯箱已关闭）就复位。
   * 复位会把**上一张**的 transform 一并擦掉，所以换到别张再换回来时，
   * 那张不会还停在放大状态。
   */
  function current() {
    var image = activeImage();
    if (!image) {
      if (img) forget();
      return null;
    }
    if (image !== img) {
      forget();
      img = image;
    }
    return img;
  }

  function apply() {
    if (!img) return;
    if (scale === 1 && tx === 0 && ty === 0) {
      // 回到适配尺寸时把属性清干净，别留一个空 transform 挡住库自己的换图位移。
      img.style.transform = "";
      img.style.transformOrigin = "";
      img.style.willChange = "";
    } else {
      img.style.transformOrigin = "50% 50%";
      img.style.transform = "translate(" + tx + "px, " + ty + "px) scale(" + scale + ")";
      img.style.willChange = "transform";
    }
    var slide = img.closest(".gslide");
    if (slide) slide.classList.toggle("zoomed", scale > 1);
  }

  /**
   * 能拖多远：图放大后比视口大出来的那一半。两个方向各自算，
   * 于是图比视口窄的那个方向就钉在正中（拖不动，也不该拖）。
   *
   * ⚠️ 两个坑都在这几行里：
   *   1) getBoundingClientRect 已经把 scale 算进去了，所以**不能**直接拿它
   *      跟视口比——要先除以当前倍数还原出「变形前的布局尺寸」；
   *   2) 调用必须发生在 apply() **之前**、scale 改掉**之前**，否则读到的是上一步
   *      的 rect。第一版就是按旧 rect 算的：刚打开时图是适配尺寸（比视口窄），
   *      算出来「没得拖」，于是第一格滚轮的平移被清成 0，表现为**只放大、不平移**。
   */
  function clampTo(nextScale) {
    if (!img) return;
    var rect = img.getBoundingClientRect();
    var layoutW = rect.width / scale;
    var layoutH = rect.height / scale;
    var maxX = Math.max(0, (layoutW * nextScale - window.innerWidth) / 2);
    var maxY = Math.max(0, (layoutH * nextScale - window.innerHeight) / 2);

    if (tx > maxX) tx = maxX;
    if (tx < -maxX) tx = -maxX;
    if (ty > maxY) ty = maxY;
    if (ty < -maxY) ty = -maxY;
  }

  /**
   * 缩放到 next 倍，并且让「缩放前位于 (refX, refY) 的那个图上的点」
   * 落到 (ax, ay)——滚轮与单指拖动时两者是同一个点（指针指着哪，哪一块留在原地）；
   * 双指时分开传，于是一次调用同时把「指头挪了」也算进去。
   *
   * 推导：设 L 为图**未变形的布局盒**中心（屏幕坐标，只在换图时变），
   * 则图上的点 u 渲染在 L + u·scale + (tx, ty)。要让原来看在 ref 处的那个点
   * 跟到 ax 去，就是解 (ref - L - tx) / scale · next = ax - L - tx'，
   * 整理开就是下面两行。
   */
  function zoomTo(next, ax, ay, refX, refY) {
    if (!img) return;
    next = Math.min(MAX, Math.max(MIN, next));

    var rect = img.getBoundingClientRect();
    var lx = rect.left + rect.width / 2 - tx;
    var ly = rect.top + rect.height / 2 - ty;
    var k = next / scale;

    tx = ax - lx - (refX - lx - tx) * k;
    ty = ay - ly - (refY - ly - ty) * k;

    clampTo(next); // 必须赶在 scale 改掉之前（见 clampTo 的说明）
    scale = next;
    if (scale === MIN) {
      tx = 0;
      ty = 0;
    }
    apply();
  }

  /** 拦下这件事：既不让库的监听收到，也不让浏览器做默认动作。 */
  function take(event) {
    event.preventDefault();
    event.stopPropagation();
  }

  /** 关闭预览。走库自己的关闭按钮，退路是它挂在 window 上的 Esc。 */
  function close() {
    var box = container();
    if (!box) return;

    var button = box.querySelector(".gclose");
    if (button) {
      button.click();
      return;
    }

    var event = new KeyboardEvent("keydown", { key: "Escape", bubbles: true });
    // 库读的是 27 这个数字键码，而 KeyboardEventInit 里没有 keyCode，只能补上。
    Object.defineProperty(event, "keyCode", { get: function () { return 27; } });
    Object.defineProperty(event, "which", { get: function () { return 27; } });
    window.dispatchEvent(event);
  }

  document.addEventListener(
    "wheel",
    function (event) {
      var image = current();
      if (!image) return; // 灯箱没开：这条监听等于不存在，页面照常滚
      event.preventDefault();
      zoomTo(scale * Math.exp(-event.deltaY * WHEEL_SENSITIVITY), event.clientX, event.clientY, event.clientX, event.clientY);
    },
    { passive: false, capture: true }
  );

  document.addEventListener(
    "mousedown",
    function (event) {
      if (event.button !== 0 || !isLightboxImage(event.target)) return;
      var image = current();
      if (!image || image !== event.target) return;

      // 放大之后才拦；没放大时「按住拖」仍然是库的换图，不去动它。
      drag = { x: event.clientX, y: event.clientY, tx: tx, ty: ty, panning: scale > 1, moved: false };
      if (drag.panning) take(event);
    },
    true
  );

  document.addEventListener(
    "mousemove",
    function (event) {
      if (!drag) return;
      var dx = event.clientX - drag.x;
      var dy = event.clientY - drag.y;

      // 不管拦不拦都要记位移：用来区分「单击」和「拖了一下又松开」，
      // 否则拖着换完图，松手时那一下会被当成单击，顺手把预览关掉。
      if (!drag.moved && Math.abs(dx) + Math.abs(dy) > TAP_SLOP) drag.moved = true;
      if (!drag.panning) return;

      take(event);
      if (!drag.moved) return;

      tx = drag.tx + dx;
      ty = drag.ty + dy;
      clampTo(scale);
      apply();
    },
    true
  );

  document.addEventListener(
    "mouseup",
    function (event) {
      // 不清掉 drag：紧随其后的 click 还要读它的 moved。
      if (!drag) return;
      // 松开也要拦：库的拖动类把收尾写在 mouseup 上，漏了这一下，
      // 它会把自己那套位移写回图上的 style，我们的缩放就没了。
      if (drag.panning) take(event);
      drag.panning = false;
    },
    true
  );

  document.addEventListener(
    "click",
    function (event) {
      if (!isLightboxImage(event.target)) return;

      // 挡住库自带的「单击放大 / 再单击还原」——它的监听挂在 <img> 上，
      // 捕获阶段先跑，stopPropagation 之后它就收不到了。
      take(event);
      var moved = drag && drag.moved;
      drag = null;
      if (moved) return; // 刚才是拖动，不是单击
      close();
    },
    true
  );

  document.addEventListener(
    "touchstart",
    function (event) {
      if (!isLightboxImage(event.target)) return;
      var image = current();
      if (!image || image !== event.target) return;

      if (event.touches.length === 2) {
        var a = event.touches[0];
        var b = event.touches[1];
        pinch = {
          distance: Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY) || 1,
          x: (a.clientX + b.clientX) / 2,
          y: (a.clientY + b.clientY) / 2,
        };
        take(event);
      } else if (event.touches.length === 1 && scale > 1) {
        drag = {
          x: event.touches[0].clientX,
          y: event.touches[0].clientY,
          tx: tx,
          ty: ty,
          panning: true,
          moved: false,
        };
        // 只有放大之后才拦单指：否则库的「左右滑动换图」就没了。
        take(event);
      }
    },
    { passive: false, capture: true }
  );

  document.addEventListener(
    "touchmove",
    function (event) {
      if (pinch && event.touches.length >= 2) {
        take(event);
        var a = event.touches[0];
        var b = event.touches[1];
        var distance = Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY) || 1;
        var x = (a.clientX + b.clientX) / 2;
        var y = (a.clientY + b.clientY) / 2;

        // 两指整体挪动 = 平移（直接加在平移量上），两指间距变化 = 缩放。
        // 先把平移落上，再以「指头当前所在的那个点」为锚点缩放——
        // 分开做完，双指缩放与双指平移就能同时生效。
        tx += x - pinch.x;
        ty += y - pinch.y;
        var ratio = distance / pinch.distance;
        pinch.distance = distance;
        pinch.x = x;
        pinch.y = y;

        if (ratio > 1.0001 || ratio < 0.9999) {
          zoomTo(scale * ratio, x, y, x, y);
        } else {
          clampTo(scale);
          apply();
        }
        return;
      }

      if (drag && drag.panning) {
        take(event);
        var point = event.touches[0];
        var dx = point.clientX - drag.x;
        var dy = point.clientY - drag.y;
        if (!drag.moved && Math.abs(dx) + Math.abs(dy) > TAP_SLOP) drag.moved = true;
        tx = drag.tx + dx;
        ty = drag.ty + dy;
        clampTo(scale);
        apply();
      }
    },
    { passive: false, capture: true }
  );

  document.addEventListener(
    "touchend",
    function (event) {
      if (pinch) {
        if (event.touches.length < 2) pinch = null;
        return;
      }
      if (drag && drag.panning) {
        // 放大状态下 touchstart 被 preventDefault 过，浏览器不会再补一个 click，
        // 所以「点一下关掉」在这里自己判。
        var tapped = !drag.moved;
        drag = null;
        if (tapped) close();
      }
    },
    true
  );
})();
