"""Free AI – העיצוב המצומצם. בונה את עמודי האתר מאפס, בלי התבנית הכבדה.

כרגע: דף הבית (index.html) והמדריך (guide-N.html).
הרצה: cd tools/site_build && python3 compact_site.py
"""
import re
from pathlib import Path
from clean_urls import clean

SITE = Path(__file__).resolve().parents[2] / "site"
CSS_VERSION = "55"
COUPON = "RVJ34jcn4j1"

NAV = [("index.html", "דף הבית"), ("course.html", "הקורס"), ("guide-1.html", "המדריך"), ("skills.html", "סקילים"), ("articles.html", "מאמרים")]

# שם הפרק, דקות קריאה
CHAPTERS = [
    ("לפני שמתחילים", 2), ("קלוד מול קלוד קוד", 3), ("פותחים חשבון קלוד", 4),
    ("מתקינים את האפליקציה", 5), ("פותחים GitHub", 4), ("מה זה ריפו ופותחים אחד", 5), ("היכרות ראשונה עם קלוד", 3), ("מיקום הפרויקט: מחשב או ענן", 3), ("בחירת המודל", 3), ("הרשאות: כמה קלוד עושה לבד", 3), ("כמה נשאר מהמנוי", 2), ("תוספות: איפה מוסיפים יכולות", 3), ("חיבור לשירותים (Connectors)", 3), ("מיומנויות (Skills)", 3), ("חבילות (Plugins)", 3), ("מתקינים סקיל ומשתמשים בו", 4), ("איך מדברים עם קלוד קוד", 4), ("חיבור GitHub לקלוד ובנייה ראשונה", 8), ("מעלים לאוויר", 5),
     ("Supabase", 3),
    ("סדר ובטיחות", 4), ("כשמשהו נתקע", 4), ("השלב הבא", 3),
]
READY = set(range(1, 24))  # פרקים שכבר כתובים


HERO_DEMO = '<div class="hero-stage"><div class="demo">\n<div class="chat"><div class="who">אתם כותבים:</div><div class="box"><span class="tx"></span><span class="cur"></span></div>\n<div class="who">קלוד קוד עושה:</div><div class="steps"><div><i>✓</i>בונה יומן תורים</div><div><i>✓</i>מוסיף טופס הזמנה ללקוחות</div><div><i>✓</i>מחבר תזכורות בוואטסאפ</div><div><i>✓</i>בונה מסך ניהול להזמנות</div></div></div>\n<div class="app">\n<div class="top p"><b>התורים שלי</b><span class="btn2">+ תור חדש</span></div>\n<div class="stats"><div class="st p"><small>תורים השבוע</small><strong data-n="38">0</strong></div><div class="st p"><small>הזמנות חדשות</small><strong data-n="7">0</strong></div><div class="st p"><small>הכנסות</small><strong data-n="4260" data-c="₪">0</strong></div></div>\n<div class="cal p"><div></div><div class="h">ראשון</div><div class="h">שני</div><div class="h">שלישי</div><div class="h">רביעי</div><div class="t">09:00</div><div class="ap ">נועה<span>תספורת</span></div><div class="slot"></div><div class="ap g">אבי<span>זקן</span></div><div class="slot"></div><div class="t">10:00</div><div class="slot"></div><div class="ap b">מיכל<span>פן</span></div><div class="slot"></div><div class="ap b">דנה<span>החלקה</span></div><div class="t">11:00</div><div class="ap g">רון<span>צבע</span></div><div class="ap" id="last">יוסי<span>תספורת</span></div><div class="slot"></div><div class="slot"></div><div class="t">12:00</div><div class="slot"></div><div class="slot"></div><div class="ap ">שירה<span>תספורת</span></div><div class="ap g">תמר<span>צבע</span></div><div class="t">13:00</div><div class="slot"></div><div class="slot"></div><div class="slot"></div><div class="slot"></div></div>\n<div class="toast"><i>✓</i>תור חדש נקבע: יוסי, שני 11:00</div>\n</div></div>\n<script>(function(){\nvar msg="תבנה לי מערכת לניהול הזמנות ותורים של העסק שלי";\nvar d=document.querySelector(\'.demo\'),chat=d.querySelector(\'.chat\'),tx=d.querySelector(\'.tx\'),st=d.querySelectorAll(\'.steps div\'),app=d.querySelector(\'.app\'),ps=app.querySelectorAll(\'.p\'),aps=app.querySelectorAll(\'.ap\'),nums=app.querySelectorAll(\'[data-n]\'),toast=app.querySelector(\'.toast\');\nvar T=[];function at(ms,f){T.push(setTimeout(f,ms))}\nfunction reset(){T.forEach(clearTimeout);T=[];tx.textContent=\'\';chat.classList.remove(\'out\');app.classList.remove(\'in\');st.forEach(function(s){s.classList.remove(\'on\')});aps.forEach(function(a){a.classList.remove(\'on\')});toast.classList.remove(\'on\');nums.forEach(function(n){n.textContent=\'0\'});ps.forEach(function(p){p.style.transitionDelay=\'\'})}\nfunction count(el){var N=+el.dataset.n,c=el.dataset.c||\'\',t0=performance.now();(function f(t){var k=Math.min(1,(t-t0)/1100);k=1-Math.pow(1-k,3);el.textContent=c+Math.round(N*k).toLocaleString(\'en-US\');if(k<1)requestAnimationFrame(f)})(t0)}\nfunction run(){reset();var k=0,step=50;\nfor(var i=1;i<=msg.length;i++)(function(i){at(i*step,function(){tx.textContent=msg.slice(0,i)})})(i);\nvar t=msg.length*step+500;\nst.forEach(function(s,n){at(t+n*650,function(){s.classList.add(\'on\')})});\nt+=st.length*650+700;\nat(t,function(){chat.classList.add(\'out\')});\nat(t+300,function(){ps.forEach(function(p,n){p.style.transitionDelay=(n*120)+\'ms\'});app.classList.add(\'in\')});\nat(t+800,function(){nums.forEach(count)});\nvar rest=[].filter.call(aps,function(a){return a.id!=\'last\'});rest.forEach(function(a,n){at(t+1000+n*170,function(){a.classList.add(\'on\')})});\nvar last=app.querySelector(\'#last\');\nat(t+1000+aps.length*170+700,function(){last.classList.add(\'on\');toast.classList.add(\'on\')});\nat(t+1000+aps.length*170+5200,run);}\nrun();})()</script></div>'


def _strings_svg():
    """קווי "חוטים" ירוקים לחלק הפתיחה: שני צרורות עקומות שזזים לאט (CSS)."""
    def bundle(n, f):
        return "".join(f'<path d="{f((i / (n - 1)) - .5)}"/>' for i in range(n))
    a = bundle(28, lambda t: f"M 560 {470 + 80 * t:.1f} C 860 {470 - 160 * t:.1f}, 1080 {330 + 60 * t:.1f}, 1500 {130 + 560 * t:.1f}")
    b = bundle(24, lambda t: f"M -60 {760 + 380 * t:.1f} C 240 {880 - 220 * t:.1f}, 460 {640 + 160 * t:.1f}, 700 {600 + 120 * t:.1f}")
    return ('<svg class="strings" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            '<defs><linearGradient id="sg-a" gradientUnits="userSpaceOnUse" x1="620" y1="0" x2="1500" y2="0">'
            '<stop offset="0" stop-color="#D43B2D" stop-opacity="0"/><stop offset=".45" stop-color="#F0A27F" stop-opacity=".75"/><stop offset="1" stop-color="#E6BB35" stop-opacity=".35"/></linearGradient>'
            '<linearGradient id="sg-b" gradientUnits="userSpaceOnUse" x1="-80" y1="0" x2="760" y2="0">'
            '<stop offset="0" stop-color="#D43B2D" stop-opacity=".25"/><stop offset=".6" stop-color="#F0A27F" stop-opacity=".7"/><stop offset="1" stop-color="#E6BB35" stop-opacity="0"/></linearGradient></defs>'
            f'<g class="s-a" fill="none" stroke="url(#sg-a)" stroke-width=".9">{a}</g>'
            f'<g class="s-b" fill="none" stroke="url(#sg-b)" stroke-width=".9">{b}</g></svg>')


STRINGS = _strings_svg()
(SITE / "assets/images/section/strings.svg").write_text(
    STRINGS.replace('<svg class="strings"', '<svg xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true" focusable="false"', '')
    .replace('</defs>', '</defs><style>g{transform-box:view-box;transform-origin:50% 50%}.s-a{animation:a 16s cubic-bezier(.77,0,.175,1) infinite alternate}.s-b{animation:b 20s cubic-bezier(.77,0,.175,1) infinite alternate}@keyframes a{to{transform:translate(-24px,-18px) rotate(-1.4deg)}}@keyframes b{to{transform:translate(20px,12px) rotate(1.2deg)}}@media (prefers-reduced-motion:reduce){g{animation:none!important}}</style>', 1))


def header(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="c-header">
            <a href="index.html" class="c-logo"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>
            <nav class="c-nav">{links}</nav>
            <a href="course.html" class="btn sm">התחל ללמוד</a>
            <button type="button" class="btn c-menu-btn" aria-label="תפריט" onclick="this.parentNode.classList.toggle('open')"><i class="icon icon-grip-lines-solid"></i></button>
        </header>'''


def burger(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<div class="gmenu" id="gmenu">
                <button type="button" class="btn" aria-label="תפריט" onclick="document.getElementById('gmenu').classList.toggle('open')"><i class="icon icon-grip-lines-solid"></i></button>
                <nav>{links}</nav>
            </div>'''


FOOTER = '''<footer class="c-foot">
            <span>© 2026 Free AI. כל הזכויות שמורות.</span>
            <nav><a href="privacy.html">פרטיות</a><a href="terms.html">תנאי שימוש</a><a href="accessibility">נגישות</a><a href="mailto:hello@free-ai.co.il">hello@free-ai.co.il</a></nav>
        </footer>'''


def page(title, desc, body, script="", cls="", css=""):
    return clean(_page(title, desc, body, script, cls, css))


def _page(title, desc, body, script="", cls="", css=""):
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="author" content="Free AI">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{desc}">
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-Regular.woff2?v=20261123" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-SemiBold.woff2?v=20261123" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-Bold.woff2?v=20261123" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="assets/fonts/fonts.css?v=20261119">
    <link rel="stylesheet" href="assets/icon/icomoon/style.css">
    <link rel="stylesheet" href="assets/css/tokens.css?v={CSS_VERSION}">
    <link rel="stylesheet" href="assets/css/compact.css?v={CSS_VERSION}">{f'''
    <link rel="stylesheet" href="assets/css/{css}?v={CSS_VERSION}">''' if css else ""}
    <link rel="shortcut icon" href="assets/images/logo/favicon.svg">
    <link rel="apple-touch-icon-precomposed" href="assets/images/logo/favicon.svg">
</head>
<body{(f' class="{cls}"' if cls else "")}>
{body}
{script}
<script src="assets/js/header.js?v=5" defer></script>
</body>
</html>
'''


# =====================================================================
# דף הבית
# =====================================================================
def build_home():
    import home_mint
    faq = "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
        ("צריך מנוי בתשלום לקלוד?", "כן. קלוד Pro ומעלה."),
        ("צריך ידע קודם?", "לא. מתחילים מאפס."),
        ("כמה זמן לוקח הקורס?", "8 שיעורים קצרים, בקצב שלכם."),
        ("למה צריך להירשם?", "כדי לצפות, להוריד קבצים ולקבל תעודה."),
        ("מה זה קלוד קוד?", 'כלי של Anthropic שבונה אתרים ומערכות לפי מה שכותבים לו. <a href="article-what-is-claude-code.html">הסבר פשוט על קלוד קוד</a>.'),
        ("קלוד קוד עובד בעברית?", "כן. כותבים לו בעברית רגילה, והוא בונה גם אתרים בעברית."),
    ])
    body = home_mint.body(header("index.html"), HERO_DEMO, STRINGS, CHAPTERS, READY, ARTICLES, f'<div class="faq">{faq}</div>')
    (SITE / "index.html").write_text(page(
        "קורס קלוד קוד בחינם בעברית | Free AI",
        "קורס קלוד קוד (Claude Code) בחינם ובעברית למתחילים, בלי ידע בתכנות: שיעורי וידאו, מדריך כתוב וסקילים מוכנים, עד אתר שעובד באוויר.", body,
        home_mint.HOME_JS, css="home.css"))
    print("index.html done")


# =====================================================================
# המדריך
# =====================================================================
GUIDE_JS = '''<script>
(function () {
    var KEY = 'freeai-guide-done', TOTAL = %(total)d, CURRENT = %(current)d;
    function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
    function save(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }
    var btn = document.getElementById('guide-done');
    function paint() {
        var done = load();
        document.querySelectorAll('.ch').forEach(function (el) { el.classList.toggle('is-done', done.indexOf(+el.dataset.ch) > -1); });
        document.getElementById('guide-fill').style.width = Math.round(done.length / TOTAL * 100) + '%%';
        document.getElementById('guide-count').textContent = done.length + ' מתוך ' + TOTAL + ' פרקים';
        var c2 = document.getElementById('guide-count-2'); if (c2) c2.textContent = 'סיימתם ' + done.length + ' מתוך ' + TOTAL + ' פרקים';
        if (btn && done.indexOf(CURRENT) > -1 && !btn.dataset.next) { btn.textContent = CURRENT === TOTAL ? 'סיימתם את המדריך ✓' : 'סיימתם ✓ הפרק הבא בקרוב'; btn.classList.add('is-done'); }
    }
    if (btn) btn.addEventListener('click', function () {
        var done = load();
        if (done.indexOf(CURRENT) < 0) { done.push(CURRENT); save(done); }
        if (window.faMark) window.faMark('guide-' + CURRENT);  // שומר גם בחשבון המשתמש (auth-gate.js)
        if (btn.dataset.next) location.href = btn.dataset.next; else paint();
    });
    var copy = document.getElementById('guide-copy');
    if (copy) copy.addEventListener('click', function () { navigator.clipboard.writeText(copy.dataset.code); copy.textContent = 'הועתק ✓'; });
    paint();
    window.addEventListener('fa-progress', paint);  // ההתקדמות מהחשבון הגיעה
    // תפריט הצד נשאר באותו מקום כשעוברים פרק
    var sc = document.querySelector('.ds-scroll');
    if (sc) {
        var y = null; try { y = sessionStorage.getItem('freeai-side-y'); } catch (e) {}
        if (y !== null) sc.scrollTop = +y;
        else { var on = sc.querySelector('.is-on'); if (on) on.scrollIntoView({block: 'center'}); }
        window.addEventListener('pagehide', function () { try { sessionStorage.setItem('freeai-side-y', sc.scrollTop); } catch (e) {} });
    }
    var tb = document.getElementById('theme-btn');
    if (tb) tb.addEventListener('click', function () {
        var d = !document.documentElement.classList.contains('dark');
        document.documentElement.classList.toggle('dark', d);
        try { localStorage.setItem('theme', d ? 'dark' : 'light'); } catch (e) {}
    });
    var mb = document.getElementById('top-menu-btn'), mp = document.getElementById('top-menu');
    function menu(open) { if (!mb) return; mp.hidden = !open; mb.setAttribute('aria-expanded', open); }
    if (mb) mb.addEventListener('click', function (e) { e.stopPropagation(); menu(mp.hidden); });
    document.addEventListener('click', function (e) { if (mp && !mp.hidden && !e.target.closest('.top-menu')) menu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { document.body.classList.remove('side-open'); menu(false); } });
    document.addEventListener('click', function (e) {
        var img = e.target.closest ? e.target.closest('.fshot img') : null;
        if (!img) return;
        var o = document.createElement('div'); o.className = 'lightbox';
        o.innerHTML = '<img src="' + img.src + '" alt="">'; o.onclick = function () { o.remove(); };
        document.body.appendChild(o);
    });
})();
    document.querySelectorAll('.split').forEach(function (sp) {
        var bar = sp.querySelector('.split-bar');
        function set(x) {
            var r = sp.getBoundingClientRect();
            var pct = Math.min(75, Math.max(25, (x - r.left) / r.width * 100));
            sp.style.setProperty('--img', pct + '%%');
        }
        bar.addEventListener('pointerdown', function (e) {
            e.preventDefault(); bar.setPointerCapture(e.pointerId); sp.classList.add('dragging');
            function mv(ev) { set(ev.clientX); }
            function up() { bar.removeEventListener('pointermove', mv); sp.classList.remove('dragging'); }
            bar.addEventListener('pointermove', mv); bar.addEventListener('pointerup', up, { once: true });
        });
    });
    document.addEventListener('click', function (e) {
        var v = e.target.closest && e.target.closest('video');
        if (!v) return;
        var box = v.parentNode;
        if (v.paused) { v.play(); box.classList.remove('paused'); } else { v.pause(); box.classList.add('paused'); }
    });
</script>'''


def _ico(paths, cls=""):
    return f'<svg class="ico{(" " + cls) if cls else ""}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


ICO = {  # Lucide
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2m-7.07-17.07 1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "play": '<circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4Z"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    "news": '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "lines": '<path d="M4 9h16M4 15h16"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "down": '<path d="M12 5v14m-6-6 6 6 6-6"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
}
SITE_LINKS = [("index.html", "דף הבית", "home"), ("course.html", "הקורס", "play"), ("guide-1.html", "המדריך", "book"), ("skills.html", "סקילים", "box"), ("articles.html", "מאמרים", "news")]

THEME_HEAD = """<script>(function(){var m='light';try{m=localStorage.getItem('theme')||'light'}catch(e){}if(window.self!==window.top)m='light';
var d=m==='dark'||(m==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.toggle('dark',d);})();</script>"""


def site_menu():
    links = "".join(f'<a href="{h}" class="menu-item{" on" if h == "guide-1.html" else ""}">{_ico(ICO[ic])}<span>{t}</span></a>' for h, t, ic in SITE_LINKS)
    return f'{links}<div class="menu-sep"></div><button type="button" class="menu-item theme-btn" id="theme-btn">{_ico(ICO["moon"], "i-moon")}{_ico(ICO["sun"], "i-sun")}<span class="t-dark">מצב כהה</span><span class="t-light">מצב בהיר</span></button>'


def sidebar(current):
    items = []
    for i, (name, _) in enumerate(CHAPTERS, 1):
        cls = "ch" + (" is-on" if i == current else "")
        inner = f'<span class="num">{i}</span><span class="nm">{name}</span>{_ico(ICO["check"], "dot")}'
        if i in READY:
            cur = ' aria-current="page"' if i == current else ""
            items.append(f'<li><a href="guide-{i}.html" class="{cls}" data-ch="{i}"{cur}>{inner}</a></li>')
        else:
            items.append(f'<li><span class="{cls} is-soon" data-ch="{i}">{inner}</span></li>')
    return f'''<aside class="ds-side" id="ds-side">
            <a href="index.html" class="ds-brand"><img src="assets/images/logo/favicon.svg" alt="" width="24" height="24"><span>Free AI</span></a>
            <div class="ds-scroll">
                <div class="ds-group">
                    <div class="ds-group-title">המדריך לקלוד קוד</div>
                    <div class="ds-prog"><div class="bar"><i id="guide-fill"></i></div><span class="count" id="guide-count"></span></div>
                    <ol class="chs">{"".join(items)}</ol>
                </div>
            </div>
            <div class="ds-profile"><span class="avatar">{_ico(ICO["user"])}</span><span class="who"><b>אורח</b><small id="guide-count-2"></small></span></div>
        </aside>'''


def rows_html(rows):
    """שורות ממוספרות. כל (None, "כותרת") פותח קבוצה חדשה: הכותרת יושבת מעל הכרטיס, עם מעוין קטן."""
    if not rows:
        return ""
    groups, cur = [], [None, []]
    for a, b in rows:
        if a is None:
            if cur[1] or cur[0]:
                groups.append(cur)
            cur = [b, []]
        else:
            cur[1].append((a, b))
    groups.append(cur)
    out = []
    for title, items in groups:
        li = "".join(f'<li class="row"><span class="tile">{k}</span>{a}<small>{b}</small></li>' for k, (a, b) in enumerate(items, 1))
        ol = f'<ol class="rows">{li}</ol>'
        out.append(f'<section class="sec"><div class="card-head"><h3>{title}</h3></div>{ol}</section>' if title else ol)
    return "".join(out) if len(out) == 1 else f'<div class="rows-stack">{"".join(out)}</div>'


def tip(text):
    return f'<div class="tipcard">{_ico(ICO["info"])}<b>טיפ</b><span>{text}</span></div>'


def split(img, alt, rows):
    """תמונה ולידה ההסברים, עם קו באמצע שאפשר לגרור ימינה ושמאלה."""
    return f'''<div class="split">{rows_html(rows)}<div class="split-bar" role="separator" aria-label="גרירה לשינוי הגודל" tabindex="0"></div><div class="fshot map"><img src="{img}" alt="{alt}"></div></div>'''


GUIDE_TITLE = {  # כותרת לגוגל לפי מה שאנשים מחפשים (השם בעמוד נשאר כמו שהוא)
    2: "מה ההבדל בין קלוד לקלוד קוד? מתי משתמשים בכל אחד",  # "מה זה קלוד קוד" שייך למאמר
    4: "התקנת קלוד קוד והורדה למחשב (Windows ו-Mac)",
    5: "מה זה GitHub ואיך פותחים חשבון – מדריך למתחילים",
    14: "סקילים בקלוד (Claude Skills): מה זה ואיך משתמשים",
    16: "איך מתקינים סקיל בקלוד ומשתמשים בו – צעד אחרי צעד",
    17: "איך כותבים פרומפט לקלוד קוד – בלי מילים טכניות",
}

GUIDE_DESC = {
    5: "פותחים חשבון GitHub בחינם, צעד אחרי צעד. זה המקום שבו נשמרים כל הפרויקטים שקלוד קוד בונה.",
    6: "מה זה ריפו (Repo) ב-GitHub, למה כל פרויקט צריך אחד, ואיך פותחים ריפו ראשון בכמה לחיצות.",
}


GUIDE_PAGE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="author" content="Free AI">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{desc}">
    {theme}
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@100..900&family=Noto+Sans:wght@100..900&family=JetBrains+Mono:wght@400;500&display=swap">
    <link rel="stylesheet" href="assets/css/guide.css?v={v}">
    <link rel="shortcut icon" href="assets/images/logo/favicon.svg">
    <link rel="apple-touch-icon-precomposed" href="assets/images/logo/favicon.svg">
</head>
<body class="guide-page">
{body}
{script}
</body>
</html>
"""


def build_chapter(n, lead, rows, note, extra="", flow="", top=""):
    name, mins = CHAPTERS[n - 1]
    rows_block = rows_html(rows)
    nxt = f' data-next="guide-{n + 1}"' if (n + 1) in READY else ""
    last = n == len(CHAPTERS)
    if last:
        nxt = ' data-next="course.html"'
    body = f'''<div class="ds-app">
        {sidebar(n)}
        <div class="ds-overlay" onclick="document.body.classList.remove('side-open')"></div>
        <div class="ds-main">
            <header class="ds-top has-head">
                <button type="button" class="icon-btn ds-burger" aria-label="תפריט" onclick="document.body.classList.toggle('side-open')">{_ico(ICO["menu"])}</button>
                <span class="ds-vsep"></span>
                <div class="page-head"><h1>{name}</h1>{f'<span class="hsep" aria-hidden="true"></span><p class="lead">{lead}</p>' if lead else ''}</div>
                <div class="ds-actions top-menu"><button type="button" class="icon-btn" id="top-menu-btn" aria-label="תפריט האתר" aria-expanded="false" aria-controls="top-menu">{_ico(ICO["lines"])}</button>
                    <div class="menu-pop" id="top-menu" hidden>{site_menu()}</div></div>
            </header>
            <main class="ds-content">
                <article class="lesson">
                    {top}{rows_block}{flow}{extra}
                    <div class="lesson-end"><span>{note}</span><div class="end-btns">{f'<a href="guide-{n - 1}.html" class="btn btn-2">→ הפרק הקודם</a>' if n > 1 else ''}<button type="button" class="btn btn-primary" id="guide-done"{nxt}>{"מעבר לקורס הפרקטי ←" if last else "סיימתי, לפרק הבא ←"}</button></div></div>
                </article>
                {FOOTER}
            </main>
        </div>
    </div>'''
    html = clean(GUIDE_PAGE.format(
        title=f"{GUIDE_TITLE.get(n, name + ' – המדריך לקלוד קוד')} | Free AI",
        desc=f"פרק {n} במדריך לקלוד קוד למי שלא מתכנת: {lead or GUIDE_DESC.get(n, name)}",
        theme=THEME_HEAD, v=CSS_VERSION, body=body,
        script=GUIDE_JS % {"total": len(CHAPTERS), "current": n}))
    (SITE / f"guide-{n}.html").write_text(html)
    print(f"guide-{n}.html done")


build_chapter(
    1, "שלושה דברים להכין, ואפשר לצאת לדרך.",
    [("מחשב", "Mac או Windows"), ("מייל", "אחד לכל השירותים"), ("כרטיס אשראי", "כ-20 דולר לחודש לקלוד")],
    "כל השאר בחינם להתחלה",
    extra=f'''
                <p class="more-link">לא בטוחים מה זה בכלל? <a href="article-what-is-claude-code.html">מה זה קלוד קוד, בהסבר פשוט</a></p>''',
)


def flow(steps):
    """תרשים זרימה: כל שלב = טקסט + צילום מסך. אם הקובץ עוד לא קיים, מוצג מקום ריק."""
    out = []
    for i, (title, text, img) in enumerate(steps, 1):
        if img.endswith(".mp4") and (SITE / "assets/images/guide" / img).exists():
            import hashlib
            ver = hashlib.md5((SITE / "assets/images/guide" / img).read_bytes()).hexdigest()[:8]
            shot = f'<div class="fshot"><video src="assets/images/guide/{img}?v={ver}" muted loop playsinline autoplay preload="metadata" aria-label="{title}"></video></div>'
        elif (SITE / "assets/images/guide" / img).exists():
            shot = f'<div class="fshot"><img src="assets/images/guide/{img}" alt="{title}" loading="lazy"></div>'
        else:
            shot = '<div class="fshot empty"><span>צילום מסך יתווסף כאן</span></div>'
        tile = f'<span class="tile">{i}</span>' if len(steps) > 1 else ''
        out.append(f'''<li class="fstep"><div class="ftext">{tile}<div><h3>{title}</h3><p>{text}</p></div></div>{shot}</li>''')
        if i < len(steps):
            out.append('<li class="farrow" aria-hidden="true">↓</li>')
    return f'\n                <ol class="flow">{"".join(out)}</ol>'


def fullvid(src, alt):
    return f'\n                <div class="fvid"><span>ככה זה נראה, מההתחלה ועד הסוף. לחיצה עוצרת, לחיצה נוספת ממשיכה.</span><video src="{src}" muted loop playsinline autoplay preload="metadata" aria-label="{alt}"></video></div>'


def gtable(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'\n                <div class="gtbl-wrap"><table class="gtbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def when(left, right):
    def col(title, items):
        li = "".join(f"<li>{x}</li>" for x in items)
        return f'<div class="when-col"><h3>{title}</h3><ul>{li}</ul></div>'
    return f'\n                <div class="when">{col(*right)}{col(*left)}</div>'


build_chapter(
    2, "לאותה חברה יש שני כלים. אחד כמו יועץ שעונה לכם, השני כמו בעל מקצוע שבא ובונה.",
    [("קלוד: שיחה", "שואלים ומקבלים תשובה, רעיון או טקסט. הוא לא נוגע בקבצים"),
     ("קלוד קוד: בנייה", "עובד בעצמו על הקבצים של הפרויקט ובונה אתר או מערכת"),
     ("מה אנחנו בוחרים", "קלוד קוד, כי במדריך הזה בונים")],
    "שניהם כלולים באותו מנוי",
    extra=when(("משתמשים בקלוד כש…", ["כותבים מייל או פוסט", "מנתחים מסמך", "מחפשים רעיון או עצה"]),
               ("משתמשים בקלוד קוד כש…", ["בונים אתר", "משנים ומתקנים אתר קיים", "מעלים אותו לאוויר"]))
          + '\n                <p class="more-link">רוצים את התמונה המלאה? <a href="article-what-is-claude-code.html">מה זה קלוד קוד, בהסבר פשוט</a></p>',
)


build_chapter(
    3, "החשבון הוא המפתח שלכם לקלוד. פותחים אותו פעם אחת.", [],
    "אם משהו נראה אחרת אצלכם, זה בסדר",
    flow=flow([
        ("נכנסים לאתר", 'בדפדפן נכנסים ל-<a href="https://claude.ai" target="_blank" rel="noopener">claude.ai</a>.', "claude-signup-1.png"),
        ("בוחרים איך נרשמים", "ממשיכים עם Google, או כותבים מייל. עם Google מדלגים על הצעד הבא.", "claude-signup-2.png"),
        ("מקלידים את הקוד מהמייל", "קלוד שולח קוד למייל. מעתיקים אותו וכותבים בחלון.", "claude-signup-3.png"),
        ("כותבים שם ומאשרים", 'כותבים את השם שלכם ומאשרים את התנאים.<small class="fnote">יכול להיות שיהיו עוד כמה שאלות, פשוט תזרמו עם זה.</small>', "claude-signup-4.png"),
        ("בוחרים מסלול", 'בשביל לעבוד עם קלוד קוד, חייבים את המנוי בתשלום. לפחות Pro, 20 דולר בחודש.<small class="fnote">בוחרים מנוי חודשי, לא שנתי.</small>', "claude-signup-5.png"),
        ("הגעתם!", "רואים את מסך הצ'אט. החשבון מוכן.", "claude-signup-6.png"),
    ]),
)


build_chapter(
    4, "באפליקציה הזאת עובדים עם קלוד קוד. מורידים, מתקינים ונכנסים.", [],
    "אם משהו נראה אחרת אצלכם, זה בסדר",
    flow=flow([
        ("נכנסים לדף ההורדה", 'בדפדפן נכנסים ל-<a href="https://claude.com/download" target="_blank" rel="noopener">claude.com/download</a>.', "claude-install-1.png"),
        ("מורידים לפי המחשב", "לוחצים על Mac או על Windows. הקובץ יורד לבד.", "claude-install-2.png"),
        ("פותחים את הקובץ", "לוחצים עליו פעמיים ומאשרים התקנה.", "claude-install-3.png"),
        ("נכנסים לחשבון", "פותחים את קלוד ומתחברים עם אותו מייל מהפרק הקודם.", "claude-install-4.png"),
        ("לוחצים על Code", "למעלה בוחרים בלשונית Code. זה המקום שבו בונים.", "claude-install-5.png"),
    ]),
)


build_chapter(
    5, "",
    [("מה זה GitHub", "כמו Google Drive, רק לפרויקטים של קוד: שם שמורים כל הקבצים, התיקיות ובקיצור כל הקוד של האתר"),
     ("למה צריך אותו", "קלוד קוד לוקח משם את הפרויקט, עובד עליו ושומר בחזרה"),
     ("מחיר", "חשבון חינמי מספיק")],
    "בשיעור הבא נלמד איך פותחים פרויקט חדש (ריפו)",
    top='<h2 class="lesson-intro">עד עכשיו הבנו ופתחנו משתמש בקלוד. עכשיו פותחים משתמש ב-GitHub</h2>',
    flow=flow([
        ("נכנסים ולוחצים על Sign up", 'בדפדפן נכנסים ל-<a href="https://github.com" target="_blank" rel="noopener">github.com</a> ולוחצים למעלה על Sign up.', "github-1.mp4"),
        ("ממשיכים עם Google (מומלץ)", 'לוחצים על Continue with Google. כך לא צריך סיסמה חדשה.', "github-2.mp4"),
        ("בוחרים את חשבון Google", 'בוחרים את המייל שלכם מהרשימה.', "github-3.mp4"),
        ("הגעתם!", 'רואים את הדף הראשי של GitHub. החשבון מוכן.', "github-4.mp4"),
    ]),
    extra=fullvid("assets/images/guide/github-signup.mp4", "הרשמה ל-GitHub מההתחלה ועד הסוף"),
)


build_chapter(
    6, "",
    [("ריפו (Repo) ב-GitHub", "אפשר פשוט לקרוא לזה פרויקט. זאת בעצם תיקייה אחת ששמור בה כל הקוד של האתר"),
     ("היסטוריה", "הריפו זוכר כל שינוי, אז תמיד אפשר לחזור אחורה"),
     ("ריפו אחד לכל פרויקט", "לא מערבבים פרויקטים באותו ריפו"),
     (None, "דוגמאות"),
     ("אתר תדמית לנגר", "ריפו 1, בשם: carpenter-website"),
     ("מערכת ניהול לקוחות לסלון לק ג'ל", "ריפו 2, בשם: nail-salon-crm")],
    "זה הכול ב-GitHub. חוזרים לקלוד, ובהמשך נחבר את קלוד ו-GitHub ביחד",
    flow=flow([
        ("לוחצים על New repository", 'ב-<a href="https://github.com/new" target="_blank" rel="noopener">GitHub</a> לוחצים על הכפתור הירוק New repository.', "github-repo-1.mp4"),
        ("נותנים שם לריפו", "שם באנגלית, בלי רווחים. למשל new-website-carpenter.", "github-repo-2.mp4"),
        ("בוחרים Private", 'Private אומר שרק אתם רואים אותו.<small class="fnote">אפשר תמיד לשנות אחר כך.</small>', "github-repo-3.mp4"),
        ("לוחצים Create repository", "הריפו נוצר. הוא ריק בינתיים, וקלוד קוד ימלא אותו.", "github-repo-4.mp4"),
    ]),
    extra=fullvid("assets/images/guide/github-repo.mp4", "פתיחת ריפו מההתחלה ועד הסוף"),
)


build_chapter(
    7, "לפני שבונים, מכירים את המסך. כל מספר בתמונה מוסבר ליד.", [],
    "בפרקים הבאים מכירים כל אחד מהם לעומק",
    top=split("assets/images/guide/claude-map.png", "המסך של קלוד קוד עם מספרים", [
     ("מצב בנייה", "הלשונית Code. כאן קלוד בונה. בלשונית קלוד (Claude) רק משוחחים"),
     ("משימה חדשה", "הכפתור New. מתחיל שיחה חדשה מאפס"),
     ("תיבת הכתיבה", "כאן כותבים מה רוצים שקלוד יעשה, בעברית רגילה"),
     ("מיקום הפרויקט", "איפה קלוד עובד: על המחשב שלכם או בענן"),
     ("בחירת הפרויקט", "הכפתור Repo. על איזו תיקייה ב-GitHub עובדים"),
     ("בחירת המודל", "איזה מוח עושה את העבודה, למשל Opus 5.5"),
     ("הרשאות", "כמה קלוד עושה לבד בלי לשאול, למשל Auto"),
     ("מצב המנוי", "העיגול הקטן. כמה נשאר לכם מהמנוי")]),
)


build_chapter(
    8, "איפה הפרויקט שלכם נמצא, ואיפה קלוד עובד עליו.",
    [("על המחשב שלכם (Local)", "הפרויקט יושב רק אצלכם. כשהמחשב כבוי, אי אפשר לעבוד עליו"),
     ("בענן (Cloud)", "הפרויקט יושב באינטרנט. נכנסים אליו מכל מחשב ומהטלפון"),
     ("מה אנחנו בוחרים", "ענן. עובדים מכל מקום ולא צריך להתקין כלום")],
    "רואים ציור של ענן למטה? אתם במקום הנכון",
    flow=flow([
        ("איך יודעים שאתם בענן", "למטה משמאל מופיע ציור של ענן.", "claude-code-cloud.png"),
        ("איך יודעים שאתם על המחשב", 'למטה כתוב This computer. לוחצים עליו ובוחרים ענן.', "claude-code-local.png"),
    ]),
)


build_chapter(
    9, "המודל הוא המוח שעושה את העבודה. בוחרים מוח לפי גודל המשימה.",
    [("Fable: הכי חזק שיש", "לבעיות הכי קשות. איטי יותר וצורך הכי הרבה מהמנוי"),
     ("Opus: חכם מאוד", "לבנייה של דברים גדולים. צורך הרבה מהמנוי"),
     ("Sonnet: חכם ומהיר", "לרוב העבודה היומיומית. חוסך במנוי"),
     ("Haiku: הכי מהיר", "למשימות קטנות ופשוטות. כמעט לא צורך מהמנוי"),
     ("Effort: זמן חשיבה", "כמה זמן המוח חושב לפני שהוא עונה. יותר זמן = יותר מדויק ויותר צריכה"),
     ("מה אנחנו בוחרים", "תלוי במשימה: ככל שהיא גדולה וקשה יותר, בוחרים מוח חזק יותר"),
     (None, "דוגמאות"),
     ("לתקן מילה או צבע באתר", "Haiku"),
     ("להוסיף עמוד או לשנות עיצוב", "Sonnet"),
     ("לבנות אתר שלם או מערכת", "Opus"),
     ("משהו מסובך ש-Opus נתקע בו", "Fable")],
    "אפשר להחליף מודל בכל רגע",
    flow=flow([
        ("איפה מחליפים", "לוחצים על שם המודל למטה מימין, ובוחרים מהרשימה.", "claude-models.png"),
    ]),
)


build_chapter(
    10, "לפני כל פעולה קלוד יכול לשאול אתכם, או פשוט לעשות. כאן קובעים את זה.",
    [("Auto: מחליט לבד", "עושה את רוב הדברים לבד, ושואל רק כשמשהו חשוב"),
     ("Accept edits: עריכת קבצים בלי לשאול", "משנה קבצים לבד, ושואל לפני כל דבר אחר"),
     ("Plan: קודם תוכנית", "מספר מה הוא מתכנן, ובונה רק אחרי שאישרתם"),
     ("מה אנחנו בוחרים", "Auto. כשרוצים לראות קודם מה הוא יעשה, Plan")],
    "אפשר להחליף בכל רגע",
    flow=flow([
        ("איפה מחליפים", "לוחצים על Auto למטה, ובוחרים מהרשימה.", "claude-permissions.png"),
    ]),
)


build_chapter(
    11, "המנוי נותן כמות עבודה מוגבלת, כמו חבילת גלישה. והיא מתמלאת מחדש.",
    [("מגבלת 5 שעות", "כמות עבודה ל-5 שעות, שמתחילות מההודעה הראשונה"),
     ("מגבלה שבועית", "כמות לכל השבוע. מתאפסת פעם בשבוע"),
     ("נגמר?", "מחכים לאיפוס, או עוברים למודל שמשתמש פחות, כמו Sonnet")],
    "שווה להציץ מדי פעם",
    flow=flow([
        ("איפה רואים", "לוחצים על העיגול הקטן בפינה למטה. רואים כמה כבר נוצל.", "claude-usage.png"),
    ]),
    extra='\n                <p class="more-link">רוצים יותר עבודה בחודש? <a href="article-claude-code-price.html">כמה עולה קלוד קוד, וכל המנויים</a></p>',
)


build_chapter(
    12, "דרך ההגדרות של קלוד תוכלו להוסיף יכולות חדשות, לחבר כלים חיצוניים ולהתקין תוספים.", [
     (None, "שלושה סוגי תוספות"),
     ("חיבורים (Connectors)", "מחברים את קלוד לכלים ואתרים חיצוניים, כמו Gmail ו-GitHub"),
     ("מיומנויות (Skills)", "נותנים לקלוד יכולות של מומחים, למשל לנהל לכם את הקמפיינים"),
     ("חבילות (Plugins)", "כמה תוספות יחד בהתקנה אחת")],
    "בפרקים הבאים מכירים כל סוג לעומק",
    top=split("assets/images/guide/settings-map.png", "מסך ההגדרות עם מספרים וחצים", [
     ("ההגדרות", "גלגל השיניים למטה, ליד השם שלכם"),
     ("התאמה אישית", "בתפריט בוחרים Customize"),
     ("סוג התוספת", "למעלה בוחרים: Connectors, Skills או Plugins"),
     ("שלי או חדשות", "Yours: מה שכבר הוספתם. Discover: החנות, שם מוצאים חדשות")]),
)


build_chapter(
    13, "חיבור הוא כמו לתת לקלוד מפתח לחשבון שלכם בשירות אחר, כדי שיעבוד שם בשבילכם.",
    [("מה זה נותן", "קלוד פועל בעצמו בשירות: שומר קוד, קורא מיילים, מעדכן נתונים"),
     ("מה זה דורש", "מתחברים פעם אחת עם החשבון שלכם בשירות ומאשרים"),
     ("חיבור רשמי", "כל החיבורים הרשמיים של קלוד נמצאים בלשונית Discover"),
     ("חיבור שלא מופיע", "כלי חיצוני שאין לו חיבור רשמי מוסיפים בכפתור Add בצד"),
     (None, "דוגמאות"),
     ("GitHub", "קלוד שומר שם את הקוד של האתר"),
     ("Gmail", "קלוד קורא מיילים וכותב טיוטות"),
     ("Facebook", "קלוד מנהל ובודק את הקמפיינים הממומנים שלכם")],
    "אפשר לנתק חיבור בכל רגע",
    flow=flow([
        ("איפה רואים ומוסיפים", 'בלשונית Connectors, תחת Yours, רואים מה כבר מחובר. בלשונית Discover מוסיפים קונקטורים חדשים.<small class="fnote">כתוב Reconnect? החיבור התנתק. לוחצים ומתחברים שוב.</small>', "settings-connectors.png"),
    ]),
)


build_chapter(
    14, "מיומנות (Skill) היא כמו מדריך עבודה של מומחה: הוראות כתובות שמלמדות את קלוד לעשות משימה מסוימת בדיוק כמו שמומחה היה עושה אותה.",
    [("מה זה נותן", "קלוד עובד בשיטה קבועה ומוכחת, ולא צריך להסביר לו מחדש כל פעם איך עושים את זה"),
     ("איך זה מופעל", "קלוד משתמש בה לבד כשהיא מתאימה, או שכותבים / ובוחרים את המיומנות המתאימה"),
     ("במה זה שונה מחיבור", "מיומנות היא רק ידע. היא לא נכנסת לשום חשבון שלכם"),
     ("מיומנויות של Anthropic", "מוכנות בלשונית Discover. לוחצים + והן נוספות"),
     ("מיומנויות מאתרים אחרים", "הורדתם מיומנות מאתר אחר? לוחצים על הכפתור הלבן Add ומעלים אותה"),
     (None, "דוגמאות"),
     ("עיצוב אתרים", "קלוד מעצב לפי כללים של מעצבים מקצועיים"),
     ("כתיבה בעברית", "טקסטים שיווקיים בעברית טובה ונכונה"),
     ("קמפיינים בפייסבוק", "קלוד מנהל קמפיינים כמו קמפיינר מומחה")],
    "אפשר להסיר מיומנות בכל רגע",
    flow=flow([
        ("איפה מוסיפים", "בלשונית Skills, תחת Discover, או בכפתור Add.", "settings-skills.png"),
        ("איך מפעילים בשם", "כותבים / ואת השם שלה בתיבת הכתיבה.", "skill-slash.png"),
    ]),
)


build_chapter(
    15, "חבילה היא כמו ארגז כלים: בהתקנה אחת מקבלים כמה מיומנויות, חיבורים ופקודות שעובדים יחד.",
    [("מה זה נותן", "תחום שלם מוכן לעבודה, בלי להרכיב לבד חלק אחרי חלק"),
     ("על מה לשים לב", "מתקינים רק ממקור מוכר. ליד כל חבילה כתוב מי יצר אותה, כמו by Anthropic"),
     (None, "דוגמאות"),
     ("Marketing", "כותב פוסטים ומיילים ללקוחות, ומתכנן קמפיין לפי העסק שלכם"),
     ("Customer Support", "עונה לפניות של לקוחות ומסדר שאלות נפוצות לאתר")],
    "אפשר להסיר חבילה בכל רגע",
    flow=flow([
        ("איפה מוסיפים", "בלשונית Plugins, תחת Discover, לוחצים על + או על Add.", "settings-plugins.png"),
    ]),
)


build_chapter(
    16, "סקיל הוא המיומנות מפרק 14. ככה מורידים אחד מהאתר, מתקינים אותו בקלוד ומפעילים אותו על האתר שלכם.",
    [("הסקיל בסרטון", "בדיקת מהירות לאתר: בודק כמה מהר האתר נטען ומתקן את מה שמאט אותו"),
     ("מאיפה מורידים", "מעמוד הסקיל באתר שלנו, בקובץ ZIP אחד"),
     ("איפה מתקינים", "באפליקציה של קלוד, בכפתור Add שבעמוד Plugins"),
     ("על מה מפעילים", "על הריפו של האתר שלכם, בבקשה רגילה בעברית"),
     ("מה מקבלים", "קלוד בודק, מתקן, מודד שוב ומסביר מה השתנה"),
     ("כמה זמן", "ההתקנה פחות מדקה. העבודה של קלוד כעשר דקות")],
    "מתקינים פעם אחת, והסקיל זמין בכל משימה",
    extra=tip("רוצים סקיל מסוים בשם? כותבים / בתיבת הכתיבה ובוחרים אותו מהרשימה.")
     + '\n                <p class="more-link">סקילים מוכנים בחינם ובעברית: <a href="skills.html">כל הסקילים שלנו</a></p>',
    flow=flow([
        ("מורידים את הסקיל", 'נכנסים לעמוד של הסקיל, למשל <a href="skill-site-speed.html">בדיקת מהירות לאתר</a>, ולוחצים "הורדה חינם (ZIP)". מתקבל קובץ אחד בתיקיית ההורדות, ולא צריך לפתוח אותו.', "skilluse-1.mp4"),
        ("מגיעים למקום ההוספה", 'באפליקציה של קלוד לוחצים על השם שלכם למטה בצד, ובתפריט בוחרים Settings. בהגדרות לוחצים Plugins, עוברים ללשונית Skills ולוחצים Browse plugins. בעמוד שנפתח לוחצים Add למעלה, ואז Upload plugin.', "skilluse-2.mp4"),
        ("מעלים את הקובץ", 'לוחצים browse, בוחרים את קובץ ה-ZIP שהורדתם ולוחצים Upload.<small class="fnote">כשקופצת ההודעה "is added", הסקיל מותקן.</small>', "skilluse-3.mp4"),
        ("פותחים משימה ומבקשים", 'לוחצים New, בודקים שלמטה נבחר הריפו של האתר, וכותבים בעברית מה רוצים. אצלנו: "תבדוק את מהירות האתר שלי ואם אפשר לשפר אותו".', "skilluse-4.mp4"),
        ("קלוד עובד עם הסקיל", 'קלוד מפעיל את הסקיל לבד, בודק את האתר, מתקן ומודד שוב. זה לקח כעשר דקות. בסוף הוא כותב בעברית מה השתנה.<small class="fnote">אצלנו דף הבית בטלפון עלה מציון 45 ל-72, ונטען ב-2.2 שניות במקום 7.6.</small>', "skilluse-5.mp4"),
    ]),
)


build_chapter(
    17, "ככל שמסבירים לקלוד ברור יותר, מקבלים משהו קרוב יותר למה שרציתם.",
    [(None, "דוגמאות"),
     ("בקשה חלשה", "\"תבנה לי אתר\""),
     ("בקשה טובה", "\"תבנה דף נחיתה לנגר. בראש תמונות עבודות וכותרת, אחריהן השירותים: פרגולות, גדרות ושולחנות. בסוף טופס יצירת קשר. צבעים חמים של עץ.\"")],
    "לא צריך מילים טכניות. מסבירים כמו לבן אדם",
    top=rows_html([("מה בונים", "סוג הדבר: דף נחיתה, אתר תדמית, מערכת לניהול לקוחות"),
     ("בשביל מי", "העסק, מה הוא עושה ומי הלקוחות שלו"),
     ("מה צריך להופיע", "שירותים, תמונות, טלפון, טופס יצירת קשר"),
     ("איך זה נראה", "צבעים, סגנון ותחושה, למשל חם, נקי, יוקרתי")])
     + tip("אפשר לדבר במקום להקליד: לוחצים על המיקרופון בתיבת הכתיבה ומדברים בעברית.")
     + tip("אחרי הבנייה הראשונה מבקשים כמה שינויים בהודעה אחת, וחוסכים במנוי. רק שיהיו קשורים, למשל כמה תיקונים באותו עמוד."),
)


build_chapter(
    18, "מחברים את הריפו לקלוד, ובונים בו את האתר הראשון.",
    [("חיבור GitHub", "פעם אחת. קלוד מקבל אישור להיכנס לחשבון שלכם"),
     ("בחירת הריפו", "בכל משימה בוחרים על איזה פרויקט עובדים"),
     ("הבנייה", "קלוד בונה את האתר ושומר אותו בריפו")],
    "בפרק הבא מעלים את האתר לאוויר",
    extra=tip("רוצים ריפו חדש? אומרים לקלוד: \"תפתח ריפו חדש לפרויקט חדש\"."),
    flow=flow([
        ("מחברים את GitHub כקונקטור", "בהגדרות: Customize ← Connectors ← Discover ← מחפשים GitHub. לוחצים Connect ומאשרים בדפדפן.", "first-1.mp4"),
        ("נותנים לקלוד גישה לריפו", 'לוחצים Fix ומאשרים בכל חלון שקופץ.<small class="fnote">אם מבקשים קוד, הוא נשלח למייל שלכם.</small>', "first-2.mp4"),
        ("בוחרים את הריפו", 'לוחצים Repo ובוחרים את הריפו שלכם. וזהו. מעכשיו ה-GitHub שלכם מחובר לקלוד.<small class="fnote">מעכשיו לא צריך לעשות יותר כלום באתר של GitHub, קלוד עושה הכול בשבילכם. בכל פרויקט שבונים, בוחרים את הריפו שלו.</small>', "first-3.mp4"),
        ("מבקשים מה לבנות", "כותבים מה רוצים ושולחים. קלוד בונה.", "first-4.mp4"),
    ]),
)


build_chapter(
    19, "כדי שכל אחד יוכל להיכנס לאתר, מחברים את הפרויקט ל-4CODE.",
    [("מה זה 4CODE", "שרת. כדי שכולם יוכלו להיכנס למערכת שבניתם, מעלים אותה לשרת מאובטח באינטרנט")],
    "מעכשיו האתר באוויר, וכל שינוי עולה לבד",
    extra=f'''
                <div class="coupon">קופון לחודש ראשון בחינם ב-4CODE: <code>{COUPON}</code><button type="button" class="btn-2 sm" id="guide-copy" data-code="{COUPON}">העתקה</button></div>''',
    flow=flow([
        ("בוחרים מסלול", 'ב-<a href="https://4code.co.il/pricing" target="_blank" rel="noopener">4code.co.il</a> לוחצים על מסלולים ובוחרים מסלול.', "4code-1.mp4"),
        ("ממלאים את הפרטים שלכם", "ממלאים את הטופס, מאשרים, ונכנסים ללוח הבקרה של 4CODE.", "4code-details.mp4"),
        ("יוצרים פרויקט", "בתפריט הצד בוחרים בפרויקטים, ואז \"יצירת פרויקט חדש\". נותנים שם ונכנסים אליו.", "4code-3.mp4"),
        ("בוחרים את פרויקט ה-GitHub שלכם", 'לוחצים על GitHub, בוחרים את הריפו מפרק 18 ומאשרים.<small class="fnote">מחברים את הפרויקט פעם אחת ל-4CODE, וזהו. הכול מתעדכן לבד.</small>', "4code-4.mp4"),
        ("בוחרים את הריפו ומפרסמים", 'בוחרים את הריפו שלכם ולוחצים "פריסה". 4CODE מעלה את האתר לבד.<small class="fnote">כשרואים "פועל" בירוק, האתר באוויר.</small>', "4code-repo.mp4"),
        ("מקבלים כתובת בחינם", 'האתר מקבל כתובת חינמית מ-4CODE (סאב-דומיין). מוצאים אותה תחת דומיין.<small class="fnote">ככה לא חייבים לקנות דומיין בהתחלה.</small>', "4code-domain.png"),
    ]),
)


build_chapter(
    20, "דאטה בייס (מסד נתונים)",
    [("דאטה בייס", "המקום שבו האתר שומר מידע. אם המערכת שלכם צריכה לנהל משתמשים, הזמנות, תורים, תשלומים או הודעות מטפסים, צריך דאטה בייס"),
     ("Supabase", "החברה שמחזיקה את הדאטה בייס בשבילכם. קלוד יודע לחבר אותו לאתר"),
     ("מה אנחנו בוחרים", "מתחילים בלי. כשצריך, מבקשים מקלוד לחבר Supabase והוא מסביר מה לעשות")],
    "Supabase חינמי להתחלה",
    extra=gtable(["מה בונים", "צריך דאטה בייס?"], [
        ("דף נחיתה או אתר תדמית", "לא. הטופס יכול פשוט לשלוח מייל"),
        ("גלריה, מחירון, פרטי קשר", "לא. אלה דברים קבועים שלא משתנים"),
        ("יומן תורים", "כן. האתר צריך לזכור אילו שעות תפוסות"),
        ("הרשמה ואזור אישי", "כן. כל משתמש נכנס עם שם וסיסמה"),
        ("חנות עם הזמנות", "כן. צריך לשמור מי הזמין מה"),
        ("מערכת ניהול לקוחות", "כן. כל המידע על הלקוחות נשמר שם")]),
)


build_chapter(
    21, "כמה הרגלים קטנים ששומרים על הפרויקט מסודר ובטוח.",
    [("ריפו אחד לכל פרויקט", "לא מערבבים שני אתרים באותו ריפו"),
     ("בודקים את הריפו לפני ששולחים", "למטה בתיבת הכתיבה רואים על איזה ריפו קלוד עובד"),
     ("ריפו פרטי", "בוחרים Private, ככה רק אתם רואים את הקוד"),
     ("סיסמאות לא נכנסות לאתר", "מבקשים מקלוד לשמור אותן בצד, ולא בתוך הקוד"),
     ],
    "אלה ההרגלים. השאר קלוד עושה",
    extra='\n                <div class="note-box key-box"><b>הכי חשוב:</b><span>לפני שהאתר עולה לאוויר, מריצים עליו את <a href="skill-security.html">סקיל בדיקת האבטחה</a> שלנו. הוא מוצא פרצות ומסביר בעברית פשוטה מה לתקן.</span></div>',
)


build_chapter(
    22, "משהו לא עובד? כמעט תמיד מספיק לספר לקלוד מה קרה.",
    [("מופיעה שגיאה", "מצלמים את המסך או מעתיקים את ההודעה, ושולחים לקלוד"),
     ("משהו התקלקל אחרי שינוי", "כותבים לקלוד: \"תחזיר את האתר למצב שהיה לפני השינוי האחרון\""),
     ("השינוי לא מופיע באתר", "מחכים דקה-שתיים ומרעננים את הדף"),
     ("קלוד חוזר על אותה טעות", "פותחים משימה חדשה ומסבירים מחדש, בקצרה"),
     ("קלוד עצר באמצע", "כותבים \"תמשיך\""),
     ("נגמרה כמות העבודה", "מחכים לאיפוס, כמו בפרק 11")],
    "לא צריך להבין מה נשבר. צריך רק לספר",
    extra=tip("אפשר להדביק צילום מסך ישר לתיבת הכתיבה. קלוד רואה אותו ומבין מה הבעיה."),
)


build_chapter(
    23, "יש לכם אתר באוויר. מכאן ממשיכים לפי מה שהעסק צריך.",
    [("כתובת פרטית", "קונים שם כמו carpenter.co.il דרך 4CODE ומחברים לאתר"),
     ("עוד עמודים", "מבקשים מקלוד להוסיף עמוד שירותים, גלריה או שאלות נפוצות"),
     ("להופיע בגוגל", "מבקשים מקלוד לסדר את האתר כך שגוגל ימצא אותו"),
     ("מערכת שזוכרת", "תורים, הרשמה או הזמנות, עם Supabase מפרק 20"),
     (None, "דוגמאות לבקשה הבאה"),
     ("עמוד חדש", "\"תוסיף עמוד גלריה עם 12 תמונות של עבודות, וקישור אליו בתפריט\""),
     ("גוגל", "\"תסדר את האתר כך שיופיע בגוגל כשמחפשים נגר בחיפה\"")],
    "נתקעתם? חוזרים לפרק 22",
    extra='\n                <p class="more-link">רוצים עוד? <a href="articles.html">כל המאמרים</a></p>',
)


# =====================================================================
# מאמרים
# =====================================================================
import html as _html

ARTICLES = []  # (קובץ, כותרת, תקציר, דקות קריאה)

ARTICLE_JS = '''<script>
document.querySelectorAll('[data-copy-from]').forEach(function (b) {
    b.addEventListener('click', function () {
        navigator.clipboard.writeText(document.getElementById(b.dataset.copyFrom).textContent);
        b.textContent = 'הועתק ✓';
        setTimeout(function () { b.textContent = 'העתקה'; }, 2000);
    });
});
document.addEventListener('click', function (e) {
    var img = e.target.closest ? e.target.closest('.fshot img') : null;
    if (!img) return;
    var o = document.createElement('div'); o.className = 'lightbox';
    o.innerHTML = '<img src="' + img.src + '" alt="">'; o.onclick = function () { o.remove(); };
    document.body.appendChild(o);
});
</script>'''


def steps(items):
    """שלבים ממוספרים בלי צילומי מסך. כל שלב: כותרת + פסקאות."""
    out = []
    for i, (title, paras, *img) in enumerate(items, 1):
        body = "".join(f"<p>{x}</p>" for x in paras)
        shot = f'<div class="fshot"><img src="assets/images/guide/{img[0]}" alt="{title}" loading="lazy"></div>' if img else ""
        out.append(f'<li class="fstep"><div class="ftext"><span class="tile">{i}</span><div><h3>{title}</h3>{body}</div></div>{shot}</li>')
    return f'<ol class="flow">{"".join(out)}</ol>'


def table(head, rows):
    """טבלת השוואה. עטופה בקופסה שגוללת לצדדים אם היא רחבה מהמסך."""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def faq_html(items):
    """שאלות נפוצות. seo_build.py הופך אותן אוטומטית לנתונים מובנים (FAQPage)."""
    return '<div class="faq">' + "".join(
        f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def duo(items):
    """כרטיסי השוואה זה לצד זה. כל פריט: (תגית, כותרת, משפט)."""
    return '<div class="duo">' + "".join(
        f'<div class="duo-c{" hl" if i else ""}"><span class="duo-tag">{t}</span><h3>{h}</h3><p>{x}</p></div>'
        for i, (t, h, x) in enumerate(items)) + '</div>'


def plans(items):
    """כרטיסי מחיר. כל פריט: (שם, מחיר, הערה, האם כלול)."""
    return '<div class="plans">' + "".join(
        f'<div class="plan{" yes" if ok else ""}"><b>{n}</b><strong>{pr}</strong><small>{note}</small><span class="plan-ok">{"קלוד קוד כלול ✓" if ok else "בלי קלוד קוד"}</span></div>'
        for n, pr, note, ok in items) + '</div>'


ILL_BUILD = """<div class="ill" aria-hidden="true">
    <div class="ill-msg"><small>אתם כותבים:</small><span>תבנה לי אתר לנגרייה שלי, עם תמונות של עבודות וטופס יצירת קשר</span></div>
    <div class="ill-go"><i></i>קלוד קוד בונה<i></i></div>
    <div class="ill-site">
        <div class="ill-bar"><span></span><span></span><span></span><em>nagariya.co.il</em></div>
        <div class="ill-top"><b>נגרות יוסי</b><span>רהיטים בהזמנה אישית</span><em>צרו קשר</em></div>
        <div class="ill-gal"><i></i><i></i><i></i></div>
        <div class="ill-form"><i></i><i></i><em>שליחה</em></div>
    </div>
</div>"""

ILL_BACKUP = """<div class="ill ill-bk" aria-hidden="true">
    <div class="bk-box gh"><b>GitHub</b><span>אתר הנגרייה</span><span>יומן תורים</span><span>חנות</span></div>
    <div class="bk-go"><i></i><em>כל לילה ב-3:00</em><i></i></div>
    <div class="bk-box dr"><b>Google Drive</b><span>אתר-הנגרייה.zip</span><span>יומן-תורים.zip</span><span>חנות.zip</span></div>
</div>"""


ILL_PRICE = """<div class="ill ill-pr" aria-hidden="true">
    <div class="pr-bill">
        <small>החשבון החודשי שלכם</small>
        <div class="pr-row"><span>מנוי Claude Pro</span><b>20$</b></div>
        <div class="pr-row"><span>קלוד קוד</span><b class="ok">כלול ✓</b></div>
        <div class="pr-row"><span>הקורס של Free AI</span><b class="ok">0$</b></div>
        <div class="pr-sum"><span>סה״כ לחודש</span><strong>20$</strong></div>
    </div>
    <div class="pr-tags"><span>Free · בלי קלוד קוד</span><span class="hl">Pro · 20$</span><span>Max · 100$</span><span>Ultra · 200$</span></div>
</div>"""


_ART_PENDING = []  # המאמרים נכתבים רק אחרי שכולם ידועים, בשביל "עוד מאמרים"


def build_article(name, title, desc, mins, body, seo_title=None, lead="", visual="", date=""):
    """מאמר: חלק פתיחה גרפי (כמו בדף הבית), ואחריו כל <h2> הופך למקטע ממוספר משלו, עם תוכן עניינים צדדי."""
    ARTICLES.append((name, title, desc, mins))
    import home2
    if date: home2.ARTICLE_DATES[name] = date
    _ART_PENDING.append((name, title, desc, mins, body, seo_title, lead, visual, date))


# קווי החוטים בפס הסיום (כמו בפס "קורס קלוד קוד, בחינם ובעברית" בדף הבית)
_CTA_LINES = "".join(
    f'<path d="M{-40 + i * 9} 300 C {120 + i * 14} {210 - i * 6}, {200 + i * 10} {60 + i * 4}, {460 + i * 6} {-20 + i * 3}" stroke="{c}" />'
    for i, c in enumerate(["#D97757", "#E6BB35", "#D43B2D", "#D97757", "#E6BB35", "#C2603F", "#D97757", "#E6BB35", "#D43B2D", "#D97757"]))

ARTICLE2_JS = '''<script>
(function () {
    var bar = document.querySelector('.a2-progress i'), body = document.querySelector('.a2-body');
    var links = [].slice.call(document.querySelectorAll('.a2-toc a[href^="#"]'));
    function onScroll() {
        if (body && bar) {
            var r = body.getBoundingClientRect(), h = r.height - innerHeight * .6;
            bar.style.transform = 'scaleX(' + Math.min(1, Math.max(0, -r.top / (h > 0 ? h : 1))) + ')';
        }
        var cur = null;
        links.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s && s.getBoundingClientRect().top < innerHeight * .35) cur = a; });
        links.forEach(function (a) { a.classList.toggle('on', a === cur); });
    }
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
    document.querySelectorAll('.a2-sh-copy').forEach(function (b) {
        b.addEventListener('click', function () {
            navigator.clipboard.writeText(b.dataset.url); b.classList.add('done');
            setTimeout(function () { b.classList.remove('done'); }, 1800);
        });
    });
    // שאלות נפוצות: נפתחות ונסגרות בתנועה רכה (גובה + שקיפות), במקום קפיצה
    var calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('.a2 .faq details').forEach(function (d) {
        var sum = d.querySelector('summary'), busy = null;
        sum.addEventListener('click', function (e) {
            if (calm || !d.animate) return;
            e.preventDefault();
            if (busy) busy.cancel();
            var from = d.offsetHeight, opening = !d.open;
            if (opening) d.open = true;
            var to = opening ? d.scrollHeight : sum.offsetHeight + 1;
            var ans = d.querySelector('p');
            if (ans) ans.animate(opening ? [{ opacity: 0, transform: 'translateY(-6px)' }, { opacity: 1, transform: 'none' }]
                                         : [{ opacity: 1 }, { opacity: 0 }], { duration: opening ? 420 : 200, easing: 'cubic-bezier(.16,1,.3,1)' });
            d.style.overflow = 'hidden';
            busy = d.animate([{ height: from + 'px' }, { height: to + 'px' }], { duration: opening ? 420 : 320, easing: 'cubic-bezier(.16,1,.3,1)' });
            busy.onfinish = function () { if (!opening) d.open = false; d.style.overflow = ''; busy = null; };
        });
    });
    document.querySelectorAll('.a2-mtoc a').forEach(function (a) { a.addEventListener('click', function () { a.closest('details').open = false; }); });
})();
</script>'''


_SHARE_ICONS = {
    "whatsapp": '<path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.08-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35M12.05 21.5h-.01a9.4 9.4 0 0 1-4.8-1.31l-.34-.2-3.56.93.95-3.47-.22-.36a9.4 9.4 0 0 1-1.44-5.02c0-5.2 4.23-9.43 9.44-9.43a9.4 9.4 0 0 1 9.43 9.44c0 5.2-4.24 9.43-9.45 9.43m8.03-17.46A11.3 11.3 0 0 0 12.05.72C5.79.72.7 5.8.7 12.06c0 2 .52 3.95 1.52 5.67L.6 23.6l6.02-1.58a11.3 11.3 0 0 0 5.42 1.38h.01c6.26 0 11.35-5.09 11.35-11.34 0-3.03-1.18-5.88-3.32-8.02"/>',
    "facebook": '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.5h-2.8V24C19.62 23.1 24 18.1 24 12.07"/>',
    "x": '<path d="M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.4l-5.8-7.58-6.63 7.58H.48l8.6-9.83L0 1.15h7.59l5.24 6.93zm-1.29 19.5h2.04L6.48 3.24H4.3z"/>',
    "linkedin": '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13M7.12 20.45H3.56V9h3.56zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0"/>',
    "telegram": '<path d="M11.94 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm4.96 7.22c.1 0 .32.02.46.14.12.1.15.23.17.33.01.06.03.24.02.38-.18 1.9-.96 6.5-1.36 8.63-.17.9-.5 1.2-.82 1.23-.7.06-1.23-.46-1.9-.9-1.06-.7-1.65-1.13-2.68-1.8-1.19-.79-.42-1.22.26-1.92.18-.19 3.25-2.98 3.31-3.23.01-.03.01-.15-.06-.21-.07-.06-.17-.04-.25-.02-.1.02-1.79 1.14-5.06 3.35-.48.33-.91.49-1.3.48-.43-.01-1.25-.24-1.86-.44-.75-.24-1.35-.37-1.3-.79.03-.22.33-.44.89-.66 3.5-1.52 5.83-2.53 6.99-3.01 3.33-1.39 4.02-1.63 4.47-1.64"/>',
    "mail": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M3 5h18v14H3zM3 6l9 7 9-7"/>',
    "copy": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M9 9h11v11H9zM5 15H4V4h11v1"/>',
}


def _share(name, title):
    from urllib.parse import quote
    url = "https://free-ai.co.il/" + name.removesuffix(".html")
    u, t = quote(url, safe=""), quote(title, safe="")
    links = [
        ("whatsapp", "וואטסאפ", f"https://wa.me/?text={t}%20{u}"),
        ("facebook", "פייסבוק", f"https://www.facebook.com/sharer/sharer.php?u={u}"),
        ("x", "X", f"https://twitter.com/intent/tweet?url={u}&text={t}"),
        ("linkedin", "לינקדאין", f"https://www.linkedin.com/sharing/share-offsite/?url={u}"),
        ("telegram", "טלגרם", f"https://t.me/share/url?url={u}&text={t}"),
        ("mail", "מייל", f"mailto:?subject={t}&body={u}"),
    ]
    ico = lambda k: f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{_SHARE_ICONS[k]}</svg>'
    out = "".join(f'<a class="a2-sh a2-sh-{k}" href="{h}" target="_blank" rel="noopener" aria-label="שיתוף ב{lab}" title="{lab}">{ico(k)}</a>' for k, lab, h in links)
    out += f'<button type="button" class="a2-sh a2-sh-copy" data-url="{url}" aria-label="העתקת הקישור" title="העתקת הקישור">{ico("copy")}</button>'
    return f'<div class="a2-card a2-share"><b>שתפו את המאמר</b><div class="a2-sh-row">{out}</div></div>'


# ניסוי: כותרות במשקל הכי עבה, וטקסט משני קטן ב-1px ובמשקל 200 (site/assets/css/m2-inner.css, .a2-exp)
_ART_EXP = {"article-what-is-claude-code.html"}


def _write_article(name, title, desc, mins, body, seo_title, lead, visual, date):
    import home2
    chunks = [c.strip() for c in re.split(r'(?=<h2>)', body) if c.strip()]
    secs, toc = [], []
    for k, c in enumerate(chunks, 1):
        m = re.match(r'<h2>(.*?)</h2>', c, re.S)
        sid = f"s{k}"
        if m:
            h = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            c = c.replace(m.group(0), f'<div class="a2-head"><span class="a2-num">{k:02d}</span><h2>{m.group(1)}</h2></div>', 1)
            toc.append(f'<li><a href="#{sid}"><span>{k}</span>{h}</a></li>')
        c = re.sub(r'(<div class="note-box"><b>[^<]*?):</b>', r'\1</b>', c)
        secs.append(f'<section class="a2-sec" id="{sid}">{c}</section>')
    toc_ol = f'<ol>{"".join(toc)}</ol>'
    others = [(i, n, t, mn) for i, (n, t, d, mn) in enumerate(ARTICLES) if n != name][:4]
    side_more = band = ""
    if others:
        side_more = '<div class="a2-card a2-smore"><b>מאמרים נוספים</b><ul>' + "".join(
            f'<li><a href="{n}"><img src="{home2._cover(n, i)}" alt="" loading="lazy" decoding="async"><span>{t}<small>{mn} דקות קריאה</small></span></a></li>'
            for i, n, t, mn in others) + '</ul><a href="articles.html" class="a2-all">לכל המאמרים ←</a></div>'
        cards = "".join(
            f'<a class="ac" href="{n}"><img src="{home2._cover(n, i)}" alt="" loading="lazy" decoding="async">'
            f'<span class="ac-b"><h3 class="ac-t">{t}</h3>{home2._meta(n, mn)}</span></a>'
            for i, n, t, mn in others[:3])
        band = ('<section class="a2-band a2-more"><div class="a2-wrap a2-pad">'
                '<div class="a2-band-head"><h2>עוד מאמרים</h2><a href="articles.html" class="a2-link">לכל המאמרים ←</a></div>'
                f'<div class="m2-arts">{cards}</div></div></section>')
    main = f'''<div class="a2-progress" aria-hidden="true"><i></i></div>
    <main class="a2{' a2-exp' if name in _ART_EXP else ''}">
        <div class="a2-wrap a2-grid">
            <div class="a2-body">
                <details class="a2-card a2-mtoc"><summary>בעמוד הזה</summary>{toc_ol}</details>
                {"".join(secs)}
            </div>
            <aside class="a2-side" aria-label="שיתוף ומאמרים נוספים"><div class="a2-stick">
                {_share(name, title)}
                <nav class="a2-card a2-toc" aria-label="תוכן העניינים"><b>בעמוד הזה</b>{toc_ol}</nav>
                {side_more}
            </div></aside>
        </div>
        {band}
        <section class="a2-band a2-cta"><div class="a2-wrap a2-pad">
            <svg class="a2-cta-lines" viewBox="0 0 460 300" fill="none" aria-hidden="true" preserveAspectRatio="none">{_CTA_LINES}</svg>
            <div><h2>רוצים לבנות דברים כאלה בעצמכם?</h2><p>הקורס חינמי ובעברית, ולא צריך לדעת לתכנת.</p></div>
            <div class="a2-cta-btns"><a href="course.html" class="a2-btn">להתחיל ללמוד בחינם</a><a href="guide-1.html" class="a2-btn ghost">למדריך הכתוב</a></div>
        </div></section>
    </main>'''
    (SITE / name).write_text(home2.inner_page(f"{seo_title or title} | Free AI", desc, "", title, lead, visual, main,
                                              meta=[("clock", f"{mins} דקות קריאה")] + ([("cal", date)] if date else []),
                                              script=ARTICLE_JS + ARTICLE2_JS, legacy_v=CSS_VERSION))
    print(f"{name} done")


def build_articles_index():
    for _a in _ART_PENDING:
        _write_article(*_a)
    import home_mint
    cards = "".join(
        f'<a href="{n}" class="card art-card"><h2>{t}</h2><p class="muted">{d}</p><span class="go">לקריאה ←</span></a>'
        for n, t, d, m in ARTICLES)
    import home2
    (SITE / "articles.html").write_text(home2.inner_page(
        "מאמרים על בינה מלאכותית ואוטומציה בעברית – Free AI", "מדריכים קצרים בעברית לבנייה ואוטומציה עם בינה מלאכותית, בלי לדעת לתכנת.",
        "", "מאמרים", "מדריכים קצרים שאפשר לעשות היום, בלי לדעת לתכנת.", home2.articles_visual(ARTICLES), home2.articles_main(ARTICLES),
        btn2=("guide-1.html", "למדריך הכתוב", "book"), legacy_v=CSS_VERSION))
    print("articles.html done")


build_article(
    "article-what-is-claude-code.html",
    "מה זה קלוד קוד? הסבר פשוט למי שלא מתכנת",
    "קלוד קוד (Claude Code) הוא כלי של Anthropic שבונה אתרים ומערכות לפי מה שכותבים לו בעברית. מה זה, כמה עולה ואיך מתחילים, בלי לדעת לתכנת.",
    6,
    f'''
            <h2>קלוד קוד בדימוי אחד</h2>
            {duo([
                ("קלוד (הצ'אט)", "יועץ", "יושב איתכם, עונה ונותן רעיונות, אבל לא נוגע בכלום."),
                ("קלוד קוד", "בעל מקצוע", "לוקח את הכלים, בונה, מתקן, ומראה לכם מה עשה."),
            ])}
            <p>קוד הוא המתכון שהמחשב קורא כדי להציג אתר, וקלוד קוד כותב אותו בשבילכם.</p>

            <h2>איך קלוד קוד עובד</h2>
            {rows_html([
                ("אתם כותבים מה רוצים", "בעברית רגילה, כמו הודעה לחבר"),
                ("הוא מתכנן", "מחליט אילו עמודים וקבצים צריך"),
                ("הוא בונה", "כותב את הקוד ויוצר את הקבצים לבד"),
                ("הוא בודק", "מריץ את מה שבנה ומתקן טעויות"),
                ("אתם מבקשים שינוי", '"תגדיל את הכותרת", "תוסיף טופס"'),
                (None, "דוגמאות"),
                ("אתר תדמית לנגר", "תמונות עבודות, שירותים וטופס"),
                ("יומן תורים לספרית", "לקוחות קובעים תור לבד"),
                ("גיבוי אוטומטי לקבצים", '<a href="article-github-backup.html">גיבוי הפרויקטים ל-Google Drive</a>'),
            ])}

            <h2>מה ההבדל בין קלוד לקלוד קוד</h2>
            {table(["", "קלוד (הצ'אט)", "קלוד קוד"], [
                ["מה עושה", "עונה, מסביר וכותב טקסט", "בונה ומשנה אתרים ומערכות"],
                ["נוגע בקבצים?", "לא", "כן, יוצר ומשנה לבד"],
                ["מה מקבלים", "תשובה על המסך", "אתר או כלי שעובד"],
                ["מתי משתמשים", "מייל, פוסט, רעיון", "אתר, דף נחיתה, מערכת לעסק"],
                ["איפה לוחצים", "הלשונית Chat", "הלשונית Code"],
            ])}
            <div class="fshot"><img src="assets/images/guide/claude-install-5.png" alt="איך נראה קלוד קוד: באפליקציה של קלוד בוחרים בלשונית Code" loading="lazy"></div>

            <h2>איפה עובדים עם קלוד קוד</h2>
            {rows_html([
                ("אפליקציה במחשב", "Mac או Windows, הכי פשוט"),
                ("בדפדפן", "claude.ai/code, בלי התקנה"),
                ("בטלפון", "האפליקציה של קלוד ל-iPhone ול-Android"),
                ("בטרמינל", "חלון פקודות שחור, למתכנתים"),
            ])}
            <div class="note-box"><b>מה אנחנו בוחרים:</b> האפליקציה במחשב, כי הכול בלחיצות.</div>

            <h2>כמה עולה קלוד קוד</h2>
            {plans([
                ("Free", "0$", "לחודש", False),
                ("Pro", "20$", "לחודש (17$ בתשלום שנתי)", True),
                ("Max", "100$", "לחודש, הרבה יותר שימוש", True),
                ("Ultra", "200$", "לחודש, הכי הרבה שימוש", True),
            ])}
            <p class="art-src">נכון ל-18 בנובמבר 2026, לפי <a href="https://claude.com/pricing" target="_blank" rel="noopener">דף המחירים של Anthropic</a>. למתחילים מספיק Pro.</p>
            <p class="more-link">כל המנויים וההבדלים ביניהם: <a href="article-claude-code-price.html">כמה עולה קלוד קוד</a>.</p>

            <h2>האם צריך לדעת לתכנת?</h2>
            {duo([
                ("לא צריך", "לדעת קוד", "מסבירים במילים מה בונים ובשביל מי."),
                ("מספיק", "עברית רגילה", 'אפשר גם לדבר במיקרופון.'),
            ])}

            <h2>איך מתחילים לעבוד עם קלוד קוד</h2>
            {rows_html([
                ("פותחים חשבון קלוד", 'ונרשמים למנוי Pro'),
                ("מתקינים את האפליקציה", 'מ-claude.com/download'),
                ("פותחים חשבון GitHub", 'כאן נשמרים הפרויקטים'),
                ("בונים פרויקט ראשון", 'כותבים בקשה ורואים אותו בונה'),
            ])}
            <p class="more-link">מעדיפים וידאו? <a href="course.html">קורס קלוד קוד בעברית, בחינם</a>.</p>

            <h2>שאלות נפוצות</h2>
            {faq_html([
                ("האם קלוד קוד בחינם?", "לא. צריך מנוי בתשלום של קלוד, לפחות Pro ב-20$ לחודש (נכון ל-18 בנובמבר 2026). הקורס והמדריך שלנו חינמיים."),
                ("האם קלוד קוד עובד בעברית?", "כן. כותבים לו בעברית רגילה, והוא עונה ובונה אתרים בעברית. ככה עשינו בכל המדריך."),
                ("צריך לדעת לתכנת כדי להשתמש בקלוד קוד?", "לא. מסבירים לו במילים מה רוצים, והוא כותב את הקוד בעצמו."),
                ("איך מורידים את קלוד קוד למחשב?", "מורידים את האפליקציה של קלוד מ-claude.com/download, מתחברים, ולוחצים על הלשונית Code. יש מדריך מלא בפרק 4."),
                ("אפשר לעבוד עם קלוד קוד מהטלפון?", "כן. קלוד קוד זמין גם באפליקציה של קלוד ל-iPhone ול-Android."),
                ("יש קורס קלוד קוד בעברית?", "כן. אצלנו יש קורס קלוד קוד חינמי בעברית, עם שיעורי וידאו ומדריך כתוב."),
            ])}
            <p class="art-src">מקורות: <a href="https://code.claude.com/docs/en/overview" target="_blank" rel="noopener">התיעוד הרשמי של קלוד קוד</a>, <a href="https://claude.com/pricing" target="_blank" rel="noopener">דף המחירים של Anthropic</a>.</p>'''
,
    seo_title="מה זה קלוד קוד (Claude Code)? הסבר פשוט בעברית",
    lead="קלוד קוד (Claude Code) הוא כלי של חברת Anthropic שבונה בשבילכם אתרים ומערכות לפי מה שאתם כותבים לו במילים רגילות. אתם מסבירים מה רוצים, והוא כותב את הקוד ובודק שהכול עובד.",
    visual=ILL_BUILD,
    date="18 בנובמבר 2026",
)

build_article(
    "article-claude-code-price.html",
    "כמה עולה קלוד קוד? ומה אפשר בחינם",
    "כמה עולה קלוד קוד (Claude Code) לחודש? כל המנויים והמחירים מהמקור הרשמי, מה כלול בכל אחד, ואיזה מנוי מספיק למתחילים.",
    5,
    f'''
            <h2>המחירון של קלוד קוד</h2>
            {plans([
                ("Free", "0$", "לחודש", False),
                ("Pro", "20$", "לחודש (17$ בתשלום שנתי)", True),
                ("Max", "100$", "לחודש, פי 5 מ-Pro", True),
                ("Ultra", "200$", "לחודש, פי 10 מ-Pro", True),
            ])}
            <p class="art-src">נכון ל-23 בנובמבר 2026, לפי <a href="https://claude.com/pricing" target="_blank" rel="noopener">דף המחירים של Anthropic</a>. המחירים בדולרים.</p>

            <h2>מה ההבדל בין המנויים</h2>
            <p>כל המנויים בתשלום נותנים את אותו קלוד קוד. ההבדל הוא רק כמה עבודה מקבלים, כמו חבילת גלישה בטלפון.</p>
            {table(["", "Pro", "Max", "Ultra"], [
                ["מחיר לחודש", "20$", "100$", "200$"],
                ["כמה עבודה", "הבסיס", "פי 5 מ-Pro", "פי 10 מ-Pro בשבוע"],
                ["מגבלת 5 שעות", "יש", "יש (פי 5)", "אין"],
                ["למי", "מתחילים ופרויקט אחד", "עבודה כל יום", "עבודה כל היום, כמה פרויקטים"],
            ])}
            <p class="more-link">מה זה מגבלת 5 שעות ואיפה רואים כמה נשאר: <a href="guide-11.html">כמה נשאר מהמנוי</a>.</p>

            <h2>איזה מנוי מתאים לכם</h2>
            {rows_html([
                ("רק מתחילים", "Pro. בונים אתר ראשון ולומדים בלי לשרוף כסף"),
                ("המכסה נגמרת כל יום", "Max. ככה זה מרגיש כשעובדים על העסק כמה שעות ביום"),
                ("עובדים על כמה פרויקטים בבת אחת", "Ultra, אבל רק אחרי שראיתם ש-Max לא מספיק"),
                (None, "דוגמאות"),
                ("אתר תדמית לנגר", "Pro מספיק. בונים בכמה ערבים"),
                ("חנות עם יומן תורים ומסך ניהול", "מתחילים ב-Pro, ועוברים ל-Max אם נתקעים בהמתנה"),
            ])}
            <div class="note-box"><b>מה אנחנו בוחרים:</b> Pro בתשלום חודשי. משדרגים רק כשהמכסה באמת עוצרת אתכם.</div>

            <h2>חודשי או שנתי</h2>
            {duo([
                ("חודשי", "20$ בחודש", "משלמים כל חודש ומבטלים מתי שרוצים."),
                ("שנתי", "17$ בחודש", "חוסכים 3$ בחודש, אבל משלמים 200$ מראש."),
            ])}
            <p>בחודש הראשון עוד לא יודעים אם זה בשבילכם. לכן מתחילים בחודשי.</p>

            <h2>מה כן בחינם</h2>
            {rows_html([
                ("קלוד הרגיל (הצ'אט)", "יש מסלול Free, אבל בלי קלוד קוד ועם מעט שימוש"),
                ("הקורס והמדריך שלנו", '<a href="course.html">קורס קלוד קוד בעברית</a> ו<a href="guide-1.html">מדריך כתוב</a>, בחינם'),
                ("GitHub", 'המקום שבו נשמרים הפרויקטים. <a href="guide-5.html">פותחים חשבון בחינם</a>'),
            ])}
            <p>קלוד קוד עצמו לא חינמי. מי שכותב "קלוד קוד בחינם" מתכוון בדרך כלל לצ'אט, ושם אי אפשר לבנות אתר שעובד.</p>

            <h2>איך חוסכים במכסה</h2>
            {rows_html([
                ("בוחרים מודל חסכוני", 'Sonnet לעבודה הרגילה, Opus רק לדברים גדולים. <a href="guide-9.html">בחירת המודל</a>'),
                ("מבקשים כמה תיקונים בהודעה אחת", "שלושה תיקונים באותו עמוד בהודעה אחת, לא בשלוש"),
                ("פותחים שיחה חדשה לכל משימה", "שיחה ארוכה מאוד צורכת יותר בכל הודעה"),
            ])}

            <h2>מנוי לצוות או לחברה</h2>
            {table(["", "Team רגיל", "Team Premium", "Enterprise"], [
                ["מחיר למושב", "25$ (20$ בשנתי)", "125$ (100$ בשנתי)", "20$ בשנתי + שימוש"],
                ["כמה אנשים", "2 עד 150", "2 עד 150", "מ-20 מושבים"],
                ["קלוד קוד", "כלול", "כלול", "כלול"],
            ])}
            <p>ב-Enterprise משלמים גם לפי כמה עובדים בפועל. Anthropic מדווחת שבחברות כאלה הממוצע הוא בערך 13$ ליום עבודה למפתח (<a href="https://code.claude.com/docs/en/costs" target="_blank" rel="noopener">מקור</a>).</p>

            <h2>שאלות נפוצות</h2>
            {faq_html([
                ("האם קלוד קוד בחינם?", "לא. צריך מנוי בתשלום, לפחות Pro ב-20$ לחודש. במסלול Free של קלוד אין קלוד קוד (נכון ל-23 בנובמבר 2026)."),
                ("כמה עולה קלוד קוד לחודש?", "20$ במנוי Pro, או 17$ לחודש בתשלום שנתי. Max עולה 100$ ו-Ultra עולה 200$."),
                ("מה קורה כשנגמרת המכסה?", "מחכים שהיא תתמלא מחדש, או עוברים למודל שצורך פחות, כמו Sonnet."),
                ("משלמים בשקלים או בדולרים?", "המחירים של Anthropic בדולרים, וחברת האשראי ממירה אותם לשקלים."),
                ("איך פותחים מנוי?", 'נרשמים ב-claude.ai ובוחרים Pro. יש מדריך צעד אחרי צעד <a href="guide-3.html">בפרק פתיחת החשבון</a>.'),
                ("יש קורס קלוד קוד בחינם?", 'כן. <a href="course.html">הקורס שלנו</a> חינמי ובעברית. משלמים רק על המנוי של קלוד.'),
            ])}
            <p class="more-link">רוצים להבין קודם מה מקבלים? <a href="article-what-is-claude-code.html">מה זה קלוד קוד, בהסבר פשוט</a>.</p>
            <p class="art-src">מקורות: <a href="https://claude.com/pricing" target="_blank" rel="noopener">דף המחירים של Anthropic</a>, <a href="https://code.claude.com/docs/en/costs" target="_blank" rel="noopener">תיעוד העלויות של קלוד קוד</a>. נבדק ב-23 בנובמבר 2026.</p>'''
,
    seo_title="קלוד קוד מחיר: כמה עולה Claude Code ומה בחינם",
    lead="קלוד קוד לא חינמי: הוא מגיע עם מנוי בתשלום של קלוד, והזול ביותר הוא Pro ב-20$ לחודש. למתחילים זה מספיק, ומשדרגים רק כשהמכסה נגמרת.",
    visual=ILL_PRICE,
    date="23 בנובמבר 2026",
)

_GS = (SITE / "files/github-drive-backup.gs").read_text()

build_article(
    "article-github-backup.html",
    "גיבוי אוטומטי של כל הפרויקטים מ-GitHub ל-Google Drive",
    "איך מגדירים פעם אחת גיבוי יומי של כל הפרויקטים ב-GitHub לתיקייה בגוגל דרייב, בחינם ובלי לדעת לתכנת.",
    6,
    f'''
            <h2>למה צריך גיבוי</h2>
            <p>GitHub הוא כמו מחסן שבו שמור הקוד של כל האתרים והכלים שבניתם.</p>
            <p>אם החשבון ננעל, נמחק או שמשהו נשבר, בלי גיבוי כל העבודה נעלמת.</p>
            <p>גיבוי הוא עותק נוסף במקום אחר, כמו מפתח רזרבי לבית שמחכה אצל השכנים.</p>

            <h2>מה הגיבוי עושה</h2>
            {rows_html([
                ("מה נשמר", "עותק מלא של כל פרויקט, כקובץ zip (קופסה אחת שכל הקבצים בתוכה)"),
                ("מתי", "כל לילה ב-3:00, לבד, גם כשהמחשב כבוי"),
                ("איפה", "בתיקייה GitHub Backups בדרייב, עם תיקייה לכל חשבון GitHub"),
                ("כמה עותקים", "תמיד אחד לכל פרויקט: הגרסה הכי עדכנית"),
                ("פרויקט שלא השתנה", "לא נוגעים בו, והגיבוי של אתמול נשאר"),
                ("הגיבוי הקודם", "עובר לפח של הדרייב ונמחק לגמרי אחרי 30 יום"),
                (None, "מה לא נשמר"),
                ("ההיסטוריה", "רואים רק את המצב האחרון, לא כל שינוי שנעשה בדרך"),
                ("ענפים (Branches)", "גרסאות צדדיות של הפרויקט. נשמרת רק הגרסה הראשית"),
                ("קבצי סיסמאות", "הם אף פעם לא נמצאים ב-GitHub, אז שומרים אותם בנפרד"),
                ("פרויקט ענק", "פרויקט מעל 50MB לא נשמר"),
            ])}

            <h2>מה צריך</h2>
            {rows_html([
                ("חשבון GitHub", "אחד או יותר, עם הפרויקטים שלכם"),
                ("חשבון Google", "זה שבדרייב שלו יישמרו הגיבויים"),
                ("10 דקות", "פעם אחת, וזהו"),
            ])}

            <h2>איך מגדירים, צעד אחרי צעד</h2>
            {steps([
                ("יוצרים מפתח ב-GitHub", [
                    "המפתח (Token) הוא כמו מפתח לבית שנותנים לשליח: הוא מאפשר לגיבוי להיכנס ולהעתיק את הפרויקטים.",
                    'נכנסים ל-<a href="https://github.com/settings/tokens/new" target="_blank" rel="noopener">github.com/settings/tokens/new</a>, כותבים בשם "גיבוי לדרייב", ובתוקף (Expiration) בוחרים No expiration.',
                    "מסמנים V ליד repo, יורדים למטה ולוחצים Generate token.",
                    'מעתיקים את המפתח שמופיע (מתחיל ב-<code class="inl">ghp_</code>) ושומרים אותו רגע בצד. הוא מוצג רק פעם אחת.',
                    "יש לכם כמה חשבונות GitHub? עושים את זה בכל אחד מהם.",
                ], "backup-1.png"),
                ("פותחים את Google Apps Script", [
                    "Apps Script הוא כמו עוזר קטן שגר בתוך חשבון הגוגל שלכם ויודע לעשות פעולות לבד, בשעה קבועה.",
                    'נכנסים ל-<a href="https://script.google.com" target="_blank" rel="noopener">script.google.com</a> עם אותו חשבון גוגל של הדרייב, ולוחצים "פרויקט חדש" (New project).',
                ], "backup-2.png"),
                ("מדביקים את הקוד", [
                    "מוחקים את כל מה שכתוב בחלון, ומדביקים במקומו את הקוד שבהמשך העמוד (כפתור העתקה).",
                    'במקום <code class="inl">PASTE_TOKEN_ACCOUNT_1</code> מדביקים את המפתח, ומשאירים את המירכאות סביבו.',
                    'יש חשבון נוסף? בשורה שמתחתיה מוחקים את <code class="inl">//</code> בתחילתה, ומדביקים שם את המפתח השני.',
                ], "backup-3.png"),
                ("שומרים ומפעילים פעם אחת", [
                    'לוחצים על סמל השמירה. בתפריט שליד הכפתור "הפעלה" (Run) בוחרים <code class="inl">setup</code>, ולוחצים "הפעלה".',
                    'גוגל תבקש אישור. לוחצים "בדיקת הרשאות", בוחרים את החשבון, לוחצים "מתקדם" (Advanced), ואז "מעבר אל..." ו"אישור" (Allow).',
                    "האזהרה מופיעה כי את הקוד הוספתם אתם ולא גוגל. זה תקין: הוא רץ רק בחשבון שלכם.",
                ], "backup-4.png"),
                ("בודקים שזה עובד", [
                    "פותחים את הדרייב ומחפשים את התיקייה GitHub Backups. בתוכה תיקייה לכל חשבון וקובץ zip לכל פרויקט.",
                    "הרבה פרויקטים? הגיבוי הראשון ממשיך לבד ברקע עד שהוא מסתיים.",
                ], "backup-5.png"),
            ])}
            <div class="note-box">טעות נפוצה: בתפריט נשאר <code class="inl">myFunction</code> במקום <code class="inl">setup</code>. ההפעלה "מצליחה", אבל לא קורה כלום.</div>

            <h2>הקוד</h2>
            <div class="code-box"><div class="code-bar"><span>הקוד של הגיבוי</span><div><a class="btn-2 sm" href="files/github-drive-backup.gs" download>הורדה</a><button type="button" class="btn-2 sm" data-copy-from="gs-code">העתקה</button></div></div><pre id="gs-code">{_html.escape(_GS)}</pre></div>

            <h2>איך יודעים שהגיבוי עדכני</h2>
            <p>בשם התיקייה שבתוך קובץ ה-zip יש קוד קצר, למשל <code class="inl">7499555</code>: זה מספר הגרסה של הפרויקט.</p>
            <p>בדף הפרויקט ב-GitHub, ליד המילה commits, מופיע אותו קוד. אם הם זהים, הגיבוי מעודכן.</p>

            <h2>שמירה על המפתח</h2>
            {rows_html([
                ("לא משתפים", "מי שיש לו את המפתח יכול לראות את כל הפרויקטים שלכם"),
                ("הקוד פרטי", "הוא נמצא רק בחשבון הגוגל שלכם, ואף אחד אחר לא רואה אותו"),
                ("המפתח דלף?", "מוחקים אותו בדף המפתחות ב-GitHub, יוצרים חדש ומחליפים בקוד"),
            ])}

            <h2>שאלות נפוצות</h2>
            <div class="faq">{"".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
                ("זה עולה כסף?", "לא. גם GitHub וגם Apps Script חינמיים לשימוש הזה."),
                ("המחשב צריך להיות דלוק?", "לא. הגיבוי רץ אצל גוגל, לא אצלכם."),
                ("איך משנים את שעת הגיבוי?", "בשורה RUN_HOUR משנים את 3 לשעה אחרת, שומרים ומפעילים שוב את setup."),
                ("איך עוצרים את הגיבוי?", "ב-Apps Script לוחצים על סמל השעון בצד (טריגרים) ומוחקים את מה שמופיע שם."),
                ("הוספתי פרויקט חדש ב-GitHub. צריך לעשות משהו?", "לא. הוא ייכנס לבד לגיבוי של הלילה."),
            ])}</div>''',
    lead="מגדירים פעם אחת, ומאז כל לילה כל הפרויקטים שלכם נשמרים לבד בתיקייה בגוגל דרייב.",
    visual=ILL_BACKUP,
)


def build_soon():
    """עמוד "בשיפוצים": מוגש במקום עמודי הקורס עד שהקורס חוזר. ממורכז, בלי איורים."""
    import home_mint
    body = f'''    <div class="wrap full">
        <section class="c-hero a-hero">
        {header("course.html")}
        </section>
    </div>
    <main class="soon">
        <h1 class="soon-big"><span class="grad">בשיפוצים</span></h1>
        <p class="soon-sub">משפצים את הקורס כדי שיהיה עוד יותר קל ללמוד.<br>וכמו תמיד: הוא נשאר בחינם.</p>
        <div class="btns"><a href="articles.html" class="btn">בינתיים, למאמרים <span class="arr">‹</span></a><a href="index.html" class="btn-2">לדף הבית</a></div>
    </main>
    <style>
        .soon {{ min-height: 62vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 18px; padding: 40px 16px 80px; }}
        .soon-big {{ font-size: clamp(72px, 16vw, 200px); line-height: .95; margin: 0; font-weight: 700; letter-spacing: -.02em; }}
        .soon-sub {{ font-size: clamp(18px, 2.4vw, 22px); color: var(--neutral-500, #6b7280); margin: 0; }}
        .soon .btns {{ justify-content: center; margin-top: 8px; }}
    </style>
{home_mint.footer(CHAPTERS, ARTICLES, READY)}'''
    (SITE / "soon.html").write_text(page("הקורס בשיפוצים – תכף חוזרים | Free AI", "משפצים את הקורס ותכף חוזרים. הקורס נשאר בחינם.", body, css="home.css"))
    print("soon.html done")


build_articles_index()
build_home()
build_soon()
import home2 as _h2
_h2.build()  # עמוד הבית הראשי (המבנה של Mintlify), נכתב מעל index.html

# הפוטר הגדול במאמרים (אחרי שכל המאמרים ידועים)
import home_mint as _hm
for _n, *_ in ARTICLES:
    _f = SITE / _n
    _f.write_text(_f.read_text().replace("<!--big-footer-->", ""))

# העמודים המשפטיים (פרטיות, תנאים, נגישות) בעיצוב החדש
import legal_pages as _lp
_lp.build()

# עמודי הסקילים בעיצוב החדש
import skills_mint as _sk
_sk.build()

# שכבת SEO (canonical, שיתוף, נתונים מובנים, sitemap) – תמיד בסוף הבנייה
import runpy as _runpy
_runpy.run_path(str(Path(__file__).resolve().parents[1] / "seo" / "seo_build.py"), run_name="__main__")
