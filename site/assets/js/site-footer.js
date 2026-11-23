/* נקודות ברקע בחלק העליון של הפוטר, בשני הצדדים. נטען מתוך הפוטר האחיד (tools/site_build/site_footer.py). */
(function () {
  var cv = document.querySelector('footer.sf canvas.sf-dots');
  if (!cv || !cv.getContext) return;
  var foot = cv.parentElement, inner = foot.querySelector('.sf-in'), ctx = cv.getContext('2d');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var G0 = [12, 140, 94], G1 = [115, 158, 22], BASE = .14, BAND = 320;
  var W = 0, H = 0, r = 1, dots = [], raf = 0, vis = false;
  function h2(a, b) { var n = Math.imul(a, 0x165667b1) + Math.imul(b, 0x27d4eb2f); n = Math.imul(n ^ (n >>> 13), 0x4bf19f61); n ^= n >>> 16; return (n >>> 0) / 0xffffffff; }
  function ss(x) { return x * x * (3 - 2 * x); }
  function noise(x, y) { var X = Math.floor(x), Y = Math.floor(y), u = ss(x - X), v = ss(y - Y), a = h2(X, Y), b = h2(X + 1, Y), c = h2(X, Y + 1), d = h2(X + 1, Y + 1), t = a + (b - a) * u; return t + (c + (d - c) * u - t) * v; }
  function field(x, y) { var fx = x / 70, fy = y / 70; return .65 * noise(fx, fy) + .35 * noise(2.3 * fx + 11.7, 2.3 * fy + 5.1); }
  function setup() {
    r = Math.min(window.devicePixelRatio || 1, 2); W = foot.clientWidth; H = Math.min(BAND, foot.clientHeight);
    if (W <= 0 || H <= 0) return;
    cv.style.width = W + 'px'; cv.style.height = H + 'px'; cv.width = W * r; cv.height = H * r; ctx.setTransform(r, 0, 0, r, 0, 0);
    var b = inner.getBoundingClientRect(), f = foot.getBoundingClientRect(), L = b.left - f.left, R = b.right - f.left;
    var now = performance.now(); dots = [];
    for (var x = 7; x < W; x += 14) {
      var out = x < L ? L - x : x > R ? x - R : -1; if (out < 0) continue;
      var ex = ss(Math.min(1, out / 72));
      for (var y = 7; y < H; y += 14) {
        if (field(Math.min(x, W - x), y) < .6) continue;
        var a = ex * Math.max(0, 1 - y / H); if (a <= .02) continue;
        dots.push({ x: x, y: y, a: a, g: Math.random() < .1, next: now + Math.random() * 6000 });
      }
    }
    draw();
  }
  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < dots.length; i++) {
      var d = dots[i], c = d.g ? 1 : 0, t = Math.max(0, Math.min(1, d.x / W));
      ctx.fillStyle = 'rgb(' + Math.round((G0[0] + (G1[0] - G0[0]) * t) * c) + ',' + Math.round((G0[1] + (G1[1] - G0[1]) * t) * c) + ',' + Math.round((G0[2] + (G1[2] - G0[2]) * t) * c) + ')';
      ctx.globalAlpha = (BASE + (.85 - BASE) * c) * d.a; ctx.fillRect(d.x - 1, d.y - 1, 2, 2);
    }
    ctx.globalAlpha = 1;
  }
  function tick(now) {
    for (var i = 0; i < dots.length; i++) { var d = dots[i]; if (now >= d.next) { d.g = Math.random() < .1; d.next = now + 2200 + Math.random() * 3800; } }
    draw(); raf = requestAnimationFrame(tick);
  }
  setup();
  if ('ResizeObserver' in window) new ResizeObserver(setup).observe(foot); else addEventListener('resize', setup);
  if (reduce || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(tick); if (!vis && raf) { cancelAnimationFrame(raf); raf = 0; } }).observe(foot);
})();
