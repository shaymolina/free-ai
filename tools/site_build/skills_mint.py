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
            f'<div class="a2-head"><span class="a2-num" aria-hidden="true">{k:02d}</span>{f"<h2>{title}</h2>" if title else ""}</div>{body}</section>')


def steps_html():
    return '<ol class="sk-steps">' + "".join(
        f'<li><span class="tile">{i}</span><div><b>{t}</b><span>{x}</span></div></li>' for i, (t, x) in enumerate(STEPS, 1)) + '</ol>'


def faq_html():
    return '<div class="faq">' + "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'


def example(s):
    return (f'<div class="sk-ex"><div class="sk-ex-c"><small>כותבים ל-Claude</small><b>"{s["prompt"]}"</b></div>'
            f'<span class="sk-ex-arr" aria-hidden="true">←</span>'
            f'<div class="sk-ex-c dark"><small>מקבלים</small><b>{s["result"]}</b></div></div>')


ICO = {
    "אבטחה": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    "ביצועים": '<path d="M4 15a8 8 0 1 1 16 0"/><path d="m12 15 4-5"/><circle cx="12" cy="15" r="1.2"/>',
}


def ico(cat):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICO[cat]}</svg>'


def card(s):
    return (f'<a class="sk-card" href="{s["page"]}" data-search="{s["name"]} {s["cat"]} {s["desc"]}">'
            f'<span class="sk-top"><span class="sk-ico">{ico(s["cat"])}</span><span class="sk-cat">{s["cat"]}</span></span>'
            f'<h3>{s["name"]}</h3><p>{s["desc"]}</p>'
            f'<span class="sk-say">"{s["prompt"]}"</span>'
            f'<span class="sk-go">לפרטים והורדה <i aria-hidden="true">←</i></span></a>')


CTA = '''<section class="a2-band a2-cta"><div class="a2-wrap a2-pad">
            <div><h2>רוצים לבנות סקיל משלכם?</h2><p>במדריך יש פרק שלם על סקילים, ואיך Claude משתמש בהם.</p></div>
            <div class="a2-cta-btns"><a href="guide-14.html" class="a2-btn">לפרק על סקילים</a><a href="service.html" class="a2-btn ghost">לקורס החינמי</a></div>
        </div></section>'''


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


# ---------------------------------------------------------------- 5 אפשרויות לאיור בפתיחה של work.html (בעל האתר בוחר)
def vis_settings():
    """1. מסך ההגדרות של Claude: רשימת סקילים עם מתגים שנדלקים."""
    rows = "".join(f'<div class="v1-row"><span class="sk-ico">{ico(s["cat"])}</span><span><b>{s["short"]}</b><small>{s["cat"]}</small></span><i class="v1-sw"></i></div>' for s in SKILLS)
    rows += '<div class="v1-row ghost"><span class="sk-ico">+</span><span><b>הסקיל הבא</b><small>בקרוב</small></span><i class="v1-sw off"></i></div>'
    return f'<div class="ill v1" aria-hidden="true"><div class="v1-bar"><span></span><span></span><span></span><em>Claude · הגדרות</em></div><div class="v1-h">Skills <small>סקילים</small></div>{rows}</div>'


def vis_zip():
    """2. קובץ ZIP שנפתח ומראה את דף ההוראות שבתוכו."""
    return ('<div class="ill v2" aria-hidden="true"><div class="v2-zip"><b>ZIP</b><span>website-security.zip</span></div>'
            '<div class="v2-doc"><div class="v2-t">SKILL.md</div><div class="v2-l"><b>שם:</b> בדיקת אבטחה</div>'
            '<div class="v2-l"><b>מתי להשתמש:</b> כשמבקשים לבדוק אבטחה של אתר</div><div class="v2-l"><b>מה לעשות:</b></div>'
            '<div class="v2-l i">1. לעבור על 34 הבדיקות</div><div class="v2-l i">2. לסמן אדום, כתום, ירוק</div><div class="v2-l i">3. להסביר בעברית פשוטה</div></div></div>')


def vis_compare():
    """3. לפני ואחרי: פרומפט ארוך מול שורה אחת."""
    return ('<div class="ill v3" aria-hidden="true"><div class="v3-c"><small>בלי סקיל</small><p>תבדוק את האתר שלי, תסתכל על המפתחות, על הכניסה, על ההרשאות, על הטפסים, על החיבור למסד הנתונים, ותכתוב לי דוח לפי דחיפות, ותסביר בעברית פשוטה, ו...</p></div>'
            '<div class="v3-c hl"><small>עם סקיל</small><p><b>"תבדוק לי את האבטחה של האתר"</b></p><span class="v3-ok">✓ אותן 34 בדיקות, כל פעם</span></div></div>')


def vis_orbit():
    """4. Claude במרכז, והסקילים מסביבו כמו כלים בחגורה."""
    plus = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>'
    names = [(s["short"], ico(s["cat"])) for s in SKILLS] + [("עוד בדרך", plus)]
    pins = "".join(f'<div class="v4-p p{i}"><span class="sk-ico">{svg}</span>{n}</div>' for i, (n, svg) in enumerate(names))
    return f'<div class="ill v4" aria-hidden="true"><svg class="v4-ring" viewBox="0 0 400 300"><ellipse cx="200" cy="150" rx="170" ry="115"/><ellipse cx="200" cy="150" rx="105" ry="70"/></svg><div class="v4-c">✦<b>Claude</b></div>{pins}</div>'


def vis_shelf():
    """5. מדף של קופסאות סקילים, אחת נשלפת."""
    boxes = "".join(f'<div class="v5-b{" out" if i == 0 else ""}"><span class="sk-ico">{ico(s["cat"])}</span><b>{s["short"]}</b><small>{s["cat"]}</small></div>' for i, s in enumerate(SKILLS))
    boxes += '<div class="v5-b soon"><b>בקרוב</b></div><div class="v5-b soon"><b>בקרוב</b></div>'
    return f'<div class="ill v5" aria-hidden="true"><div class="v5-shelf">{boxes}</div><div class="v5-board"></div><div class="v5-cap">הורדה חינם · ZIP אחד · מתקינים בדקה</div></div>'


VISUALS = [vis_settings, vis_zip, vis_compare, vis_orbit, vis_shelf]


SEARCH_JS = '''<script>
(function () {
    var input = document.querySelector('.sk-search');
    var items = document.querySelectorAll('.sk-card'), empty = document.querySelector('.sk-empty'), count = document.querySelector('.sk-count');
    if (!input) return;
    function run() {
        var q = (input.value || '').trim(), shown = 0;
        items.forEach(function (el) {
            var ok = !q || el.dataset.search.indexOf(q) !== -1;
            el.hidden = !ok; if (ok) shown++;
        });
        empty.hidden = shown > 0;
        count.textContent = shown + ' סקילים';
    }
    input.addEventListener('input', run);
})();
</script>'''


def build_library(visual=None, out="work.html"):
    tools = ('<div class="sk-tools"><label class="sk-find"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">'
             '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
             '<input type="search" class="sk-search" placeholder="חיפוש סקיל, למשל: אבטחה" aria-label="חיפוש סקיל"></label>'
             f'<span class="sk-count">{len(SKILLS)} סקילים</span></div>')
    grid = f'<div class="sk-grid">{"".join(card(s) for s in SKILLS)}</div><p class="sk-empty" hidden>אין עדיין סקיל כזה. עוד סקילים בדרך.</p>'
    what = ('<p>סקיל הוא כמו דף הוראות שמדביקים למומחה על השולחן. Claude קורא אותו רק כשהבקשה שלכם מתאימה, ואז עובד לפי השיטה שכתובה בו.</p>'
            '<div class="duo"><div class="duo-c"><span class="duo-tag">בלי סקיל</span><h3>פרומפט ארוך כל פעם</h3><p>צריך לזכור מה לבקש, ובכל פעם יוצא קצת אחרת.</p></div>'
            '<div class="duo-c hl"><span class="duo-tag">עם סקיל</span><h3>שורה אחת</h3><p>"תבדוק לי את האבטחה של האתר", ו-Claude עובר על אותן 34 בדיקות כל פעם.</p></div></div>')
    main = f'''<main class="a2 sk">
        <div class="a2-wrap"><div class="a2-body">
            {sec(1, "", tools + grid, "skills")}
            {sec(2, "מה זה סקיל", what)}
            {sec(3, "איך מתקינים", steps_html() + '<p>ההורדה פתוחה לכל מי שיש לו חשבון באתר. ההרשמה חינם ולוקחת פחות מדקה.</p>')}
            {sec(4, "שאלות נפוצות", faq_html())}
        </div></div>
        {CTA}
    </main>'''
    html = home2.inner_page(
        "סקילים לקלוד (Claude Skills) בעברית – להורדה בחינם | Free AI",
        "סקילים מוכנים ל-Claude בעברית, להורדה בחינם: בדיקת אבטחה לאתר, בדיקת מהירות ועוד. כל סקיל עם דוגמה, קוד מקור ומדריך התקנה.",
        "", "סקילים",
        "סקיל מלמד את Claude לעשות עבודה של מומחה. מורידים בחינם, מתקינים בדקה, וכותבים לו בקשה רגילה.",
        visual if visual is not None else library_visual(), main, btn2=("#skills", "לכל הסקילים", "box"), script=SEARCH_JS, legacy_v=CSS_VERSION)
    open(os.path.join(SITE, out), "w").write(html)
    print(f"{out} done")


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
        <div class="a2-wrap"><div class="a2-body">
            {sec(1, "מה הסקיל בודק", checks)}
            {sec(2, "דוגמה", example(s))}
            {sec(3, "הורדה והתקנה", dl, "download")}
            {more}
        </div></div>
        {CTA}
    </main>'''
    title, desc = s["seo"]
    html = home2.inner_page(title, desc, "", s["name"], s["desc"], visual_chat(s, VIS[s["page"]]), main,
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
