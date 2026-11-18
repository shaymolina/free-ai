"""בדיקת SEO לכל האתר. מדפיס רשימת בעיות לפי חומרה.
הרצה: python3 tools/seo/seo_audit.py   (אפשר להוסיף --json)"""
import json
import re
import sys
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"


def text(s):
    return unescape(re.sub(r"<[^>]+>", " ", s)).strip()


def main():
    pages = {f.stem: f.read_text() for f in sorted(SITE.glob("*.html"))}
    issues = []  # (חומרה, עמוד, בעיה)
    add = lambda sev, p, msg: issues.append((sev, p, msg))
    titles, descs, inbound = Counter(), Counter(), defaultdict(int)
    sitemap = (SITE / "sitemap.xml").read_text() if (SITE / "sitemap.xml").exists() else ""
    if not sitemap:
        add("קריטי", "-", "אין sitemap.xml")
    if not (SITE / "robots.txt").exists():
        add("קריטי", "-", "אין robots.txt")

    for p, h in pages.items():
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        t = unescape(t.group(1).strip()) if t else ""
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        d = unescape(d.group(1)) if d else ""
        titles[t] += 1
        descs[d] += 1
        if not t:
            add("קריטי", p, "אין כותרת (title)")
        elif not 25 <= len(t) <= 65:
            add("בינוני", p, f"אורך כותרת {len(t)} תווים (מומלץ 25–65)")
        if not d:
            add("קריטי", p, "אין תיאור (meta description)")
        elif not 70 <= len(d) <= 165:
            add("בינוני", p, f"אורך תיאור {len(d)} תווים (מומלץ 70–165)")
        h1 = re.findall(r"<h1\b", h)
        if len(h1) != 1:
            add("גבוה", p, f"{len(h1)} כותרות H1 (צריך בדיוק 1)")
        for tag, sev in (('rel="canonical"', "גבוה"), ('property="og:image"', "בינוני"),
                         ("application/ld+json", "בינוני")):
            if tag not in h:
                add(sev, p, f"חסר {tag}")
        if 'lang="he"' not in h:
            add("גבוה", p, "חסר lang=he")
        for img in re.findall(r"<img\b[^>]*>", h):
            if "alt=" not in img:
                add("נמוך", p, "תמונה בלי alt: " + img[:80])
        words = len(text(re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S)).split())
        if words < 250 and p not in ("privacy", "terms"):
            add("נמוך", p, f"תוכן דל: {words} מילים")
        if p != "index" and f"/{p}<" not in sitemap and sitemap:
            add("גבוה", p, "העמוד לא נמצא ב-sitemap")
        for href in re.findall(r'href="([^"#?:]+)(?:[#?][^"]*)?"', h):
            if href.startswith(("assets/", "files/", "/assets")) or "." in href.rsplit("/", 1)[-1]:
                if href.endswith(".html"):
                    add("בינוני", p, f"קישור עם .html: {href}")
                continue
            target = "index" if href in ("/", "") else href.strip("/")
            if target not in pages:
                add("גבוה", p, f"קישור שבור: {href}")
            elif target != p:
                inbound[target] += 1

    for p in pages:
        if p != "index" and inbound[p] == 0:
            add("גבוה", p, "עמוד יתום: אף עמוד לא מקשר אליו")
    for t, n in titles.items():
        if t and n > 1:
            add("בינוני", "-", f"כותרת כפולה ב-{n} עמודים: {t}")
    for d, n in descs.items():
        if d and n > 1:
            add("בינוני", "-", f"תיאור כפול ב-{n} עמודים: {d[:60]}")

    order = {"קריטי": 0, "גבוה": 1, "בינוני": 2, "נמוך": 3}
    issues = sorted(set(issues), key=lambda i: (order[i[0]], i[1]))
    if "--json" in sys.argv:
        print(json.dumps([dict(severity=s, page=p, issue=m) for s, p, m in issues], ensure_ascii=False, indent=1))
        return
    print(f"עמודים: {len(pages)} | בעיות: {len(issues)}")
    for s, p, m in issues:
        print(f"[{s}] {p}: {m}")


if __name__ == "__main__":
    main()
