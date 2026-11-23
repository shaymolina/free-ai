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

  var G = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>';

  function strings() {
    var d = '';
    for (var i = 0; i < 16; i++) {
      var y = 40 + i * 34;
      d += '<path d="M-20 ' + (y + 120) + ' C 120 ' + (y - 80 + i * 6) + ', 260 ' + (y + 160 - i * 9) + ', 420 ' + (y - 40) + '"/>';
    }
    return '<svg class="ag-strings" viewBox="0 0 400 640" preserveAspectRatio="none" aria-hidden="true">' + d + '</svg>';
  }
  var CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 10.5l3.2 3L15 6.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function showGate() {
    if (box) return;
    box = el('div');
    box.id = 'ag';
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'ag-t');
    box.innerHTML =
      '<div class="ag-card">' +
        '<div class="ag-form">' +
          '<img class="ag-logo" src="assets/images/logo/logo.svg" alt="Free AI">' +
          '<h2 class="ag-title" id="ag-t">כניסה ל-Free AI</h2>' +
          '<p class="ag-sub">כדי להמשיך לקרוא צריך להתחבר. בפעם הראשונה החשבון נפתח לבד.</p>' +
          '<button class="ag-google" type="button">' + G + '<span>המשך עם Google</span></button>' +
          '<p class="ag-err" role="alert" hidden></p>' +
          '<div class="ag-or"><span>מה גוגל מעבירה אלינו</span></div>' +
          '<p class="ag-note">רק שם, מייל ותמונת פרופיל. אין סיסמה לזכור ואין כרטיס אשראי.</p>' +
          '<p class="ag-fine">בהתחברות אתם מסכימים ל<a href="terms">תנאי השימוש</a> ול<a href="privacy">מדיניות הפרטיות</a>.</p>' +
          '<a class="ag-home" href="/"><span aria-hidden="true">→</span> חזרה לדף הבית</a>' +
        '</div>' +
        '<aside class="ag-side" aria-hidden="true">' + strings() +
          '<div class="ag-side-in">' +
            '<div class="ag-kicker">חשבון חינמי</div>' +
            '<div class="ag-side-t">לומדים קלוד קוד בעברית, בלי לדעת לתכנת</div>' +
            '<ul class="ag-list">' +
              '<li>' + CHECK + 'המדריך הכתוב, 22 פרקים</li>' +
              '<li>' + CHECK + 'הקורס, שיעור אחרי שיעור</li>' +
              '<li>' + CHECK + 'מאמרים וסקילים להורדה</li>' +
            '</ul>' +
          '</div>' +
        '</aside>' +
      '</div>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { requestAnimationFrame(function () { box.classList.add('is-in'); }); });

    var btn = box.querySelector('.ag-google');
    if (!CFG.clientId) { btn.disabled = true; showErr('ההתחברות עם גוגל עוד לא הוגדרה באתר.'); return; }
    var tc = null;
    function fail(t) { btn.classList.remove('is-busy'); if (t) showErr(t); }
    loadGis(function (err) {
      if (err) return showErr('לא הצלחנו לטעון את ההתחברות של גוגל. בדקו את החיבור ורעננו את העמוד.');
      tc = google.accounts.oauth2.initTokenClient({
        client_id: CFG.clientId, scope: 'openid email profile',
        callback: function (r) {
          if (!r || !r.access_token) return fail('ההתחברות לא הושלמה. נסו שוב.');
          fetch('https://www.googleapis.com/oauth2/v3/userinfo', { headers: { Authorization: 'Bearer ' + r.access_token } })
            .then(function (x) { return x.json(); })
            .then(function (p) {
              if (!p.email) throw 0;
              save({ name: p.name || '', email: p.email, picture: p.picture || '', sub: p.sub, at: Date.now() });
              unlock();
            })
            .catch(function () { fail('ההתחברות לא הצליחה. נסו שוב.'); });
        },
        error_callback: function () { fail(); }
      });
    });
    btn.addEventListener('click', function () {
      if (!tc) return showErr('רגע, ההתחברות עוד נטענת. נסו שוב בעוד שנייה.');
      btn.classList.add('is-busy');
      tc.requestAccessToken();
    });
    setTimeout(function () { btn.focus(); }, 50);
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
