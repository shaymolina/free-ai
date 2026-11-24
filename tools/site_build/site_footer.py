"""פוטר אחד לכל האתר (חוץ מעמודי המדריך guide-*, שבהם אין פוטר). מקור יחיד: כאן. העיצוב ב-site/assets/css/site-footer.css.
apply_all() מחליף כל פוטר שיש בעמוד (ישן או חדש) בפוטר הזה, בכל העמודים. רץ אוטומטית מתוך seo_build.py,
כך שגם עמוד שנבנה מתבנית ישנה יקבל תמיד את הפוטר המעודכן."""
import glob
import hashlib
import os
import re

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "site")
START, END = "<!-- site-footer -->", "<!-- /site-footer -->"

GUIDE = [("guide-1", "לפני שמתחילים"), ("guide-3", "פותחים חשבון קלוד"), ("guide-5", "פותחים GitHub"),
         ("guide-7", "היכרות ראשונה עם קלוד"), ("guide-19", "מעלים לאוויר")]
TOOLS = [("guide-4", "Claude Code"), ("guide-13", "Connectors"), ("guide-14", "Skills"), ("guide-19", "4CODE")]
LEARN = [("course", "הקורס"), ("guide-1", "המדריך"), ("skills", "סקילים"), ("articles", "מאמרים")]
INFO = [("privacy", "פרטיות"), ("terms", "תנאי שימוש"), ("accessibility", "נגישות")]


def _v(name="css/site-footer.css"):
    return hashlib.md5(open(os.path.join(SITE, "assets", name), "rb").read()).hexdigest()[:8]


def _articles():
    """המאמרים: החדש ראשון, עם כותרת קצרה מתוך ה-<title>."""
    out = []
    for f in sorted(glob.glob(os.path.join(SITE, "article-*.html")), key=os.path.getmtime, reverse=True)[:4]:
        m = re.search(r"<title>(.*?)</title>", open(f).read(), re.S)
        t = (m.group(1) if m else "").split("|")[0].strip()
        short = t.split(" (")[0].split(" של ")[0].rstrip("?") + ("?" if "?" in t else "")
        out.append((os.path.basename(f)[:-5], short))
    return out


def footer_html():
    cols = [("לומדים", LEARN), ("המדריך", GUIDE), ("מאמרים", _articles()), ("כלים", TOOLS), ("מידע", INFO)]
    c = "".join(
        f'<div class="sf-col"><h2>{h}</h2><ul>{"".join(f"<li><a href=\"{a}\">{t}</a></li>" for a, t in links)}</ul></div>'
        for h, links in cols if links)
    return (f'{START}<link rel="stylesheet" href="assets/css/site-footer.css?v={_v()}">'
            '<footer class="sf" id="site-footer">'
            '<canvas class="sf-dots" aria-hidden="true"></canvas>'
            '<div class="sf-word" aria-hidden="true"><img src="assets/images/logo/logo-footer.png" alt="" width="1280" height="399" loading="lazy"></div>'
            '<div class="sf-in">'
            '<div class="sf-brand"><a class="sf-logo" href="/" aria-label="Free AI, לדף הבית"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>'
            '<div><p class="sf-tag-h">קלוד קוד בחינם</p><p class="sf-tag-p">קורס Claude Code למתחילים, בלי ידע בתכנות. שיעורי וידאו, מדריך כתוב וסקילים.</p></div>'
            '<a class="sf-mail" href="mailto:hello@free-ai.co.il">hello@free-ai.co.il</a></div>'
            f'<nav class="sf-cols" aria-label="קישורים בפוטר">{c}</nav>'
            '</div>'
            '<div class="sf-bot"><span class="sf-copy">© 2026 Free AI. כל הזכויות שמורות.</span>'
            '<a class="sf-top" href="#">חזרה למעלה ↑</a></div>'
            f'</footer><script src="assets/js/site-footer.js?v={_v("js/site-footer.js")}" defer></script>{END}')


FOOTER_RE = re.compile(r"<footer\b[^>]*>.*?</footer>", re.S)


def apply(path, html=None):
    s = open(path).read()
    if os.path.basename(path).startswith("guide-"):  # במדריך אין פוטר
        s = re.sub(re.escape(START) + ".*?" + re.escape(END), "", s, flags=re.S)
        open(path, "w").write(FOOTER_RE.sub("", s))
        return
    s = re.sub(re.escape(START) + ".*?" + re.escape(END), "<!--sf-slot-->", s, flags=re.S)
    if "<!--sf-slot-->" not in s:
        s, n = FOOTER_RE.subn("<!--sf-slot-->", s, count=1)
        if not n:
            s = s.replace("</body>", "<!--sf-slot-->\n</body>", 1)
    s = FOOTER_RE.sub("", s)  # פוטרים ישנים נוספים, אם יש
    s = s.replace("<!--sf-slot-->", html or footer_html(), 1)
    open(path, "w").write(s)


def apply_all():
    html = footer_html()
    pages = sorted(glob.glob(os.path.join(SITE, "*.html")))
    for p in pages:
        apply(p, html)
    print(f"site footer: {len(pages)} pages")


if __name__ == "__main__":
    apply_all()
