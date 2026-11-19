/* הדר נדבק: אחרי תחילת גלילה ההדר מתכווץ למרכז, עם זכוכית מטושטשת. רק במחשב. */
(function () {
  var h = document.querySelector('.c-header, .tf-header .header-inner');
  if (!h) return;
  var sp = document.createElement('div');
  sp.className = 'hdr-spacer';
  h.parentNode.insertBefore(sp, h);
  var on = false, busy = 0;
  function zoom() { var w = h.offsetWidth; return w ? h.getBoundingClientRect().width / w : 1; }
  function from(r, z) {
    h.style.setProperty('--y0', r.top / z + 'px');
    h.style.setProperty('--x0', r.left / z + 'px');
    h.style.setProperty('--x1', (innerWidth / z - r.right / z) + 'px');
  }
  function update() {
    var s = window.scrollY > 30 && innerWidth > 991;
    if (s === on) return;
    on = s;
    clearTimeout(busy);
    if (s) {
      var z = zoom(), r = h.getBoundingClientRect();
      sp.style.height = h.offsetHeight + 'px';
      sp.style.display = 'block';
      from(r, z);
      h.classList.add('hdr-fixed');
      h.offsetWidth;
      h.classList.add('hdr-small');
    } else {
      var z2 = zoom();
      from(sp.getBoundingClientRect(), z2);
      h.classList.remove('hdr-small');
      busy = setTimeout(function () {
        h.classList.remove('hdr-fixed');
        sp.style.display = 'none';
      }, 360);
    }
  }
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', function () { if (on && innerWidth <= 991) update(); });
  update();
})();

/* חשיפה בגלילה: כרטיסים ומקטעים שמתחת למסך עולים פנימה פעם אחת. מי שביקש פחות תנועה – בלי. */
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var els = document.querySelectorAll('.three > *, .sec-title, .faq > *, .art-list > *, .art-sec, .art-cta, .lesson .fstep, .lesson .row');
  if (!els.length) return;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      io.unobserve(el);
      el.classList.add('rv-in');
      setTimeout(function () { el.classList.remove('rv', 'rv-in'); el.style.removeProperty('--rv-d'); }, 1200);
    });
  }, { rootMargin: '0px 0px -6% 0px' });
  els.forEach(function (el) {
    if (el.getBoundingClientRect().top < innerHeight * 0.92) return;
    var i = Array.prototype.indexOf.call(el.parentNode.children, el) % 4;
    el.style.setProperty('--rv-d', (i * 70) + 'ms');
    el.classList.add('rv');
    io.observe(el);
  });
})();
