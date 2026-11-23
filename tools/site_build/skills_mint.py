"""עמודי הסקילים בעיצוב החדש של האתר (home2.inner_page): ספריית הסקילים (work.html) ועמוד לכל סקיל.
הרצה: python3 tools/site_build/skills_mint.py  (רץ גם בסוף compact_site.py). אחר כך seo_build.py מוסיף הדר, פוטר ו-SEO."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "site")
sys.path.insert(0, HERE)
import home2  # noqa: E402

CSS_VERSION = "54"

SKILLS = [
    {
        "page": "work-single.html",
        "name": "בדיקת אבטחה לאתר ולאפליקציה",
        "short": "בדיקת אבטחה",
        "cat": "אבטחה",
        "desc": "עובר על 34 פרצות אבטחה באתר או באפליקציה שבניתם עם AI, ומחזיר דוח אדום, כתום וירוק בעברית פשוטה.",
        "prompt": "תבדוק לי את האבטחה של האתר",
        "result": "רשימה של כל החורים באתר לפי דחיפות, ומה לתקן קודם.",
        "checks": [
            ("34 בדיקות", "הפרצות הנפוצות באתרים שנבנו עם Lovable, Bolt, Base44 ו-Claude Code."),
            ("דוח בשלושה צבעים", "אדום לתקן עכשיו, כתום לתקן בקרוב, ירוק תקין."),
            ("עברית פשוטה", "כל בעיה מוסברת בלי מונחים טכניים."),
            ("מה לתקן קודם", "הרשימה מסודרת לפי מה שהכי מסוכן."),
        ],
        "src": "https://github.com/openforge-lab/website-security",
        "seo": ("בדיקת אבטחה לאתר ולאפליקציה – סקיל ל-Claude | Free AI",
                "סקיל חינמי ל-Claude שבודק 34 פרצות אבטחה באתר או באפליקציה שבניתם עם AI ונותן דוח אדום / כתום / ירוק בעברית."),
    },
    {
        "page": "work-site-speed.html",
        "name": "בדיקת מהירות לאתר",
        "short": "בדיקת מהירות",
        "cat": "ביצועים",
        "desc": "בודק 69 דברים שמאטים את האתר, כולל איפה השרת יושב ביחס לגולשים בישראל, ומדרג כל תיקון לפי כמה שניות הוא חוסך.",
        "prompt": "האתר שלי איטי, תבדוק",
        "result": "דוח עם מה לתקן קודם, ופרומפט מוכן לכל תיקון.",
        "checks": [
            ("69 בדיקות", "כל מה שגורם לאתר להיטען לאט."),
            ("שרת מול גולשים בישראל", "בודק אם השרת רחוק מדי מהקהל שלכם."),
            ("דירוג לפי שניות", "רואים כמה זמן טעינה כל תיקון חוסך."),
            ("פרומפט לכל תיקון", "מעתיקים ל-Claude והוא מתקן."),
        ],
        "src": "https://github.com/openforge-lab/site-speed",
        "seo": ("בדיקת מהירות לאתר – סקיל ל-Claude | Free AI",
                "סקיל חינמי ל-Claude שבודק 69 דברים שמאטים את האתר ומדרג תיקונים לפי כמה שניות כל אחד חוסך."),
    },
]

STEPS = [
    ("מורידים את הסקיל", "קובץ ZIP אחד, מהעמוד של הסקיל."),
    ("מעלים אותו ל-Claude", "בהגדרות, תחת Skills (סקילים)."),
    ("מפעילים", "לחיצה על המתג ליד הסקיל."),
    ("כותבים בקשה רגילה", "Claude מזהה מתי צריך את הסקיל ומשתמש בו לבד."),
]

FAQ = [
    ("מה זה סקיל?", "חבילת הוראות ש-Claude טוען רק כשצריך אותה. היא מלמדת אותו לעשות משימה אחת כמו מומחה, בלי שתכתבו פרומפט ארוך כל פעם."),
    ("כמה זה עולה?", "כלום. כל הסקילים חינם, צריך רק חשבון באתר (גם הוא חינם)."),
    ("זה בטוח להוריד?", "לכל סקיל יש קישור לקוד המקור ב-GitHub, אז אפשר לראות בדיוק מה יש בו לפני שמתקינים."),
    ("זה עובד גם בקלוד הרגיל, לא רק בקלוד קוד?", "כן. מעלים את הסקיל בהגדרות של Claude והוא זמין בשניהם."),
]


def zip_url(src):
    return src + "/archive/refs/heads/main.zip"


def sec(k, title, body, sid=None):
    return (f'<section class="a2-sec"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}>'
            f'<div class="a2-head"><span class="a2-num" aria-hidden="true">{k:02d}</span><h2>{title}</h2></div>{body}</section>')


def steps_html():
    return '<ol class="sk-steps">' + "".join(
        f'<li><span class="tile">{i}</span><div><b>{t}</b><span>{x}</span></div></li>' for i, (t, x) in enumerate(STEPS, 1)) + '</ol>'


def faq_html():
    return '<div class="faq">' + "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'


def example(s):
    return (f'<div class="sk-ex"><div class="sk-ex-c"><small>כותבים ל-Claude</small><b>"{s["prompt"]}"</b></div>'
            f'<span class="sk-ex-arr" aria-hidden="true">←</span>'
            f'<div class="sk-ex-c dark"><small>מקבלים</small><b>{s["result"]}</b></div></div>')


def card(s):
    return (f'<article class="sk-card" data-cat="{s["cat"]}" data-search="{s["name"]} {s["cat"]} {s["desc"]}">'
            f'<span class="sk-tag">{s["cat"]}</span><h3><a href="{s["page"]}">{s["name"]}</a></h3><p>{s["desc"]}</p>'
            f'<div class="sk-say"><small>כותבים ל-Claude</small>"{s["prompt"]}"</div>'
            f'<div class="sk-btns"><a href="{s["page"]}" class="a2-btn">לפרטים והורדה</a>'
            f'<a href="{s["src"]}" class="a2-btn ghost" target="_blank" rel="noopener">קוד המקור</a></div></article>')


CTA = '''<section class="a2-cta">
                <h2>רוצים לבנות סקיל משלכם?</h2><p>במדריך יש פרק שלם על סקילים, ואיך Claude משתמש בהם.</p>
                <div class="a2-cta-btns"><a href="guide-14.html" class="a2-btn">לפרק על סקילים</a><a href="service.html" class="a2-btn ghost">לקורס החינמי</a></div>
            </section>'''


def visual_chat(s, rows):
    """האיור בפתיחה: בקשה ל-Claude, הסקיל נדלק, ודוח שמתמלא."""
    rr = "".join(f'<div class="sv-row {c}"><i></i><span>{t}</span><em>{m}</em></div>' for c, t, m in rows)
    return (f'<div class="ill sk-vis" aria-hidden="true">'
            f'<div class="sv-ask"><small>אתם כותבים:</small><span>{s["prompt"]}</span></div>'
            f'<div class="sv-on"><span class="sv-dot"></span>הסקיל "{s["short"]}" פעיל</div>'
            f'<div class="sv-rep"><b>הדוח</b>{rr}</div></div>')


VIS = {
    "work-single.html": [("r", "מפתח סודי חשוף בקוד", "לתקן עכשיו"), ("o", "אין הגבלה על ניסיונות כניסה", "בקרוב"),
                         ("g", "חיבור מוצפן (https)", "תקין"), ("g", "סיסמאות נשמרות מוצפנות", "תקין")],
    "work-site-speed.html": [("r", "תמונות כבדות בעמוד הבית", "‎-2.4 שנ׳"), ("o", "השרת יושב באמריקה", "‎-0.8 שנ׳"),
                             ("o", "פונט נטען לפני הטקסט", "‎-0.4 שנ׳"), ("g", "דחיסת קבצים", "תקין")],
}


def library_visual():
    s = SKILLS[0]
    return visual_chat(s, VIS[s["page"]])


SEARCH_JS = '''<script>
(function () {
    var input = document.querySelector('.sk-search'), btns = document.querySelectorAll('.sk-filter [data-filter]');
    var items = document.querySelectorAll('.sk-card'), empty = document.querySelector('.sk-empty'), cat = 'all';
    if (!input) return;
    function run() {
        var q = (input.value || '').trim(), shown = 0;
        items.forEach(function (el) {
            var ok = (cat === 'all' || el.dataset.cat === cat) && (!q || el.dataset.search.indexOf(q) !== -1);
            el.hidden = !ok; if (ok) shown++;
        });
        empty.hidden = shown > 0;
    }
    btns.forEach(function (b) {
        b.addEventListener('click', function () {
            btns.forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-pressed', 'false'); });
            b.classList.add('active'); b.setAttribute('aria-pressed', 'true'); cat = b.dataset.filter; run();
        });
    });
    input.addEventListener('input', run);
})();
</script>'''


def build_library():
    cats = []
    for s in SKILLS:
        if s["cat"] not in cats:
            cats.append(s["cat"])
    filt = '<button type="button" class="active" aria-pressed="true" data-filter="all">הכל</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-filter="{c}">{c}</button>' for c in cats)
    tools = (f'<div class="sk-tools"><input type="search" class="sk-search" placeholder="חיפוש סקיל, למשל: אבטחה" aria-label="חיפוש סקיל">'
             f'<div class="sk-filter" role="group" aria-label="קטגוריות">{filt}</div></div>')
    grid = f'<div class="sk-grid">{"".join(card(s) for s in SKILLS)}</div><p class="sk-empty" hidden>אין עדיין סקיל כזה. עוד סקילים בדרך.</p>'
    what = ('<p>סקיל הוא כמו דף הוראות שמדביקים למומחה על השולחן. Claude קורא אותו רק כשהבקשה שלכם מתאימה, ואז עובד לפי השיטה שכתובה בו.</p>'
            '<div class="duo"><div class="duo-c"><span class="duo-tag">בלי סקיל</span><h3>פרומפט ארוך כל פעם</h3><p>צריך לזכור מה לבקש, ובכל פעם יוצא קצת אחרת.</p></div>'
            '<div class="duo-c hl"><span class="duo-tag">עם סקיל</span><h3>שורה אחת</h3><p>"תבדוק לי את האבטחה של האתר", ו-Claude עובר על אותן 34 בדיקות כל פעם.</p></div></div>')
    main = f'''<main class="a2 sk">
        <div class="a2-wrap a2-body">
            {sec(1, "הסקילים", tools + grid, "skills")}
            {sec(2, "מה זה סקיל", what)}
            {sec(3, "איך מתקינים", steps_html() + '<p>ההורדה פתוחה לכל מי שיש לו חשבון באתר. ההרשמה חינם ולוקחת פחות מדקה.</p>')}
            {sec(4, "שאלות נפוצות", faq_html())}
            {CTA}
        </div>
    </main>'''
    html = home2.inner_page(
        "סקילים לקלוד (Claude Skills) בעברית – להורדה בחינם | Free AI",
        "סקילים מוכנים ל-Claude בעברית, להורדה בחינם: בדיקת אבטחה לאתר, בדיקת מהירות ועוד. כל סקיל עם דוגמה, קוד מקור ומדריך התקנה.",
        f"סקילים · {len(SKILLS)} להורדה חינם", "סקילים מוכנים ל-Claude",
        "סקיל מלמד את Claude לעשות עבודה של מומחה. מורידים בחינם, מתקינים בדקה, וכותבים לו בקשה רגילה.",
        library_visual(), main, btn2=("#skills", "לכל הסקילים", "box"), script=SEARCH_JS, legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "work.html"), "w").write(html)
    print("work.html done")


def build_skill(s):
    checks = '<ul class="rows">' + "".join(f'<li class="row"><span class="tile">{i}</span>{t}<small>{x}</small></li>'
                                           for i, (t, x) in enumerate(s["checks"], 1)) + '</ul>'
    dl = (f'<p>נכנסתם עם החשבון שלכם, אז ההורדה פתוחה. רוצים לראות מה יש בפנים לפני שמתקינים? כל הקוד פתוח ב-GitHub.</p>'
          f'<div class="sk-btns"><a href="{zip_url(s["src"])}" class="a2-btn" download>הורדה חינם (ZIP)</a>'
          f'<a href="{s["src"]}" class="a2-btn ghost" target="_blank" rel="noopener">קוד המקור ב-GitHub</a></div>' + steps_html())
    others = [o for o in SKILLS if o is not s]
    more = sec(4, "עוד סקילים", f'<div class="sk-grid">{"".join(card(o) for o in others)}</div>'
               '<p><a href="work.html">לכל הסקילים</a></p>') if others else ""
    main = f'''<main class="a2 sk">
        <div class="a2-wrap a2-body">
            {sec(1, "מה הסקיל בודק", checks)}
            {sec(2, "דוגמה", example(s))}
            {sec(3, "הורדה והתקנה", dl, "download")}
            {more}
            {CTA}
        </div>
    </main>'''
    title, desc = s["seo"]
    html = home2.inner_page(title, desc, f"סקיל · {s['cat']}", s["name"], s["desc"], visual_chat(s, VIS[s["page"]]), main,
                            btn2=("work.html", "לכל הסקילים", "box"), legacy_v=CSS_VERSION)
    html, n = re.subn(r'href="service"([^>]*>\s*)להתחיל ללמוד בחינם', r'href="#download"\1הורדה חינם', html, count=1)
    assert n == 1
    open(os.path.join(SITE, s["page"]), "w").write(html)
    print(f"{s['page']} done")


def build():
    build_library()
    for s in SKILLS:
        build_skill(s)


if __name__ == "__main__":
    build()
