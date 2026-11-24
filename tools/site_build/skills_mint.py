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


def sec(k, title, body, sid=None, sub=""):
    head = f"<h2>{title}</h2>" if title else ""
    if sub:
        head += f'<p class="sk-sub">{sub}</p>'
    return (f'<section class="a2-sec"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}>'
            f'<div class="a2-head"><span class="a2-num" aria-hidden="true">{k:02d}</span>{head}</div>{body}</section>')


def svg(name):
    return home2.icon(name, "sk-i")


def feats(items, numbered=False):
    """שורת עמודות כמו בדף הבית: אייקון בריבוע לבן, משפט מודגש ואחריו הסבר אפור, קו מקווקו בין עמודות."""
    out = []
    for k, (ic, t, x) in enumerate(items, 1):
        mark = f'<span class="sk-n">{k}</span>' if numbered else svg(ic)
        out.append(f'<li><span class="sk-sq">{mark}</span><p><b>{t}</b> {x}</p></li>')
    return f'<ul class="sk-feats c{len(items)}">{"".join(out)}</ul>'


STEP_ICONS = ["up", "box", "gear", "chat"]


def steps_html():
    return feats([(STEP_ICONS[i], t, x) for i, (t, x) in enumerate(STEPS)], numbered=True)


def faq_html():
    return '<div class="faq">' + "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'


ICO = {
    "אבטחה": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    "ביצועים": '<path d="M4 15a8 8 0 1 1 16 0"/><path d="m12 15 4-5"/><circle cx="12" cy="15" r="1.2"/>',
}


def ico(cat):
    return f'<svg class="sk-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICO[cat]}</svg>'


VIS = {
    "work-single.html": [("r", "מפתח סודי חשוף בקוד", "לתקן עכשיו"), ("o", "אין הגבלה על ניסיונות כניסה", "בקרוב"),
                         ("g", "חיבור מוצפן (https)", "תקין"), ("g", "סיסמאות נשמרות מוצפנות", "תקין")],
    "work-site-speed.html": [("r", "תמונות כבדות בעמוד הבית", "‎-2.4 שנ׳"), ("o", "השרת יושב באמריקה", "‎-0.8 שנ׳"),
                             ("o", "פונט נטען לפני הטקסט", "‎-0.4 שנ׳"), ("g", "דחיסת קבצים", "תקין")],
}


def report(s, n=4):
    """דוח קטן בחלון לבן: שורה לכל ממצא, נקודה בצבע ותווית."""
    rows = "".join(f'<div class="sk-row {c}"><i></i><span>{t}</span><em>{m}</em></div>' for c, t, m in VIS[s["page"]][:n])
    return f'<div class="sk-win"><div class="sk-bar"><span class="sk-ic">{ico(s["cat"])}</span><b>{s["short"]}</b><em>הדוח</em></div>{rows}</div>'


def card(s):
    """כרטיס סקיל בסגנון כרטיסי דף הבית: משטח בז' עם איור, ומתחתיו שם, משפט וקישור."""
    return (f'<a class="sk-card" href="{s["page"]}" data-search="{s["name"]} {s["cat"]} {s["desc"]}">'
            f'<span class="sk-art" aria-hidden="true">{report(s, 3)}</span>'
            f'<span class="sk-cap"><h3>{s["name"]}</h3><span class="sk-desc">{s["desc"]}</span>'
            f'<span class="sk-go">לפרטים והורדה {svg("chev-l")}</span></span></a>')


CTA = '''<section class="a2-band a2-cta"><div class="a2-wrap a2-pad">
            <div><h2>רוצים לבנות סקיל משלכם?</h2><p>במדריך יש פרק שלם על סקילים, ואיך Claude משתמש בהם.</p></div>
            <div class="a2-cta-btns"><a href="guide-14.html" class="a2-btn">לפרק על סקילים</a><a href="service.html" class="a2-btn ghost">לקורס החינמי</a></div>
        </div></section>'''


def hero_library():
    """האיור בפתיחה: חלון של Claude. בלי סקיל, פרומפט ארוך ומחוק. עם סקיל, שורה אחת."""
    return ('<div class="ill sk-hero" aria-hidden="true"><div class="sk-win">'
            '<div class="sk-bar"><span class="sk-dots"><i></i><i></i><i></i></span><b>Claude</b></div>'
            '<div class="sk-msg old"><small>בלי סקיל</small><p>תבדוק את האתר שלי, תסתכל על המפתחות, על הכניסה, על ההרשאות, על הטפסים, '
            'על החיבור למסד הנתונים, ותכתוב לי דוח לפי דחיפות, ותסביר בעברית פשוטה, ו...</p></div>'
            f'<div class="sk-msg new"><small>עם סקיל</small><p>"תבדוק לי את האבטחה של האתר"</p>'
            f'<span class="sk-on">{ico("אבטחה")}הסקיל "בדיקת אבטחה" עובד</span></div>'
            f'<div class="sk-ok">{svg("check")}אותן 34 בדיקות, כל פעם</div>'
            '</div></div>')


def hero_skill(s):
    """האיור בפתיחה של עמוד סקיל: הבקשה, ומתחתיה הדוח."""
    return (f'<div class="ill sk-hero" aria-hidden="true"><div class="sk-ask"><small>אתם כותבים</small>"{s["prompt"]}"</div>{report(s)}</div>')


SEARCH_JS = '''<script>
(function () {
    var input = document.querySelector('.sk-search');
    var items = document.querySelectorAll('.sk-card'), empty = document.querySelector('.sk-empty');
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
</script>'''


def build_library():
    find = ('<label class="sk-find">' + svg("search") +
            '<input type="search" class="sk-search" placeholder="חיפוש סקיל, למשל: אבטחה" aria-label="חיפוש סקיל"></label>')
    grid = f'<div class="sk-grid">{"".join(card(s) for s in SKILLS)}</div><p class="sk-empty" hidden>אין עדיין סקיל כזה. עוד סקילים בדרך.</p>'
    what = feats([
        ("file", "דף הוראות למומחה.", "סקיל אומר ל-Claude בדיוק איך לעשות משימה אחת, צעד אחרי צעד."),
        ("spark", "נדלק רק כשצריך.", "Claude קורא אותו כשהבקשה שלכם מתאימה, ולא לפני."),
        ("check", "אותה תוצאה כל פעם.", "לא צריך לזכור מה לבקש. שורה אחת מספיקה."),
    ])
    main = f'''<main class="a2 sk">
        <div class="a2-wrap"><div class="a2-body">
            {sec(1, "", find + grid, "skills")}
            {sec(2, "מה זה סקיל", what, sub="יכולת מוכנה ש-Claude מוסיף לעצמו.")}
            {sec(3, "איך מתקינים", steps_html(), sub="ארבעה צעדים, פחות מדקה. ההורדה פתוחה לכל מי שנרשם, וההרשמה חינם.")}
            {sec(4, "שאלות נפוצות", faq_html())}
        </div></div>
        {CTA}
    </main>'''
    html = home2.inner_page(
        "סקילים לקלוד (Claude Skills) בעברית – להורדה בחינם | Free AI",
        "סקילים מוכנים ל-Claude בעברית, להורדה בחינם: בדיקת אבטחה לאתר, בדיקת מהירות ועוד. כל סקיל עם דוגמה, קוד מקור ומדריך התקנה.",
        "", "סקילים",
        "סקיל מלמד את Claude לעשות עבודה של מומחה. מורידים בחינם, מתקינים בדקה, וכותבים לו בקשה רגילה.",
        hero_library(), main, btn2=("#skills", "לכל הסקילים", "box"), script=SEARCH_JS, legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "work.html"), "w").write(html)
    print("work.html done")


def build_skill(s):
    checks = feats([("check", t + ".", x) for t, x in s["checks"]], numbered=True)
    example = (f'<div class="sk-duo"><div class="sk-art"><div class="sk-ask"><small>כותבים ל-Claude</small>"{s["prompt"]}"</div></div>'
               f'<div class="sk-art">{report(s, 3)}</div></div>'
               f'<div class="sk-duo cap"><p><b>כותבים</b> בקשה רגילה, בעברית.</p><p><b>מקבלים</b> {s["result"]}</p></div>')
    dl = (f'<div class="sk-btns"><a href="{zip_url(s["src"])}" class="a2-btn" download>הורדה חינם (ZIP)</a>'
          f'<a href="{s["src"]}" class="a2-btn ghost" target="_blank" rel="noopener">קוד המקור ב-GitHub</a></div>' + steps_html())
    others = [o for o in SKILLS if o is not s]
    more = sec(4, "עוד סקילים", f'<div class="sk-grid">{"".join(card(o) for o in others)}</div>') if others else ""
    main = f'''<main class="a2 sk">
        <div class="a2-wrap"><div class="a2-body">
            {sec(1, "מה הסקיל בודק", checks)}
            {sec(2, "דוגמה", example)}
            {sec(3, "הורדה והתקנה", dl, "download", sub="רוצים לראות מה יש בפנים לפני שמתקינים? כל הקוד פתוח ב-GitHub.")}
            {more}
        </div></div>
        {CTA}
    </main>'''
    title, desc = s["seo"]
    html = home2.inner_page(title, desc, "", s["name"], s["desc"], hero_skill(s), main,
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
