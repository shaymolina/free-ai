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

  var items = [];

  function setup(cv) {
    var kind = cv.dataset.kind, k = KINDS[kind] || null;
    var it = { cv: cv, ctx: cv.getContext('2d'), kind: kind, k: k, t0: 0, vis: false, w: 0, h: 0, flip: cv.dataset.flip === '1', done: false };
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

  function draw(it, time) { it.last = time; if (it.kind === 'wave') drawWave(it, time); else if (it.k) drawStrings(it, time); }

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
      b.textContent = p ? 'הפעלה' : 'עצירה';
      b.setAttribute('aria-pressed', p ? 'true' : 'false');
    });
  }

  initCanvases(); initRoll(); initCarousels(); initMarquee();
})();
