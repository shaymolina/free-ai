"""מוסיף קישורים למדריך בכל עמודי האתר: תפריט עליון, תפריט מובייל, פוטר ודף הבית.

בטוח להריץ שוב ושוב (לא מוסיף פעמיים). להריץ אחרי שבונים מחדש עמודים אחרים:
cd tools/site_build && python3 guide_links.py
"""
from clean_urls import clean
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"
GUIDE = "guide-1.html"

NAV_ANCHOR = '''                        <li class="menu-item">
                            <a href="work.html" class="item-link link1'''
NAV_ITEM = f'''                        <li class="menu-item">
                            <a href="{GUIDE}" class="item-link link1">המדריך</a>
                        </li>
'''
MOBILE_ITEM = f'''                            <li>
                                <div class="item">
                                    <a href="{GUIDE}" class="mb-menu-link text-display-1">
                                        <span class="text">המדריך</span>
                                    </a>
                                </div>
                            </li>
'''
FOOTER_ANCHOR = '''                        <a href="work.html" class="text-body-1 fw-semibold">
                            סקילים'''
FOOTER_ITEM = f'''                        <a href="{GUIDE}" class="text-body-1 fw-semibold">
                            המדריך
                            <div class="social-item">
                                <i class="icon icon-arrow-top-right"></i>
                            </div>
                        </a>
'''
HERO_ANCHOR = '''                        <a href="work.html" class="tf-btn-2">
                            סקילים ל-Claude
                        </a>'''
HERO_BTN = f'''
                        <a href="{GUIDE}" class="tf-btn-2">
                            המדריך המלא
                        </a>'''
HOME_ANCHOR = "            <!-- section-awards -->"
HOME_BLOCK = f'''            <!-- section-guide -->
            <div class="section-awards flat-spacing pb-0">
                <div class="container">
                    <div class="heading-section center mb-48">
                        <div class="heading-sub fw-semibold style-1 mb-0 effectFade fadeUp">המדריך המלא ל-Claude Code</div>
                    </div>
                    <div class="d-grid gap-16">
                        <a href="{GUIDE}" class="awards-item effectFade fadeUp">
                            <div class="image">
                                <i class="icon icon-book-open-solid skill-icon"></i>
                            </div>
                            <div class="title text-body-1 text-white">פרק 1: לפני שמתחילים</div>
                            <div class="text text-body-1 text-white">מא' עד ת', למי שלא מתכנת</div>
                            <div class="year text-body-1 text-neutral-400">/ 13 פרקים</div>
                        </a>
                    </div>
                </div>
            </div>
            <!-- /section-guide -->
'''


def patch(html, name):
    # תפריט עליון
    if f'<a href="{GUIDE}" class="item-link' not in html:
        assert NAV_ANCHOR in html, name
        html = html.replace(NAV_ANCHOR, NAV_ITEM + NAV_ANCHOR, 1)
    # תפריט מובייל
    if f'<a href="{GUIDE}" class="mb-menu-link' not in html:
        m = re.search(r' *<li>\s*<div class="item">\s*<a href="work\.html" class="mb-menu-link text-display-1">', html)
        assert m, name
        html = html[:m.start()] + MOBILE_ITEM + html[m.start():]
    # פוטר
    if f'<a href="{GUIDE}" class="text-body-1 fw-semibold">' not in html:
        assert FOOTER_ANCHOR in html, name
        html = html.replace(FOOTER_ANCHOR, FOOTER_ITEM + FOOTER_ANCHOR, 1)
    # דף הבית: כפתור בראש העמוד ובלוק המדריך
    if name == "index.html":
        if "המדריך המלא\n" not in html:
            assert HERO_ANCHOR in html, name
            html = html.replace(HERO_ANCHOR, HERO_ANCHOR + HERO_BTN, 1)
        if "<!-- section-guide -->" not in html:
            assert HOME_ANCHOR in html, name
            html = html.replace(HOME_ANCHOR, HOME_BLOCK + HOME_ANCHOR, 1)
    return html


for f in sorted(SITE.glob("*.html")):
    old = f.read_text()
    new = patch(old, f.name)
    if new != old:
        f.write_text(clean(new))
        print("updated", f.name)
