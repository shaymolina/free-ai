"""הדר אחד לכל האתר. מקור יחיד: כאן. העיצוב ב-site/assets/css/site-header.css, ההתנהגות ב-site/assets/js/site-header.js.
apply_all() מחליף את ההדר בכל העמודים (חוץ מהמדריך, שיש לו מסך משלו). רץ אוטומטית בתחילת tools/seo/seo_build.py."""
import hashlib, os, re

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "site")
LINKS = [("service", "הקורס"), ("guide-1", "המדריך"), ("work", "סקילים"), ("articles", "מאמרים")]
START, END = "<!-- site-header -->", "<!-- /site-header -->"


def _v():
    h = hashlib.md5()
    for f in ("css/site-header.css", "js/site-header.js"):
        h.update(open(os.path.join(SITE, "assets", f), "rb").read())
    return h.hexdigest()[:8]


def _active(slug):
    if slug.startswith("service"): return "service"
    if slug.startswith("guide"): return "guide-1"
    if slug.startswith("work"): return "work"
    if slug.startswith("article"): return "articles"
    return ""


def header_html(slug):
    act = _active(slug)
    def link(h, t, cls):
        on = ' aria-current="page"' if h == act else ""
        return f'<a class="{cls}" href="{h}"{on}>{t}</a>'
    nav = "".join(link(h, t, "gh-link") for h, t in LINKS)
    mob = link("/", "דף הבית", "gh-mlink") + "".join(link(h, t, "gh-mlink") for h, t in LINKS)
    v = _v()
    return (f'{START}<link rel="stylesheet" href="assets/css/site-header.css?v={v}">'
            '<header class="gh" id="gh"><div class="gh-in">'
            '<a class="gh-logo" href="/" aria-label="Free AI, לדף הבית"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>'
            f'<nav class="gh-nav" aria-label="ניווט ראשי">{nav}</nav>'
            '<a class="gh-btn" href="service">התחל ללמוד</a>'
            '<button class="gh-burger" type="button" aria-label="תפריט" aria-expanded="false" aria-controls="gh-m">'
            '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 6h14M3 10h14M3 14h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>'
            f'</div><nav class="gh-m" id="gh-m" aria-label="תפריט" hidden>{mob}<a class="gh-btn" href="service">התחל ללמוד</a></nav></header>'
            f'<script src="assets/js/site-header.js?v={v}" defer></script>{END}')


def _cut(s, open_re):
    """מוחק תגית header שמתחילה בביטוי, עד הסגירה שלה."""
    m = re.search(open_re, s)
    if not m: return s, False
    j = s.find("</header>", m.start())
    return s[:m.start()] + s[j + 9:], True


def apply(path):
    slug = os.path.basename(path)[:-5]
    if slug.startswith("guide-"): return False
    s = open(path).read()
    s = re.sub(re.escape(START) + ".*?" + re.escape(END), "", s, flags=re.S)
    for pat in (r'<header[^>]*\bid="top"', r'<header[^>]*\bid="top-m"', r'<header class="tf-header[^"]*"', r'<header class="c-header[^"]*"'):
        s, _ = _cut(s, pat)
    s = re.sub(r'\s*<!-- Mobile Menu -->\s*<div class="offcanvas-menu">.*?<!-- /Mobile Menu -->', "", s, flags=re.S)
    s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + header_html(slug), s, count=1)
    open(path, "w").write(s)
    return True


def apply_all():
    n = sum(apply(os.path.join(SITE, f)) for f in sorted(os.listdir(SITE)) if f.endswith(".html"))
    print(f"site header: {n} pages")


if __name__ == "__main__":
    apply_all()
