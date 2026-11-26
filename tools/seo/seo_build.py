"""שכבת SEO לאתר: מוסיף לכל עמוד canonical, Open Graph, נתונים מובנים (JSON-LD),
דואג ל-H1 אחד, ובונה sitemap.xml ו-robots.txt.
בטוח להריץ שוב ושוב (מחליף את הבלוק הקודם).
הרצה: python3 tools/seo/seo_build.py   (תמיד אחרי כל בנייה של עמודים)"""
import json
import re
import subprocess
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
BASE = "https://free-ai.co.il"
SITE_NAME = "Free AI"
OG_IMAGE = BASE + "/assets/images/og-hero.png"
NOINDEX = {"soon"}  # עמודים שלא צריכים להופיע בגוגל (שם הקובץ בלי .html)
LOW = {"privacy", "terms", "accessibility"}

START, END = "<!-- seo -->", "<!-- /seo -->"


def slug(f: Path) -> str:
    return f.stem


def url_of(s: str) -> str:
    return BASE + "/" if s == "index" else f"{BASE}/{s}"


def meta(html, name):
    m = re.search(rf'<meta name="{name}" content="([^"]*)"', html)
    return unescape(m.group(1)) if m else ""


def title_of(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    return unescape(m.group(1).strip()) if m else SITE_NAME


def lastmod(f: Path) -> str:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(f)],
                             cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return out or date.today().isoformat()
    except Exception:
        return date.today().isoformat()


def faqs_of(html):
    """השאלות הנפוצות שמופיעות בעמוד (details/summary), בשביל FAQPage. רק מה שהגולש רואה."""
    clean = lambda x: re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", x))).strip()
    return [(clean(q), clean(a)) for q, a in re.findall(
        r'<details class="card"><summary>(.*?)</summary><p>(.*?)</p></details>', html, re.S)]


def schema(s, title, desc, url, mod, faqs=()):
    org = {"@type": "Organization", "@id": BASE + "/#org", "name": SITE_NAME, "url": BASE + "/",
           "logo": BASE + "/assets/images/logo/logo-footer.png"}
    graph = []
    if s == "index":
        graph += [org, {"@type": "WebSite", "@id": BASE + "/#site", "name": SITE_NAME, "url": BASE + "/",
                        "inLanguage": "he", "publisher": {"@id": BASE + "/#org"}}]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "דף הבית", "item": BASE + "/"}]
    if s.startswith("guide-"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "המדריך", "item": BASE + "/guide-1"})
        graph.append({"@type": "TechArticle", "headline": title.split(" – ")[0], "description": desc,
                      "inLanguage": "he", "url": url, "dateModified": mod, "isAccessibleForFree": True,
                      "author": {"@id": BASE + "/#org"}, "publisher": org, "image": OG_IMAGE})
    elif s.startswith("article-"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "מאמרים", "item": BASE + "/articles"})
        graph.append({"@type": "Article", "headline": title.split(" | ")[0], "description": desc,
                      "inLanguage": "he", "url": url, "dateModified": mod, "isAccessibleForFree": True,
                      "author": {"@id": BASE + "/#org"}, "publisher": org, "image": OG_IMAGE})
    elif s in ("course", "course-lovable"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "קורסים", "item": BASE + "/courses"})
        graph.append({"@type": "Course", "name": "קורס Lovable" if s == "course-lovable" else "קורס Claude Code", "description": desc, "inLanguage": "he",
                      "url": url, "isAccessibleForFree": True, "provider": org,
                      "offers": {"@type": "Offer", "price": 0, "priceCurrency": "ILS", "category": "Free"},
                      "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                                            "courseWorkload": "PT2H"}})
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    if s != "index":
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": title.split(" – ")[0].split(" | ")[0]})
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    return {"@context": "https://schema.org", "@graph": graph}


def fix_h1(html):
    """בעמודים בעיצוב הישן הכותרת הראשית היא div – הופכים אותה ל-h1."""
    if "<h1" in html:
        return html
    m = re.search(r'<div class="title text-display-2', html)
    if not m:
        return html
    depth, i = 0, m.start()
    for t in re.finditer(r"<(/?)div\b[^>]*>", html[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            a, b = i + t.start(), i + t.end()
            html = html[:a] + "</h1>" + html[b:]
            break
    return html[:m.start()] + '<h1 class="title text-display-2' + html[m.end():]


def block(s, html, mod):
    title, desc, url = title_of(html), meta(html, "description"), url_of(s)
    esc = lambda x: x.replace("&", "&amp;").replace('"', "&quot;")
    lines = [START,
             f'<link rel="canonical" href="{url}">',
             '<meta name="robots" content="noindex, follow">' if s in NOINDEX else
             '<meta name="robots" content="index, follow, max-image-preview:large">',
             f'<meta property="og:type" content="{"article" if s.startswith(("guide-", "article-")) else "website"}">',
             f'<meta property="og:site_name" content="{SITE_NAME}">',
             '<meta property="og:locale" content="he_IL">',
             f'<meta property="og:title" content="{esc(title)}">',
             f'<meta property="og:description" content="{esc(desc)}">',
             f'<meta property="og:url" content="{url}">',
             f'<meta property="og:image" content="{OG_IMAGE}">',
             '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
             '<meta name="twitter:card" content="summary_large_image">',
             '<script type="application/ld+json">' +
             json.dumps(schema(s, title, desc, url, mod, faqs_of(html)), ensure_ascii=False) + "</script>",
             END]
    return "\n    ".join(lines)


def main():
    import sys as _s; _s.path.insert(0, str(Path(__file__).resolve().parents[1] / "site_build"))
    import site_header; site_header.apply_all()  # הדר אחד לכל האתר
    import site_footer; site_footer.apply_all()  # פוטר אחד לכל האתר
    pages, llms = [], []
    for f in sorted(SITE.glob("*.html")):
        s, html = slug(f), f.read_text()
        html = re.sub(rf"\s*{re.escape(START)}.*?{re.escape(END)}", "", html, flags=re.S)
        html = fix_h1(html)
        mod = lastmod(f)
        html = html.replace("</head>", "    " + block(s, html, mod) + "\n</head>", 1)
        f.write_text(html)
        if s not in NOINDEX:
            pages.append((s, mod))
            llms.append((s, title_of(html), meta(html, "description")))
    pri = lambda s: "1.0" if s == "index" else "0.3" if s in LOW else "0.8"
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{url_of(s)}</loc><lastmod>{m}</lastmod><priority>{pri(s)}</priority></url>"
            for s, m in pages]
    (SITE / "sitemap.xml").write_text("\n".join(xml + ["</urlset>", ""]))
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /files/\n\nSitemap: {BASE}/sitemap.xml\n")
    order = lambda x: (x[0] != "index", not x[0].startswith("guide-"), int(x[0][6:]) if x[0].startswith("guide-") else 0, x[0])
    txt = [f"# {SITE_NAME}", "", "> לומדים AI בעברית ובחינם, בלי ידע קודם: קורס Lovable, קורס Claude Code, מדריך כתוב, סקילים ומאמרים.", ""]
    txt += [f"- [{t}]({url_of(s)}): {d}" for s, t, d in sorted(llms, key=order)]
    (SITE / "llms.txt").write_text("\n".join(txt) + "\n")
    print(f"SEO: {len(pages)} pages in sitemap")


if __name__ == "__main__":
    main()
