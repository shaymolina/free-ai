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
