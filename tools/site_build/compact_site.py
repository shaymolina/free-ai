"""Free AI – העיצוב המצומצם. בונה את עמודי האתר מאפס, בלי התבנית הכבדה.

כרגע: דף הבית (index.html) והמדריך (guide-N.html).
הרצה: cd tools/site_build && python3 compact_site.py
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"
CSS_VERSION = "9"
COUPON = "RVJ34jcn4j1"

NAV = [("index.html", "דף הבית"), ("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים")]

# שם הפרק, דקות קריאה
CHAPTERS = [
    ("לפני שמתחילים", 2), ("Claude מול Claude Code", 3), ("פותחים חשבון Claude", 4),
    ("מתקינים את האפליקציה", 5), ("פותחים GitHub", 4), ("פותחים 4CODE", 4),
    ("Supabase, כן או לא", 3), ("הפרויקט הראשון", 8), ("מעלים לאוויר", 5),
    ("איך מדברים עם Claude Code", 4), ("סדר ובטיחות", 4), ("כשמשהו נתקע", 4), ("השלב הבא", 3),
]
READY = {1}  # פרקים שכבר כתובים


def header(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="c-header">
            <a href="index.html" class="c-logo"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>
            <nav class="c-nav">{links}</nav>
            <a href="service.html" class="btn sm">התחל ללמוד</a>
            <button type="button" class="btn c-menu-btn" aria-label="תפריט" onclick="this.parentNode.classList.toggle('open')"><i class="icon icon-grip-lines-solid"></i></button>
        </header>'''


FOOTER = '''<footer class="c-foot">
            <span>© 2026 Free AI. כל הזכויות שמורות.</span>
            <nav><a href="privacy.html">פרטיות</a><a href="terms.html">תנאי שימוש</a></nav>
        </footer>'''


def page(title, desc, body, script="", cls=""):
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="author" content="Free AI">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{desc}">
    <link rel="stylesheet" href="assets/fonts/fonts.css">
    <link rel="stylesheet" href="assets/icon/icomoon/style.css">
    <link rel="stylesheet" href="assets/css/compact.css?v={CSS_VERSION}">
    <link rel="shortcut icon" href="assets/images/logo/favicon.svg">
    <link rel="apple-touch-icon-precomposed" href="assets/images/logo/favicon.svg">
</head>
<body{(f' class="{cls}"' if cls else "")}>
{body}
{script}
</body>
</html>
'''


# =====================================================================
# דף הבית
# =====================================================================
def build_home():
    rows = "".join(
        f'<a href="guide-1.html"><span class="dot{" on" if i == 1 else ""}"></span>{i}. {name}<small>{mins} דק\'</small></a>'
        for i, (name, mins) in enumerate(CHAPTERS[:4], 1))
    faq = "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in [
        ("צריך מנוי בתשלום ל-Claude?", "כן. Claude Pro ומעלה."),
        ("צריך ידע קודם?", "לא. מתחילים מאפס."),
        ("כמה זמן לוקח הקורס?", "8 שיעורים קצרים, בקצב שלכם."),
        ("למה צריך להירשם?", "כדי לצפות, להוריד קבצים ולקבל תעודה."),
    ])
    body = f'''    <div class="wrap full">
        <section class="c-hero">
        {header("index.html")}
            <div class="hero-in">
                <div class="hero-text">
                    <h1 class="hero-title"><span class="grad">לומדים Claude Code.</span><span class="hero-line"><span class="grad">בלי לדעת לתכנת.</span>
                        <span class="hero-pill"><img src="assets/images/item/hero-1.svg" alt=""><img src="assets/images/item/hero-2.svg" alt=""><img src="assets/images/item/hero-3.svg" alt=""></span></span></h1>
                    <p>קורס, מדריך כתוב וסקילים מוכנים. מהצעד הראשון ועד אתר שעובד באוויר.</p>
                </div>
                <div class="card preview">{rows}<a href="guide-1.html" class="muted"><span class="dot"></span>ועוד {len(CHAPTERS) - 4} פרקים</a></div>
            </div>
        </section>
    </div>
    <main class="wrap full stack" style="margin-top:16px">
        <div class="three">
            <a href="service.html" class="card pick"><h2>הקורס</h2><p class="muted">8 שיעורי וידאו קצרים, לפי הסדר.</p><span class="go">לקורס ←</span></a>
            <a href="guide-1.html" class="card pick"><h2>המדריך</h2><p class="muted">{len(CHAPTERS)} פרקים קצרים לקריאה, צעד אחרי צעד.</p><span class="go">למדריך ←</span></a>
            <a href="work.html" class="card pick"><h2>סקילים</h2><p class="muted">יכולות מוכנות ל-Claude, להורדה בחינם.</p><span class="go">לסקילים ←</span></a>
        </div>
        <div class="sec-title"><span class="chip">שאלות נפוצות</span></div>
        <div class="faq">{faq}</div>
        {FOOTER}
    </main>'''
    (SITE / "index.html").write_text(page(
        "Free AI – לומדים Claude Code בחינם, בעברית",
        "קורס, מדריך כתוב וסקילים ל-Claude Code בעברית ובחינם. מהצעד הראשון ועד אתר שעובד באוויר.", body))
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
        if (btn && done.indexOf(CURRENT) > -1 && !btn.dataset.next) { btn.textContent = 'סיימתם ✓ הפרק הבא בקרוב'; btn.classList.add('is-done'); }
    }
    if (btn) btn.addEventListener('click', function () {
        var done = load();
        if (done.indexOf(CURRENT) < 0) { done.push(CURRENT); save(done); }
        if (btn.dataset.next) location.href = btn.dataset.next; else paint();
    });
    var copy = document.getElementById('guide-copy');
    if (copy) copy.addEventListener('click', function () { navigator.clipboard.writeText(copy.dataset.code); copy.textContent = 'הועתק ✓'; });
    paint();
})();
</script>'''


def sidebar(current):
    items = []
    for i, (name, _) in enumerate(CHAPTERS, 1):
        cls = "ch" + (" is-on" if i == current else "")
        inner = f'<span class="dot">✓</span>{i}. {name}'
        if i in READY:
            items.append(f'<li><a href="guide-{i}.html" class="{cls}" data-ch="{i}">{inner}</a></li>')
        else:
            items.append(f'<li><span class="{cls}" data-ch="{i}">{inner}</span></li>')
    return f'''<aside class="card side">
                <h3>המדריך ל-Claude Code</h3>
                <div class="bar"><i id="guide-fill"></i></div>
                <div class="count" id="guide-count"></div>
                <ol class="chs">{"".join(items)}</ol>
            </aside>'''


def build_chapter(n, lead, rows, note, extra=""):
    name, mins = CHAPTERS[n - 1]
    row_html = "".join(f'<li class="row"><span class="tile">{i}</span>{a}<small>{b}</small></li>' for i, (a, b) in enumerate(rows, 1))
    nxt = f' data-next="guide-{n + 1}.html"' if (n + 1) in READY else ""
    body = f'''    <div class="wrap full c-top">
        {header("guide-1.html")}
    </div>
    <main class="wrap full stack guide-main" style="margin-top:16px">
        <div class="course">
            {sidebar(n)}
            <article class="card lesson">
                <span class="chip" style="align-self:flex-start">פרק {n} · {mins} דקות</span>
                <h1>{name}</h1>
                <p class="lead">{lead}</p>
                <ol class="rows">{row_html}</ol>{extra}
                <div class="lesson-end"><span>{note}</span><button type="button" class="btn" id="guide-done"{nxt}>סיימתי, לפרק הבא ←</button></div>
            </article>
        </div>
        {FOOTER}
    </main>'''
    (SITE / f"guide-{n}.html").write_text(page(
        f"{name} – המדריך ל-Claude Code | Free AI",
        f"פרק {n} במדריך ל-Claude Code למי שלא מתכנת: {lead}", body,
        GUIDE_JS % {"total": len(CHAPTERS), "current": n}, cls="guide-page"))
    print(f"guide-{n}.html done")


build_home()
build_chapter(
    1, "שלושה דברים להכין, ואפשר לצאת לדרך.",
    [("מחשב", "Mac או Windows"), ("מייל", "אחד לכל השירותים"), ("כרטיס אשראי", "כ-20 דולר לחודש ל-Claude")],
    "כל השאר בחינם להתחלה",
    extra=f'''
                <div class="coupon">קופון לחודש ראשון בחינם ב-4CODE: <code>{COUPON}</code><button type="button" class="btn-2 sm" id="guide-copy" data-code="{COUPON}">העתקה</button></div>''',
)
