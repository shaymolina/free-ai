/* אזור משתמשים: התחברות עם גוגל, דרך Supabase.
   מי שלא מחובר ונכנס לעמוד נעול רואה חלון התחברות מעל עמוד מטושטש.
   ההגדרות (כתובת הפרויקט, המפתח הציבורי, האם העמוד נעול) מגיעות מ-window.FA_AUTH, שנכתב בכל עמוד ע"י tools/site_build/site_header.py. */
(function () {
  var CFG = window.FA_AUTH || {};
  if (!window.supabase || !CFG.url) return;
  var SB = window.supabase.createClient(CFG.url, CFG.key, {
    auth: { flowType: 'pkce', detectSessionInUrl: true, persistSession: true, autoRefreshToken: true }
  });
  var user = null, box = null;
  var BACK = function () { return location.origin + location.pathname; };

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s || '').replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function msg(t, info) { var e = box && box.querySelector('.ag-err'); if (e) { e.textContent = t; e.classList.toggle('is-info', !!info); e.hidden = false; } }
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

  function card() {
    return '<div class="ag-card">' +
      '<img class="ag-logo" src="assets/images/logo/favicon.svg" alt="Free AI" width="56" height="56">' +
      '<h2 class="ag-title" id="ag-t">ברוכים הבאים ל-Free AI</h2>' +
      '<p class="ag-desc">מתחברים בלחיצה אחת, וממשיכים מאיפה שעצרתם.</p>' +
      '<button class="ag-btn ag-outline ag-google" type="button">' + G + '<span>המשך עם Google</span></button>' +
      '<p class="ag-err" role="alert" hidden></p>' +
      '<p class="ag-fine">בהתחברות אתם מסכימים ל<a href="terms">תנאי השימוש</a> ול<a href="privacy">מדיניות הפרטיות</a></p>' +
    '</div>';
  }

  function showGate() {
    document.documentElement.classList.add('ag-lock');
    if (box) return;
    box = el('div');
    box.id = 'ag';
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-labelledby', 'ag-t');
    box.innerHTML = card();
    document.body.appendChild(box);
    requestAnimationFrame(function () { requestAnimationFrame(function () { box && box.classList.add('is-in'); }); });

    // גוגל: עוברים לגוגל וחוזרים לאותו עמוד, מחוברים
    var g = box.querySelector('.ag-google');
    g.addEventListener('click', function () {
      busy(g, true);
      SB.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: BACK() } }).then(function (r) {
        if (r.error) { busy(g, false); msg(he(r.error)); }
      });
    });
  }

  function unlock() {
    document.documentElement.classList.remove('ag-lock');
    if (box) { var b = box; box = null; b.classList.remove('is-in'); setTimeout(function () { b.remove(); }, 400); }
    renderMe();
    renderSide();
    touch();
    syncProgress();
  }

  // ---- התקדמות במדריך: נשמרת בדפדפן (freeai-guide-done) ובטבלת progress, ומתמזגת בכל כניסה ----
  var GKEY = 'freeai-guide-done';
  function localDone() { try { return JSON.parse(localStorage.getItem(GKEY)) || []; } catch (e) { return []; } }
  var synced = false;
  function syncProgress() {
    if (!user || synced) return;
    synced = true;
    SB.from('progress').select('item').then(function (r) {
      if (r.error) return;
      var server = {}, local = localDone(), all = local.slice(), missing = [];
      r.data.forEach(function (x) { var m = /^guide-(\d+)$/.exec(x.item); if (m) server[+m[1]] = 1; });
      Object.keys(server).forEach(function (n) { if (all.indexOf(+n) < 0) all.push(+n); });
      local.forEach(function (n) { if (!server[n]) missing.push({ item: 'guide-' + n }); });
      all.sort(function (a, b) { return a - b; });
      try { localStorage.setItem(GKEY, JSON.stringify(all)); } catch (e) {}
      if (missing.length) SB.from('progress').upsert(missing, { onConflict: 'user_id,item', ignoreDuplicates: true }).then(function () {});
      window.dispatchEvent(new Event('fa-progress'));
    });
  }
  // המדריך קורא לזה כשלוחצים "סיימתי". אם הדף עובר לפרק הבא לפני שזה נשמר, הסנכרון בדף הבא משלים.
  window.faMark = function (item) {
    if (user) SB.from('progress').upsert({ item: item }, { onConflict: 'user_id,item', ignoreDuplicates: true }).then(function () {});
  };

  // ---- כרטיס המשתמש בתפריט הצד של המדריך ----
  function renderSide() {
    var card = document.querySelector('.ds-profile');
    if (!card || !user || card.dataset.me) return;
    card.dataset.me = '1';
    var md = user.user_metadata || {};
    var name = md.full_name || md.name || (user.email || '').split('@')[0], pic = md.avatar_url || md.picture || '';
    var av = card.querySelector('.avatar'), b = card.querySelector('.who b');
    if (b) b.textContent = name;
    if (av && pic) {
      var img = el('img'); img.src = pic; img.alt = ''; img.referrerPolicy = 'no-referrer';
      img.onerror = function () { av.textContent = (name || '?').charAt(0); };
      av.textContent = ''; av.appendChild(img); av.classList.add('has-pic');
    }
    var out = el('button', 'ds-out', ic('<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>'));
    out.type = 'button'; out.title = 'התנתקות'; out.setAttribute('aria-label', 'התנתקות');
    out.addEventListener('click', signOut);
    card.appendChild(out);
  }
  function signOut() {
    try { localStorage.removeItem(GKEY); } catch (e) {}
    SB.auth.signOut().finally(function () { location.reload(); });
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
    me.querySelector('.ag-out').addEventListener('click', signOut);
  }

  SB.auth.onAuthStateChange(function (event, session) {
    if (event === 'SIGNED_OUT') { user = null; return; }
    if (session && !user) { user = session.user; setTimeout(unlock, 0); }
  });

  function start() {
    SB.auth.getSession().then(function (r) {
      var s = r.data && r.data.session;
      if (s) { user = s.user; unlock(); return; }
      // תצוגה מקדימה של העמוד בתוך דף הבית (iframe מאותו אתר) לא ננעלת
      var framed = false; try { framed = self !== top && top.location.host === location.host; } catch (e) {}
      if (CFG.locked && !framed) showGate();
      else document.documentElement.classList.remove('ag-lock');
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
