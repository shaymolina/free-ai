"""עמודי הסקילים בעיצוב החדש של האתר (home2.inner_page): ספריית הסקילים (skills.html) ועמוד לכל סקיל.
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
        "page": "skill-security.html",
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
        "page": "skill-site-speed.html",
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

FAQ = [
    ("מה זה סקיל?", "חבילת הוראות ש-Claude טוען רק כשצריך אותה. היא מלמדת אותו לעשות משימה אחת כמו מומחה, בלי שתכתבו פרומפט ארוך כל פעם."),
    ("כמה זה עולה?", "כלום. כל הסקילים חינם."),
    ("צריך להירשם?", "לא. הסקילים פתוחים לכולם, וההורדה בלחיצה."),
    ("זה בטוח להוריד?", "לכל סקיל יש קישור לקוד המקור ב-GitHub, אז אפשר לראות בדיוק מה יש בו לפני שמתקינים."),
    ("זה עובד גם בקלוד הרגיל, לא רק בקלוד קוד?", "כן. מעלים את הסקיל בהגדרות של Claude והוא זמין בשניהם."),
    ("אילו עוד סקילים כדאי להתקין?", 'ריכזנו <a href="article-claude-skills.html">10 סקילים שכדאי להתקין בקלוד</a>, כולל אלה ש-Anthropic כבר בנתה.'),
]


def zip_url(src):
    return src + "/archive/refs/heads/main.zip"


def sec(k, title, body, sid=None, sub=""):
    head = f"<h2>{title}</h2>" if title else ""
    if sub:
        head += f'<p class="sk-sub">{sub}</p>'
    return (f'<section class="a2-sec"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}>'
            f'<div class="a2-head"><span class="a2-num" aria-hidden="true">{k:02d}</span>{head}</div>{body}</section>')


def cover(s):
    return "assets/images/articles/" + s["page"].removesuffix(".html") + ".webp?v=4"


def card(s, k=0):
    """כרטיס סקיל כמו כרטיס מאמר: תמונת שער צבעונית, והשם בלבן בתחתית."""
    return (f'<a class="ac" href="{s["page"]}" data-search="{s["name"]} {s["cat"]} {s["desc"]}">'
            f'<img src="{cover(s)}" alt="" loading="{"eager" if k < 3 else "lazy"}" decoding="async">'
            f'<span class="ac-b"><h3 class="ac-t">{s["name"]}</h3>'
            f'<span class="ac-m"><span>{s["cat"]}</span><i aria-hidden="true"></i><span>הורדה חינם</span></span></span></a>')


def cards(items):
    return f'<div class="m2-arts">{"".join(card(s, k) for k, s in enumerate(items))}</div>'


def shot(src, alt):
    return f'<img class="sk-st-img" src="assets/images/guide/{src}" alt="{alt}" loading="lazy">'


INSTALL = [
    ("מורידים את הסקיל", ["בעמוד של הסקיל לוחצים על \"הורדה חינם\" ומקבלים קובץ ZIP אחד. לא צריך לפתוח אותו."], None),
    ("מעלים אותו ל-Claude", ["בהגדרות של Claude נכנסים ל-Customize, בוחרים Skills (סקילים), ולוחצים על Add (הוספה). שם בוחרים את הקובץ שהורדתם."],
     ("settings-skills.png", "מסך הסקילים בהגדרות של Claude")),
    ("משתמשים בו", ["כותבים בקשה רגילה, ו-Claude מפעיל את הסקיל לבד כשהוא מתאים. רוצים להפעיל אותו בכוח? כותבים / ואת שם הסקיל."],
     ("skill-slash.png", "הפעלת סקיל עם / בתיבת הכתיבה")),
]


def install_html():
    out = []
    for k, (t, paras, img) in enumerate(INSTALL, 1):
        body = "".join(f"<p>{x}</p>" for x in paras)
        out.append(f'<li><div class="sk-st-t"><h3>{k}. {t}</h3>{body}</div>{shot(*img) if img else ""}</li>')
    return f'<ol class="sk-steps">{"".join(out)}</ol>'


def faq_html():
    return '<div class="faq">' + "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'


CTA = """<section class="a2-band a2-cta"><div class="a2-wrap a2-pad">
            <div><h2>רוצים לבנות סקיל משלכם?</h2><p>במדריך יש פרק שלם על סקילים, ואיך Claude משתמש בהם.</p></div>
            <div class="a2-cta-btns"><a href="guide-14.html" class="a2-btn">לפרק על סקילים</a><a href="course.html" class="a2-btn ghost">לקורס החינמי</a></div>
        </div></section>"""

HERO_SHOT = '<img class="sk-full shot" src="assets/images/skills/claude-plugins.webp" alt="מסך התוספות והסקילים ב-Claude" decoding="async">'

SEARCH_JS = """<script>
(function () {
    var input = document.querySelector('.sk-search');
    var items = document.querySelectorAll('.sk-list .ac'), empty = document.querySelector('.sk-empty');
    if (!input) return;
    input.addEventListener('input', function () {
        var q = (input.value || '').trim(), shown = 0;
        items.forEach(function (el) {
            var ok = !q || el.dataset.search.indexOf(q) !== -1;
            el.hidden = !ok; if (ok) shown++;
        });
        empty.hidden = shown > 0;
    });
})();
</script>"""


def build_library():
    find = ('<label class="sk-find">' + home2.icon("search", "sk-i") +
            '<input type="search" class="sk-search" placeholder="חיפוש סקיל" aria-label="חיפוש סקיל"></label>')
    main = f"""<main class="a2 sk">
        <section class="a2-more sk-list" id="skills"><div class="a2-wrap a2-pad">
            <div class="a2-band-head"><h2>כל הסקילים.</h2>{find}</div>
            {cards(SKILLS)}
            <p class="sk-empty" hidden>אין עדיין סקיל כזה. עוד סקילים בדרך.</p>
        </div></section>
        <div class="a2-band"><div class="a2-wrap"><div class="a2-body">
            {sec(1, "איך מתקינים", install_html())}
            {sec(2, "שאלות נפוצות", faq_html())}
        </div></div></div>
        {CTA}
    </main>"""
    html = home2.inner_page(
        "סקילים לקלוד (Claude Skills) בעברית – להורדה בחינם | Free AI",
        "סקילים מוכנים ל-Claude בעברית, להורדה בחינם: בדיקת אבטחה לאתר, בדיקת מהירות ועוד. כל סקיל עם דוגמה, קוד מקור ומדריך התקנה.",
        "", "סקילים",
        "סקיל מלמד את Claude לעשות עבודה של מומחה. מורידים בחינם, מעלים ל-Claude, וכותבים לו בקשה רגילה.",
        HERO_SHOT, main, btn2=("#skills", "לכל הסקילים", "box"), script=SEARCH_JS, legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "skills.html"), "w").write(html)
    print("skills.html done")


def build_skill(s):
    checks = '<dl class="sk-dl">' + "".join(f'<div><dt>{t}</dt><dd>{x}</dd></div>' for t, x in s["checks"]) + '</dl>'
    example = (f'<div class="tbl-wrap"><table class="tbl"><tbody>'
               f'<tr><td><b>כותבים ל-Claude</b></td><td>"{s["prompt"]}"</td></tr>'
               f'<tr><td><b>מקבלים</b></td><td>{s["result"]}</td></tr></tbody></table></div>')
    dl = (f'<div class="sk-btns"><a href="{zip_url(s["src"])}" class="a2-btn" download>הורדה חינם (ZIP)</a>'
          f'<a href="{s["src"]}" class="a2-btn ghost" target="_blank" rel="noopener">קוד המקור ב-GitHub</a></div>' + install_html())
    others = [o for o in SKILLS if o is not s]
    more = ("""<section class="a2-band a2-more"><div class="a2-wrap a2-pad">
            <div class="a2-band-head"><h2>עוד סקילים</h2><a href="skills.html" class="a2-link">לכל הסקילים ←</a></div>"""
            + cards(others) + "</div></section>") if others else ""
    main = f"""<main class="a2 sk">
        <div class="a2-wrap"><div class="a2-body">
            {sec(1, "מה הסקיל בודק", checks)}
            {sec(2, "דוגמה", example)}
            {sec(3, "הורדה והתקנה", dl, "download")}
        </div></div>
        {more}
        {CTA}
    </main>"""
    title, desc = s["seo"]
    vis = f'<img class="sk-full" src="{cover(s).replace(".webp?", "-wide.webp?")}" alt="" decoding="async">'
    html = home2.inner_page(title, desc, "", s["name"], s["desc"], vis, main,
                            btn2=("skills.html", "לכל הסקילים", "box"), legacy_v=CSS_VERSION)
    html, n = re.subn(r'href="(?:course|guide-1(?:\.html)?)"([^>]*>\s*)להתחיל ללמוד בחינם', r'href="#download"\1הורדה חינם', html, count=1)
    assert n == 1
    open(os.path.join(SITE, s["page"]), "w").write(html)
    print(f"{s['page']} done")


def build():
    build_library()
    for s in SKILLS:
        build_skill(s)


if __name__ == "__main__":
    build()
