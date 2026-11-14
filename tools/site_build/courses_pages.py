"""עמודי הקורסים של Free AI: service.html (כל המסלולים) ו-service-single.html (מסלול Claude מאפס)."""
import re
from pathlib import Path
from common import apply_common

ROOT = Path(__file__).resolve().parents[2]

DISCLOSURE = "גילוי נאות: Free AI מקבל עמלה מ-4CODE על הרשמה דרך הקישור שלנו. זה לא משנה לכם את המחיר."

LESSONS = [
    ("מה זה Claude ואיך מתחילים", "פותחים חשבון, מכירים את המסך ושואלים את השאלה הראשונה."),
    ("איך מבקשים נכון", "איך לכתוב בקשה שמקבלת תשובה טובה כבר בפעם הראשונה."),
    ("פרויקטים וקבצים", "מעלים מסמכים, שומרים הקשר ועובדים על נושא אחד לאורך זמן."),
    ("Artifacts – בונים דברים בתוך הצ'אט", "מסמכים, טבלאות ודפים שנבנים מול העיניים."),
    ("סקילים – משדרגים את Claude בלחיצה", "מתקינים סקיל ומקבלים יכולת חדשה בלי להסביר כל פעם מחדש."),
    ("חיבור לכלים שאתם כבר משתמשים בהם", "מחברים את Claude למייל, ליומן ולמסמכים שלכם."),
    ("Claude Code – בונים אתר בלי לכתוב קוד", "מתארים במילים מה רוצים, ו-Claude בונה את האתר."),
    ("מעלים לאוויר", "דומיין ואחסון – כדי שהאתר שבניתם יעבוד 24/7."),
]

SIGNUP_FORM = '''<form class="form-contact effectFade fadeUp" id="signup" data-signup>
                                <h4 class="heading fw-semibold">הרשמה חינם</h4>
                                <fieldset class="mb-21">
                                    <label class="fw-semibold text-body-3 mb-20">שם מלא</label>
                                    <input type="text" name="name" placeholder="השם שיופיע בתעודה" required>
                                </fieldset>
                                <fieldset class="mb-21">
                                    <label class="fw-semibold text-body-3 mb-20">מייל</label>
                                    <input type="email" name="email" dir="ltr" placeholder="name@example.com" required>
                                </fieldset>
                                <button type="submit" class="tf-btn w-100">שלחו לי קוד כניסה</button>
                                <p class="text-body-3 text-secondary mt-3 mb-0">בהרשמה אתם מסכימים ל<a href="terms.html" class="link-underline">תנאי השימוש</a> ול<a href="privacy.html" class="link-underline">מדיניות הפרטיות</a>.</p>
                            </form>'''


def sub1(html, pattern, repl, flags=re.S):
    new, n = re.subn(pattern, repl, html, count=1, flags=flags)
    assert n == 1, pattern
    return new


def rep(html, pairs):
    for a, b in pairs:
        assert a in html, a
        html = html.replace(a, b, 1)
    return html


def add_style(html, css):
    return html.replace("</head>", f"    <style>\n{css}\n    </style>\n</head>", 1)


def hero(html, line1, line2, text):
    html = sub1(html, r'(<span class="title1 fw-semibold text-gradient-1">).*?(</span>)', lambda m: m.group(1) + line1 + m.group(2))
    html = sub1(html, r'(<div class="title2 d-flex gap-20 justify-content-center flex-wrap">\s*<span class="fw-semibold text-gradient-1">).*?(</span>)',
                lambda m: m.group(1) + line2 + m.group(2))
    html = sub1(html, r'(<div class="section-hero v\d">.*?<p class="text[^"]*">).*?(</p>)', lambda m: m.group(1) + "\n                        " + text + "\n                    " + m.group(2))
    return html


def process(html, heading_title, steps):
    html = rep(html, [
        ('<div class="heading-sub fw-semibold effectFade fadeUp">Process</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">איך זה עובד</div>'),
        ('<div class="heading-title text-gradient-3 effectFade fadeRotateX">From Idea <br> to Production</div>', f'<div class="heading-title text-gradient-3 effectFade fadeRotateX">{heading_title}</div>'),
        ('<div dir="ltr" class="swiper tf-swiper swiper-box-shadow"', '<div dir="rtl" class="swiper tf-swiper swiper-box-shadow"'),
    ])
    olds = [
        ("Discover & Scope", "Align on problems, data reality, and success metrics. Opportunity brief, KPI model, phased roadmap, effort/cost ranges.", "3-7 DAYS"),
        ("<h4 class=\"title fw-semibold\">Prototype</h4>", "De-risk unknowns and validate value quickly. Clickable UX, tech spike repo, initial eval rubric, demo.", "1-2 WEEKS"),
        ("Validate & Evals", "Prove accuracy, usability, safety, and cost. Eval dashboard, acceptance thresholds, decision to iterate/ship.", "1 WEEKS"),
    ]
    for (ot, ox, otime), (t, x, time) in zip(olds, steps):
        if ot.startswith("<h4"):
            t = f'<h4 class="title fw-semibold">{t}</h4>'
        html = rep(html, [(ot, t), (ox, x), (otime, time)])
    return html


def faqs(html, items, title="שאלות <br>ותשובות"):
    html = rep(html, [
        ('<div class="heading-sub fw-semibold effectFade fadeUp">FAQs</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">שאלות נפוצות</div>'),
        ("Frequently Asked <br>Questions", title),
    ])
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
                                    <div class="accordion-body">
                                        {a}
                                    </div>
                                </div>
                            </div>''')
    return sub1(html, r'(<div class="accordion-asked" id="accordion-asked">).*?(\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <!-- /section-faqs -->)',
                lambda m: m.group(1) + "\n" + "\n".join(rows) + m.group(2))


def signup(html, title):
    html = rep(html, [
        ('<div id="contact" class="flat-spacing pt-0">', '<div id="contact" class="flat-spacing pt-0">'),
        ('<div class="heading-sub fw-semibold effectFade fadeUp">Contact</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הרשמה</div>'),
        ("Let’s Build <br> Intelligent Things", title),
        ('<div class="title fw-semibold mb-2">E-mail address</div>\n                                            <div class="text">hello@youraiagency.com</div>',
         '<div class="title fw-semibold mb-2">פחות מדקה</div>\n                                            <div class="text">הרשמה עם Google או קוד למייל</div>'),
        ('<i class="icon icon-envelope-solid"></i>', '<i class="icon icon-bolt-solid"></i>'),
        ('<div class="title fw-semibold mb-2">Phone number</div>\n                                            <div class="text">+1 (647) 555 0172</div>',
         '<div class="title fw-semibold mb-2">בחינם, לתמיד</div>\n                                            <div class="text">בלי כרטיס אשראי ובלי מנוי</div>'),
        ('<i class="icon icon-headset-solid"></i>', '<i class="icon icon-check-solid"></i>'),
    ])
    return sub1(html, r'<form class="form-contact effectFade fadeUp">.*?</form>', lambda m: SIGNUP_FORM)


def check_english(name, html):
    body = html.split("<body", 1)[1]
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    left = re.findall(r">\s*([^<>]*[A-Za-z]{3,}[^<>]*?)\s*<", body)
    allowed = ("Claude", "Lovable", "n8n", "Free AI", "Artifacts", "Google", "4CODE", "ChatGPT", "Gemini", "Cursor", "Supabase", "Code")
    bad = [x for x in left if re.sub("|".join(allowed), "", x) and re.search(r"[A-Za-z]{3,}", re.sub("|".join(allowed), "", x))]
    print(f"{name} done; leftover English:", bad[:20])


PROCESS_STEPS = [
    ("נרשמים", "בלחיצה עם Google, או עם קוד שמגיע למייל. בלי סיסמה ובלי כרטיס אשראי.", "דקה אחת"),
    ("צופים ומתרגלים", "סרטון קצר, סיכום, קישורים וקבצים להורדה בכל שיעור. האתר זוכר איפה עצרתם.", "בקצב שלכם"),
    ("מקבלים תעודה", "מסיימים מסלול ומקבלים תעודת סיום עם השם שלכם – להראות ללקוחות ולמעסיקים.", "בסוף מסלול"),
]

COMMON_CSS = '''        .accordion-faq_item.style-1 .accordion-title { gap: 16px; }
        .track-status { display: inline-block; font-size: 14px; font-weight: 600; padding: 6px 14px; line-height: 1.3; letter-spacing: 0; border-radius: 999px; margin-inline-start: 12px; vertical-align: middle; white-space: nowrap; }
        .track-status.open { background: var(--brand, #7a5cff); color: #fff; }
        .track-status.soon { background: rgba(255,255,255,.12); color: inherit; border: 1px solid currentColor; opacity: .7; }'''


# =====================================================================
# service.html – כל המסלולים
# =====================================================================
def build_service():
    html = (ROOT / "aigocy-about/service.html").read_text()
    html = apply_common(html, "service.html", "קורסים – Free AI",
                        "5 מסלולי AI בעברית, בחינם: Claude מאפס, Lovable, סוכני AI, אוטומציות n8n והעלאה לאוויר.")

    html = hero(html, "קורסי AI", "בעברית, בחינם",
                "חמישה מסלולים קצרים ומעשיים – מהשאלה הראשונה ל-Claude ועד אתר, אפליקציה <br> או אוטומציה שעובדים באוויר. בלי לשלם שקל.")

    # ---------- Services → המסלולים ----------
    html = rep(html, [
        ('<div class="heading-sub fw-semibold effectFade fadeUp">Services</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">המסלולים</div>'),
        ('<div class="heading-title text-gradient-3 effectFade fadeRotateX">End-to-End AI Services</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">מה לומדים כאן</div>'),
        ("We turn ambiguous AI ideas into production features your users trust—combining strategy, <br> design, engineering, and rigorous evaluation.",
         "המסלול הראשון כבר פתוח, והשאר מצטרפים בהדרגה. <br> כל מסלול מתחיל מאפס ונגמר במשהו שעובד באמת."),
    ])
    tracks = [
        ("Claude מאפס", True, "service-5.jpg",
         "הקורס המלא – מהשאלה הראשונה ועד עבודה יומיומית עם Claude. 8 שיעורים קצרים: איך מבקשים נכון, פרויקטים וקבצים, Artifacts, סקילים, חיבור לכלים, ובסוף בונים אתר עם Claude Code ומעלים אותו לאוויר.",
         ["8 שיעורים", "מתחילים", "לרשימת השיעורים"]),
        ("בונים אפליקציה עם Lovable", False, "service-6.jpg",
         "מרעיון לאפליקציה אמיתית – בלי לכתוב קוד. מסכים ועיצוב, משתמשים והרשמה, ומסד נתונים שמחזיק את המידע.",
         ["מסכים ועיצוב", "משתמשים והרשמה", "מסד נתונים"]),
        ("סוכני AI", False, "service-7.jpg",
         "עוזרים שעובדים בשבילכם, גם כשאתם לא. בונים סוכן שעונה ללקוחות, מתחבר לכלים שלכם ומבצע משימות לבד.",
         ["סוכן שירות לקוחות", "חיבור לכלים", "משימות אוטומטיות"]),
        ("אוטומציות עם n8n", False, "service-8.jpg",
         "תהליכים שרצים לבד וחוסכים שעות כל שבוע: לידים שנכנסים ל-CRM, מיילים והודעות שיוצאים בזמן, ותבניות מוכנות להורדה.",
         ["לידים ו-CRM", "מיילים והודעות", "תבניות מוכנות"]),
        ("מעלים לאוויר", False, "service-1.jpg",
         "דומיין, אחסון ושרת שעובד 24/7 – צעד אחרי צעד, עם 4CODE. כדי שכל מה שבניתם במסלולים האחרים יהיה זמין לכולם.<br><small class=\"text-neutral-400\">" + DISCLOSURE + "</small>",
         ["דומיין", "אחסון", "שרת שרץ כל הזמן"]),
    ]
    items = []
    for i, (title, is_open, img, text, tags) in enumerate(tracks, 1):
        first = i == 1
        status = '<span class="track-status open">פתוח עכשיו</span>' if is_open else '<span class="track-status soon">בקרוב</span>'
        href = "service-single.html" if is_open else "contact.html#signup"
        tag_html = "\n".join(f'                                        <a href="{href}" class="tags-item fw-semibold">{t}</a>' for t in tags)
        items.append(f'''                    <div class="accordion-faq_item style-1 effectFade fadeRotateX" role="presentation">
                        <div class="accordion-action{'' if first else ' collapsed'}" data-bs-target="#faq-{i}" role="button"
                            data-bs-toggle="collapse" aria-controls="faq-{i}" aria-expanded="{'true' if first else 'false'}">
                            <div class="accordion-title">
                                <span>{title} {status}</span>
                                <i class="icon icon-arrow-top-right"></i>
                            </div>
                        </div>
                        <div id="faq-{i}" class="collapse{' show' if first else ''}" data-bs-parent="#accordion-services">
                            <div class="accordion-content">
                                <div class="image">
                                    <img src="assets/images/section/{img}" alt="">
                                </div>
                                <div class="content">
                                    <div class="text-body-3 text-neutral-300 text">{text}</div>
                                    <div class="list-tags">
{tag_html}
                                    </div>
                                    <div class="text-body-1 num">0{i}</div>
                                </div>
                            </div>
                        </div>
                    </div>''')
    html = sub1(html, r'(<div class="accordion-faq_list gap-32" id="accordion-services">).*?(\n                </div>\n            </div>\n        </div>\n        <!-- /section-services -->)',
                lambda m: m.group(1) + "\n" + "\n".join(items) + m.group(2))

    # ---------- Partner → הכלים שלומדים ----------
    tools = ["Claude", "Lovable", "n8n", "Claude Code", "ChatGPT", "Gemini", "Cursor", "Supabase"]
    html = rep(html, [('<p class="text-secondary text fw-semibold">Trusted by 100+ <br> top-tier brands</p>', '<p class="text-secondary text fw-semibold">הכלים <br> שלומדים כאן</p>')])
    html = sub1(html, r'(<div class="infiniteSlide infiniteSlide_partner" data-clone="5">).*?(</div>)',
                lambda m: m.group(1) + "".join(f'\n                                    <span class="tool-name">{t}</span>' for t in tools) + "\n                                " + m.group(2))

    # ---------- Process ----------
    html = process(html, "שלושה צעדים. <br> אפס שקלים.", PROCESS_STEPS)

    # ---------- Pricing: מוסר (אין מחירים – הכל חינם, ודף הבית כבר משווה) ----------
    html = sub1(html, r"\s*<!-- section-pricing -->.*?<!-- /section-pricing -->", "")

    # ---------- FAQ ----------
    html = faqs(html, [
        ("הקורסים באמת בחינם?", "כן. כל המסלולים, השיעורים, הקבצים והתעודות – בחינם, בלי כרטיס אשראי ובלי מנוי."),
        ("באיזה מסלול כדאי להתחיל?", "אם אתם חדשים ב-AI – ב-Claude מאפס. הוא נותן את הבסיס לכל שאר המסלולים, ובסופו כבר תבנו אתר ותעלו אותו לאוויר."),
        ("מתי ייפתחו שאר המסלולים?", "המסלולים נפתחים אחד אחרי השני, לפי קצב הצילום. מי שנרשם יראה כל מסלול חדש ברגע שהוא עולה."),
        ("צריך ידע קודם או ידע בקוד?", "לא. כל מסלול מתחיל מאפס ומסביר כל צעד בעברית פשוטה. גם בשיעורים שבונים בהם אתרים לא כותבים קוד."),
        ("למה צריך להירשם?", "ההרשמה פותחת את הסרטונים וההורדות, שומרת את ההתקדמות ומאפשרת לקבל תעודה בסוף מסלול. היא לוקחת פחות מדקה – עם Google או עם קוד למייל."),
    ])

    # ---------- Contact → הרשמה ----------
    html = signup(html, "מתחילים מהשיעור <br> הראשון")

    html = add_style(html, COMMON_CSS)
    (ROOT / "site/service.html").write_text(html)
    check_english("service.html", html)


# =====================================================================
# service-single.html – מסלול Claude מאפס
# =====================================================================
def build_single():
    html = (ROOT / "aigocy-about/service-single.html").read_text()
    html = apply_common(html, "service.html", "Claude מאפס – הקורס המלא | Free AI",
                        "קורס Claude מאפס בעברית ובחינם: 8 שיעורים קצרים, מהשאלה הראשונה ועד אתר שבניתם עם Claude Code ועובד באוויר.")

    html = hero(html, "Claude", "מאפס",
                "הקורס המלא, בעברית ובחינם. מהשאלה הראשונה ועד אתר שבניתם בעצמכם <br> עם Claude Code – ועובד באוויר.")

    # ---------- תיאור ----------
    html = rep(html, [
        ('<div class="heading fw-semibold mb-20 effectFade fadeUp">Innovative AI UX & Product Design</div>',
         '<div class="heading fw-semibold mb-20 effectFade fadeUp">על המסלול</div>'),
    ])
    html = sub1(html, r'(<div class="col-md-7 md-mb-24">\s*<p class="text-secondary effectFade fadeUp">).*?(</p>)',
                lambda m: m.group(1) + "\n                            Claude הוא אחד מכלי ה-AI החזקים שיש היום, אבל רוב האנשים משתמשים רק בחלק קטן ממה שהוא יודע לעשות. במסלול הזה עוברים צעד אחרי צעד: פותחים חשבון, לומדים לבקש נכון, עובדים עם קבצים ופרויקטים, בונים מסמכים ודפים בתוך הצ'אט, מתקינים סקילים ומחברים את Claude לכלים שאתם כבר משתמשים בהם. בסוף המסלול בונים אתר שלם עם Claude Code – בלי לכתוב שורת קוד – ומעלים אותו לאוויר.\n                        " + m.group(2))
    html = sub1(html, r'(<div class="col-md-5">\s*<p class="text-secondary mb-30 effectFade fadeUp">).*?(</p>)',
                lambda m: m.group(1) + "\n                            מתאים לבעלי עסקים, לפרילנסרים ולכל מי שסקרן. לא צריך ידע קודם – רק מחשב וחשבון Claude. כל שיעור קצר וממוקד, ונגמר במשהו שאפשר להשתמש בו מיד.\n                        " + m.group(2))
    html = sub1(html, r'(<div class="list-tags effectFade fadeUp">).*?(</div>)',
                lambda m: m.group(1) + '''
                            <a href="#lessons" class="tags-item fw-semibold">8 שיעורים</a>
                            <a href="#lessons" class="tags-item fw-semibold">מתחילים</a>
                            <a href="contact.html#signup" class="tags-item fw-semibold">בחינם</a>
                        ''' + m.group(2))

    # ---------- What We Do → רשימת השיעורים ----------
    rows = []
    for i, (title, desc) in enumerate(LESSONS, 1):
        rows.append(f'''                            <li class="lesson-row effectFade fadeUp">
                                <span class="lesson-num text-body-1 fw-semibold">{i:02d}</span>
                                <div class="lesson-body">
                                    <div class="lesson-title fw-semibold">{title}</div>
                                    <div class="lesson-desc text-secondary">{desc}</div>
                                </div>
                                <span class="tags-item fw-semibold lesson-status">בצילום</span>
                            </li>''')
    lessons_html = '''<div class="row mb-80" id="lessons">
                    <div class="col-12">
                        <div class="heading fw-semibold mb-20 effectFade fadeUp">רשימת השיעורים</div>
                        <p class="text-secondary mb-30 effectFade fadeUp">8 שיעורים, לפי הסדר. הסרטונים בצילום עכשיו ויעלו בקרוב – מי שנרשם יראה כל שיעור ברגע שהוא עולה.</p>
                        <ol class="lesson-list">
''' + "\n".join(rows) + f'''
                        </ol>
                        <div class="hosting-note effectFade fadeUp">
                            <i class="icon icon-bolt-solid"></i>
                            <div>
                                <div class="fw-semibold mb-4">בשיעור 8 מעלים את האתר לאוויר עם 4CODE</div>
                                <p class="text-secondary mb-0">כדי שהאתר יעבוד 24/7 צריך אחסון. בשיעור מראים צעד אחרי צעד איך מחברים דומיין ואחסון ב-4CODE – חברת האחסון שאנחנו עובדים איתה.</p>
                                <p class="text-body-3 text-neutral-400 mt-2 mb-0">{DISCLOSURE}</p>
                            </div>
                        </div>
                    </div>
                </div>'''
    html = sub1(html, r'<div class="row mb-40">\s*<div class="col-12">\s*<div class="heading fw-semibold mb-20 effectFade fadeUp">What We Do\?</div>.*?</p>\s*</div>\s*</div>',
                lambda m: lessons_html)

    # ---------- Key Deliverables → מה מקבלים ----------
    html = rep(html, [
        ('<div class="heading fw-semibold mb-20 effectFade fadeUp">Key Deliverables</div>', '<div class="heading fw-semibold mb-20 effectFade fadeUp">מה מקבלים</div>'),
        ("Identify high-ROI use cases and define a realistic, measurable AI roadmap. Our AI Strategy & Mapping process aligns technology with business goals through stakeholder discovery, KPI modeling, and data readiness assessment to ensure sustainable growth and measurable transformation. ",
         "בסוף המסלול תדעו לעבוד עם Claude כל יום – ויהיה לכם אתר משלכם שעובד באוויר."),
        ("Human-centered AI experiences that feel intuitive and intelligent", "שליטה בכלים של Claude: פרויקטים, קבצים, Artifacts וסקילים"),
        ("Seamless integration of AI into digital products and workflows", "Claude שמחובר למייל, ליומן ולמסמכים שלכם"),
        ("Data-driven design decisions informed by real user behavior", "אתר שבניתם בעצמכם עם Claude Code – ועובד באוויר"),
        ("Scalable design systems for adaptive, AI-powered products", "תעודת סיום עם השם שלכם"),
        ('<h6 class="title fw-semibold mb-16 effectFade fadeUp">What\'s included service?</h6>', '<h6 class="title fw-semibold mb-16 effectFade fadeUp">בכל שיעור</h6>'),
        ("+ Product Research & Discovery", "+ סרטון קצר וממוקד"),
        ("+ AI & Automation Integration", "+ סיכום וקישורים מתחת לסרטון"),
        ("+ Design System Architecture", "+ קבצים ופרומפטים להורדה"),
        ("+ Continuous Optimization & Testing", "+ סימון ✓ ושמירת התקדמות"),
        ('''<a href="contact.html" class="tf-btn effectFade fadeRotateX">
                            Let’s Connect
                        </a>''', '''<a href="contact.html#signup" class="tf-btn effectFade fadeRotateX">
                            הרשמה חינם
                        </a>'''),
    ])

    # ---------- Process ----------
    html = process(html, "איך לומדים <br> במסלול", [
        ("נרשמים", "בלחיצה עם Google, או עם קוד שמגיע למייל. בלי סיסמה ובלי כרטיס אשראי.", "דקה אחת"),
        ("צופים לפי הסדר", "שיעור אחרי שיעור, כל אחד קצר וממוקד. מסמנים ✓ וממשיכים בדיוק מאיפה שעצרתם.", "8 שיעורים"),
        ("בונים ומעלים לאוויר", "בונים אתר עם Claude Code, מעלים אותו לאוויר ומקבלים תעודת סיום.", "בסוף מסלול"),
    ])

    # ---------- FAQ ----------
    html = faqs(html, [
        ("צריך לשלם על Claude?", "אפשר להתחיל עם החשבון החינמי של Claude. בחלק מהשיעורים (למשל Claude Code) נדרש מנוי בתשלום ל-Claude עצמו – נסביר בכל שיעור מה בדיוק צריך."),
        ("מתי עולים הסרטונים?", "השיעורים בצילום עכשיו ויעלו בהדרגה. מי שנרשם יראה כל שיעור ברגע שהוא עולה, והאתר ישמור לו את ההתקדמות."),
        ("צריך לדעת לתכנת?", "לא. גם בשיעור על Claude Code לא כותבים קוד – מתארים במילים מה רוצים, ו-Claude בונה."),
        ("כמה עולה להעלות את האתר לאוויר?", "אחסון ודומיין עולים כסף אצל כל חברת אחסון. בשיעור 8 מראים איך עושים את זה עם 4CODE. " + DISCLOSURE),
        ("מקבלים תעודה?", "כן. מסיימים את כל 8 השיעורים ומקבלים תעודת סיום עם השם שלכם, המסלול והתאריך."),
    ])

    # ---------- Contact → הרשמה ----------
    html = signup(html, "מתחילים את <br> Claude מאפס")

    html = add_style(html, COMMON_CSS + '''
        .lesson-list { list-style: none; padding: 0; margin: 0 0 32px; display: grid; gap: 12px; }
        .lesson-row { display: flex; align-items: center; gap: 20px; padding: 20px 24px; border-radius: 16px; border: 1px solid rgba(127,127,127,.25); }
        .lesson-num { flex: 0 0 auto; min-width: 36px; opacity: .55; }
        .lesson-body { flex: 1 1 auto; min-width: 0; }
        .lesson-title { font-size: 20px; margin-bottom: 4px; }
        .lesson-status { flex: 0 0 auto; pointer-events: none; white-space: nowrap; border: 1px solid rgba(127,127,127,.4); padding: 6px 14px; border-radius: 999px; font-size: 14px; line-height: 1.3; }
        .hosting-note { display: flex; gap: 16px; align-items: flex-start; padding: 24px; border-radius: 16px; background: rgba(127,127,127,.08); }
        .hosting-note > .icon { font-size: 24px; margin-top: 2px; }
        @media (max-width: 575px) {
            .lesson-row { flex-wrap: wrap; gap: 8px 14px; padding: 16px; }
            .lesson-body { flex-basis: calc(100% - 50px); }
            .lesson-status { margin-inline-start: 50px; }
            .lesson-title { font-size: 17px; }
        }''')
    (ROOT / "site/service-single.html").write_text(html)
    check_english("service-single.html", html)


build_service()
build_single()
