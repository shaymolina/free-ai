"""עמודי הקורסים בעיצוב החדש (home2.inner_page):
courses.html (כל הקורסים), course-lovable.html (קורס Lovable) ו-course.html (קורס Claude Code, מגיע בקרוב עם הרשמה להודעה).
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
    {"page": "course-lovable.html", "name": "קורס Lovable", "desc": "בונים אתרים ואפליקציות עם Lovable, בלי לכתוב קוד.",
     "status": "זמין עכשיו", "img": "course-lovable", "kind": "שיעורי וידאו"},
    {"page": "course.html", "name": "קורס Claude Code", "desc": "בונים עם Claude Code, מהחשבון הראשון ועד אתר באוויר.",
     "status": "עולה בשבוע הבא", "img": "course-claude-code", "kind": "שיעורי וידאו"},
]

NOTIFY = "claude-code-course"  # השם שנשמר בטבלת progress כ-notify-claude-code-course


def img(name, wide=False):
    return f"assets/images/articles/{name}{'-wide' if wide else ''}.webp?v=4"


def course_cards(items):
    out = []
    for k, c in enumerate(items):
        out.append(f'<a class="ac" href="{c["page"]}">'
                   f'<img src="{img(c["img"])}" alt="" loading="{"eager" if k < 3 else "lazy"}" decoding="async">'
                   f'<span class="ac-b"><h3 class="ac-t">{c["name"]}</h3>'
                   f'<span class="ac-m"><span>{c["status"]}</span><i aria-hidden="true"></i><span>{c["kind"]}</span></span></span></a>')
    return f'<div class="m2-arts">{"".join(out)}</div>'


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
                ("באיזה קורס להתחיל?", 'רוצים אתר או אפליקציה מהר? <a href="course-lovable.html">קורס Lovable</a>. רוצים לבנות דברים גדולים יותר ולעבוד עם הקבצים שלכם? <a href="course.html">קורס Claude Code</a>, שעולה בשבוע הבא.'),
                ("יעלו עוד קורסים?", "כן. כל קורס חדש יופיע בעמוד הזה."),
            ]))}
        </div></div></div>
        {cta("מתחילים מקורס Lovable", "שיעורי וידאו מוקלטים, בעברית ובקצב שלכם.", [("course-lovable.html", "לקורס Lovable", None), ("course.html", "קורס Claude Code: הרשמה להודעה", None)])}
    </main>"""
    vis = home2.courses_cards_html()
    html = home2.inner_page(
        "קורסי AI בחינם ובעברית: Lovable ו-Claude Code | Free AI",
        "קורסי AI בחינם ובעברית למתחילים, בלי ידע קודם: קורס Lovable לבניית אתרים ואפליקציות, וקורס Claude Code שעולה בקרוב.",
        "", "קורסים",
        "קורסים מוקלטים בעברית לכלי AI שכדאי להכיר. בחינם, ובלי ידע קודם.",
        vis, main, btn1=("course-lovable.html", "לקורס Lovable", None), btn2=("#courses", "לכל הקורסים", "play"), legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "courses.html"), "w").write(html)
    print("courses.html done")


# ---------------------------------------------------------------- קורס Lovable
LOVABLE_LESSONS = []  # (שם השיעור, משפט, קישור לסרטון). מתמלא כשהקישורים מגיעים.


def lessons_html():
    if not LOVABLE_LESSONS:
        return '<p>השיעורים עולים לכאן היום.</p>'
    rows = "".join(f'<li><div class="sk-st-t"><h3>{k}. <a href="{u}" target="_blank" rel="noopener">{t}</a></h3><p>{d}</p></div></li>'
                   for k, (t, d, u) in enumerate(LOVABLE_LESSONS, 1))
    return f'<ol class="sk-steps">{rows}</ol>'


def build_lovable():
    main = f"""<main class="a2 sk">
        <div class="a2-band"><div class="a2-wrap"><div class="a2-body">
            {sec(1, "מה זה Lovable", "<p>Lovable בונה אתר או אפליקציה לפי מה שכותבים לו. מתארים במילים מה רוצים, רואים את התוצאה תוך דקות, ומבקשים שינויים עד שזה נראה נכון.</p>")}
            {sec(2, "השיעורים", lessons_html(), "lessons")}
            {sec(3, "למי הקורס מתאים", table([
                ("בעלי עסקים", "אתר לעסק, דף נחיתה או טופס הזמנות, בלי לחכות למתכנת."),
                ("מי שיש לו רעיון", "גרסה ראשונה שעובדת, להראות לאנשים ולבדוק אם זה מעניין אותם."),
                ("מי שרק מתחיל עם AI", "הדרך הכי מהירה לראות מה AI יודע לבנות."),
            ]))}
            {sec(4, "שאלות נפוצות", faq([
                ("הקורס בחינם?", "כן. כל השיעורים בחינם."),
                ("צריך לשלם על Lovable?", "יש ל-Lovable תוכנית חינמית שמספיקה כדי להתחיל, ותוכניות בתשלום למי שבונה הרבה."),
                ("צריך לדעת לתכנת?", "לא. כותבים ל-Lovable בשפה רגילה."),
                ("מה ההבדל בין Lovable ל-Claude Code?", 'Lovable עובד בדפדפן ומתאים לבנות אתר או אפליקציה מהר. Claude Code עובד על הקבצים שלכם ומתאים לפרויקטים גדולים יותר. <a href="course.html">קורס Claude Code</a> עולה בשבוע הבא.'),
            ]))}
        </div></div></div>
        {cta("אחרי Lovable: קורס Claude Code", "עולה בשבוע הבא. נרשמים ומקבלים הודעה ביום שהוא עולה.", [("course.html", "לקורס Claude Code", None), ("courses.html", "לכל הקורסים", None)])}
    </main>"""
    vis = f'<img class="sk-full" src="{img("course-lovable", True)}" alt="" decoding="async">'
    html = home2.inner_page(
        "קורס Lovable בחינם ובעברית למתחילים | Free AI",
        "קורס Lovable בחינם ובעברית: בונים אתרים ואפליקציות עם AI בלי לכתוב קוד. שיעורי וידאו מוקלטים למתחילים, בקצב שלכם.",
        "", "קורס Lovable",
        "בונים אתרים ואפליקציות עם Lovable, בעברית ובלי לכתוב קוד. שיעורי וידאו מוקלטים, בקצב שלכם.",
        vis, main, btn1=("#lessons", "לשיעורים", None), btn2=("courses.html", "לכל הקורסים", "play"), legacy_v=CSS_VERSION)
    open(os.path.join(SITE, "course-lovable.html"), "w").write(html)
    print("course-lovable.html done")


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
                ("אפשר להתחיל כבר עכשיו?", 'כן. <a href="guide-1.html">המדריך הכתוב</a> מכסה את כל הדרך, ו<a href="course-lovable.html">קורס Lovable</a> כבר זמין.'),
            ]))}
        </div></div></div>
        {cta("בינתיים, קורס Lovable", "כבר זמין, בחינם ובעברית.", [("course-lovable.html", "לקורס Lovable", None), ("guide-1.html", "למדריך הכתוב", None)])}
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


def build():
    build_courses()
    build_lovable()
    build_claude()


if __name__ == "__main__":
    build()
