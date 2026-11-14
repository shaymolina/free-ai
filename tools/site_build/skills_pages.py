"""עמוד ספריית הסקילים (work.html) ועמוד סקיל (work-single.html) – נבנים מתוך האתר המשוכפל."""
import re
from pathlib import Path
from common import apply_common, replace_section

ROOT = Path(__file__).resolve().parents[2]

SKILLS = [
    {
        "slug": "website-security",
        "title": "בדיקת אבטחה <br> לאתר ולאפליקציה",
        "name": "בדיקת אבטחה לאתר ולאפליקציה",
        "cat": "אבטחה",
        "desc": "בודק 34 פרצות אבטחה באתר או באפליקציה שבניתם עם AI ונותן דוח אדום / כתום / ירוק בעברית פשוטה.",
        "prompt": "תבדוק לי את האבטחה של האתר",
        "result": "רשימה של כל החורים ומה לתקן קודם",
        "img": "featured-works-1.jpg",
        "page": "work-single.html",
        "src": "https://github.com/openforge-lab/website-security",
    },
    {
        "slug": "site-speed",
        "title": "בדיקת מהירות <br> לאתר",
        "name": "בדיקת מהירות לאתר",
        "cat": "ביצועים",
        "desc": "בודק 69 דברים שמאטים את האתר, כולל מיקום השרת מול הגולשים בישראל, ומדרג תיקונים לפי כמה שניות כל אחד חוסך.",
        "prompt": "האתר שלי איטי, תבדוק",
        "result": "דוח עם מה לתקן קודם ופרומפט מוכן לכל תיקון",
        "img": "featured-works-2.jpg",
        "page": None,
        "src": "https://github.com/openforge-lab/site-speed",
    },
]
CATEGORIES = [("אבטחה", True), ("ביצועים", True), ("כתיבה", False), ("שיווק", False), ("עסק", False), ("קוד", False)]


def zip_url(src):
    return src + "/archive/refs/heads/main.zip"


def sub1(html, pat, repl):
    new, n = re.subn(pat, lambda m: repl, html, count=1, flags=re.S)
    assert n == 1, pat
    return new


def rep(html, pairs):
    for a, b in pairs:
        assert a in html, a
        html = html.replace(a, b, 1)
    return html


def hero(html, line1, line2, text):
    html = sub1(html, r'<span class="title1 fw-semibold text-gradient-1">[^<]*</span>',
                f'<span class="title1 fw-semibold text-gradient-1">{line1}</span>')
    html = re.sub(r'(<div class="title2 d-flex gap-20 justify-content-center flex-wrap">\s*<span class="fw-semibold text-gradient-1">)[^<]*(</span>)',
                  lambda m: m.group(1) + line2 + m.group(2), html, count=1)
    html = re.sub(r'(<p class="text effectFade fadeUp">\s*).*?(\s*</p>)', lambda m: m.group(1) + text + m.group(2), html, count=1, flags=re.S)
    return html


def work_item(i, s, total, first=False):
    dots = "\n".join(
        f'                                    <span{" class=\"active\"" if k == i else ""}></span>' for k in range(total))
    if s["page"]:
        href, label = s["page"], "לפרטי הסקיל"
    else:
        href, label = "contact.html#signup", "הורדה חינם"
    extra = " effectFade fadeUp no-div" if first else ""
    return f'''                    <div class="skill-entry" data-cat="{s['cat']}" data-search="{s['name']} {s['cat']} {s['desc']}">
                        <div class="featured-works-item {extra}">
                            <div class="image main-mouse-hover">
                                <img src="assets/images/section/{s['img']}" alt="{s['name']}">
                                <a href="{href}" class="tf-mouse view-project h6">
                                    {label}
                                    <i class="icon icon-arrow-top-right"></i>
                                </a>
                            </div>
                            <div class="content">
                                <div class="pagi-dot">
{dots}
                                </div>
                                <div class="bot">
                                    <h4 class="heading fw-semibold">{s['title']}</h4>
                                    <div class="grid-text">
                                        <div class="item">
                                            <div class="title text-secondary">מה הוא עושה</div>
                                            <div class="text-body-3 fw-semibold">{s['desc']}</div>
                                        </div>
                                        <div class="item">
                                            <div class="title text-secondary">כותבים ל-Claude</div>
                                            <div class="fw-semibold text-body-3">"{s['prompt']}"</div>
                                        </div>
                                        <div class="item">
                                            <div class="title text-secondary">קטגוריה</div>
                                            <div class="fw-semibold text-body-3">{s['cat']}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>'''


def signup_section(html, sub, title):
    html = rep(html, [
        ('<div class="heading-sub fw-semibold effectFade fadeUp">Contact</div>', f'<div class="heading-sub fw-semibold effectFade fadeUp">{sub}</div>'),
        ("Let’s Build <br> Intelligent Things", title),
        ('<div class="title fw-semibold mb-2">E-mail address</div>\n                                            <div class="text">hello@youraiagency.com</div>',
         '<div class="title fw-semibold mb-2">פחות מדקה</div>\n                                            <div class="text">הרשמה עם Google או קוד למייל</div>'),
        ('<i class="icon icon-envelope-solid"></i>', '<i class="icon icon-bolt-solid"></i>'),
        ('<div class="title fw-semibold mb-2">Phone number</div>\n                                            <div class="text">+1 (647) 555 0172</div>',
         '<div class="title fw-semibold mb-2">בחינם, לתמיד</div>\n                                            <div class="text">בלי כרטיס אשראי ובלי מנוי</div>'),
        ('<i class="icon icon-headset-solid"></i>', '<i class="icon icon-check-solid"></i>'),
    ])
    return sub1(html, r'<form class="form-contact effectFade fadeUp">.*?</form>', '''<form class="form-contact effectFade fadeUp" id="signup" data-signup>
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
                            </form>''')


def add_style(html, css):
    return html.replace("</head>", f"    <style>\n{css}\n    </style>\n</head>", 1)


def check_english(name, html):
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", html.split("<body", 1)[1], flags=re.S)
    left = re.findall(r">\s*([^<>]*[A-Za-z]{3,}[^<>]*?)\s*<", body)
    allowed = ("Free AI", "Claude", "GitHub", "Google", "Lovable", "Bolt", "Base44", "ZIP")
    bad = [x for x in left if re.sub("|".join(allowed), "", x).strip() and re.search(r"[A-Za-z]{3,}", re.sub("|".join(allowed), "", x))]
    print(f"{name} done; leftover English:", bad[:20])


# =====================================================================
# work.html – ספריית הסקילים
# =====================================================================
html = (ROOT / "aigocy-about/work.html").read_text()
html = apply_common(html, "work.html", "ספריית סקילים ל-Claude בעברית – Free AI",
                    "סקילים מוכנים ל-Claude בעברית, להורדה בחינם: בדיקת אבטחה לאתר, בדיקת מהירות ועוד. כל סקיל עם דוגמה, קוד מקור ומדריך התקנה.")

html = hero(html, "ספריית סקילים", "ל-Claude",
            "סקילים מוכנים בעברית שמלמדים את Claude לעשות עבודה של מומחה. <br> מורידים בחינם, מתקינים בדקה – ומשתמשים מיד.")

# ---------- הסקילים ----------
cat_tags = ['                            <button type="button" class="tags-item fw-semibold active" data-filter="all">הכל</button>']
for c, live in CATEGORIES:
    soon = "" if live else ' <span class="soon">בקרוב</span>'
    cat_tags.append(f'                            <button type="button" class="tags-item fw-semibold" data-filter="{c}">{c}{soon}</button>')
items = "\n".join(work_item(i, s, len(SKILLS), i == 0) for i, s in enumerate(SKILLS))
html = replace_section(html, "section-featured-works", f'''<!-- section-featured-works -->
        <div id="works" class="section-featured-works flat-spacing">
            <div class="container">
                <div class="heading-section mb-0">
                    <div class="heading-sub fw-semibold mx-auto effectFade fadeUp">הסקילים</div>
                </div>
                <div class="skills-tools effectFade fadeUp">
                    <input type="search" class="skills-search" placeholder="חיפוש סקיל – למשל: אבטחה, מהירות" aria-label="חיפוש סקיל">
                    <div class="list-tags skills-filter">
{chr(10).join(cat_tags)}
                    </div>
                </div>
                <p class="skills-empty text-secondary text-center" hidden>עוד אין סקילים בקטגוריה הזו – הם בדרך.</p>
                <div class="featured-works-list position-relative">
{items}
                </div>
            </div>
        </div>
        <!-- /section-featured-works -->''')

# ---------- Why delay → איך מתקינים ----------
steps = [
    ("נרשמים ומורידים את הסקיל", "קובץ ZIP אחד"),
    ("מעלים את הקובץ ל-Claude", "בהגדרות, תחת סקילים"),
    ("מפעילים את הסקיל", "לחיצה אחת"),
    ("כותבים ל-Claude בקשה רגילה", "הסקיל עובד לבד"),
]
rows = []
for i, (title, note) in enumerate(steps, 1):
    rows.append(f'''                        <div class="delay-item">
                            <div class="left">
                                <h6 class="effectFade fadeUp title fw-semibold mb-12">{title}</h6>
                                <h6 class="effectFade fadeUp title fw-semibold">/ 0{i}</h6>
                            </div>
                            <div class="right">
                                <div class="delay-progress mb-12">
                                    <div class="progress-line" data-progress="{i * 25}"></div>
                                    <h4 class="number-progress fw-semibold text-white">{i}/4</h4>
                                </div>
                                <div class="text text-secondary text-end">/ {note}</div>
                            </div>
                        </div>''')
html = re.sub(r'(<div class="delay-wrap">).*?(\n                    </div>\n                </div>\n            </div>\n            <!-- /section-delay -->)',
              lambda m: m.group(1) + "\n" + "\n".join(rows) + '''
                    </div>
                    <div class="d-flex justify-content-center mt-5">
                        <a href="blog-single.html" class="tf-btn-2 effectFade fadeUp">המדריך המלא: איך מתקינים סקיל</a>''' + m.group(2),
              html, count=1, flags=re.S)
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">Why Delay Hurts</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">איך מתקינים</div>'),
    ('The longer you wait, the harder <br> it is to catch up.', 'ארבעה צעדים, <br> פחות מדקה.'),
])

# ---------- Pricing → ₪0 ----------
html = re.sub(r'(<div class="heading-sub fw-semibold effectFade fadeUp">)Pricing Plans(</div>\s*<div class="heading-title text-gradient-3 gap-8 d-grid effectFade fadeRotateX">).*?(\n                        </div>\n                    </div>\n                    <div class="row">)',
              lambda m: m.group(1) + "מחיר" + m.group(2) + "\n                            <span>כל הסקילים.</span>\n                            <span>₪0. לתמיד.</span>" + m.group(3),
              html, count=1, flags=re.S)
html = rep(html, [
    ('<i class="icon icon-user-friends-solid fs-24"></i>\n                                        <div class="fw-semibold text">Starter Plan</div>',
     '<i class="icon icon-user-friends-solid fs-24"></i>\n                                        <div class="fw-semibold text">בלי הרשמה</div>'),
    ('<div class="fw-semibold text-secondary">For startups</div>', '<div class="fw-semibold text-secondary">לכל גולש</div>'),
    ('<div class="price-number fw-bold" data-month="1000" data-year="9900">$9,900</div>\n                                        <h6 class="price-per">/ year</h6>',
     '<div class="price-number fw-bold">₪0</div>\n                                        <h6 class="price-per">לצפייה</h6>'),
    ('''<a href="contact.html" class="tf-btn">
                                        Get Started
                                    </a>''', '''<a href="#works" class="tf-btn">
                                        לסקילים
                                    </a>'''),
    ('<div class="title fw-semibold mb-4">What’s included</div>', '<div class="title fw-semibold mb-4">מה רואים</div>'),
    ("Prove value in two weeks with a clickable UX, tech spike, and a clear go/no-go roadmap.", "את כל הסקילים, מה כל אחד עושה ואיך משתמשים בו – פתוח לכולם."),
    ("Discovery workshop", "מה כל סקיל עושה"),
    ("Opportunity brief", "דוגמה: מה כותבים ומה מקבלים"),
    ("Clickable UX", "קוד המקור ב-GitHub"),
    ("1 data source & 1 integration", "מדריך התקנה בבלוג"),
    ('<i class="icon icon-building fs-24"></i>\n                                        <div class="fw-semibold text">Enterprise Plan</div>',
     '<i class="icon icon-building fs-24"></i>\n                                        <div class="fw-semibold text">עם הרשמה חינם</div>'),
    ('<div class="fw-semibold text-neutral-400">For organisations</div>', '<div class="fw-semibold text-neutral-400">פחות מדקה</div>'),
    ('<div class="price-number fw-bold" data-month="1700" data-year="19900">$19,900</div>\n                                        <h6 class="price-per">/ year</h6>',
     '<div class="price-number fw-bold">₪0</div>\n                                        <h6 class="price-per">לתמיד</h6>'),
    ('''<a href="contact.html" class="tf-btn">
                                        Get Started
                                    </a>''', '''<a href="contact.html#signup" class="tf-btn">
                                        הרשמה חינם
                                    </a>'''),
    ('<div class="title fw-semibold mb-4">What’s included</div>', '<div class="title fw-semibold mb-4">מה מקבלים</div>'),
    ("Compliance-ready delivery for complex orgs—multi-env releases, canaries, and change management.", "הורדה של כל סקיל בלחיצה, וגישה לכל הקורסים באתר."),
    ("Everything in Starter", "כל מה שבלי הרשמה"),
    ("CI/CD, tracing, alerts, guardrails", "הורדה של כל הסקילים"),
    ("Full eval dashboard", "סקילים חדשים ברגע שעולים"),
    ("3 data source & 3 integration", "עזרה בוואטסאפ"),
])

# ---------- FAQ ----------
faqs = [
    ("מה זה סקיל?", "סקיל הוא חבילת הוראות ש-Claude טוען כשצריך אותה. הוא מלמד את Claude לעשות משימה מסוימת כמו מומחה – למשל לבדוק אבטחה של אתר – בלי שתצטרכו לכתוב פרומפט ארוך כל פעם."),
    ("איך מתקינים סקיל?", "מורידים קובץ ZIP, מעלים אותו ל-Claude בהגדרות ומפעילים. <a href=\"blog-single.html\" class=\"link-underline\">במדריך המלא</a> יש הסבר צעד אחרי צעד."),
    ("זה בטוח להוריד?", "כל סקיל מגיע עם קישור לקוד המקור ב-GitHub, כך שאפשר לראות בדיוק מה יש בו לפני שמתקינים."),
    ("למה צריך להירשם כדי להוריד?", "ההרשמה חינם ולוקחת פחות מדקה. היא פותחת את כל ההורדות והקורסים באתר."),
]
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">FAQs</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">שאלות נפוצות</div>'),
    ("Frequently Asked <br>Questions", "שאלות על <br>סקילים"),
])
olds = ["What’s the typical timeline from idea to v1?", "What do we need to start?", "Which models/stack do you use?", "Are model/API costs included in pricing?"]
ans_old = "A clear problem statement, success metrics, access to sample data, and a stakeholder who can make decisions. We’ll run a kickoff workshop to align scope."
for (q, a), oq in zip(faqs, olds):
    html = rep(html, [(oq, q), (ans_old, a)])

# ---------- Contact → הרשמה ----------
html = signup_section(html, "הרשמה", "נרשמים חינם <br> ומורידים")

html = add_style(html, """        /* RTL: פס ההתקדמות גדל מימין, המספר בצד ימין */
        .delay-item .delay-progress .progress-line { right: 0; left: auto; }
        .delay-item .delay-progress .number-progress { right: 30px; left: auto; }
        /* חיפוש וקטגוריות */
        .skills-tools { display: flex; flex-direction: column; align-items: center; gap: 20px; margin: 40px auto 8px; max-width: 760px; }
        .skills-search { width: 100%; max-width: 480px; height: 56px; border-radius: 999px; padding: 0 24px; border: 1px solid var(--neutral-200); background: var(--white); }
        .skills-filter { justify-content: center; }
        .skills-filter .tags-item { display: flex; align-items: center; padding: 7px 15px; border-radius: 99px; cursor: pointer;
            background: var(--white); color: var(--neutral-700, #3f3f46); border: 1px solid var(--neutral-200); }
        .skills-filter .tags-item:hover { color: var(--brand); }
        .skills-filter .tags-item.active { background: #18181B; border-color: #18181B; color: var(--white); }
        .skills-filter .soon { font-size: 12px; opacity: .6; margin-inline-start: 4px; }
        .skills-empty { margin-top: 40px; }
        .skill-entry[hidden] { display: none !important; }""")

html = html.replace("</body>", """<script>
(function () {
    var input = document.querySelector('.skills-search');
    var btns = document.querySelectorAll('.skills-filter [data-filter]');
    var items = document.querySelectorAll('.skill-entry');
    var empty = document.querySelector('.skills-empty');
    var cat = 'all';
    function run() {
        var q = (input.value || '').trim();
        var shown = 0;
        items.forEach(function (el) {
            var ok = (cat === 'all' || el.dataset.cat === cat) && (!q || el.dataset.search.indexOf(q) !== -1);
            el.hidden = !ok;
            if (ok) shown++;
        });
        empty.hidden = shown > 0;
        if (window.ScrollTrigger) ScrollTrigger.refresh();
    }
    btns.forEach(function (b) {
        b.addEventListener('click', function () {
            btns.forEach(function (x) { x.classList.remove('active'); });
            b.classList.add('active');
            cat = b.dataset.filter;
            run();
        });
    });
    input.addEventListener('input', run);
})();
</script>
</body>""", 1)

(ROOT / "site/work.html").write_text(html)
check_english("work.html", html)

# =====================================================================
# work-single.html – בדיקת אבטחה לאתר ולאפליקציה
# =====================================================================
s = SKILLS[0]
html = (ROOT / "aigocy-about/work-single.html").read_text()
html = apply_common(html, "work.html", "בדיקת אבטחה לאתר ולאפליקציה – סקיל ל-Claude | Free AI",
                    "סקיל חינמי ל-Claude שבודק 34 פרצות אבטחה באתר או באפליקציה שבניתם עם AI ונותן דוח אדום / כתום / ירוק בעברית.")
html = hero(html, "בדיקת אבטחה", "לאתר ולאפליקציה",
            "סקיל ל-Claude שבודק 34 פרצות אבטחה באתר או באפליקציה שבניתם עם AI, <br> ונותן דוח אדום / כתום / ירוק בעברית פשוטה.")

detail = f'''<!-- section-work-single -->
        <div id="works" class="section-work-single flat-spacing pt-0">
            <div class="container">
                <div class="row mb-32">
                    <div class="col-12">
                        <div class="wrap-image mb-60 effectFade fadeZoom">
                            <img src="assets/images/section/work-single-1.jpg" alt="">
                        </div>
                        <h2 class="heading fw-semibold mb-32 effectFade fadeUp">מה הסקיל עושה</h2>
                        <p class="text-secondary effectFade fadeUp">
                            בניתם אתר או אפליקציה עם Lovable, Bolt, Base44 או Claude Code? הכלים האלה בונים מהר, אבל לא תמיד סוגרים את כל הדלתות.
                            הסקיל הזה מלמד את Claude לעבור על 34 פרצות אבטחה נפוצות – ולהסביר כל בעיה בעברית פשוטה, בלי מונחים טכניים.
                            <br><br>
                            בסוף מקבלים דוח בצבעים: אדום – לתקן עכשיו, כתום – לתקן בקרוב, ירוק – תקין. כך יודעים בדיוק מה לתקן קודם.
                        </p>
                    </div>
                </div>
                <div class="row mb-60">
                    <div class="col-md-8 md-mb-24">
                        <div class="text-body-1 fw-semibold text-secondary mb-15 effectFade fadeUp">
                            מתאים לאתרים שנבנו עם
                        </div>
                        <div class="list-tags effectFade fadeUp">
                            <span class="tags-item fw-semibold">Lovable</span>
                            <span class="tags-item fw-semibold">Bolt</span>
                            <span class="tags-item fw-semibold">Base44</span>
                            <span class="tags-item fw-semibold">Claude Code</span>
                            <span class="tags-item fw-semibold">ועוד</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-body-1 fw-semibold text-secondary mb-15 effectFade fadeUp" data-delay="0.1">
                            קטגוריה
                        </div>
                        <div class="list-tags effectFade fadeUp" data-delay="0.1">
                            <a href="work.html" class="tags-item fw-semibold">{s['cat']}</a>
                        </div>
                    </div>
                </div>
                <div class="row mb-60">
                    <div class="col-12">
                        <h2 class="heading fw-semibold mb-20 effectFade fadeUp">דוגמה לשימוש</h2>
                        <div class="skill-example effectFade fadeUp">
                            <div class="example-box">
                                <div class="text-body-1 fw-semibold text-secondary mb-12">כותבים ל-Claude</div>
                                <h5 class="fw-semibold">"{s['prompt']}"</h5>
                            </div>
                            <i class="icon icon-arrow-top-right example-arrow"></i>
                            <div class="example-box dark">
                                <div class="text-body-1 fw-semibold text-neutral-400 mb-12">מקבלים</div>
                                <h5 class="fw-semibold text-white">רשימה של כל החורים באתר, מסודרת לפי דחיפות – ומה לתקן קודם.</h5>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mb-60">
                    <div class="col-12">
                        <div class="wrap-image effectFade fadeZoom">
                            <img src="assets/images/section/work-single-2.jpg" alt="">
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <h2 class="heading fw-semibold mb-20 effectFade fadeUp">הורדה והתקנה</h2>
                        <p class="text-secondary effectFade fadeUp">
                            הסקיל חינמי. נרשמים, מורידים קובץ ZIP ומעלים אותו ל-Claude – כל התהליך לוקח פחות מדקה.
                            לא בטוחים איך? <a href="blog-single.html" class="link-underline">המדריך "איך מתקינים סקיל"</a> מסביר צעד אחרי צעד.
                            רוצים לראות מה יש בפנים לפני שמתקינים? כל הקוד פתוח ב-GitHub.
                        </p>
                        <div class="d-flex gap-16 flex-wrap mt-4 effectFade fadeUp">
                            <a href="contact.html#signup" class="tf-btn" data-download="{zip_url(s['src'])}">
                                הורדה חינם
                            </a>
                            <a href="{s['src']}" class="tf-btn-2" target="_blank" rel="noopener">
                                קוד המקור ב-GitHub
                            </a>
                            <a href="blog-single.html" class="tf-btn-2">
                                איך מתקינים סקיל
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- /section-work-single -->'''
html = replace_section(html, "section-work-single", detail)

# המלצות מומצאות – מסירים את כל הקופסה השחורה
html = sub1(html, r'\s*<div class="box-black">\s*<div class="light-box"></div>.*?<!-- /section-testimonials -->\s*</div>', "")

# ---------- Next project → סקיל נוסף ----------
o = SKILLS[1]
html = rep(html, [
    ('<div class="heading-sub fw-semibold effectFade fadeUp">Project</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">עוד סקיל</div>'),
    ('<div class="heading-title text-gradient-3 effectFade fadeRotateX">Next Project</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">גם זה בחינם</div>'),
    ('<img src="assets/images/section/featured-works-3.jpg" alt="">', f'<img src="assets/images/section/{o["img"]}" alt="{o["name"]}">'),
    ('<a href="work-single.html" class="tf-mouse view-project h6">\n                                    View Project',
     '<a href="contact.html#signup" class="tf-mouse view-project h6">\n                                    הורדה חינם'),
    ('<span></span>\n                                    <span></span>\n                                    <span class="active"></span>\n                                    <span></span>',
     '<span></span>\n                                    <span class="active"></span>'),
    ('<h4 class="heading fw-semibold">Clinical Note <br> Summarizer</h4>', f'<h4 class="heading fw-semibold">{o["title"]}</h4>'),
    ('<div class="title text-secondary">DESCRIPTION</div>', '<div class="title text-secondary">מה הוא עושה</div>'),
    ("Clinic-lobby assistant answering pre-visit questions; decreased front-desk calls by 28%.", o["desc"]),
    ('<div class="title text-secondary">DELIVERABLES</div>\n                                            <div class="fw-semibold">PHI-safe RAG, HIPAA-aligned workflows</div>',
     f'<div class="title text-secondary">כותבים ל-Claude</div>\n                                            <div class="fw-semibold text-body-3">"{o["prompt"]}"</div>'),
    ('<div class="title text-secondary">INDUSTRY</div>\n                                            <div class="fw-semibold">Healthcare</div>',
     f'<div class="title text-secondary">קטגוריה</div>\n                                            <div class="fw-semibold text-body-3">{o["cat"]}</div>'),
])
html = html.replace('''                </div>
            </div>
        </div>
        <!-- /section-featured-works -->''', '''                </div>
                <div class="d-flex justify-content-center mt-5">
                    <a href="work.html" class="tf-btn-2 effectFade fadeUp">לכל הסקילים</a>
                </div>
            </div>
        </div>
        <!-- /section-featured-works -->''', 1)

html = add_style(html, """        .list-tags span.tags-item { display: flex; align-items: center; padding: 7px 15px; border-radius: 99px;
            color: var(--neutral-300); background: var(--neutral-700); border: 1px solid var(--neutral-600); }
        .skill-example { display: flex; align-items: center; gap: 24px; margin-top: 12px; }
        .skill-example .example-box { flex: 1; padding: 32px; border-radius: 24px; background: var(--neutral-100); }
        .skill-example .example-box.dark { background: #18181B; }
        .skill-example .example-arrow { font-size: 28px; transform: rotate(-135deg); }
        @media (max-width: 767px) {
            .skill-example { flex-direction: column; align-items: stretch; }
            .skill-example .example-arrow { align-self: center; transform: rotate(135deg); }
        }""")

(ROOT / "site/work-single.html").write_text(html)
check_english("work-single.html", html)
