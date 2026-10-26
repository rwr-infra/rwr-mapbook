/*
 * Building E 页面的 3D 预览（原生 WebGL，不引任何外部库）
 *
 * 数据来自地编模板 vao0822.svg（tools/building3d/build.py 解析成
 * docs/b3d/data.json，与贴图一起放在 docs/b3d/），链路是这样的：
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

  // 本脚本、data.json 与所有贴图同住在 <站点根>/b3d/ 下，所以只要拿到「自己这一
  // 份的根」就够：脚本地址去掉 b3d/viewer.js 剩下的就是根。用 currentScript 最准
  // （脚本是同步执行的），退路才是按 src 里带 viewer.js 反查。
  var self = document.currentScript || document.querySelector('script[src*="viewer.js"]');
  var BASE = "";
  if (self && self.src) {
    var u = new URL(self.src, location.href);
    BASE = u.pathname.replace(/b3d\/viewer\.js$/, "");
  }
  var B3D = BASE + "b3d/";
  var DATA_URL = B3D + "data.json";

  var DATA = null;          // data.json
  var IMG = {};             // 纹理缓存
  var STYLE_TEX = {};       // style → 合成好的墙面纹理
  var view = null;          // BoxView 实例
  // editable=false：按模板固定值来，素材下拉/格子输入只读；点「自定义调节」才解锁
  // lotW/lotD = 楼占地（SVG 单位，1 单位 0.5 m）；33×33 = 16.5×16.5 m
  // roofBlur / roofGrow / tileScale：屋顶瓦片缩放、斑驳扩散、斑驳模糊，已调到位的定值，
  // 不再挂滑条（滑条去掉后仍留在 state 里，渲染照读，改值只改这里）。
  var state = { name: "", floors: 4, lotW: 33, lotD: 33, wall: "#cfc9bd", roof: "#8a8578", bright: 1.05, rotX: 0.45, rotY: 0.6, zoom: 1, editable: false, wallDetail: true, roofCutout: true, roofBlur: 20, roofGrow: 0.02, tileScale: 2.8 };

  var LANG = (document.documentElement.lang || "zh-hans").toLowerCase();
  var COPY = {
    "zh-hans": {
      eyebrow: "交互式材质检查器", title: "建筑预览", live: "实时渲染",
      hint: "拖动旋转 · 滚轮或双指缩放", reset: "复位视角",
      customizeOff: "自定义调节：关", customizeOn: "自定义调节：开",
      customizeHint: "解锁后可更换素材与图集格子", building: "建筑",
      prevBuilding: "上一个建筑", nextBuilding: "下一个建筑", floors: "层数", lotW: "楼长（单位）", lotD: "楼宽（单位）",
      lotHint: "占地按 SVG 单位填，1 单位 = 0.5 m",
      wall: "墙面色", roof: "屋顶色",
      brightness: "亮度", details: "材质与图集参数", none: "（无）",
      wallDetail: "墙面遮罩层", roofCutout: "屋顶斑驳层",
      follower: "3D 预览 · 跟随", back: "回到原位", close: "收起",
      noWebgl: "这个浏览器没有启用 WebGL，无法显示预览。", failed: "预览出错：",
      dataFailed: "预览数据加载失败", atlas: "图集", grid: "网格 列×行",
      cells: "图集格子 atlas_cell（列 / 行，修改后实时更新）",
      params: "模板参数（修改后实时更新）", cellsUnit: " 格",
      pickCell: "点图集上的格子 → 指给该单元",
      cellSplit: "切分", cellSplitHint: "把这张贴图切成几列几行（列 × 行）",
      chooseUnit: "在图集上点一块，换到这里", addBlock: "新建小块",
      popBack: "返回", popDel: "删除",
      spanOf: "单元切分 宽×高（格）",
      faces: ["一层正面", "一层右面", "一层背面", "一层左面", "其它层正面", "其它层右面", "其它层背面", "其它层左面"]
    },
    "zh-hant": {
      eyebrow: "互動式材質檢查器", title: "建築預覽", live: "即時渲染",
      hint: "拖曳旋轉 · 滾輪或雙指縮放", reset: "重設視角",
      customizeOff: "自訂調節：關", customizeOn: "自訂調節：開",
      customizeHint: "解鎖後可更換素材與圖集格子", building: "建築",
      prevBuilding: "上一個建築", nextBuilding: "下一個建築", floors: "層數", lotW: "樓長（單位）", lotD: "樓寬（單位）",
      lotHint: "占地按 SVG 單位填，1 單位 = 0.5 m",
      wall: "牆面色", roof: "屋頂色",
      brightness: "亮度", details: "材質與圖集參數", none: "（無）",
      wallDetail: "牆面遮罩層", roofCutout: "屋頂斑駁層",
      follower: "3D 預覽 · 跟隨", back: "回到原位", close: "收起",
      noWebgl: "此瀏覽器未啟用 WebGL，無法顯示預覽。", failed: "預覽出錯：",
      dataFailed: "預覽資料載入失敗", atlas: "圖集", grid: "網格 欄×列",
      cells: "圖集格子 atlas_cell（欄 / 列，修改後即時更新）",
      params: "範本參數（修改後即時更新）", cellsUnit: " 格",
      pickCell: "點圖集上的格子 → 指給該單元",
      cellSplit: "切分", cellSplitHint: "把這張貼圖切成幾欄幾列（欄 × 列）",
      chooseUnit: "在圖集上點一塊，換到這裡", addBlock: "新建小塊",
      popBack: "返回", popDel: "刪除",
      spanOf: "單元切分 寬×高（格）",
      faces: ["一樓正面", "一樓右面", "一樓背面", "一樓左面", "其他樓層正面", "其他樓層右面", "其他樓層背面", "其他樓層左面"]
    },
    en: {
      eyebrow: "Interactive material inspector", title: "Building preview", live: "Live render",
      hint: "Drag to orbit · scroll or pinch to zoom", reset: "Reset view",
      customizeOff: "Custom controls: off", customizeOn: "Custom controls: on",
      customizeHint: "Unlock materials and atlas cells", building: "Building",
      prevBuilding: "Previous building", nextBuilding: "Next building", floors: "Floors", lotW: "Footprint length (units)", lotD: "Footprint width (units)",
      lotHint: "Footprint in SVG units; 1 unit = 0.5 m",
      wall: "Wall tint", roof: "Roof tint",
      brightness: "Brightness", details: "Material and atlas parameters", none: "(none)",
      wallDetail: "Wall detail mask", roofCutout: "Roof grime layer",
      follower: "3D preview · following", back: "Back to preview", close: "Dismiss",
      noWebgl: "WebGL is disabled in this browser, so the preview cannot be shown.", failed: "Preview error: ",
      dataFailed: "Preview data could not be loaded", atlas: "Atlas", grid: "Grid cols×rows",
      cells: "Atlas cells (column / row; updates live)", params: "Template parameters (updates live)",
      cellsUnit: " cells", pickCell: "Click an atlas cell to assign it",
      cellSplit: "Split", cellSplitHint: "How many columns × rows this texture is split into",
      chooseUnit: "Click an atlas cell for this block", addBlock: "New block",
      popBack: "Back", popDel: "Delete",
      spanOf: "Unit split w×h (cells)",
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
  // 英文名包成 <abbr title="中文">，站内 abbr-tap.js 会接管显示
  function abbr(text, tip) {
    if (!tip) return esc(text);
    return '<abbr title="' + esc(tip) + '">' + esc(text) + '</abbr>';
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function img(name) {
    if (!IMG[name]) {
      var i = new Image();
      i.src = B3D + name;
      IMG[name] = i;
    }
    return IMG[name];
  }
  function nums(str, fb) {
    var p = String(str == null ? "" : str).trim().split(/\s+/).map(Number).filter(function (n) { return !isNaN(n); });
    if (!p.length) return [fb, fb];
    return [p[0], p.length > 1 ? p[1] : p[0]];
  }
  // 每张图集自己的网格（data.json 的 atlas_grids）：换图集自动匹配，不用手数。
  // ⚠️ 之前全局一个 8×8，选 world_atlas1（16×16）这类图集整面墙的格子就全错位了。
  function gridOf(atlasName) {
    return (DATA.atlas_grids && DATA.atlas_grids[atlasName]) || DATA.atlas_grid || [8, 8];
  }
  // 四面样式下拉的候选：只给**现役材质实际在用**的 style（带格数），
  // 不再全量甩素材库——style 全集里有一批是极特殊图集/老系列的，选了也拼不对。
  var RELEVANT = null;
  function relevantStyles() {
    if (RELEVANT) return RELEVANT;
    var set = {};
    Object.keys(DATA.materials).forEach(function (n) {
      var m = DATA.materials[n];
      ["1st", "other"].forEach(function (g) {
        (m.floors[g] || []).forEach(function (s) { if (s && DATA.styles[s]) set[s] = 1; });
      });
    });
    RELEVANT = Object.keys(set).sort();
    return RELEVANT;
  }

  /* ── 把 style 拼成一条墙面纹理：sequence 每项 1~2 个单元，横向依次排开 ──
     ⚠️ 必须用**这一栋自己的图集** atlasName，且用这张图集自己的网格
     gridOf()——网格写死 8×8 的时代，非 8 列的图集整面墙格子全错位。 */
  // 单元切分：每个单元可单独设（DATA.cell_spans[单元名]=[宽格,高格]）；
  // 没单独设的用图集默认——配置在 tools/building3d/build.py 生成的 data.json
  // （atlas_spans / atlas_unit_spans），前端只在这份数据缺失时用下面的兜底。
  // building_atlas2/3/4 三张图集统一按「宽1×高2」编号（坐标表的行 0-3 就是按
  // 这种大格编的：门 [2,0]→基础行0-1、窗 [*,1]→基础行2-3）。像素换算必须
  // 坐标 × 原生格，不能按基础格算，否则整面墙的格子全错位。
  var DEFAULT_SPANS = {
    "building_atlas2.png": [1, 2],
    "building_atlas3.png": [1, 2],
    "building_atlas4.png": [1, 2]
  };
  // 三张图集统一按「宽1×高2」编号，目前没有需要回退成 1×1 的单元；
  // 保留此结构以便将来个别单元微调切分（按图集区分）。
  var ATLAS_UNIT_SPANS = {};
  function nativeSpan(ak) {
    var d = (DATA.atlas_spans && DATA.atlas_spans[ak]) || (ak && DEFAULT_SPANS[ak]);
    return (d && d[0] > 0 && d[1] > 0) ? d : [1, 1];
  }
  /* 原生格网格（大格数）：如 atlas2 = 8×4 个 32×64 大格 */
  function nativeGrid(ak) {
    var g = gridOf(ak), ns = nativeSpan(ak);
    return [Math.max(1, Math.floor(g[0] / ns[0])), Math.max(1, Math.floor(g[1] / ns[1]))];
  }
  function spanOf(u, ak) {
    var s = DATA.cell_spans && DATA.cell_spans[u];     // 用户手调优先
    if (s && s[0] > 0 && s[1] > 0) return s;
    var us = (DATA.atlas_unit_spans && DATA.atlas_unit_spans[ak]) ||
             (ak && ATLAS_UNIT_SPANS[ak]);
    s = us && us[u];                                   // 图集内个别单元回退
    if (s && s[0] > 0 && s[1] > 0) return s;
    return nativeSpan(ak);
  }
  function cellCodeText(u, ak) {
    var c = cellOf(u, ak);
    var sp = spanOf(u, ak);
    // 只在手动改过切分时追加后缀，图集默认（如 atlas2 的 1×2）不加，免得刷屏
    var custom = DATA.cell_spans && DATA.cell_spans[u];
    return c[0] + "," + c[1] + (custom ? " ·" + sp[0] + "×" + sp[1] : "");
  }

  /* ⚠️ building_atlas4 的「单元名 → 格子」要单独校正。
     data.json 里的坐标来自地编模板 vao0822.svg，是按模板默认图集 building_atlas2
     的「8 列 × 4 行（1 宽 × 2 高）」原生格编号的。atlas4 也按同一套 1×2 框
     解释，但它的内容分布不同：门是 64×128（1×2，整扇），窗图只占 64×128
     格子的上半段（下半透明），内容只在左上区域。按 1×2 坐标直接取会错位，
     这里逐格校正坐标；切分统一为 1×2，整格原样映射到一层楼面。
     ⚠️ 不要裁掉格子里的透明留白——那是窗户在楼层里的定位偏移，窗图贴在格内
     自然位置（贴顶、下方留白露砖），整格拉伸到一层高度即还原游戏排布。
     全站只有 BuildingWhite2（实拍那栋）用 atlas4，不影响 atlas2/atlas3 的材质。 */
  var ATLAS4_CELL_FIX = {
    "building_atlas4.png": {
      house_window: [1, 0],      // 窄窗（64×128 格上半段有图，下半透明=定位留白）
      house_window_big: [4, 0],  // 四格大窗（同）
      house_door: [0, 0],        // 双开门（64×128，整扇 1×2）
      house_empty: [0, 1]        // 1×2 框里 row≥1 都是空的；[5,4] 在 8×4 下越界
    }
  };
  function cellOf(unit, ak) {
    var fix = ATLAS4_CELL_FIX[ak];
    if (fix && fix[unit]) return fix[unit];
    return DATA.cells[unit] || [0, 0];
  }

  function styleTexture(styleName, atlasName) {
    var ak = atlasName || DATA.default_atlas;
    var ck = ak + "|" + styleName;
    if (STYLE_TEX[ck]) return STYLE_TEX[ck];
    var seq = DATA.styles[styleName];
    if (!seq) return null;
    var atlas = img(ak);
    if (!atlas.complete || !atlas.naturalWidth) return null;
    var g0 = gridOf(ak);
    var cw = atlas.naturalWidth / g0[0];
    var chh = atlas.naturalHeight / g0[1];
    // 每个单元按自己的切分裁：宽 spanCols 格、高 spanRows 格（atlas2 默认 1×2）
    var segs = [];
    seq.forEach(function (item) {
      item.forEach(function (unit) {
        var c = cellOf(unit, ak);
        var sp = spanOf(unit, ak);
        segs.push({ c: c, w: sp[0], h: sp[1] });
      });
    });
    if (!segs.length) return null;
    var out = document.createElement("canvas");
    out.width = segs.reduce(function (a, s) { return a + s.w * cw; }, 0);
    out.height = segs.reduce(function (a, s) { return Math.max(a, s.h); }, 1) * chh;
    var cx = out.getContext("2d");
    var ns = nativeSpan(ak);                   // 坐标按原生格换算成像素
    var x = 0;
    segs.forEach(function (s) {
      // 整格原样绘制：把 1×2 原生格（含格子里窗户上下的透明留白）按自然像素
      // 拷贝进条带，**不裁剪**。留白是窗户在楼层里的定位偏移，必须保留——
      // 整个格子映射到一层楼面，窗图落在格内自然位置（贴顶、下方留白露砖）。
      cx.drawImage(atlas, s.c[0] * cw * ns[0], s.c[1] * chh * ns[1], s.w * cw, s.h * chh,
        x, out.height - s.h * chh, s.w * cw, s.h * chh);
      x += s.w * cw;
    });
    out.__units = segs.length;
    // 真实宽高比（POT 拉伸前）：单元裁块 32×64 这种 1×2 的，映射到墙面时
    // 宽度跟着比例缩（高=1 个槽 → 宽=0.5 个槽），整条按 __units 均分宽会把
    // 窗户压成 1×1 方块——所以保留 __aw 让贴图按真实比例铺。
    out.__aw = out.width / out.height;
    // 每个单元占**整条宽**的比例（POT 拉伸后依然成立）：铺贴层用它逐单元
    // 裁源矩形、判定「单个单元在剩余墙宽里放不放得下」。__ufx[k] = 前 k 个
    // 单元的累计比例（源矩形左边界），__ufx[n] = 1。
    var uf = [], ufx = [0], acc = 0;
    segs.forEach(function (s) {
      var f = s.w * cw / out.width;
      uf.push(f); acc += f; ufx.push(acc);
    });
    out.__uf = uf;
    out.__ufx = ufx;
    // ⚠️ WebGL1 里非 2 的幂（如 224×32）的纹理配 REPEAT+mipmap 会采样失败
    //    （整面变透明、CSS 黑底透出）——统一拉伸到 2 的幂
    var pot = function (n) { var v = 1; while (v < n) v *= 2; return v; };
    var W = pot(out.width), H = pot(out.height);
    if (W !== out.width || H !== out.height) {
      var p2 = document.createElement("canvas");
      p2.width = W; p2.height = H;
      p2.getContext("2d").drawImage(out, 0, 0, W, H);
      p2.__units = segs.length;
      p2.__aw = out.__aw;
      p2.__uf = out.__uf;
      p2.__ufx = out.__ufx;
      STYLE_TEX[ck] = p2;
      return p2;
    }
    STYLE_TEX[ck] = out;
    return out;
  }

  /* ── 游戏世界常数（米）→ 预览单位 ─────────────────────────────────────
   * 标定链（原始数据 + 实拍截图对出来的；只作内部注释，页面不再列这些数）：
   *   terrain.cfg PageWorldX=1024 m  ↔  objects.svg 2048×2048
   *     ⇒ 1 SVG 单位 = 0.5 m；一栋 100×100 单位 = 50×50 m 的楼
   *   墙 style 槽宽   1.5625 m   = 50/32，整 4 个 8 元素序列，一格不剩
   *   层距（一窗行）   2.85 m     实拍窗行间距 97~98 px ÷ 33.2 px/m
   *   层间檐口       厚 0.20 m、凸出 0.33 m（左侧轮廓实测 11 px）
   *   墙 detail 格    2.00 m     detail_texture_scale 2 2（砖 ≈0.22 m）
   *   屋顶格          1.50 m     roof_texture_scale 1.5 1.5（瓦 16 texel ≈0.19 m）
   *   斑驳 cutout 格  15.0 m     detail_cutout_texture_scale 15 15
   *
   * ⚠️ METER 是「画布单位 / 米」的**恒定**换算，不随楼的大小变化：
   *    定标 = 一栋 100×100 单位（50×50 m）的楼在画布上占满 16.5 单位。
   *    所以楼占地填 33×33 时，它在画布上就只有 16.5/3 = 5.5 单位宽，
   *    而砖格 / 层高 / 槽宽这些世界周期**一个都不变**——跟游戏里
   *    「同一份材质贴在不同大小的 rect 上」是同一件事。
   */
  var FULL_LOT = 100;                    // 定标基准：100 SVG 单位的楼
  var FULL_W = 16.5;                     // 占满 16.5 画布单位
  var UNIT_M = 0.5;                      // 1 SVG 单位 = 0.5 m
  var METER = FULL_W / (FULL_LOT * UNIT_M);   // = 0.33 画布单位/米
  var SLOT = 1.5625 * METER;             // 一个 style 槽（方格）
  var FLOOR = 2.85 * METER;              // 一层 = 一个窗行（含层顶檐口）
  var LEDGE_T = 0.20 * METER;            // 檐口厚
  var LEDGE_P = 0.33 * METER;            // 檐口凸出墙面
  var BRICK = 2.00 * METER;              // 墙面 detail 格周期
  var TILE = 1.50 * METER;               // 屋顶格周期
  var GRIME = 15.0 * METER;              // cutout 斑驳格周期
  var MAX_FLOORS = 22;                   // 层数上限（参考楼 height=22）
  var MIN_LOT = 4, MAX_LOT = 400;        // 楼占地（SVG 单位）可调范围

  /* ── 场景：若干层盒子（四面各自的 style）+ 楼板 + 屋顶 ── */
  function buildScene(mat) {
    var boxes = [];
    // 地面：顶面正好在 y=0，建筑站在上面；大一圈，避免转视角时露出边
    boxes.push({ ground: true, size: [80, 0.6, 80], y: -0.6,
                 faces: { top: { tint: [0.36, 0.35, 0.33] },
                          default: { tint: [0.5, 0.5, 0.48] } } });
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
    // 楼占地按「SVG 单位」填（1 单位 = 0.5 m）：填 33×33 就是 16.5×16.5 m，
    // 在画布上占 5.5 单位宽（100×100 的楼占满 16.5）。层高/檐口/纹理周期
    // 是**世界常数**，不跟着楼大小变——楼越小，一面上能铺的槽/砖越少。
    // 门窗条按**单个单元**生成：从 style 序列逐个往右排，放不下的那个单元
    // 不生成、整行居中（见 composeWallFace ③）；砖块 detail 是连续纹理，
    // 平铺到边、被边缘切断无所谓。
    var lotW = Math.max(MIN_LOT, Math.min(+state.lotW || 33, MAX_LOT));
    var lotD = Math.max(MIN_LOT, Math.min(+state.lotD || 33, MAX_LOT));
    var W = lotW * UNIT_M * METER, D = lotD * UNIT_M * METER;
    // 墙面 detail 层（侧栏勾选，默认开）：**整面墙一张画布**（面级合成）——
    // ① 墙基色 → ② 砖块 detail 全平铺（跨层连续，砖缝不随楼层重开）→
    // ③ 砖块铺完后 cutout 整面上一次（不随楼层/画布重复）→ ④ 各层门窗条
    // **盖在墙纹之上**（source-over：窗/门是独立一层，砖纹不再透过窗玻璃；
    // 每层重开、**顶边贴本层檐口**）。
    // 一面墙对应一个盒子，tile [1,1]。砖块倍率固定 1.6、cutout 遮罩倍率固定 1
    //（原「墙面纹理缩放/遮罩缩放」滑杆已撤，侧栏换成了屋顶斑驳的模糊/扩散）。
    function composeWallFace(sideIdx) {
      // 画布固定 POT。横向 1024：一槽 0.52 单位 ≈ 32 px，窗格才不糊。
      var FW = 1024, FH = 1024;
      var sx = FW / faceW[sideIdx], sy = FH / total;
      var cv = document.createElement("canvas");
      cv.width = FW; cv.height = FH;
      var cx = cv.getContext("2d");
      cx.fillStyle = state.wall;
      cx.fillRect(0, 0, FW, FH);
      var dImg = img(mat.detail_texture || "wall_atlas1.png");
      if (state.wallDetail && dImg.complete && dImg.naturalWidth && mat.detail_cell) {
        // ① 砖块全平铺（世界周期 = BRICK×bs，跨层连续，砖缝不随楼层重开）。
        //    ⚠️ 砖块必须画在独立图层上：destination-in 对整个画布生效，
        //    直接怼在面画布上会把先铺的墙面基色一起抠穿（整面墙透明）。
        //    正确顺序：砖块图层平铺 → 图层内抠洞 → 整层盖回基色。
        var tile = cropCell(dImg, mat.detail_cell);
        var bs = 1.6;   // 砖块倍率固定 1.6（原「墙面纹理缩放」滑杆已撤，取用户调定的值）
        var pw = Math.max(2, BRICK * bs * sx), ph = Math.max(2, BRICK * bs * sy);
        var brick = document.createElement("canvas");
        brick.width = FW; brick.height = FH;
        var bx = brick.getContext("2d");
        for (var wy = 0; wy < FH; wy += ph)
          for (var wx = 0; wx < FW; wx += pw)
            bx.drawImage(tile, wx, FH - wy - ph, pw, ph);   // 从底往上铺
        // ② 砖块铺完 → cutout 整面上一次（遮罩缩放独立控制周期，只抠砖）
        if (mat.detail_cutout) {
          var dcim = img(mat.detail_cutout);
          if (dcim.complete && dcim.naturalWidth) {
            var ms = 1;   // 遮罩倍率固定 1（原「遮罩缩放」滑杆已撤）
            var dsc = nums(mat.detail_scale, [3, 3]), csc2 = nums(mat.detail_cutout_scale, mat.detail_scale || "3 3");
            var mc = document.createElement("canvas");
            mc.width = Math.max(2, Math.round(csc2[0] / dsc[0] * pw * ms));
            mc.height = Math.max(2, Math.round(csc2[1] / dsc[1] * ph * ms));
            var mx = mc.getContext("2d");
            mx.imageSmoothingEnabled = false;
            mx.drawImage(channelMask(dcim), 0, 0, mc.width, mc.height);
            bx.globalCompositeOperation = "destination-in";
            bx.fillStyle = bx.createPattern(mc, "repeat");
            bx.fillRect(0, 0, FW, FH);
            bx.globalCompositeOperation = "source-over";
          }
        }
        cx.drawImage(brick, 0, 0);
      }
      // ③ 各层门窗条盖在墙纹之上（source-over：窗是独立一层，砖纹不穿透）
      for (var f2 = 0; f2 < n; f2++) {
        var tf = tex[f2 === 0 ? "1st" : "other"][sideIdx];
        if (!tf) continue;
        // 窗条按**整层高度 FLOOR** 铺（不是 SLOT 槽宽）：一个 1×2 单元本来就
        // 映射到一整层，整格（含窗户上下的透明留白）原样拉伸到一层高度 → 窗图
        // 落在格内自然位置（贴顶、下方留白露砖），还原游戏里「单元→楼层」的
        // 排布。用 SLOT 当条高会把窗压成一层不到一半、且单格宽度只剩 ~0.78 m
        // （比 1.5625 m 槽宽窄一截，窗数偏多）。
        cx.globalCompositeOperation = "source-over";
        // 整窗机制（**按单个单元**判定）：从 style 序列第一个单元起逐个往右排，
        // 墙上放不下的那个单元不生成（宁缺勿切），排完的整行再居中——
        // 左右留白均分。例：下一个窗宽 10 m、右侧只剩 8 m → 该窗不生成，
        // 已排好的部分左留 4 m、右留 4 m。不是按整条组合块截断。
        // 每单元占整条宽的比例在 __uf/__ufx（POT 拉伸后仍成立）。
        var uf = tf.__uf, ufx = tf.__ufx;
        if (uf && uf.length) {
          var swT = tf.__aw * FLOOR * sx;         // 一整条组合块的世界宽 → px
          var swH = FLOOR * sy;                   // 一条窗行 = 一整层高
          var yTop = FH - (f2 + 1) * FLOOR * sy;
          var laid = [], cum = 0, k2 = 0, guard = 0;
          while (guard++ < 999) {
            var idx = k2 % uf.length;
            var uw2 = uf[idx] * swT;
            if (cum + uw2 > FW + 0.5) break;      // 这个单元放不下 → 到此为止
            laid.push(idx); cum += uw2; k2++;
          }
          var bx0 = (FW - cum) / 2;               // 整行居中，左右留白均分
          var xcur = bx0;
          laid.forEach(function (idx2) {
            cx.drawImage(tf, ufx[idx2] * tf.width, 0, uf[idx2] * tf.width, tf.height,
              xcur, yTop, uf[idx2] * swT, swH);
            xcur += uf[idx2] * swT;
          });
        }
        cx.globalCompositeOperation = "source-over";
      }
      // 稳定贴图键：同一面墙每次重绘复用同一个 GL 纹理、只重传像素。
      // （原来用随机键 → 每改一次参数就新建 4 张 1024² 纹理且从不释放）
      cv.__k = "wall" + sideIdx;
      return cv;
    }
    var fkeys = ["front", "right", "back", "left"];
    // front/back 铺在 X 向（宽 W），right/left 铺在 Z 向（深 D）——
    // 之前右/左面也按 W 算重复次数，进深改成 D 后会导致纹理被拉伸。
    var faceW = [W, W, D, D];
    var n = Math.max(1, Math.min(+state.floors || 11, MAX_FLOORS));
    var total = n * FLOOR;                 // 墙高（每层顶部自带檐口）
    var wallFaces = { top: { tint: hex2rgb(state.wall) }, bottom: { tint: hex2rgb(state.wall) } };
    fkeys.forEach(function (k, i) {
      var t = tex[n > 1 ? "other" : "1st"][i] || tex["1st"][i];
      wallFaces[k] = t
        ? { canvas: composeWallFace(i), tile: [1, 1], tint: [1, 1, 1] }
        : { tint: hex2rgb(state.wall) };
    });
    boxes.push({ size: [W, total, D], y: 0, faces: wallFaces });
    for (var f = 0; f < n; f++) {
      // 层间檐口：顶面压在 (f+1)×FLOOR，也就是本层的最上沿（窗贴着它）。
      // 实拍左侧轮廓实测：凸出 0.33 m、厚 0.20 m。层间的它和墙面同色
      // （SVG 材质参数里没有檐口的独立字段），所以跟随墙面色。
      // ⚠️ 最顶上那道（屋顶线）不是「层间分隔檐」：它用的是**屋顶基础色**，
      //    和屋顶薄片的侧面连成一条屋顶包边——实拍楼顶就是屋顶色压边，
      //    不是下面那种墙色檐口。
      var isTop = (f === n - 1);
      boxes.push({ size: [W + 2 * LEDGE_P, LEDGE_T, D + 2 * LEDGE_P],
                   y: (f + 1) * FLOOR - LEDGE_T,
                   faces: { default: { tint: hex2rgb(isTop ? state.roof : state.wall) } } });
    }
    // 屋顶：roof_texture（明暗遮罩）+ cutout **纯蒙版镂空**：
    //   cutout 本身不渲染，只作为蒙版对屋顶贴图裁剪——黑色部分（G=0）=
    //   纹理保留；白色部分（G=255，黄/白簇）= 抠空，直接露出纯屋顶色
    //   （不带任何纹理）。cutout 整张循环铺、周期 = 15 m（GRIME），边缘大幅柔化。
    // 整个顶面烘成一张 FACE² 画布（面级合成才能让 cutout 与纹理格错频衔接
    // 循环），面 tint 白、tile [1,1]。⚠️ 明暗烘进 RGB 时必须先铺黑底——
    // 明暗变化只存在于 alpha，WebGL 混合没开，透明画布上传后就是一片平涂
    // （"关掉斑驳层屋顶纹理消失"的根因）。镂空区 alpha=0，shader 端 discard。
    var r = mat.roof || {};
    var rImg = img(r.texture || "wall_atlas1.png");
    var roofFace = { tint: hex2rgb(state.roof) };
    var topW = W + 2 * LEDGE_P, topD = D + 2 * LEDGE_P;
    if (rImg.complete && rImg.naturalWidth && r.cell) {
      var FACE = 1024;
      var pxPer = FACE / topW;                 // 顶面画布上 1 个世界单位的像素数
      var face = document.createElement("canvas");
      face.width = FACE; face.height = FACE;
      var fx2 = face.getContext("2d");
      var rrgb = hex2rgb(state.roof);
      var rcss = "rgb(" + Math.round(rrgb[0] * 255) + "," + Math.round(rrgb[1] * 255) + "," + Math.round(rrgb[2] * 255) + ")";
      // 单格屋顶面：屋顶色 × (1 - 明暗 alpha)，**先铺黑底**再叠，烘成不透明
      var c = cropCell(rImg, r.cell);
      var rl = document.createElement("canvas");
      rl.width = c.width; rl.height = c.height;
      var rlx = rl.getContext("2d");
      rlx.fillStyle = rcss; rlx.fillRect(0, 0, c.width, c.height);
      rlx.globalCompositeOperation = "destination-out";
      rlx.drawImage(c, 0, 0);                  // alpha 越大 → 屋顶色越暗
      var base = document.createElement("canvas");
      base.width = c.width; base.height = c.height;
      var bsx = base.getContext("2d");
      bsx.fillStyle = "#000"; bsx.fillRect(0, 0, c.width, c.height);
      bsx.drawImage(rl, 0, 0);
      // 屋顶纹理格铺满整个顶面（格级明暗跟着 roof_texture 循环）。
      // 格的世界周期 = TILE（roof_texture_scale 1.5 m × METER）×瓦片缩放，
      // 默认 2.8（用户调定的观感值）；滑杆只做预览缩放。
      var ts = Math.max(0.1, state.tileScale || 1);
      var big = document.createElement("canvas");
      big.width = big.height = Math.max(4, Math.round(TILE * ts * pxPer));
      var bgx = big.getContext("2d");
      bgx.imageSmoothingEnabled = true;
      bgx.drawImage(base, 0, 0, big.width, big.height);
      var cellPat = fx2.createPattern(big, "repeat");
      if (r.cutout && state.roofCutout) {
        var rc = img(r.cutout);
        if (rc.complete && rc.naturalWidth) {
          // ① 镂空处直接露**纯屋顶色**（不带任何纹理）——屋顶是蓝的就露出蓝
          fx2.fillStyle = rcss;
          fx2.fillRect(0, 0, FACE, FACE);
          // ② 屋顶贴图画到独立画布上，cutout 只作蒙版对它镂空（本身不渲染）：
          //    白色部分（G=255）抠掉，黑色部分（G=0）保留纹理。
          //    斑驳格世界周期 = GRIME（15 m × METER）——cutout 没有图集格子，
          //    整张 cutout.png 就是一次循环。柔化/膨胀由面板滑杆实时调。
          var P = Math.max(64, Math.round(GRIME * pxPer));
          var gp = maskPatternCanvas(channelMask(rc), P, state.roofBlur, P * state.roofGrow);
          var roofTop = document.createElement("canvas");
          roofTop.width = FACE; roofTop.height = FACE;
          var rtx = roofTop.getContext("2d");
          rtx.fillStyle = cellPat;
          rtx.fillRect(0, 0, FACE, FACE);
          rtx.globalCompositeOperation = "destination-out";
          rtx.fillStyle = rtx.createPattern(gp, "repeat");
          rtx.fillRect(0, 0, FACE, FACE);
          fx2.drawImage(roofTop, 0, 0);          // 带洞的屋顶盖在纯色上
        }
      } else {
        fx2.fillStyle = cellPat;
        fx2.fillRect(0, 0, FACE, FACE);
      }
      face.__k = "roof";                      // 稳定贴图键，同墙面
      roofFace = { canvas: face, tile: [1, 1], tint: [1, 1, 1] };
    }
    // 屋顶侧面不用合成画布（镂空在 0.05 薄片侧面上没有意义），纯屋顶色即可
    var roofSide = { tint: hex2rgb(state.roof) };
    // ⚠️ 屋顶在游戏里没有厚度，就是往最上面那道檐上贴一层材质——这里只给
    //    0.05 的薄片，侧面基本看不见，直接压在顶层分隔檐上。
    boxes.push({ size: [topW, 0.05, topD], y: total - 0.02,
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
      // ⚠️ 建筑图集（building_atlas*）是 RGBA，背景是**透明黑**（alpha=0）：
      //    游戏里这些地方是镂空（窗洞/门洞/墙面空隙），墙色只染不透明的窗板。
      //    不 discard 的话透明区会画成不透明的黑块——整面墙看起来就是黑的。
      //    遮罩贴图（wall_atlas1 这类「RGB 全 0、只有 alpha 在变」的细节层，
      //    屋顶常用）：直接 t.rgb*uTint 会整片全黑，得用 alpha 把底色压暗。
      "if(uMask<0.5&&t.a<0.5)discard;" +
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
    var hit = this.texCache[key];
    if (hit) {
      // 命中说明这张纹理是墙面/屋顶这类"每次重绘都会换内容"的画布：
      // 复用同一个 GL 纹理、把新像素重传上去（不新建、不泄漏）。
      // __static 的（纯白底）就不用重传了。
      if (!canvas.__static) {
        gl.bindTexture(gl.TEXTURE_2D, hit);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas);
        gl.generateMipmap(gl.TEXTURE_2D);
      }
      return hit;
    }
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
    c.__static = true;                       // 内容不变，tex() 命中时不用重传
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
    // 取景：按场景包围盒算距离，楼多大楼小都正好占满画面。
    // 旧算法 span 里硬加 4.8（为正面箭头留的固定余量），33×33 的小楼
    // 会被推得很远、缩成画面一角；现在余量按箭头实际外伸（1.65）折算。
    var arrowZ = span / 2 + 1.65;              // 正面箭头最远点（arrowPos 的 z2）
    var zext = arrowZ + span / 2;              // 场景在 z 上的总跨度
    var f = 1 / Math.tan(45 * Math.PI / 360);
    var tanV = Math.tan(45 * Math.PI / 360);
    var tanH = tanV * cv.width / cv.height;    // 水平半视口（跟画布长宽比走）
    var rH = 0.5 * Math.hypot(span, zext);     // 水平对角线：任意旋转角都不出画
    var vExt = h * Math.cos(this.rotX) + zext * Math.sin(this.rotX);  // 俯视时深度投影进竖向
    var dist = Math.max(rH / tanH, (vExt / 2) / tanV) * 1.06 / this.zoom;
    // 取景中心：楼体几何中心、往 +Z（箭头侧）偏一点，让箭头一起入画
    var tx = 0, ty = h * 0.45, tz = (arrowZ - span / 2) / 2;
    var cx = tx + Math.sin(this.rotY) * Math.cos(this.rotX) * dist;
    var cy = ty + Math.sin(this.rotX) * dist;
    var cz = tz + Math.cos(this.rotY) * Math.cos(this.rotX) * dist;
    var z = norm3([cx - tx, cy - ty, cz - tz]), x3 = norm3(cross([0, 1, 0], z)), y3 = cross(z, x3);
    gl.uniformMatrix4fv(this.loc.uP, false, new Float32Array([
      f / (cv.width / cv.height), 0, 0, 0, 0, f, 0, 0, 0, 0, -1, -1, 0, 0, -0.1, 0]));
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
        // ↑ composeWallFace / 屋顶画布都会自带 __k（稳定键）。没有 __k 的走随机键。 
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
      '<div class="ts-b3d__basic"><div class="ts-b3d__field ts-b3d__field--wide">' +
      '<label for="b3dPick">' + TEXT.building + '</label>' +
      '<span class="ts-b3d__pickrow">' +
      '<select id="b3dPick">' + DATA.order.map(function (n) {
        return '<option value="' + n + '">' + n + '</option>';
      }).join("") + '</select>' +
      // 选择条右侧的上/下翻键：竖着叠一对小箭头，像数字框的加减（循环切换）
      '<span class="ts-b3d__spin">' +
      '<button type="button" class="ts-b3d__step" id="b3dPrev" title="' + esc(TEXT.prevBuilding) + '" aria-label="' + esc(TEXT.prevBuilding) + '">▲</button>' +
      '<button type="button" class="ts-b3d__step" id="b3dNext" title="' + esc(TEXT.nextBuilding) + '" aria-label="' + esc(TEXT.nextBuilding) + '">▼</button>' +
      '</span></span></div>' +
      '<label class="ts-b3d__field"><span>' + TEXT.floors + '</span><input type="number" id="b3dFloors" min="1" max="' + MAX_FLOORS + '" value="' + state.floors + '"></label>' +
      // 楼占地：按 SVG 单位填（1 单位 = 0.5 m）。楼改小只是能铺的槽/砖变少，
      // 砖格、层高这些世界周期不动——跟游戏里同一份材质贴不同大小的 rect 一样。
      '<label class="ts-b3d__field"><span>' + TEXT.lotW + '</span><input type="number" id="b3dLotW" min="' + MIN_LOT + '" max="' + MAX_LOT + '" value="' + state.lotW + '" title="' + esc(TEXT.lotHint) + '"></label>' +
      '<label class="ts-b3d__field"><span>' + TEXT.lotD + '</span><input type="number" id="b3dLotD" min="' + MIN_LOT + '" max="' + MAX_LOT + '" value="' + state.lotD + '" title="' + esc(TEXT.lotHint) + '"></label>' +
      '<div class="ts-b3d__colors">' +
      '<label class="ts-b3d__field ts-b3d__field--swatch"><span>' + TEXT.wall + '</span><input type="color" id="b3dWall" value="#cfc9bd"></label>' +
      '<label class="ts-b3d__field ts-b3d__field--swatch"><span>' + TEXT.roof + '</span><input type="color" id="b3dRoof" value="#8a8578"></label>' +
      '</div>' +
      // 墙面遮罩层 / 屋顶斑驳层：两个开关并在一行（半栏宽，各占一半）
      '<div class="ts-b3d__checks">' +
      '<label class="ts-b3d__field ts-b3d__field--check"><input type="checkbox" id="b3dWallDetail"' + (state.wallDetail ? " checked" : "") + '><span>' + TEXT.wallDetail + '</span></label>' +
      '<label class="ts-b3d__field ts-b3d__field--check"><input type="checkbox" id="b3dRoofCutout"' + (state.roofCutout ? " checked" : "") + '><span>' + TEXT.roofCutout + '</span></label>' +
      '</div></div>' +
      '<details class="ts-b3d__details"><summary>' + TEXT.details + '</summary><div class="ts-b3d__info" id="b3dInfo"></div></details>' +
      '</div></section>';
    var pick = document.getElementById("b3dPick");
    var fl = document.getElementById("b3dFloors");
    var wall = document.getElementById("b3dWall");
    var roof = document.getElementById("b3dRoof");
    var wdCk = document.getElementById("b3dWallDetail");
    var rcCk = document.getElementById("b3dRoofCutout");
    if (wdCk) wdCk.onchange = function () { state.wallDetail = wdCk.checked; draw(); };
    if (rcCk) rcCk.onchange = function () { state.roofCutout = rcCk.checked; draw(); };
    // 屋顶瓦片缩放 / 斑驳扩散 / 斑驳模糊三个参数已经定死在 state 里（2.8 / 0.02 / 20），
    // 不再暴露滑条：调好的值直接当常量用。
    // 换建筑：墙/屋顶色回到模板语义色（color/roof_color 指 fill 还是 stroke）
    function selectBuilding(name) {
      if (!name || !DATA.materials[name]) name = DATA.order[0];
      state.name = name;
      pick.value = name;
      applyMatColors(DATA.materials[name]);
      draw();
    }
    pick.onchange = function () { selectBuilding(pick.value); };
    // 上/下翻键：按 DATA.order 顺序循环切换
    function stepBuilding(d) {
      var i = DATA.order.indexOf(state.name);
      if (i < 0) i = 0;
      var n = DATA.order.length;
      selectBuilding(DATA.order[(i + d + n) % n]);
    }
    var prevBtn = document.getElementById("b3dPrev"), nextBtn = document.getElementById("b3dNext");
    if (prevBtn) prevBtn.onclick = function () { stepBuilding(-1); };
    if (nextBtn) nextBtn.onclick = function () { stepBuilding(1); };
    fl.onchange = function () { state.floors = +fl.value; draw(); };
    var lw = document.getElementById("b3dLotW"), ld = document.getElementById("b3dLotD");
    if (lw) lw.onchange = function () { state.lotW = +lw.value; draw(); };
    if (ld) ld.onchange = function () { state.lotD = +ld.value; draw(); };
    wall.oninput = function () { state.wall = wall.value; draw(); };
    roof.oninput = function () { state.roof = roof.value; draw(); };
    document.getElementById("b3dReset").onclick = function () {
      state.rotX = 0.45; state.rotY = 0.6; state.zoom = 1;
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
    // 默认楼：2020Busy（BuildingBritish4_1st 属极特殊素材 normandy，已整体剔除）
    state.name = DATA.materials["2020Busy"] ? "2020Busy" : DATA.order[0];
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
    var mat = DATA.materials[state.name];
    if (!mat) return;
    var cv = document.getElementById("b3dCanvas");
    if (!cv) return;
    // 等图集就位（第一帧可能还没解码完）
    // 墙面必须等当前建筑自己的 atlas_texture；只等 default_atlas 会让 British /
    // Normandy 等建筑在首帧永久退化成纯色墙，图片后来加载完也不会再触发绘制。
    var need = [DATA.default_atlas, mat.atlas_texture, mat.detail_texture, (mat.roof || {}).texture,
                (mat.roof || {}).cutout, (mat.roof || {}).cutout_b, mat.detail_cutout]
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
    // 按住顶栏（按钮除外）拖动浮窗：转成 left/top 定位，限制在视口内
    var bar = floatBox.querySelector(".ts-b3d__floatbar");
    if (bar) bar.addEventListener("pointerdown", function (ev) {
      if (ev.target.closest("button")) return;
      ev.preventDefault();
      var r = floatBox.getBoundingClientRect();
      var dx = ev.clientX - r.left, dy = ev.clientY - r.top;
      floatBox.style.right = "auto"; floatBox.style.bottom = "auto";
      floatBox.style.left = r.left + "px"; floatBox.style.top = r.top + "px";
      floatBox.classList.add("ts-b3d__float--drag");   // 关掉入场动画防拖动闪跳
      var move = function (e) {
        var x = Math.min(Math.max(0, e.clientX - dx), window.innerWidth - floatBox.offsetWidth);
        var y = Math.min(Math.max(0, e.clientY - dy), window.innerHeight - floatBox.offsetHeight);
        floatBox.style.left = x + "px"; floatBox.style.top = y + "px";
      };
      var up = function () {
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
        window.removeEventListener("pointercancel", up);
      };
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
      window.addEventListener("pointercancel", up);
    });
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
    // 只在「3D 预览」这一节内才出浮窗：上界 = 小节标题（h2#3d-…），下界 = 后面第一个
    // ## 标题的顶边（预览后面还有「其它」一节，不能再拿正文末尾当下界）。视口与这一节
    // 不相交（翻回表格区 / 其它 / 页脚）就隐藏，原位画布看得见时也不出浮窗。
    var article = host.closest("article") || document.body;
    var heading = document.querySelector('h2[id^="3d"]');
    var regionTop = heading || stage;
    var regionEnd = null;                       // 本节之后的第一个同级标题
    if (heading) {
      var heads = article.querySelectorAll("h2");
      for (var hi = 0; hi < heads.length; hi++) {
        if (heads[hi] === heading && heads[hi + 1]) { regionEnd = heads[hi + 1]; break; }
      }
    }
    var seenOnce = false;
    var update = function () {
      var canvasVisible = (function () {
        var r = stage.getBoundingClientRect();
        return r.bottom > 0 && r.top < window.innerHeight;
      })();
      var inRegion = (function () {
        var top = regionTop.getBoundingClientRect().top;
        var bottom = regionEnd
          ? regionEnd.getBoundingClientRect().top
          : article.getBoundingClientRect().bottom;
        return bottom > 0 && top < window.innerHeight;
      })();
      if (canvasVisible) {
        seenOnce = true;                        // 预览露过面才允许之后弹浮窗
        floatDismissed = false;                 // 回到原位就复位「收起」
        floatBox.hidden = true;
      } else if (inRegion && seenOnce && !floatDismissed) {
        floatBox.hidden = false;
        drawFloat();
      } else {
        floatBox.hidden = true;                 // 不在 3D 预览这一节 → 不显示
      }
    };
    var queued = false;
    var onScroll = function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; update(); });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
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
  /* cutout 遮罩：生成器已把颜色通道预转成真 alpha（<名>__mask.png）。
     ⚠️ 不能在前端读原 cutout.png 的颜色通道——它的 alpha 全 0，而浏览器 canvas
     按**预乘 alpha** 存储，drawImage 全透明图后 RGB 一律变 0（之前斑驳
     「怎么调都没变化」的根因）。 */ 
  function channelMask(im) {
    var cv = document.createElement("canvas");
    cv.width = im.naturalWidth; cv.height = im.naturalHeight;
    cv.getContext("2d").drawImage(im, 0, 0);
    return cv;
  }
  /* 把通道遮罩整张放大到 size²（双线性），再做大半径柔化——
     游戏实拍的露砖边缘不是硬边，用户要求加大模糊。 */
  function maskPatternCanvas(cm, size, blurPx, grow) {
    var up = document.createElement("canvas");
    up.width = up.height = size;
    var ux = up.getContext("2d");
    ux.imageSmoothingEnabled = true;
    ux.drawImage(cm, 0, 0, cm.width, cm.height, 0, 0, size, size);
    // 膨胀（dilate）：8 方向偏移重复绘制，alpha 叠加 = 白区向外扩 grow 像素
    if (grow > 0) {
      var dl = document.createElement("canvas");
      dl.width = dl.height = size;
      var dx = dl.getContext("2d");
      var r = Math.round(grow);
      for (var iy = -r; iy <= r; iy += r)
        for (var ix = -r; ix <= r; ix += r)
          dx.drawImage(up, ix, iy);
      up = dl;
    }
    var cv = document.createElement("canvas");
    cv.width = cv.height = size;
    var cx = cv.getContext("2d");
    cx.filter = "blur(" + (blurPx || 7) + "px)";
    cx.drawImage(up, 0, 0);
    return cv;
  }
  /* 按 atlas_cell 从图集裁一格：[列,行,总列,总行,边距u,边距v]。
     第 5/6 个数是 UV 内缩（0.0078125 = 256px 图的半像素），防止采样吃到
     相邻格子的颜色——裁矩形按整图 UV 往里缩。
     ⚠️ 输出画布必须保持 **2 的幂**：内缩后 252 这种尺寸配 REPEAT+mipmap
     在 WebGL1 是 incomplete texture，采样恒为黑（屋顶"开不开遮罩都全黑"
     的根因）。所以把内缩后的裁块再缩放回整格尺寸（无边距时 1:1 不变）。 */
  function pot(n) { var p = 1; while (p < n) p *= 2; return p; }
  function cropCell(im, cell) {
    var cols = cell[2] || 1, rows = cell[3] || cols;
    var cw = im.naturalWidth / cols, ch = im.naturalHeight / rows;
    var m0 = cell[4] || 0, m1 = cell[5] || 0;
    var sx = cell[0] * cw + m0 * im.naturalWidth;
    var sy = cell[1] * ch + m0 * im.naturalHeight;
    var sw = Math.max(1, cw - (m0 + m1) * im.naturalWidth);
    var sh = Math.max(1, ch - (m0 + m1) * im.naturalHeight);
    var cv = document.createElement("canvas");
    cv.width = pot(Math.max(1, Math.round(cw)));
    cv.height = pot(Math.max(1, Math.round(ch)));
    cv.getContext("2d").drawImage(im, sx, sy, sw, sh, 0, 0, cv.width, cv.height);
    return cv;
  }
  /* 把通道遮罩 cm 平铺**乘进** dst 的 alpha（cutout 语义：G=255 保留底图纹理、
     G=0 抠掉——用户实拍确认，不是涂黑）。fx/fy = cutout_scale / 底图_scale，
     即 cutout 覆盖的世界尺寸是底图一格的几倍 → tile 要**放大** fx 倍
     （之前除反了，一格 cutout 缩进底图一格，斑驳密了 36 倍）。
     ⚠️ 缩放必须关平滑，双线性会把遮罩糊成灰。 */
  function multiplyMask(dst, cm, fx, fy) {
    var tw = Math.max(1, Math.round(dst.width * fx)), th = Math.max(1, Math.round(dst.height * fy));
    var tc = document.createElement("canvas"); tc.width = tw; tc.height = th;
    var mtx = tc.getContext("2d");
    mtx.imageSmoothingEnabled = false;
    mtx.drawImage(cm, 0, 0, cm.width, cm.height, 0, 0, tw, th);
    var cx = dst.getContext("2d");
    cx.globalCompositeOperation = "destination-in";
    cx.fillStyle = cx.createPattern(tc, "repeat");
    cx.fillRect(0, 0, dst.width, dst.height);
    cx.globalCompositeOperation = "source-over";
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

  // 每个纹理字段只给「数据里真的在用」的候选，不混全量素材库：
  // atlas_texture → 实际引用的建筑图集；detail_texture / roof_texture → 各自引用的贴图
  var USED_TEX = null;
  function usedTex(field) {
    if (!USED_TEX) {
      USED_TEX = { atlas_texture: {}, detail_texture: {}, roof_texture: {} };
      Object.keys(DATA.materials).forEach(function (n) {
        var m = DATA.materials[n];
        if (m.atlas_texture) USED_TEX.atlas_texture[m.atlas_texture] = 1;
        if (m.detail_texture) USED_TEX.detail_texture[m.detail_texture] = 1;
        if (m.roof && m.roof.texture) USED_TEX.roof_texture[m.roof.texture] = 1;
      });
    }
    return Object.keys(USED_TEX[field] || {}).sort();
  }

  var texSelect = function (key, val) {
    let opts = '<option value="">' + TEXT.none + '</option>';
    const list = usedTex(key).slice();
    const cur = String(val || "").trim().split(/\s+/)[0];
    // 当前值不在「在用清单」里（比如从别的楼切过来）也要能显示，不能悄悄丢掉
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
      if (k === "atlas_texture") {
        // 图集选择搬到了面板最上面（atlasPickerRow，一层正面之前）：
        // 它管整栋八面所有单元，摆在参数列表里太靠后、也不好找。
        return;
      }
      if (/^(detail_texture|roof_texture)$/.test(k)) {
        // 纹理文件名字段 → 下拉（只列数据里在用的）；格子/缩放字段走普通输入框
        rows += '<div class="ts-b3d__kv"><span>' + label + '</span>' + texSelect(k, val) + '</div>';
        return;
      }
      if (k === "roof_texture_atlas_cell" || k === "detail_texture_atlas_cell") {
        // 屋顶 / 墙面材质格共用一套版式（以前两处各写一遍）：
        //   [名字]  [缩略图 + 列,行]        [切分 列 × 行]
        // 一件占一栏，正好填满 kv 的三条轨道；原来 6 个节点硬塞进 3 栏，
        // 后三个（切分那两个数字）会被挤到下一行、跑到标签底下去。
        var isRoof = k === "roof_texture_atlas_cell";
        var arr = (isRoof ? mat.roof.cell : mat.detail_cell) || (isRoof ? [0, 0, 1, 1] : [0, 0, 8, 8]);
        var kind = isRoof ? "roof" : "detail";
        var base = isRoof ? "Roof" : "Detail";
        rows += '<div class="ts-b3d__kv ts-b3d__kv--cell"><span>' + label + '</span>' +
          '<span class="ts-b3d__cellsrc">' +
          '<button type="button" class="ts-b3d__cellpick" data-pick' + kind + '="1" title="' +
          arr[0] + ',' + arr[1] + '"' + dis() + '>' +
          '<canvas width="28" height="28" data-' + kind + 'thumb></canvas></button>' +
          '<code data-' + kind + 'code>' + arr[0] + ',' + arr[1] + '</code></span>' +
          '<span class="ts-b3d__cellcut">' +
          '<span class="ts-b3d__dim">' + TEXT.cellSplit + '</span>' +
          '<input type="number" data-' + kind + 'dim="2" value="' + arr[2] + '" min="1" title="' + esc(TEXT.cellSplitHint) + '"' + dis() + '>' +
          '<span class="ts-b3d__dim">×</span>' +
          '<input type="number" data-' + kind + 'dim="3" value="' + arr[3] + '" min="1" title="' + esc(TEXT.cellSplitHint) + '"' + dis() + '>' +
          '</span></div>' +
          '<div class="ts-b3d__atlasbox" id="b3d' + base + 'Box" hidden>' +
          '<span class="ts-b3d__dim">' + TEXT.pickCell + '</span>' +
          '<canvas id="b3d' + base + 'Pick" width="224" height="224"></canvas></div>';
        return;
      }
      rows += '<div class="ts-b3d__kv"><span>' + label + '</span>' +
        '<input data-key="' + k + '" value="' + String(val).replace(/"/g, "&quot;") + '"' + dis() + '></div>';
    });
    return rows;
  }

  // 图集选择（整张图集缩小 + 网格线，点图换图集）——摆在面板最上面、
  // 「一层正面」之前：它管整栋楼八面所有单元，是全局设定，放最前才对。
  function atlasPickerRow(mat) {
    var curA = mat.atlas_texture || DATA.default_atlas;
    var cands = usedTex("atlas_texture").slice();
    if (cands.indexOf(curA) < 0) cands.unshift(curA);
    return '<div class="ts-b3d__kv ts-b3d__kv--wide"><span>' + TEXT.atlas + '</span><div class="ts-b3d__atlases">' +
      cands.map(function (a) {
        return '<button type="button" class="ts-b3d__atlasopt' + (a === curA ? " ts-b3d__atlasopt--on" : "") + '"' +
          ' data-atlas="' + esc(a) + '" title="' + esc(a) + '"' + dis() + '>' +
          '<canvas width="40" height="40" data-atlasthumb="' + esc(a) + '"></canvas>' +
          '<code>' + esc(a) + '</code></button>';
      }).join("") + '</div></div>';
  }

  // 选格器展开状态（跨 draw()→info() 重建保留）：null=都收起 / "wall"=墙面 / "roof"=屋顶
  // popOpen = 展开了选单元列表的那个面（"1st:0" 这类），popIdx = 该面序列里的扁平序号，-1 = 新建小块
  var pickOpen = null, activeUnit = null, popOpen = null, popIdx = -1;

  function info(mat) {
    var el = document.getElementById("b3dInfo");
    if (!el) return;
    var f = mat.floors;
    var canEdit = state.editable;
    // 每层每面的 style：默认只读展示（带中文注释）；开了自定义调节就能下拉换。
    // ⚠️ 下拉候选只列 relevantStyles()（现役材质在用的），不再全量素材库。
    // 配方条：把选中样式的 sequence 按从左到右画成一排单元小图（所见即所得的
    // 「一面墙怎么拼」）。块与块之间不加间隔、直接相连（就像真实墙面上那一条带）。
    // 每个小块可点（解锁后）：点开下方展开一个「选单元」列表，点了就把这个
    // 位置的单元换掉；条尾还有「＋新建小块」，往序列末尾追加新单元。
    function flatSeq(seq) {
      var out = [];
      seq.forEach(function (item, i) { item.forEach(function (u, j) { out.push([i, j, u]); }); });
      return out;
    }
    function cellPopup(styleName, idx) {
      var append = idx < 0;
      var cur = null;
      if (!append) {
        var e = flatSeq(DATA.styles[styleName] || [])[idx];
        if (e) cur = e[2];
      }
      var head = '<div class="ts-b3d__cellpop-head"><span class="ts-b3d__dim">' +
        (append ? TEXT.addBlock : TEXT.chooseUnit) + '</span>' +
        (cur ? '<code>' + esc(cur) + '</code>' : "") +
        '<span class="ts-b3d__cellpop-btns">' +
        '<button type="button" class="ts-b3d__popatlas" data-popback="1"' + dis() + '>' + TEXT.popBack + '</button>' +
        (!append ? '<button type="button" class="ts-b3d__popatlas ts-b3d__popatlas--del" data-popdel="1"' + dis() + '>' + TEXT.popDel + '</button>' : "") +
        '</span></div>';
      // 直接在图集大图上点格子 → 把那格指给这个小块（有同名单元就用名字，
      // 没有就按 列,行 现造一个自定义单元）；比一排缩略图直观。
      var body = '<canvas id="b3dPopPick" width="224" height="224"></canvas>' +
        (cur ? '<div class="ts-b3d__kv ts-b3d__spanrow"><span>' + TEXT.spanOf + '</span>' +
        '<input type="number" data-span="0" min="1" value="1" style="width:42px"' + dis() + '>' +
        '<span class="ts-b3d__dim">×</span>' +
        '<input type="number" data-span="1" min="1" value="1" style="width:42px"' + dis() + '>' +
        '<code data-spanunit></code></div>' : "");
      return '<div class="ts-b3d__cellpop">' + head + body + '</div>';
    }
    function recipeStrip(styleName, fk) {
      var seq = DATA.styles[styleName];
      if (!seq || !seq.length) return "";
      var blocks = [];
      flatSeq(seq).forEach(function (e, idx) {
        var u = e[2], sp = spanOf(u, mat.atlas_texture);
        blocks.push('<button type="button" class="ts-b3d__recipeblock" data-seg="' + fk + '" data-segidx="' + idx + '"' +
          ' title="' + esc(u + " " + cellCodeText(u, mat.atlas_texture)) + '"' + dis() + '>' +
          '<canvas width="' + (32 * sp[0]) + '" height="' + (32 * sp[1]) + '"' +
          ' data-rthumb="' + esc(u) + '"' +
          (/(^|_)empty/.test(u) ? ' class="ts-b3d__recipeempty"' : "") + '></canvas></button>');
      });
      if (canEdit)
        blocks.push('<button type="button" class="ts-b3d__recipeadd" data-segadd="' + fk + '" title="' + TEXT.addBlock + '"' + dis() + '>＋</button>');
      return '<div class="ts-b3d__recipe">' + blocks.join("") + '</div>';
    }
    function faceRow(label, g, i) {
      var val = f[g][i] || "", fk = g + ":" + i;
      // 每个面一组：标签行 + 配方条（+展开的选格页），分割线画在这组的最下面
      //（原来压在标签和小块中间，看着像把墙带和它的名字隔开了）。
      // 只读模式不再打 style 名（apartment1_1st_floor_busy 这类游戏内部 ID 对人没意义）；
      // 没配样式的面留个短横。
      if (!canEdit)
        return '<div class="ts-b3d__face">' +
          '<div class="ts-b3d__kv"><span>' + label + '</span>' +
          (val ? "" : '<span class="ts-b3d__dim">—</span>') + '</div>' +
          recipeStrip(val, fk) + '</div>';
      var rel = relevantStyles();
      var opts = '<option value="">' + TEXT.none + '</option>';
      rel.forEach(function (s) {
        var seq = DATA.styles[s] || [];
        var n = seq.reduce(function (a, it) { return a + it.length; }, 0);
        opts += '<option value="' + s + '"' + (s === val ? " selected" : "") + '>' +
          esc(s) + ' (' + n + TEXT.cellsUnit + ')</option>';
      });
      // 当前值不在候选里（比如从别的建筑切过来）也要能显示，不能悄悄丢掉
      if (val && rel.indexOf(val) < 0)
        opts = '<option value="' + val + '" selected>' + esc(val) + '</option>' + opts;
      return '<div class="ts-b3d__face">' +
        '<div class="ts-b3d__kv"><span>' + label + '</span><select data-floor="' + fk + '" style="max-width:170px">' + opts + '</select></div>' +
        recipeStrip(val, fk) +
        (popOpen === fk ? cellPopup(val, popIdx) : "") + '</div>';
    }
    // 图集格子（atlas_cell）：本栋 8 个面用到的基础单元。改成「小图预览 +
    // 点大图选格」，替代原来手敲 列/行 数字——格子指错整面墙就乱，看图选最直观。
    var units = [];
    ["1st", "other"].forEach(function (g) {
      (f[g] || []).forEach(function (s) {
        (DATA.styles[s] || []).forEach(function (item) {
          item.forEach(function (u) { if (units.indexOf(u) < 0) units.push(u); });
        });
      });
    });
    function cellRows() {
      // 图集本身的选择挪到面板最上面（atlasPickerRow），这里只留这张图集的网格；
      // 选格走配方条小块点开的弹出页（里面就是这张图集的大图）。
      return '<div class="ts-b3d__kv"><span>' + TEXT.grid + '</span>' +
        '<input data-grid="1" value="' + gridOf(mat.atlas_texture).join(" ") + '" style="width:56px"' + dis() + '></div>';
    }
    el.innerHTML =
      atlasPickerRow(mat) +
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
    el.querySelectorAll("input[data-key], select[data-key], select[data-floor], input[data-grid]").forEach(function (el2) {
      el2.onchange = function () {
        var v = el2.value;
        if (el2.dataset.grid) {                      // 图集网格 列×行 → 记到这张图集名下
          var gv = String(v).split(/\s+/).map(Number).filter(function (n) { return !isNaN(n); });
          if (gv.length >= 2) {
            DATA.atlas_grids = DATA.atlas_grids || {};
            DATA.atlas_grids[mat.atlas_texture || DATA.default_atlas] = [gv[0], gv[1]];
            DATA.atlas_grid = [gv[0], gv[1]];
            var ngv = nativeGrid(mat.atlas_texture || DATA.default_atlas);
            units.forEach(function (u) {             // 网格变小 → 越界格子收回最后一格（按原生格）
              var c = DATA.cells[u];
              if (!c) return;
              if (c[0] >= ngv[0]) c[0] = ngv[0] - 1;
              if (c[1] >= ngv[1]) c[1] = ngv[1] - 1;
            });
            STYLE_TEX = {}; draw();
          }
          return;
        }
        if (el2.dataset.floor) {
          var fg = el2.dataset.floor.split(":");
          mat.floors[fg[0]][+fg[1]] = v || null;
          draw();
          return;
        }
        var k = el2.dataset.key;
        if (k === "atlas_texture") {                 // 换图集 → 网格自动匹配 + 缓存失效
          mat.atlas_texture = v || DATA.default_atlas;
          DATA.atlas_grid = gridOf(mat.atlas_texture);
          STYLE_TEX = {};
          draw();
          return;
        }
        if (k === "detail_texture") mat.detail_texture = v || "wall_atlas1.png";
        else if (k === "roof_texture") {
          mat.roof.texture = v || "wall_atlas1.png";
          paintRoofThumb(); paintRoofPicker();          // 屋顶贴图换了 → 缩略图/大图重画
        }
        else if (k === "detail_texture_atlas_cell") mat.detail_cell = v.split(/\s+/).map(Number);
        else if (k === "roof_texture_atlas_cell") mat.roof.cell = v.split(/\s+/).map(Number);
        else if (k === "detail_texture_scale") mat.detail_scale = v;
        else if (k === "roof_texture_scale" || k === "roof_scale") mat.roof.scale = v;
        else if (k === "roof_color") mat.roof.color = v;
        else mat[k] = v;
        draw();
      };
    });

    /* ── 弹出页里的图集大图：点哪格就把那格指给这个小块 ──
       画布在弹出页（#b3dPopPick）里，随 popOpen 渲染，重建面板后重画。 */
    function atlasOf() {
      var ak = mat.atlas_texture || DATA.default_atlas;
      return { ak: ak, g: gridOf(ak), atlas: img(ak) };
    }
    function paintThumbs() {
      var a = atlasOf();
      if (!a.atlas.complete || !a.atlas.naturalWidth) return;
      var cw = a.atlas.naturalWidth / a.g[0], ch = a.atlas.naturalHeight / a.g[1];
      var ns = nativeSpan(a.ak);
      el.querySelectorAll("canvas[data-thumb]").forEach(function (cnv) {
        var u = cnv.dataset.thumb;
        var c = cellOf(u, a.ak);            // 走 cellOf：atlas4 的校正格才画得对
        var sp = spanOf(u, a.ak);
        var cx = cnv.getContext("2d");
        cx.clearRect(0, 0, cnv.width, cnv.height);
        cx.drawImage(a.atlas, c[0] * cw * ns[0], c[1] * ch * ns[1], sp[0] * cw, sp[1] * ch, 0, 0, cnv.width, cnv.height);
      });
    }
    // 配方条：各面样式 sequence 的单元小图（换样式 draw() 重建面板后重画）
    function paintRecipes() {
      var a = atlasOf();
      if (!a.atlas.complete || !a.atlas.naturalWidth) return;
      var cw = a.atlas.naturalWidth / a.g[0], ch = a.atlas.naturalHeight / a.g[1];
      var ns = nativeSpan(a.ak);
      el.querySelectorAll("canvas[data-rthumb]").forEach(function (cnv) {
        var u = cnv.dataset.rthumb;
        var c = cellOf(u, a.ak);            // 同上：配方条也按校正后的格画
        var sp = spanOf(u, a.ak);
        var cx = cnv.getContext("2d");
        cx.imageSmoothingEnabled = false;
        cx.clearRect(0, 0, cnv.width, cnv.height);
        cx.drawImage(a.atlas, c[0] * cw * ns[0], c[1] * ch * ns[1], sp[0] * cw, sp[1] * ch, 0, 0, cnv.width, cnv.height);
      });
    }
    function paintPicker() {
      var a = atlasOf();
      var cv = document.getElementById("b3dPopPick");
      if (!cv || !a.atlas.complete || !a.atlas.naturalWidth) return;
      var S = cv.width, cx = cv.getContext("2d");
      var ng = nativeGrid(a.ak);                 // 大格网格（atlas2 = 8×4）
      var ns = nativeSpan(a.ak);
      cx.imageSmoothingEnabled = false;
      cx.clearRect(0, 0, S, S);
      cx.drawImage(a.atlas, 0, 0, a.atlas.naturalWidth, a.atlas.naturalHeight, 0, 0, S, S);
      cx.lineWidth = 1; cx.strokeStyle = "rgba(0,0,0,0.4)";
      for (var i = 1; i < ng[0]; i++) { cx.beginPath(); cx.moveTo(i * S / ng[0] + 0.5, 0); cx.lineTo(i * S / ng[0] + 0.5, S); cx.stroke(); }
      for (var j = 1; j < ng[1]; j++) { cx.beginPath(); cx.moveTo(0, j * S / ng[1] + 0.5); cx.lineTo(S, j * S / ng[1] + 0.5); cx.stroke(); }
      // 已被占用的格子描白框（按各单元自己的切分画整块），正要指的那个描红框
      units.forEach(function (u) {
        var c = cellOf(u, a.ak);            // 用校正后的格：atlas4 描框才对位
        if (!c) return;
        var sp = spanOf(u, a.ak);
        cx.lineWidth = u === activeUnit ? 2 : 1;
        cx.strokeStyle = u === activeUnit ? "#e24b4a" : "rgba(255,255,255,0.9)";
        cx.strokeRect(c[0] * ns[0] * S / a.g[0] + 1, c[1] * ns[1] * S / a.g[1] + 1,
                      sp[0] * S / a.g[0] - 2, sp[1] * S / a.g[1] - 2);
      });
    }
    // 列表里的坐标徽章 + 选格框里的切分输入，跟当前单元同步
    function syncSpanUI() {
      units.forEach(function (u) {
        var code = el.querySelector('[data-cellcode="' + u + '"]');
        if (code) code.textContent = cellCodeText(u, atlasOf().ak);
      });
      if (!activeUnit) return;
      var sp = spanOf(activeUnit, atlasOf().ak);
      el.querySelectorAll("input[data-span]").forEach(function (inp) {
        inp.value = sp[+inp.dataset.span];
      });
      var su = el.querySelector("[data-spanunit]");
      if (su) su.textContent = activeUnit;
    }
    // 点配方条上的小块 → 展开/收起该面的图集选格页（activeUnit 记当前单元，
    // 「单元切分」跟着它走）；在图集上点格子 = 把那格指给这个位置。
    el.querySelectorAll("[data-seg]").forEach(function (btn) {
      btn.onclick = function () {
        if (!state.editable) return;
        var k = btn.dataset.seg, idx = +btn.dataset.segidx;
        if (popOpen === k && popIdx === idx) { popOpen = null; popIdx = -1; activeUnit = null; }
        else {
          popOpen = k; popIdx = idx;
          var sv0 = mat.floors[k.split(":")[0]] && mat.floors[k.split(":")[0]][+k.split(":")[1]];
          var e0 = sv0 ? flatSeq(DATA.styles[sv0] || [])[idx] : null;
          activeUnit = e0 ? e0[2] : null;
        }
        pickOpen = null;                               // 与屋顶/材质选格框互斥
        draw();                                        // 重建面板：弹出页内联渲染
      };
    });
    // 条尾「＋新建小块」→ 同款图集选格页，点中的格子追加到序列末尾（扩展排序）
    el.querySelectorAll("[data-segadd]").forEach(function (btn) {
      btn.onclick = function () {
        if (!state.editable) return;
        var k = btn.dataset.segadd;
        if (popOpen === k && popIdx === -1) { popOpen = null; popIdx = -1; activeUnit = null; }
        else { popOpen = k; popIdx = -1; activeUnit = null; }
        pickOpen = null;
        draw();
      };
    });
    // 弹出页：把图集上点中的格子变成单元指给这块——已有单元占这格就直接用
    // 它的名字；没有就按 列,行 现造一个自定义单元（custom_r行c列）。
    function assignCell(col, row) {
      if (!state.editable || popOpen == null) return;
      var a = atlasOf();
      var hit = null;
      Object.keys(DATA.cells).forEach(function (u) {
        var c = cellOf(u, a.ak);
        if (!hit && c && c[0] === col && c[1] === row) hit = u;
      });
      var name = hit || ("custom_r" + row + "c" + col);
      if (!hit) DATA.cells[name] = [col, row];
      var p = popOpen.split(":");
      var sv = mat.floors[p[0]] && mat.floors[p[0]][+p[1]];
      if (!sv) return;
      var seq = DATA.styles[sv] || (DATA.styles[sv] = []);
      if (popIdx < 0) {                                            // 新建小块
        seq.push([name]);
        popIdx = flatSeq(seq).length - 1;            // 弹出页切到新块的页
      } else {
        var e = flatSeq(seq)[popIdx];
        if (e) seq[e[0]][e[1]] = name;                             // 替换这块
      }
      activeUnit = name;
      STYLE_TEX = {};                                // 合成纹理缓存失效
      draw();                                        // 重建：块图/红框/切分同步
    }
    // 弹出页的图集大图：点格子 = 选格（按大格算，atlas2 = 8×4）
    var popCv = document.getElementById("b3dPopPick");
    if (popCv) popCv.addEventListener("click", function (ev) {
      var a = atlasOf();
      var ng = nativeGrid(a.ak);
      var r = popCv.getBoundingClientRect();
      var col = Math.min(ng[0] - 1, Math.max(0, Math.floor((ev.clientX - r.left) / r.width * ng[0])));
      var row = Math.min(ng[1] - 1, Math.max(0, Math.floor((ev.clientY - r.top) / r.height * ng[1])));
      assignCell(col, row);
    });
    // 「返回」：收起弹出页，不改任何东西
    el.querySelectorAll("[data-popback]").forEach(function (btn) {
      btn.onclick = function () {
        popOpen = null; popIdx = -1; activeUnit = null;
        draw();
      };
    });
    // 「删除」：把弹出页对应的这个块从序列里删掉（l/r 成对的另一半保留）
    el.querySelectorAll("[data-popdel]").forEach(function (btn) {
      btn.onclick = function () {
        if (!state.editable || popOpen == null || popIdx < 0) return;
        var p = popOpen.split(":");
        var sv = mat.floors[p[0]] && mat.floors[p[0]][+p[1]];
        var seq = sv ? DATA.styles[sv] : null;
        var e = seq ? flatSeq(seq)[popIdx] : null;
        if (e) {
          seq[e[0]].splice(e[1], 1);
          if (!seq[e[0]].length) seq.splice(e[0], 1);  // 半边删空了，整项拿掉
          STYLE_TEX = {};
        }
        popOpen = null; popIdx = -1; activeUnit = null;
        draw();
      };
    });
    // 单元切分（宽×高格数）：每个单元各自一份，改哪格只影响那一格
    el.querySelectorAll("input[data-span]").forEach(function (inp) {
      inp.onchange = function () {
        if (!activeUnit || !state.editable) return;
        var n = Math.max(1, Math.round(+inp.value) || 1);
        inp.value = n;
        DATA.cell_spans = DATA.cell_spans || {};
        DATA.cell_spans[activeUnit] = DATA.cell_spans[activeUnit] || [1, 1];
        DATA.cell_spans[activeUnit][+inp.dataset.span] = n;
        var a = atlasOf(), c = DATA.cells[activeUnit] || (DATA.cells[activeUnit] = [0, 0]);  // 整块别出图集右/下边界
        var sp0 = spanOf(activeUnit, a.ak), ns0 = nativeSpan(a.ak);
        if (c[0] * ns0[0] + sp0[0] > a.g[0]) c[0] = Math.max(0, Math.floor((a.g[0] - sp0[0]) / ns0[0]));
        if (c[1] * ns0[1] + sp0[1] > a.g[1]) c[1] = Math.max(0, Math.floor((a.g[1] - sp0[1]) / ns0[1]));
        STYLE_TEX = {};                                // 合成纹理缓存失效
        syncSpanUI(); paintThumbs(); paintPicker();
        draw();
      };
    });
    /* ── 屋顶格子：同款「小图 + 点大图选格」。区别于墙面单元：屋顶贴图不是
       固定网格的图集，切几列几行由 roof.cell 的第 3、4 个数定义，
       所以网格随输入变，点大图只定 列/行。 ── */
    var roofBox = document.getElementById("b3dRoofBox");
    var roofCv = document.getElementById("b3dRoofPick");
    function roofDims() {
      var c = mat.roof.cell || [0, 0, 1, 1];
      return [Math.max(1, c[2] | 0), Math.max(1, c[3] | 0)];
    }
    function paintRoofThumb() {
      var cnv = el.querySelector("canvas[data-roofthumb]");
      if (!cnv) return;
      var rImg2 = img(mat.roof.texture);
      if (!rImg2.complete || !rImg2.naturalWidth) return;
      var c = mat.roof.cell || [0, 0, 1, 1];
      var cw = rImg2.naturalWidth / Math.max(1, c[2] | 0);
      var ch2 = rImg2.naturalHeight / Math.max(1, c[3] | 0);
      var cx = cnv.getContext("2d");
      cx.clearRect(0, 0, cnv.width, cnv.height);
      cx.drawImage(rImg2, c[0] * cw, c[1] * ch2, cw, ch2, 0, 0, cnv.width, cnv.height);
    }
    function paintRoofPicker() {
      if (!roofCv || !roofBox || roofBox.hidden) return;
      var rImg2 = img(mat.roof.texture);
      if (!rImg2.complete || !rImg2.naturalWidth) return;
      var S = roofCv.width, cx = roofCv.getContext("2d");
      var d = roofDims(), c = mat.roof.cell || [0, 0, 0, 0];
      cx.imageSmoothingEnabled = false;
      cx.clearRect(0, 0, S, S);
      cx.drawImage(rImg2, 0, 0, rImg2.naturalWidth, rImg2.naturalHeight, 0, 0, S, S);
      cx.lineWidth = 1; cx.strokeStyle = "rgba(0,0,0,0.4)";
      for (var i = 1; i < d[0]; i++) { cx.beginPath(); cx.moveTo(i * S / d[0] + 0.5, 0); cx.lineTo(i * S / d[0] + 0.5, S); cx.stroke(); }
      for (var j = 1; j < d[1]; j++) { cx.beginPath(); cx.moveTo(0, j * S / d[1] + 0.5); cx.lineTo(S, j * S / d[1] + 0.5); cx.stroke(); }
      // 当前选中的格子描红框（屋顶贴图只有本栋在用，不用描占用白框）
      cx.lineWidth = 2; cx.strokeStyle = "#e24b4a";
      cx.strokeRect(c[0] * S / d[0] + 1, c[1] * S / d[1] + 1, S / d[0] - 2, S / d[1] - 2);
    }
    var roofBtn = el.querySelector("[data-pickroof]");
    if (roofBtn) roofBtn.onclick = function () {
      if (!state.editable) return;
      if (pickOpen === "roof") { pickOpen = null; roofBox.hidden = true; return; }
      pickOpen = "roof"; activeUnit = null;            // 两框互斥
      popOpen = null; popIdx = -1;                     // 与配方条弹出页互斥
      var dbg1 = document.getElementById("b3dDetailBox");
      if (dbg1) dbg1.hidden = true;
      roofBox.hidden = false;
      paintRoofPicker();
    };
    if (roofCv) roofCv.addEventListener("click", function (ev) {
      if (!roofBox || roofBox.hidden || !state.editable) return;
      var rImg2 = img(mat.roof.texture);
      if (!rImg2.complete || !rImg2.naturalWidth) return;
      var d = roofDims();
      var r = roofCv.getBoundingClientRect();
      var col = Math.min(d[0] - 1, Math.max(0, Math.floor((ev.clientX - r.left) / r.width * d[0])));
      var row = Math.min(d[1] - 1, Math.max(0, Math.floor((ev.clientY - r.top) / r.height * d[1])));
      mat.roof.cell = mat.roof.cell || [0, 0, 1, 1];
      mat.roof.cell[0] = col; mat.roof.cell[1] = row;
      var code = el.querySelector("[data-roofcode]");
      if (code) code.textContent = col + "," + row;
      if (roofBtn) roofBtn.title = col + "," + row;
      paintRoofThumb(); paintRoofPicker();
      draw();
    });
    el.querySelectorAll("input[data-roofdim]").forEach(function (el2) {
      el2.onchange = function () {
        var n = Math.max(1, Math.round(+el2.value) || 1);
        el2.value = n;
        mat.roof.cell = mat.roof.cell || [0, 0, 1, 1];
        mat.roof.cell[+el2.dataset.roofdim] = n;
        // 列/行越界了就收回最后一格
        if (mat.roof.cell[0] >= mat.roof.cell[2]) mat.roof.cell[0] = mat.roof.cell[2] - 1;
        if (mat.roof.cell[1] >= mat.roof.cell[3]) mat.roof.cell[1] = mat.roof.cell[3] - 1;
        var code = el.querySelector("[data-roofcode]");
        if (code) code.textContent = mat.roof.cell[0] + "," + mat.roof.cell[1];
        if (roofBtn) roofBtn.title = mat.roof.cell[0] + "," + mat.roof.cell[1];
        paintRoofThumb(); paintRoofPicker();
        draw();
      };
    });
    /* ── 墙面材质格（detail_texture_atlas_cell）：同屋顶选格。贴图固定走
       detail_texture（wall_atlas1），网格由 detail_cell 第 3、4 个数定义。 ── */
    var detailBox = document.getElementById("b3dDetailBox");
    var detailCv = document.getElementById("b3dDetailPick");
    function detailDims() {
      var c = mat.detail_cell || [0, 0, 8, 8];
      return [Math.max(1, c[2] | 0), Math.max(1, c[3] | 0)];
    }
    function paintDetailThumb() {
      var cnv = el.querySelector("canvas[data-detailthumb]");
      if (!cnv) return;
      var dImg2 = img(mat.detail_texture || "wall_atlas1.png");
      if (!dImg2.complete || !dImg2.naturalWidth) return;
      var c = mat.detail_cell || [0, 0, 8, 8];
      var cw = dImg2.naturalWidth / Math.max(1, c[2] | 0);
      var ch2 = dImg2.naturalHeight / Math.max(1, c[3] | 0);
      var cx = cnv.getContext("2d");
      cx.clearRect(0, 0, cnv.width, cnv.height);
      cx.drawImage(dImg2, c[0] * cw, c[1] * ch2, cw, ch2, 0, 0, cnv.width, cnv.height);
    }
    function paintDetailPicker() {
      if (!detailCv || !detailBox || detailBox.hidden) return;
      var dImg2 = img(mat.detail_texture || "wall_atlas1.png");
      if (!dImg2.complete || !dImg2.naturalWidth) return;
      var S = detailCv.width, cx = detailCv.getContext("2d");
      var d = detailDims(), c = mat.detail_cell || [0, 0, 0, 0];
      cx.imageSmoothingEnabled = false;
      cx.clearRect(0, 0, S, S);
      cx.drawImage(dImg2, 0, 0, dImg2.naturalWidth, dImg2.naturalHeight, 0, 0, S, S);
      cx.lineWidth = 1; cx.strokeStyle = "rgba(0,0,0,0.4)";
      for (var i = 1; i < d[0]; i++) { cx.beginPath(); cx.moveTo(i * S / d[0] + 0.5, 0); cx.lineTo(i * S / d[0] + 0.5, S); cx.stroke(); }
      for (var j = 1; j < d[1]; j++) { cx.beginPath(); cx.moveTo(0, j * S / d[1] + 0.5); cx.lineTo(S, j * S / d[1] + 0.5); cx.stroke(); }
      cx.lineWidth = 2; cx.strokeStyle = "#e24b4a";
      cx.strokeRect(c[0] * S / d[0] + 1, c[1] * S / d[1] + 1, S / d[0] - 2, S / d[1] - 2);
    }
    var detailBtn = el.querySelector("[data-pickdetail]");
    if (detailBtn) detailBtn.onclick = function () {
      if (!state.editable) return;
      if (pickOpen === "detail") { pickOpen = null; detailBox.hidden = true; return; }
      pickOpen = "detail"; activeUnit = null;          // 框互斥
      popOpen = null; popIdx = -1;                     // 与配方条弹出页互斥
      if (roofBox) roofBox.hidden = true;
      detailBox.hidden = false;
      paintDetailPicker();
    };
    if (detailCv) detailCv.addEventListener("click", function (ev) {
      if (!detailBox || detailBox.hidden || !state.editable) return;
      var dImg2 = img(mat.detail_texture || "wall_atlas1.png");
      if (!dImg2.complete || !dImg2.naturalWidth) return;
      var d = detailDims();
      var r = detailCv.getBoundingClientRect();
      var col = Math.min(d[0] - 1, Math.max(0, Math.floor((ev.clientX - r.left) / r.width * d[0])));
      var row = Math.min(d[1] - 1, Math.max(0, Math.floor((ev.clientY - r.top) / r.height * d[1])));
      mat.detail_cell = mat.detail_cell || [0, 0, 8, 8];
      mat.detail_cell[0] = col; mat.detail_cell[1] = row;
      var code = el.querySelector("[data-detailcode]");
      if (code) code.textContent = col + "," + row;
      if (detailBtn) detailBtn.title = col + "," + row;
      paintDetailThumb(); paintDetailPicker();
      draw();
    });
    el.querySelectorAll("input[data-detaildim]").forEach(function (el2) {
      el2.onchange = function () {
        var n = Math.max(1, Math.round(+el2.value) || 1);
        el2.value = n;
        mat.detail_cell = mat.detail_cell || [0, 0, 8, 8];
        mat.detail_cell[+el2.dataset.detaildim] = n;
        if (mat.detail_cell[0] >= mat.detail_cell[2]) mat.detail_cell[0] = mat.detail_cell[2] - 1;
        if (mat.detail_cell[1] >= mat.detail_cell[3]) mat.detail_cell[1] = mat.detail_cell[3] - 1;
        var code = el.querySelector("[data-detailcode]");
        if (code) code.textContent = mat.detail_cell[0] + "," + mat.detail_cell[1];
        if (detailBtn) detailBtn.title = mat.detail_cell[0] + "," + mat.detail_cell[1];
        paintDetailThumb(); paintDetailPicker();
        draw();
      };
    });
    /* ── 图集缩略图选择：点缩略图切图集，选中态由重建后的面板呈现 ── */
    el.querySelectorAll("[data-atlas]").forEach(function (btn) {
      btn.onclick = function () {
        if (!state.editable) return;
        if (btn.dataset.atlas === (mat.atlas_texture || DATA.default_atlas)) return;
        mat.atlas_texture = btn.dataset.atlas;
        DATA.atlas_grid = gridOf(mat.atlas_texture);   // 换图集 → 网格自动匹配
        STYLE_TEX = {};
        draw();
      };
    });
    function paintAtlasOpts() {
      el.querySelectorAll("canvas[data-atlasthumb]").forEach(function (cnv) {
        var a = cnv.dataset.atlasthumb;
        var im = img(a);
        var paint = function () {
          if (!im.naturalWidth) return;
          var g = gridOf(a), S = cnv.width, cx = cnv.getContext("2d");
          cx.imageSmoothingEnabled = false;
          cx.clearRect(0, 0, S, S);
          cx.drawImage(im, 0, 0, im.naturalWidth, im.naturalHeight, 0, 0, S, S);
          cx.lineWidth = 1; cx.strokeStyle = "rgba(0,0,0,0.35)";
          for (var i = 1; i < g[0]; i++) { cx.beginPath(); cx.moveTo(i * S / g[0] + 0.5, 0); cx.lineTo(i * S / g[0] + 0.5, S); cx.stroke(); }
          for (var j = 1; j < g[1]; j++) { cx.beginPath(); cx.moveTo(0, j * S / g[1] + 0.5); cx.lineTo(S, j * S / g[1] + 0.5); cx.stroke(); }
        };
        if (im.complete && im.naturalWidth) paint();
        else im.addEventListener("load", paint, { once: true });
      });
    }
    // 面板重建后恢复展开中的选格框/弹出页（调网格/换贴图时不再被折叠）
    if (popOpen != null) { syncSpanUI(); if (activeUnit) paintPicker(); }
    else if (pickOpen === "roof" && roofBox) { roofBox.hidden = false; paintRoofPicker(); }
    else if (pickOpen === "detail" && detailBox) { detailBox.hidden = false; paintDetailPicker(); }
    paintAtlasOpts();
    paintRoofThumb();
    paintDetailThumb();
    paintThumbs();
    paintRecipes();
  }

  fetch(DATA_URL).then(function (r) { return r.json(); }).then(function (d) {
    DATA = d;
    ui();
  }).catch(function (e) {
    holder.innerHTML = '<p class="ts-b3d__dim">' + TEXT.dataFailed + ' (' + DATA_URL + '): ' + esc(e) + '</p>';
  });
})();
