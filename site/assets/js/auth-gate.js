/* התחברות עם גוגל או עם מייל וסיסמה. מי שלא מחובר רואה חלון התחברות מעל עמוד מטושטש.
   ההגדרות (מזהה הלקוח של גוגל, האם העמוד נעול) מגיעות מ-window.FA_AUTH, שנכתב בכל עמוד ע"י tools/site_build/site_header.py. */
(function () {
  var CFG = window.FA_AUTH || {}, KEY = 'fa_user', mem = null;

  function get() {
    try { var u = JSON.parse(localStorage.getItem(KEY)); if (u && u.email) return u; } catch (e) {}
    return mem;
  }
  function save(u) { mem = u; try { localStorage.setItem(KEY, JSON.stringify(u)); } catch (e) {} }
  function clear() { mem = null; try { localStorage.removeItem(KEY); } catch (e) {} }

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

  var box = null;
  function showErr(t) { var e = box && box.querySelector('.ag-err'); if (e) { e.textContent = t; e.hidden = false; } }
  function hideErr() { var e = box && box.querySelector('.ag-err'); if (e) e.hidden = true; }

  var G = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>';

  function ic(d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>'; }
  var I_MAIL = ic('<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>');
  var I_KEY = ic('<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r=".5" fill="currentColor"/>');
  var I_EYE = ic('<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>');
  var I_EYE_OFF = ic('<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/>');

  function showGate() {
    if (box) return;
    box = el('div');
    box.id = 'ag';
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'ag-t');
    box.innerHTML =
      '<div class="ag-card">' +
        '<div class="ag-head">' +
          '<h2 class="ag-title" id="ag-t">התחברות עם מייל</h2>' +
          '<p class="ag-desc">המדריך, הקורס והמאמרים פתוחים למי שמחובר. בחינם.</p>' +
        '</div>' +
        '<div class="ag-content">' +
          '<div class="ag-social">' +
            '<span class="ag-label ag-label-xs">התחברות עם</span>' +
            '<button class="ag-btn ag-outline ag-google" type="button">' + G + '<span>Google</span></button>' +
          '</div>' +
          '<div class="ag-or"><span>או</span></div>' +
          '<form class="ag-form" novalidate>' +
            '<div class="ag-field">' +
              '<label class="ag-label" for="ag-email">מייל</label>' +
              '<div class="ag-rel"><span class="ag-ico">' + I_MAIL + '</span>' +
              '<input class="ag-input" id="ag-email" name="email" type="email" placeholder="name@gmail.com" autocomplete="email" dir="ltr" required></div>' +
            '</div>' +
            '<div class="ag-field">' +
              '<div class="ag-row"><label class="ag-label" for="ag-pass">סיסמה</label>' +
              '<a href="#" class="ag-forgot">שכחת סיסמה?</a></div>' +
              '<div class="ag-rel"><span class="ag-ico">' + I_KEY + '</span>' +
              '<input class="ag-input ag-input-pass" id="ag-pass" name="password" type="password" autocomplete="current-password" dir="ltr" required>' +
              '<button class="ag-eye" type="button" aria-label="הצגת הסיסמה">' + I_EYE + '</button></div>' +
            '</div>' +
            '<p class="ag-err" role="alert" hidden></p>' +
            '<button class="ag-btn ag-primary ag-submit" type="submit">התחברות</button>' +
          '</form>' +
        '</div>' +
        '<div class="ag-footer">' +
          '<p class="ag-fine">בהתחברות אתם מסכימים ל<a href="terms">תנאי השימוש</a> ול<a href="privacy">מדיניות הפרטיות</a></p>' +
        '</div>' +
      '</div>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { requestAnimationFrame(function () { box.classList.add('is-in'); }); });

    // סיסמה: הצגה והסתרה
    var pass = box.querySelector('#ag-pass'), eye = box.querySelector('.ag-eye');
    eye.addEventListener('click', function () {
      var show = pass.type === 'password';
      pass.type = show ? 'text' : 'password';
      eye.innerHTML = show ? I_EYE_OFF : I_EYE;
      eye.setAttribute('aria-label', show ? 'הסתרת הסיסמה' : 'הצגת הסיסמה');
    });
    box.querySelector('.ag-forgot').addEventListener('click', function (e) {
      e.preventDefault();
      showErr('נרשמתם עם מייל של גוגל? לחצו על Google למעלה ותיכנסו בלי סיסמה.');
    });

    // מייל וסיסמה: השרת פותח חשבון בכניסה הראשונה, ובודק את הסיסמה בכניסות הבאות
    var form = box.querySelector('.ag-form'), submit = box.querySelector('.ag-submit');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.email.value.trim(), pw = form.password.value;
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return showErr('המייל לא נראה תקין.');
      if (pw.length < 8) return showErr('הסיסמה צריכה להיות לפחות 8 תווים.');
      hideErr(); submit.disabled = true; submit.classList.add('is-busy');
      fetch('/api/auth/email', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({ email: email, password: pw }) })
        .then(function (r) { return r.json().catch(function () { return { error: 'server' }; }); })
        .then(function (d) {
          if (d && d.user) { save({ name: d.user.name || '', email: d.user.email, picture: '', at: Date.now(), via: 'email' }); return unlock(); }
          throw d && d.error;
        })
        .catch(function (code) {
          submit.disabled = false; submit.classList.remove('is-busy');
          showErr(code === 'wrong_password' ? 'הסיסמה לא נכונה.'
            : code === 'google_account' ? 'המייל הזה נרשם דרך גוגל. לחצו על Google למעלה.'
            : 'ההתחברות עם מייל לא זמינה כרגע. נסו עם Google.');
        });
    });

    var btn = box.querySelector('.ag-google');
    if (!CFG.clientId) { btn.disabled = true; return; }
    var tc = null;
    function fail(t) { btn.classList.remove('is-busy'); if (t) showErr(t); }
    loadGis(function (err) {
      if (err) return;
      tc = google.accounts.oauth2.initTokenClient({
        client_id: CFG.clientId, scope: 'openid email profile',
        callback: function (r) {
          if (!r || !r.access_token) return fail('ההתחברות לא הושלמה. נסו שוב.');
          fetch('https://www.googleapis.com/oauth2/v3/userinfo', { headers: { Authorization: 'Bearer ' + r.access_token } })
            .then(function (x) { return x.json(); })
            .then(function (p) {
              if (!p.email) throw 0;
              save({ name: p.name || '', email: p.email, picture: p.picture || '', sub: p.sub, at: Date.now(), via: 'google' });
              fetch('/api/auth/google', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({ access_token: r.access_token }) }).catch(function () {});
              unlock();
            })
            .catch(function () { fail('ההתחברות לא הצליחה. נסו שוב.'); });
        },
        error_callback: function () { fail(); }
      });
    });
    btn.addEventListener('click', function () {
      if (!tc) return showErr('רגע, ההתחברות של גוגל עוד נטענת. נסו שוב בעוד שנייה.');
      btn.classList.add('is-busy');
      tc.requestAccessToken();
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
      try { navigator.sendBeacon('/api/auth/logout'); } catch (e) {}
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
