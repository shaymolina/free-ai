/* הדר אחד לכל האתר: גלולה בגלילה, תפריט בנייד. */
(function () {
  var h = document.getElementById('gh');
  if (!h) return;
  function u() { h.classList.toggle('is-pill', window.scrollY > 30); }
  addEventListener('scroll', u, { passive: true }); u();
  var b = h.querySelector('.gh-burger'), m = document.getElementById('gh-m');
  if (b && m) b.addEventListener('click', function () {
    var open = m.hidden; m.hidden = !open; b.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
