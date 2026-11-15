"""חלקים משותפים לכל העמודים: תפריט עליון, תפריט מובייל, פוטר."""
import re

SITE_URL = "https://free-ai.co.il"

NAV = [
    ("index.html", "דף הבית"),
    ("service.html", "הקורס"),
    ("work.html", "סקילים"),
]


def header(active):
    items = "\n".join(
        f'''                        <li class="menu-item">
                            <a href="{href}" class="item-link link1{' active' if href == active else ''}">{label}</a>
                        </li>'''
        for href, label in NAV
    )
    return f'''<!-- Header -->
        <header class="tf-header header2">
            <div class="header-inner">
                <a href="index.html" class="logo-site">
                    <img src="assets/images/logo/logo.svg" alt="Free AI">
                </a>
                <div class="box-navigation">
                    <ul class="nav-menu-main">
{items}
                    </ul>
                </div>
                <a href="service.html" class="tf-btn d-lg-flex d-none">
                    התחל ללמוד
                </a>
                <a href="#" class="tf-btn open-mb-menu mobile-menu d-lg-none d-flex">
                    <i class="icon icon-grip-lines-solid"></i>
                </a>
            </div>
        </header>
        <!-- /Header -->'''


def mobile_menu():
    items = "\n".join(
        f'''                            <li>
                                <div class="item">
                                    <a href="{href}" class="mb-menu-link text-display-1">
                                        <span class="text">{label}</span>
                                    </a>
                                </div>
                            </li>'''
        for href, label in NAV
    )
    return f'''<!-- Mobile Menu -->
    <div class="offcanvas-menu">
        <div class="offcanvas-content">
            <div class="container h-100">
                <div class="offcanvas-content_wrapin">
                    <div class="canvas_head">
                        <a href="index.html" class="logo-site">
                            <img src="assets/images/logo/logo.svg" alt="Free AI" style="height:56px">
                        </a>
                        <div class="btn-mobile-menu close-mb-menu text-caption link">
                            <i class="icon icon-close"></i>
                            סגירה
                        </div>
                    </div>
                    <div class="canvas_center">
                        <ul class="nav-ul-mb" id="mobile-menu">
{items}
                        </ul>
                    </div>
                    <div class="canvas_foot">
                        <div class="left">
                            <a href="service.html" class="text-caption text-neutral-200">התחל ללמוד</a>
                            <p class="text-caption text-neutral-200">
                                ישראל <span class="clock"></span>
                            </p>
                        </div>
                        <div class="right">
                            <a href="work.html" class="tf-link-icon text-caption text-neutral-200">
                                <i class="icon icon-arrow-top-right"></i>
                                סקילים
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- /Mobile Menu -->'''


FOOTER = '''<!-- footer -->
        <footer class="tf-footer">
            <div class="footer-image">
                <img class="effectFade fadeUp" src="assets/images/logo/logo-footer.png" alt="">
            </div>
            <div class="container">
                <div class="footer-content">
                    <a href="index.html" class="footer-logo">
                        <img src="assets/images/logo/logo-2.svg" alt="Free AI">
                    </a>
                    <div class="title h6 fw-semibold">קורס Claude מאפס. <br> פתוח לכולם, בחינם.</div>
                    <div class="text">שיעור חדש עולה כל שבוע.</div>
                    <div class="tf-social-1 justify-content-center">
                        <a href="service.html" class="text-body-1 fw-semibold">
                            הקורס
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
                <div class="footer-bottom">
                    <ul class="footer-links d-flex gap-24 align-items-center">
                        <li>
                            <a href="privacy.html" class="fw-semibold link-underline link1">פרטיות</a>
                        </li>
                        <li>
                            <a href="terms.html" class="fw-semibold link-underline link1">תנאי שימוש</a>
                        </li>
                    </ul>
                    <p class="text-secondary coppy-rights text-center">© 2026 Free AI. כל הזכויות שמורות.</p>
                    <a href="#" class="action-go-top d-flex gap-8 align-items-center justify-content-end link1">
                        <span class="fw-semibold">חזרה למעלה</span>
                        <i class="icon icon-long-arrow-alt-up-solid fs-20"></i>
                    </a>
                </div>
            </div>
        </footer>
        <!-- /footer -->'''


def apply_common(html, active, title, description):
    html = re.sub(r'<html [^>]*lang="en-US">', '<html lang="he" dir="rtl">', html)
    html = html.replace('<!--[if IE 8]><html class="ie" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US"> <![endif]-->\n', "")
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, flags=re.S)
    html = re.sub(r'<meta name="author" content="[^"]*">', '<meta name="author" content="Free AI">', html)
    html = re.sub(r'<meta name="description"\s+content="[^"]*">', f'<meta name="description" content="{description}">', html, flags=re.S)
    page = "" if active == "index.html" and title.startswith("Free AI") else active
    og = f'''<meta property="og:type" content="website">
    <meta property="og:site_name" content="Free AI">
    <meta property="og:locale" content="he_IL">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{SITE_URL}/assets/images/og.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="assets/images/logo/logo.svg" type="image/svg+xml">
    '''
    html = re.sub(r'(<meta name="description" content="[^"]*">)', lambda m: m.group(1) + "\n    " + og.rstrip(), html, count=1)
    html = html.replace('<button id="goTop">', '<button id="goTop" aria-label="חזרה למעלה">')
    html = html.replace('<link rel="stylesheet" type="text/css" href="assets/css/styles.css">',
                        '<link rel="stylesheet" type="text/css" href="assets/css/styles.css?v=2">\n    <link rel="stylesheet" type="text/css" href="assets/css/rtl.css?v=3">')
    html = re.sub(r"<!-- Header -->.*?<!-- /Header -->", lambda m: header(active), html, flags=re.S)
    html = re.sub(r"<!-- footer -->.*?<!-- /footer -->", lambda m: FOOTER, html, flags=re.S)
    html = re.sub(r"<!-- Mobile Menu -->.*?<!-- /Mobile Menu -->", lambda m: mobile_menu(), html, flags=re.S)
    # אייקונים מוטים בכותרת: אייקוני Claude במקום לוגואים מומצאים של התבנית
    for a, b in [("item-10", "hero-1"), ("item-11", "hero-2"), ("item-12", "hero-3"),
                 ("item-13", "hero-1"), ("item-14", "hero-2"), ("item-15", "hero-3")]:
        html = html.replace(f"assets/images/item/{a}.svg", f"assets/images/item/{b}.svg")
    # כתום המותג במקום האדום של התבנית, ותמונת רקע חמה לטופס ההרשמה
    html = html.replace('stop-color="#EA2B16"', 'stop-color="#C2603F"').replace('stop-color="#FF3B26"', 'stop-color="#D97757"')
    html = html.replace("assets/images/section/contact-image-bg.jpg", "assets/images/section/contact-warm.jpg")
    # מסירים את כפתור ההגדרות של התבנית
    html = re.sub(r"\s*<!-- Left Bar -->.*?<!-- /Setting Color -->", "", html, flags=re.S)
    return html


def replace_section(html, name, new):
    pat = re.compile(rf"<!-- {re.escape(name)} -->.*?<!-- /{re.escape(name)} -->", re.S)
    if not pat.search(html):
        raise SystemExit(f"section not found: {name}")
    return pat.sub(lambda m: new.strip(), html, count=1)
