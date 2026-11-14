"""עמודי "עליי" ו"צור קשר / הרשמה" של Free AI – נבנים מתוך about.html ו-contact.html של האתר המשוכפל."""
import re
from pathlib import Path
from common import apply_common

ROOT = Path(__file__).resolve().parents[2]


def rep(html, pairs):
    for a, b in pairs:
        assert a in html, a
        html = html.replace(a, b, 1)
    return html


def sub1(pattern, repl, html):
    new, n = re.subn(pattern, lambda m: repl(m) if callable(repl) else repl, html, count=1, flags=re.S)
    assert n == 1, pattern
    return new


def faq(html, items):
    """מחליף את 4 השאלות של התבנית (לכולן אותה תשובה)."""
    olds = ["What’s the typical timeline from idea to v1?", "What do we need to start?",
            "Which models/stack do you use?", "Are model/API costs included in pricing?"]
    ans_old = "A clear problem statement, success metrics, access to sample data, and a stakeholder who can make decisions. We’ll run a kickoff workshop to align scope."
    html = rep(html, [
        ('<div class="heading-sub fw-semibold effectFade fadeUp">FAQs</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">שאלות נפוצות</div>'),
        ("Frequently Asked <br>Questions", "שאלות <br>ותשובות"),
    ])
    for (q, a), oq in zip(items, olds):
        html = rep(html, [(oq, q), (ans_old, a)])
    return html


SIGNUP_FORM = '''<form class="form-contact{extra} effectFade fadeUp" id="signup" data-signup>
                                <h4 class="heading fw-semibold">הרשמה חינם</h4>
                                <fieldset class="mb-21">
                                    <label class="fw-semibold text-body-3 mb-20" for="signup-name">שם מלא</label>
                                    <input type="text" id="signup-name" name="name" autocomplete="name" placeholder="השם שיופיע בתעודה" required>
                                </fieldset>
                                <fieldset class="mb-21">
                                    <label class="fw-semibold text-body-3 mb-20" for="signup-email">מייל</label>
                                    <input type="email" id="signup-email" name="email" autocomplete="email" dir="ltr" placeholder="name@example.com" required>
                                </fieldset>
                                <button type="submit" class="tf-btn w-100">שלחו לי קוד כניסה</button>
                                <p class="text-body-3 text-secondary mt-3 mb-0">בהרשמה אתם מסכימים ל<a href="terms.html" class="link-underline">תנאי השימוש</a> ול<a href="privacy.html" class="link-underline">מדיניות הפרטיות</a>.</p>
                            </form>'''

WHATSAPP = "https://wa.me/"

TOOLS = ["Claude", "Lovable", "n8n", "Claude Code", "ChatGPT", "Gemini", "Cursor", "Supabase"]

PAGE_CSS = '''
    <style>
        /* תיקוני RTL לעמוד */
        .section-hero .content-wrap .text { text-wrap: balance; }
        .form-contact input[dir="ltr"] { text-align: right; }
        .form-contact input[dir="ltr"]::placeholder { text-align: right; }
        .awards-item .skill-icon { font-size: 30px; color: var(--white); }
        .tool-wrap .free-ai-center { width: 204px; height: 70px; display: flex; align-items: center; justify-content: center;
            background: radial-gradient(circle at 50% 0, #3a3a3a, #272727); color: #fff; font-size: 28px; font-weight: 600; direction: ltr; }
        @media (max-width: 767px) { .tool-wrap .free-ai-center { width: 100px; height: 34px; font-size: 14px; } }
        .box-quotes .image img.quote-neutral { object-fit: cover; height: 100%; }
    </style>
</head>'''


def add_css(html):
    return html.replace("</head>", PAGE_CSS, 1)


# =====================================================================
# about.html – עליי
# =====================================================================
html = (ROOT / "aigocy-about/about.html").read_text()
html = apply_common(
    html,
    "about.html",
    "עליי – למה בניתי את Free AI",
    "הסיפור מאחורי Free AI: קורסי AI בעברית עולים אלפי שקלים, אז פתחתי את כל הידע – Claude, Lovable, סוכנים ו-n8n – בחינם, בעברית, צעד אחרי צעד.",
)
html = add_css(html)

# ---------- Hero ----------
html = rep(html, [
    ('<span class="title1 fw-semibold text-gradient-1">Aigocy Empowering</span>', '<span class="title1 fw-semibold text-gradient-1">למה בניתי את</span>'),
    ('<span class="fw-semibold text-gradient-1">Industries</span>', '<span class="fw-semibold text-gradient-1">Free AI</span>'),
    ("We build human-centered AI solutions that transform workflows, enhance decision-making, <br> and accelerate innovation across diverse global industries.",
     "קורסי AI בעברית עולים אלפי שקלים, ורוב האנשים פשוט מוותרים. <br> אז פתחתי את כל הידע לכולם – בחינם, בעברית, צעד אחרי צעד."),
])

# ---------- About (הסיפור) ----------
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">About Us</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הסיפור</div>'),
    ('<div class="heading-title text-gradient-2 effectFade fadeRotateX">Human-Centered AI, <br> Built for Production</div>',
     '<div class="heading-title text-gradient-2 effectFade fadeRotateX">היי, אני שי. <br> ככה התחיל Free AI</div>'),
    ("Available for worldwide project", "פתוח לכולם, מכל מקום"),
    ('<h5 class="title fw-semibold text-white">Based in <span class="text-brand">Montréal, Canada</span></h5>',
     '<h5 class="title fw-semibold text-white">לומדים ב<span class="text-brand">עברית, מאפס</span></h5>'),
    ('''<a href="contact.html" class="tf-btn">
                                    Start a Project
                                </a>''', '''<a href="contact.html#signup" class="tf-btn">
                                    הרשמה חינם
                                </a>'''),
    ('<h4 class="title fw-semibold effectFade fadeUp">Our Mission</h4>', '<h4 class="title fw-semibold effectFade fadeUp">המטרה</h4>'),
    ("Based in Montréal, Canada, we build human-centered AI for production. Our mission is to create intelligent systems that empower people and organizations. By uniting research, design, and engineering, we deliver scalable and reliable AI solutions—technology that’s practical, trustworthy, and designed to make a meaningful impact in the real world.",
     "ראיתי בעלי עסקים, פרילנסרים וסתם סקרנים שרוצים ללמוד AI – ונתקעים מול קורסים שעולים אלפי שקלים. "
     "רובם מוותרים. אז בניתי את Free AI: כל הידע – Claude, Lovable, סוכני AI, אוטומציות n8n והעלאה לאוויר – "
     "בחינם, בעברית פשוטה, צעד אחרי צעד. בלי מנוי, בלי כרטיס אשראי, ולתמיד."),
    # עד שתהיה תמונה אמיתית של שי – תמונה ניטרלית, לא פנים של מישהו אחר
    ('<img src="assets/images/section/quotes-1.jpg" alt="">', '<img src="assets/images/section/service-3.jpg" alt="" class="quote-neutral">'),
    ("Good AI feels obvious—because the hard work is hidden.", "ידע טוב לא צריך לעלות אלפי שקלים."),
    ('<div class="name text-body-3 fw-semibold">Ava Collins</div>', '<div class="name text-body-3 fw-semibold">שי</div>'),
    ("<div class=\"sub text-body-3\">Aigocy’s Design Lead</div>", '<div class="sub text-body-3">המייסד של Free AI</div>'),
])

# ---------- Partner → הכלים שלומדים ----------
html = rep(html, [('<p class="text-secondary text fw-semibold">Trusted by 100+ <br> top-tier brands</p>',
                   '<p class="text-secondary text fw-semibold">הכלים <br> שלומדים כאן</p>')])
html = sub1(r'(<div class="infiniteSlide infiniteSlide_partner" data-clone="5">).*?(</div>)',
            lambda m: m.group(1) + "".join(f'\n                                    <span class="tool-name">{t}</span>' for t in TOOLS) + "\n                                " + m.group(2),
            html)

# ---------- Core values → העקרונות ----------
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">Core Values</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">העקרונות</div>'),
    ('<div class="heading-title text-gradient-3 effectFade fadeRotateX">Guided by Principles</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">על מה Free AI בנוי</div>'),
    ('<h4 class="title fw-semibold">Innovation</h4>', '<h4 class="title fw-semibold">בחינם, באמת</h4>'),
    ("Innovation drives everything we do. We leverage emerging technologies, challenge conventions, and explore new possibilities to create solutions. Through insight, experimentation, and strategy, we craft transformative experiences that fuel growth, redefine standards, and create meaningful impact—ensuring every project shapes the future with purpose.",
     "כל השיעורים, הקבצים, הסקילים והתעודות פתוחים לכולם. בלי מנוי, בלי כרטיס אשראי ובלי \"שבוע ניסיון\". "
     "ההרשמה נדרשת רק כדי לשמור לכם את ההתקדמות ולהנפיק תעודה."),
    ('<h4 class="title fw-semibold">Creativity</h4>', '<h4 class="title fw-semibold">בעברית פשוטה</h4>'),
    ("Creativity is the core of our agency. We transform ideas into compelling experiences that inspire, engage, and resonate. By blending imagination with strategy, we craft innovative solutions that stand out in crowded markets. Every project is an opportunity to explore new perspectives, push boundaries, and deliver work that is both original and impactful, leaving a lasting impression.",
     "בלי מונחים מסובכים ובלי להניח שאתם כבר יודעים. כל מסלול מתחיל מאפס, וכל צעד מוסבר כאילו זו הפעם הראשונה."),
    ('<h4 class="title fw-semibold">Collaboration</h4>', '<h4 class="title fw-semibold">לומדים בעשייה</h4>'),
    ("At the heart of our work lies collaboration—bringing together diverse talents, perspectives, and expertise to achieve results. We foster open communication, encourage co-creation, and build strong partnerships with clients, ensuring every project reflects shared vision and purpose. By working together, we transform ideas into impactful solutions that drive innovation and lasting value.",
     "לא רק להבין, אלא לבנות. כל שיעור נגמר במשהו שעובד – אתר, אפליקציה, סוכן או אוטומציה – "
     "ומגיע עם קבצים ותבניות מוכנים להורדה."),
    ('<h4 class="title fw-semibold">Excellence</h4>', '<h4 class="title fw-semibold">עד שזה באוויר</h4>'),
    ("Excellence drives everything we do. From concept to execution, we pursue the highest standards in design, strategy, and delivery. Every detail matters, every decision is intentional, and every outcome reflects our commitment to quality. By continually refining our skills and processes, we ensure each project not only meets expectations but sets new benchmarks in creativity and performance.",
     "לא עוצרים בהדגמה. מלמדים גם איך לחבר דומיין ואחסון, כדי שמה שבניתם ירוץ 24/7 ויעבוד בשבילכם באמת."),
])

# ---------- Tools ----------
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">Tools</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הכלים</div>'),
    ('<div class="heading-title text-gradient-3 effectFade fadeRotateX">We work with <br> powerful AI tools</div>',
     '<div class="heading-title text-gradient-3 effectFade fadeRotateX">לומדים את <br> הכלים הכי חזקים</div>'),
    ("We design, build, and evaluate with a modern AI stack—LLMs, vector <br> search, orchestration, and observability—so your features are fast, <br> reliable, and secure.",
     "Claude, Lovable, n8n, Cursor ועוד – הכלים שבעלי עסקים <br> ופרילנסרים משתמשים בהם היום, בהסבר צעד אחרי צעד."),
    ('''<a href="contact.html" class="tf-btn effectFade fadeRotateX">
                    Get Started
                </a>''', '''<a href="service.html" class="tf-btn effectFade fadeRotateX">
                    לכל הקורסים
                </a>'''),
])

# הלוגו של Aigocy במרכז התרשים → Free AI
html = rep(html, [('''<div class="image-center flex-shrink">
                        <img src="assets/images/section/tool-center.svg" alt="">
                    </div>''', '''<div class="image-center flex-shrink free-ai-center">
                        <span>Free AI</span>
                    </div>''')])

# ---------- box-black: בלי צוות ובלי המלצות מומצאות ----------
html = sub1(r"\s*<!-- section-team -->.*?<!-- /section-team -->", "", html)
html = sub1(r"\s*<!-- section-testimonials -->.*?<!-- /section-testimonials -->", "", html)

# ---------- Statistic → מספרים אמיתיים ----------
html = rep(html, [
    ('<div class="heading-sub fw-semibold style-1 effectFade fadeUp">Statistic</div>', '<div class="heading-sub fw-semibold style-1 effectFade fadeUp">במספרים</div>'),
    ('<div class="heading-title text-white effectFade fadeRotateX">Human-centered <br> AI, built for <br> production</div>',
     '<div class="heading-title text-white effectFade fadeRotateX">כל הידע. <br> בלי המחיר. <br> לתמיד.</div>'),
    ("We shipped our first copilot in 7 weeks and cut support tickets by 31%. The eval dashboards made every decision obvious.",
     "קורסי AI בעברית עולים אלפי שקלים. כאן מקבלים את אותו ידע – מסלולים מלאים, קבצים ותעודה – בחינם."),
    ('<div class="title fw-semibold text-body-1">OUR GROWTH</div>', '<div class="title fw-semibold text-body-1">מחיר לכל הקורסים</div>'),
    ('<span class="number text-white fw-semibold">230</span>\n                                                <span class="prefix text-brand">K</span>',
     '<span class="prefix text-brand">₪</span>\n                                                <span class="number text-white fw-semibold">0</span>'),
    ('<div class="title fw-semibold text-body-1">UPTIME FOR KEY FLOWS</div>', '<div class="title fw-semibold text-body-1">מסלולי לימוד</div>'),
    ('<span class="number text-white fw-semibold">95</span>\n                                                <span class="prefix text-brand">%</span>',
     '<span class="number text-white fw-semibold">5</span>\n                                                <span class="prefix text-brand">+</span>'),
    ('<div class="title fw-semibold text-body-1">ON TIME DELIVERY</div>', '<div class="title fw-semibold text-body-1">בעברית</div>'),
    ('<span class="number text-white fw-semibold">99</span>\n                                                <span class="prefix text-brand">%</span>',
     '<span class="number text-white fw-semibold">100</span>\n                                                <span class="prefix text-brand">%</span>'),
])

# ---------- Awards → מה לומדים כאן (המסלולים) ----------
tracks = [
    ("book-open-solid", "Claude מאפס", "מהשאלה הראשונה ועד עבודה יומיומית עם Claude", "01"),
    ("desktop-solid", "בונים אפליקציה עם Lovable", "מרעיון לאפליקציה אמיתית – בלי לכתוב קוד", "02"),
    ("robot-solid", "סוכני AI", "עוזרים שעובדים בשבילכם, גם כשאתם לא", "03"),
    ("plug-solid", "אוטומציות עם n8n", "תהליכים שרצים לבד וחוסכים שעות כל שבוע", "04"),
    ("global", "מעלים לאוויר", "דומיין, אחסון ושרת שעובד 24/7", "05"),
]
rows = []
for i, (icon, title, text, num) in enumerate(tracks):
    delay = f' data-delay="0.{i}"' if i else ""
    rows.append(f'''                        <a href="service.html" class="awards-item effectFade fadeUp"{delay}>
                            <div class="image">
                                <i class="icon icon-{icon} skill-icon"></i>
                            </div>
                            <div class="title text-body-1 text-white">{title}</div>
                            <div class="text text-body-1 text-white">{text}</div>
                            <div class="year text-body-1 text-neutral-400">{num}</div>
                        </a>''')
html = sub1(r'(<div class="d-grid gap-16">).*?(\n                    </div>\n                </div>\n            </div>\n            <!-- /section-awards -->)',
            lambda m: m.group(1) + "\n" + "\n".join(rows) + m.group(2), html)
html = rep(html, [('<div class="heading-sub fw-semibold style-1 mb-0 effectFade fadeUp">Awards</div>',
                   '<div class="heading-sub fw-semibold style-1 mb-0 effectFade fadeUp">מה לומדים כאן</div>')])

# ---------- FAQ ----------
html = faq(html, [
    ("מי עומד מאחורי Free AI?", "אני, שי. בניתי את Free AI כי ראיתי כמה אנשים רוצים ללמוד AI ומוותרים בגלל המחיר. כל השיעורים כאן נבנים כדי שתוכלו ללמוד לבד, בקצב שלכם."),
    ("למה הכל בחינם?", "כי ידע כזה לא צריך לעלות אלפי שקלים. המטרה היא שכל מי שרוצה – בעל עסק, פרילנסר או סקרן – יוכל ללמוד ולבנות בעצמו."),
    ("איך האתר מרוויח אם הכל חינם?", "בשיעורים שבהם צריך אחסון אני ממליץ על חברת אחסון שאני עובד איתה, ומקבל עמלה אם נרשמים דרכי. זה לא עולה לכם כלום, ותמיד כתוב בגלוי כשמדובר בהמלצה כזו."),
    ("למי זה מתאים?", "לבעלי עסקים שרוצים לחסוך זמן, לפרילנסרים שרוצים לבנות ללקוחות, ולכל מי שסקרן להבין AI ולהשתמש בו ביומיום. לא צריך ידע קודם."),
])

# ---------- Contact → הרשמה ----------
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">Contact</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הרשמה</div>'),
    ("Let’s Build <br> Intelligent Things", "מתחילים מהשיעור <br> הראשון"),
    ('<div class="title fw-semibold mb-2">E-mail address</div>\n                                            <div class="text">hello@youraiagency.com</div>',
     '<div class="title fw-semibold mb-2">פחות מדקה</div>\n                                            <div class="text">שם, מייל, וקוד כניסה מגיע אליכם</div>'),
    ('<i class="icon icon-envelope-solid"></i>', '<i class="icon icon-bolt-solid"></i>'),
    ('''<div class="contact-item effectFade fadeRotateX" data-delay="0.1">
                                        <i class="icon icon-headset-solid"></i>
                                        <div class="content">
                                            <div class="title fw-semibold mb-2">Phone number</div>
                                            <div class="text">+1 (647) 555 0172</div>
                                        </div>
                                    </div>''', f'''<a href="{WHATSAPP}" target="_blank" rel="noopener" class="contact-item effectFade fadeRotateX" data-delay="0.1">
                                        <i class="icon icon-comments-solid"></i>
                                        <div class="content">
                                            <div class="title fw-semibold mb-2">שאלה? כתבו לי בוואטסאפ</div>
                                            <div class="text">פותחים שיחה בלחיצה</div>
                                        </div>
                                    </a>'''),
])
html = sub1(r'<form class="form-contact effectFade fadeUp">.*?</form>', SIGNUP_FORM.format(extra=""), html)

(ROOT / "site/about.html").write_text(html)


# =====================================================================
# contact.html – צור קשר + הרשמה
# =====================================================================
html = (ROOT / "aigocy-about/contact.html").read_text()
html = apply_common(
    html,
    "contact.html",
    "צור קשר והרשמה – Free AI",
    "נרשמים בחינם ל-Free AI ומתחילים ללמוד AI בעברית. שאלה? כתבו לנו בוואטסאפ.",
)
html = add_css(html)

# ---------- Hero ----------
html = rep(html, [
    ('<span class="title1 fw-semibold text-gradient-1">Let’s Build Intelligent</span>', '<span class="title1 fw-semibold text-gradient-1">נרשמים פעם אחת.</span>'),
    ('<span class="fw-semibold text-gradient-1">Things</span>', '<span class="fw-semibold text-gradient-1">לומדים לתמיד</span>'),
    ("Reach out to our team today and let’s collaborate to turn your ideas into innovative <br> solutions that truly inspire",
     "הרשמה חינם בפחות מדקה – בלי סיסמה ובלי כרטיס אשראי. <br> יש שאלה? כתבו לנו בוואטסאפ."),
])

# ---------- שלוש קופסאות ----------
html = sub1(r'<div class="row mb-60">.*?\n                    </div>\n                    <div class="row">', f'''<div class="row mb-60">
                        <div class="col-md-4 md-mb-24">
                            <div class="box-contact-item text-center effectFade fadeUp">
                                <i class="icon icon-envelope-solid"></i>
                                <h6 class="title fw-semibold">קוד כניסה למייל</h6>
                                <p class="text">
                                    בלי סיסמה – מקבלים קוד ונכנסים
                                </p>
                            </div>
                        </div>
                        <div class="col-md-4 md-mb-24">
                            <div class="box-contact-item text-center effectFade fadeUp" data-delay="0.1">
                                <i class="icon icon-comments-solid"></i>
                                <h6 class="title fw-semibold">שאלה? כתבו לנו בוואטסאפ</h6>
                                <a href="{WHATSAPP}" target="_blank" rel="noopener" class="text" data-whatsapp>
                                    פתיחת שיחה
                                </a>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="box-contact-item text-center effectFade fadeUp" data-delay="0.2">
                                <i class="icon icon-check-solid"></i>
                                <h6 class="title fw-semibold">בחינם, לתמיד</h6>
                                <p class="text">
                                    בלי כרטיס אשראי ובלי מנוי
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="row">''', html)

# ---------- עמודה שמאל (בעברית: ימין) ----------
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">Contact</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הרשמה</div>'),
    ("Let’s Build <br> Intelligent Things", "מתחילים מהשיעור <br> הראשון"),
    ("combining creativity, technology, and strategy to craft solutions that think, adapt, and inspire. Connect with us to turn visionary ideas into meaningful, data-driven realities.",
     "משאירים שם ומייל, מקבלים קוד כניסה, ומתחילים. ההרשמה שומרת לכם את ההתקדמות, פותחת את הסרטונים וההורדות, ומאפשרת לקבל תעודה בסוף כל מסלול."),
])
html = sub1(r'<div class="tf-social-1 gap-24 effectFade fadeRotateX">.*?\n                                </div>\n                            </div>\n                        </div>',
            f'''<div class="tf-social-1 gap-24 effectFade fadeRotateX">
                                    <a href="{WHATSAPP}" target="_blank" rel="noopener" class="text-body-1 fw-semibold" data-whatsapp>
                                        וואטסאפ
                                        <div class="social-item">
                                            <i class="icon icon-comments-solid"></i>
                                        </div>
                                    </a>
                                    <a href="service.html" class="text-body-1 fw-semibold">
                                        קורסים
                                        <div class="social-item">
                                            <i class="icon icon-arrow-top-right"></i>
                                        </div>
                                    </a>
                                    <a href="work.html" class="text-body-1 fw-semibold">
                                        סקילים
                                        <div class="social-item">
                                            <i class="icon icon-arrow-top-right"></i>
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>''', html)

html = sub1(r'<form class="form-contact m-0 effectFade fadeUp">.*?</form>', SIGNUP_FORM.format(extra=" m-0"), html)

# ---------- בלי מפה ----------
html = sub1(r"\s*<!-- map -->.*?<!-- /map -->", "", html)

# ---------- FAQ ----------
html = faq(html, [
    ("זה באמת בחינם?", "כן. כל השיעורים, הקבצים, הסקילים והתעודות – בחינם, בלי כרטיס אשראי ובלי מנוי."),
    ("למה צריך להירשם?", "ההרשמה שומרת לכם את ההתקדמות, פותחת את הסרטונים וההורדות, ומאפשרת לקבל תעודה בסוף מסלול. היא לוקחת פחות מדקה."),
    ("לא קיבלתי קוד, מה עושים?", "חכו דקה ובדקו גם בתיקיית הספאם או קידומי מכירות. אם הקוד עדיין לא הגיע, בקשו קוד חדש או כתבו לנו בוואטסאפ."),
    ("מה תעשו עם המייל שלי?", "נשתמש בו כדי שתוכלו להיכנס לאתר ולשמור את ההתקדמות שלכם. לא נמכור אותו ולא נעביר אותו לאף אחד. כל הפרטים במדיניות הפרטיות."),
])

(ROOT / "site/contact.html").write_text(html)

for name in ("about.html", "contact.html"):
    out = (ROOT / "site" / name).read_text()
    left = re.findall(r">\s*([A-Za-z][A-Za-z ,’'&\-]{6,})\s*<", out)
    print(name, "done; leftover English:", [x for x in left if x.strip() not in ("Free AI", "Claude Code")][:20])
