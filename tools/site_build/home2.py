"""דף בית 2: המבנה, העיצוב והאנימציות של דף הבית של Mintlify, עם התוכן של Free AI.
המקור: mint_ref/page.html (ה-HTML שלהם אחרי רינדור). כאן מחליפים את התוכן, ו-site/assets/js/m2.js מפעיל את האנימציות."""
import glob, os, re, sys
from bs4 import BeautifulSoup, NavigableString

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "site")
sys.path.insert(0, HERE)
import home_mint  # noqa: E402

def _asset_version():
    """גרסה לפי התוכן של קבצי העיצוב והקוד, כדי שהדפדפן ייקח את החדשים אחרי כל שינוי."""
    import hashlib
    h = hashlib.md5()
    for f in ("css/m2.css", "css/m2-he.css", "css/m2-inner.css", "css/tokens.css", "js/m2.js"):
        h.update(open(os.path.join(os.path.dirname(__file__), "..", "..", "site", "assets", f), "rb").read())
    return h.hexdigest()[:8]


V = _asset_version()
HEAD = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>קורס קלוד קוד בחינם בעברית | Free AI</title>
    <meta name="description" content="קורס קלוד קוד (Claude Code) בחינם ובעברית למתחילים, בלי ידע בתכנות: שיעורי וידאו, מדריך כתוב וסקילים מוכנים, עד אתר שעובד באוויר.">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-Regular.woff2?v=20261117" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-SemiBold.woff2?v=20261117" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="assets/fonts/fonts.css?v=20261119">
    <link rel="stylesheet" href="assets/css/tokens.css?v={v}">
    <link rel="stylesheet" href="assets/css/m2.css?v={v}">
    <link rel="stylesheet" href="assets/css/m2-mock.css?v={v}">
    <link rel="stylesheet" href="assets/css/m2-he.css?v={v}">
    <link rel="shortcut icon" href="assets/images/logo/favicon.svg">
</head>
<body class="overflow-x-hidden">
"""


def frag(html):
    return BeautifulSoup(html, "html.parser")


def put(el, html):
    """מחליף את כל התוכן של אלמנט ב-HTML חדש."""
    el.clear()
    for c in list(frag(html).contents):
        el.append(c)


def icon(name, cls="size-4"):
    return home_mint.icon(name, cls)


def roller(text):
    """מספר שמתגלגל, באותו מבנה של המונה שלהם (עמודת ספרות שזזה למעלה)."""
    out = []
    for ch in text:
        if ch.isdigit():
            digs = "".join(f'<span data-digit="{d}" class="flex h-[1em] shrink-0 items-center justify-center leading-[1em] before:content-[attr(data-digit)]"></span>' for d in range(10))
            out.append(f'<span class="relative inline-flex h-[1em] overflow-hidden leading-[1em]"><span class="flex flex-col transition-transform duration-700 ease-[var(--ease-out-soft)] motion-reduce:transition-none" data-to="{ch}" style="transform:translateY(-{ch}em) translateZ(0)">{digs}</span></span>')
        else:
            out.append(f'<span class="opacity-50">{ch}</span>' if ch in ".," else ch)
    return f'<span class="inline-flex h-[1em] items-center leading-[1em] tabular-nums" dir="ltr" data-roller><span class="sr-only">{text}</span><span class="contents" aria-hidden="true">{"".join(out)}</span></span>'


def counts():
    n_ch = len(glob.glob(os.path.join(SITE, "guide-*.html")))
    arts = []
    for f in sorted(glob.glob(os.path.join(SITE, "article-*.html")), key=os.path.getmtime, reverse=True):
        t = re.search(r"<title>(.*?)</title>", open(f).read()).group(1).split("|")[0].strip()
        arts.append((os.path.basename(f), t))
    return n_ch, arts


# ---------------------------------------------------------------- כותרת עליונה
def do_header(soup):
    h = soup.find("header")
    logo = h.find("a", attrs={"aria-label": "Go to homepage"})
    logo["href"] = "index.html"; logo["aria-label"] = "Free AI, לדף הבית"
    put(logo, '<img src="assets/images/logo/logo.svg" alt="Free AI" style="height:30px;width:auto">')
    nav = [("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]
    for li, (href, txt) in zip(h.find("ul").find_all("li", recursive=False), nav):
        b = li.find(["button", "a"])
        a = soup.new_tag("a", href=href); a["class"] = b["class"]; a.string = txt
        b.replace_with(a)
    acts = h.find("div", class_="gap-1.5", recursive=True)
    for a in h.find_all("a"):
        if a.get("href") == "https://app.mintlify.com":
            a["href"] = "guide-1.html"; put(a, "למדריך הכתוב")
        elif a.get("href") == "/contact/sales":
            a["href"] = "service.html"; put(a, "התחל ללמוד")
    vp = h.find("div", class_="top-full")
    if vp: vp.decompose()


# ---------------------------------------------------------------- פתיחה
def do_hero(sec, n_ch):
    cv = sec.find("canvas"); cv["data-rib"] = "hero"; cv["data-flip"] = "1"; cv["aria-hidden"] = "true"
    sec.find("a", href="/data").decompose()  # בלי התגית מעל הכותרת
    h1 = sec.find("h1"); put(h1, "קורס קלוד קוד בחינם ובעברית"); h1["class"] = h1.get("class", []) + ["m2-h1"]
    p = h1.find_next("p")
    put(p, 'קורס Claude Code למתחילים, בלי ידע בתכנות. <span class="font-medium text-text-main">שיעורי וידאו</span>, <span class="font-medium text-text-main">מדריך כתוב</span> ו<span class="font-medium text-text-main">סקילים</span>.')
    a1 = sec.find("a", href="https://app.mintlify.com/signup"); a1["href"] = "service.html"
    a1.contents[0].replace_with("להתחיל ללמוד בחינם")
    a2 = sec.find("a", href="https://app.mintlify.com/api/auth/google/discovery"); a2["href"] = "guide-1.html"
    put(a2, icon("book", "size-4 text-brand") + "למדריך הכתוב")
    a2.find_parent("div").find_next_sibling("div").decompose()  # בלי "מה צריך כדי להתחיל"
    box = sec.find(attrs={"aria-label": "Mintlify documentation preview"})
    box["aria-label"] = "המדריך הכתוב של Free AI"
    imgs = box.find_all("img")
    # תצוגה חיה של העמוד הראשון במדריך (לא צילום), כך שכל שינוי במדריך מופיע כאן לבד
    live = BeautifulSoup(
        '<iframe class="m2-live" src="guide-1.html" title="המדריך הכתוב: פרק 1" tabindex="-1" aria-hidden="true" scrolling="no"></iframe>'
        '<span class="m2-live-fade" aria-hidden="true"></span>'
        '<script>(function(){var f=document.querySelector(".m2-live");if(!f)return;var W=1200;'
        'function fit(){var w=f.parentNode.clientWidth;f.style.transform="scale("+(w/W)+")"}'
        'fit();addEventListener("resize",fit);'
        'f.addEventListener("load",function(){try{var d=f.contentDocument;d.documentElement.style.overflow="hidden";d.documentElement.classList.remove("dark");'
        'd.querySelectorAll("a,button,input").forEach(function(e){e.tabIndex=-1})}catch(e){}})})()</script>', "html.parser")
    imgs[0].replace_with(live)
    imgs[1].decompose()


def soup_tag(node, name, **attrs):
    s = BeautifulSoup("", "html.parser")
    return s.new_tag(name, attrs=attrs)


# ---------------------------------------------------------------- כלים + פס מספרים
# כל כלי: שם, קישור, והלוגו האמיתי (סימן + שם כמו שהחברה מציירת אותו). לסקילים, לקונקטורים ולפלאגינים אין לוגו משלהם, אז הם מקבלים את הסימן של קלוד.
TOOLS = [("Claude", "guide-3.html", ["claude-mark.svg", "claude-text.svg"]),
         ("Claude Code", "guide-4.html", ["claudecode-mark.svg", "claudecode-text.svg"]),
         ("Skills", "guide-14.html", ["claude-mark.svg", None]),
         ("Connectors", "guide-13.html", ["claude-mark.svg", None]),
         ("GitHub", "guide-5.html", ["github-mark.svg", "github-text.svg"]),
         ("4CODE", "guide-18.html", ["4code-logo.png"]),
         ("Supabase", "guide-13.html", ["supabase-logo.svg"]),
         ("Cloudflare", "guide-18.html", ["cloudflare-mark.svg", "cloudflare-text.svg"])]


def do_tools(sec, n_ch, n_art):
    h2 = sec.find("h2"); put(h2, f'<strong class="font-medium text-text-main">{len(TOOLS)} הכלים</strong> שהופכים אדם אחד לצוות שלם.')
    a = h2.find_next("a"); a["href"] = "guide-1.html"; a.contents[0].replace_with("למדריך המלא")
    cards = sec.find_all("div", class_="group/card")
    cards[0].parent["class"] = cards[0].parent["class"] + ["m2-tools"]
    while len(cards) < len(TOOLS):  # שורה עליונה: 4 כלים של קלוד, שורה תחתונה: 4 כלים חיצוניים
        c = copy.copy(cards[-1]); cards[-1].insert_after(c); cards.append(c)
    for card, (name, href, ic) in zip(cards, TOOLS):
        logo = card.find_all("span", recursive=False)[1]
        parts = "".join(f'<img class="{("tl-mark" if k == 0 and len(ic) > 1 else "tl-word")}" src="assets/images/brands/{f}" alt="">' if f else f'<span class="tl-name">{name}</span>' for k, f in enumerate(ic))
        put(logo, f'<span class="tool-logo" dir="ltr" data-tool="{name}">{parts}</span>')
        for x in card.find_all("span", class_="sr-only", recursive=False): x.decompose()
        link = card.find("a", recursive=False)
        arrow = '<span class="pointer-events-none absolute bottom-3 left-3 opacity-0 transition-opacity duration-150 ease-out group-hover/card:opacity-100">' + icon("chev-l", "text-text-sub size-4") + '</span>'
        if link:
            link["href"] = href; link["aria-label"] = name
        else:
            link = frag(f'<a class="absolute inset-0 rounded-[6px] focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand" href="{href}" aria-label="{name}">{arrow}</a>')
            card.append(link)
    tk = sec.find(string=re.compile("Agents at work today")).parent
    tk.string = "הקורס במספרים"
    items = [("פרקים במדריך", str(n_ch)), ("שיעורי וידאו", "8"), ("מאמרים", str(n_art)), ("מחיר", "₪0"), ("בעברית", "100%")]
    rows = sec.find("div", attrs={"aria-label": "Live stats, focus to pause"})
    rows["aria-label"] = "הקורס במספרים"; rows["data-ticker"] = ""
    rows["class"] = ["tk-view"]
    one = "".join(f'<span class="tk-item"><b dir="ltr">{val}</b>{lab}</span>' for lab, val in items)
    group = f'<div class="tk-group">{one}{one}</div>'
    put(rows, f'<div class="tk-track">{group}' + f'<div class="tk-group" aria-hidden="true">{one}{one}</div>' * 3 + '</div>')


# ---------------------------------------------------------------- כותרת מקטע (קו ירוק + שתי שורות + כפתור)
def do_head(sec, title, sub, href=None, label=None):
    h2 = sec.find("h2")
    put(h2, f'<span class="m2-ht">{title}</span><span class="m2-hs block text-foreground-tertiary">{sub}</span>')
    if href:
        a = sec.find("header").find("a")
        a["href"] = href; a.contents[0].replace_with(label)


def carousel_buttons(sec, what):
    for b in sec.find("header").find_all("button"):
        b["aria-label"] = ("הקודם: " if "Previous" in b["aria-label"] else "הבא: ") + what
        b["data-car"] = "-1" if b["aria-label"].startswith("הקודם") else "1"
        svg = b.find("svg"); cl = svg.get("class", [])
        svg["class"] = [c for c in cl if c != "rotate-180"] + ([] if "rotate-180" in cl else ["rotate-180"])


import copy

STORIES = [
    ("#5C1E0F", "אתר לעסק", 'ככה <span class="text-white">הודעה אחת בעברית</span> הופכת לאתר עם גלריה וטופס', [("1", "הודעה בעברית"), ("0", "שורות קוד שאתם כותבים")],
     "article-what-is-claude-code.html", "assets/images/claude/build-site.jpg"),
    ("#4763D6", "גיבוי אוטומטי", 'ככה <span class="text-white">כל הפרויקטים</span> נשמרים לבד בגוגל דרייב, כל לילה', [("03:00", "כל לילה"), ("₪0", "עלות")],
     "article-github-backup.html", "assets/images/guide/backup-1.png"),
    ("#C8553A", "מעלים לאוויר", 'ככה האתר מקבל <span class="text-white">כתובת אמיתית</span> שאפשר לשלוח לכל אחד', [("1", "כתובת לשתף"), ("30", "ימים בחינם עם הקופון")],
     "guide-18.html", "assets/images/guide/claude-map.png"),
    ("#7A3FC4", "סקילים", 'ככה <span class="text-white">יכולת מוכנה</span> נכנסת לקלוד בלחיצה אחת', [("1", "לחיצה להורדה"), ("₪0", "מחיר")],
     "work.html", "assets/images/home2/skills-w.webp"),
]


def do_stories(sec):
    do_head(sec, "מה בונים עם קלוד קוד.", "דוגמאות אמיתיות מהמדריך ומהמאמרים.", "articles.html", "לכל המאמרים")
    carousel_buttons(sec, "דוגמה")
    track = sec.find(attrs={"aria-label": "Enterprise customer stories"})
    track["aria-label"] = "דוגמאות"; track["data-track"] = ""
    cards = track.find_all("div", class_="carousel-card-dim", recursive=False)
    tpl = cards[0]
    for c in cards: c.extract()
    for color, tag, title, nums, href, img in STORIES:
        c = copy.copy(tpl)
        a = c.find("a"); a["href"] = href; a["data-occlude"] = ""
        left = a.find("div")
        left["class"] = [k for k in left["class"] if not k.startswith("bg-[")]; left["style"] = f"background-color:{color}"
        left.find("canvas")["data-carddots"] = ""
        inner = left.find("div")
        inner.find("svg").replace_with(frag(f'<span class="self-start text-[15px]/5 font-semibold tracking-[0.02em] text-white">{tag}</span>'))
        put(inner.find("h3"), f'<span class="text-white/70">{title}</span>')
        for blk, (n, lab) in zip(inner.find("div", class_="mt-8").find_all("div", recursive=False), nums):
            ps = blk.find_all("p"); put(ps[0], f'<span dir="ltr">{n}</span>'); put(ps[1], lab)
        btn = inner.find("span", class_="group"); btn.contents[0].replace_with("לסיפור המלא")
        right = a.find_all("div", recursive=False)[1]
        bg = right.find_all("div", recursive=False)
        bg[0]["style"] = f"background-image:url({img})"
        bg[1]["class"] = [k for k in bg[1]["class"] if not k.startswith("bg-[")]; bg[1]["style"] = f"background-color:{color}"
        track.append(c)
    sec.find("canvas", class_="-z-10")["data-sectiondots"] = ""



# ---------------------------------------------------------------- שישה כרטיסים עם הדגמות
def bento_mocks():
    """ההדגמות הזזות מדף הבית הראשון (home_mint.sec_bento), לפי הסדר."""
    html = home_mint.sec_bento()
    soup = BeautifulSoup(html, "html.parser")
    return [(li.find("h3").get_text(), str(li.find("div", class_="mk"))) for li in soup.find_all("li", class_="bento-c")]


RIVES = [("agent-native-platform-warm3", "agent-native-platform-mobile-warm3"), ("self-updating-knowledge-warm3", None), ("control-who-has-access-warm3", None),
         ("connect-with-your-systems-warm3", None), ("collaborate-with-your-team-and-agents-warm3", None), ("build-on-top-of-your-existing-setup-warm3", "build-on-top-of-your-existing-setup-mobile-warm3")]


BENTO_TITLES = ["כותבים בעברית, קלוד קוד בונה",
                "מתחילים מאפס, בלי ידע ובחינם",
                "אתם מחליטים, קלוד עושה את העבודה",
                "מתחברים לשירותים",
                "עובדים כבר על קורס סוכנים. כן, גם בחינם.",
                "רעיון בבוקר, אתר באוויר בערב"]


def do_bento(sec):
    """הכרטיסים המקוריים שלהם עם אנימציות ה-Rive המקוריות, והכותרות בעברית."""
    do_head(sec, "כל מה שצריך לאתר הראשון.", "בלי לכתוב שורת קוד.", "service.html", "התחל ללמוד")
    titles = BENTO_TITLES
    for art, title, (src, mob) in zip(sec.find_all("article"), titles, RIVES):
        box = art.find("div", class_="absolute")
        attrs = f' data-rive="assets/rive/{src}.riv"' + (f' data-rive-m="assets/rive/{mob}.riv"' if mob else "")
        put(box, f'<canvas aria-hidden="true" class="absolute inset-0 size-full"{attrs}></canvas>')
        put(art.find("h3"), title)


def mock_css():
    """הכללים של ההדגמות מתוך home.css, לקובץ נפרד של דף 2."""
    lines = open(os.path.join(SITE, "assets", "css", "home.css")).read().splitlines()
    keep = [l for l in lines if l.startswith("@keyframes")]
    a = next(i for i, l in enumerate(lines) if l.startswith(".mk {"))
    b = max(i for i, l in enumerate(lines) if l.startswith(".mk-"))
    while b + 1 < len(lines) and lines[b + 1].startswith(" "):
        b += 1
    keep += [l for l in lines[a:b + 1] if not l.startswith(".bento-c")]
    keep.append(".mk .ico { width: 16px; height: 16px; flex-shrink: 0; }")
    keep.append("article:hover .mk { transform: translate3d(0, -4px, 0) scale(1.015); }")
    open(os.path.join(SITE, "assets", "css", "m2-mock.css"), "w").write("/* נוצר אוטומטית מ-home.css על ידי home2.py */\n" + "\n".join(keep) + "\n")



# ---------------------------------------------------------------- גל + מספרים
# אייקונים מ-Lucide (רישיון ISC): צוות, קוביות בנייה, מתנה.
STAT_ICONS = {
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "blocks": '<rect width="7" height="7" x="14" y="3" rx="1"/><path d="M10 21V8a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1H3"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
}

def do_scale(sec, n_ch):
    do_head(sec, "קלוד קוד כבר משנה את הדרך שבה אנשים עובדים.", "הגיע הזמן שגם אתם תדעו לעבוד איתו.", "guide-1.html", "לפרק הראשון")
    cv = sec.find("canvas"); cv["data-rib"] = "wave"; cv["data-flip"] = "1"; cv["aria-hidden"] = "true"
    stats = [("1", "אדם, היכולת של צוות", "users"), ("∞", "דברים שתוכלו לבנות", "blocks"), ("₪0", "לקורס. למדריכים. לכל הידע", "gift")]
    grid = sec.find_all("div", class_="gap-6")[0].parent  # בעברית הריפוד צריך להיות בצד של הקו המפריד
    grid["class"] = grid["class"] + ["m2-stats"]
    for blk, (n, lab, ic) in zip(sec.find_all("div", class_="gap-6"), stats):
        ps = blk.find_all("p"); put(ps[0], f'<span dir="ltr">{n}</span>'); put(ps[1], lab)
        blk.find("svg").replace_with(frag(f'<svg aria-hidden="true" class="shrink-0 select-none size-5 text-foreground-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{STAT_ICONS[ic]}</svg>'))


# ---------------------------------------------------------------- כרטיסים צבעוניים
STARTS = [("הקורס", "8 שיעורי וידאו, לפי הסדר.", "service.html", "לקורס"),
          ("המדריך", "{n} פרקים לקריאה, צעד אחרי צעד.", "guide-1.html", "למדריך"),
          ("סקילים", "יכולות מוכנות לקלוד, להורדה בחינם.", "work.html", "לסקילים"),
          ("מאמרים", "מדריכים קצרים שאפשר לעשות היום.", "articles.html", "למאמרים"),
          ("הפרק הראשון", "שלושה דברים להכין, ואפשר לצאת לדרך.", "guide-1.html", "לפרק 1")]


# אייקונים לכרטיסי הלמידה: Phosphor Icons (duotone), רישיון MIT
START_ICONS = {
    "play": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 256\" fill=\"currentColor\"><path d=\"M228.23,134.69,84.15,222.81A8,8,0,0,1,72,216.12V39.88a8,8,0,0,1,12.15-6.69l144.08,88.12A7.82,7.82,0,0,1,228.23,134.69Z\" opacity=\"0.2\"/><path d=\"M232.4,114.49,88.32,26.35a16,16,0,0,0-16.2-.3A15.86,15.86,0,0,0,64,39.87V216.13A15.94,15.94,0,0,0,80,232a16.07,16.07,0,0,0,8.36-2.35L232.4,141.51a15.81,15.81,0,0,0,0-27ZM80,215.94V40l143.83,88Z\"/></svg>",
    "book-open-text": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 256\" fill=\"currentColor\"><path d=\"M232,56V200H160a32,32,0,0,0-32,32V88a32,32,0,0,1,32-32Z\" opacity=\"0.2\"/><path d=\"M232,48H160a40,40,0,0,0-32,16A40,40,0,0,0,96,48H24a8,8,0,0,0-8,8V200a8,8,0,0,0,8,8H96a24,24,0,0,1,24,24,8,8,0,0,0,16,0,24,24,0,0,1,24-24h72a8,8,0,0,0,8-8V56A8,8,0,0,0,232,48ZM96,192H32V64H96a24,24,0,0,1,24,24V200A39.81,39.81,0,0,0,96,192Zm128,0H160a39.81,39.81,0,0,0-24,8V88a24,24,0,0,1,24-24h64ZM160,88h40a8,8,0,0,1,0,16H160a8,8,0,0,1,0-16Zm48,40a8,8,0,0,1-8,8H160a8,8,0,0,1,0-16h40A8,8,0,0,1,208,128Zm0,32a8,8,0,0,1-8,8H160a8,8,0,0,1,0-16h40A8,8,0,0,1,208,160Z\"/></svg>",
    "sparkle": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 256\" fill=\"currentColor\"><path d=\"M194.82,151.43l-55.09,20.3-20.3,55.09a7.92,7.92,0,0,1-14.86,0l-20.3-55.09-55.09-20.3a7.92,7.92,0,0,1,0-14.86l55.09-20.3,20.3-55.09a7.92,7.92,0,0,1,14.86,0l20.3,55.09,55.09,20.3A7.92,7.92,0,0,1,194.82,151.43Z\" opacity=\"0.2\"/><path d=\"M197.58,129.06,146,110l-19-51.62a15.92,15.92,0,0,0-29.88,0L78,110l-51.62,19a15.92,15.92,0,0,0,0,29.88L78,178l19,51.62a15.92,15.92,0,0,0,29.88,0L146,178l51.62-19a15.92,15.92,0,0,0,0-29.88ZM137,164.22a8,8,0,0,0-4.74,4.74L112,223.85,91.78,169A8,8,0,0,0,87,164.22L32.15,144,87,123.78A8,8,0,0,0,91.78,119L112,64.15,132.22,119a8,8,0,0,0,4.74,4.74L191.85,144ZM144,40a8,8,0,0,1,8-8h16V16a8,8,0,0,1,16,0V32h16a8,8,0,0,1,0,16H184V64a8,8,0,0,1-16,0V48H152A8,8,0,0,1,144,40ZM248,88a8,8,0,0,1-8,8h-8v8a8,8,0,0,1-16,0V96h-8a8,8,0,0,1,0-16h8V72a8,8,0,0,1,16,0v8h8A8,8,0,0,1,248,88Z\"/></svg>",
    "article": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 256\" fill=\"currentColor\"><path d=\"M224,56V200a8,8,0,0,1-8,8H40a8,8,0,0,1-8-8V56a8,8,0,0,1,8-8H216A8,8,0,0,1,224,56Z\" opacity=\"0.2\"/><path d=\"M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,160H40V56H216V200ZM184,96a8,8,0,0,1-8,8H80a8,8,0,0,1,0-16h96A8,8,0,0,1,184,96Zm0,32a8,8,0,0,1-8,8H80a8,8,0,0,1,0-16h96A8,8,0,0,1,184,128Zm0,32a8,8,0,0,1-8,8H80a8,8,0,0,1,0-16h96A8,8,0,0,1,184,160Z\"/></svg>",
    "rocket-launch": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 256\" fill=\"currentColor\"><path d=\"M184,120v61.65a8,8,0,0,1-2.34,5.65l-34.35,34.35a8,8,0,0,1-13.57-4.53L128,176ZM136,72H74.35a8,8,0,0,0-5.65,2.34L34.35,108.69a8,8,0,0,0,4.53,13.57L80,128ZM40,216c37.65,0,50.69-19.69,54.56-28.18L68.18,161.44C59.69,165.31,40,178.35,40,216Z\" opacity=\"0.2\"/><path d=\"M223.85,47.12a16,16,0,0,0-15-15c-12.58-.75-44.73.4-71.41,27.07L132.69,64H74.36A15.91,15.91,0,0,0,63,68.68L28.7,103a16,16,0,0,0,9.07,27.16l38.47,5.37,44.21,44.21,5.37,38.49a15.94,15.94,0,0,0,10.78,12.92,16.11,16.11,0,0,0,5.1.83A15.91,15.91,0,0,0,153,227.3L187.32,193A15.91,15.91,0,0,0,192,181.64V123.31l4.77-4.77C223.45,91.86,224.6,59.71,223.85,47.12ZM74.36,80h42.33L77.16,119.52,40,114.34Zm74.41-9.45a76.65,76.65,0,0,1,59.11-22.47,76.46,76.46,0,0,1-22.42,59.16L128,164.68,91.32,128ZM176,181.64,141.67,216l-5.19-37.17L176,139.31Zm-74.16,9.5C97.34,201,82.29,224,40,224a8,8,0,0,1-8-8c0-42.29,23-57.34,32.86-61.85a8,8,0,0,1,6.64,14.56c-6.43,2.93-20.62,12.36-23.12,38.91,26.55-2.5,36-16.69,38.91-23.12a8,8,0,1,1,14.56,6.64Z\"/></svg>"
}
START_ICON_NAMES = ["play", "book-open-text", "sparkle", "article", "rocket-launch"]


def do_starts(sec, n_ch):
    do_head(sec, "קורס, מדריך, סקילים, מאמרים ועוד.", "הכול כאן, בחינם.")
    sec.find("header").find("a").decompose()  # בלי כפתור "התחל ללמוד" ליד החצים
    carousel_buttons(sec, "דרך להתחיל")
    track = sec.find(attrs={"aria-label": "Startup customer stories"})
    track["aria-label"] = "מאיפה מתחילים"; track["data-track"] = ""
    cards = track.find_all("div", recursive=False)
    tpl = cards[0]
    for c in cards: c.extract()
    for k, (t, d, href, go) in enumerate(STARTS):
        c = copy.copy(tpl)
        a = c.find("a"); a["href"] = href; a["data-occlude"] = ""
        imgs = a.find_all("img")
        imgs[0]["src"] = f"assets/images/home2/learn-{k}.webp"; imgs[0]["alt"] = ""
        for x in ("srcset", "sizes"): imgs[0].attrs.pop(x, None)
        imgs[1].decompose()
        ic = START_ICONS[START_ICON_NAMES[k]].replace("<svg ", '<svg aria-hidden="true" ', 1)
        imgs[0].parent.append(frag(f'<span class="m2-card-ic">{ic}</span>'))
        put(a.find("p"), f'<span class="font-medium text-text-main">{t}</span> {d.format(n=n_ch)}')
        sp = a.find("span", class_="mt-auto"); arrow = sp.find("svg")
        put(sp, go); sp.append(arrow)
        track.append(c)
    sec.find("canvas", class_="-z-10")["data-sectiondots"] = ""


# ---------------------------------------------------------------- בקשות לדוגמה (במקום המלצות)
def do_prompts(sec):
    do_head(sec, "מה כותבים לקלוד קוד.", "הודעות אמיתיות, בעברית רגילה.", "guide-7.html", "איך כותבים בקשה טובה")
    btn = sec.find("button"); btn.string = "עצירת הדוגמאות"; btn["data-pause"] = ""; btn["aria-pressed"] = "false"
    figs = sec.find_all("figure")
    grid = figs[0].parent; grid["data-rotate"] = ""
    for fig, (ic, name, role, quote) in zip(figs, home_mint.PROMPTS):
        box = fig.find("div", class_="size-12")
        put(box, icon(ic, "size-6 text-text-main"))
        box["class"] = [k for k in box["class"] if not k.startswith("bg-")] + ["bg-background-soft"]
        put(fig.find("figcaption"), name)
        put(fig.find("figcaption").find_next_sibling("span"), role)
        put(fig.find("blockquote"), f'"{quote}"')
    import json
    pool = json.dumps([[icon(ic, "size-6 text-text-main"), n, r, f'"{q}"'] for ic, n, r, q in home_mint.PROMPTS], ensure_ascii=False)
    grid.append(frag(f'<script type="application/json" data-pool>{pool}</script>'))


# ---------------------------------------------------------------- מאמרים אחרונים
def do_posts(sec, arts):
    do_head(sec, "מאמרים אחרונים.", "קצרים, ואפשר לעשות אותם היום.", "articles.html", "לכל המאמרים")
    items = arts[:2] + [("articles.html", "כל המאמרים במקום אחד")]
    for a in sec.find_all("a", href=re.compile("^/blog/")):
        k = [x["href"] for x in a.find_parent("div").find_all("a", recursive=False)].index(a["href"]) % 3
        href, title = items[k]
        a["href"] = href
        img = a.find("img"); img["src"] = f"assets/images/home2/post-{k}{'-w' if k in (0, 1) else ''}.webp"; img["alt"] = ""
        for x in ("srcset", "sizes"): img.attrs.pop(x, None)
        spans = a.find("div", class_="items-center").find_all("span", recursive=False)
        put(spans[0], "מאמר" if k < 2 else "מאמרים"); put(spans[1], "נובמבר 2026" if k < 2 else "")
        put(a.find("p"), title)
    for b in sec.find("header").find_all("button"): b.decompose()


# ---------------------------------------------------------------- פס סיום
def do_cta(sec):
    sec.find("svg")["data-flow"] = ""
    h2 = sec.find("h2"); put(h2, "קורס קלוד קוד, בחינם ובעברית")
    links = h2.find_next("div").find_all("a")
    links[0]["href"] = "guide-1.html"; put(links[0], "למדריך הכתוב")
    links[1]["href"] = "service.html"; links[1].contents[0].replace_with("התחל ללמוד")


# ---------------------------------------------------------------- שאלות נפוצות
# השאלות שאנשים באמת מחפשים בגוגל (docs/seo/longtail-2026-11-18.md). המחירים נבדקו ב-claude.com/pricing.
FAQ = [("מה זה קלוד קוד?", "כלי של Anthropic שבונה אתרים, אפליקציות ומערכות לפי מה שכותבים לו בשפה רגילה.", ("article-what-is-claude-code.html", "הסבר פשוט על קלוד קוד")),
       ("האם קלוד קוד בחינם?", "קלוד קוד עצמו דורש מנוי בתשלום לקלוד, החל מ-Pro. הקורס שלנו, המדריך וכל הידע כאן בחינם.", None),
       ("כמה עולה קלוד קוד לחודש?", "המנוי הזול שכולל אותו הוא Pro: ‏20$ לחודש, או 17$ לחודש בתשלום שנתי. יש גם Max ב-100$.", ("article-claude-code-price.html", "כל המחירים")),
       ("האם קלוד קוד עובד בעברית?", "כן. כותבים לו בעברית רגילה, והוא בונה גם אתרים בעברית.", None),
       ("איך מתקינים קלוד קוד על המחשב?", "מורידים את אפליקציית Claude למחשב, ל-Mac או ל-Windows, וקלוד קוד נמצא בתוכה. אפשר לעבוד איתו גם בדפדפן.", ("guide-4.html", "מדריך ההתקנה")),
       ("מה ההבדל בין קלוד לקלוד קוד?", "קלוד משוחח איתכם ועונה. קלוד קוד עובד על הקבצים שלכם ובונה בפועל.", ("guide-2.html", "ההבדל בפירוט")),
       ("צריך לדעת לתכנת?", "לא. הקורס מתחיל מאפס ומתאים לכל רמה.", ("guide-1.html", "לפרק הראשון")),
       ("איך מתחילים ללמוד קלוד קוד?", "נכנסים לקורס: 8 שיעורי וידאו ומדריך כתוב בעברית, בקצב שלכם.", ("service.html", "לקורס"))]


def do_faq(sec):
    put(sec.find("h2"), "שאלות נפוצות")
    items = sec.find_all("div", attrs={"data-slot": "accordion-item"})
    while len(items) < len(FAQ):
        c = copy.copy(items[-1]); items[-1].insert_after(c); items.append(c)
    for k, it in enumerate(items):
        if k >= len(FAQ):
            it.decompose(); continue
        q, a, link = FAQ[k]
        b = it.find("button"); svg = b.find("svg"); put(b, q); b.append(svg)
        b["data-faq"] = ""
        panel = it.find("div", attrs={"data-slot": "accordion-content"})
        b["id"] = f"faq-q{k}"; panel["id"] = f"faq-a{k}"; b["aria-controls"] = panel["id"]; panel["aria-labelledby"] = b["id"]
        body = it.find("div", attrs={"data-slot": "accordion-content"}).find("div")
        put(body, f"<p>{a}</p>" + (f'<p><a class="faq-link" href="{link[0]}">{link[1]}</a></p>' if link else ""))


# ---------------------------------------------------------------- פוטר
def do_footer(soup, arts):
    f = soup.find("footer")
    f.find("canvas")["data-sectiondots"] = ""; f.find("canvas")["data-clip"] = ""; f.find("canvas")["data-feather"] = ".06"
    logo = f.find("a", attrs={"aria-label": "Go to homepage"}); logo["href"] = "index.html"; logo["aria-label"] = "Free AI, לדף הבית"
    put(logo, '<img src="assets/images/logo/logo.svg" alt="Free AI" style="height:34px;width:auto">')
    for st in f.find_all("a", href="https://status.mintlify.com/"):
        st["href"] = "mailto:hello@free-ai.co.il"; st.attrs.pop("target", None); st.attrs.pop("rel", None)
        st.find_all("span", recursive=False)[0].decompose()
        st.find("span").string = "hello@free-ai.co.il"
    cols = [("לומדים", [("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]),
            ("המדריך", [("guide-1.html", "לפני שמתחילים"), ("guide-3.html", "פותחים חשבון קלוד"), ("guide-5.html", "פותחים GitHub"), ("guide-7.html", "היכרות ראשונה עם קלוד"), ("guide-18.html", "מעלים לאוויר")]),
            ("מאמרים", [(h, t.split(" (")[0].split(" של ")[0].rstrip("?") + ("?" if "?" in t else "")) for h, t in arts[:4]]),
            ("כלים", [("guide-4.html", "Claude Code"), ("guide-13.html", "Connectors"), ("guide-14.html", "Skills"), ("guide-18.html", "4CODE")]),
            ("מידע", [("privacy.html", "פרטיות"), ("terms.html", "תנאי שימוש")])]
    for div, (h, links) in zip(f.find("div", class_="lg:grid-cols-5").find_all("div", recursive=False), cols):
        div.find("h3").string = h
        ul = div.find("ul"); tpl = ul.find("a"); cls = tpl["class"]; ul.clear()
        for href, t in links:
            ul.append(frag(f'<li><a class="{" ".join(cls)}" href="{href}">{t}</a></li>'))
    bottom = f.find(attrs={"aria-label": "Theme switcher"}).find_parent("div", class_="justify-between")
    put(bottom, '<span class="text-sm/5 text-neutral-500">© 2026 Free AI. כל הזכויות שמורות.</span><a class="text-sm/5 font-medium text-text-main hover:text-brand" href="#top" data-totop>חזרה למעלה ↑</a>')



def do_mobile_header(soup):
    h = soup.find_all("header")[1]
    logo = h.find("a", attrs={"aria-label": "Go to homepage"}); logo["href"] = "index.html"; logo["aria-label"] = "Free AI, לדף הבית"
    put(logo, '<img src="assets/images/logo/logo.svg" alt="Free AI" style="height:30px;width:auto">')
    b = h.find("button"); b["aria-label"] = "תפריט"; b["aria-controls"] = "m-menu"; b["data-menu"] = ""
    b["class"] = [c if c != "-mr-1.5" else "-ml-1.5" for c in b["class"]]
    links = [("index.html", "דף הבית"), ("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]
    lis = "".join(f'<li><a class="flex h-12 items-center border-b border-border-line text-base/6 font-medium text-text-main" href="{a}">{t}</a></li>' for a, t in links)
    h.append(frag(f'<nav id="m-menu" hidden aria-label="תפריט ראשי" class="absolute inset-x-0 top-16 z-[105] bg-neutral-0 px-5 pb-6 shadow-[0_12px_24px_-12px_rgba(0,0,0,.15)]"><ul>{lis}</ul>'
                  f'<a class="mt-5 flex h-11 items-center justify-center rounded-[4px] bg-neutral-900 text-sm/4 font-medium text-white" href="service.html">התחל ללמוד</a></nav>'))


SHOW_PROMPTS = False  # "מה כותבים לקלוד קוד": מוסתר כרגע, נחזיר בהמשך
SHOW_POSTS = False    # "מאמרים אחרונים": מוסתר כרגע


def transform(s):
    n_ch, arts = counts()
    soup = BeautifulSoup(s, "html.parser")
    do_header(soup)
    do_mobile_header(soup)
    secs = [x for x in soup.find("main").find_all("section") if x.find_parent("section") is None]
    do_hero(secs[0], n_ch)
    do_tools(secs[1], n_ch, len(arts))
    do_bento(secs[2])
    secs[3].decompose()  # בלי "מה בונים עם קלוד קוד"
    do_scale(secs[4], n_ch)
    do_starts(secs[5], n_ch)
    do_prompts(secs[6]) if SHOW_PROMPTS else secs[6].decompose()
    do_posts(secs[7], arts) if SHOW_POSTS else secs[7].decompose()
    do_cta(secs[8])
    do_faq(secs[9])
    do_footer(soup, arts)
    soup.find("header")["id"] = "top"
    soup.find_all("header")[1]["id"] = "top-m"
    return str(soup)


def build():
    src = open(os.path.join(HERE, "mint_ref", "page.html")).read()
    mock_css()
    out = HEAD.format(v=V) + transform(src) + f'\n<script src="assets/js/m2.js?v={V}" defer></script>\n</body>\n</html>\n'
    from clean_urls import clean
    open(os.path.join(SITE, "index.html"), "w").write(clean(out))  # זה עמוד הבית הראשי
    old = os.path.join(SITE, "home-2.html")
    if os.path.exists(old): os.remove(old)
    print("index.html (home-2) done")


if __name__ == "__main__":
    build()


# ---------------------------------------------------------------- עמודים פנימיים (מאמרים) עם הפתיחה של דף הבית
INNER_HEAD = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="author" content="Free AI">
    <meta name="description" content="{desc}">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-Regular.woff2?v=20261117" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="assets/fonts/files/kobi/Kobi-SemiBold.woff2?v=20261117" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="assets/fonts/fonts.css?v=20261119">
    <style>@layer properties, theme, base, legacy, components, utilities;</style>
    <link rel="stylesheet" href="assets/css/tokens.css?v={v}">
    <link rel="stylesheet" href="assets/css/m2.css?v={v}">
    <link rel="stylesheet" href="assets/css/m2-mock.css?v={v}">
    <link rel="stylesheet" href="assets/css/m2-he.css?v={v}">
    <style>@import url("assets/css/compact.css?v={lv}") layer(legacy); @import url("assets/css/home.css?v={lv}") layer(legacy);</style>
    <link rel="stylesheet" href="assets/css/m2-inner.css?v={v}">
    <link rel="shortcut icon" href="assets/images/logo/favicon.svg">
</head>
<body class="overflow-x-hidden m2-inner">
"""


def inner_page(title, desc, chip, h1, lead, visual, main_html, btn2=("articles.html", "לכל המאמרים", "file"), script="", legacy_v="1", live=None):
    """עמוד פנימי: כותרת עליונה, פתיחה (חוטים מונפשים, כותרת עבה, כפתורים, איור במסגרת) ופוטר כמו בדף הבית.
    main_html: התוכן שמתחת לפתיחה (תגית <main> שלמה)."""
    _, arts = counts()
    soup = BeautifulSoup(open(os.path.join(HERE, "mint_ref", "page.html")).read(), "html.parser")
    do_header(soup)
    do_mobile_header(soup)
    m = soup.find("main")
    secs = [x for x in m.find_all("section") if x.find_parent("section") is None]
    sec = secs[0]
    for x in secs[1:]:
        x.decompose()
    cv = sec.find("canvas"); cv["data-rib"] = "hero"; cv["data-flip"] = "1"; cv["aria-hidden"] = "true"
    tag = sec.find("a", href="/data")
    if not chip:
        tag.decompose()
    else:
        tag.replace_with(frag(f'<span class="m2-chip inline-flex w-fit items-center gap-2 rounded-[2px] border border-border-sub bg-background-main px-2.5 py-1 text-xs/4 font-medium tracking-[0.02em] text-text-sub"><i></i>{chip}</span>'))
    h = sec.find("h1"); put(h, h1); h["class"] = h.get("class", []) + ["m2-h1", "m2-h1-wrap"]
    put(h.find_next("p"), lead)
    a1 = sec.find("a", href="https://app.mintlify.com/signup"); a1["href"] = "service.html"
    a1.contents[0].replace_with("להתחיל ללמוד בחינם")
    for k in ("target", "rel"): a1.attrs.pop(k, None)
    a2 = sec.find("a", href="https://app.mintlify.com/api/auth/google/discovery"); a2["href"] = btn2[0]
    for k in ("target", "rel", "referrerpolicy"): a2.attrs.pop(k, None)
    put(a2, icon(btn2[2], "size-4 text-brand") + btn2[1])
    a2.find_parent("div").find_next_sibling("div").decompose()
    box = sec.find(attrs={"aria-label": "Mintlify documentation preview"})
    box["aria-label"] = h1; box["class"] = [c for c in box["class"] if not c.startswith("aspect-")] + ["m2-vis-box"]
    for img in box.find_all("img")[1:]:
        img.decompose()
    if live:  # תצוגה חיה של עמוד באתר, כמו המדריך בדף הבית
        box["class"] = [c for c in box["class"] if c != "m2-vis-box"] + ["aspect-[1080/656]"]
        box.find("img").replace_with(frag(
            f'<iframe class="m2-live" src="{live}" title="{h1}" tabindex="-1" aria-hidden="true" scrolling="no"></iframe>'
            '<span class="m2-live-fade" aria-hidden="true"></span>'
            '<script>(function(){var f=document.querySelector(".m2-live");if(!f)return;var W=1200;'
            'function fit(){var w=f.parentNode.clientWidth;f.style.transform="scale("+(w/W)+")"}'
            'fit();addEventListener("resize",fit);'
            'f.addEventListener("load",function(){try{var d=f.contentDocument;d.documentElement.style.overflow="hidden";d.documentElement.classList.remove("dark");'
            'd.querySelectorAll("a,button,input").forEach(function(e){e.tabIndex=-1})}catch(e){}})})()</script>'))
    else:
        box.find("img").replace_with(frag(f'<div class="m2-vis">{visual}</div>'))
    m.name = "div"; m["class"] = ["overflow-x-clip", "m2-top"]
    m.insert_after(frag(main_html))
    do_footer(soup, arts)
    soup.find("header")["id"] = "top"
    soup.find_all("header")[1]["id"] = "top-m"
    out = (INNER_HEAD.format(title=title, desc=desc, v=V, lv=legacy_v) + str(soup)
           + f'\n<script src="assets/js/m2.js?v={V}" defer></script>\n{script}\n</body>\n</html>\n')
    from clean_urls import clean
    return clean(out)


# ---------------------------------------------------------------- רשימת המאמרים: הכרטיסים הצבעוניים של "סיפורים" מדף הבית
# לכל מאמר: צבע, כותרת (החלק החשוב בלבן), שני מספרים, תמונה
ARTICLE_CARDS = {
    "article-what-is-claude-code.html": ("#5C1E0F", 'מה זה <span class="text-white">קלוד קוד</span>, ואיך הודעה בעברית הופכת לאתר',
                                         [("1", "הודעה בעברית"), ("0", "שורות קוד שאתם כותבים")], "assets/images/claude/build-site.jpg"),
    "article-github-backup.html": ("#4763D6", '<span class="text-white">גיבוי אוטומטי</span> של כל הפרויקטים מ-GitHub לגוגל דרייב',
                                   [("03:00", "כל לילה"), ("₪0", "עלות")], "assets/images/guide/backup-1.png"),
    "article-claude-code-price.html": ("#C8553A", 'כמה עולה <span class="text-white">קלוד קוד</span>, ואיזה מנוי מספיק למתחילים',
                                       [("20$", "Pro לחודש"), ("0$", "הקורס שלנו")], "assets/images/guide/claude-usage.png"),
}
CARD_COLORS = ["#5C1E0F", "#4763D6", "#C8553A", "#7A3FC4"]


POST_IMGS = ["post-0-w.webp", "post-1-w.webp", "post-2.webp", "post-0.webp", "post-1.webp"]


def _cover(href, k):
    """תמונת השער של המאמר (tools/site_build/covers.py), ואם אין: אחת מתמונות הרקע של דף הבית."""
    import covers
    return covers.cover(href) or "assets/images/home2/" + POST_IMGS[k % len(POST_IMGS)]


ARTICLE_DATES = {}  # קובץ -> "עודכן ב..." (ממלא build_article)


def _meta(href, mins):
    d = ARTICLE_DATES.get(href)
    return f'<span class="ac-m"><span>{mins} דקות קריאה</span>' + (f'<i aria-hidden="true"></i><span>{d}</span>' if d else "") + '</span>'


def articles_main(articles):
    """articles: [(קובץ, כותרת, תיאור, דקות)].
    רשת של עד 3 כרטיסים מרובעים בשורה: התמונה ממלאת את הכרטיס, והכותרת בלבן על מעבר כהה בתחתית."""
    soup = BeautifulSoup(open(os.path.join(HERE, "mint_ref", "page.html")).read(), "html.parser")
    sec = [x for x in soup.find("main").find_all("section") if x.find_parent("section") is None][7]
    do_head(sec, "כל המאמרים.", f"{len(articles)} מאמרים קצרים, ואפשר לעשות כל אחד היום.")
    sec.find("header").find("div", class_="shrink-0").decompose()
    grid = sec.find("div", class_="grid-cols-3")
    sec.find(attrs={"aria-label": "Latest blog posts"}).decompose()
    grid["class"] = ["m2-arts"]
    grid.clear()
    out = []
    for k, (href, title, desc, mins) in enumerate(articles):
        out.append(f'<a class="ac" href="{href}">'
                   f'<img src="{_cover(href, k)}" alt="" loading="{"eager" if k < 3 else "lazy"}" decoding="async">'
                   f'<span class="ac-b"><h2 class="ac-t">{title}</h2>{_meta(href, mins)}</span></a>')
    grid.append(frag("".join(out)))
    pad = sec.find("div", class_="pb-30")
    if pad: pad["class"] = ["grid-layout", "relative", "pb-12", "lg:pb-16"]
    return f'<main class="m2-arts-main">{sec}</main>'


def articles_visual(articles):
    """האיור בפתיחה של עמוד המאמרים: רשימת המאמרים שעולה לאט בלולאה (כל מאמר עם תמונת השער שלו)."""
    items = [(_cover(href, k), "מאמר", title, f"{mins} דקות") for k, (href, title, desc, mins) in enumerate(articles)]
    items.append(("assets/images/home2/post-2.webp", "מהאתר", "המדריך הכתוב, פרק אחרי פרק", "מדריך"))
    one = "".join(f'<div class="toc-it"><img src="{i}" alt=""><div><small>{t}</small><b>{h}</b></div><em>{m}</em></div>' for i, t, h, m in items)
    reps = max(2, 6 // len(items))
    return f'<div class="toc"><div class="toc-track">{one * reps}{one * reps}</div></div>'
