"""Free AI – העיצוב המצומצם. בונה את עמודי האתר מאפס, בלי התבנית הכבדה.

כרגע: דף הבית (index.html) והמדריך (guide-N.html).
הרצה: cd tools/site_build && python3 compact_site.py
"""
from pathlib import Path
from clean_urls import clean

SITE = Path(__file__).resolve().parents[2] / "site"
CSS_VERSION = "29"
COUPON = "RVJ34jcn4j1"

NAV = [("index.html", "דף הבית"), ("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]

# שם הפרק, דקות קריאה
CHAPTERS = [
    ("לפני שמתחילים", 2), ("קלוד מול קלוד קוד", 3), ("פותחים חשבון קלוד", 4),
    ("מתקינים את האפליקציה", 5), ("פותחים GitHub", 4), ("מה זה ריפו ופותחים אחד", 5), ("היכרות ראשונה עם קלוד", 3), ("מיקום הפרויקט: מחשב או ענן", 3), ("בחירת המודל", 3), ("הרשאות: כמה קלוד עושה לבד", 3), ("כמה נשאר מהמנוי", 2), ("תוספות: איפה מוסיפים יכולות", 3), ("חיבור לשירותים (Connectors)", 3), ("מיומנויות (Skills)", 3), ("חבילות (Plugins)", 3), ("איך מדברים עם קלוד קוד", 4), ("הפרויקט הראשון", 8), ("מעלים לאוויר", 5),
    ("פותחים 4CODE", 4), ("Supabase, כן או לא", 3),
    ("סדר ובטיחות", 4), ("כשמשהו נתקע", 4), ("השלב הבא", 3),
]
READY = set(range(1, 20))  # פרקים שכבר כתובים


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
    return clean(_page(title, desc, body, script, cls))


def _page(title, desc, body, script="", cls=""):
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="author" content="Free AI">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{desc}">
    <link rel="stylesheet" href="assets/fonts/fonts.css?v=20261117">
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
        ("צריך מנוי בתשלום לקלוד?", "כן. קלוד Pro ומעלה."),
        ("צריך ידע קודם?", "לא. מתחילים מאפס."),
        ("כמה זמן לוקח הקורס?", "8 שיעורים קצרים, בקצב שלכם."),
        ("למה צריך להירשם?", "כדי לצפות, להוריד קבצים ולקבל תעודה."),
    ])
    body = f'''    <div class="wrap full">
        <section class="c-hero">
        {header("index.html")}
            <div class="hero-in">
                <div class="hero-text">
                    <h1 class="hero-title"><span class="hero-line"><span class="grad">קורס קלוד קוד בחינם</span>
                        <span class="hero-pill"><img src="assets/images/item/hero-1.svg" alt=""><img src="assets/images/item/hero-2.svg" alt=""><img src="assets/images/item/hero-3.svg" alt=""></span></span></h1>
                    <p>קורס Claude Code בעברית למתחילים, בלי ידע בתכנות: שיעורי וידאו, מדריך כתוב צעד אחרי צעד וסקילים מוכנים להורדה.</p>
                </div>
                <div class="card hero-vid"><video src="assets/images/guide/first-4.mp4" muted loop playsinline autoplay preload="metadata" aria-label="כותבים לקלוד קוד בקשה בעברית, והוא בונה אתר"></video></div>
            </div>
        </section>
    </div>
    <main class="wrap full stack" style="margin-top:16px">
        <div class="three">
            <a href="service.html" class="card pick"><h2>הקורס</h2><p class="muted">8 שיעורי וידאו קצרים, לפי הסדר.</p><span class="go">לקורס ←</span></a>
            <a href="guide-1.html" class="card pick"><h2>המדריך</h2><p class="muted">{len(CHAPTERS)} פרקים קצרים לקריאה, צעד אחרי צעד.</p><span class="go">למדריך ←</span></a>
            <a href="work.html" class="card pick"><h2>סקילים</h2><p class="muted">יכולות מוכנות לקלוד, להורדה בחינם.</p><span class="go">לסקילים ←</span></a>
        </div>
        <h2 class="sec-title">שאלות נפוצות</h2>
        <div class="faq">{faq}</div>
        {FOOTER}
    </main>'''
    (SITE / "index.html").write_text(page(
        "קורס קלוד קוד בחינם בעברית | Free AI",
        "קורס קלוד קוד (Claude Code) בחינם ובעברית למתחילים, בלי ידע בתכנות: שיעורי וידאו, מדריך כתוב וסקילים מוכנים, עד אתר שעובד באוויר.", body))
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
                <h3>המדריך לקלוד קוד</h3>
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


GUIDE_TITLE = {  # כותרת לגוגל לפי מה שאנשים מחפשים (השם בעמוד נשאר כמו שהוא)
    2: "מה זה קלוד קוד? ההבדל בין קלוד לקלוד קוד",
    4: "התקנת קלוד קוד (Claude Code) צעד אחרי צעד",
    5: "מה זה GitHub ואיך פותחים חשבון – מדריך למתחילים",
    14: "סקילים בקלוד (Claude Skills): מה זה ואיך משתמשים",
    16: "איך כותבים פרומפט לקלוד קוד – בלי מילים טכניות",
}

GUIDE_DESC = {
    5: "פותחים חשבון GitHub בחינם, צעד אחרי צעד. זה המקום שבו נשמרים כל הפרויקטים שקלוד קוד בונה.",
    6: "מה זה ריפו (Repo) ב-GitHub, למה כל פרויקט צריך אחד, ואיך פותחים ריפו ראשון בכמה לחיצות.",
}


def build_chapter(n, lead, rows, note, extra="", flow="", top=""):
    name, mins = CHAPTERS[n - 1]
    rows_block = rows_html(rows)
    nxt = f' data-next="guide-{n + 1}"' if (n + 1) in READY else ""
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
        f"{GUIDE_TITLE.get(n, name + ' – המדריך לקלוד קוד')} | Free AI",
        f"פרק {n} במדריך לקלוד קוד למי שלא מתכנת: {lead or GUIDE_DESC.get(n, name)}", body,
        GUIDE_JS % {"total": len(CHAPTERS), "current": n}, cls="guide-page"))
    print(f"guide-{n}.html done")


build_home()
build_chapter(
    1, "שלושה דברים להכין, ואפשר לצאת לדרך.",
    [("מחשב", "Mac או Windows"), ("מייל", "אחד לכל השירותים"), ("כרטיס אשראי", "כ-20 דולר לחודש לקלוד")],
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
        tile = f'<span class="tile">{i}</span>' if len(steps) > 1 else ''
        out.append(f'''<li class="fstep"><div class="ftext">{tile}<div><h3>{title}</h3><p>{text}</p></div></div>{shot}</li>''')
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
    2, "לאותה חברה יש שני כלים. אחד כמו יועץ שעונה לכם, השני כמו בעל מקצוע שבא ובונה.",
    [("קלוד: שיחה", "שואלים ומקבלים תשובה, רעיון או טקסט. הוא לא נוגע בקבצים"),
     ("קלוד קוד: בנייה", "עובד בעצמו על הקבצים של הפרויקט ובונה אתר או מערכת"),
     ("מה אנחנו בוחרים", "קלוד קוד, כי במדריך הזה בונים")],
    "שניהם כלולים באותו מנוי",
    extra=when(("משתמשים בקלוד כש…", ["כותבים מייל או פוסט", "מנתחים מסמך", "מחפשים רעיון או עצה"]),
               ("משתמשים בקלוד קוד כש…", ["בונים אתר", "משנים ומתקנים אתר קיים", "מעלים אותו לאוויר"])),
)


build_chapter(
    3, "החשבון הוא המפתח שלכם לקלוד. פותחים אותו פעם אחת, צעד אחרי צעד.", [],
    "אם משהו נראה אחרת אצלכם, זה בסדר",
    flow=flow([
        ("נכנסים לאתר", 'בדפדפן נכנסים ל-<a href="https://claude.ai" target="_blank" rel="noopener">claude.ai</a>.', "claude-signup-1.png"),
        ("בוחרים איך נרשמים", "ממשיכים עם Google, או כותבים מייל. עם Google מדלגים על הצעד הבא.", "claude-signup-2.png"),
        ("מקלידים את הקוד מהמייל", "קלוד שולח קוד למייל. מעתיקים אותו וכותבים בחלון.", "claude-signup-3.png"),
        ("כותבים שם ומאשרים", 'כותבים את השם שלכם ומאשרים את התנאים.<small class="fnote">יכול להיות שיהיו עוד כמה שאלות, פשוט תזרמו עם זה.</small>', "claude-signup-4.png"),
        ("בוחרים מסלול", 'בשביל לעבוד עם קלוד קוד, חייבים את המנוי בתשלום. לפחות Pro, 20 דולר בחודש.<small class="fnote">* שימו לב שאתם בוחרים מנוי חודשי ולא שנתי.</small>', "claude-signup-5.png"),
        ("הגעתם!", "רואים את מסך הצ'אט. החשבון מוכן.", "claude-signup-6.png"),
    ]),
)


build_chapter(
    4, "האפליקציה היא סדנת העבודה של קלוד קוד על המחשב שלכם. מורידים, מתקינים, נכנסים.", [],
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
    [("מה זה GitHub", "כמו Google Drive, אבל לפרויקטים של קוד: שם שמורים כל הקבצים והתיקיות"),
     ("למה צריך אותו", "קלוד קוד לוקח משם את הפרויקט, עובד עליו ושומר בחזרה"),
     ("מחיר", "חשבון חינמי מספיק")],
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
    8, "איפה הפרויקט שלכם נמצא, ואיפה קלוד עובד עליו. יש שתי אפשרויות.",
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
     ("Accept edits: עריכת קבצים בלי לשאול", "משנה קבצים לבד, אבל עוצר ושואל לפני פעולות אחרות, כמו הרצת פקודות"),
     ("Plan: קודם תוכנית", "מספר מה הוא מתכנן, ובונה רק אחרי שאישרתם"),
     ("מה אנחנו בוחרים", "Auto. כשרוצים לראות קודם מה הוא יעשה, Plan")],
    "אפשר להחליף בכל רגע",
    flow=flow([
        ("איפה מחליפים", "לוחצים על Auto למטה, ובוחרים מהרשימה.", "claude-permissions.png"),
    ]),
)


build_chapter(
    11, "המנוי נותן כמות עבודה מוגבלת, כמו חבילת גלישה. והיא מתמלאת מחדש.",
    [("מגבלת 5 שעות", "כמות לחלון של 5 שעות. החלון מתחיל מההודעה הראשונה"),
     ("מגבלה שבועית", "כמות לכל השבוע. מתאפסת פעם בשבוע"),
     ("נגמר?", "מחכים לאיפוס, או עוברים למודל שמשתמש פחות, כמו Sonnet")],
    "שווה להציץ מדי פעם",
    flow=flow([
        ("איפה רואים", "לוחצים על העיגול הקטן בפינה למטה. רואים כמה כבר נוצל.", "claude-usage.png"),
    ]),
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
        ("איפה רואים ומוסיפים", 'בלשונית Connectors, תחת Yours, רואים מה כבר מחובר. מוסיפים חיבור רשמי תחת Discover, או כלי אחר בכפתור Add.<small class="fnote">כתוב Reconnect? החיבור התנתק. לוחצים ומתחברים שוב.</small>', "settings-connectors.png"),
    ]),
)


build_chapter(
    14, "מיומנות היא כמו חוברת הוראות: קלוד קורא אותה כשמגיעה משימה מתאימה, ועושה אותה בדרך הנכונה.",
    [("מה זה נותן", "תוצאה טובה ואחידה יותר במשימות שחוזרות על עצמן"),
     ("איך זה מופעל", "קלוד פותח אותה לבד כשהיא מתאימה. אפשר גם לקרוא לה בשם עם / בתיבת הכתיבה"),
     ("במה זה שונה מחיבור", "מיומנות היא רק ידע. היא לא נכנסת לשום חשבון שלכם"),
     ("מיומנויות של Anthropic", "מוכנות בלשונית Discover. לוחצים + והן נוספות"),
     ("מיומנויות מאתרים אחרים", "הורדתם מיומנות מאתר אחר? לוחצים על הכפתור הלבן Add ומעלים אותה"),
     (None, "דוגמאות"),
     ("עיצוב אתרים", "קלוד מעצב לפי כללים של מעצבים מקצועיים"),
     ("כתיבה בעברית", "טקסטים שיווקיים בעברית טובה ונכונה"),
     ("קמפיינים בפייסבוק", "הופכת את קלוד לקמפיינר מומחה בפייסבוק")],
    "אפשר להסיר מיומנות בכל רגע",
    flow=flow([
        ("איפה מוסיפים", "בלשונית Skills: מיומנות של Anthropic מוסיפים ב-+ תחת Discover, ומיומנות שהורדתם מעלים בכפתור Add.", "settings-skills.png"),
        ("איך מפעילים בשם", "כותבים / ואת שם המיומנות בתיבת הכתיבה, ובוחרים אותה מהרשימה שקופצת.", "skill-slash.png"),
    ]),
)


build_chapter(
    15, "חבילה היא כמו ארגז כלים: בהתקנה אחת מקבלים כמה מיומנויות, חיבורים ופקודות שעובדים יחד.",
    [("מה זה נותן", "תחום שלם מוכן לעבודה, בלי להרכיב לבד חלק אחרי חלק"),
     ("על מה לשים לב", "מתקינים רק ממקור מוכר. ליד כל חבילה כתוב מי יצר אותה, כמו by Anthropic"),
     (None, "דוגמאות"),
     ("Data", "שאלות על נתונים, טבלאות וגרפים"),
     ("google-workspace", "עבודה עם Google Drive, Docs ו-Sheets")],
    "אפשר להסיר חבילה בכל רגע",
    flow=flow([
        ("איפה מוסיפים", "בלשונית Plugins, תחת Discover, לוחצים על + או על Add.", "settings-plugins.png"),
    ]),
)


build_chapter(
    16, "קלוד קוד עובד לפי מה שכותבים לו. כמו בעל מקצוע: ככל שההסבר ברור יותר, התוצאה קרובה יותר למה שרציתם.",
    [("מה בונים", "סוג הדבר: דף נחיתה, אתר תדמית, מערכת לניהול לקוחות"),
     ("בשביל מי", "העסק, מה הוא עושה ומי הלקוחות שלו"),
     ("מה צריך להופיע", "החלקים שחייבים להיות: שירותים, תמונות, טלפון, טופס יצירת קשר"),
     ("איך זה נראה", "צבעים, סגנון ותחושה, למשל חם, נקי, יוקרתי"),
     ("אפשר לדבר במקום להקליד", "לוחצים על המיקרופון בתיבת הכתיבה ומדברים בעברית"),
     ("אחרי הבנייה הראשונה", "מבקשים שינוי אחד בכל פעם, ובודקים שיצא כמו שרציתם"),
     (None, "דוגמאות"),
     ("בקשה חלשה", "\"תבנה לי אתר\""),
     ("בקשה טובה", "\"תבנה דף נחיתה לנגר. בראש תמונות עבודות וכותרת, אחריהן השירותים: פרגולות, גדרות ושולחנות. בסוף טופס יצירת קשר. צבעים חמים של עץ.\"")],
    "לא צריך מילים טכניות. מסבירים כמו לבן אדם",
)


build_chapter(
    17, "מחברים את GitHub לקלוד, בוחרים את הריפו מפרק 6, וכותבים את הבקשה הראשונה.",
    [("חיבור GitHub", "פעם אחת: נותנים לקלוד אישור להיכנס לחשבון GitHub שלכם"),
     ("התקנת האפליקציה של קלוד", "פעם אחת: מאשרים לקלוד לעבוד על הריפו. בלי זה הריפו לא יופיע ברשימה"),
     ("בחירת הריפו", "בכל משימה חדשה בוחרים על איזה פרויקט עובדים"),
     ("איפה העבודה נשמרת", "קלוד שומר הכול בריפו ב-GitHub. כלום לא הולך לאיבוד")],
    "בפרק הבא מעלים את האתר לאוויר",
    flow=flow([
        ("מחברים את GitHub", 'בהגדרות, בלשונית Connectors, מחפשים GitHub Integration ולוחצים Connect. בדף של GitHub לוחצים Authorize.', "first-1.mp4"),
        ("מתקינים את האפליקציה של קלוד", 'לוחצים על GitHub Integration. ליד Claude GitHub App לוחצים Fix, בוחרים All repositories ומאשרים.<small class="fnote">GitHub ישלח קוד למייל כדי לוודא שזה אתם.</small>', "first-2.mp4"),
        ("בוחרים את הריפו", "במשימה חדשה לוחצים על Repo, כותבים את שם הריפו ובוחרים אותו.", "first-3.mp4"),
        ("כותבים מה לבנות", "כותבים או מדברים את הבקשה, ושולחים. קלוד בונה את האתר ומספר מה עשה.", "first-4.mp4"),
    ]),
)


build_chapter(
    18, "האתר כבר שמור ב-GitHub, אבל רק אתם רואים אותו. להעלות לאוויר זה לשים אותו בכתובת שכל אחד יכול להיכנס אליה.",
    [("אחסון (Hosting)", "מחשב שדלוק תמיד ומציג את האתר לכל מי שנכנס. כמו חנות ברחוב"),
     ("כתובת (דומיין)", "השם שמקלידים בדפדפן כדי להגיע לאתר. כמו שלט על החנות"),
     ("עדכונים", "כל שינוי שקלוד שומר ב-GitHub עולה לאתר לבד"),
     ("מה אנחנו בוחרים", "4CODE: מתחילים בחינם, בעברית, וכל השינויים עולים לאוויר בלחיצה"),
     (None, "דוגמאות"),
     ("כתובת חינמית", "שם-האתר.il.4code.site, מוכנה מיד ובלי לשלם"),
     ("כתובת פרטית", "carpenter.co.il, קונים דרך 4CODE ומחברים לאתר")],
    "בפרק הבא פותחים חשבון ב-4CODE",
)


build_chapter(
    19, "4CODE הוא המקום שבו האתר שלכם יחיה באינטרנט. פותחים חשבון חינמי ויוצרים פרויקט.",
    [("מסלול חינם", "אתר אחד באוויר, בלי לשלם"),
     ("מסלול Pro", "עד 3 אתרים, גיבויים ותמיכה. 9 דולר בחודש"),
     ("מה אנחנו בוחרים", "מתחילים בחינם. עוברים ל-Pro כשיש יותר מאתר אחד")],
    "יש לכם קופון? בפרק 1 יש קופון לחודש ראשון חינם",
    flow=flow([
        ("בוחרים מסלול", 'ב-<a href="https://4code.co.il/pricing" target="_blank" rel="noopener">4code.co.il</a> לוחצים על מסלולים, ובחינם לוחצים "מתחילים בחינם".<small class="fnote">אחר כך ממלאים שם, מייל וטלפון, ומסיימים את ההזמנה.</small>', "4code-1.mp4"),
        ("נכנסים לפלטפורמה", "לוחצים \"התחברות לחשבון\" ומאשרים ל-4code-platform להתחבר.", "4code-2.mp4"),
        ("יוצרים פרויקט", "בפרויקטים לוחצים \"יצירת פרויקט\", נותנים שם ונכנסים אליו.", "4code-3.mp4"),
    ]),
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


def build_article(name, title, desc, mins, body):
    ARTICLES.append((name, title, desc, mins))
    page_body = f'''    <main class="wrap stack c-top">
        {header("articles.html")}
        <article class="card article">
            <h1>{title}</h1>
{body}
            <div class="art-cta"><span>רוצים ללמוד לבנות דברים כאלה בעצמכם? הקורס חינמי.</span><a href="service.html" class="btn">התחל ללמוד</a></div>
        </article>
        {FOOTER}
    </main>'''
    (SITE / name).write_text(page(f"{title} | Free AI", desc, page_body, ARTICLE_JS))
    print(f"{name} done")


def build_articles_index():
    cards = "".join(
        f'<a href="{n}" class="card art-card"><h2>{t}</h2><p class="muted">{d}</p><span class="go">לקריאה ←</span></a>'
        for n, t, d, m in ARTICLES)
    body = f'''    <main class="wrap stack c-top">
        {header("articles.html")}
        <div class="art-head"><h1>מאמרים</h1><p>מדריכים קצרים שאפשר לעשות היום, בלי לדעת לתכנת.</p></div>
        <div class="art-list">{cards}</div>
        {FOOTER}
    </main>'''
    (SITE / "articles.html").write_text(page(
        "מאמרים על בינה מלאכותית ואוטומציה בעברית – Free AI", "מדריכים קצרים בעברית לבנייה ואוטומציה עם בינה מלאכותית, בלי לדעת לתכנת.", body))
    print("articles.html done")


_GS = (SITE / "files/github-drive-backup.gs").read_text()

build_article(
    "article-github-backup.html",
    "גיבוי אוטומטי של כל הפרויקטים מ-GitHub ל-Google Drive",
    "איך מגדירים פעם אחת גיבוי יומי של כל הפרויקטים ב-GitHub לתיקייה בגוגל דרייב, בחינם ובלי לדעת לתכנת.",
    6,
    f'''            <p class="lead">מגדירים פעם אחת, ומאז כל לילה כל הפרויקטים שלכם נשמרים לבד בתיקייה בגוגל דרייב.</p>

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
)

build_articles_index()

# שכבת SEO (canonical, שיתוף, נתונים מובנים, sitemap) – תמיד בסוף הבנייה
import runpy as _runpy
_runpy.run_path(str(Path(__file__).resolve().parents[1] / "seo" / "seo_build.py"), run_name="__main__")
