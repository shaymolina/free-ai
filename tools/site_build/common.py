"""חלקים משותפים לכל העמודים: תפריט עליון, תפריט מובייל, פוטר."""
import re

NAV = [
    ("index.html", "דף הבית"),
    ("service.html", "קורסים"),
    ("work.html", "סקילים"),
    ("blog-standard.html", "בלוג"),
    ("about.html", "עליי"),
    ("contact.html", "צור קשר"),
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
                <a href="contact.html#signup" class="tf-btn d-lg-flex d-none">
                    הרשמה חינם
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
                            <img src="assets/images/logo/logo-2.svg" alt="Free AI" style="height:48px">
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
                            <a href="contact.html#signup" class="text-caption text-neutral-200">הרשמה חינם</a>
                            <p class="text-caption text-neutral-200">
                                ישראל <span class="clock"></span>
                            </p>
                        </div>
                        <div class="right">
                            <a href="work.html" class="tf-link-icon text-caption text-neutral-200">
                                <i class="icon icon-arrow-top-right"></i>
                                סקילים
                            </a>
                            <a href="blog-standard.html" class="tf-link-icon text-caption text-neutral-200">
                                <i class="icon icon-arrow-top-right"></i>
                                מדריכים
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- /Mobile Menu -->'''


FOOTER = '''<!-- footer -->
        <footer>
            <div class="footer-image">
                <img class="effectFade fadeUp" src="assets/images/logo/logo-footer.png" alt="">
            </div>
            <div class="container">
                <div class="footer-content">
                    <a href="index.html" class="footer-logo">
                        <img src="assets/images/logo/logo-2.svg" alt="Free AI">
                    </a>
                    <div class="title h6 fw-semibold">כל הידע של AI. <br> פתוח לכולם, בחינם.</div>
                    <div class="text">שיעור חדש עולה כל שבוע.</div>
                    <div class="tf-social-1 justify-content-center">
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
                        <a href="blog-standard.html" class="text-body-1 fw-semibold">
                            מדריכים
                            <div class="social-item">
                                <i class="icon icon-arrow-top-right"></i>
                            </div>
                        </a>
                        <a href="contact.html" class="text-body-1 fw-semibold">
                            צור קשר
                            <div class="social-item">
                                <i class="icon icon-arrow-top-right"></i>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="footer-bottom">
                    <ul class="footer-links d-flex gap-24 align-items-center">
                        <li>
                            <a href="about.html" class="fw-semibold link-underline link1">עליי</a>
                        </li>
                        <li>
                            <a href="contact.html" class="fw-semibold link-underline link1">צור קשר</a>
                        </li>
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
    html = html.replace('<link rel="stylesheet" type="text/css" href="assets/css/styles.css">',
                        '<link rel="stylesheet" type="text/css" href="assets/css/styles.css">\n    <link rel="stylesheet" type="text/css" href="assets/css/rtl.css">')
    html = re.sub(r"<!-- Header -->.*?<!-- /Header -->", lambda m: header(active), html, flags=re.S)
    html = re.sub(r"<!-- footer -->.*?<!-- /footer -->", lambda m: FOOTER, html, flags=re.S)
    html = re.sub(r"<!-- Mobile Menu -->.*?<!-- /Mobile Menu -->", lambda m: mobile_menu(), html, flags=re.S)
    # מסירים את כפתור ההגדרות של התבנית
    html = re.sub(r"\s*<!-- Left Bar -->.*?<!-- /Setting Color -->", "", html, flags=re.S)
    return html


def replace_section(html, name, new):
    pat = re.compile(rf"<!-- {re.escape(name)} -->.*?<!-- /{re.escape(name)} -->", re.S)
    if not pat.search(html):
        raise SystemExit(f"section not found: {name}")
    return pat.sub(lambda m: new.strip(), html, count=1)
