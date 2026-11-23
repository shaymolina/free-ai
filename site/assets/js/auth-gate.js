/* התחברות עם גוגל. מי שלא מחובר רואה חלון התחברות מעל עמוד מטושטש.
   ההגדרות (מזהה הלקוח של גוגל, האם העמוד נעול) מגיעות מ-window.FA_AUTH, שנכתב בכל עמוד ע"י tools/site_build/site_header.py. */
(function () {
  var CFG = window.FA_AUTH || {}, KEY = 'fa_user', mem = null;

  function get() {
    try { var u = JSON.parse(localStorage.getItem(KEY)); if (u && u.email) return u; } catch (e) {}
    return mem;
  }
  function save(u) { mem = u; try { localStorage.setItem(KEY, JSON.stringify(u)); } catch (e) {} }
  function clear() { mem = null; try { localStorage.removeItem(KEY); } catch (e) {} }

  function decode(t) {
    var p = t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    while (p.length % 4) p += '=';
    var s = atob(p);
    try { s = decodeURIComponent(s.split('').map(function (c) { return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2); }).join('')); } catch (e) {}
    return JSON.parse(s);
  }

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s || '').replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  var gisLoading = null;
  function loadGis(cb) {
    if (window.google && google.accounts && google.accounts.id) return cb();
    if (!gisLoading) {
      gisLoading = [];
      var s = document.createElement('script');
      s.src = 'https://accounts.google.com/gsi/client'; s.async = true;
      s.onload = function () { gisLoading.forEach(function (f) { f(); }); };
      s.onerror = function () { gisLoading.forEach(function (f) { f(new Error('gis')); }); };
      document.head.appendChild(s);
    }
    gisLoading.push(cb);
  }

  function onCredential(r) {
    try {
      var p = decode(r.credential);
      save({ name: p.name || '', email: p.email, picture: p.picture || '', sub: p.sub, at: Date.now() });
      unlock();
    } catch (e) { showErr('ההתחברות לא הצליחה. נסו שוב.'); }
  }

  var box = null;
  function showErr(t) { var e = box && box.querySelector('.ag-err'); if (e) { e.textContent = t; e.hidden = false; } }

  function strings() {
    var d = '';
    for (var i = 0; i < 7; i++) {
      var y = 18 + i * 13;
      d += '<path d="M-10 ' + y + ' C 90 ' + (y - 30 + i * 4) + ', 230 ' + (y + 40 - i * 5) + ', 420 ' + (y - 8) + '"/>';
    }
    return '<svg class="ag-strings" viewBox="0 0 400 120" preserveAspectRatio="none" aria-hidden="true">' + d + '</svg>';
  }

  function showGate() {
    if (box) return;
    box = el('div');
    box.id = 'ag';
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'ag-t');
    box.innerHTML =
      '<div class="ag-card">' + strings() +
      '<img class="ag-logo" src="assets/images/logo/logo.svg" alt="Free AI">' +
      '<h2 class="ag-title" id="ag-t">מתחברים ומתחילים</h2>' +
      '<p class="ag-text">המדריך, הקורס והמאמרים פתוחים למי שמחובר. זה בחינם, ולוקח לחיצה אחת עם חשבון גוגל.</p>' +
      '<div class="ag-btn" id="ag-g"></div>' +
      '<p class="ag-err" hidden></p>' +
      '<p class="ag-fine">בהתחברות אתם מסכימים ל<a href="terms">תנאי השימוש</a> ול<a href="privacy">מדיניות הפרטיות</a>.</p>' +
      '<a class="ag-home" href="/">חזרה לדף הבית</a>' +
      '</div>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { requestAnimationFrame(function () { box.classList.add('is-in'); }); });

    if (!CFG.clientId) { showErr('ההתחברות עם גוגל עוד לא הוגדרה באתר.'); return; }
    loadGis(function (err) {
      if (err) return showErr('לא הצלחנו לטעון את ההתחברות של גוגל. בדקו את החיבור ורעננו את העמוד.');
      google.accounts.id.initialize({ client_id: CFG.clientId, callback: onCredential, auto_select: true, ux_mode: 'popup', context: 'signin' });
      var w = Math.min(320, box.querySelector('.ag-card').clientWidth - 56);
      google.accounts.id.renderButton(document.getElementById('ag-g'), { theme: 'outline', size: 'large', shape: 'pill', text: 'continue_with', locale: 'he', width: w });
      google.accounts.id.prompt();
    });
  }

  function unlock() {
    document.documentElement.classList.remove('ag-lock');
    if (box) { var b = box; box = null; b.classList.remove('is-in'); setTimeout(function () { b.remove(); }, 400); }
    renderMe();
  }

  function renderMe() {
    var u = get(), inner = document.querySelector('.gh-in'), old = document.querySelector('.ag-me');
    if (old) old.remove();
    if (!u || !inner) return;
    var me = el('div', 'ag-me');
    var first = esc((u.name || u.email).trim().charAt(0));
    me.innerHTML =
      '<button class="ag-av" type="button" aria-label="החשבון שלי" aria-expanded="false">' +
      (u.picture ? '<img src="' + esc(u.picture) + '" alt="" referrerpolicy="no-referrer">' : first) + '</button>' +
      '<div class="ag-menu" hidden><div class="ag-name">' + esc(u.name) + '</div><div class="ag-mail">' + esc(u.email) + '</div>' +
      '<button class="ag-out" type="button">התנתקות</button></div>';
    var btn = inner.querySelector('.gh-btn') || inner.querySelector('.gh-burger');
    inner.insertBefore(me, btn);
    var av = me.querySelector('.ag-av'), menu = me.querySelector('.ag-menu');
    var img = av.querySelector('img'); if (img) img.onerror = function () { av.textContent = first; };
    av.addEventListener('click', function (e) { e.stopPropagation(); menu.hidden = !menu.hidden; av.setAttribute('aria-expanded', menu.hidden ? 'false' : 'true'); });
    document.addEventListener('click', function (e) { if (!me.contains(e.target)) { menu.hidden = true; av.setAttribute('aria-expanded', 'false'); } });
    me.querySelector('.ag-out').addEventListener('click', function () {
      clear();
      try { if (window.google && google.accounts) google.accounts.id.disableAutoSelect(); } catch (e) {}
      location.reload();
    });
  }

  function start() {
    var preview = /[?&]login\b/.test(location.search);
    if (CFG.locked && (CFG.clientId || preview) && !get()) {
      document.documentElement.classList.add('ag-lock');
      showGate();
    } else {
      document.documentElement.classList.remove('ag-lock');
      renderMe();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
