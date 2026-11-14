"""דף הבית של Free AI – נבנה מתוך index.html של האתר המשוכפל."""
import re
from pathlib import Path
from common import apply_common, replace_section

ROOT = Path(__file__).resolve().parents[2]
html = (ROOT / "aigocy-about/index.html").read_text()

html = apply_common(
    html,
    "index.html",
    "Free AI – לומדים Claude מאפס, בעברית",
    "קורס Claude בעברית: שיעורים קצרים, קבצים מוכנים וסקילים – מהשאלה הראשונה ועד Claude Code.",
)

# ---------- Hero ----------
html = html.replace("AI-Driven Agency\n", "קורס Claude בעברית\n")
html = html.replace(
    '<span class="title1 fw-semibold text-gradient-1">Your AI Sprint Team</span>',
    '<span class="title1 fw-semibold text-gradient-1">לומדים Claude</span>',
)
html = html.replace(
    '<span class="fw-semibold text-gradient-1">on Demand</span>',
    '<span class="fw-semibold text-gradient-1">מאפס.</span>',
)
html = html.replace(
    "From discovery to deployment, we plug into your stack to prototype, <br> validate, and launch AI experiences your users actually love.",
    "שיעורים קצרים בעברית – מהשאלה הראשונה ועד סקילים ו-Claude Code. <br> בלי ידע קודם.",
)
html = html.replace(
    '''<a href="service.html" class="tf-btn">
                            Explore Services
                        </a>
                        <a href="#pricing" class="tf-btn-2">
                            View Pricing Plans
                        </a>''',
    '''<a href="service-single.html" class="tf-btn">
                            לקורס Claude
                        </a>
                        <a href="work.html" class="tf-btn-2">
                            סקילים ל-Claude
                        </a>''',
)
html = html.replace('<span class="fw-semibold link1">Scroll for more</span>', '<span class="fw-semibold link1">גוללים למטה</span>')

# ---------- About ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">About Us</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הקורס</div>')
html = html.replace('<div class="heading-title text-gradient-2 effectFade fadeRotateX">Human-Centered AI, <br> Built for Production</div>',
                    '<div class="heading-title text-gradient-2 effectFade fadeRotateX">Claude, <br> בעברית פשוטה</div>')
html = html.replace("Available for worldwide project", "הקורס הראשון באתר")
html = html.replace('<h5 class="title fw-semibold text-white">Based in <span class="text-brand">Montréal, Canada</span></h5>',
                    '<h5 class="title fw-semibold text-white">לומדים ב<span class="text-brand">עברית, מאפס</span></h5>')
html = html.replace('''<a href="contact.html" class="tf-btn">
                                    Start a Project
                                </a>''', '''<a href="service-single.html" class="tf-btn">
                                    לשיעור הראשון
                                </a>''')
html = html.replace("Trusted by 120+ clients across 4 industries - <br> shipping AI from idea to production in 8–10 weeks",
                    "שיעורים קצרים, קבצים מוכנים וסקילים - <br> מהשאלה הראשונה ועד עבודה יומיומית עם Claude")
html = html.replace("Trustpilot\n", "שיעורים בקורס\n")
html = html.replace('<span class="number" data-speed="1500" data-to="120" data-inviewport="yes">10</span><span>+</span>',
                    '<span class="number" data-speed="1500" data-to="8" data-inviewport="yes">8</span>')
html = html.replace("Good AI feels obvious—because the hard work is hidden.", "Claude הוא הכלי הכי חזק שיש היום. צריך רק לדעת מה לבקש.")
html = html.replace('<div class="name text-body-3 fw-semibold">Ava Collins</div>', '<div class="name text-body-3 fw-semibold">שי</div>')
html = html.replace("<div class=\"sub text-body-3\">Aigocy’s Design Lead</div>", '<div class="sub text-body-3">המייסד של Free AI</div>')

# ---------- Partner → הכלים שלומדים ----------
tools = ["Claude", "Projects", "Artifacts", "Skills", "Claude Code", "MCP", "Desktop", "Mobile"]
html = html.replace('<p class="text-secondary text fw-semibold">Trusted by 100+ <br> top-tier brands</p>',
                    '<p class="text-secondary text fw-semibold">מה לומדים <br> בקורס</p>')
html = re.sub(
    r'(<div class="infiniteSlide infiniteSlide_partner" data-clone="5">).*?(</div>)',
    lambda m: m.group(1) + "".join(f'\n                                    <span class="tool-name">{t}</span>' for t in tools) + "\n                                " + m.group(2),
    html, count=1, flags=re.S,
)

# ---------- Services → המסלולים ----------
tracks = [
    ("מתחילים <br> עם Claude", "פותחים חשבון, מכירים את המסך ושואלים את השאלה הראשונה.", "claude-start.jpg"),
    ("לבקש <br> נכון", "איך כותבים בקשה שמקבלת תשובה טובה כבר בפעם הראשונה.", "claude-prompt.jpg"),
    ("Projects <br> וקבצים", "מלמדים את Claude על העסק שלכם פעם אחת – והוא זוכר.", "claude-projects.jpg"),
    ("Artifacts", "גרפים, מסמכים וכלים קטנים שנבנים ישר בתוך השיחה.", "claude-artifacts.jpg"),
    ("סקילים <br> ו-Claude Code", "מוסיפים ל-Claude יכולות חדשות ובונים אתר שלם.", "claude-code.jpg"),
]
items = []
for i, (title, text, img) in enumerate(tracks, 1):
    first = i == 1
    items.append(f'''                                <div class="accordion-faq_item effectFade fadeUp" role="presentation">
                                    <div class="accordion-action services-image-btn{' active-img' if first else ' collapsed'}" data-img="assets/images/claude/{img}" data-bs-target="#faq-{i}" role="button"
                                        data-bs-toggle="collapse" aria-controls="faq-{i}" aria-expanded="{'true' if first else 'false'}">
                                        <div class="accordion-title">
                                            {title}
                                            <div class="text-body-1 num">(0{i})</div>
                                        </div>
                                    </div>
                                    <div id="faq-{i}" class="collapse{' show' if first else ''}" data-bs-parent="#accordion-services">
                                        <div class="accordion-content">
                                            <div class="text-body-3 text-neutral-300 text">{text}</div>
                                        </div>
                                    </div>
                                </div>''')
html = re.sub(r'(<div class="accordion-faq_list" id="accordion-services">).*?(\n                            </div>\n                        </div>\n                        <div class="services-image)',
              lambda m: m.group(1) + "\n" + "\n".join(items) + m.group(2), html, count=1, flags=re.S)
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Services</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">מה בקורס</div>')
html = html.replace('<div class="heading-title text-gradient-3 effectFade fadeRotateX">End-to-End <br> AI Services</div>',
                    '<div class="heading-title text-gradient-3 effectFade fadeRotateX">Claude <br> מאפס</div>')
html = html.replace("We turn ambiguous AI ideas into production features your users trust—combining strategy, design, engineering, and rigorous evaluation.",
                    "חמישה פרקים. כל פרק נגמר במשהו שעובד – תשובה טובה יותר, מסמך, כלי או אתר.")

# ---------- Featured works → מה תבנו ----------
html = html.replace('<div class="heading-sub fw-semibold mx-auto effectFade fadeUp">Featured Works</div>', '<div class="heading-sub fw-semibold mx-auto effectFade fadeUp">מה תבנו עם Claude</div>')
projects = [
    ("אתר עסקי <br> עם Claude Code", "אתר מלא, מהרעיון ועד כתובת באוויר – בלי לכתוב שורת קוד.", "Claude Code", "מתקדם"),
    ("דוח אבטחה <br> עם סקיל", "סקיל אחד בודק את האתר ומחזיר דוח בעברית: מה תקין ומה לתקן.", "סקילים", "בינוני"),
    ("עוזר לעסק <br> עם Projects", "Claude שמכיר את המחירון והנהלים שלכם ועונה ללקוחות בשבילכם.", "Projects", "מתחילים"),
    ("מחשבון מחיר <br> עם Artifacts", "כלי קטן שאפשר לשלוח ללקוחות בקישור – נבנה בשיחה אחת.", "Artifacts", "מתחילים"),
]
for (title, desc, track, level), old in zip(projects, [
    ("Support Copilot <br> for SaaS", "Draft replies and pulls account context; reduced first-response time by 38%.", "AI strategy, AI UX flows, <br> LLM agent, RAG", "SaaS"),
    ("Underwriting <br> Risk Copilot", "Built a triage assistant to summarize claims; cut manual review time by 42%.", "Use-case mapping, Prompt & UI patterns", "Fintech"),
    ("Clinical Note <br> Summarizer", "Clinic-lobby assistant answering pre-visit questions; decreased front-desk calls by 28%.", "PHI-safe RAG, HIPAA-aligned workflows", "Healthcare"),
    ("Catalog Intelligence <br> Engine", "Launched a shopping copilot that understands attributes; raised add-to-cart by 12%.", "Data cleaning & embeddings", "Ecommerce/Retail"),
]):
    for a, b in zip(old, (title, desc, track, level)):
        assert a in html, a
        html = html.replace(a, b, 1)
html = html.replace('<div class="title text-secondary">DESCRIPTION</div>', '<div class="title text-secondary">מה בונים</div>')
html = html.replace('<div class="title text-secondary">DELIVERABLES</div>', '<div class="title text-secondary">פרק</div>')
html = html.replace('<div class="title text-secondary">INDUSTRY</div>', '<div class="title text-secondary">רמה</div>')
html = html.replace('href="work-single.html" class="tf-mouse view-project h6">\n                                        View Project', 'href="service-single.html" class="tf-mouse view-project h6">\n                                        לקורס')

# ---------- Process → איך זה עובד ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Process</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">איך זה עובד</div>')
html = html.replace('<div class="heading-title text-gradient-3 effectFade fadeRotateX">From Idea <br> to Production</div>',
                    '<div class="heading-title text-gradient-3 effectFade fadeRotateX">שלושה צעדים <br> ומתחילים</div>')
for a, b in [
    ("Discover & Scope", "נרשמים"),
    ("Align on problems, data reality, and success metrics. Opportunity brief, KPI model, phased roadmap, effort/cost ranges.", "בלחיצה עם Google, או עם קוד שמגיע למייל. בלי סיסמה ובלי כרטיס אשראי."),
    ("3-7 DAYS", "דקה אחת"),
    ("<h4 class=\"title fw-semibold\">Prototype</h4>", "<h4 class=\"title fw-semibold\">צופים ומתרגלים</h4>"),
    ("De-risk unknowns and validate value quickly. Clickable UX, tech spike repo, initial eval rubric, demo.", "סרטון קצר, סיכום, קישורים וקבצים להורדה בכל שיעור. האתר זוכר איפה עצרתם."),
    ("1-2 WEEKS", "בקצב שלכם"),
    ("Validate & Evals", "מקבלים תעודה"),
    ("Prove accuracy, usability, safety, and cost. Eval dashboard, acceptance thresholds, decision to iterate/ship.", "מסיימים את הקורס ומקבלים תעודה עם השם שלכם."),
    ("1 WEEKS", "בסוף הקורס"),
]:
    assert a in html, a
    html = html.replace(a, b, 1)

html = html.replace('<div dir="ltr" class="swiper tf-swiper swiper-box-shadow" data-preview="1.78"', '<div dir="rtl" class="swiper tf-swiper swiper-box-shadow" data-preview="1.78"')

# ---------- Benefits → למה Free AI ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Benefits</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">איך לומדים</div>')
html = html.replace('<div class="heading-title text-gradient-3 effectFade fadeRotateX">Why Choose Us</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">לומדים בעשייה</div>')
for a, b in [
    ("Accuracy\n", "Chat\n"), ("Latency\n", "Projects\n"), ("Safety\n", "Artifacts\n"), ("Cost\n", "Skills\n"),
    ("Outcome over Output", "תוצאה, לא תיאוריה"),
    ("We measure what matters - accuracy, latency, safety, and <br> cost - so every sprint ships business value, not just features.", "כל שיעור נגמר במשהו שעובד – תשובה, מסמך, כלי או <br> אתר. לא רק להבין, אלא לבנות."),
    ("Eval-First Reliability", "שומר את ההתקדמות"),
    ("From day one, we run offline/online evals, canary tests, and tracing. You see how models perform - and why.", "מסמנים ✓ על כל שיעור שסיימתם, וחוזרים בדיוק לנקודה שבה עצרתם."),
    ("Secure by Design</h6>\n                                    <p class=\"text text-secondary\">PII handling, SSO/SAML, RBAC, encryption, and audit trails -built in, not bolted on. Enterprise-ready from the start.",
     "גם עם החשבון החינמי</h6>\n                                    <p class=\"text text-secondary\">רוב השיעורים עובדים עם החשבון החינמי של Claude. כשצריך מנוי – כתוב מראש."),
    ("Design-Led AI Experiences", "קבצים מוכנים להורדה"),
    ("We craft prompts, interfaces, and guardrails that feel intuitive - so adoption rises and support tickets fall.", "פרומפטים, סקילים וצ'קליסטים – מורידים ומשתמשים, בלי לבנות מאפס."),
]:
    assert a in html, a
    html = html.replace(a, b, 1)

# ---------- Features → בכל שיעור ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Features</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">בכל שיעור</div>')
html = html.replace('<div class="heading-title text-gradient-3 effectFade fadeRotateX">All Features in One</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">כל מה שצריך, במקום אחד</div>')
for a, b in [
    ("Agent-Powered Workflows", "סרטון קצר וממוקד"),
    ("Turn repetitive tasks into autonomous flows—agents plan, execute, and report with guardrails, audit trails, and clear handoff to humans.", "בלי חפירות ובלי מילוי. רק מה שצריך כדי להתקדם לשלב הבא."),
    ("Eval-First Quality", "סיכום וקישורים"),
    ("Measure accuracy, latency, safety, and cost from day one. Our evals and dashboards keep models reliable and budgets predictable.", "כל מה שהוזכר בשיעור מופיע מתחת לסרטון – ליישום מיידי, בלי לחפש."),
    ("Private Knowledge RAG", "קבצים להורדה"),
    ("Make your docs, tickets, and wikis instantly useful with retrieval augmented generation—freshness, citations, and explainability built in.", "תבניות, פרומפטים וצ'קליסטים מוכנים לכל שיעור שצריך אותם."),
    ("Human-Centered AI UX", "בעברית פשוטה"),
    ("Interfaces, prompts, and error states designed for trust and adoption—so the smart thing is also the obvious thing to do.", "בלי מונחים מסובכים. מסבירים כל צעד כאילו זו הפעם הראשונה."),
    ("<h6 class=\"title fw-semibold\">Secure by Design</h6>\n                                    <p class=\"text-secondary\">\n                                        PII handling, SSO/SAML, RBAC, secrets management, and compliance workflows—ship AI that’s safe, auditable, and enterprise-ready.",
     "<h6 class=\"title fw-semibold\">מעלים לאוויר</h6>\n                                    <p class=\"text-secondary\">\n                                        הדרכה צעד-צעד לאחסון ושרת, כדי שמה שבניתם ירוץ 24/7."),
    ("Seamless Integrations", "עזרה בוואטסאפ"),
    ("Plug into your stack (CRM, helpdesk, ERP, data warehouse) with webhooks and APIs to turn insights into action—fast.", "נתקעתם? שולחים שאלה בלחיצה ומקבלים תשובה."),
]:
    assert a in html, a
    html = html.replace(a, b, 1)

# ---------- Tools ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Tools</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">Claude בכל מקום</div>')
html = html.replace('<div class="heading-title text-gradient-3 effectFade fadeRotateX">We work with powerful AI tools</div>', '<div class="heading-title text-gradient-3 effectFade fadeRotateX">באתר, במחשב ובטלפון</div>')
html = html.replace("We design, build, and evaluate with a modern AI stack—LLMs, vector search, orchestration, and observability—so your features are fast, reliable, and secure.",
                    "Claude באתר, באפליקציה למחשב ובטלפון, ו-Claude Code לבניית אתרים – כל אחד בהסבר צעד אחרי צעד.")
html = html.replace('''<a href="contact.html" class="tf-btn effectFade fadeRotateX">
                            Get Started
                        </a>''', '''<a href="service-single.html" class="tf-btn effectFade fadeRotateX">
                            לקורס Claude
                        </a>''')

# ---------- box-black: בלי צוות ובלי המלצות מומצאות ----------
html = re.sub(r"\s*<!-- section-team -->.*?<!-- /section-team -->", "", html, count=1, flags=re.S)
html = re.sub(r"\s*<!-- section-testimonials -->.*?<!-- /section-testimonials -->", "", html, count=1, flags=re.S)

html = html.replace('<div class="heading-sub fw-semibold style-1 effectFade fadeUp">Statistic</div>', '<div class="heading-sub fw-semibold style-1 effectFade fadeUp">במספרים</div>')
html = html.replace('<div class="heading-title text-white effectFade fadeRotateX">Human-centered <br> AI, built for <br> production</div>',
                    '<div class="heading-title text-white effectFade fadeRotateX">Claude. <br> בעברית. <br> מאפס.</div>')
html = html.replace("We shipped our first copilot in 7 weeks and cut support tickets by 31%. The eval dashboards made every decision obvious.\n                                </div>\n                                <div class=\"swiper swiper-progressbar\">",
                    "קורס מלא ב-Claude – שיעורים קצרים, קבצים מוכנים ותעודה בסוף. בלי ידע קודם.\n                                </div>\n                                <div class=\"swiper swiper-progressbar\">")
for a, b in [
    ('<div class="title fw-semibold text-body-1">OUR GROWTH</div>', '<div class="title fw-semibold text-body-1">שיעורים</div>'),
    ('<span class="number text-white fw-semibold">230</span>\n                                                <span class="prefix text-brand">K</span>', '<span class="number text-white fw-semibold">8</span>\n                                                <span class="prefix text-brand"></span>'),
    ('<div class="title fw-semibold text-body-1">UPTIME FOR KEY FLOWS</div>', '<div class="title fw-semibold text-body-1">פרקים</div>'),
    ('<span class="number text-white fw-semibold">95</span>\n                                                <span class="prefix text-brand">%</span>', '<span class="number text-white fw-semibold">5</span>\n                                                <span class="prefix text-brand"></span>'),
    ('<div class="title fw-semibold text-body-1">ON TIME DELIVERY</div>', '<div class="title fw-semibold text-body-1">בעברית</div>'),
    ('<span class="number text-white fw-semibold">99</span>\n                                                <span class="prefix text-brand">%</span>', '<span class="number text-white fw-semibold">100</span>\n                                                <span class="prefix text-brand">%</span>'),
]:
    assert a in html, a
    html = html.replace(a, b, 1)

# Awards → ספריית סקילים
skills = [
    ("shield-alt-solid", "בדיקת אבטחה לאתר", "34 בדיקות – דוח אדום / כתום / ירוק בעברית", "/ אבטחה"),
    ("tachometer-alt-solid", "בדיקת מהירות לאתר", "69 בדיקות ופרומפט מוכן לכל תיקון", "/ ביצועים"),
    ("book-solid", "סקילים לכתיבה", "פוסטים, מיילים ודפי נחיתה בסגנון שלכם", "/ בקרוב"),
    ("bullseye-solid", "סקילים לשיווק", "מודעות, קהלים ותוכן לרשתות", "/ בקרוב"),
]
rows = []
for i, (img, title, text, year) in enumerate(skills):
    delay = f' data-delay="0.{i}"' if i else ""
    rows.append(f'''                        <a href="work.html" class="awards-item effectFade fadeUp"{delay}>
                            <div class="image">
                                <i class="icon icon-{img} skill-icon"></i>
                            </div>
                            <div class="title text-body-1 text-white">{title}</div>
                            <div class="text text-body-1 text-white">{text}</div>
                            <div class="year text-body-1 text-neutral-400">{year}</div>
                        </a>''')
html = re.sub(r'(<div class="d-grid gap-16">).*?(\n                    </div>\n                </div>\n            </div>\n            <!-- /section-awards -->)',
              lambda m: m.group(1) + "\n" + "\n".join(rows) + m.group(2), html, count=1, flags=re.S)
html = html.replace('<div class="heading-sub fw-semibold style-1 mb-0 effectFade fadeUp">Awards</div>', '<div class="heading-sub fw-semibold style-1 mb-0 effectFade fadeUp">ספריית סקילים ל-Claude</div>')

# ---------- Pricing ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Pricing Plans</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">מחיר</div>')
html = re.sub(r'(<div class="heading-title text-gradient-3 gap-8 effectFade fadeRotateX">).*?(</div>\n                </div>\n                <div class="row">)',
              lambda m: m.group(1) + "\n                        אותו ידע. <br>\n                        <div class=\"h-8 d-none d-lg-block\"></div>\n                        בלי המחיר.\n                    " + m.group(2), html, count=1, flags=re.S)
for a, b in [
    ('<div class="fw-semibold text">Starter Plan</div>', '<div class="fw-semibold text">קורס AI רגיל</div>'),
    ('<div class="fw-semibold text-secondary">For startups</div>', '<div class="fw-semibold text-secondary">בשוק היום</div>'),
    ('<div class="price-number fw-bold" data-month="1000" data-year="9900">$9,900</div>\n                                    <h6 class="price-per">/ year</h6>', '<div class="price-number fw-bold" style="text-decoration:line-through">₪3,000</div>\n                                    <h6 class="price-per">ומעלה</h6>'),
    ('''<a href="contact.html" class="tf-btn">
                                    Get Started
                                </a>
                            </div>
                            <div class="line"></div>
                            <div class="content">
                                <div>
                                    <div class="title fw-semibold mb-4">What’s included</div>
                                    <div class="text fw-semibold">
                                        Prove value in two weeks with a clickable UX, tech spike, and a clear go/no-go roadmap.''', '''<span></span>
                            </div>
                            <div class="line"></div>
                            <div class="content">
                                <div>
                                    <div class="title fw-semibold mb-4">מה מקבלים</div>
                                    <div class="text fw-semibold">
                                        קורס אחד, בתשלום מראש, ולרוב עם גישה מוגבלת בזמן.'''),
    ("Discovery workshop", "קורס אחד בלבד"),
    ("Opportunity brief", "גישה מוגבלת בזמן"),
    ("Clickable UX", "קבצים ותבניות בתשלום נוסף"),
    ("1 data source & 1 integration", "תעודה בתשלום"),
    ('<div class="fw-semibold text">Enterprise Plan</div>', '<div class="fw-semibold text">Free AI</div>'),
    ('<div class="fw-semibold text-neutral-400">For organisations</div>', '<div class="fw-semibold text-neutral-400">לכולם</div>'),
    ('<div class="price-number fw-bold" data-month="1700" data-year="19900">$19,900</div>\n                                    <h6 class="price-per">/ year</h6>', '<div class="price-number fw-bold">₪0</div>\n                                    <h6 class="price-per">לתמיד</h6>'),
    ('''<a href="contact.html" class="tf-btn">
                                    Get Started
                                </a>''', '''<a href="contact.html#signup" class="tf-btn">
                                    הרשמה חינם
                                </a>'''),
    ('<div class="title fw-semibold mb-4">What’s included</div>', '<div class="title fw-semibold mb-4">מה מקבלים</div>'),
    ("Compliance-ready delivery for complex orgs—multi-env releases, canaries, and change management.", "כל המסלולים, כל הקבצים וכל הסקילים – פתוחים מהיום הראשון."),
    ("Everything in Starter", "כל 5 המסלולים"),
    ("CI/CD, tracing, alerts, guardrails", "כל הקבצים והסקילים"),
    ("Full eval dashboard", "תעודת סיום לכל מסלול"),
    ("3 data source & 3 integration", "עזרה בוואטסאפ"),
]:
    assert a in html, a
    html = html.replace(a, b, 1)

# ---------- FAQ ----------
faqs = [
    ("צריך מנוי בתשלום ל-Claude?", "לא. רוב השיעורים עובדים עם החשבון החינמי. בשיעורים שצריך מנוי – כתוב את זה מראש."),
    ("צריך ידע קודם?", "לא. הקורס מתחיל מפתיחת חשבון ומסביר כל צעד בעברית פשוטה."),
    ("כמה זמן לוקח הקורס?", "8 שיעורים קצרים. אפשר לסיים בערב אחד, או בקצב שלכם – האתר זוכר איפה עצרתם."),
    ("למה צריך להירשם?", "ההרשמה שומרת את ההתקדמות, פותחת את הקבצים להורדה ומאפשרת לקבל תעודה בסוף הקורס."),
]
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">FAQs</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">שאלות נפוצות</div>')
html = html.replace("Frequently Asked <br>Questions", "שאלות <br>ותשובות")
olds = ["What’s the typical timeline from idea to v1?", "What do we need to start?", "Which models/stack do you use?", "Are model/API costs included in pricing?"]
ans_old = "A clear problem statement, success metrics, access to sample data, and a stakeholder who can make decisions. We’ll run a kickoff workshop to align scope."
for (q, a), oq in zip(faqs, olds):
    html = html.replace(oq, q, 1)
    html = html.replace(ans_old, a, 1)

# ---------- Contact → הרשמה ----------
html = html.replace('<div class="heading-sub fw-semibold effectFade fadeUp">Contact</div>', '<div class="heading-sub fw-semibold effectFade fadeUp">הרשמה</div>')
html = html.replace("Let’s Build <br> Intelligent Things", "מתחילים מהשיעור <br> הראשון")
html = html.replace('<div class="title fw-semibold mb-2">E-mail address</div>\n                                            <div class="text">hello@youraiagency.com</div>',
                    '<div class="title fw-semibold mb-2">פחות מדקה</div>\n                                            <div class="text">הרשמה עם Google או קוד למייל</div>')
html = html.replace('<i class="icon icon-envelope-solid"></i>', '<i class="icon icon-bolt-solid"></i>', 1)
html = html.replace('<div class="title fw-semibold mb-2">Phone number</div>\n                                            <div class="text">+1 (647) 555 0172</div>',
                    '<div class="title fw-semibold mb-2">8 שיעורים</div>\n                                            <div class="text">מהשאלה הראשונה ועד Claude Code</div>')
html = html.replace('<i class="icon icon-headset-solid"></i>', '<i class="icon icon-check-solid"></i>', 1)
html = re.sub(r'<form class="form-contact effectFade fadeUp">.*?</form>', '''<form class="form-contact effectFade fadeUp" id="signup" data-signup>
                                <h4 class="heading fw-semibold">הרשמה לקורס</h4>
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
                            </form>''', html, count=1, flags=re.S)

html = html.replace('<img src="assets/images/section/quotes-1.jpg" alt="">', '<img src="assets/images/logo/logo-1.svg" alt="Free AI" style="object-fit:contain;background:#09090B;padding:16px">')
# ---------- תמונות Claude ----------
for n, img in enumerate(["build-site", "security-skill", "projects-assistant", "artifact-tool"], 1):
    a = f'src="assets/images/section/featured-works-{n}.jpg" alt=""'
    assert a in html, a
    html = html.replace(a, f'src="assets/images/claude/{img}.jpg" alt=""')
html = html.replace('<img src="assets/images/section/service-1.jpg" alt="">', '<img src="assets/images/claude/claude-start.jpg" alt="">')
html = html.replace('href="service.html" class="tf-mouse view-project h6">\n                                        View Project', 'href="service-single.html" class="tf-mouse view-project h6">\n                                        לקורס')

# ---------- בלי בלוק מחירים ----------
html = re.sub(r"\s*<!-- section-pricing -->.*?<!-- /section-pricing -->", "", html, count=1, flags=re.S)

(ROOT / "site/index.html").write_text(html)
left = re.findall(r">\s*([A-Za-z][A-Za-z ,’'&\-]{6,})\s*<", html)
print("index.html done; leftover English:", [x for x in left if x.strip() not in ("Free AI",)][:20])
