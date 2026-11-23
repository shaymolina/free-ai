"""הדר אחד לכל האתר. מקור יחיד: כאן. העיצוב ב-site/assets/css/site-header.css, ההתנהגות ב-site/assets/js/site-header.js.
apply_all() מחליף את ההדר בכל העמודים (חוץ מהמדריך, שיש לו מסך משלו). רץ אוטומטית בתחילת tools/seo/seo_build.py."""
import hashlib, os, re

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "site")
LINKS = [("service", "הקורס"), ("guide-1", "המדריך"), ("work", "סקילים"), ("articles", "מאמרים")]
START, END = "<!-- site-header -->", "<!-- /site-header -->"

# אזור משתמשים (Supabase): כתובת הפרויקט והמפתח הציבורי שלו (publishable, לא סודי). ההתחברות עם גוגל מוגדרת בתוך Supabase.
# העמודים ב-OPEN פתוחים לכולם, כל השאר דורשים התחברות.
SUPABASE_URL = "https://utkbzapqkucetphugmul.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0a2J6YXBxa3VjZXRwaHVnbXVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTU0MTQ2MjksImV4cCI6MjExMDk5MDYyOX0.VbAtIlS9kxXrTkrezkE3JlzZMsGH2QRG3OlqCQY018o"  # anon (ציבורי)
SUPABASE_JS = "assets/js/vendor/supabase-2.45.4.js"
OPEN = {"index", "privacy", "terms", "accessibility", "articles", "work"}
A_START, A_END = "<!-- auth-gate -->", "<!-- /auth-gate -->"
# סרגל הנגישות (נבנה מ-tools/a11y-toolbar עם npm run build:a11y). מעל מסך ההתחברות, כדי שיעבוד גם שם.
X_START, X_END = "<!-- a11y-toolbar -->", "<!-- /a11y-toolbar -->"
A11Y_Z = 100010


def _v(files=("css/site-header.css", "js/site-header.js")):
    h = hashlib.md5()
    for f in files:
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


def auth_html(slug):
    locked = "false" if slug in OPEN else "true"
    v = _v(("css/auth-gate.css", "js/auth-gate.js"))
    ref = SUPABASE_URL.split("//")[1].split(".")[0]
    # הסקריפט הקטן נועל את העמוד מיד (בלי הבהוב) כשאין חיבור שמור בדפדפן
    return (f'{A_START}<link rel="stylesheet" href="assets/css/auth-gate.css?v={v}">'
            f'<script>window.FA_AUTH={{url:"{SUPABASE_URL}",key:"{SUPABASE_KEY}",locked:{locked}}};'
            f'(function(a,u){{try{{u=localStorage.getItem("sb-{ref}-auth-token")}}catch(e){{}}'
            'var f=0;try{f=self!==top&&top.location.host===location.host}catch(e){}if(a.locked&&!f&&!u)document.documentElement.classList.add("ag-lock")})(window.FA_AUTH)</script>'
            f'<script src="{SUPABASE_JS}" defer></script>'
            f'<script src="assets/js/auth-gate.js?v={v}" defer></script>{A_END}')


def a11y_html():
    v = _v(("js/a11y-toolbar.js",))
    return (f'{X_START}<script src="assets/js/a11y-toolbar.js?v={v}" data-language="he" '
            f'data-position="bottom-left" data-z-index="{A11Y_Z}" async></script>{X_END}')


def apply_a11y(path):
    s = open(path).read()
    s = re.sub(re.escape(X_START) + ".*?" + re.escape(X_END), "", s, flags=re.S)
    s = s.replace("</head>", a11y_html() + "</head>", 1)
    open(path, "w").write(s)


def apply_viewport(path):
    """זום שלא חסום (בלי maximum-scale). הקישור לנגישות נמצא בפוטר האחיד (site_footer.py)."""
    s = open(path).read()
    s = re.sub(r'(<meta name="viewport" content="[^"]*?),\s*(?:maximum-scale=[\d.]+|user-scalable=(?:no|0))', r"\1", s)
    s = re.sub(r'(<meta name="viewport" content="[^"]*?),\s*(?:maximum-scale=[\d.]+|user-scalable=(?:no|0))', r"\1", s)
    open(path, "w").write(s)


def apply_auth(path):
    slug = os.path.basename(path)[:-5]
    s = open(path).read()
    s = re.sub(re.escape(A_START) + ".*?" + re.escape(A_END), "", s, flags=re.S)
    s = s.replace("</head>", auth_html(slug) + "</head>", 1)
    open(path, "w").write(s)


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
    pages = [os.path.join(SITE, f) for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    n = sum(apply(p) for p in pages)
    for p in pages: apply_auth(p)
    for p in pages: apply_a11y(p)
    for p in pages: apply_viewport(p)
    print(f"site header: {n} pages")


if __name__ == "__main__":
    apply_all()
