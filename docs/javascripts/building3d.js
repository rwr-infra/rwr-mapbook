/*
 * Building E 页面的 3D 预览（原生 WebGL，不引任何外部库）
 *
 * 数据来自地编模板 vao0822.svg（tools/building3d.py 解析成
 * docs/assets/tables/building/data.json），链路是这样的：
 *
 *   建筑（material_XXX）
 *     ├─ 1st_floor_1..4   一层 正 / 右 / 背 / 左 四面各引用一个 style
 *     ├─ other_floor_1..4 其它层四面
 *     └─ roof_texture / roof_texture_atlas_cell / roof_scale / roof_color
 *   style（building_style_XXX）
 *     └─ sequence = …     一串基础单元，横向拼起来就是这一面墙
 *   基础单元（texture_groups__XXX）
 *     └─ 名字 = 列,行    图集里的坐标（游戏资源只存名字，坐标就靠模板这张表）
 *
 * ⚠️ 只在 `html[data-ts-page="building"]` 的页面上启动；数据也是到那时才 fetch，
 *    别的页面不会白下载。
 */

(function () {
  if (document.documentElement.getAttribute("data-ts-page") !== "building") return;
  var holder = document.querySelector(".ts-b3d");
  if (!holder) return;

  // 站点根：本脚本在 <根>/javascripts/ 下，去掉文件名与 javascripts/ 得到根
  var self = document.querySelector('script[src*="building3d"]');
  var BASE = "";
  if (self) {
    var u = new URL(self.src, location.href);
    BASE = u.pathname.replace(/javascripts\/[^/]*$/, "");
  }
  var DATA_URL = BASE + "assets/tables/building/data.json";

  var DATA = null;          // data.json
  var IMG = {};             // 纹理缓存
  var STYLE_TEX = {};       // style → 合成好的墙面纹理
  var view = null;          // BoxView 实例
  // editable=false：按模板固定值来，素材下拉/格子输入只读；点「自定义调节」才解锁
  var state = { name: "", floors: 2, wall: "#cfc9bd", roof: "#8a8578", bright: 1.05, rotX: 0.38, rotY: 0.72, zoom: 0.82, editable: false };

  var LANG = (document.documentElement.lang || "zh-hans").toLowerCase();
  var COPY = {
    "zh-hans": {
      eyebrow: "交互式材质检查器", title: "建筑预览", live: "实时渲染",
      hint: "拖动旋转 · 滚轮或双指缩放", reset: "复位视角",
      customizeOff: "自定义调节：关", customizeOn: "自定义调节：开",
      customizeHint: "解锁后可更换素材与图集格子", building: "建筑",
      custom: "自定义", floors: "层数", wall: "墙面色", roof: "屋顶色",
      brightness: "亮度", details: "材质与图集参数", none: "（无）",
      follower: "3D 预览 · 跟随", back: "回到原位", close: "收起",
      noWebgl: "这个浏览器没有启用 WebGL，无法显示预览。", failed: "预览出错：",
      dataFailed: "预览数据加载失败", atlas: "图集", grid: "网格 列×行",
      cells: "图集格子 atlas_cell（列 / 行，修改后实时更新）",
      params: "模板参数（修改后实时更新）", cellsUnit: " 格",
      faces: ["一层正面", "一层右面", "一层背面", "一层左面", "其它层正面", "其它层右面", "其它层背面", "其它层左面"]
    },
    "zh-hant": {
      eyebrow: "互動式材質檢查器", title: "建築預覽", live: "即時渲染",
      hint: "拖曳旋轉 · 滾輪或雙指縮放", reset: "重設視角",
      customizeOff: "自訂調節：關", customizeOn: "自訂調節：開",
      customizeHint: "解鎖後可更換素材與圖集格子", building: "建築",
      custom: "自訂", floors: "層數", wall: "牆面色", roof: "屋頂色",
      brightness: "亮度", details: "材質與圖集參數", none: "（無）",
      follower: "3D 預覽 · 跟隨", back: "回到原位", close: "收起",
      noWebgl: "此瀏覽器未啟用 WebGL，無法顯示預覽。", failed: "預覽出錯：",
      dataFailed: "預覽資料載入失敗", atlas: "圖集", grid: "網格 欄×列",
      cells: "圖集格子 atlas_cell（欄 / 列，修改後即時更新）",
      params: "範本參數（修改後即時更新）", cellsUnit: " 格",
      faces: ["一樓正面", "一樓右面", "一樓背面", "一樓左面", "其他樓層正面", "其他樓層右面", "其他樓層背面", "其他樓層左面"]
    },
    en: {
      eyebrow: "Interactive material inspector", title: "Building preview", live: "Live render",
      hint: "Drag to orbit · scroll or pinch to zoom", reset: "Reset view",
      customizeOff: "Custom controls: off", customizeOn: "Custom controls: on",
      customizeHint: "Unlock materials and atlas cells", building: "Building",
      custom: "Custom", floors: "Floors", wall: "Wall tint", roof: "Roof tint",
      brightness: "Brightness", details: "Material and atlas parameters", none: "(none)",
      follower: "3D preview · following", back: "Back to preview", close: "Dismiss",
      noWebgl: "WebGL is disabled in this browser, so the preview cannot be shown.", failed: "Preview error: ",
      dataFailed: "Preview data could not be loaded", atlas: "Atlas", grid: "Grid cols×rows",
      cells: "Atlas cells (column / row; updates live)", params: "Template parameters (updates live)",
      cellsUnit: " cells",
      faces: ["First floor · front", "First floor · right", "First floor · back", "First floor · left", "Upper floors · front", "Upper floors · right", "Upper floors · back", "Upper floors · left"]
    }
  };
  var TEXT = COPY[LANG] || (LANG.indexOf("zh-hant") === 0 ? COPY["zh-hant"] : (LANG.indexOf("en") === 0 ? COPY.en : COPY["zh-hans"]));

  /* ── 英文名的中文注释：鼠标悬停/点一下就能看到（站内 <abbr title> 那套）── */
  var ZH_KEY = {
    name: "建筑名",
    color: "墙体取色方式：fill=填充色 / stroke=描边色",
    color_variance: "墙体颜色的随机扰动范围",
    atlas_texture: "墙体图集：这栋楼墙面用哪张图集",
    detail_texture: "细节贴图：叠在墙面上、按 alpha 压暗底色的遮罩",
    detail_texture_atlas_cell: "细节贴图格子：列 行 列数 行数",
    detail_texture_scale: "细节贴图平铺次数：列 行",
    roof_texture: "屋顶贴图",
    roof_texture_atlas_cell: "屋顶贴图格子：列 行 列数 行数",
    roof_texture_scale: "屋顶贴图平铺次数",
    roof_scale: "屋顶缩放",
    roof_color: "屋顶取色方式：fill=填充色 / stroke=描边色",
    fill: "填充色（图形内部颜色）",
    stroke: "描边色（图形轮廓颜色）",
    atlas_grid: "图集网格：整张图集横竖各分多少格"
  };
  // 单元名 / style 名里的英文词 → 中文，拼不出就原样留着
  var ZH_WORD = {
    apartment: "公寓", house: "住宅", shop: "商铺", factory: "工厂", office: "办公",
    barrack: "营房", church: "教堂", hotel: "旅馆", garage: "车库", shed: "棚屋",
    window: "窗", door: "门", wall: "墙", roof: "屋顶", floor: "层", empty: "空",
    ruin: "废墟", wood: "木", brick: "砖", concrete: "混凝土", stone: "石",
    metal: "金属", glass: "玻璃", normandy: "诺曼底", provence: "普罗旺斯",
    tropical: "热带", desert: "沙漠", busy: "密集", wide: "宽", narrow: "窄",
    small: "小", big: "大", front: "正面", back: "背面", left: "左", right: "右",
    top: "顶", bottom: "底", side: "侧", corner: "转角", pillar: "柱", stair: "楼梯",
    balcony: "阳台", vent: "通风口", sign: "招牌", board: "板"
  };
  function zhOf(name) {
    var parts = String(name || "").split(/[_\s]+/).filter(Boolean);
    var out = parts.map(function (p) {
      var low = p.toLowerCase();
      if (ZH_WORD[low]) return ZH_WORD[low];
      var m = /^([a-z]+)(\d+)$/i.exec(p);           // apartment1 → 公寓1
      if (m && ZH_WORD[m[1].toLowerCase()]) return ZH_WORD[m[1].toLowerCase()] + m[2];
      return p;
    });
    var s = out.join("·");
    return s === String(name) ? null : s;           // 没翻出来就不加注释
  }
  // 英文名包成 <abbr title="中文">，站内 abbr-tap.js 会接管显示
  function abbr(text, tip) {
    if (!tip) return esc(text);
    return '<abbr title="' + esc(tip) + '">' + esc(text) + '</abbr>';
  }
  function named(text) {
    return LANG.indexOf("en") === 0 ? esc(text) : abbr(text, zhOf(text));
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function img(name) {
    if (!IMG[name]) {
      var i = new Image();
      i.src = BASE + "assets/tables/building/" + name;
      IMG[name] = i;
    }
    return IMG[name];
  }
  function nums(str, fb) {
    var p = String(str == null ? "" : str).trim().split(/\s+/).map(Number).filter(function (n) { return !isNaN(n); });
    if (!p.length) return [fb, fb];
    return [p[0], p.length > 1 ? p[1] : p[0]];
  }

  /* ── 把 style 拼成一条墙面纹理：sequence 每项 1~2 个单元，横向依次排开 ──
     ⚠️ 必须用**这一栋自己的图集** atlasName（地图 objects.svg 里每栋楼各自指定：
     normandy / provence / tropical / building_atlas2/3/4）——之前一律用
     DATA.default_atlas，所以 British 系列整面墙的格子全是错的。 */
  function styleTexture(styleName, atlasName) {
    var ak = atlasName || DATA.default_atlas;
    var ck = ak + "|" + styleName;
    if (STYLE_TEX[ck]) return STYLE_TEX[ck];
    var seq = DATA.styles[styleName];
    if (!seq) return null;
    var atlas = img(ak);
    if (!atlas.complete || !atlas.naturalWidth) return null;
    var cw = atlas.naturalWidth / DATA.atlas_grid[0];
    var chh = atlas.naturalHeight / DATA.atlas_grid[1];
    // 先数这一面总共占多少格（每项 1~2 格）
    var cells = [];
    seq.forEach(function (item) {
      item.forEach(function (unit) {
        var c = DATA.cells[unit];
        cells.push(c || [0, 0]);
      });
    });
    if (!cells.length) return null;
    var out = document.createElement("canvas");
    out.width = cells.length * cw;
    out.height = chh;
    var cx = out.getContext("2d");
    cells.forEach(function (c, i) {
      cx.drawImage(atlas, c[0] * cw, c[1] * chh, cw, chh, i * cw, 0, cw, chh);
    });
    out.__units = cells.length;
    // ⚠️ WebGL1 里非 2 的幂（如 224×32）的纹理配 REPEAT+mipmap 会采样失败
    //    （整面变透明、CSS 黑底透出）——统一拉伸到 2 的幂
    var pot = function (n) { var v = 1; while (v < n) v *= 2; return v; };
    var W = pot(out.width), H = pot(out.height);
    if (W !== out.width || H !== out.height) {
      var p2 = document.createElement("canvas");
      p2.width = W; p2.height = H;
      p2.getContext("2d").drawImage(out, 0, 0, W, H);
      p2.__units = cells.length;
      STYLE_TEX[ck] = p2;
      return p2;
    }
    STYLE_TEX[ck] = out;
    return out;
  }

  /* ── 场景：若干层盒子（四面各自的 style）+ 楼板 + 屋顶 ── */
  function buildScene(mat) {
    var boxes = [];
    // 地面：顶面正好在 y=0，建筑站在上面；大一圈，避免转视角时露出边
    boxes.push({ ground: true, size: [80, 0.6, 80], y: -0.6,
                 faces: { top: { tint: [0.36, 0.35, 0.33] },
                          default: { tint: [0.5, 0.5, 0.48] } } });
    var unit = 1.5;                       // 一个单元的世界尺寸
    var groups = ["1st", "other"];
    // 各面 style 合成纹理，取最长的那一面决定楼体宽度
    var tex = {};
    var maxUnits = 1;
    groups.forEach(function (g) {
      tex[g] = [];
      for (var i = 0; i < 4; i++) {
        var s = mat.floors[g][i];
        var t = s ? styleTexture(s, mat.atlas_texture) : null;
        tex[g].push(t);
        if (t && t.__units > maxUnits) maxUnits = t.__units;
      }
    });
    // 底面统一成方形（16.5 × 16.5），长宽一致：层高 1.4。
    // 短 style 的墙面纹理会靠 REPEAT 重复铺满，正好铺成整齐的窗户列。
    var W = 16.5, D = W, fh = 1.4;
    var fkeys = ["front", "right", "back", "left"];
    // front/back 铺在 X 向（宽 W），right/left 铺在 Z 向（深 D）——
    // 之前右/左面也按 W 算重复次数，进深改成 D 后会导致纹理被拉伸。
    var faceW = [W, W, D, D];
    var n = Math.max(1, Math.min(+state.floors || 2, 12));
    for (var f = 0; f < n; f++) {
      var g2 = f === 0 ? "1st" : "other";
      var faces = { top: { tint: hex2rgb(state.wall) } };
      fkeys.forEach(function (k, i) {
        var t = tex[g2][i];
        faces[k] = t
          ? { canvas: t, tile: [faceW[i] / (t.__units * unit), fh / unit], tint: hex2rgb(state.wall) }
          : { tint: hex2rgb(state.wall) };
      });
      boxes.push({ size: [W, fh, D], y: f * (fh + 0.28), faces: faces });
      // 层间分隔檐：四周凸出墙面 0.35，就是参考图里每层之间那道浅色横带
      boxes.push({ size: [W + 0.7, 0.26, D + 0.7], y: f * (fh + 0.28) + fh,
                   faces: { default: { tint: [0.82, 0.76, 0.62] } } });
    }
    // 屋顶：roof_texture + 格子 + 缩放 + 颜色
    var r = mat.roof || {};
    var rImg = img(r.texture || "wall_atlas1.png");
    var roofFace = { tint: hex2rgb(state.roof) };
    if (rImg.complete && rImg.naturalWidth && r.cell) {
      var cw = rImg.naturalWidth / r.cell[2];
      var ch2 = rImg.naturalHeight / r.cell[3];
      var c = document.createElement("canvas");
      c.width = Math.max(1, cw); c.height = Math.max(1, ch2);
      c.getContext("2d").drawImage(rImg, r.cell[0] * cw, r.cell[1] * ch2, cw, ch2, 0, 0, c.width, c.height);
      roofFace = { canvas: c, tile: nums(r.scale, [6, 6]), tint: hex2rgb(state.roof) };
    }
    // 屋顶：出檐与层间分隔檐完全一致（0.35），从正面看檐口和各层横带在一条线上
    //    （参考 2020Busy 游戏实拍）。顶面贴图以屋顶板边缘为准：
    //    X 向正好铺满 roof_scale[0] 个纹理格、另一向按同一格宽换算，
    //    纹理从 UV 0 起铺、余数裁掉，格子保持正方不拉伸。
    //    屋顶侧面用屋顶材质本身（游戏里檐口侧面就是屋顶色）。
    var rs = nums(r.scale, [6, 6]);
    var topW = W + 0.7, topD = D + 0.7;
    var cellW = topW / Math.max(1, rs[0]);      // 一个纹理重复在顶面上的世界宽
    if (roofFace.canvas) {
      roofFace.tile = [rs[0], topD / cellW];
      roofFace.mask = isMask(roofFace.canvas);
    }
    var roofSide = roofFace.canvas
      ? { canvas: roofFace.canvas, tile: [1, 1], mask: isMask(roofFace.canvas), tint: hex2rgb(state.roof) }
      : { tint: hex2rgb(state.roof) };
    // ⚠️ 屋顶在游戏里没有厚度，就是往最上面那道檐上贴一层材质——这里只给
    //    0.05 的薄片，侧面基本看不见，直接压在顶层分隔檐上。
    boxes.push({ size: [topW, 0.05, topD], y: n * (fh + 0.28) - 0.02,
                 faces: { top: roofFace, default: roofSide } });
    // 没有底部基座：一楼材质直接接地（2020Busy 游戏实拍如此）
    return boxes;
  }

  function hex2rgb(h) {
    var m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(String(h || "").trim());
    if (!m) return [1, 1, 1];
    return [parseInt(m[1], 16) / 255, parseInt(m[2], 16) / 255, parseInt(m[3], 16) / 255];
  }

  /* ── 极简 WebGL 盒子渲染器（与 rwr-material-preview/render3d.js 同源） ── */
  function BoxView(canvas) {
    var gl = canvas.getContext("webgl", { antialias: true, alpha: false, powerPreference: "high-performance" });
    if (!gl) return null;
    this.gl = gl; this.canvas = canvas; this.texCache = {}; this.geometry = [];
    this._frame = 0;
    this.rotX = state.rotX; this.rotY = state.rotY; this.zoom = state.zoom; this.bright = state.bright;
    this.boxes = [];
    var vs = "attribute vec3 aPos;attribute vec2 aUV;attribute vec3 aN;uniform mat4 uP;uniform mat4 uV;" +
      "varying vec2 vUV;varying vec3 vN;void main(){vUV=aUV;vN=aN;gl_Position=uP*uV*vec4(aPos,1.0);}";
    var fs = "precision mediump float;varying vec2 vUV;varying vec3 vN;uniform sampler2D uT;uniform vec3 uTint;" +
      "uniform vec2 uTile;uniform float uBright;uniform vec3 uLight;uniform float uMask;" +
      "void main(){vec4 t=texture2D(uT,vUV*uTile);" +
      // ⚠️ 遮罩贴图（wall_atlas1 这类「RGB 全 0、只有 alpha 在变」的细节层，屋顶常用）：
      //    直接 t.rgb*uTint 会整片全黑，得改成用 alpha 把底色压暗（游戏里就是这么叠的）
      "vec3 c=(uMask>0.5)?uTint*(1.0-t.a):t.rgb*uTint;" +
      "float l=max(dot(normalize(vN),normalize(uLight)),0.0);c*=(0.8+0.3*l)*uBright;" +
      "gl_FragColor=vec4(c,(uMask>0.5)?1.0:t.a);}";
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; }
    var p = gl.createProgram();
    gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p); gl.useProgram(p); this.prog = p;
    this.loc = {
      aPos: gl.getAttribLocation(p, "aPos"), aUV: gl.getAttribLocation(p, "aUV"), aN: gl.getAttribLocation(p, "aN"),
      uP: gl.getUniformLocation(p, "uP"), uV: gl.getUniformLocation(p, "uV"), uT: gl.getUniformLocation(p, "uT"),
      uTint: gl.getUniformLocation(p, "uTint"), uTile: gl.getUniformLocation(p, "uTile"),
      uBright: gl.getUniformLocation(p, "uBright"), uLight: gl.getUniformLocation(p, "uLight"),
      uMask: gl.getUniformLocation(p, "uMask")
    };
    gl.enable(gl.DEPTH_TEST); gl.enable(gl.CULL_FACE);
    // 背景灰：原来那套深色底在贴图上看着像没画出来，灰色更接近游戏里的雾底
    gl.clearColor(0.23, 0.25, 0.24, 1);
    this._bind();
    if (window.ResizeObserver) {
      var selfView = this;
      this._resizeObserver = new ResizeObserver(function () { selfView.scheduleDraw(); });
      this._resizeObserver.observe(canvas);
    }
  }
  BoxView.prototype.scheduleDraw = function () {
    var self = this;
    if (this._frame) return;
    this._frame = requestAnimationFrame(function () { self._frame = 0; self.draw(); });
  };
  BoxView.prototype._bind = function () {
    var self = this, cv = this.canvas;
    var pointers = {}, pinch = 0;
    function distance() {
      var ps = Object.keys(pointers).map(function (k) { return pointers[k]; });
      return ps.length < 2 ? 0 : Math.hypot(ps[0][0] - ps[1][0], ps[0][1] - ps[1][1]);
    }
    cv.style.touchAction = "none";
    cv.addEventListener("pointerdown", function (e) {
      pointers[e.pointerId] = [e.clientX, e.clientY];
      pinch = distance();
      if (cv.setPointerCapture) cv.setPointerCapture(e.pointerId);
      cv.classList.add("is-dragging");
    });
    function release(e) {
      delete pointers[e.pointerId]; pinch = distance();
      if (!Object.keys(pointers).length) cv.classList.remove("is-dragging");
    }
    cv.addEventListener("pointerup", release);
    cv.addEventListener("pointercancel", release);
    cv.addEventListener("pointermove", function (e) {
      if (!pointers[e.pointerId]) return;
      var oldX = pointers[e.pointerId][0], oldY = pointers[e.pointerId][1];
      pointers[e.pointerId] = [e.clientX, e.clientY];
      if (Object.keys(pointers).length > 1) {
        var nextPinch = distance();
        if (pinch && nextPinch) self.zoom = Math.max(0.22, Math.min(3.2, self.zoom * nextPinch / pinch));
        pinch = nextPinch;
        self.scheduleDraw();
        return;
      }
      self.rotY -= (e.clientX - oldX) * 0.009;
      // 上下：往下拖 → 模型往下转（相机升高、俯看，模型顶部朝屏幕下方倒）
      self.rotX = Math.max(-1.15, Math.min(1.2, self.rotX + (e.clientY - oldY) * 0.009));
      self.scheduleDraw();
    });
    cv.addEventListener("wheel", function (e) {
      e.preventDefault();
      self.zoom = Math.max(0.22, Math.min(3.2, self.zoom * Math.exp(-e.deltaY * 0.0012)));
      self.scheduleDraw();
    }, { passive: false });
  };
  BoxView.prototype.tex = function (canvas, key) {
    var gl = this.gl;
    if (this.texCache[key]) return this.texCache[key];
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.generateMipmap(gl.TEXTURE_2D);
    this.texCache[key] = t;
    return t;
  };
  BoxView.prototype.white = function () {
    if (this._w) return this._w;
    var c = document.createElement("canvas"); c.width = c.height = 4;
    var x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, 4, 4);
    this._w = this.tex(c, "__white__");
    return this._w;
  };
  BoxView.prototype.setBoxes = function (b) {
    var gl = this.gl;
    this.geometry.forEach(function (entry) {
      entry.buffers.forEach(function (buf) { gl.deleteBuffer(buf); });
    });
    this.boxes = b;
    this.geometry = b.map(function (box) {
      var g = boxGeo(box.size[0], box.size[1], box.size[2], box.x || 0, box.y || 0, box.z || 0);
      var buffers = [];
      function upload(data, target) {
        var buffer = gl.createBuffer(); buffers.push(buffer);
        gl.bindBuffer(target, buffer); gl.bufferData(target, data, gl.STATIC_DRAW);
        return buffer;
      }
      return {
        box: box, buffers: buffers,
        pos: upload(g.pos, gl.ARRAY_BUFFER), uv: upload(g.uv, gl.ARRAY_BUFFER),
        nor: upload(g.nor, gl.ARRAY_BUFFER), idx: upload(g.idx, gl.ELEMENT_ARRAY_BUFFER)
      };
    });
    if (this.arrow) this.arrow.buffers.forEach(function (buf) { gl.deleteBuffer(buf); });
    var fd = 0;
    b.forEach(function (box) { if (!box.ground) fd = Math.max(fd, box.size[2]); });
    var y = 0.1, z0 = fd / 2 + 0.2, z1 = z0 + 0.85, z2 = z1 + 0.6;
    var arrowPos = new Float32Array([
      -0.16, y, z1, -0.16, y, z0, 0.16, y, z0,
      -0.16, y, z1, 0.16, y, z0, 0.16, y, z1,
      0, y, z2, 0.55, y, z1, -0.55, y, z1
    ]);
    var arrowUv = new Float32Array(arrowPos.length / 3 * 2);
    var arrowNor = new Float32Array(arrowPos.length);
    for (var i = 1; i < arrowNor.length; i += 3) arrowNor[i] = 1;
    var arrowBuffers = [];
    function arrowUpload(data) {
      var buffer = gl.createBuffer(); arrowBuffers.push(buffer);
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer); gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
      return buffer;
    }
    this.arrow = { buffers: arrowBuffers, pos: arrowUpload(arrowPos), uv: arrowUpload(arrowUv), nor: arrowUpload(arrowNor) };
  };
  BoxView.prototype.draw = function () {
    var gl = this.gl, cv = this.canvas, self = this;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var cssW = Math.max(1, Math.round(cv.clientWidth));
    var cssH = Math.max(1, Math.round(cv.clientHeight));
    var pixelW = Math.round(cssW * dpr), pixelH = Math.round(cssH * dpr);
    if (cv.width !== pixelW || cv.height !== pixelH) { cv.width = pixelW; cv.height = pixelH; }
    gl.viewport(0, 0, cv.width, cv.height);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    var span = 1, h = 1;
    this.boxes.forEach(function (b) {
      if (b.ground) return;              // 地面不参与取景，否则相机会被撑到天上去
      span = Math.max(span, b.size[0], b.size[2]);
      h = Math.max(h, (b.y || 0) + b.size[1]);
    });
    // +3.4：正面箭头伸到 footprint 外侧，取景要把它算进去，
    //        否则俯视时箭头（+Z 一侧）会掉到画面下沿外面看不见。
    span += 4.8;
    var dist = (span + h) * 0.95 / this.zoom;
    var cx = Math.sin(this.rotY) * Math.cos(this.rotX) * dist;
    var cz = Math.cos(this.rotY) * Math.cos(this.rotX) * dist;
    var cy = Math.sin(this.rotX) * dist + h * 0.4;
    var f = 1 / Math.tan(45 * Math.PI / 360);
    gl.uniformMatrix4fv(this.loc.uP, false, new Float32Array([
      f / (cv.width / cv.height), 0, 0, 0, 0, f, 0, 0, 0, 0, -1, -1, 0, 0, -0.1, 0]));
    // 取景点往正面（+Z，箭头那一侧）前移一点，让箭头和楼体一起居中
    var tz = 2.2;
    var z = norm3([cx, cy, cz - tz]), x3 = norm3(cross([0, 1, 0], z)), y3 = cross(z, x3);
    gl.uniformMatrix4fv(this.loc.uV, false, new Float32Array([
      x3[0], y3[0], z[0], 0, x3[1], y3[1], z[1], 0, x3[2], y3[2], z[2], 0,
      -dot3(x3, [cx, cy, cz]), -dot3(y3, [cx, cy, cz]), -dot3(z, [cx, cy, cz]), 1]));
    gl.uniform3fv(this.loc.uLight, new Float32Array([0.4, 0.9, 0.6]));
    this.geometry.forEach(function (entry) {
      var b = entry.box;
      gl.bindBuffer(gl.ARRAY_BUFFER, entry.pos);
      gl.enableVertexAttribArray(self.loc.aPos); gl.vertexAttribPointer(self.loc.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, entry.uv);
      gl.enableVertexAttribArray(self.loc.aUV); gl.vertexAttribPointer(self.loc.aUV, 2, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, entry.nor);
      gl.enableVertexAttribArray(self.loc.aN); gl.vertexAttribPointer(self.loc.aN, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, entry.idx);
      ["front", "back", "right", "left", "top", "bottom"].forEach(function (k, fi) {
        var m = b.faces[k] || b.faces.default;
        if (!m) return;
        var tex = m.canvas ? self.tex(m.canvas, m.canvas.__k || (m.canvas.__k = "t" + Math.random())) : self.white();
        gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.uniform1i(self.loc.uT, 0);
        gl.uniform3fv(self.loc.uTint, new Float32Array(m.tint || [1, 1, 1]));
        gl.uniform2fv(self.loc.uTile, new Float32Array(m.tile || [1, 1]));
        // 遮罩贴图走 uMask 分支（用 alpha 压暗底色），普通贴图走 t.rgb*uTint
        var mk = m.canvas ? (m.mask !== undefined ? m.mask : isMask(m.canvas)) : false;
        gl.uniform1f(self.loc.uMask, mk ? 1 : 0);
        gl.uniform1f(self.loc.uBright, self.bright);
        gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, fi * 12);
      });
    });
    // 正方向箭头：整场只画一支，贴着建筑正面底边（贴图边缘）向外指——
    //    ⚠️ 两个坑：① 之前画在每个盒子的循环里，地面/楼板/屋檐各来一支，
    //      楼板那几支还埋在楼体里；② 三角形绕序算出来法线是 **-Y**（朝下），
    //      开着 CULL_FACE 时俯视会被整个剔除——这就是"俯视看不到"的真因，
    //      跟偏移量无关。所以这里把顶点反过来（法线 +Y）并在画箭头期间
    //      临时关掉背面剔除，任何视角都不会消失。
    (function () {
      if (!self.arrow) return;
      gl.bindBuffer(gl.ARRAY_BUFFER, self.arrow.pos);
      gl.enableVertexAttribArray(self.loc.aPos); gl.vertexAttribPointer(self.loc.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, self.arrow.uv);
      gl.enableVertexAttribArray(self.loc.aUV); gl.vertexAttribPointer(self.loc.aUV, 2, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, self.arrow.nor);
      gl.enableVertexAttribArray(self.loc.aN); gl.vertexAttribPointer(self.loc.aN, 3, gl.FLOAT, false, 0, 0);
      gl.bindTexture(gl.TEXTURE_2D, self.white());
      gl.uniform1i(self.loc.uT, 0);
      gl.uniform3fv(self.loc.uTint, new Float32Array([0.85, 0.18, 0.14]));
      gl.uniform2fv(self.loc.uTile, new Float32Array([1, 1]));
      gl.uniform1f(self.loc.uMask, 0);
      gl.uniform1f(self.loc.uBright, self.bright);
      gl.disable(gl.CULL_FACE);          // 相机转到地平线以下时也不能消失
      gl.drawArrays(gl.TRIANGLES, 0, 9);
      gl.enable(gl.CULL_FACE);
    })();
  };
  function boxGeo(w, h, d, ox, oy, oz) {
    var x = w / 2, y = h / 2, z = d / 2;
    var faces = [
      { n: [0, 0, 1], v: [[-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]] },
      { n: [0, 0, -1], v: [[x, -y, -z], [-x, -y, -z], [-x, y, -z], [x, y, -z]] },
      { n: [1, 0, 0], v: [[x, -y, z], [x, -y, -z], [x, y, -z], [x, y, z]] },
      { n: [-1, 0, 0], v: [[-x, -y, -z], [-x, -y, z], [-x, y, z], [-x, y, -z]] },
      { n: [0, 1, 0], v: [[-x, y, z], [x, y, z], [x, y, -z], [-x, y, -z]] },
      { n: [0, -1, 0], v: [[-x, -y, -z], [x, -y, -z], [x, -y, z], [-x, -y, z]] }
    ];
    var pos = [], uv = [], nor = [], idx = [];
    var uvs = [[0, 1], [1, 1], [1, 0], [0, 0]];
    faces.forEach(function (f, fi) {
      f.v.forEach(function (p, i) {
        pos.push(p[0] + ox, p[1] + oy + h / 2, p[2] + oz);
        uv.push(uvs[i][0], uvs[i][1]);
        nor.push(f.n[0], f.n[1], f.n[2]);
      });
      var b = fi * 4;
      idx.push(b, b + 1, b + 2, b, b + 2, b + 3);
    });
    return { pos: new Float32Array(pos), uv: new Float32Array(uv), nor: new Float32Array(nor), idx: new Uint16Array(idx) };
  }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function dot3(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function norm3(a) { var l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; }

  /* ── 界面 ──────────────────────────────────────────────── */
  function ui() {
    holder.innerHTML =
      '<section class="ts-b3d__shell" aria-label="' + esc(TEXT.title) + '">' +
      '<header class="ts-b3d__head"><div><span class="ts-b3d__eyebrow">' + TEXT.eyebrow + '</span>' +
      '<strong>' + TEXT.title + '</strong></div><span class="ts-b3d__live"><i></i>' + TEXT.live + '</span></header>' +
      '<div class="ts-b3d__stage"><canvas id="b3dCanvas" width="960" height="720" aria-label="' + esc(TEXT.title) + '"></canvas>' +
      '<span class="ts-b3d__hint">' + TEXT.hint + '</span>' +
      '<div class="ts-b3d__ctrls">' +
      '<button class="ts-b3d__btn" id="b3dReset" type="button">' + TEXT.reset + '</button>' +
      '<button class="ts-b3d__btn" id="b3dUnlock" type="button" aria-pressed="false">' + TEXT.customizeOff + '</button>' +
      '<span class="ts-b3d__dim">' + TEXT.customizeHint + '</span>' +
      '</div></div>' +
      '<div class="ts-b3d__side">' +
      '<div class="ts-b3d__basic"><label class="ts-b3d__field ts-b3d__field--wide"><span>' + TEXT.building + '</span>' +
      '<select id="b3dPick">' + DATA.order.map(function (n) {
        return '<option value="' + n + '">' + n + '</option>';
      }).join("") + '<option value="__custom__">' + TEXT.custom + '</option>' + '</select></label>' +
      '<label class="ts-b3d__field"><span>' + TEXT.floors + '</span><input type="number" id="b3dFloors" min="1" max="12" value="2"></label>' +
      '<label class="ts-b3d__field"><span>' + TEXT.wall + '</span><input type="color" id="b3dWall" value="#cfc9bd"></label>' +
      '<label class="ts-b3d__field"><span>' + TEXT.roof + '</span><input type="color" id="b3dRoof" value="#8a8578"></label>' +
      '<label class="ts-b3d__field ts-b3d__field--range"><span>' + TEXT.brightness + '</span><input type="range" id="b3dBright" min="0.6" max="3" step="0.1" value="1.05"></label></div>' +
      '<details class="ts-b3d__details"><summary>' + TEXT.details + '</summary><div class="ts-b3d__info" id="b3dInfo"></div></details>' +
      '</div></section>';
    var pick = document.getElementById("b3dPick");
    var fl = document.getElementById("b3dFloors");
    var wall = document.getElementById("b3dWall");
    var roof = document.getElementById("b3dRoof");
    var br = document.getElementById("b3dBright");
    pick.onchange = function () {
      state.name = pick.value;
      // 选「自定义」直接把调节开关打开（自定义就是要随便改，不然还得再点一次）
      if (state.name === "__custom__" && !state.editable) {
        var ub = document.getElementById("b3dUnlock");
        state.editable = true;
        if (ub) { ub.textContent = TEXT.customizeOn; ub.classList.add("ts-b3d__btn--on"); ub.setAttribute("aria-pressed", "true"); }
      }
      // 换建筑 → 墙/屋顶色回到模板语义色（color/roof_color 指 fill 还是 stroke）
      if (state.name !== "__custom__" && DATA.materials[state.name])
        applyMatColors(DATA.materials[state.name]);
      draw();
    };
    fl.onchange = function () { state.floors = +fl.value; draw(); };
    wall.oninput = function () { state.wall = wall.value; draw(); };
    roof.oninput = function () { state.roof = roof.value; draw(); };
    br.oninput = function () {
      state.bright = +br.value;
      if (view) { view.bright = state.bright; view.scheduleDraw(); }
      if (floatView) { floatView.bright = state.bright; floatView.scheduleDraw(); }
    };
    document.getElementById("b3dReset").onclick = function () {
      state.rotX = 0.38; state.rotY = 0.72; state.zoom = 0.82;
      if (view) { view.rotX = state.rotX; view.rotY = state.rotY; view.zoom = state.zoom; view.scheduleDraw(); }
    };
    // 自定义调节开关：关着的时候所有素材下拉/格子输入都是只读（按模板固定值渲染）
    var unlockBtn = document.getElementById("b3dUnlock");
    unlockBtn.onclick = function () {
      state.editable = !state.editable;
      unlockBtn.textContent = state.editable ? TEXT.customizeOn : TEXT.customizeOff;
      unlockBtn.classList.toggle("ts-b3d__btn--on", state.editable);
      unlockBtn.setAttribute("aria-pressed", state.editable ? "true" : "false");
      if (state.editable) document.querySelector(".ts-b3d__details").open = true;
      draw();                       // info() 按 state.editable 重画面板
    };
    state.name = DATA.materials["BuildingBritish4_1st"] ? "BuildingBritish4_1st" : DATA.order[0];
    pick.value = state.name;
    applyMatColors(DATA.materials[state.name]);
    draw();
    setupFloat();
  }

  // 模板里 color / roof_color 只是「取 fill 还是取 stroke」的语义开关，
  // 实际色值在各 material rect 的 style 上（如 2020Busy：墙=stroke #c6c3c3、
  // 屋顶=fill #a1c1be）。切建筑时把两个取色器同步成模板色；没有色值的
  // 建筑保持当前选色不动。
  function applyMatColors(mat) {
    if (!mat) return;
    function colOf(sem, dft) {
      var v = sem === "stroke" ? mat.stroke : mat.fill;
      return /^#[0-9a-fA-F]{6}$/.test(String(v || "")) ? v : dft;
    }
    state.wall = colOf(mat.color, state.wall);
    if (mat.roof) state.roof = colOf(mat.roof.color, state.roof);
    var w = document.getElementById("b3dWall"), rf = document.getElementById("b3dRoof");
    if (w) w.value = state.wall;
    if (rf) rf.value = state.roof;
  }

  function draw() {
    var mat;
    if (state.name === "__custom__") {
      // 自定义：从上一次选中的真实建筑克隆一份起点，之后随便改都不动原数据
      if (!state.custom) {
        var src = DATA.materials[state.lastName] || DATA.materials[DATA.order[0]];
        state.custom = JSON.parse(JSON.stringify(src));
        state.custom.name = TEXT.custom;
      }
      mat = state.custom;
    } else {
      mat = DATA.materials[state.name];
      if (mat) state.lastName = state.name;
    }
    if (!mat) return;
    var cv = document.getElementById("b3dCanvas");
    if (!cv) return;
    // 等图集就位（第一帧可能还没解码完）
    // 墙面必须等当前建筑自己的 atlas_texture；只等 default_atlas 会让 British /
    // Normandy 等建筑在首帧永久退化成纯色墙，图片后来加载完也不会再触发绘制。
    var need = [DATA.default_atlas, mat.atlas_texture, mat.detail_texture, (mat.roof || {}).texture]
      .filter(Boolean).map(img);
    // ⚠️ 去重：roof 和 detail 常是同一张图（img 缓存返回同一个 Image 对象），
    //    不去重的话计数器永远减不到 0，go 一次都不会执行，画布就一直是黑的。
    var pending = [];
    need.forEach(function (i) {
      if (!i.complete && pending.indexOf(i) < 0) pending.push(i);
    });
    var go = function () {
      try {
        if (!view) {
          view = new BoxView(cv);
          if (!view || !view.gl) {
            var c2 = cv.getContext("2d");
            c2.fillStyle = "#ccc"; c2.font = "13px sans-serif";
            c2.fillText(TEXT.noWebgl, 12, 26);
            return;
          }
        }
        view.bright = state.bright;
        view.setBoxes(buildScene(mat));
        view.draw();
        drawFloat();                 // 浮窗（如果正显示着）同步重画
        info(mat);
      } catch (e) {
        window.__b3dErr = String(e && e.stack || e);
        var tip = document.createElement("p");
        tip.className = "ts-b3d__dim";
        tip.textContent = TEXT.failed + window.__b3dErr;
        cv.parentNode.appendChild(tip);
      }
    };
    if (!pending.length) { go(); return; }
    var left = pending.length;
    pending.forEach(function (i) {
      var done = function () { if (--left <= 0) go(); };
      i.addEventListener("load", done, { once: true });
      i.addEventListener("error", done, { once: true });
    });
  }

  /* ── 页面往下翻、3D 预览滚出视口时，右下角浮出小窗继续看 ──────────
     ⚠️ 不搬动原画布（搬了 IntersectionObserver 会自触发来回弹），
        而是另开一块小画布同画一遍；两边视角互相同步。 */
  var floatView = null, floatBox = null, floatDismissed = false;

  function setupFloat() {
    if (!window.IntersectionObserver) return;
    var host = document.querySelector(".ts-b3d");
    var stage = document.querySelector(".ts-b3d__stage");
    if (!host || !stage) return;
    floatBox = document.createElement("div");
    floatBox.className = "ts-b3d__float";
    floatBox.hidden = true;
    floatBox.innerHTML =
      '<div class="ts-b3d__floatbar"><span>' + TEXT.follower + '</span>' +
      '<span><button class="ts-b3d__btn" id="b3dFloatBack" type="button">' + TEXT.back + '</button> ' +
      '<button class="ts-b3d__btn" id="b3dFloatClose" type="button" aria-label="' + esc(TEXT.close) + '">×</button></span></div>' +
      '<canvas id="b3dFloatCanvas" width="320" height="240"></canvas>';
    document.body.appendChild(floatBox);
    document.getElementById("b3dFloatBack").onclick = function () {
      host.scrollIntoView({ behavior: "smooth", block: "center" });
    };
    document.getElementById("b3dFloatClose").onclick = function () {
      floatDismissed = true;
      floatBox.hidden = true;
    };
    var fc = document.getElementById("b3dFloatCanvas");
    // 在浮窗里拖动 → 视角同步回主画布，两边保持一致
    var syncBack = function () {
      requestAnimationFrame(function () {
        if (!floatView || !view) return;
        view.rotX = floatView.rotX; view.rotY = floatView.rotY; view.zoom = floatView.zoom;
        view.scheduleDraw();
      });
    };
    fc.addEventListener("pointermove", syncBack);
    fc.addEventListener("wheel", syncBack, { passive: true });
    // seenOnce：3D 预览得先露过面（用户看过）才允许浮窗——否则刚打开页面、
    // 预览还在下面没滚到时就弹出来，反而碍事。
    var seenOnce = false;
    new IntersectionObserver(function (es) {
      var vis = es[es.length - 1].isIntersecting;
      if (vis) {
        seenOnce = true;
        floatDismissed = false;                 // 回到原位就复位「收起」
        floatBox.hidden = true;
      } else if (seenOnce && !floatDismissed) {
        floatBox.hidden = false;
        drawFloat();
      }
    }, { threshold: 0 }).observe(stage);
  }

  function drawFloat() {
    if (!floatBox || floatBox.hidden || !view || !view.boxes.length) return;
    var fc = document.getElementById("b3dFloatCanvas");
    if (!fc) return;
    if (!floatView) {
      floatView = new BoxView(fc);
      if (!floatView || !floatView.gl) { floatView = null; return; }
    }
    floatView.rotX = view.rotX; floatView.rotY = view.rotY;
    floatView.zoom = view.zoom; floatView.bright = view.bright;
    floatView.setBoxes(view.boxes);
    floatView.draw();
  }

  /* 判断一张裁出来的图是不是「黑 + alpha」的细节遮罩：遮罩的 RGB 全是 0，
     只有 alpha 在变（wall_atlas1 就是这样，砖缝/污渍靠它压暗底色） */
  function isMask(cv) {
    if (cv.__mask !== undefined) return cv.__mask;
    var c = cv.getContext("2d");
    var d = c.getImageData(0, 0, cv.width, cv.height).data;
    var sum = 0;
    for (var i = 0; i < d.length; i += 4) sum += d[i] + d[i + 1] + d[i + 2];
    cv.__mask = sum === 0;
    return cv.__mask;
  }

  // 可编辑参数的扁平视图：name → 当前值（存回 mat，键名保持模板写法）
  function flat(mat) {
    var out = {};
    Object.keys(mat).forEach(function (k) {
      if (k === "floors") return;
      if (k === "detail_cell") { out["detail_texture_atlas_cell"] = (mat.detail_cell || []).join(" "); return; }
      if (k === "detail_scale") { out["detail_texture_scale"] = mat.detail_scale; return; }
      if (k === "roof") {
        out["roof_texture"] = mat.roof.texture;      // 屋顶贴图本身也要能下拉换
        out["roof_texture_atlas_cell"] = (mat.roof.cell || []).join(" ");
        out["roof_texture_scale"] = mat.roof.scale;
        out["roof_scale"] = mat.roof.scale;
        return;
      }
      out[k] = mat[k];
    });
    return out;
  }

  var texSelect = function (key, val) {
    let opts = '<option value="">' + TEXT.none + '</option>';
    const list = (DATA.textures || []).slice();
    const cur = String(val || "").trim().split(/\s+/)[0];
    if (cur && list.indexOf(cur) < 0) list.unshift(cur);
    list.forEach(function (t) {
      opts += '<option value="' + t + '"' + (t === cur ? " selected" : "") + '>' + t + '</option>';
    });
    return '<select data-key="' + key + '" data-file="1"' + dis() + '>' + opts + '</select>';
  };

  // 自定义调节没开 → 素材下拉与格子输入只读（按模板固定值渲染）
  function dis() { return state.editable ? "" : " disabled"; }

  function editorRows(mat) {
    const flat0 = flat(mat);
    let rows = "";
    Object.keys(flat0).forEach(function (k) {
      const val = flat0[k];
      const label = LANG.indexOf("en") === 0 ? esc(k) : abbr(k, ZH_KEY[k]);
      if (/_texture(_atlas_cell)?$/.test(k) || k === "atlas_texture") {
        // 纹理文件名 → 下拉（值可能带格子参数，只取文件名部分；改动只写文件名）
        rows += '<div class="ts-b3d__kv"><span>' + label + '</span>' + texSelect(k, val) + '</div>';
        return;
      }
      rows += '<div class="ts-b3d__kv"><span>' + label + '</span>' +
        '<input data-key="' + k + '" value="' + String(val).replace(/"/g, "&quot;") + '"' + dis() + '></div>';
    });
    return rows;
  }

  function info(mat) {
    var el = document.getElementById("b3dInfo");
    if (!el) return;
    var f = mat.floors;
    var canEdit = state.editable || state.name === "__custom__";
    // 每层每面的 style：默认只读展示（带中文注释）；开了自定义调节就能下拉换
    function faceRow(label, g, i) {
      var val = f[g][i] || "";
      if (!canEdit)
        return '<div class="ts-b3d__kv"><span>' + label + '</span><code>' +
          (val ? named(val) : "—") + '</code></div>';
      var opts = '<option value="">' + TEXT.none + '</option>';
      Object.keys(DATA.styles).sort().forEach(function (s) {
        opts += '<option value="' + s + '"' + (s === val ? " selected" : "") + '>' + s + '</option>';
      });
      return '<div class="ts-b3d__kv"><span>' + label + '</span><select data-floor="' + g + ':' + i + '" style="max-width:170px">' + opts + '</select></div>';
    }
    function line(label, unit) {
      var seq = DATA.styles[unit];
      var n = seq ? seq.reduce(function (a, s) { return a + s.length; }, 0) : 0;
      return '<div class="ts-b3d__kv"><span>' + label + '</span><code>' + (unit || "—") +
        '</code><span class="ts-b3d__dim">' + (n ? n + TEXT.cellsUnit : "") + '</span></div>';
    }
    // 图集格子（atlas_cell）：本栋 8 个面用到的基础单元，各自在图集里的 列/行
    // ——墙面就是这些格子横着拼出来的，格子指错整面墙就乱，所以直接摆出来可改
    var units = [];
    ["1st", "other"].forEach(function (g) {
      (f[g] || []).forEach(function (s) {
        (DATA.styles[s] || []).forEach(function (item) {
          item.forEach(function (u) { if (units.indexOf(u) < 0) units.push(u); });
        });
      });
    });
    function cellRows() {
      var head = '<div class="ts-b3d__kv"><span>' + TEXT.atlas + '</span><code>' +
        (mat.atlas_texture || DATA.default_atlas) + '</code>' +
        '<span class="ts-b3d__dim">' + TEXT.grid + '</span>' +
        '<input data-grid="1" value="' + (DATA.atlas_grid || [8, 8]).join(" ") + '" style="width:56px"' + dis() + '></div>';
      return head + units.map(function (u) {
        var c = DATA.cells[u] || [0, 0];
        return '<div class="ts-b3d__kv"><span>' + named(u) + '</span>' +
          '<input type="number" data-cell="' + u + '" data-axis="0" value="' + c[0] + '" style="width:44px"' + dis() + '>' +
          '<input type="number" data-cell="' + u + '" data-axis="1" value="' + c[1] + '" style="width:44px"' + dis() + '></div>';
      }).join("");
    }
    el.innerHTML =
      faceRow(TEXT.faces[0], "1st", 0) +
      faceRow(TEXT.faces[1], "1st", 1) +
      faceRow(TEXT.faces[2], "1st", 2) +
      faceRow(TEXT.faces[3], "1st", 3) +
      faceRow(TEXT.faces[4], "other", 0) +
      faceRow(TEXT.faces[5], "other", 1) +
      faceRow(TEXT.faces[6], "other", 2) +
      faceRow(TEXT.faces[7], "other", 3) +
      '<p class="ts-b3d__dim ts-b3d__section-label">' + TEXT.cells + '</p>' +
      cellRows() +
      '<p class="ts-b3d__dim ts-b3d__section-label">' + TEXT.params + '</p>' +
      editorRows(mat);
    // 参数改动 → 回写 mat（纹理只写文件名）并重绘
    el.querySelectorAll("input[data-key], select[data-key], select[data-floor], input[data-cell], input[data-grid]").forEach(function (el2) {
      el2.onchange = function () {
        var v = el2.value;
        if (el2.dataset.cell) {                     // 单元 → 图集格子
          var u = el2.dataset.cell, ax = +el2.dataset.axis;
          DATA.cells[u] = DATA.cells[u] || [0, 0];
          DATA.cells[u][ax] = +v || 0;
          STYLE_TEX = {};                            // 合成纹理缓存失效
          draw();
          return;
        }
        if (el2.dataset.grid) {                      // 图集网格 列×行
          var gv = String(v).split(/\s+/).map(Number).filter(function (n) { return !isNaN(n); });
          if (gv.length >= 2) { DATA.atlas_grid = [gv[0], gv[1]]; STYLE_TEX = {}; draw(); }
          return;
        }
        if (el2.dataset.floor) {
          var fg = el2.dataset.floor.split(":");
          mat.floors[fg[0]][+fg[1]] = v || null;
          draw();
          return;
        }
        var k = el2.dataset.key;
        if (k === "atlas_texture") {                 // 换图集 → 合成纹理缓存失效
          mat.atlas_texture = v || DATA.default_atlas;
          STYLE_TEX = {};
          draw();
          return;
        }
        if (k === "detail_texture") mat.detail_texture = v || "wall_atlas1.png";
        else if (k === "atlas_texture") mat.atlas_texture = v || DATA.default_atlas;
        else if (k === "roof_texture") mat.roof.texture = v || "wall_atlas1.png";
        else if (k === "detail_texture_atlas_cell") mat.detail_cell = v.split(/\s+/).map(Number);
        else if (k === "roof_texture_atlas_cell") mat.roof.cell = v.split(/\s+/).map(Number);
        else if (k === "detail_texture_scale") mat.detail_scale = v;
        else if (k === "roof_texture_scale" || k === "roof_scale") mat.roof.scale = v;
        else if (k === "roof_color") mat.roof.color = v;
        else mat[k] = v;
        draw();
      };
    });
  }

  fetch(DATA_URL).then(function (r) { return r.json(); }).then(function (d) {
    DATA = d;
    ui();
  }).catch(function (e) {
    holder.innerHTML = '<p class="ts-b3d__dim">' + TEXT.dataFailed + ' (' + DATA_URL + '): ' + esc(e) + '</p>';
  });
})();
