"""Free AI – העיצוב המצומצם. בונה את עמודי האתר מאפס, בלי התבנית הכבדה.

כרגע: דף הבית (index.html) והמדריך (guide-N.html).
הרצה: cd tools/site_build && python3 compact_site.py
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"
CSS_VERSION = "25"
COUPON = "RVJ34jcn4j1"

NAV = [("index.html", "דף הבית"), ("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים")]

# שם הפרק, דקות קריאה
CHAPTERS = [
    ("לפני שמתחילים", 2), ("Claude מול Claude Code", 3), ("פותחים חשבון Claude", 4),
    ("מתקינים את האפליקציה", 5), ("פותחים GitHub", 4), ("מה זה ריפו ופותחים אחד", 5), ("היכרות ראשונה עם Claude", 3), ("ענן או מחשב", 3), ("המוח של Claude", 3), ("כמה חופש נותנים לו", 3), ("מד הדלק", 2), ("הפרויקט הראשון", 8), ("מעלים לאוויר", 5),
    ("פותחים 4CODE", 4), ("Supabase, כן או לא", 3),
    ("איך מדברים עם Claude Code", 4), ("סדר ובטיחות", 4), ("כשמשהו נתקע", 4), ("השלב הבא", 3),
]
READY = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}  # פרקים שכבר כתובים


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


def rows_html(rows):
    parts, k = [], 0
    for a, b in rows:
        if a is None:  # כותרת מפרידה, והמספור מתחיל מחדש
            parts.append(f'<li class="rows-sep">{b}</li>'); k = 0
        else:
            k += 1
            parts.append(f'<li class="row"><span class="tile">{k}</span>{a}<small>{b}</small></li>')
    return f'<ol class="rows">{"".join(parts)}</ol>' if rows else ""


def split(img, alt, rows):
    """תמונה ולידה ההסברים, עם קו באמצע שאפשר לגרור ימינה ושמאלה."""
    return f'''<div class="split">{rows_html(rows)}<div class="split-bar" role="separator" aria-label="גרירה לשינוי הגודל" tabindex="0"></div><div class="fshot map"><img src="{img}" alt="{alt}"></div></div>'''


def build_chapter(n, lead, rows, note, extra="", flow="", top=""):
    name, mins = CHAPTERS[n - 1]
    rows_block = rows_html(rows)
    nxt = f' data-next="guide-{n + 1}.html"' if (n + 1) in READY else ""
    body = f'''    <main class="wrap full stack guide-main" style="padding-top:14px">
        <div class="course">
            {burger("guide-1.html")}
            {sidebar(n)}
            <article class="card lesson">
                <h1>{name}</h1>
                {f'<p class="lead">{lead}</p>' if lead else ''}
                {top}{rows_block}{flow}{extra}
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
        if img.endswith(".mp4") and (SITE / "assets/images/guide" / img).exists():
            shot = f'<div class="fshot"><video src="assets/images/guide/{img}" muted loop playsinline autoplay preload="metadata" aria-label="{title}"></video></div>'
        elif (SITE / "assets/images/guide" / img).exists():
            shot = f'<div class="fshot"><img src="assets/images/guide/{img}" alt="{title}" loading="lazy"></div>'
        else:
            shot = '<div class="fshot empty"><span>צילום מסך יתווסף כאן</span></div>'
        out.append(f'''<li class="fstep"><div class="ftext"><span class="tile">{i}</span><div><h3>{title}</h3><p>{text}</p></div></div>{shot}</li>''')
        if i < len(steps):
            out.append('<li class="farrow" aria-hidden="true">↓</li>')
    return f'\n                <ol class="flow">{"".join(out)}</ol>'


def fullvid(src, alt):
    return f'\n                <div class="fvid"><span>ככה זה נראה, מההתחלה ועד הסוף. לחיצה עוצרת, לחיצה נוספת ממשיכה.</span><video src="{src}" muted loop playsinline autoplay preload="metadata" aria-label="{alt}"></video></div>'


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
    [("ריפו (Repo) ב-GitHub", "תיקייה של פרויקט שמכילה את כל הקוד והקבצים שלו"),
     ("היסטוריה", "הריפו שומר גם את כל השינויים בקוד, אפשר תמיד לחזור אחורה"),
     ("ריפו אחד לכל פרויקט", "לא מערבבים פרויקטים באותו ריפו"),
     (None, "דוגמאות"),
     ("אתר תדמית לנגר", "ריפו 1, בשם: carpenter-website"),
     ("מערכת ניהול לקוחות לסלון לק ג'ל", "ריפו 2, בשם: nail-salon-crm"),
     ("וכן הלאה", "פרויקט חדש, ריפו חדש")],
    "ריפו אחד לכל פרויקט",
    flow=flow([
        ("לוחצים על New repository", 'ב-<a href="https://github.com/new" target="_blank" rel="noopener">GitHub</a> לוחצים על הכפתור הירוק New repository.', "github-repo-1.mp4"),
        ("נותנים שם לריפו", "שם באנגלית, בלי רווחים. למשל new-website-carpenter.", "github-repo-2.mp4"),
        ("בוחרים Private", 'Private אומר שרק אתם רואים אותו.<small class="fnote">אפשר תמיד לשנות אחר כך.</small>', "github-repo-3.mp4"),
        ("לוחצים Create repository", "הריפו נוצר. הוא ריק בינתיים, ו-Claude Code ימלא אותו.", "github-repo-4.mp4"),
    ]),
    extra=fullvid("assets/images/guide/github-repo.mp4", "פתיחת ריפו מההתחלה ועד הסוף"),
)


build_chapter(
    7, "לפני שבונים, מכירים את הכפתורים. כל מספר בתמונה מוסבר ליד.", [],
    "בפרקים הבאים מכירים כל כפתור לעומק",
    top=split("assets/images/guide/claude-map.png", "המסך של Claude Code עם מספרים", [
     ("Code", "הלשונית שבה בונים. תמיד בוחרים בה"),
     ("New", "פותחים שיחה חדשה עם Claude"),
     ("התיבה", "פה כותבים ל-Claude מה רוצים, בעברית רגילה"),
     ("הענן", "איפה Claude עובד"),
     ("Repo", "על איזה פרויקט עובדים, כלומר איזו תיקייה"),
     ("Opus 5.5", "המוח של Claude"),
     ("Auto", "כמה חופש נותנים לו"),
     ("העיגול", "מד הדלק: כמה נשאר מהמנוי")]),
)


build_chapter(
    8, "Claude יכול לעבוד בשני מקומות. אנחנו בוחרים בענן.",
    [("מחשב (Local)", "Claude עובד אצלכם בבית, על המחשב שלכם. מכבים את המחשב, והוא נעצר"),
     ("ענן (Cloud)", "Claude עובד במחשב של Claude באינטרנט. אפשר לכבות את המחשב שלכם"),
     ("מה בוחרים", "תמיד ענן. ככה לא צריך להתקין כלום")],
    "רואים ענן ליד הכפתור? אתם במקום הנכון",
    flow=flow([
        ("ככה נראה ענן", "למטה משמאל יש ציור של ענן. אם הוא שם, הכל טוב.", "claude-code-cloud.png"),
        ("ככה נראה מחשב", 'אם כתוב This computer, Claude עובד על המחשב שלכם. לוחצים ובוחרים ענן.', "claude-code-local.png"),
    ]),
)


build_chapter(
    9, "כמו לבחור איזה עוזר עובד אתכם היום.",
    [("Opus", "העוזר הכי חכם. טוב לעבודות גדולות, אבל שורף יותר מהמנוי"),
     ("Sonnet", "חכם ומהיר. מתאים לרוב העבודה"),
     ("Haiku", "הכי זריז. מתאים לדברים קטנים"),
     ("Effort", "כמה זמן העוזר חושב לפני שעונה. Medium זה מספיק")],
    "לא בטוחים? משאירים כמו שזה",
    flow=flow([
        ("איפה בוחרים", "לוחצים על שם המוח למטה מימין, ובוחרים מהרשימה.", "claude-models.png"),
    ]),
)


build_chapter(
    10, "כמו לתת למישהו מפתח לבית. כמה מותר לו לעשות בלי לשאול?",
    [("Auto", "Claude מסתדר לבד ושואל רק כשבאמת צריך. מתחילים עם זה"),
     ("Accept edits", "מותר לו לשנות קבצים בלי לשאול אתכם"),
     ("Plan", "קודם הוא מספר מה הוא מתכנן, ובונה רק אחרי שאמרתם כן")],
    "בהתחלה משאירים Auto",
    flow=flow([
        ("איפה בוחרים", "לוחצים על Auto למטה, ובוחרים מהרשימה.", "claude-permissions.png"),
    ]),
)


build_chapter(
    11, "המנוי עובד כמו חבילת גלישה בטלפון. יש כמות, והיא מתמלאת מחדש.",
    [("כל 5 שעות", "יש כמות לעבודה. היא מתחילה לרוץ מההודעה הראשונה"),
     ("כל שבוע", "יש גם כמות לכל השבוע"),
     ("נגמר?", "מחכים קצת, והכמות מתמלאת מחדש")],
    "שווה להציץ מדי פעם",
    flow=flow([
        ("איפה רואים", "לוחצים על העיגול הקטן בפינה למטה. רואים כמה כבר נוצל.", "claude-usage.png"),
    ]),
)
