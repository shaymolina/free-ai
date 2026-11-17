"""Free AI – העיצוב המצומצם. בונה את עמודי האתר מאפס, בלי התבנית הכבדה.

כרגע: דף הבית (index.html) והמדריך (guide-N.html).
הרצה: cd tools/site_build && python3 compact_site.py
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"
CSS_VERSION = "17"
COUPON = "RVJ34jcn4j1"

NAV = [("index.html", "דף הבית"), ("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים")]

# שם הפרק, דקות קריאה
CHAPTERS = [
    ("לפני שמתחילים", 2), ("Claude מול Claude Code", 3), ("פותחים חשבון Claude", 4),
    ("מתקינים את האפליקציה", 5), ("פותחים GitHub", 4), ("מה זה ריפו ופותחים אחד", 5), ("הפרויקט הראשון", 8), ("מעלים לאוויר", 5),
    ("פותחים 4CODE", 4), ("Supabase, כן או לא", 3),
    ("איך מדברים עם Claude Code", 4), ("סדר ובטיחות", 4), ("כשמשהו נתקע", 4), ("השלב הבא", 3),
]
READY = {1, 2, 3, 4, 5, 6}  # פרקים שכבר כתובים


def header(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="c-header">
            <a href="index.html" class="c-logo"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>
            <nav class="c-nav">{links}</nav>
            <a href="service.html" class="btn sm">התחל ללמוד</a>
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
        f'<a href="guide-{i if i in READY else 1}.html"><span class="dot{" on" if i == 1 else ""}"></span>{i}. {name}</a>'
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
    document.addEventListener('click', function (e) {
        var img = e.target.closest ? e.target.closest('.fshot img') : null;
        if (!img) return;
        var o = document.createElement('div'); o.className = 'lightbox';
        o.innerHTML = '<img src="' + img.src + '" alt="">'; o.onclick = function () { o.remove(); };
        document.body.appendChild(o);
    });
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


def build_chapter(n, lead, rows, note, extra="", flow=""):
    name, mins = CHAPTERS[n - 1]
    parts, k = [], 0
    for a, b in rows:
        if a is None:  # כותרת מפרידה, והמספור מתחיל מחדש
            parts.append(f'<li class="rows-sep">{b}</li>'); k = 0
        else:
            k += 1
            parts.append(f'<li class="row"><span class="tile">{k}</span>{a}<small>{b}</small></li>')
    row_html = "".join(parts)
    rows_block = f'<ol class="rows">{row_html}</ol>' if rows else ""
    nxt = f' data-next="guide-{n + 1}.html"' if (n + 1) in READY else ""
    body = f'''    <main class="wrap full stack guide-main" style="padding-top:14px">
        <div class="course">
            {burger("guide-1.html")}
            {sidebar(n)}
            <article class="card lesson">
                <h1>{name}</h1>
                {f'<p class="lead">{lead}</p>' if lead else ''}
                {rows_block}{flow}{extra}
                <div class="lesson-end"><span>{note}</span><button type="button" class="btn btn-brand" id="guide-done"{nxt}>סיימתי, לפרק הבא ←</button></div>
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


def flow(steps):
    """תרשים זרימה: כל שלב = טקסט + צילום מסך. אם הקובץ עוד לא קיים, מוצג מקום ריק."""
    out = []
    for i, (title, text, img) in enumerate(steps, 1):
        if (SITE / "assets/images/guide" / img).exists():
            shot = f'<div class="fshot"><img src="assets/images/guide/{img}" alt="{title}" loading="lazy"></div>'
        else:
            shot = '<div class="fshot empty"><span>צילום מסך יתווסף כאן</span></div>'
        out.append(f'''<li class="fstep"><div class="ftext"><span class="tile">{i}</span><div><h3>{title}</h3><p>{text}</p></div></div>{shot}</li>''')
        if i < len(steps):
            out.append('<li class="farrow" aria-hidden="true">↓</li>')
    return f'\n                <ol class="flow">{"".join(out)}</ol>'


def when(left, right):
    def col(title, items):
        li = "".join(f"<li>{x}</li>" for x in items)
        return f'<div class="when-col"><h3>{title}</h3><ul>{li}</ul></div>'
    return f'\n                <div class="when">{col(*right)}{col(*left)}</div>'


build_chapter(
    2, "אחד עונה. השני בונה.",
    [("Claude הרגיל", "צ'אט: שואלים, כותבים, מקבלים עצות"),
     ("Claude Code", "עובד על הקבצים שלכם ובונה אתרים"),
     ("איך בוחרים", "צריכים תשובה? Claude. צריכים שיבנה? Claude Code")],
    "שניהם כלולים באותו מנוי",
    extra=when(("משתמשים ב-Claude כש…", ["כותבים מייל או פוסט", "מנתחים מסמך", "מחפשים רעיון או עצה"]),
               ("משתמשים ב-Claude Code כש…", ["בונים אתר", "משנים ומתקנים אתר קיים", "מעלים אותו לאוויר"])),
)


build_chapter(
    3, "צעד אחרי צעד, עם צילום מסך לכל שלב.", [],
    "אם משהו נראה אחרת אצלכם, זה בסדר",
    flow=flow([
        ("נכנסים לאתר", 'בדפדפן נכנסים ל-<a href="https://claude.ai" target="_blank" rel="noopener">claude.ai</a>.', "claude-signup-1.png"),
        ("בוחרים איך נרשמים", "ממשיכים עם Google, או כותבים מייל. עם Google מדלגים על הצעד הבא.", "claude-signup-2.png"),
        ("מקלידים את הקוד מהמייל", "Claude שולח קוד למייל. מעתיקים אותו וכותבים בחלון.", "claude-signup-3.png"),
        ("כותבים שם ומאשרים", 'כותבים את השם שלכם ומאשרים את התנאים.<small class="fnote">יכול להיות שיהיו עוד כמה שאלות, פשוט תזרמו עם זה.</small>', "claude-signup-4.png"),
        ("בוחרים מסלול", 'בשביל לעבוד עם Claude Code, חייבים את המנוי בתשלום. לפחות Pro, 20 דולר בחודש.<small class="fnote">* שימו לב שאתם בוחרים מנוי חודשי ולא שנתי.</small>', "claude-signup-5.png"),
        ("הגעתם!", "רואים את מסך הצ'אט. החשבון מוכן.", "claude-signup-6.png"),
    ]),
)


build_chapter(
    4, "מורידים, מתקינים, נכנסים.", [],
    "אם משהו נראה אחרת אצלכם, זה בסדר",
    flow=flow([
        ("נכנסים לדף ההורדה", 'בדפדפן נכנסים ל-<a href="https://claude.com/download" target="_blank" rel="noopener">claude.com/download</a>.', "claude-install-1.png"),
        ("מורידים לפי המחשב", "לוחצים על Mac או על Windows. הקובץ יורד לבד.", "claude-install-2.png"),
        ("פותחים את הקובץ", "לוחצים עליו פעמיים ומאשרים התקנה.", "claude-install-3.png"),
        ("נכנסים לחשבון", "פותחים את Claude ומתחברים עם אותו מייל מהפרק הקודם.", "claude-install-4.png"),
        ("לוחצים על Code", "למעלה בוחרים בלשונית Code. זה המקום שבו בונים.", "claude-install-5.png"),
    ]),
)


build_chapter(
    5, "GitHub: שם נשמר הפרויקט שלכם. חשבון חינמי.",
    [("מה זה GitHub", "כמו Google Drive, אבל למתכנתים: שם שומרים קבצים ותיקיות"),
     ("למה צריך", "כל הפרויקט שלכם יושב שם, ו-Claude Code עובד עליו"),
     ("כמה עולה", "חשבון חינמי מספיק")],
    "אם משהו נראה אחרת אצלכם, זה בסדר",
    flow='<div class="fgif"><img src="assets/images/guide/github-signup.gif" alt="הרשמה ל-GitHub מההתחלה ועד הסוף" loading="lazy"><span>ככה זה נראה, מההתחלה ועד הסוף</span></div>' + flow([
        ("נכנסים ולוחצים על Sign up", 'בדפדפן נכנסים ל-<a href="https://github.com" target="_blank" rel="noopener">github.com</a> ולוחצים למעלה על Sign up.', "github-1.gif"),
        ("ממשיכים עם Google (מומלץ)", 'לוחצים על Continue with Google. כך לא צריך סיסמה חדשה.', "github-2.gif"),
        ("בוחרים את חשבון Google", 'בוחרים את המייל שלכם מהרשימה.', "github-3.gif"),
        ("הגעתם!", 'רואים את הדף הראשי של GitHub. החשבון מוכן.', "github-4.gif"),
    ]),
)


build_chapter(
    6, "",
    [("ריפו (Repo) ב-GitHub", "תיקייה של פרויקט שמכילה את כל הקוד והקבצים שלו"),
     ("היסטוריה", "הריפו שומר גם את כל השינויים בקוד, אפשר תמיד לחזור אחורה"),
     ("ריפו אחד לכל פרויקט", "לא מערבבים פרויקטים באותו ריפו"),
     (None, "דוגמאות"),
     ("אתר תדמית לנגר", "ריפו 1, בשם: carpenter-website"),
     ("מערכת ניהול לקוחות לסלון לק ג'ל", "ריפו 2, בשם: nail-salon-crm"),
     ("וכן הלאה", "פרויקט חדש, ריפו חדש")],
    "ריפו אחד לכל פרויקט",
    flow='<div class="fgif"><img src="assets/images/guide/github-repo.gif" alt="פתיחת ריפו מההתחלה ועד הסוף" loading="lazy"><span>ככה זה נראה, מההתחלה ועד הסוף</span></div>' + flow([
        ("לוחצים על New repository", 'ב-<a href="https://github.com/new" target="_blank" rel="noopener">GitHub</a> לוחצים על הכפתור הירוק New repository.', "github-repo-1.gif"),
        ("נותנים שם לריפו", "שם באנגלית, בלי רווחים. למשל new-website-carpenter.", "github-repo-2.gif"),
        ("בוחרים Private", 'Private אומר שרק אתם רואים אותו.<small class="fnote">אפשר תמיד לשנות אחר כך.</small>', "github-repo-3.gif"),
        ("לוחצים Create repository", "הריפו נוצר. הוא ריק בינתיים, ו-Claude Code ימלא אותו.", "github-repo-4.gif"),
    ]),
)
