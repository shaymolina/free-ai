"""עמודי הקורסים בעיצוב החדש (home2.inner_page):
courses.html (כל הקורסים), lovable-1.html (קורס Lovable) ו-course.html (קורס Claude Code, מגיע בקרוב עם הרשמה להודעה).
רץ מתוך compact_site.py. ההרשמה להודעה: כפתור עם data-notify, ש-site/assets/js/auth-gate.js מטפל בו.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "site")
sys.path.insert(0, HERE)
import home2  # noqa: E402
from skills_mint import sec, CSS_VERSION  # noqa: E402

# כל קורס: עמוד, שם, משפט, מצב (זמין / בקרוב), שם התמונה
COURSES = [
    {"page": "lovable-1.html", "name": "קורס Lovable", "desc": "בונים אתרים ואפליקציות עם Lovable, בלי לכתוב קוד.",
     "status": "זמין עכשיו", "img": "course-lovable", "kind": "שיעורי וידאו"},
    {"page": "course.html", "name": "קורס Claude Code", "desc": "בונים עם Claude Code, מהחשבון הראשון ועד אתר באוויר.",
     "status": "בקרוב", "img": "course-claude-code", "kind": "שיעורי וידאו", "soon": True},
]

# המדריכים הכתובים: אותו מבנה. מדריך בלי עמוד (page=None) מוצג אפור עם "בקרוב".
GUIDES = [
    {"page": "guide-1.html", "name": "מדריך Claude Code", "desc": "24 פרקים קצרים, מהחשבון הראשון ועד אתר באוויר.",
     "status": "24 פרקים", "img": "guide-claude-code", "kind": "מדריך כתוב"},
    {"page": None, "name": "מדריך Lovable", "desc": "",
     "status": "בקרוב", "img": "guide-lovable", "kind": "מדריך כתוב", "soon": True},
]

SOON_CSS = "<style>.ac.is-soon img{filter:grayscale(1) brightness(.85)}.ac.is-soon{cursor:default}</style>"

NOTIFY = "claude-code-course"  # השם שנשמר בטבלת progress כ-notify-claude-code-course


def img(name, wide=False):
    return f"assets/images/articles/{name}{'-wide' if wide else ''}.webp?v=4"


def course_cards(items):
    out = []
    for k, c in enumerate(items):
        tag = "a" if c["page"] else "div"
        href = f' href="{c["page"]}"' if c["page"] else ""
        out.append(f'<{tag} class="ac{" is-soon" if c.get("soon") else ""}"{href}>'
                   f'<img src="{img(c["img"])}" alt="" loading="{"eager" if k < 3 else "lazy"}" decoding="async">'
                   f'<span class="ac-b"><h3 class="ac-t">{c["name"]}</h3>'
                   f'<span class="ac-m"><span>{c["status"]}</span><i aria-hidden="true"></i><span>{c["kind"]}</span></span></span></{tag}>')
    return f'{SOON_CSS}<div class="m2-arts">{"".join(out)}</div>'


def faq(items):
    return '<div class="faq">' + "".join(f'<details class="card"><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'


def table(rows):
    body = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><tbody>{body}</tbody></table></div>'


def cta(title, text, btns):
    b = "".join(f'<a href="{h}" class="a2-btn{" ghost" if k else ""}"{f" data-notify={chr(34)}{n}{chr(34)}" if n else ""}>{t}</a>'
                for k, (h, t, n) in enumerate(btns))
    return f"""<section class="a2-band a2-cta"><div class="a2-wrap a2-pad">
            <div><h2>{title}</h2><p>{text}</p></div>
            <div class="a2-cta-btns">{b}</div>
        </div></section>"""


MORE = table([
    ('<a href="guide-1.html">המדריך הכתוב</a>', "24 פרקים קצרים על Claude Code, מהחשבון הראשון ועד אתר באוויר."),
    ('<a href="skills.html">סקילים</a>', "יכולות מוכנות ל-Claude, להורדה בחינם."),
    ('<a href="articles.html">מאמרים</a>', "מדריכים קצרים שאפשר לעשות היום."),
])


# ---------------------------------------------------------------- כל הקורסים
def build_courses():
    main = f"""<main class="a2 sk">
        <section class="a2-more sk-list" id="courses"><div class="a2-wrap a2-pad">
            <div class="a2-band-head"><h2>כל הקורסים.</h2></div>
            {course_cards(COURSES)}
        </div></section>
        <div class="a2-band"><div class="a2-wrap"><div class="a2-body">
            {sec(1, "עוד דרכים ללמוד", MORE)}
            {sec(2, "שאלות נפוצות", faq([
                ("הקורסים באמת בחינם?", "כן. כל הקורסים, המדריכים והסקילים כאן בחינם. על הכלים עצמם (Lovable, Claude) לפעמים צריך מנוי."),
                ("צריך ידע קודם?", "לא. כל קורס מתחיל מאפס, גם למי שלא כתב שורת קוד."),
                ("באיזה קורס להתחיל?", 'רוצים אתר או אפליקציה מהר? <a href="lovable-1.html">קורס Lovable</a>. רוצים לבנות דברים גדולים יותר ולעבוד עם הקבצים שלכם? <a href="course.html">קורס Claude Code</a>, שעולה בשבוע הבא.'),
                ("יעלו עוד קורסים?", "כן. כל קורס חדש יופיע בעמוד הזה."),
            ]))}
        </div></div></div>
        {cta("מתחילים מקורס Lovable", "שיעורי וידאו מוקלטים, בעברית ובקצב שלכם.", [("lovable-1.html", "לקורס Lovable", None), ("course.html", "קורס Claude Code: הרשמה להודעה", None)])}
    </main>"""
    vis = home2.courses_cards_html()
    html = home2.inner_page(
        "קורסי AI בחינם ובעברית: Lovable ו-Claude Code | Free AI",
        "קורסי AI בחינם ובעברית למתחילים, בלי ידע קודם: קורס Lovable לבניית אתרים ואפליקציות, וקורס Claude Code שעולה בקרוב.",
        "", "קורסים",
        "קורסים מוקלטים בעברית לכלי AI שכדאי להכיר. בחינם, ובלי ידע קודם.",
        vis, main, btn1=("lovable-1.html", "לקורס Lovable", None), btn2=("#courses", "לכל הקורסים", "play"), legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "courses.html"), "w").write(html)
    print("courses.html done")


# ---------------------------------------------------------------- קורס Claude Code (בקרוב)
def build_claude():
    learn = table([
        ("החשבון וההתקנה", "פותחים חשבון Claude ומתקינים את האפליקציה במחשב."),
        ("הפרויקט הראשון", "פותחים מקום לפרויקט ב-GitHub ומחברים אותו ל-Claude Code."),
        ("איך מבקשים", "כותבים בקשה בעברית רגילה ומקבלים בדיוק מה שרציתם."),
        ("סקילים וחיבורים", "מוסיפים ל-Claude יכולות ומחברים אותו לשירותים שאתם כבר משתמשים בהם."),
        ("מעלים לאוויר", "האתר מקבל כתובת שאפשר לשלוח לכל אחד."),
    ])
    notify_btn = f'<p><a href="#" class="a2-btn" data-notify="{NOTIFY}">להירשם ולקבל הודעה</a></p>'
    main = f"""<main class="a2 sk">
        <div class="a2-band"><div class="a2-wrap"><div class="a2-body">
            {sec(1, "מה לומדים", learn)}
            {sec(2, "הרשמה להודעה", "<p>נרשמים עם גוגל או מייל, ומקבלים הודעה ביום שהקורס עולה.</p>" + notify_btn, "notify")}
            {sec(3, "בינתיים", MORE)}
            {sec(4, "שאלות נפוצות", faq([
                ("מתי הקורס עולה?", "בשבוע הבא. מי שנרשם מקבל הודעה."),
                ("הקורס בחינם?", "כן. משלמים רק על המנוי של Claude, החל מ-Pro."),
                ("צריך לדעת לתכנת?", "לא. הקורס מתחיל מאפס."),
                ("אפשר להתחיל כבר עכשיו?", 'כן. <a href="guide-1.html">המדריך הכתוב</a> מכסה את כל הדרך, ו<a href="lovable-1.html">קורס Lovable</a> כבר זמין.'),
            ]))}
        </div></div></div>
        {cta("בינתיים, קורס Lovable", "כבר זמין, בחינם ובעברית.", [("lovable-1.html", "לקורס Lovable", None), ("guide-1.html", "למדריך הכתוב", None)])}
    </main>"""
    vis = f'<img class="sk-full" src="{img("course-claude-code", True)}" alt="" decoding="async">'
    html = home2.inner_page(
        "קורס קלוד קוד (Claude Code) בחינם ובעברית | Free AI",
        "קורס קלוד קוד (Claude Code) בחינם ובעברית למתחילים, בלי ידע בתכנות. הקורס עולה בשבוע הבא: נרשמים ומקבלים הודעה.",
        "", "קורס Claude Code",
        "הקורס עולה בשבוע הבא. נרשמים עכשיו ומקבלים הודעה ביום שהוא עולה.",
        vis, main, btn1=("#notify", "להירשם ולקבל הודעה", NOTIFY), btn2=("guide-1.html", "בינתיים, למדריך הכתוב", "book"), legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "course.html"), "w").write(html)
    print("course.html done")


# ---------------------------------------------------------------- כל המדריכים
def guides_visual():
    """שני המדריכים בכרטיסים, כמו האיור בעמוד הקורסים. Lovable אפור עם "בקרוב"."""
    return home2.courses_cards_html([("guide-1.html", "guide-claude-code", "מדריך Claude Code", "24 פרקים", "on"),
                                     (None, "guide-lovable", "מדריך Lovable", "בקרוב", "soon")])


def build_guides():
    main = f"""<main class="a2 sk">
        <section class="a2-more sk-list" id="guides"><div class="a2-wrap a2-pad">
            <div class="a2-band-head"><h2>כל המדריכים.</h2></div>
            {course_cards(GUIDES)}
        </div></section>
        <div class="a2-band"><div class="a2-wrap"><div class="a2-body">
            {sec(1, "שאלות נפוצות", faq([
                ("מה ההבדל בין מדריך לקורס?", 'מדריך קוראים, פרק אחרי פרק, עם צילומי מסך. קורס רואים בווידאו. <a href="courses.html">לכל הקורסים</a>.'),
                ("המדריכים בחינם?", "כן, כולם."),
                ("מתי עולה מדריך Lovable?", 'בקרוב. בינתיים יש <a href="lovable-1.html">קורס Lovable</a> בווידאו.'),
            ]))}
        </div></div></div>
        {cta("מתחילים במדריך Claude Code", "24 פרקים קצרים, צעד אחרי צעד.", [("guide-1.html", "לפרק הראשון", None), ("courses.html", "לכל הקורסים", None)])}
    </main>"""
    html = home2.inner_page(
        "מדריכי AI בחינם ובעברית: Claude Code ו-Lovable | Free AI",
        "מדריכים כתובים בעברית לכלי AI, בחינם ובלי ידע קודם: מדריך Claude Code ב-24 פרקים, ומדריך Lovable שעולה בקרוב.",
        "", "מדריכים",
        "מדריכים כתובים בעברית, פרק אחרי פרק, עם צילומי מסך. בחינם, ובלי ידע קודם.",
        guides_visual(), main, btn1=("guide-1.html", "למדריך Claude Code", None), btn2=("#guides", "לכל המדריכים", "book"), legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "guides.html"), "w").write(html)
    print("guides.html done")


def build():
    build_guides()
    build_courses()
    build_claude()


if __name__ == "__main__":
    build()
