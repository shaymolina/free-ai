/* אזור משתמשים: התחברות עם גוגל או עם מייל וסיסמה, דרך Supabase.
   מי שלא מחובר ונכנס לעמוד נעול רואה חלון התחברות מעל עמוד מטושטש.
   ההגדרות (כתובת הפרויקט, המפתח הציבורי, האם העמוד נעול) מגיעות מ-window.FA_AUTH, שנכתב בכל עמוד ע"י tools/site_build/site_header.py. */
(function () {
  var CFG = window.FA_AUTH || {};
  if (!window.supabase || !CFG.url) return;
  var SB = window.supabase.createClient(CFG.url, CFG.key, {
    auth: { flowType: 'pkce', detectSessionInUrl: true, persistSession: true, autoRefreshToken: true }
  });
  var user = null, box = null, recovering = false;
  var BACK = function () { return location.origin + location.pathname; };

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s || '').replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function msg(t, info) { var e = box && box.querySelector('.ag-err'); if (e) { e.textContent = t; e.classList.toggle('is-info', !!info); e.hidden = false; } }
  function hideMsg() { var e = box && box.querySelector('.ag-err'); if (e) e.hidden = true; }
  function busy(b, on) { b.disabled = on; b.classList.toggle('is-busy', on); }

  function he(err) {
    var m = String((err && err.message) || err || '').toLowerCase();
    if (m.indexOf('rate limit') > -1 || m.indexOf('too many') > -1 || m.indexOf('security purposes') > -1) return 'יותר מדי ניסיונות. נסו שוב בעוד כמה דקות.';
    if (m.indexOf('not confirmed') > -1) return 'צריך לאשר את המייל קודם. חפשו אצלכם מייל מ-Supabase ולחצו על הקישור.';
    if (m.indexOf('password should') > -1 || m.indexOf('weak') > -1) return 'הסיסמה חלשה מדי. נסו לפחות 8 תווים עם אותיות ומספרים.';
    if (m.indexOf('provider is not enabled') > -1 || m.indexOf('unsupported provider') > -1) return 'ההתחברות עם גוגל עוד לא הופעלה באתר. בינתיים אפשר עם מייל וסיסמה.';
    if (m.indexOf('failed to fetch') > -1 || m.indexOf('network') > -1) return 'אין חיבור לשרת. בדקו את האינטרנט ונסו שוב.';
    return 'משהו לא עבד. נסו שוב.';
  }

  var G = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>';
  function ic(d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>'; }
  var I_MAIL = ic('<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>');
  var I_KEY = ic('<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r=".5" fill="currentColor"/>');
  var I_EYE = ic('<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>');
  var I_EYE_OFF = ic('<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/>');

  function passField(id, label, extra, auto) {
    return '<div class="ag-field">' +
      '<div class="ag-row"><label class="ag-label" for="' + id + '">' + label + '</label>' + (extra || '') + '</div>' +
      '<div class="ag-rel"><span class="ag-ico">' + I_KEY + '</span>' +
      '<input class="ag-input ag-input-pass" id="' + id + '" name="password" type="password" autocomplete="' + auto + '" dir="ltr" required>' +
      '<button class="ag-eye" type="button" aria-label="הצגת הסיסמה">' + I_EYE + '</button></div>' +
    '</div>';
  }
  var FINE = '<div class="ag-footer"><p class="ag-fine">בהתחברות אתם מסכימים ל<a href="terms">תנאי השימוש</a> ול<a href="privacy">מדיניות הפרטיות</a></p></div>';

  function cardSignIn() {
    return '<div class="ag-card">' +
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
          passField('ag-pass', 'סיסמה', '<a href="#" class="ag-forgot">שכחת סיסמה?</a>', 'current-password') +
          '<p class="ag-err" role="alert" hidden></p>' +
          '<button class="ag-btn ag-primary ag-submit" type="submit">התחברות</button>' +
        '</form>' +
      '</div>' + FINE +
    '</div>';
  }
  function cardReset() {
    return '<div class="ag-card">' +
      '<div class="ag-head">' +
        '<h2 class="ag-title" id="ag-t">סיסמה חדשה</h2>' +
        '<p class="ag-desc">בוחרים סיסמה חדשה, ומאותו רגע נכנסים איתה.</p>' +
      '</div>' +
      '<div class="ag-content">' +
        '<form class="ag-form" novalidate>' +
          passField('ag-pass', 'סיסמה חדשה', '', 'new-password') +
          '<p class="ag-err" role="alert" hidden></p>' +
          '<button class="ag-btn ag-primary ag-submit" type="submit">שמירת הסיסמה</button>' +
        '</form>' +
      '</div>' +
    '</div>';
  }

  function wireEye() {
    var pass = box.querySelector('#ag-pass'), eye = box.querySelector('.ag-eye');
    eye.addEventListener('click', function () {
      var show = pass.type === 'password';
      pass.type = show ? 'text' : 'password';
      eye.innerHTML = show ? I_EYE_OFF : I_EYE;
      eye.setAttribute('aria-label', show ? 'הסתרת הסיסמה' : 'הצגת הסיסמה');
    });
  }

  function showGate(mode) {
    document.documentElement.classList.add('ag-lock');
    if (!box) {
      box = el('div');
      box.id = 'ag';
      box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'ag-t');
      document.body.appendChild(box);
      requestAnimationFrame(function () { requestAnimationFrame(function () { box && box.classList.add('is-in'); }); });
    }
    box.innerHTML = mode === 'reset' ? cardReset() : cardSignIn();
    wireEye();
    var form = box.querySelector('.ag-form'), submit = box.querySelector('.ag-submit');

    if (mode === 'reset') {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var pw = form.password.value;
        if (pw.length < 8) return msg('הסיסמה צריכה להיות לפחות 8 תווים.');
        hideMsg(); busy(submit, true);
        SB.auth.updateUser({ password: pw }).then(function (r) {
          if (r.error) throw r.error;
          recovering = false; user = r.data.user; unlock();
        }).catch(function (err) { busy(submit, false); msg(he(err)); });
      });
      return;
    }

    // גוגל: עוברים לגוגל וחוזרים לאותו עמוד, מחוברים
    var g = box.querySelector('.ag-google');
    g.addEventListener('click', function () {
      busy(g, true);
      SB.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: BACK() } }).then(function (r) {
        if (r.error) { busy(g, false); msg(he(r.error)); }
      });
    });

    // שכחת סיסמה: שולחים קישור איפוס למייל שבשדה
    box.querySelector('.ag-forgot').addEventListener('click', function (e) {
      e.preventDefault();
      var email = form.email.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { form.email.focus(); return msg('כתבו קודם את המייל שלכם בשדה למעלה.'); }
      hideMsg();
      SB.auth.resetPasswordForEmail(email, { redirectTo: BACK() }).then(function (r) {
        if (r.error) return msg(he(r.error));
        msg('שלחנו קישור לאיפוס הסיסמה ל-' + email + '. לוחצים עליו וחוזרים לכאן.', true);
      });
    });

    // מייל וסיסמה: קודם מנסים להיכנס. אין חשבון כזה? פותחים אחד.
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.email.value.trim().toLowerCase(), pw = form.password.value;
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return msg('המייל לא נראה תקין.');
      if (pw.length < 8) return msg('הסיסמה צריכה להיות לפחות 8 תווים.');
      hideMsg(); busy(submit, true);
      SB.auth.signInWithPassword({ email: email, password: pw }).then(function (r) {
        if (!r.error) { user = r.data.user; return unlock(); }
        if (String(r.error.message).toLowerCase().indexOf('invalid login') === -1) throw r.error;
        return SB.auth.signUp({ email: email, password: pw, options: { emailRedirectTo: BACK() } }).then(function (s) {
          if (s.error) {
            if (String(s.error.message).toLowerCase().indexOf('already') > -1) { busy(submit, false); return msg('הסיסמה לא נכונה. נרשמתם עם גוגל? לחצו על Google למעלה.'); }
            throw s.error;
          }
          if (s.data.user && s.data.user.identities && s.data.user.identities.length === 0) { busy(submit, false); return msg('הסיסמה לא נכונה. נרשמתם עם גוגל? לחצו על Google למעלה.'); }
          if (s.data.session) { user = s.data.user; return unlock(); }
          busy(submit, false);
          msg('כמעט סיימנו: שלחנו מייל אישור ל-' + email + '. לוחצים על הקישור שבו וחוזרים לכאן.', true);
        });
      }).catch(function (err) { busy(submit, false); msg(he(err)); });
    });
  }

  function unlock() {
    document.documentElement.classList.remove('ag-lock');
    if (box) { var b = box; box = null; b.classList.remove('is-in'); setTimeout(function () { b.remove(); }, 400); }
    renderMe();
    touch();
  }

  // מעדכן בטבלת profiles מתי המשתמש נכנס לאחרונה (פעם ביום לכל היותר)
  function touch() {
    if (!user) return;
    var k = 'fa_seen_' + user.id, d = new Date().toISOString().slice(0, 10);
    try { if (localStorage.getItem(k) === d) return; localStorage.setItem(k, d); } catch (e) {}
    SB.from('profiles').update({ last_seen_at: new Date().toISOString() }).eq('id', user.id).then(function () {});
  }

  function renderMe() {
    var inner = document.querySelector('.gh-in'), old = document.querySelector('.ag-me');
    if (old) old.remove();
    if (!user || !inner) return;
    var md = user.user_metadata || {};
    var name = md.full_name || md.name || (user.email || '').split('@')[0], pic = md.avatar_url || md.picture || '';
    var first = esc((name || user.email || '?').trim().charAt(0));
    var me = el('div', 'ag-me');
    me.innerHTML =
      '<button class="ag-av" type="button" aria-label="החשבון שלי" aria-expanded="false">' +
      (pic ? '<img src="' + esc(pic) + '" alt="" referrerpolicy="no-referrer">' : first) + '</button>' +
      '<div class="ag-menu" hidden><div class="ag-name">' + esc(name) + '</div><div class="ag-mail">' + esc(user.email) + '</div>' +
      '<button class="ag-out" type="button">התנתקות</button></div>';
    inner.insertBefore(me, inner.querySelector('.gh-btn') || inner.querySelector('.gh-burger'));
    var av = me.querySelector('.ag-av'), menu = me.querySelector('.ag-menu');
    var img = av.querySelector('img'); if (img) img.onerror = function () { av.textContent = first; };
    av.addEventListener('click', function (e) { e.stopPropagation(); menu.hidden = !menu.hidden; av.setAttribute('aria-expanded', menu.hidden ? 'false' : 'true'); });
    document.addEventListener('click', function (e) { if (!me.contains(e.target)) { menu.hidden = true; av.setAttribute('aria-expanded', 'false'); } });
    me.querySelector('.ag-out').addEventListener('click', function () {
      SB.auth.signOut().finally(function () { location.reload(); });
    });
  }

  SB.auth.onAuthStateChange(function (event, session) {
    if (event === 'PASSWORD_RECOVERY') { recovering = true; user = session && session.user; setTimeout(function () { showGate('reset'); }, 0); return; }
    if (event === 'SIGNED_OUT') { user = null; return; }
    if (session && !recovering && !user) { user = session.user; setTimeout(unlock, 0); }
  });

  function start() {
    SB.auth.getSession().then(function (r) {
      var s = r.data && r.data.session;
      if (recovering) return;
      if (s) { user = s.user; unlock(); return; }
      // תצוגה מקדימה של העמוד בתוך דף הבית (iframe מאותו אתר) לא ננעלת
      var framed = false; try { framed = self !== top && top.location.host === location.host; } catch (e) {}
      if (CFG.locked && !framed) showGate('signin');
      else document.documentElement.classList.remove('ag-lock');
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
