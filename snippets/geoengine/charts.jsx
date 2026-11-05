// Interactive observability charts for /geoengine/observability.
// Plain SVG drawn in the browser; the data is generated deterministically to look like real run records.
// Styles are injected once, only on pages that render one of these charts.

export const GE_CHART_CSS = ".ge-obs,.ge-tip{--ge-panel:#ffffff;--ge-panel2:#f3f0ea;--ge-line:#e0dbd1;--ge-text:#1a121c;--ge-muted:#6b6270;--ge-accent:#4d7c00;--ge-accent-ink:#ffffff;--ge-amber:#b9770e;--ge-code:#f6f3ec;--ge-s1:#2a78d6;--ge-crit:#d63c3b;--ge-good:#2f8a2f;--ge-font:\"Space Grotesk\",system-ui,-apple-system,\"Segoe UI\",sans-serif}html.dark .ge-obs,html.dark .ge-tip{--ge-panel:#1f1422;--ge-panel2:#271a2b;--ge-line:#3a2b3e;--ge-text:#ece6ee;--ge-muted:#a99fae;--ge-accent:#c5ff5a;--ge-accent-ink:#1b2400;--ge-amber:#eba941;--ge-code:#120a14;--ge-s1:#3987e5;--ge-crit:#e66767;--ge-good:#7fd17f}.ge-chart{background:var(--ge-panel);border:1px solid var(--ge-line);border-radius:14px;padding:14px 12px 8px;margin:14px 0}.ge-obs svg.viz{width:100%;height:auto;display:block}.ge-obs .vt{fill:var(--ge-muted);font:12px var(--ge-font)}.ge-obs .vt-title{fill:var(--ge-text);font-weight:600;font-size:13px}.ge-obs .vt-ax{fill:var(--ge-muted);font-size:11.5px}.ge-obs .vt-lab{fill:var(--ge-text);font-size:12px;font-weight:600}.ge-obs .vt-phase{fill:var(--ge-muted);font-size:11px;letter-spacing:.08em;text-transform:uppercase}.ge-obs .vgrid{stroke:var(--ge-line);stroke-width:1}.ge-obs .vlimit{stroke:var(--ge-muted);stroke-width:1.2;stroke-dasharray:4 3}.ge-obs .vlimit.strong{stroke:var(--ge-text);stroke-width:1.6;stroke-dasharray:none}.ge-obs .vline{fill:none;stroke:var(--ge-s1);stroke-width:2;stroke-linejoin:round}.ge-obs .vpeak{fill:var(--ge-s1);stroke:var(--ge-panel);stroke-width:2}.ge-obs .vcross{stroke:var(--ge-muted);stroke-width:1}.ge-obs .vdot{fill:var(--ge-s1);stroke:var(--ge-panel);stroke-width:2}.ge-obs .vbar{fill:var(--ge-s1)}.ge-obs .vbar.warn{fill:var(--ge-amber)}.ge-obs .vbar.crit{fill:var(--ge-crit)}.ge-obs .vtrack{fill:var(--ge-panel2);stroke:var(--ge-line)}.ge-tip{position:fixed;display:none;pointer-events:none;z-index:50;background:var(--ge-code);border:1px solid var(--ge-line);border-radius:8px;padding:7px 10px;font-size:12.5px;line-height:1.5;box-shadow:0 4px 18px rgba(0,0,0,.35)}.ge-tip b{font-weight:600}.ge-obs .hist-ctl{margin:12px 0}.ge-obs .seg{display:inline-flex;align-items:center;gap:4px;margin-right:18px;font-size:13px;color:var(--ge-muted)}.ge-obs .seg span{margin-right:6px}.ge-obs .seg button{background:var(--ge-panel);color:var(--ge-text);border:1px solid var(--ge-line);border-radius:8px;padding:5px 10px;font:600 13px var(--ge-font);cursor:pointer}.ge-obs .seg button.on{background:var(--ge-accent);color:var(--ge-accent-ink);border-color:var(--ge-accent)}.ge-obs .rng{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ge-muted)}.ge-obs .rng input{accent-color:var(--ge-accent)}.ge-obs .hist-out{font-size:14.5px}.ge-obs .stat{display:inline-block;border-radius:999px;padding:1px 10px;font-weight:600;font-size:13px;border:1px solid}.ge-obs .stat.crit{border-color:var(--ge-crit);color:var(--ge-text)}.ge-obs .stat.warn{border-color:var(--ge-amber);color:var(--ge-text)}.ge-obs .stat.ok{border-color:var(--ge-good);color:var(--ge-text)}";

export const geCharts = () => {
  if (typeof window === "undefined") return null;
  if (window.__geCharts) return window.__geCharts;
  if (!document.getElementById("ge-chart-css")) {
    const st = document.createElement("style");
    st.id = "ge-chart-css";
    st.textContent = GE_CHART_CSS;
    document.head.appendChild(st);
  }
  var NS = "http://www.w3.org/2000/svg";
    function el(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      if (parent) parent.appendChild(e);
      return e;
    }
    function txt(parent, x, y, s, cls, anchor) {
      var t = el("text", { x: x, y: y, class: cls || "vt", "text-anchor": anchor || "start" }, parent);
      t.textContent = s; return t;
    }
    var seed = 42;
    function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
    function gauss() { var u = rnd() || 1e-9, v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    var tip = document.querySelector(".ge-tip"); if (!tip) { tip = document.createElement("div"); tip.className = "ge-tip"; document.body.appendChild(tip); }
    function showTip(html, cx, cy) {
      tip.innerHTML = html; tip.style.display = "block";
      var w = tip.offsetWidth, h = tip.offsetHeight;
      var x = cx + 14, y = cy - h - 10;
      if (x + w > window.innerWidth - 8) x = cx - w - 14;
      if (y < 8) y = cy + 16;
      tip.style.left = x + "px"; tip.style.top = y + "px";
    }
    function hideTip() { tip.style.display = "none"; }
    function fmtMin(m) { var mm = Math.floor(m), ss = Math.round((m - mm) * 60); if (ss === 60) { mm++; ss = 0; } return mm + ":" + (ss < 10 ? "0" : "") + ss; }
  
    // ------------------------------------------------------------- one run
    var RUN_MIN = 42;
    var cpuMem = [], gpu = [];
    for (var t = 0; t <= RUN_MIN * 60; t += 30) {
      var m = t / 60, mem, cpu;
      if (m < 4) { mem = 2 + m * 5.2 + gauss() * 0.4; cpu = 3.6 + gauss() * 0.25; }
      else if (m < 36) {
        mem = 24 + 4 * Math.sin(m / 3) + gauss() * 0.8;
        if (m > 26.5 && m < 30) mem += 10 * Math.sin((m - 26.5) / 3.5 * Math.PI);
        cpu = 1.2 + gauss() * 0.15;
      } else { mem = 14 - (m - 36) * 1.1 + gauss() * 0.4; cpu = 2.9 + gauss() * 0.3; }
      cpuMem.push({ m: m, mem: Math.max(0.5, mem), cpu: Math.max(0.1, cpu) });
    }
    for (t = 0; t <= RUN_MIN * 60; t += 5) {
      m = t / 60; var g = 0;
      if (m >= 4 && m < 36) { g = 90 + gauss() * 3; if ((t % 120) < 15) g = 18 + gauss() * 6; }
      gpu.push({ m: m, g: Math.max(0, Math.min(100, g)) });
    }
    var peak = cpuMem.reduce(function (a, b) { return b.mem > a.mem ? b : a; });
  
  
    function fitW(host) { return Math.round(Math.max(320, Math.min(760, host.clientWidth || 760))); }

    function runChart(host) {
      var W = fitW(host), narrow = W < 560, ML = narrow ? 40 : 64, MR = narrow ? 12 : 96, PH = 92, GAP = 34, MT = 30;
      var panels = [
        { key: "mem", data: cpuMem, max: 72, ticks: [0, 32, 64], unit: "GiB", title: "Memory (GiB) · every 30 s", limit: 64, limitLabel: "class limit 64" },
        { key: "cpu", data: cpuMem, max: 9, ticks: [0, 4, 8], unit: "cores", title: "CPU (cores) · every 30 s", limit: 8, limitLabel: "class limit 8" },
        { key: "g", data: gpu, max: 100, ticks: [0, 50, 100], unit: "%", title: "GPU utilisation (%) · every 5 s", limit: null },
      ];
      var H = MT + panels.length * (PH + GAP) + 18;
      var s = el("svg", { viewBox: "0 0 " + W + " " + H, class: "viz", role: "img", "aria-label": "One run: memory, CPU and GPU utilisation over 42 minutes" }, host);
      var X = function (mm) { return ML + (mm / RUN_MIN) * (W - ML - MR); };
      var cross = [], dots = [];
      panels.forEach(function (p, i) {
        var top = MT + i * (PH + GAP) + 16;
        var Y = function (v) { return top + PH - (v / p.max) * PH; };
        p.Y = Y; p.top = top;
        txt(s, ML, top - 6, p.title, "vt vt-title");
        p.ticks.forEach(function (tv) {
          el("line", { x1: ML, x2: W - MR, y1: Y(tv), y2: Y(tv), class: "vgrid" }, s);
          txt(s, ML - 8, Y(tv) + 4, String(tv), "vt vt-ax", "end");
        });
        if (p.limit) {
          el("line", { x1: ML, x2: W - MR, y1: Y(p.limit), y2: Y(p.limit), class: "vlimit" }, s);
          if (narrow) txt(s, W - MR, Y(p.limit) - 5, p.limitLabel, "vt vt-ax", "end");
          else txt(s, W - MR + 6, Y(p.limit) + 4, p.limitLabel, "vt vt-ax");
        }
        var d = p.data.map(function (r, k) { return (k ? "L" : "M") + X(r.m).toFixed(1) + " " + Y(r[p.key]).toFixed(1); }).join("");
        el("path", { d: d, class: "vline" }, s);
        if (p.key === "mem") {
          el("circle", { cx: X(peak.m), cy: Y(peak.mem), r: 5, class: "vpeak" }, s);
          txt(s, X(peak.m) + 9, Y(peak.mem) - 6, "peak " + peak.mem.toFixed(1) + " GiB", "vt vt-lab");
        }
        if (p.key === "g") {
          if (!narrow) txt(s, W - MR, top - 6, "dips: waiting on storage reads", "vt vt-ax", "end");
        }
        cross.push(el("line", { x1: 0, x2: 0, y1: top, y2: top + PH, class: "vcross", visibility: "hidden" }, s));
        dots.push(el("circle", { cx: 0, cy: 0, r: 4.5, class: "vdot", visibility: "hidden" }, s));
      });
      (narrow ? [0, 20, 40] : [0, 10, 20, 30, 40]).forEach(function (mm) { txt(s, X(mm), H - 4, mm + " min", "vt vt-ax", "middle"); });
      // phase labels
      [[0, 4, "load"], [4, 36, "inference"], [36, 42, "write"]].forEach(function (ph) {
        el("line", { x1: X(ph[0]) + 2, x2: X(ph[1]) - 2, y1: 14, y2: 14, class: "vgrid" }, s);
        txt(s, X((ph[0] + ph[1]) / 2), 10, ph[2], "vt vt-phase", "middle");
      });
      var hit = el("rect", { x: ML, y: MT, width: W - ML - MR, height: H - MT - 18, fill: "transparent", style: "cursor:crosshair" }, s);
      function move(ev) {
        var pt = s.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
        var loc = pt.matrixTransform(s.getScreenCTM().inverse());
        var mm = Math.max(0, Math.min(RUN_MIN, (loc.x - ML) / (W - ML - MR) * RUN_MIN));
        var a = cpuMem[Math.round(mm * 2)], b = gpu[Math.round(mm * 12)];
        var vals = [a.mem, a.cpu, b.g], ms = [a.m, a.m, b.m];
        panels.forEach(function (p, i) {
          var x = X(ms[i]);
          cross[i].setAttribute("x1", x); cross[i].setAttribute("x2", x); cross[i].setAttribute("visibility", "visible");
          dots[i].setAttribute("cx", x); dots[i].setAttribute("cy", p.Y(vals[i])); dots[i].setAttribute("visibility", "visible");
        });
        showTip("<b>" + fmtMin(a.m) + "</b> into the run<br>Memory <b>" + a.mem.toFixed(1) + " GiB</b><br>CPU <b>" + a.cpu.toFixed(2) + " cores</b><br>GPU <b>" + Math.round(b.g) + "%</b>", ev.clientX, ev.clientY);
      }
      function leave() { cross.concat(dots).forEach(function (e) { e.setAttribute("visibility", "hidden"); }); hideTip(); }
      hit.addEventListener("pointermove", move); hit.addEventListener("pointerleave", leave);
    }
  
    // ------------------------------------------------------------- 200 tasks
    seed = 7;
    var peaks = [];
    for (var i = 0; i < 200; i++) peaks.push(Math.exp(Math.log(19) + gauss() * 0.11));
    peaks[17] = 41.8; peaks[88] = 44.6; peaks[150] = 39.9;
    var sorted = peaks.slice().sort(function (a, b) { return a - b; });
    function pct(p) { return sorted[Math.min(sorted.length - 1, Math.floor(p * sorted.length))]; }
  
    function histChart(host, ctl) {
      var W = fitW(host), narrow = W < 560, H = narrow ? 210 : 250, ML = narrow ? 36 : 48, MR = narrow ? 12 : 20, MT = 18, MB = 34, BIN = 2, XMAX = 66;
      var s = el("svg", { viewBox: "0 0 " + W + " " + H, class: "viz", role: "img", "aria-label": "Histogram of peak memory across 200 tasks" }, host);
      var X = function (v) { return ML + v / XMAX * (W - ML - MR); };
      var nb = Math.ceil(XMAX / BIN), bins = [];
      for (var k = 0; k < nb; k++) bins.push({ lo: k * BIN, hi: (k + 1) * BIN, n: 0, ids: [] });
      peaks.forEach(function (v, idx) { var b = bins[Math.min(nb - 1, Math.floor(v / BIN))]; b.n++; b.ids.push(idx); });
      var maxN = Math.max.apply(null, bins.map(function (b) { return b.n; }));
      var top = Math.ceil(maxN / 10) * 10;
      var Y = function (n) { return MT + (H - MT - MB) * (1 - n / top); };
      [0, top / 2, top].forEach(function (tv) {
        el("line", { x1: ML, x2: W - MR, y1: Y(tv), y2: Y(tv), class: "vgrid" }, s);
        txt(s, ML - 8, Y(tv) + 4, String(tv), "vt vt-ax", "end");
      });
      for (var v = 0; v <= 64; v += 16) txt(s, X(v), H - 12, v + " GiB", "vt vt-ax", "middle");
      txt(s, ML, MT - 4, "tasks", "vt vt-ax");
      var rects = bins.map(function (b) {
        var r = el("rect", { x: X(b.lo) + 1, y: Y(b.n), width: Math.max(0, X(b.hi) - X(b.lo) - 2), height: Math.max(0, Y(0) - Y(b.n)), rx: 2, class: "vbar" }, s);
        r.addEventListener("pointermove", function (ev) { if (b.n) showTip("<b>" + b.n + " task" + (b.n > 1 ? "s" : "") + "</b> peaked at " + b.lo + "–" + b.hi + " GiB", ev.clientX, ev.clientY); });
        r.addEventListener("pointerleave", hideTip);
        return r;
      });
      var lim = el("line", { x1: 0, x2: 0, y1: MT - 6, y2: Y(0), class: "vlimit strong" }, s);
      var limT = txt(s, 0, MT + 4, "", "vt vt-lab");
      var safe = el("line", { x1: 0, x2: 0, y1: MT + 10, y2: Y(0), class: "vlimit" }, s);
  
      var classes = [16, 32, 48, 64];
      var state = { cls: 32, head: 20 };
      var btns = ctl.querySelectorAll("[data-cls]"), slider = ctl.querySelector("[data-ge=headroom]"), out = ctl.querySelector("[data-ge=out]"), hv = ctl.querySelector("[data-ge=headval]");
      function render() {
        var c = state.cls, h = state.head / 100, safeLine = c / (1 + h);
        var oom = peaks.filter(function (p) { return p > c; }).length;
        var risk = peaks.filter(function (p) { return p > safeLine && p <= c; }).length;
        bins.forEach(function (b, k) {
          var mid = (b.lo + b.hi) / 2;
          rects[k].setAttribute("class", "vbar" + (mid > c ? " crit" : mid > safeLine ? " warn" : ""));
        });
        lim.setAttribute("x1", X(c)); lim.setAttribute("x2", X(c));
        safe.setAttribute("x1", X(safeLine)); safe.setAttribute("x2", X(safeLine));
        limT.setAttribute("x", X(c) + 6); limT.textContent = c + " GiB class";
        if (X(c) + 90 > W) { limT.setAttribute("x", X(c) - 6); limT.setAttribute("text-anchor", "end"); } else limT.setAttribute("text-anchor", "start");
        hv.textContent = state.head + "%";
        btns.forEach(function (b) { b.classList.toggle("on", +b.dataset.cls === c); });
        var rec = classes.filter(function (k) { return sorted[sorted.length - 1] * (1 + h) <= k; })[0];
        var p95 = pct(0.95);
        out.innerHTML =
          (oom ? '<span class="stat crit">✕ ' + oom + ' of 200 tasks would be OOM-killed</span>' : '<span class="stat ok">✓ no task exceeds the class</span>') +
          (risk ? ' <span class="stat warn">! ' + risk + ' inside the headroom band</span>' : "") +
          '<br>p95 peak <b>' + p95.toFixed(1) + ' GiB</b> · largest <b>' + sorted[sorted.length - 1].toFixed(1) + ' GiB</b> · recommended class with ' + state.head + '% headroom: <b>' + (rec ? rec + " GiB" : "split the largest inputs") + '</b>';
      }
      btns.forEach(function (b) { b.addEventListener("click", function () { state.cls = +b.dataset.cls; render(); }); });
      slider.addEventListener("input", function () { state.head = +slider.value; render(); });
      render();
    }
  
    // ------------------------------------------------------------- requested vs used
    function bulletChart(host) {
      var rows = [
        { w: "land-cover-classify 2.0.0", req: 64, used: +peak.mem.toFixed(1), cls: "gpu" },
        { w: "cloud-removal-ndvi 2.3.1", req: 64, used: +pct(0.95).toFixed(1), cls: "highmem" },
        { w: "building-change-detect 3.0.2", req: 32, used: 14.2, cls: "gpu" },
        { w: "sar-flood-extent 1.4.0", req: 16, used: 5.1, cls: "cpu" },
        { w: "resample-cog 1.1.0", req: 8, used: 2.2, cls: "cpu" },
        { w: "grid-creator 1.0.0", req: 4, used: 0.6, cls: "cpu" },
      ];
      var W = fitW(host), narrow = W < 560, ML = narrow ? 12 : 210, MR = narrow ? 70 : 110, RH = narrow ? 50 : 34, MT = 10;
      var H = MT + rows.length * RH + 26;
      var s = el("svg", { viewBox: "0 0 " + W + " " + H, class: "viz", role: "img", "aria-label": "Requested memory versus p95 peak memory per worker" }, host);
      var X = function (v) { return ML + v / 64 * (W - ML - MR); };
      [0, 16, 32, 48, 64].forEach(function (v) {
        el("line", { x1: X(v), x2: X(v), y1: MT, y2: H - 22, class: "vgrid" }, s);
        txt(s, X(v), H - 6, v + " GiB", "vt vt-ax", narrow && v === 0 ? "start" : "middle");
      });
      rows.forEach(function (r, i) {
        var y = MT + i * RH + (narrow ? 20 : 6);
        if (narrow) txt(s, ML, y - 6, r.w, "vt");
        else txt(s, ML - 12, y + 15, r.w, "vt", "end");
        el("rect", { x: X(0), y: y, width: X(r.req) - X(0), height: 22, rx: 4, class: "vtrack" }, s);
        var b = el("rect", { x: X(0), y: y + 5, width: Math.max(3, X(r.used) - X(0)), height: 12, rx: 3, class: "vbar" }, s);
        var idle = Math.round((1 - r.used / r.req) * 100);
        txt(s, X(r.req) + 8, y + 15, idle + "% idle", "vt vt-lab");
        var hit = el("rect", { x: X(0), y: y - (narrow ? 20 : 4), width: W - ML, height: RH, fill: "transparent" }, s);
        hit.addEventListener("pointermove", function (ev) { showTip("<b>" + r.w + "</b><br>Requested <b>" + r.req + " GiB</b> (" + r.cls + ")<br>p95 peak <b>" + r.used + " GiB</b><br>Reserved but unused <b>" + idle + "%</b>", ev.clientX, ev.clientY); });
        hit.addEventListener("pointerleave", hideTip);
      });
    }
  
  
  window.__geCharts = { runChart: runChart, histChart: histChart, bulletChart: bulletChart };
  return window.__geCharts;
};

export const GeRunChart = () => {
  const ref = useRef(null);
  useEffect(() => { const c = geCharts(); if (!c || !ref.current) return; ref.current.innerHTML = ""; c.runChart(ref.current); }, []);
  return <div className="ge-obs"><div className="ge-chart"><div ref={ref} /></div></div>;
};

export const GeBatchChart = () => {
  const ref = useRef(null);
  const ctl = useRef(null);
  useEffect(() => { const c = geCharts(); if (!c || !ref.current) return; ref.current.innerHTML = ""; c.histChart(ref.current, ctl.current); }, []);
  return (
    <div className="ge-obs"><div className="hist-ctl" ref={ctl}>
      <div className="seg"><span>Class</span>
        <button type="button" data-cls="16">16 GiB</button><button type="button" data-cls="32">32 GiB</button>
        <button type="button" data-cls="48">48 GiB</button><button type="button" data-cls="64">64 GiB</button>
      </div>
      <label className="rng">Headroom <input data-ge="headroom" type="range" min="0" max="40" step="5" defaultValue="20" /> <b data-ge="headval">20%</b></label>
      <div className="ge-chart"><div ref={ref} /></div>
      <p className="hist-out" data-ge="out"></p>
    </div></div>
  );
};

export const GeReservedChart = () => {
  const ref = useRef(null);
  useEffect(() => { const c = geCharts(); if (!c || !ref.current) return; ref.current.innerHTML = ""; c.bulletChart(ref.current); }, []);
  return <div className="ge-obs"><div className="ge-chart"><div ref={ref} /></div></div>;
};
