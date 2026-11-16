"""המדריך המלא ל-Claude Code: עמוד לכל פרק (guide-N.html).

נבנה מתוך site/service-single.html (העמוד המוגמר), כדי לרשת את העיצוב, התפריט והפוטר.
הרצה: cd tools/site_build && python3 guide_pages.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

DISCLOSURE = "גילוי נאות: Free AI מקבל עמלה מ-4CODE על הרשמה דרך הקישור שלנו. המחיר לא משתנה."

# (כותרת, תיאור קצר, קובץ או None אם עוד לא עלה)
CHAPTERS = [
    ("לפני שמתחילים", "למי זה מתאים, מה מכינים וכמה זה עולה.", "guide-1.html"),
    ("Claude הרגיל מול Claude Code", "מה ההבדל, ומתי משתמשים בכל אחד.", None),
    ("פותחים חשבון Claude", "הרשמה ובחירת מסלול.", None),
    ("מתקינים את האפליקציה במחשב", "הורדה, התקנה וכניסה ראשונה.", None),
    ("פותחים חשבון GitHub", "הכספת שבה נשמר הפרויקט.", None),
    ("פותחים משתמש ב-4CODE", "המגרש שעליו האתר יושב.", None),
    ("Supabase – מתי כן ומתי לא", "הזיכרון של המוצר, ומתי בכלל צריך אותו.", None),
    ("הפרויקט הראשון מא' עד ת'", "בונים אתר פשוט ביחד.", None),
    ("מעלים את האתר לאוויר", "כתובת חינמית מ-4CODE או דומיין משלכם.", None),
    ("איך מדברים עם Claude Code", "בקשות טובות ותבניות מוכנות.", None),
    ("סדר ובטיחות", "פרויקטים, סיסמאות וגיבויים.", None),
    ("כשמשהו נתקע", "התקלות הנפוצות ומה כותבים ל-Claude.", None),
    ("השלב הבא", "תשלומים, מיילים ועבודה מהטלפון.", None),
]

CSS = '''
        .guide-kicker { display: inline-block; font-size: 15px; font-weight: 600; padding: 6px 14px; border-radius: 999px; border: 1px solid rgba(127,127,127,.4); margin-bottom: 16px; }
        .guide-lead { font-size: 20px; line-height: 1.6; }
        .guide-block { margin-bottom: 80px; }
        .guide-block .features-item .title { font-size: 24px; line-height: 1.3; }
        .guide-block .features-item .icon i { font-size: 30px; }
        .lesson-row.is-current { background: var(--white, #fff); border-color: transparent; box-shadow: 0 8px 24px rgba(0,0,0,.08); }
        .lesson-row.is-current .lesson-status { background: var(--primary, #D97757); border-color: transparent; color: #fff; }
        a.lesson-row { color: inherit; text-decoration: none; }
        .cost-price { flex: 0 0 auto; font-size: 20px; font-weight: 700; white-space: nowrap; }
        .cost-total { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 24px; border-radius: 16px; background: #1F1E1D; color: #fff; margin-bottom: 16px; }
        .cost-total .cost-price { font-size: 26px; }
        .guide-next { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
        .section-process.guide-prep { padding-bottom: 0; overflow-x: clip; }
        @media (max-width: 767px) {
            .guide-block { margin-bottom: 48px; }
            .guide-lead { font-size: 18px; }
            .cost-price { font-size: 17px; }
            .cost-total { flex-direction: column; align-items: flex-start; }
            .guide-prep .swiper { overflow: visible; }
            .guide-prep .swiper-wrapper { flex-direction: column; gap: 16px; transform: none !important; }
            .guide-prep .swiper-slide { width: 100% !important; margin: 0 !important; height: auto; }
        }
        @media (max-width: 575px) {
            .cost-row .cost-price { margin-inline-start: 50px; }
        }'''


def sub1(html, pattern, repl):
    new, n = re.subn(pattern, repl, html, count=1, flags=re.S)
    assert n == 1, pattern
    return new


def section(html, name, new):
    return sub1(html, rf"<!-- {re.escape(name)} -->.*?<!-- /{re.escape(name)} -->", lambda m: new.strip())


def head(html, title, description):
    html = sub1(html, r"<title>.*?</title>", lambda m: f"<title>{title}</title>")
    html = sub1(html, r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{description}">')
    html = html.replace("    </style>\n</head>", CSS + "\n    </style>\n</head>", 1)
    # התפריט: המדריך פעיל במקום הקורס
    html = html.replace('class="item-link link1 active"', 'class="item-link link1"')
    html = html.replace('<a href="guide-1.html" class="item-link link1">', '<a href="guide-1.html" class="item-link link1 active">', 1)
    return html


def hero(html, line1, line2, text):
    html = sub1(html, r'(<span class="title1 fw-semibold text-gradient-1">).*?(</span>)', lambda m: m.group(1) + line1 + m.group(2))
    html = sub1(html, r'(<div class="title2 d-flex gap-20 justify-content-center flex-wrap">\s*<span class="fw-semibold text-gradient-1">).*?(</span>)',
                lambda m: m.group(1) + line2 + m.group(2))
    return sub1(html, r'(<p class="text text-body-3 effectFade fadeUp">).*?(</p>)', lambda m: m.group(1) + text + m.group(2))


def feature_cards(cards):
    out = []
    for i, (icon, title, text) in enumerate(cards):
        delay = f' data-delay="0.{i % 2}"' if i % 2 else ""
        out.append(f'''                    <div class="col-md-6 mb-24">
                        <div class="features-item style-2 h-100 effectFade fadeRotateX"{delay}>
                            <div class="icon"><i class="icon-{icon}"></i></div>
                            <h4 class="title fw-semibold">{title}</h4>
                            <p class="text-secondary">{text}</p>
                        </div>
                    </div>''')
    return "\n".join(out)


def process_cards(steps):
    out = []
    for i, (icon, title, text, tag) in enumerate(steps, 1):
        out.append(f'''                                        <div class="swiper-slide">
                                            <div class="process-card">
                                                <i class="icon icon-{icon}"></i>
                                                <div class="content">
                                                    <h4 class="title fw-semibold">{title}</h4>
                                                    <p class="text text-secondary">{text}</p>
                                                </div>
                                                <div class="bot">
                                                    <div class="time fw-semibold">{tag}</div>
                                                    <div class="number">
                                                        <span class="text-neutral-400">{i:02d}</span>
                                                        <span class="text-neutral-200">/{len(steps):02d}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>''')
    return "\n".join(out)


def cost_rows(rows):
    out = []
    for i, (name, what, price) in enumerate(rows, 1):
        out.append(f'''                            <li class="lesson-row cost-row effectFade fadeUp">
                                <span class="lesson-num text-body-1 fw-semibold">{i:02d}</span>
                                <div class="lesson-body">
                                    <div class="lesson-title fw-semibold">{name}</div>
                                    <div class="lesson-desc text-secondary">{what}</div>
                                </div>
                                <span class="cost-price">{price}</span>
                            </li>''')
    return "\n".join(out)


def glossary(items):
    rows = []
    for i, (q, a) in enumerate(items, 1):
        first = i == 1
        delay = f' data-delay="0.{i - 1}"' if i > 1 else ""
        rows.append(f'''                            <div class="accordion-asked-item effectFade fadeRotateX"{delay}>
                                <div class="accordion-asked-title" id="asked{i}">
                                    <button class="accordion-button text-body-1 fw-semibold{'' if first else ' collapsed'}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{i}" aria-expanded="{'true' if first else 'false'}" aria-controls="collapse{i}">
                                        {q}
                                        <span class="right-icon"></span>
                                    </button>
                                </div>
                                <div id="collapse{i}" role="region" class="accordion-collapse collapse{' show' if first else ''}" aria-labelledby="asked{i}" data-bs-parent="#accordion-asked">
                                    <div class="accordion-body">{a}</div>
                                </div>
                            </div>''')
    return "\n".join(rows)


def chapter_list(current):
    rows = []
    for i, (title, desc, href) in enumerate(CHAPTERS, 1):
        if i == current:
            status, cls, tag, link = "אתם כאן", " is-current", "div", ""
        elif href:
            status, cls, tag, link = "לקריאה", "", "a", f' href="{href}"'
        else:
            status, cls, tag, link = "בקרוב", "", "div", ""
        rows.append(f'''                            <li>
                                <{tag}{link} class="lesson-row{cls} effectFade fadeUp">
                                    <span class="lesson-num text-body-1 fw-semibold">{i:02d}</span>
                                    <div class="lesson-body">
                                        <div class="lesson-title fw-semibold">{title}</div>
                                        <div class="lesson-desc text-secondary">{desc}</div>
                                    </div>
                                    <span class="tags-item fw-semibold lesson-status">{status}</span>
                                </{tag}>
                            </li>''')
    return "\n".join(rows)


# =====================================================================
# פרק 1 – לפני שמתחילים
# =====================================================================
def build_chapter_1():
    html = (SITE / "service-single.html").read_text()
    html = head(html, "לפני שמתחילים – המדריך המלא ל-Claude Code | Free AI",
                "פרק 1 במדריך המלא ל-Claude Code למי שלא מתכנת: למי זה מתאים, מה אפשר לבנות, מה צריך להכין וכמה זה עולה בחודש.")
    html = hero(html, "לפני", "שמתחילים", f"המדריך המלא ל-Claude Code · פרק 1 מתוך {len(CHAPTERS)} · 5 דקות קריאה")

    builds = feature_cards([
        ("desktop-solid", "אתר לעסק", "דף בית, שירותים, תמונות וכפתור וואטסאפ. בדיוק כמו שאתם רוצים אותו."),
        ("bolt-solid", "דף נחיתה", "עמוד אחד עם מטרה אחת: שישאירו פרטים או יקנו."),
        ("clipboard-check-solid", "מערכת הזמנות", "לקוחות קובעים תור או מזמינים לבד, ואתם רואים הכל במקום אחד."),
        ("user-friends-solid", "אזור אישי ללקוחות", "הרשמה, כניסה ותוכן שרק הלקוחות שלכם רואים."),
    ])

    prep = process_cards([
        ("desktop-solid", "מחשב", "Mac או Windows. לא חייב חדש ולא חייב חזק.", "יש לכם כבר"),
        ("envelope-solid", "מייל", "איתו נרשמים לכל השירותים במדריך. עדיף מייל אחד לכולם.", "יש לכם כבר"),
        ("credit-card-solid", "כרטיס אשראי", "למנוי של Claude ולאחסון האתר. את הסכומים תראו מיד למטה.", "2 דקות"),
    ])

    costs = cost_rows([
        ("Claude", "המנוי שכולל את Claude Code. זה מה שבונה בשבילכם.", "כ-20 דולר לחודש"),
        ("GitHub", "הכספת שבה נשמר הפרויקט.", "חינם"),
        ("Supabase", "הזיכרון של המוצר. רק אם צריך, ולא כל אתר צריך.", "חינם להתחלה"),
        ("4CODE", "האחסון של האתר, כולל כתובת חינמית.", "לפי המחירון באתר 4CODE"),
    ])

    main = f'''<!-- section-services-single -->
        <div id="services" class="section-services-single flat-spacing pt-0">
            <div class="container">
                <div class="row">
                    <div class="col-12">
                        <div class="top-image mb-40 effectFade fadeZoom">
                            <img src="assets/images/claude/build-site.jpg" alt="אתר של מאפייה שנבנה עם Claude Code">
                        </div>
                    </div>
                </div>

                <div class="guide-block" id="who">
                    <div class="row">
                        <div class="col-12">
                            <span class="guide-kicker effectFade fadeUp">למי זה מתאים</span>
                            <div class="heading fw-semibold mb-20 effectFade fadeUp">לא צריך לדעת לתכנת</div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-7 md-mb-24">
                            <p class="text-secondary guide-lead effectFade fadeUp">המדריך הזה נכתב לבעלי עסקים, לפרילנסרים ולכל מי שיש לו רעיון ואין לו מתכנת. אתם מסבירים ל-Claude Code במילים שלכם מה אתם רוצים, והוא בונה. אנחנו נלך איתכם צעד אחרי צעד, מהורדת האפליקציה ועד אתר שעובד באוויר.</p>
                        </div>
                        <div class="col-md-5">
                            <p class="text-secondary mb-30 effectFade fadeUp">אם אתם יודעים לשלוח מייל ולהתקין אפליקציה בטלפון, אתם יודעים מספיק.</p>
                            <div class="list-tags effectFade fadeUp">
                                <a href="#chapters" class="tags-item fw-semibold">{len(CHAPTERS)} פרקים</a>
                                <a href="#who" class="tags-item fw-semibold">בלי ידע קודם</a>
                                <a href="#costs" class="tags-item fw-semibold">בעברית פשוטה</a>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="guide-block mb-0" id="build">
                    <div class="row">
                        <div class="col-12">
                            <span class="guide-kicker effectFade fadeUp">מה יוצא לכם מזה</span>
                            <div class="heading fw-semibold mb-20 effectFade fadeUp">מה תדעו לבנות בסוף</div>
                            <p class="text-secondary mb-30 effectFade fadeUp">בסוף המדריך יהיה לכם אתר משלכם באוויר, ותדעו לבנות את הבא לבד.</p>
                        </div>
                    </div>
                    <div class="row">
{builds}
                    </div>
                </div>
            </div>
        </div>
        <!-- /section-services-single -->
        <!-- section-process -->
        <div class="section-process guide-prep flat-spacing pt-0" id="prep">
            <div class="container">
                <div class="row">
                    <div class="col-lg-5">
                        <div class="process-heading h-100">
                            <div class="heading-section mb-80">
                                <div class="heading-sub fw-semibold effectFade fadeUp">מה צריך להכין</div>
                                <div class="heading-title text-gradient-3 effectFade fadeRotateX">שלושה דברים <br> וזהו</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-7">
                        <div class="process-slide">
                            <div dir="rtl" class="swiper tf-swiper swiper-box-shadow" data-preview="3" data-tablet="3" data-mobile-sm="1" data-mobile="1"
                                data-loop="false" data-center="false" data-space-lg="24" data-space-md="24" data-space="30" >
                                <div class="swiper-wrapper">
{prep}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="hosting-note effectFade fadeUp mt-4">
                    <i class="icon icon-bolt-solid"></i>
                    <div>
                        <div class="fw-semibold mb-4">ואיפה האתר יגור?</div>
                        <p class="text-secondary mb-0">במדריך נעבוד עם 4CODE, אחסון ישראלי עם תמיכה בעברית. נפתח שם משתמש ביחד בפרק 6, אז כרגע לא צריך לעשות כלום.</p>
                        <p class="text-body-3 text-neutral-400 mt-2 mb-0">{DISCLOSURE}</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- /section-process -->
        <!-- section-costs -->
        <div class="section-services-single flat-spacing" id="costs" style="margin-top:0">
            <div class="container">
                <div class="row">
                    <div class="col-12">
                        <span class="guide-kicker effectFade fadeUp">כמה זה עולה בחודש</span>
                        <div class="heading fw-semibold mb-20 effectFade fadeUp">פחות מארוחה במסעדה</div>
                        <p class="text-secondary mb-30 effectFade fadeUp">אלה כל השירותים שנשתמש בהם במדריך. רק שניים מהם עולים כסף.</p>
                        <ol class="lesson-list">
{costs}
                        </ol>
                        <div class="cost-total effectFade fadeUp">
                            <div>
                                <div class="fw-semibold">בשביל להתחיל לבנות</div>
                                <div class="text-body-3" style="opacity:.7">את האחסון מוסיפים רק כשמעלים את האתר לאוויר.</div>
                            </div>
                            <span class="cost-price">כ-20 דולר לחודש</span>
                        </div>
                        <p class="text-body-3 text-neutral-400 mb-0 effectFade fadeUp">המחירים נכונים ליום כתיבת המדריך ויכולים להשתנות. בכל פרק נראה איפה בודקים את המחיר העדכני.</p>
                    </div>
                </div>
            </div>
        </div>
        <!-- /section-costs -->'''
    html = section(html, "section-services-single", main)

    # ---------- מילון קצר (בעיצוב השאלות הנפוצות) ----------
    html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">שאלות נפוצות</div>',
                        '<div class="heading-sub fw-semibold effectFade fadeUp">מילון קצר</div>', 1)
    html = sub1(html, r'(<div class="heading-title text-gradient-3 effectFade fadeRotateX">)\s*שאלות <br>ותשובות\s*(</div>)',
                lambda m: m.group(1) + "חמש מילים <br>שכדאי להכיר" + m.group(2))
    html = sub1(html, r'(<div class="accordion-asked" id="accordion-asked">).*?(\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <!-- /section-faqs -->)',
                lambda m: m.group(1) + "\n" + glossary([
                    ("אתר", "דפים שכל אחד יכול לפתוח בדפדפן, כמו חלון ראווה של העסק שלכם."),
                    ("אפליקציה", "אתר שגם עושה דברים: נרשמים אליו, מזמינים דרכו, והוא זוכר כל משתמש."),
                    ("קוד", "ההוראות שמהן בנוי האתר. Claude Code כותב אותן, ואתם לא צריכים לקרוא אותן."),
                    ("שרת", "מחשב שדולק כל הזמן ומציג את האתר שלכם לכל מי שנכנס. זה מה שנקרא אחסון."),
                    ("מסד נתונים", "הזיכרון של האתר. שם נשמרים הלקוחות, ההזמנות וכל מה שהאתר צריך לזכור."),
                ]) + m.group(2))

    # ---------- כל הפרקים (במקום טופס ההרשמה) ----------
    chapters = f'''<!-- section-contact -->
        <div id="chapters" class="section-services-single flat-spacing pt-0" style="margin-top:0">
            <div class="container">
                <div class="row">
                    <div class="col-12">
                        <span class="guide-kicker effectFade fadeUp">המדריך המלא</span>
                        <div class="heading fw-semibold mb-20 effectFade fadeUp">כל הפרקים</div>
                        <p class="text-secondary mb-30 effectFade fadeUp">{len(CHAPTERS)} פרקים, לפי הסדר. פרק חדש עולה בכל פעם.</p>
                        <ol class="lesson-list">
{chapter_list(1)}
                        </ol>
                        <div class="guide-next effectFade fadeUp">
                            <span class="tf-btn" style="opacity:.5;pointer-events:none">הפרק הבא: Claude הרגיל מול Claude Code – בקרוב</span>
                            <a href="service.html" class="tf-btn-2">מעדיפים וידאו? לקורס</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- /section-contact -->'''
    html = section(html, "section-contact", chapters)

    (SITE / "guide-1.html").write_text(html)
    print("guide-1.html done")


build_chapter_1()
