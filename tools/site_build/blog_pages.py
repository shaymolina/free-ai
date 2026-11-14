"""בלוג המדריכים, מאמר בודד, מדיניות פרטיות ותנאי שימוש – נבנים מתוך blog-standard.html ו-blog-single.html של התבנית."""
import re
from pathlib import Path
from common import apply_common

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "aigocy-about"
OUT = ROOT / "site"
DATE = "14 בנובמבר 2026"

STYLE = '''    <style>
        /* blog – RTL */
        .article-blog .infor_name { -webkit-line-clamp: 2; }
        .article-blog .infor_excerpt { margin-top: 10px; -webkit-line-clamp: 3; -webkit-box-orient: vertical; display: -webkit-box; overflow: hidden; }
        .article-blog .tf-btn-2 .icon { transform: scaleX(-1); }
        .sidebar-cta .text { margin-bottom: 20px; }
        @media (min-width: 426px) { .article-blog.style-horizontal .blog-image { flex: 0 0 300px; } }
        .blog-single-wrap .article-body { display: flex; flex-direction: column; gap: 20px; }
        .blog-single-wrap .article-body h2 { font-size: 28px; line-height: 1.3; margin: 16px 0 0; }
        .blog-single-wrap .article-body ol, .blog-single-wrap .article-body ul { padding-right: 22px; padding-left: 0; display: flex; flex-direction: column; gap: 10px; }
        .blog-single-wrap .article-body ol { list-style: decimal; }
        .blog-single-wrap .article-body ul { list-style: disc; }
        .blog-single-wrap .article-body li { display: list-item; list-style: inherit; }
        .blog-single-wrap .article-body li::marker { color: var(--primary); font-weight: 600; }
        .blog-single-wrap .article-body a:not(.tf-btn) { color: var(--primary); text-decoration: underline; text-underline-offset: 3px; }
        .blog-single-wrap .path { direction: rtl; unicode-bidi: isolate; font-weight: 600; }
        .blockquote-wrap { padding: 56px 56px 64px 39px; }
        .blockquote-wrap svg { right: auto; left: 40px; }
        .blockquote-wrap .tf-btn-2 { margin-top: 24px; position: relative; z-index: 1; }
        .blockquote-wrap p { position: relative; z-index: 1; }
        .entry-footer .tags-links { max-width: none; }
        .legal-wrap .updated { color: var(--neutral-400); }
        @media (max-width: 767px) {
            .blockquote-wrap { padding: 36px 24px 76px; }
            .blog-single-wrap .article-body h2 { font-size: 23px; }
        }
    </style>
</head>'''

POSTS = [
    {
        "img": "blog-1.jpg",
        "cat": "סקילים",
        "title": "איך מתקינים סקיל ב-Claude – המדריך הקצר",
        "excerpt": "מה זה סקיל, איפה מעלים את קובץ ה-zip ואיך משתמשים בו בשיחה חדשה. חמש דקות, בלי ידע טכני.",
    },
    {
        "img": "blog-2.jpg",
        "cat": "Claude",
        "title": "מה זה Claude ואיך מתחילים",
        "excerpt": "הכירו את Claude: מה הוא יודע לעשות, איך פותחים חשבון, ואיך לנסח בקשה ראשונה שמקבלת תשובה טובה.",
    },
    {
        "img": "blog-3.jpg",
        "cat": "אחסון",
        "title": "איך בוחרים אחסון לאתר שבניתם עם AI",
        "excerpt": "בניתם אתר עם Claude או Lovable? הנה מה חשוב לבדוק לפני שבוחרים אחסון, ומה ההבדל בין אחסון רגיל לשרת.",
    },
]
CATS = ["Claude", "סקילים", "Lovable", "n8n", "אחסון"]


def page_title(html, title, crumbs):
    parts = ['<a href="index.html" class="link1">דף הבית</a>']
    for label, href in crumbs:
        parts.append("<div>/</div>")
        parts.append(f'<a href="{href}" class="link1">{label}</a>' if href else f"<div>{label}</div>")
    crumb_html = "\n                    ".join(parts)
    new = f'''<!-- page-title -->
        <div class="section-page-title">
            <div class="container text-center">
                <h1 class="page-title fw-semibold effectFade fadeZoom">{title}</h1>
                <div class="breadcrumbs effectFade fadeUp">
                    {crumb_html}
                </div>
            </div>
        </div>
        <!-- /page-title -->'''
    return re.sub(r"<!-- page-title -->.*?<!-- /page-title -->", lambda m: new, html, count=1, flags=re.S)


def sidebar():
    recent = "\n".join(f'''                                    <div class="relatest-post-item">
                                        <div class="image">
                                            <img loading="lazy" width="80" height="80" src="assets/images/blog/{p['img']}" alt="{p['title']}">
                                        </div>
                                        <div class="content">
                                            <h6 class="title text-body-1">
                                                <a href="blog-single.html" class="link1">
                                                    {p['title']}
                                                </a>
                                            </h6>
                                            <p class="time text-body-3 text-white-64">{DATE}</p>
                                        </div>
                                    </div>''' for p in POSTS)
    cats = "\n".join(f'''                                    <div class="item">
                                        <a href="blog-standard.html" class="text-body-1 link1">{c}</a>
                                    </div>''' for c in CATS)
    return f'''<div class="col-lg-4">
                        <div class="blog-sidebar m-lg-0">
                            <div class="sidebar-item effectFade fadeUp no-div">
                                <h5 class="sidebar-title">
                                    מדריכים אחרונים
                                </h5>
                                <div class="list-relatest-post">
{recent}
                                </div>
                            </div>
                            <div class="sidebar-item effectFade fadeUp no-div">
                                <h5 class="sidebar-title">
                                    נושאים
                                </h5>
                                <div class="sidebar-categories">
{cats}
                                </div>
                            </div>
                            <div class="sidebar-item sidebar-cta effectFade fadeUp no-div">
                                <h5 class="sidebar-title">
                                    לומדים בחינם
                                </h5>
                                <p class="text text-body-2 text-secondary">קורסים מלאים בעברית, קבצים להורדה וסקילים מוכנים לעבודה עם Claude. ההרשמה לוקחת פחות מדקה.</p>
                                <a href="contact.html#signup" class="tf-btn w-100">הרשמה חינם</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!-- /Blog With Sidebar -->'''


def replace_sidebar(html):
    new, n = re.subn(r'<div class="col-lg-4">\s*<div class="blog-sidebar m-lg-0">.*?<!-- /Blog With Sidebar -->',
                     lambda m: sidebar(), html, count=1, flags=re.S)
    assert n == 1
    return new


def finish(html, name):
    html = html.replace("</head>", STYLE, 1)
    (OUT / name).write_text(html)
    vis = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S)
    vis = re.sub(r"<svg.*?</svg>", "", vis, flags=re.S)
    left = re.findall(r">\s*([A-Za-z][A-Za-z ,’'&\-]{4,})\s*<", vis)
    ok = {"Free AI", "Claude", "Lovable", "Claude Code"}
    print(f"{name} done; leftover English:", [x for x in left if x.strip() not in ok][:20])


# ======================= blog-standard.html =======================
html = (SRC / "blog-standard.html").read_text()
html = apply_common(html, "blog-standard.html", "בלוג מדריכים – Free AI",
                    "מדריכים פתוחים בעברית ל-Claude, סקילים, Lovable, n8n ואחסון אתרים. קצר, ברור ובחינם.")
html = page_title(html, "בלוג מדריכים", [("בלוג", None)])
cards = "\n".join(f'''                            <div class="article-blog style-horizontal hover-img effectFade fadeUp no-div">
                                <a href="blog-single.html" class="blog-image img-style">
                                    <img loading="lazy" width="426" height="307" src="assets/images/blog/{p['img']}" alt="{p['title']}">
                                </a>
                                <div class="blog-content">
                                    <div class="infor">
                                        <p class="infor_sub text-secondary">
                                            {p['cat']}
                                        </p>
                                        <h6 class="fw-semibold">
                                            <a href="blog-single.html" class="link1 infor_name">
                                                {p['title']}
                                            </a>
                                        </h6>
                                        <p class="infor_excerpt text-body-3 text-secondary">{p['excerpt']}</p>
                                    </div>
                                    <a href="blog-single.html" class="tf-btn-2">
                                        לקריאה
                                        <i class="icon icon-arrow-top-right"></i>
                                    </a>
                                </div>
                            </div>''' for p in POSTS)
html, n = re.subn(r'(<div class="tf-grid-layout">).*?(\n                        </div>\n                    </div>\n                    <div class="col-lg-4">)',
                  lambda m: m.group(1) + "\n" + cards + m.group(2), html, count=1, flags=re.S)
assert n == 1
html = replace_sidebar(html)
finish(html, "blog-standard.html")


# ======================= blog-single.html =======================
SINGLE_SRC = (SRC / "blog-single.html").read_text()
ART_TITLE = POSTS[0]["title"]

article = f'''<div class="blog-single-wrap">
                            <div class="image effectFade fadeZoom">
                                <img loading="lazy" width="777" height="548" src="assets/images/blog/blog-4.jpg" alt="{ART_TITLE}">
                            </div>
                            <div class="meta-list">
                                <div class="meta-item">
                                    <i class="icon icon-user-solid"></i>
                                    <span>Free AI</span>
                                </div>
                                <div class="meta-item">
                                    <i class="icon icon-clock-solid"></i>
                                    <span>{DATE}</span>
                                </div>
                                <div class="meta-item">
                                    <i class="icon icon-book-open-solid"></i>
                                    <span>3 דקות קריאה</span>
                                </div>
                            </div>
                            <div class="article-body text-body-2">
                                <p>סקיל הוא דרך ללמד את Claude לעשות משימה מסוימת בדיוק כמו שאתם רוצים – בכל פעם מחדש, בלי להסביר מההתחלה. במדריך הזה תראו מה זה סקיל, איך מתקינים אותו בכמה לחיצות ואיך משתמשים בו בשיחה.</p>

                                <h2 class="fw-semibold">מה זה סקיל?</h2>
                                <p>סקיל (Skill) הוא תיקייה קטנה עם הוראות, ולפעמים גם קבצים ותסריטים, שמסבירה ל-Claude איך לבצע משימה אחת: לבדוק אבטחה של אתר, למדוד מהירות, לכתוב מסמך בפורמט קבוע ועוד. התיקייה מגיעה כקובץ zip.</p>
                                <p>היתרון הגדול: Claude טוען את הסקיל רק כשהוא רלוונטי. אתם לא צריכים להדביק פרומפט ארוך או לזכור את כל השלבים – מספיק לבקש את המשימה במילים רגילות.</p>

                                <h2 class="fw-semibold">איך מתקינים סקיל – צעד אחרי צעד</h2>
                                <ol>
                                    <li>מורידים את קובץ ה-zip של הסקיל. לא צריך לפתוח אותו.</li>
                                    <li>נכנסים ל-Claude ולוחצים על השם שלכם בפינה, ואז על <span class="path">הגדרות</span> (Settings).</li>
                                    <li>עוברים ללשונית <span class="path">יכולות</span> (Capabilities) וגוללים לאזור <span class="path">סקילים</span> (Skills).</li>
                                    <li>לוחצים על <span class="path">העלאת סקיל</span> (Upload skill) ובוחרים את קובץ ה-zip.</li>
                                    <li>מוודאים שהמתג שליד הסקיל החדש דלוק.</li>
                                </ol>
                                <p>לא רואים את אזור הסקילים? בדקו שבאותו מסך מופעלת גם האפשרות של יצירת קבצים והרצת קוד – סקילים נשענים עליה.</p>

                                <h2 class="fw-semibold">איך משתמשים בסקיל</h2>
                                <p>פותחים שיחה חדשה ומבקשים את המשימה בשפה רגילה. למשל, אחרי שהתקנתם את סקיל בדיקת האבטחה, כותבים: "תבדוק את האבטחה של האתר שלי" ומצרפים את הקבצים או את הכתובת. Claude מזהה לבד שיש לו סקיל מתאים ומשתמש בו.</p>
                                <p>כדאי לפתוח שיחה חדשה אחרי ההתקנה, כדי ש-Claude יכיר את הסקיל מההתחלה. רוצים להפסיק להשתמש בו? מכבים את המתג באותו מסך, או מוחקים אותו.</p>
                            </div>
                            <div class="blockquote-wrap">
                                <h5 class="fw-medium text-white">טיפ אבטחה: סקיל יכול להריץ קוד. התקינו רק סקילים ממקור שאתם סומכים עליו, ואם יש לכם ספק – פתחו את הקבצים ובדקו מה כתוב בהם.</h5>
                                <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M44.375 70.4063V41.0938C44.375 33.0729 47.0729 26.3646 52.4687 20.9688C58.0104 15.4271 65.5208 11.6354 75 9.59375V29.0625C71.3542 30.2292 68.9479 31.6875 67.7812 33.4375C66.6146 35.0417 65.9583 37.0833 65.8125 39.5625H75V70.4063H44.375ZM5 70.4063V41.0938C5 33.0729 7.69792 26.3646 13.0938 20.9688C18.6354 15.4271 26.1458 11.6354 35.625 9.59375V29.0625C32.125 30.2292 29.7187 31.6875 28.4062 33.4375C27.2396 35.0417 26.5833 37.0833 26.4375 39.5625H35.625V70.4063H5Z" fill="#27272A"/>
                                </svg>
                            </div>
                            <div class="article-body text-body-2">
                                <h2 class="fw-semibold">מאיפה מביאים סקילים?</h2>
                                <p>ב<a href="work.html">ספריית הסקילים של Free AI</a> תמצאו סקילים מוכנים בעברית – למשל בדיקת אבטחה לאתר ובדיקת מהירות לאתר. כל סקיל מגיע עם הסבר קצר, קובץ להורדה ודוגמה לשימוש.</p>
                            </div>
                            <div class="blockquote-wrap">
                                <h5 class="fw-semibold text-white">רוצים ללמוד את כל זה לעומק?</h5>
                                <p class="text-body-2 text-secondary mt-12">נרשמים בחינם ומקבלים גישה לקורס Claude מאפס, לכל הסקילים ולקבצים להורדה. בלי כרטיס אשראי.</p>
                                <a href="contact.html#signup" class="tf-btn-2">הרשמה חינם</a>
                            </div>
                            <div class="entry-footer">
                                <div class="tags-links">
                                    <h6 class="text-body-1">נושאים:</h6>
                                    <div class="list-tags">
                                        <a href="blog-standard.html" class="tags-item fw-semibold">Claude</a>
                                        <a href="blog-standard.html" class="tags-item fw-semibold">סקילים</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    '''

html = apply_common(SINGLE_SRC, "blog-standard.html", f"{ART_TITLE} | Free AI",
                    "מה זה סקיל ב-Claude, איך מתקינים אותו מקובץ zip דרך ההגדרות, ואיך משתמשים בו בשיחה חדשה. מדריך קצר בעברית.")
html = page_title(html, "מדריכים", [("בלוג", "blog-standard.html"), ("סקילים", None)])
html, n = re.subn(r'<div class="blog-single-wrap">.*?</div>\s*</div>\s*(?=<div class="col-lg-4">)', lambda m: article, html, count=1, flags=re.S)
assert n == 1
html = replace_sidebar(html)
# כותרת המאמר מעל התמונה
html = html.replace('<div class="blog-single-wrap">\n                            <div class="image effectFade fadeZoom">',
                    f'<div class="blog-single-wrap">\n                            <h2 class="h3 fw-semibold mb-0">{ART_TITLE}</h2>\n                            <div class="image effectFade fadeZoom">', 1)
finish(html, "blog-single.html")


# ======================= privacy.html / terms.html =======================
def legal(name, title, desc, body):
    html = apply_common(SINGLE_SRC, "", f"{title} – Free AI", desc)
    html = page_title(html, title, [(title, None)])
    section = f'''<!-- Blog With Sidebar -->
        <section class="section-blog flat-spacing">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-8">
                        <div class="blog-single-wrap legal-wrap">
                            <div class="article-body text-body-2">
                                <p class="updated">עודכן לאחרונה: {DATE}</p>
{body}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!-- /Blog With Sidebar -->'''
    html, n = re.subn(r"<!-- Blog With Sidebar -->.*?<!-- /Blog With Sidebar -->", lambda m: section, html, count=1, flags=re.S)
    assert n == 1
    finish(html, name)


def blocks(items):
    out = []
    for h, paras in items:
        out.append(f'                                <h2 class="fw-semibold">{h}</h2>')
        for p in paras:
            if isinstance(p, list):
                lis = "\n".join(f"                                    <li>{x}</li>" for x in p)
                out.append(f"                                <ul>\n{lis}\n                                </ul>")
            else:
                out.append(f"                                <p>{p}</p>")
    return "\n".join(out)


privacy = blocks([
    ("כללי", [
        "Free AI (\"האתר\", \"אנחנו\") מציע קורסים, מדריכים וסקילים ל-AI בעברית, בחינם. המדיניות הזו מסבירה איזה מידע אנחנו אוספים כשאתם משתמשים באתר, למה, ומה הזכויות שלכם. השימוש באתר מהווה הסכמה למדיניות הזו.",
    ]),
    ("איזה מידע אנחנו אוספים", [
        "כשנרשמים ומשתמשים באתר, אנחנו שומרים את המידע הבא:",
        [
            "<strong>פרטי הרשמה:</strong> שם וכתובת מייל. אם נרשמים עם Google, אנחנו מקבלים מ-Google רק את השם, המייל ותמונת הפרופיל.",
            "<strong>התקדמות בלימוד:</strong> אילו שיעורים התחלתם וסיימתם, ותעודות שקיבלתם.",
            "<strong>הורדות:</strong> אילו קבצים וסקילים הורדתם.",
            "<strong>לחיצות על קישורים:</strong> לחיצות על קישורים יוצאים מהאתר, כולל קישורי שותפים.",
            "<strong>מידע טכני:</strong> נתונים בסיסיים שהדפדפן שולח, כמו סוג מכשיר ודפדפן, לצורך הפעלת האתר ואבטחתו.",
        ],
        "אנחנו לא אוספים פרטי תשלום – אין באתר שום תשלום.",
    ]),
    ("למה אנחנו משתמשים במידע", [
        [
            "כדי לפתוח לכם חשבון ולאפשר כניסה.",
            "כדי לשמור את ההתקדמות שלכם ולהנפיק תעודת סיום עם השם שלכם.",
            "כדי לשלוח לכם קוד כניסה ועדכונים הקשורים לחשבון. מיילים שיווקיים יישלחו רק אם הסכמתם, ותמיד אפשר להסיר את עצמכם.",
            "כדי להבין אילו שיעורים, קבצים וקישורים מועילים, ולשפר את האתר.",
        ],
    ]),
    ("עם מי המידע משותף", [
        "אנחנו לא מוכרים מידע אישי. המידע משותף רק במקרים האלה:",
        [
            "<strong>ספקי תשתית:</strong> חברות שמספקות לנו אחסון, מסד נתונים, שליחת מיילים והתחברות (למשל Google). הן מעבדות את המידע רק כדי לתת לנו את השירות.",
            "<strong>סרטוני YouTube:</strong> חלק מהשיעורים כוללים סרטונים מוטמעים מ-YouTube. כשאתם צופים בהם, YouTube (חברת Google) עשויה לאסוף מידע לפי מדיניות הפרטיות שלה.",
            "<strong>דרישה לפי חוק:</strong> אם נידרש למסור מידע על פי דין או צו של רשות מוסמכת.",
        ],
    ]),
    ("קישורי שותפים", [
        "בחלק מהשיעורים, במיוחד בנושא העלאת אתרים לאוויר, אנחנו ממליצים על חברת האחסון 4CODE. הקישורים אליה הם קישורי שותפים: אם תירשמו דרכם, ייתכן שנקבל עמלה. זה לא עולה לכם יותר, וזה מה שמאפשר לנו להשאיר את כל התוכן בחינם. כשאתם עוברים לאתר של 4CODE, חלה עליכם מדיניות הפרטיות שלה.",
    ]),
    ("עוגיות ואחסון בדפדפן", [
        "האתר משתמש בעוגיות ובאחסון מקומי בדפדפן כדי לשמור אתכם מחוברים ולזכור העדפות. אפשר למחוק אותם בהגדרות הדפדפן, אבל אז ייתכן שתצטרכו להתחבר מחדש.",
    ]),
    ("אבטחת מידע ושמירה", [
        "אנחנו נוקטים אמצעים סבירים כדי להגן על המידע, אבל אף מערכת אינה חסינה לחלוטין. המידע נשמר כל עוד החשבון שלכם פעיל, או עד שתבקשו למחוק אותו.",
    ]),
    ("הזכויות שלכם", [
        "אתם יכולים לבקש לעיין במידע ששמור עליכם, לתקן אותו או למחוק את החשבון וכל המידע הקשור אליו. כדי לעשות זאת, פנו אלינו דרך <a href=\"contact.html\">עמוד יצירת הקשר</a> ונטפל בבקשה בהקדם.",
    ]),
    ("שינויים במדיניות", [
        "ייתכן שנעדכן את המדיניות מדי פעם. תאריך העדכון האחרון מופיע בראש העמוד, ושינויים מהותיים נפרסם באתר.",
    ]),
])

terms = blocks([
    ("כללי", [
        "תנאים אלה חלים על השימוש באתר Free AI ובכל התכנים שבו. השימוש באתר, וההרשמה אליו בפרט, מהווים הסכמה לתנאים. אם אינכם מסכימים להם, אנא אל תשתמשו באתר.",
    ]),
    ("שירות חינמי", [
        "כל הקורסים, המדריכים, הקבצים, הסקילים והתעודות באתר ניתנים בחינם. אנחנו רשאים להוסיף, לשנות או להסיר תכנים, ולהפסיק את השירות כולו או חלקו, בכל עת.",
    ]),
    ("החשבון שלכם", [
        [
            "החשבון אישי ומיועד לכם בלבד. אין להעביר אותו או לשתף את פרטי הכניסה עם אחרים.",
            "יש למסור שם וכתובת מייל נכונים. השם שתמסרו הוא השם שיופיע בתעודת הסיום.",
            "אתם אחראים לפעולות שנעשות בחשבון שלכם. אם אתם חושדים בשימוש לא מורשה, פנו אלינו.",
            "אנחנו רשאים לחסום חשבון שמשתמש באתר לרעה, למשל בהורדה אוטומטית של תכנים או בניסיון לפגוע באתר.",
        ],
    ]),
    ("שימוש בתכנים", [
        "התכנים באתר מיועדים ללימוד ולשימוש אישי ועסקי שלכם. אפשר להשתמש בקבצים ובתבניות בפרויקטים שלכם. אין להעתיק את התכנים ולהפיץ או למכור אותם כקורס או כמוצר מתחרה בלי אישור בכתב.",
    ]),
    ("סקילים וכלים של צד שלישי", [
        "חלק מהסקילים והקבצים באתר מבוססים על עבודה של אחרים, או נועדו לפעול בכלים של חברות אחרות כמו Claude, Lovable ו-n8n. כל סקיל כפוף לרישיון שמצורף אליו, והשימוש בכלים עצמם כפוף לתנאים של החברות שמפעילות אותם. לפני שימוש מסחרי, בדקו את הרישיון של הסקיל.",
    ]),
    ("התכנים ניתנים כפי שהם", [
        "אנחנו משתדלים שהתכנים יהיו מדויקים ועדכניים, אבל הם ניתנים \"כפי שהם\" בלי התחייבות. כלי AI משתנים מהר, וייתכן שמסכים או שלבים יהיו שונים ממה שמוצג. האחריות לשימוש בתכנים, בסקילים ובקוד שנוצר בעזרתם – כולל בדיקה לפני העלאה לאוויר – היא שלכם. Free AI לא יהיה אחראי לנזק שנגרם מהשימוש באתר או בתכניו.",
    ]),
    ("קישורים לאתרים אחרים", [
        "באתר יש קישורים לאתרים ולשירותים חיצוניים, וחלקם קישורי שותפים (למשל לחברת האחסון 4CODE) שעליהם אנחנו עשויים לקבל עמלה. אנחנו לא אחראים לתכנים, למחירים או לשירות של אתרים אלה. פרטים נוספים ב<a href=\"privacy.html\">מדיניות הפרטיות</a>.",
    ]),
    ("שינויים בתנאים", [
        "אנחנו רשאים לעדכן את התנאים מעת לעת. תאריך העדכון האחרון מופיע בראש העמוד, והמשך השימוש באתר אחרי עדכון מהווה הסכמה לתנאים המעודכנים.",
    ]),
    ("יצירת קשר", [
        "שאלות על התנאים? פנו אלינו דרך <a href=\"contact.html\">עמוד יצירת הקשר</a>.",
    ]),
])

legal("privacy.html", "מדיניות פרטיות",
      "איזה מידע Free AI אוסף, למה, עם מי הוא משותף ומה הזכויות שלכם.", privacy)
legal("terms.html", "תנאי שימוש",
      "תנאי השימוש באתר Free AI – שירות חינמי, חשבון אישי, רישיונות סקילים ושימוש בתכנים.", terms)

for f in ("blog-two-columns.html", "blog-three-columns.html", "index-v2.html"):
    (OUT / f).unlink(missing_ok=True)
