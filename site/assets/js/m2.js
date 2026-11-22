/* Free AI – דף בית 2: האנימציות של דף הבית של Mintlify (סרט חוטים, מונים, פס מספרים, קרוסלות, נקודות). */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DPR = Math.min(window.devicePixelRatio || 1, 2);
  /* ---------- סרט חוטים (כמו בפתיחה של Mintlify): 24 חוטים, סיבוב, הבזקי צבע ---------- */
  var RIB = {
    hero: { W: 1720, H: 1080, count: 24, res: 81, spacing: 4.9, amp: 163, freq: .75, phase: .14, twist: .41, bulge: .66, morph: .5,
      speed: .66, from: '#18e299', to: '#baff24', pColors: ['#d87cff', '#ffa723', '#44aeff', '#ffa3d3'], pSize: 3, pLen: 88,
      pSpeed: .84, pSparse: .32, seed: 2025, rotate: -28, edge: .25 }
  };
  RIB.wave = Object.assign({}, RIB.hero, { pSpeed: 1.15, rotate: 0 });
  function hx(c) { return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]; }
  function hash(a, b, c) {
    var r = (Math.imul(a, 0x165667b1) + Math.imul(b, 0x27d4eb2f) + Math.imul(c, 0x3a8f05c5)) | 0;
    r = Math.imul(r ^ (r >>> 13), 0x4bf19f61); r ^= r >>> 16;
    return ((r >>> 0) % 1e5) / 1e5;
  }
  function ribPoints(g, e, T) {
    var pts = [], n = g.res - 1, ang = g.rotate * Math.PI / 180, co = Math.cos(ang), si = Math.sin(ang);
    var cx = g.W / 2, cy = g.H / 2, ph = g.phase * (e - (g.count - 1) / 2), om = g.freq * Math.PI * 2, spin = .7 * T;
    var off = (e / (g.count - 1) - .5) * g.count * g.spacing;
    for (var j = 0; j <= n; j++) {
      var t = j / n, bul = 1 + g.bulge * Math.sin(t * Math.PI);
      var a = Math.sin(om * t + ph), b = Math.sin(.5 * om * t - 2 * ph + spin);
      var m = Math.sin(3.7 * t + .2 * e) * Math.cos(2.1 * t + .13 * e);
      var x = t * g.W, y = cy + off + (a + g.twist * b + g.morph * m) * .5 * bul * g.amp;
      var dx = x - cx, dy = y - cy;
      pts.push([cx + dx * co - dy * si, cy + dx * si + dy * co]);
    }
    return pts;
  }
  function drawRibbon(it, time) {
    var c = it.ctx, g = it.g, w = it.w, h = it.h;
    var T = reduce ? 0 : time / 1000 * g.speed, intro = reduce ? 1 : Math.min(time / 1500, 1);
    c.setTransform(DPR, 0, 0, DPR, 0, 0); c.clearRect(0, 0, w, h);
    if (it.flip) { c.translate(w, 0); c.scale(-1, 1); }
    var s = Math.max(w / g.W, h / g.H); c.translate((w - g.W * s) / 2, (h - g.H * s) / 2); c.scale(s, s);
    c.lineJoin = 'round'; c.lineCap = 'round'; c.lineWidth = 1;
    var A = hx(g.from), B = hx(g.to), lines = [];
    for (var e = 0; e < g.count; e++) {
      var P = ribPoints(g, e, T); lines.push(P);
      var k = e / (g.count - 1), col = [0, 1, 2].map(function (q) { return Math.round(A[q] + (B[q] - A[q]) * k); }).join(',');
      var f = P[0], l = P[P.length - 1], gr = c.createLinearGradient(f[0], f[1], l[0], l[1]);
      gr.addColorStop(0, 'rgba(' + col + ',0)'); gr.addColorStop(g.edge, 'rgba(' + col + ',1)');
      gr.addColorStop(1 - g.edge, 'rgba(' + col + ',1)'); gr.addColorStop(1, 'rgba(' + col + ',0)');
      c.strokeStyle = gr;
      if (intro < 1) {
        var r = Math.min(intro / (.6 + .4 * hash(e, 53, g.seed)), 1), sm = r * r * (3 - 2 * r);
        if (sm <= 0) continue;
        var len = 0; for (var q = 1; q < P.length; q++) len += Math.hypot(P[q][0] - P[q - 1][0], P[q][1] - P[q - 1][1]);
        c.setLineDash([len * sm, len + 1]);
      } else c.setLineDash([]);
      c.beginPath(); c.moveTo(f[0], f[1]);
      for (var j = 1; j < P.length - 1; j++) c.quadraticCurveTo(P[j][0], P[j][1], (P[j][0] + P[j + 1][0]) / 2, (P[j][1] + P[j + 1][1]) / 2);
      c.lineTo(l[0], l[1]); c.stroke();
    }
    c.setLineDash([]);
    if (!reduce && intro >= 1) {
      var life = Math.max(.8, 3.4 / Math.max(.15, g.pSpeed)), cyc = life + 2.2;
      c.lineWidth = g.pSize;
      for (var e2 = 0; e2 < g.count; e2++) {
        if (hash(e2, 7, g.seed) > g.pSparse) continue;
        var o = (T + .18 * e2 - 1.8 * hash(e2, 3, g.seed)) % cyc; if (o < 0) o += cyc;
        if (o > life) continue;
        var u = o / life, fade = u < .18 ? u / .18 : u > .68 ? (1 - u) / .32 : 1;
        var pt = along(lines[e2], u), colr = g.pColors[Math.floor(hash(e2, 11, g.seed) * g.pColors.length) % g.pColors.length];
        var d = Math.hypot(pt[2], pt[3]) || 1, vx = pt[2] / d, vy = pt[3] / d, half = g.pLen / 2;
        var x1 = pt[0] - vx * half, y1 = pt[1] - vy * half, x2 = pt[0] + vx * half, y2 = pt[1] + vy * half;
        var pc = hx(colr), pg = c.createLinearGradient(x1, y1, x2, y2);
        pg.addColorStop(0, 'rgba(' + pc + ',0)'); pg.addColorStop(1, 'rgba(' + pc + ',1)');
        c.strokeStyle = pg; c.globalAlpha = fade;
        c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
      }
      c.globalAlpha = 1;
    }
    c.setTransform(1, 0, 0, 1, 0, 0);
  }
  function along(P, u) {
    var segs = [], tot = 0;
    for (var i = 1; i < P.length; i++) { var d = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); segs.push(d); tot += d; }
    var target = u * tot, acc = 0;
    for (var j = 0; j < segs.length; j++) {
      if (acc + segs[j] >= target) { var a = P[j], b = P[j + 1], f = segs[j] ? (target - acc) / segs[j] : 0; return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, b[0] - a[0], b[1] - a[1]]; }
      acc += segs[j];
    }
    var z = P[P.length - 1]; return [z[0], z[1], 0, 0];
  }


  /* ---------- קנבסים של סרט חוטים ---------- */
  function initRibbons() {
    document.querySelectorAll('canvas[data-rib]').forEach(function (cv) {
      var it = { cv: cv, ctx: cv.getContext('2d'), g: RIB[cv.dataset.rib], flip: cv.dataset.flip === '1', w: 1, h: 1, t0: 0, last: 0, on: false };
      if (!it.g) return;
      function size() {
        var r = cv.getBoundingClientRect();
        it.w = Math.max(1, r.width); it.h = Math.max(1, r.height);
        cv.width = Math.round(it.w * DPR); cv.height = Math.round(it.h * DPR);
        drawRibbon(it, reduce ? 0 : it.last);
      }
      size();
      if ('ResizeObserver' in window) new ResizeObserver(size).observe(cv);
      if (reduce) return;
      function loop(now) {
        if (!it.on) return;
        if (!it.t0) it.t0 = now - it.last;
        it.last = now - it.t0; drawRibbon(it, it.last);
        requestAnimationFrame(loop);
      }
      new IntersectionObserver(function (es) {
        var vis = es[0].isIntersecting;
        if (vis && !it.on) { it.on = true; it.t0 = 0; requestAnimationFrame(loop); }
        if (!vis) it.on = false;
      }, { rootMargin: '10% 0px' }).observe(cv);
    });
  }

  /* ---------- מונים שמתגלגלים ---------- */
  function initRollers() {
    var els = document.querySelectorAll('[data-roller]');
    els.forEach(function (el) {
      var cols = el.querySelectorAll('[data-to]');
      if (reduce) return;
      cols.forEach(function (c) { c.style.transform = 'translateY(0) translateZ(0)'; });
      var io = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return;
        io.disconnect();
        cols.forEach(function (c, i) {
          setTimeout(function () { c.style.transform = 'translateY(-' + c.dataset.to + 'em) translateZ(0)'; }, 120 + i * 90);
        });
      }, { threshold: .5 });
      io.observe(el);
    });
  }

  /* ---------- פס מספרים שרץ ---------- */
  function initTicker() {
    document.querySelectorAll('[data-ticker]').forEach(function (view) {
      var track = view.querySelector('.tk-track'), x = 0, paused = false, last = 0;
      if (reduce || !track) return;
      var rtl = getComputedStyle(view).direction === 'rtl';
      ['mouseenter', 'focusin'].forEach(function (e) { view.addEventListener(e, function () { paused = true; }); });
      ['mouseleave', 'focusout'].forEach(function (e) { view.addEventListener(e, function () { paused = false; }); });
      function step(t) {
        var dt = last ? Math.min(t - last, 50) : 16; last = t;
        if (!paused) {
          var w = track.firstElementChild.offsetWidth;
          x = (x + dt * .035) % w;  /* זז משמאל לימין */
          track.style.transform = 'translate3d(' + (rtl ? x : x - w) + 'px,0,0)';
        }
        requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }


  /* ---------- רעש חלק (לבחירת איפה יש נקודות) ---------- */
  function h2(a, b) { var n = Math.imul(a, 0x165667b1) + Math.imul(b, 0x27d4eb2f); n = Math.imul(n ^ (n >>> 13), 0x4bf19f61); n ^= n >>> 16; return (n >>> 0) / 0xffffffff; }
  function sstep(x) { return x * x * (3 - 2 * x); }
  function noise(x, y) {
    var X = Math.floor(x), Y = Math.floor(y), u = sstep(x - X), v = sstep(y - Y);
    var a = h2(X, Y), b = h2(X + 1, Y), c = h2(X, Y + 1), d = h2(X + 1, Y + 1), top = a + (b - a) * u;
    return top + (c + (d - c) * u - top) * v;
  }
  function field(x, y, sc) { var fx = x / sc, fy = y / sc; return .65 * noise(fx, fy) + .35 * noise(2.3 * fx + 11.7, 2.3 * fy + 5.1); }

  /* ---------- נקודות לבנות על כרטיס צבעוני ---------- */
  function initCardDots() {
    document.querySelectorAll('canvas[data-carddots]').forEach(function (cv) {
      var par = cv.parentElement, ctx = cv.getContext('2d');
      function draw() {
        var w = par.clientWidth, h = par.clientHeight, r = window.devicePixelRatio || 1;
        if (!w || !h) return;
        cv.style.width = w + 'px'; cv.style.height = h + 'px'; cv.width = w * r; cv.height = h * r;
        ctx.setTransform(r, 0, 0, r, 0, 0); ctx.clearRect(0, 0, w, h); ctx.fillStyle = '#ffffff';
        for (var x = 8; x < w; x += 16) for (var y = 8; y < h; y += 16) {
          if (field(x, y, 110) < .62) continue;
          ctx.globalAlpha = h2(Math.round(x), Math.round(y)) < .1 ? .3 : .18; ctx.fillRect(x - 1, y - 1, 2, 2);
        }
        ctx.globalAlpha = 1;
      }
      draw(); if ('ResizeObserver' in window) new ResizeObserver(draw).observe(par);
    });
  }

  /* ---------- שדה נקודות ברוחב כל המסך: מהבהבות בירוק, נדלקות ליד העכבר, גל בלחיצה ---------- */
  function initSectionDots() {
    document.querySelectorAll('canvas[data-sectiondots]').forEach(function (cv) {
      var par = cv.parentElement, ctx = cv.getContext('2d'), r = window.devicePixelRatio || 1;
      var clip = cv.hasAttribute('data-clip'), feather = +(cv.dataset.feather || .2);
      var W = 0, H = 0, dots = [], trail = [], raf = 0, vis = false, lastSample = 0;
      var G0 = [12, 140, 94], G1 = [115, 158, 22], BASE = .12;
      var occ = function () { return [].slice.call(par.querySelectorAll('[data-occlude]')); };
      function fadeY(y) { var t = Math.min(feather * innerHeight, H / 2); return t <= 0 ? 1 : Math.max(0, Math.min(1, y / t, (H - y) / t)); }
      function fadeX(x) { var t = Math.min(feather * innerWidth, W / 2); return t <= 0 ? 1 : Math.max(0, Math.min(1, x / t, (W - x) / t)); }
      function inner() { var a = cv.getBoundingClientRect(), b = par.getBoundingClientRect(); return [b.left - a.left, b.right - a.left]; }
      function setup() {
        var b = par.getBoundingClientRect(); W = innerWidth; H = par.clientHeight;
        if (W <= 0 || H <= 0) return;
        cv.style.left = (-b.left) + 'px'; cv.style.top = '0px'; cv.style.width = W + 'px'; cv.style.height = H + 'px';
        cv.width = W * r; cv.height = H * r; ctx.setTransform(r, 0, 0, r, 0, 0);
        var now = performance.now(), sc = clip ? 70 : 110, th = clip ? .62 : .54; dots = [];
        for (var x = 7; x < W; x += 14) for (var y = 7; y < H; y += 14) {
          if (field(clip ? Math.min(x, W - x) : x, y, sc) < th) continue;
          dots.push({ x: x, y: y, g: Math.random() < .1, next: now + Math.random() * 6000, pulses: [] });
        }
        draw(now);
      }
      function draw(now) {
        ctx.clearRect(0, 0, W, H);
        trail = trail.filter(function (p) { return now - p.t <= 600; });
        var cr = cv.getBoundingClientRect();
        var rects = occ().map(function (e) { var q = e.getBoundingClientRect(); return [q.left - cr.left, q.top - cr.top, q.right - cr.left, q.bottom - cr.top]; });
        var lr = clip ? inner() : null;
        for (var i = 0; i < dots.length; i++) {
          var d = dots[i], ex;
          if (clip) { if (d.x >= lr[0] && d.x <= lr[1]) continue; ex = sstep(Math.max(0, Math.min(1, (d.x < lr[0] ? lr[0] - d.x : d.x - lr[1]) / 72))); }
          else ex = fadeX(d.x);
          var a = fadeY(d.y) * ex; if (a <= 0) continue;
          var hid = false; for (var k = 0; k < rects.length; k++) { var q = rects[k]; if (d.x >= q[0] && d.x <= q[2] && d.y >= q[1] && d.y <= q[3]) { hid = true; break; } }
          if (hid) continue;
          var pul = d.pulses.some(function (w) { return now >= w[0] && now <= w[1]; }), hov = 0;
          for (var t = 0; t < trail.length; t++) { var dd = Math.hypot(d.x - trail[t].x, d.y - trail[t].y); if (dd < 42) hov = Math.max(hov, sstep(1 - dd / 42)); }
          var c = Math.max(d.g ? 1 : 0, pul ? 1 : 0, hov), f = Math.max(0, Math.min(1, d.x / W));
          var gc = [G0[0] + (G1[0] - G0[0]) * f, G0[1] + (G1[1] - G0[1]) * f, G0[2] + (G1[2] - G0[2]) * f];
          ctx.fillStyle = 'rgb(' + Math.round(gc[0] * c) + ',' + Math.round(gc[1] * c) + ',' + Math.round(gc[2] * c) + ')';
          ctx.globalAlpha = (BASE + (.85 - BASE) * c) * a; ctx.fillRect(d.x - 1, d.y - 1, 2, 2);
        }
        ctx.globalAlpha = 1;
      }
      function tick(now) {
        for (var i = 0; i < dots.length; i++) {
          var d = dots[i]; d.pulses = d.pulses.filter(function (w) { return w[1] >= now; });
          if (now >= d.next) { d.g = Math.random() < .1; d.next = now + 2200 + Math.random() * 3800; }
        }
        draw(now); raf = requestAnimationFrame(tick);
      }
      function local(e) { var q = cv.getBoundingClientRect(); return { x: e.clientX - q.left, y: e.clientY - q.top }; }
      setup();
      if ('ResizeObserver' in window) new ResizeObserver(setup).observe(par);
      addEventListener('resize', setup);
      if (reduce) return;
      new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(tick); if (!vis && raf) { cancelAnimationFrame(raf); raf = 0; } }, { rootMargin: '20% 0px' }).observe(cv);
      addEventListener('pointermove', function (e) {
        if (!vis) return; var p = local(e), t = performance.now();
        if (p.x < -42 || p.x > W + 42 || p.y < -42 || p.y > H + 42) return;
        if (t - lastSample >= 16 || !trail.length) { trail.push({ x: p.x, y: p.y, t: t }); if (trail.length > 60) trail.shift(); lastSample = t; }
        else trail[trail.length - 1] = { x: p.x, y: p.y, t: t };
      }, { passive: true });
      addEventListener('click', function (e) {
        if (!vis || (e.target.closest && e.target.closest('a,button,input,select,textarea,label,[role="button"]'))) return;
        var p = local(e), t = performance.now();
        if (p.x < 0 || p.x > W || p.y < 0 || p.y > H) return;
        if (clip) { var lr = inner(); if (p.x >= lr[0] && p.x <= lr[1]) return; }
        dots.forEach(function (d) { var s0 = t + Math.hypot(d.x - p.x, d.y - p.y) * 1.4; d.pulses.push([s0, s0 + 160]); if (d.pulses.length > 8) d.pulses.shift(); });
      });
    });
  }

  /* ---------- קרוסלות: חיצים ---------- */
  function initCarousels() {
    document.querySelectorAll('[data-track]').forEach(function (track) {
      var sec = track.closest('section'), btns = sec.querySelectorAll('[data-car]');
      function card() { var c = track.firstElementChild; return c ? c.getBoundingClientRect().width + 16 : 400; }
      function edges() {
        var max = track.scrollWidth - track.clientWidth, x = Math.abs(track.scrollLeft);
        btns.forEach(function (b) { b.disabled = b.dataset.car === '-1' ? x < 4 : x > max - 4; });
      }
      btns.forEach(function (b) { b.addEventListener('click', function () { track.scrollBy({ left: (getComputedStyle(track).direction === 'rtl' ? -1 : 1) * (+b.dataset.car) * card(), behavior: reduce ? 'auto' : 'smooth' }); }); });
      track.addEventListener('scroll', edges, { passive: true }); edges();
      var dims = track.querySelectorAll('.carousel-card-dim');
      if (dims.length && 'IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('is-on', e.intersectionRatio > .7); }); }, { root: track, threshold: [0, .7, 1] });
        dims.forEach(function (d) { io.observe(d); });
      } else dims.forEach(function (d) { d.classList.add('is-on'); });
    });
  }

  /* ---------- קווי זרימה בפס הסיום: נושמים, ושביטים צבעוניים רצים עליהם ---------- */
  function initFlow() {
    var svg = document.querySelector('svg[data-flow]');
    if (!svg) return;
    var NS = 'http://www.w3.org/2000/svg', groups = svg.querySelectorAll(':scope > g');
    var tails = groups[0] ? groups[0].querySelectorAll('path') : [], band = groups[1];
    var wires = band ? [].slice.call(band.querySelectorAll(':scope > path')) : [];
    var comets = band ? [].slice.call(band.querySelectorAll(':scope > g')) : [];
    var grads = svg.querySelectorAll('linearGradient'), maskRect = svg.querySelector('mask rect:last-child');
    var COLORS = ['#ffa723', '#d87cff', '#44aeff', '#ffa3d3'], C = { streak: 32, durMin: 1000, durMax: 2000, gapMin: 900, gapMax: 3200, yEnter: 200, yExit: 880 };
    var sec = svg.closest('section'), bounds = sec.querySelector(':scope > .grid-layout') || sec;
    var VW = 848, VH = 868;
    function fitBand() {
      var r = svg.getBoundingClientRect(); if (!r.width) return;
      var o = bounds.getBoundingClientRect(), flip = getComputedStyle(svg).transform !== 'none';
      var ax = function (x) { var v = (x - r.left) / r.width * VW; return Math.max(0, Math.min(VW, flip ? VW - v : v)); };
      var l = ax(o.left), rr = ax(o.right), top = Math.max(0, Math.min(VH, (sec.getBoundingClientRect().top - r.top) / r.height * VH));
      maskRect.setAttribute('x', Math.min(l, rr)); maskRect.setAttribute('width', Math.abs(rr - l)); maskRect.setAttribute('y', top); maskRect.setAttribute('height', VH - top);
    }
    fitBand(); if ('ResizeObserver' in window) new ResizeObserver(fitBand).observe(svg); addEventListener('resize', fitBand);
    if (reduce) { wires.forEach(function (w) { w.style.opacity = .82; }); return; }
    var pts = wires.map(function (w) { var L = w.getTotalLength(), a = []; for (var i = 0; i < 64; i++) { var q = w.getPointAtLength(L * i / 63); a.push({ x: q.x, y: q.y }); } return a; });
    var ranges = pts.map(function (a) { var en = -1, ex = -1; for (var i = 0; i < a.length; i++) { if (a[i].y >= C.yEnter && en < 0) en = i; if (a[i].y <= C.yExit) ex = i; } return en < 0 || ex <= en ? null : [en, ex]; });
    var ok = ranges.map(function (r, i) { return r ? i : -1; }).filter(function (i) { return i >= 0; });
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function ease(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
    var cs = comets.map(function (g, n) { return { g: g, wire: ok[n % ok.length], color: n % 4, begin: 0, dur: rnd(C.durMin, C.durMax) }; });
    var t0 = 0, on = false;
    function frame(now) {
      if (!on) return;
      if (!t0) { t0 = now; cs.forEach(function (c, n) { c.begin = now - c.dur * ((n + .5) / cs.length); }); }
      var ph = (now - t0) / 5200;
      wires.forEach(function (w, e) { var k = (Math.sin((ph + e * .085) * 2 * Math.PI - Math.PI / 2) + 1) / 2; w.style.opacity = .8 + .2 * k; });
      var busy = {}; cs.forEach(function (c) { var t = (now - c.begin) / c.dur; if (t >= 0 && t < 1) busy[c.wire] = 1; });
      cs.forEach(function (c, n) {
        var t = (now - c.begin) / c.dur, rg = ranges[c.wire];
        if (t < 0 || t >= 1 || !rg) {
          if (t >= 1) {
            delete busy[c.wire];
            var free = ok.filter(function (i) { return !busy[i]; }); var pool = free.length ? free : ok;
            c.wire = pool[Math.floor(Math.random() * pool.length)]; busy[c.wire] = 1;
            c.color = Math.floor(Math.random() * 4); c.dur = rnd(C.durMin, C.durMax); c.begin = now + rnd(C.gapMin, C.gapMax);
          }
          c.g.style.opacity = 0; return;
        }
        var P = pts[c.wire], f = rg[0] + (rg[1] - rg[0]) * ease(t), i0 = Math.floor(f), i1 = Math.min(P.length - 1, i0 + 1), fr = f - i0;
        var x = P[i0].x + (P[i1].x - P[i0].x) * fr, y = P[i0].y + (P[i1].y - P[i0].y) * fr, seg = [{ x: x, y: y }], left = C.streak, px = x, py = y;
        for (var j = i0; j >= 0 && left > 0; j--) {
          var d = Math.hypot(px - P[j].x, py - P[j].y);
          if (d >= left) { var u = left / (d || 1); seg.push({ x: px + (P[j].x - px) * u, y: py + (P[j].y - py) * u }); left = 0; }
          else if (d > 0) { seg.push({ x: P[j].x, y: P[j].y }); left -= d; px = P[j].x; py = P[j].y; }
        }
        c.g.firstElementChild.setAttribute('d', seg.map(function (q, k) { return (k ? 'L' : 'M') + q.x.toFixed(1) + ' ' + q.y.toFixed(1); }).join(''));
        var gr = grads[n]; if (gr) { var z = seg[seg.length - 1]; gr.setAttribute('x1', seg[0].x.toFixed(1)); gr.setAttribute('y1', seg[0].y.toFixed(1)); gr.setAttribute('x2', z.x.toFixed(1)); gr.setAttribute('y2', z.y.toFixed(1)); [].forEach.call(gr.children, function (st) { st.setAttribute('stop-color', COLORS[c.color]); }); }
        c.g.style.opacity = Math.min(1, t / .18) * Math.min(1, (1 - t) / .22);
      });
      requestAnimationFrame(frame);
    }
    new IntersectionObserver(function (es) { var v = es[0].isIntersecting; if (v && !on) { on = true; requestAnimationFrame(frame); } if (!v) on = false; }, { rootMargin: '15% 0px' }).observe(svg);
  }

  /* ---------- בקשות לדוגמה: מתחלפות אחת אחת, עם כפתור עצירה ---------- */
  function initRotate() {
    var grid = document.querySelector('[data-rotate]'); if (!grid) return;
    var figs = [].slice.call(grid.querySelectorAll('figure')), pool = JSON.parse(grid.querySelector('[data-pool]').textContent);
    var btn = document.querySelector('[data-pause]'), paused = reduce, shown = figs.map(function (f, i) { return i; }), next = figs.length, slot = 0;
    figs.forEach(function (f) { f.style.transition = 'opacity .45s cubic-bezier(.4,0,.2,1)'; });
    if (btn) btn.addEventListener('click', function () { paused = !paused; btn.textContent = paused ? 'הפעלת הדוגמאות' : 'עצירת הדוגמאות'; btn.setAttribute('aria-pressed', paused); });
    if (reduce && btn) btn.hidden = true;
    setInterval(function () {
      if (paused || document.hidden) return;
      var f = figs[slot], item = pool[next % pool.length];
      f.style.opacity = 0;
      setTimeout(function () {
        f.querySelector('.size-12').innerHTML = item[0]; f.querySelector('figcaption').textContent = item[1];
        f.querySelector('figcaption').nextElementSibling.textContent = item[2]; f.querySelector('blockquote').textContent = item[3];
        f.style.opacity = 1;
      }, 450);
      next++; slot = (slot + 1) % figs.length;
    }, 3200);
  }

  /* ---------- שאלות נפוצות: פתיחה וסגירה ---------- */
  function initFaq() {
    document.querySelectorAll('[data-faq]').forEach(function (b) {
      b.addEventListener('click', function () {
        var open = b.getAttribute('aria-expanded') !== 'true', item = b.closest('[data-slot="accordion-item"]');
        var panel = document.getElementById(b.getAttribute('aria-controls'));
        b.setAttribute('aria-expanded', open);
        [item, b, b.parentElement, panel].forEach(function (el) { el.setAttribute('data-state', open ? 'open' : 'closed'); });
      });
    });
  }

  /* ---------- תפריט בטלפון ---------- */
  function initMenu() {
    var b = document.querySelector('[data-menu]'), m = document.getElementById('m-menu'); if (!b || !m) return;
    function set(o) { b.setAttribute('aria-expanded', o); m.hidden = !o; }
    b.addEventListener('click', function () { set(b.getAttribute('aria-expanded') !== 'true'); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  }

  /* ---------- כרטיסי Rive: נטענים כשמתקרבים, ומקבלים ריחוף ---------- */
  function initRive() {
    var cvs = [].slice.call(document.querySelectorAll('canvas[data-rive]'));
    if (!cvs.length) return;
    var loading = false;
    function boot() {
      if (loading) return; loading = true;
      var sc = document.createElement('script'); sc.src = 'assets/rive/rive.js'; sc.onload = function () {
        rive.RuntimeLoader.setWasmUrl('assets/rive/rive.wasm');
        var mobile = matchMedia('(max-width: 767px)').matches;
        cvs.forEach(function (cv) {
          var src = mobile && cv.dataset.riveM ? cv.dataset.riveM : cv.dataset.rive, hov = null, want = false;
          var r = new rive.Rive({ src: src, canvas: cv, stateMachines: 'State Machine 1', autoplay: !reduce, autoBind: true, shouldDisableRiveListeners: true,
            layout: new rive.Layout({ fit: rive.Fit.Cover, alignment: rive.Alignment.Center }),
            onLoad: function () {
              r.resizeDrawingSurfaceToCanvas(); cv._rive = r; cv.dispatchEvent(new Event('riveload'));
              var vm = r.viewModelInstance;
              if (vm) { var d = vm.boolean('darkMode'); if (d) d.value = false; hov = vm.boolean('ishover'); if (hov) hov.value = want; }
              if (reduce) { r.play(); setTimeout(function () { r.pause(); }, 600); }
            } });
          var card = cv.closest('.group') || cv.parentElement;
          if (!cv.dataset.nohover) card.addEventListener('mouseenter', function () { want = true; if (hov) hov.value = true; });
          card.addEventListener('mouseleave', function () { want = false; if (hov) hov.value = false; });
          if ('ResizeObserver' in window) new ResizeObserver(function () { r.resizeDrawingSurfaceToCanvas(); }).observe(cv);
          new IntersectionObserver(function (es) { if (reduce) return; es[0].isIntersecting ? r.startRendering() : r.stopRendering(); }).observe(cv);
        });
      };
      document.head.appendChild(sc);
    }
    var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); boot(); } }, { rootMargin: '600px 0px' });
    cvs.forEach(function (c) { io.observe(c); });
  }

  /* ---------- "מתחברים לשירותים": האייקונים של 4CODE ו-GitHub מעל הריבועים שבאנימציה ---------- */
  function initConnectIcons() {
    var cv = document.querySelector('canvas[data-rive*="connect-with-your-systems"]'); if (!cv) return;
    cv.dataset.nohover = '1';
    var box = cv.parentElement, AW = 344, AH = 414, tiles = [[172, 207, 'assets/images/brands/4code-mark.png'], [239.5, 207, 'assets/images/brands/github-mark.svg']], els = [];
    tiles.forEach(function (t) { var d = document.createElement('span'); d.className = 'cn-tile'; d.innerHTML = '<img src="' + t[2] + '" alt="">'; box.appendChild(d); els.push(d); });
    function place() {
      var w = cv.clientWidth, h = cv.clientHeight, s = Math.max(w / AW, h / AH);
      els.forEach(function (d, i) {
        var t = tiles[i], size = 60 * s;
        d.style.cssText = 'left:' + (w / 2 + (t[0] - AW / 2) * s - size / 2) + 'px;top:' + (h / 2 + (t[1] - AH / 2) * s - size / 2) + 'px;width:' + size + 'px;height:' + size + 'px;border-radius:' + 13 * s + 'px';
      });
    }
    place(); if ('ResizeObserver' in window) new ResizeObserver(place).observe(cv);
  }

  initConnectIcons();
  initRive();
  initMenu(); initFlow(); initRotate(); initFaq();
  /* ---------- מתג בהיר / כהה / לפי המערכת, כמו בתבנית ---------- */
  function initTheme() {
    var sw = document.querySelector('[data-theme-switch]'); if (!sw) return;
    var btns = sw.querySelectorAll('button'), mq = matchMedia('(prefers-color-scheme: dark)'), KEY = 'm2-theme';
    var mode = 'light'; try { mode = localStorage.getItem(KEY) || 'light'; } catch (e) {}
    function apply() {
      var dark = mode === 'dark' || (mode === 'system' && mq.matches);
      document.documentElement.classList.toggle('dark', dark);
      btns.forEach(function (b) {
        var on = b.getAttribute('aria-label').toLowerCase() === mode;
        b.setAttribute('aria-checked', on ? 'true' : 'false');
        b.classList.toggle('border-border-primary', on); b.classList.toggle('border-transparent', !on);
      });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { mode = b.getAttribute('aria-label').toLowerCase(); try { localStorage.setItem(KEY, mode); } catch (e) {} apply(); }); });
    mq.addEventListener && mq.addEventListener('change', apply); apply();
  }
  initTheme(); initRibbons(); initRollers(); initTicker(); initCardDots(); initSectionDots(); initCarousels();
})();
