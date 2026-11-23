"""עמוד הצהרת הנגישות (site/accessibility.html).
נבנה מתוך privacy.html, כדי לקבל בדיוק את העיצוב של שאר העמודים המשפטיים.
הרצה: python3 tools/site_build/accessibility_page.py  ואחר כך python3 tools/seo/seo_build.py"""
import os
import re

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "site")
TITLE = "הצהרת נגישות"
DESC = "מה עשינו כדי שאפשר יהיה להשתמש ב-Free AI עם מוגבלות, איך עובד תפריט הנגישות, מה עוד לא מושלם ואיך פונים אלינו."
DATE = "23 בנובמבר 2026"
MAIL = '<a href="mailto:hello@free-ai.co.il">hello@free-ai.co.il</a>'

SECTIONS = [
    ("מה עשינו באתר", [
        [
            "כל העמודים מוגדרים בעברית ומימין לשמאל, כך שקוראי מסך מקריאים אותם נכון.",
            "אפשר לעבור על כל האתר עם המקלדת בלבד: Tab כדי לזוז, Enter כדי ללחוץ, Esc כדי לסגור חלון. מה שנבחר מקבל מסגרת שרואים.",
            "הכותרות בכל עמוד מסודרות לפי רמות, ואפשר לדלג ביניהן עם קורא מסך.",
            "לתמונות יש תיאור בטקסט. תמונות שהן רק קישוט מוסתרות מקוראי מסך.",
            "האתר מתאים את עצמו לטלפון, לטאבלט ולמחשב, ואפשר להגדיל את התצוגה עם הזום של הדפדפן.",
            "אין באתר תוכן מהבהב.",
        ],
    ]),
    ("תפריט הנגישות", [
        "בפינה של כל עמוד יש כפתור כחול עגול עם סמל של כיסא גלגלים. הוא פותח תפריט שבו אפשר:",
        [
            "להגדיל את הטקסט עד 160%, ולהגדיל ריווח בין אותיות, בין מילים ובין שורות.",
            "לעבור לגופן פשוט וקריא.",
            "לבחור ניגודיות גבוהה, כהה או בהירה, להפוך צבעים או להציג בגווני אפור.",
            "לעצור אנימציות ולהפחית תנועה.",
            "להדגיש קישורים וכותרות, להוסיף סרגל קריאה או מסכת קריאה, להגדיל את סמן העכבר ולהדגיש את המקום שבו נמצא המיקוד.",
            "להסתיר תמונות.",
        ],
        "ההגדרות נשמרות רק בדפדפן שלכם, ו\"איפוס כל ההגדרות\" מחזיר הכול למצב הרגיל. התפריט משנה את התצוגה אצלכם בלבד. הוא לא מחליף את העבודה על הנגישות של האתר עצמו.",
    ]),
    ("רמת הנגישות", [
        "אנחנו עובדים כדי שהאתר יעמוד בתקנה 35 לתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע\"ג-2013, ובתקן הישראלי ת\"י 5568, שמבוסס על הנחיות WCAG 2.0 ברמה AA.",
        "בדקנו את העמודים המרכזיים בכלי בדיקה אוטומטי ובשימוש במקלדת בלבד. האתר עוד לא עבר בדיקה של מורשה נגישות.",
    ]),
    ("מה עוד לא מושלם", [
        [
            "בכמה מקומות טקסט אפור בהיר לא בולט מספיק על הרקע. אנחנו מתקנים את זה.",
            "ייתכן שלחלק מהסרטונים עדיין אין כתוביות.",
            "סרטוני YouTube, ההתחברות עם Google ותכנים אחרים של חברות חיצוניות לא בשליטה שלנו.",
            "הסקילים להורדה הם קבצי טקסט וקוד, לא מסמכים מונגשים.",
        ],
        "מצאתם משהו שלא כתוב כאן? נשמח לדעת.",
    ]),
    ("נתקלתם בבעיה?", [
        f"כתבו לרכז הנגישות של Free AI: {MAIL}",
        "כדי שנוכל לתקן מהר, ציינו באיזה עמוד זה קרה, מה ניסיתם לעשות, ובאיזה מכשיר, דפדפן וטכנולוגיה מסייעת השתמשתם (למשל NVDA, VoiceOver או הגדלת מסך). נחזור אליכם בהקדם.",
    ]),
    ("הסדרי נגישות פיזיים", [
        "Free AI פועל באינטרנט בלבד. אין לנו משרד או מקום לקבלת קהל.",
    ]),
]


def body():
    out = [f'                                <p class="updated">עודכן לאחרונה: {DATE}</p>']
    for h, items in SECTIONS:
        out.append(f'                                <h2 class="fw-semibold">{h}</h2>')
        for item in items:
            if isinstance(item, list):
                lis = "\n".join(f"                                    <li>{x}</li>" for x in item)
                out.append(f"                                <ul>\n{lis}\n                                </ul>")
            else:
                out.append(f"                                <p>{item}</p>")
    return "\n".join(out)


def build():
    src = open(os.path.join(SITE, "privacy.html")).read()
    s = src.replace("<title>מדיניות פרטיות – Free AI</title>", f"<title>{TITLE} – Free AI</title>")
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', s, count=1)
    s = s.replace('<h1 class="page-title fw-semibold effectFade fadeZoom">מדיניות פרטיות</h1>',
                  f'<h1 class="page-title fw-semibold effectFade fadeZoom">{TITLE}</h1>')
    s = s.replace("<div>/</div>\n                    <div>מדיניות פרטיות</div>", f"<div>/</div>\n                    <div>{TITLE}</div>")
    s, n = re.subn(r'(<div class="article-body text-body-2">\n).*?(\n                            </div>\n                        </div>)',
                   lambda m: m.group(1) + body() + m.group(2), s, count=1, flags=re.S)
    assert n == 1 and TITLE in s
    # בלוק ה-SEO נבנה מחדש ב-seo_build.py
    s = re.sub(r"<!-- seo -->.*?<!-- /seo -->", "", s, flags=re.S)
    open(os.path.join(SITE, "accessibility.html"), "w").write(s)
    print("accessibility.html built")


if __name__ == "__main__":
    build()
