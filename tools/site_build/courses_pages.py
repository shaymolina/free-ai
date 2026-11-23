"""עמודי הקורס של Free AI: service.html (פרקי קורס Claude) ו-service-single.html (רשימת השיעורים)."""
from clean_urls import clean
import re
from pathlib import Path
from common import apply_common

ROOT = Path(__file__).resolve().parents[2]

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
    allowed = ("Claude", "Lovable", "n8n", "Free AI", "Artifacts", "Google", "4CODE", "ChatGPT", "Gemini", "Cursor", "Supabase", "Code", "Projects", "Skills", "MCP", "Desktop", "Mobile")
    bad = [x for x in left if re.sub("|".join(allowed), "", x) and re.search(r"[A-Za-z]{3,}", re.sub("|".join(allowed), "", x))]
    print(f"{name} done; leftover English:", bad[:20])


PROCESS_STEPS = [
    ("נרשמים", "בלחיצה עם Google, או עם קוד שמגיע למייל. בלי סיסמה ובלי כרטיס אשראי.", "דקה אחת"),
    ("צופים ומתרגלים", "סרטון קצר, סיכום, קישורים וקבצים להורדה בכל שיעור. האתר זוכר איפה עצרתם.", "בקצב שלכם"),
    ("מקבלים תעודה", "מסיימים את הקורס ומקבלים תעודת סיום עם השם שלכם – להראות ללקוחות ולמעסיקים.", "בסוף הקורס"),
]

COMMON_CSS = '''        .accordion-faq_item.style-1 .accordion-title { gap: 16px; }
        .track-status { display: inline-block; font-size: 14px; font-weight: 600; padding: 6px 14px; line-height: 1.3; letter-spacing: 0; border-radius: 999px; margin-inline-start: 12px; vertical-align: middle; white-space: nowrap; }
        .track-status.open { background: var(--brand, #7a5cff); color: #fff; }
        .track-status.soon { background: rgba(255,255,255,.12); color: inherit; border: 1px solid currentColor; opacity: .7; }'''


# =====================================================================
# service.html – פרקי הקורס
# =====================================================================
def build_service():
    html = (ROOT / "aigocy-about/service.html").read_text()
    html = apply_common(html, "service.html", "קורס קלוד קוד (Claude Code) מאפס – בחינם ובעברית | Free AI",
                        "קורס קלוד קוד (Claude Code) בעברית ובחינם, למי שלא יודע לתכנת: 8 שיעורי וידאו קצרים, מהשאלה הראשונה ועד אתר שבניתם בעצמכם.")

    html = hero(html, "קורס Claude", "המלא, בחינם",
                "קורס אחד, מאפס ועד הסוף – מהשאלה הראשונה ל-Claude ועד אתר <br> שבניתם בעצמכם עם Claude Code. בלי לשלם שקל.")

    # ---------- Services → פרקי הקורס ----------
    html = rep(html, [
        ('<div class="heading-sub fw-semibold effectFade fadeUp">Services</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">פרקי הקורס</div>'),
        ('<div class="heading-title text-gradient-3 effectFade fadeRotateX">End-to-End AI Services</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">מה לומדים בקורס</div>'),
        ("We turn ambiguous AI ideas into production features your users trust—combining strategy, <br> design, engineering, and rigorous evaluation.",
         "חמישה פרקים, שמונה שיעורים קצרים. <br> כל פרק נגמר במשהו שעובד באמת."),
    ])
    tracks = [
        ("מתחילים עם Claude", "claude-start.jpg",
         "פותחים חשבון, מכירים את המסך ושואלים את השאלה הראשונה. בלי ידע קודם.",
         ["שיעור 1", "פותחים חשבון", "השאלה הראשונה"]),
        ("לבקש נכון", "claude-prompt.jpg",
         "איך כותבים בקשה שמקבלת תשובה טובה כבר בפעם הראשונה – ואיך מתקנים כשלא.",
         ["שיעור 2", "בקשה טובה", "דוגמאות מוכנות"]),
        ("Projects וקבצים", "claude-projects.jpg",
         "מלמדים את Claude על העסק שלכם פעם אחת – מעלים מסמכים, והוא זוכר.",
         ["שיעור 3", "מסמכים", "עוזר לעסק"]),
        ("Artifacts", "claude-artifacts.jpg",
         "גרפים, מסמכים וכלים קטנים שנבנים ישר בתוך השיחה, ואפשר לשלוח בקישור.",
         ["שיעור 4", "מסמכים וגרפים", "כלים קטנים"]),
        ("סקילים ו-Claude Code", "claude-code.jpg",
         "מתקינים סקילים, מחברים את Claude למייל וליומן, ובונים אתר שלם עם Claude Code – ומעלים אותו לאוויר.",
         ["שיעורים 5–8", "סקילים", "Claude Code"]),
    ]
    items = []
    for i, (title, img, text, tags) in enumerate(tracks, 1):
        first = i == 1
        href = "service-single.html"
        tag_html = "\n".join(f'                                        <a href="{href}" class="tags-item fw-semibold">{t}</a>' for t in tags)
        items.append(f'''                    <div class="accordion-faq_item style-1 effectFade fadeRotateX" role="presentation">
                        <div class="accordion-action{'' if first else ' collapsed'}" data-bs-target="#faq-{i}" role="button"
                            data-bs-toggle="collapse" aria-controls="faq-{i}" aria-expanded="{'true' if first else 'false'}">
                            <div class="accordion-title">
                                <span>{title}</span>
                                <i class="icon icon-arrow-top-right"></i>
                            </div>
                        </div>
                        <div id="faq-{i}" class="collapse{' show' if first else ''}" data-bs-parent="#accordion-services">
                            <div class="accordion-content">
                                <div class="image">
                                    <img src="assets/images/claude/{img}" alt="">
                                </div>
                                <div class="content">
                                    <div class="text-body-3 text-neutral-300 text">{text}</div>
                                    <div class="text-body-1 num">0{i}</div>
                                </div>
                            </div>
                        </div>
                    </div>''')
    html = sub1(html, r'(<div class="accordion-faq_list gap-32" id="accordion-services">).*?(\n                </div>\n            </div>\n        </div>\n        <!-- /section-services -->)',
                lambda m: m.group(1) + "\n" + "\n".join(items) + m.group(2))

    # ---------- Partner → הכלים שלומדים ----------
    tools = ["Claude", "Projects", "Artifacts", "Skills", "Claude Code", "MCP", "Desktop", "Mobile"]
    html = rep(html, [('<p class="text-secondary text fw-semibold">Trusted by 100+ <br> top-tier brands</p>', '<p class="text-secondary text fw-semibold">מה לומדים <br> בקורס</p>')])
    html = sub1(html, r'(<div class="infiniteSlide infiniteSlide_partner" data-clone="5">).*?(</div>)',
                lambda m: m.group(1) + "".join(f'\n                                    <span class="tool-name">{t}</span>' for t in tools) + "\n                                " + m.group(2))

    # ---------- Process ----------
    html = process(html, "שלושה צעדים. <br> אפס שקלים.", PROCESS_STEPS)

    # ---------- Pricing: מוסר (אין מחירים – הכל חינם, ודף הבית כבר משווה) ----------
    html = sub1(html, r"\s*<!-- section-pricing -->.*?<!-- /section-pricing -->", "")

    # ---------- FAQ ----------
    html = faqs(html, [
        ("הקורס באמת בחינם?", "כן. כל השיעורים, הקבצים, הסקילים והתעודה – בחינם, בלי כרטיס אשראי ובלי מנוי."),
        ("צריך מנוי בתשלום ל-Claude?", "לא בשביל להתחיל. רוב השיעורים עובדים עם החשבון החינמי של Claude. בשיעורים שצריך מנוי – כתוב את זה מראש."),
        ("מתי עולים השיעורים?", "השיעורים עולים אחד אחרי השני, לפי קצב הצילום. מי שנרשם יראה כל שיעור חדש ברגע שהוא עולה."),
        ("צריך ידע קודם או ידע בקוד?", "לא. הקורס מתחיל מפתיחת חשבון ומסביר כל צעד בעברית פשוטה. גם בשיעור על Claude Code לא כותבים קוד."),
        ("למה צריך להירשם?", "ההרשמה פותחת את הסרטונים וההורדות, שומרת את ההתקדמות ומאפשרת לקבל תעודה בסוף הקורס. היא לוקחת פחות מדקה – עם Google או עם קוד למייל."),
    ])

    # ---------- Contact → הרשמה ----------
    html = signup(html, "מתחילים מהשיעור <br> הראשון")

    html = add_style(html, COMMON_CSS)
    (ROOT / "site/service.html").write_text(clean(html))
    check_english("service.html", html)


# =====================================================================
# service-single.html – רשימת השיעורים
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
         '<div class="heading fw-semibold mb-20 effectFade fadeUp">על הקורס</div>'),
    ])
    html = sub1(html, r'(<div class="col-md-7 md-mb-24">\s*<p class="text-secondary effectFade fadeUp">).*?(</p>)',
                lambda m: m.group(1) + "\n                            Claude הוא אחד מכלי ה-AI החזקים שיש היום, אבל רוב האנשים משתמשים רק בחלק קטן ממה שהוא יודע לעשות. בקורס הזה עוברים צעד אחרי צעד: פותחים חשבון, לומדים לבקש נכון, עובדים עם קבצים ופרויקטים, בונים מסמכים ודפים בתוך הצ'אט, מתקינים סקילים ומחברים את Claude לכלים שאתם כבר משתמשים בהם. בסוף הקורס בונים אתר שלם עם Claude Code – בלי לכתוב שורת קוד – ומעלים אותו לאוויר.\n                        " + m.group(2))
    html = sub1(html, r'(<div class="col-md-5">\s*<p class="text-secondary mb-30 effectFade fadeUp">).*?(</p>)',
                lambda m: m.group(1) + "\n                            מתאים לבעלי עסקים, לפרילנסרים ולכל מי שסקרן. לא צריך ידע קודם – רק מחשב וחשבון Claude. כל שיעור קצר וממוקד, ונגמר במשהו שאפשר להשתמש בו מיד.\n                        " + m.group(2))
    html = re.sub(r'\s*<div class="list-tags effectFade fadeUp">.*?</div>', '', html, count=1, flags=re.S)

    # ---------- What We Do → רשימת השיעורים ----------
    rows = []
    for i, (title, desc) in enumerate(LESSONS, 1):
        rows.append(f'''                            <li class="lesson-row effectFade fadeUp">
                                <span class="lesson-num text-body-1 fw-semibold">{i:02d}</span>
                                <div class="lesson-body">
                                    <div class="lesson-title fw-semibold">{title}</div>
                                    <div class="lesson-desc text-secondary">{desc}</div>
                                </div>
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
                                <div class="coupon">
                                    <span class="coupon-label">קוד קופון לחודש ראשון בחינם:</span>
                                    <span class="coupon-code">RVJ34jcn4j1</span>
                                    <button type="button" class="coupon-copy" onclick="navigator.clipboard.writeText('RVJ34jcn4j1');this.textContent='הועתק ✓'">העתקה</button>
                                </div>
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
         "בסוף הקורס תדעו לעבוד עם Claude כל יום – ויהיה לכם אתר משלכם שעובד באוויר."),
        ("Human-centered AI experiences that feel intuitive and intelligent", "שליטה בכלים של Claude: פרויקטים, קבצים, Artifacts וסקילים"),
        ("Seamless integration of AI into digital products and workflows", "Claude שמחובר למייל, ליומן ולמסמכים שלכם"),
        ("Data-driven design decisions informed by real user behavior", "אתר שבניתם בעצמכם עם Claude Code – ועובד באוויר"),
        ("Scalable design systems for adaptive, AI-powered products", "תעודת סיום עם השם שלכם"),
        ('<h6 class="title fw-semibold mb-16 effectFade fadeUp">What\'s included service?</h6>', '<h6 class="title fw-semibold mb-16 effectFade fadeUp">בכל שיעור</h6>'),
        ("+ Product Research & Discovery", "+ סרטון קצר וממוקד"),
        ("+ AI & Automation Integration", "+ סיכום וקישורים מתחת לסרטון"),
        ("+ Design System Architecture", "+ קבצים ופרומפטים להורדה"),
        ("+ Continuous Optimization & Testing", "+ שמירת התקדמות"),
        ('''<a href="contact.html" class="tf-btn effectFade fadeRotateX">
                            Let’s Connect
                        </a>''', '''<a href="contact.html#signup" class="tf-btn effectFade fadeRotateX">
                            הרשמה חינם
                        </a>'''),
    ])

    # ---------- Process ----------
    html = process(html, "איך לומדים <br> בקורס", [
        ("נרשמים", "בלחיצה עם Google, או עם קוד שמגיע למייל. בלי סיסמה ובלי כרטיס אשראי.", "דקה אחת"),
        ("צופים לפי הסדר", "שיעור אחרי שיעור, כל אחד קצר וממוקד. מסמנים ✓ וממשיכים בדיוק מאיפה שעצרתם.", "8 שיעורים"),
        ("בונים ומעלים לאוויר", "בונים אתר עם Claude Code, מעלים אותו לאוויר ומקבלים תעודת סיום.", "בסוף הקורס"),
    ])

    # ---------- FAQ ----------
    html = faqs(html, [
        ("צריך לשלם על Claude?", "אפשר להתחיל עם החשבון החינמי של Claude. בחלק מהשיעורים (למשל Claude Code) נדרש מנוי בתשלום ל-Claude עצמו – נסביר בכל שיעור מה בדיוק צריך."),
        ("מתי עולים הסרטונים?", "השיעורים בצילום עכשיו ויעלו בהדרגה. מי שנרשם יראה כל שיעור ברגע שהוא עולה, והאתר ישמור לו את ההתקדמות."),
        ("צריך לדעת לתכנת?", "לא. גם בשיעור על Claude Code לא כותבים קוד – מתארים במילים מה רוצים, ו-Claude בונה."),
        ("כמה עולה להעלות את האתר לאוויר?", "בשיעור 8 מראים איך עושים את זה עם 4CODE. מתחילים שם בחינם, ומשדרגים רק אם הפרויקט גדל."),
        ("מקבלים תעודה?", "כן. מסיימים את כל 8 השיעורים ומקבלים תעודת סיום עם השם שלכם והתאריך."),
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
        .coupon { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin-top: 16px; padding: 14px 16px; border-radius: 14px; background: var(--white, #fff); border: 1px dashed rgba(127,127,127,.5); }
        .coupon-label { font-weight: 600; }
        .coupon-code { direction: ltr; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 18px; font-weight: 700; letter-spacing: .04em; padding: 6px 12px; border-radius: 8px; background: rgba(127,127,127,.12); user-select: all; }
        .coupon-copy { border: 0; cursor: pointer; font-family: inherit; font-size: 14px; font-weight: 600; padding: 8px 16px; border-radius: 999px; background: #1F1E1D; color: #fff; }
        .hosting-note > .icon { font-size: 24px; margin-top: 2px; }
        @media (max-width: 575px) {
            .lesson-row { flex-wrap: wrap; gap: 8px 14px; padding: 16px; }
            .lesson-body { flex-basis: calc(100% - 50px); }
            .lesson-status { margin-inline-start: 50px; }
            .lesson-title { font-size: 17px; }
        }''')
    (ROOT / "site/service-single.html").write_text(clean(html))
    check_english("service-single.html", html)


build_service()
build_single()
