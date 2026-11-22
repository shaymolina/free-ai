/* Free AI – אנימציות דף הבית (בהשראת Mintlify):
   חוטים שמצטיירים וזזים (canvas), גל חוטים, מספרים שמתגלגלים, קרוסלות, המלצות שרצות.
   בלי JavaScript הכול נשאר במקום ונקרא; מי שביקש פחות תנועה מקבל ציור סטטי. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DPR = Math.min(window.devicePixelRatio || 1, 2);

  function easeOutExpo(x) { return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); }
  function bez(p0, p1, p2, p3, t) { var u = 1 - t; return u * u * u * p0 + 3 * u * u * t * p1 + 3 * u * t * t * p2 + t * t * t * p3; }

  /* ---------- צורות החוטים (במערכת קואורדינטות וירטואלית W x H) ---------- */
  var KINDS = {
    hero: { W: 1440, H: 900, bundles: [
      { n: 26, amp: 18, sp: .35, stops: [[0, '45,212,191', 0], [.55, '74,222,128', .7], [.8, '163,230,53', .85], [1, '163,230,53', .3]],
        f: function (t) { return [820 + 300 * t, 480, 980 + 250 * t, 380 - 60 * t, 1150 + 60 * t, 300 + 120 * t, 1500, 110 + 300 * t]; } },
      { n: 24, amp: 16, sp: .28, stops: [[0, '45,212,191', .15], [.45, '74,222,128', .7], [1, '163,230,53', 0]],
        f: function (t) { return [-60, 820 + 420 * t, 250 + 60 * t, 880 - 160 * t, 520 - 40 * t, 690 + 100 * t, 760, 600 + 160 * t]; } }
    ] },
    card: { W: 600, H: 360, bundles: [
      { n: 18, amp: 14, sp: .3, stops: [[0, '45,212,191', .1], [.5, '74,222,128', .55], [1, '163,230,53', .2]],
        f: function (t) { return [-40, 250 + 90 * t, 160, 120 - 160 * t, 380, 330 + 120 * t, 660, 90 + 200 * t]; } }
    ] },
    art: { W: 400, H: 460, bundles: [
      { n: 34, amp: 20, sp: .45, stops: [[0, '255,255,255', .05], [.5, '255,255,255', .6], [1, '255,255,255', .15]],
        f: function (t) { return [-40, 420 + 240 * t, 120, 300 - 260 * t, 260, 200 + 300 * t, 440, 40 + 160 * t]; } }
    ] },
    art2: { W: 400, H: 460, bundles: [
      { n: 30, amp: 10, sp: .3, stops: [[0, '8,60,40', .35], [.5, '8,60,40', .5], [1, '8,60,40', .3]],
        f: function (t) { var y = 230 + 560 * t; return [-40, y + 40, 120, y - 90, 280, y + 90, 440, y - 30]; } }
    ] },
    art3: { W: 400, H: 460, bundles: [
      { n: 16, amp: 16, sp: .4, stops: [[0, '94,234,212', .1], [.5, '129,140,248', .8], [1, '94,234,212', .3]],
        f: function (t) { return [-40, 400 + 160 * t, 130, -160 + 260 * t, 270, 640 - 260 * t, 440, 60 + 160 * t]; } }
    ] },
    cta: { W: 760, H: 260, bundles: [
      { n: 8, amp: 8, sp: .4, stops: [[0, '74,222,128', .1], [.5, '34,197,94', 1], [1, '163,230,53', .9]],
        f: function (t) { return [480 + 300 * t, 290, 600 + 280 * t, 220, 650 + 260 * t, 100, 700 + 280 * t, -30]; } },
      { n: 6, amp: 8, sp: .3, stops: [[0, '96,165,250', .1], [.5, '59,130,246', .8], [1, '45,212,191', .8]],
        f: function (t) { return [400 + 300 * t, 290, 540 + 280 * t, 230, 600 + 260 * t, 110, 640 + 280 * t, -30]; } },
      { n: 6, amp: 8, sp: .35, stops: [[0, '250,204,21', .1], [.5, '234,179,8', .9], [1, '163,230,53', .9]],
        f: function (t) { return [540 + 260 * t, 290, 660 + 250 * t, 215, 720 + 240 * t, 95, 760 + 240 * t, -30]; } }
    ] }
  };


  /* ---------- סרט חוטים (כמו בפתיחה של Mintlify): 24 חוטים, סיבוב, הבזקי צבע ---------- */
  var RIB = {
    hero: { W: 1720, H: 1080, count: 24, res: 81, spacing: 4.9, amp: 163, freq: .75, phase: .14, twist: .41, bulge: .66, morph: .5,
      speed: .66, from: '#e0461c', to: '#ffc62e', pColors: ['#d87cff', '#ffa723', '#44aeff', '#ffa3d3'], pSize: 3, pLen: 88,
      pSpeed: .84, pSparse: .32, seed: 2025, rotate: -28, edge: .25 }
  };
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

  var items = [];

  function setup(cv) {
    var kind = cv.dataset.kind, k = KINDS[kind] || null, g = RIB[cv.dataset.rib] || null;
    var it = { cv: cv, ctx: cv.getContext('2d'), kind: kind, k: k, t0: 0, vis: false, w: 0, h: 0, flip: cv.dataset.flip === '1', done: false, g: g };
    function size() {
      var r = cv.getBoundingClientRect();
      it.w = Math.max(1, cv.clientWidth); it.h = Math.max(1, cv.clientHeight);
      cv.width = Math.round(it.w * DPR); cv.height = Math.round(it.h * DPR);
      draw(it, it.last || 0);
    }
    it.size = size;
    size();
    items.push(it);
    return it;
  }

  function drawStrings(it, time) {
    var c = it.ctx, k = it.k, w = it.w, h = it.h;
    var s = Math.max(w / k.W, h / k.H), ox = (w - k.W * s) / 2, oy = (h - k.H * s) / 2;
    var prog = reduce ? 1 : easeOutExpo(Math.min(1, time / 2600));
    c.setTransform(DPR, 0, 0, DPR, 0, 0);
    c.clearRect(0, 0, w, h);
    if (it.flip) { c.translate(w, 0); c.scale(-1, 1); }
    c.lineWidth = .9;
    k.bundles.forEach(function (b) {
      var g = c.createLinearGradient(ox, 0, ox + k.W * s, 0);
      b.stops.forEach(function (st) { g.addColorStop(st[0], 'rgba(' + st[1] + ',' + st[2] + ')'); });
      c.strokeStyle = g;
      for (var i = 0; i < b.n; i++) {
        var t = i / (b.n - 1) - .5, p = b.f(t);
        var wob = reduce ? 0 : Math.sin(time / 1000 * b.sp + i * .18) * b.amp;
        var wob2 = reduce ? 0 : Math.cos(time / 1000 * b.sp * .8 + i * .12) * b.amp * .7;
        var P = [p[0], p[1], p[2], p[3] + wob, p[4], p[5] - wob2, p[6], p[7] + wob2 * .5];
        var steps = 60, last = Math.max(2, Math.round(steps * prog));
        c.beginPath();
        for (var j = 0; j <= last; j++) {
          var u = j / steps;
          var x = ox + bez(P[0], P[2], P[4], P[6], u) * s, y = oy + bez(P[1], P[3], P[5], P[7], u) * s;
          if (j) c.lineTo(x, y); else c.moveTo(x, y);
        }
        c.stroke();
      }
    });
    c.setTransform(1, 0, 0, 1, 0, 0);
    if (reduce || (prog >= 1 && it.kind === 'static')) it.done = true;
  }

  function drawWave(it, time) {
    var c = it.ctx, w = it.w, h = it.h, n = 30;
    var prog = reduce ? 1 : easeOutExpo(Math.min(1, time / 2400));
    var T = reduce ? 0 : time / 1000;
    c.setTransform(DPR, 0, 0, DPR, 0, 0);
    c.clearRect(0, 0, w, h);
    if (it.flip) { c.translate(w, 0); c.scale(-1, 1); }
    c.lineWidth = .85;
    var A = [45, 212, 191], B = [163, 230, 53], M = [74, 222, 128];
    for (var i = 0; i < n; i++) {
      var k = i / (n - 1);
      var col = k < .5 ? mix(A, M, k * 2) : mix(M, B, (k - .5) * 2);
      var g = c.createLinearGradient(0, 0, w, 0);
      g.addColorStop(0, 'rgba(' + col + ',0)'); g.addColorStop(.12, 'rgba(' + col + ',.75)');
      g.addColorStop(.88, 'rgba(' + col + ',.75)'); g.addColorStop(1, 'rgba(' + col + ',0)');
      c.strokeStyle = g;
      var ph = k * Math.PI * 1.7 + T * .45;
      var last = Math.max(2, Math.round(90 * prog));
      c.beginPath();
      for (var j = 0; j <= last; j++) {
        var u = j / 90, x = u * w;
        var spread = h * (.3 * Math.pow(1 - u, 1.8) + .03) * (k - .5) * 2;
        var amp = h * (.26 - .12 * u);
        var y = h * .5 + spread + amp * Math.sin(u * Math.PI * 1.9 + ph);
        if (j) c.lineTo(x, y); else c.moveTo(x, y);
      }
      c.stroke();
    }
    c.setTransform(1, 0, 0, 1, 0, 0);
  }
  function mix(a, b, t) { return [0, 1, 2].map(function (q) { return Math.round(a[q] + (b[q] - a[q]) * t); }).join(','); }

  function draw(it, time) { it.last = time; if (it.g) drawRibbon(it, time); else if (it.kind === 'wave') drawWave(it, time); else if (it.k) drawStrings(it, time); }

  function initCanvases() {
    var cvs = document.querySelectorAll('canvas[data-kind]');
    if (!cvs.length) return;
    cvs.forEach(setup);
    if (reduce) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var it = items.filter(function (x) { return x.cv === e.target; })[0];
        if (!it) return;
        it.vis = e.isIntersecting;
        if (it.vis && !it.t0) it.t0 = performance.now();
      });
    });
    items.forEach(function (it) { io.observe(it.cv); });
    function loop(now) {
      items.forEach(function (it) { if (it.vis) draw(it, now - it.t0); });
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { items.forEach(function (it) { it.size(); }); }, 120); });
  }

  /* ---------- מספרים שמתגלגלים פנימה ---------- */
  function initRoll() {
    var els = document.querySelectorAll('[data-roll]');
    els.forEach(function (el) {
      var txt = el.textContent;
      el.setAttribute('aria-label', txt);
      el.innerHTML = txt.split('').map(function (ch, i) {
        return '<span class="dg" aria-hidden="true" style="--i:' + i + '"><span>' + (ch === ' ' ? '&nbsp;' : ch) + '</span></span>';
      }).join('');
    });
    if (reduce || !('IntersectionObserver' in window)) { els.forEach(function (el) { el.classList.add('rolled'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('rolled'); io.unobserve(e.target); } });
    }, { threshold: .4 });
    els.forEach(function (el) { el.classList.add('roll'); io.observe(el); });
  }

  /* ---------- קרוסלות: חיצים + עמעום הכרטיסים שלא במרכז ---------- */
  function initCarousels() {
    document.querySelectorAll('[data-carousel]').forEach(function (wrap) {
      var view = wrap.querySelector('.car'), cards = view.querySelectorAll('.car-track > li');
      var prev = wrap.querySelector('[data-car="-1"]'), next = wrap.querySelector('[data-car="1"]');
      function step(dir) {
        var w = cards[0] ? cards[0].getBoundingClientRect().width + 12 : 400;
        view.scrollBy({ left: -dir * w, behavior: reduce ? 'auto' : 'smooth' });
      }
      if (prev) prev.addEventListener('click', function () { step(-1); });
      if (next) next.addEventListener('click', function () { step(1); });
      function edges() {
        var max = view.scrollWidth - view.clientWidth, x = Math.abs(view.scrollLeft);
        if (prev) prev.disabled = x < 4;
        if (next) next.disabled = x > max - 4;
      }
      view.addEventListener('scroll', edges, { passive: true }); edges();
      if (wrap.hasAttribute('data-dim') && 'IntersectionObserver' in window) {
        view.classList.add('dim');
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (e) { e.target.classList.toggle('is-on', e.intersectionRatio > .75); });
        }, { root: view, threshold: [0, .75, 1] });
        cards.forEach(function (c) { io.observe(c); });
      }
    });
  }

  /* ---------- המלצות שרצות: כפתור עצירה ---------- */
  function initMarquee() {
    var b = document.getElementById('pr-pause'), box = document.getElementById('prompts');
    if (!b || !box) return;
    b.addEventListener('click', function () {
      var p = box.classList.toggle('paused');
      b.textContent = p ? 'הפעלת הדוגמאות' : 'עצירת הדוגמאות';
      b.setAttribute('aria-pressed', p ? 'true' : 'false');
    });
  }

  initCanvases(); initRoll(); initCarousels(); initMarquee();
})();
