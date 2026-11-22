"""דף בית 2: המבנה, העיצוב והאנימציות של דף הבית של Mintlify, עם התוכן של Free AI.
המקור: mint_ref/page.html (ה-HTML שלהם אחרי רינדור). כאן מחליפים את התוכן, ו-site/assets/js/m2.js מפעיל את האנימציות."""
import glob, os, re, sys
from bs4 import BeautifulSoup, NavigableString

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "..", "site")
sys.path.insert(0, HERE)
import home_mint  # noqa: E402

V = "1"
HEAD = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>קורס קלוד קוד בחינם | Free AI</title>
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
    chip = sec.find("a", href="/data"); chip["href"] = "guide-1.html"
    sp = chip.find_all("span", recursive=False)
    put(sp[0], "המדריך הכתוב")
    num = sp[1].find("span", class_="font-paper")
    put(num, roller(str(n_ch)) + " פרקים")
    h1 = sec.find("h1"); put(h1, "קורס קלוד קוד<br>בחינם ובעברית")
    p = h1.find_next("p")
    put(p, 'קורס Claude Code למתחילים, בלי ידע בתכנות. <span class="font-medium text-text-main">שיעורי וידאו</span>, <span class="font-medium text-text-main">מדריך כתוב</span> ו<span class="font-medium text-text-main">סקילים</span>.')
    a1 = sec.find("a", href="https://app.mintlify.com/signup"); a1["href"] = "service.html"
    a1.contents[0].replace_with("התחל ללמוד")
    a2 = sec.find("a", href="https://app.mintlify.com/api/auth/google/discovery"); a2["href"] = "guide-1.html"
    put(a2, icon("book", "size-4 text-brand") + "למדריך הכתוב")
    btn = a2.find_parent("div").find_next_sibling("div").find("button")
    a3 = soup_tag(sec, "a", href="guide-1.html"); a3["class"] = btn["class"]
    put(a3, f'<span class="flex items-center gap-1">{icon("box")}{icon("chat")}{icon("coin")}</span>מה צריך כדי להתחיל{icon("chev-l", "size-4")}')
    btn.replace_with(a3)
    box = sec.find(attrs={"aria-label": "Mintlify documentation preview"})
    box["aria-label"] = "המדריך הכתוב של Free AI"
    imgs = box.find_all("img")
    imgs[0]["src"] = "assets/images/home2/preview.webp"; imgs[0]["alt"] = "המדריך הכתוב: פרק 1, לפני שמתחילים"
    for k in ("srcset", "sizes"):
        imgs[0].attrs.pop(k, None)
    imgs[1].decompose()


def soup_tag(node, name, **attrs):
    s = BeautifulSoup("", "html.parser")
    return s.new_tag(name, attrs=attrs)


# ---------------------------------------------------------------- כלים + פס מספרים
TOOLS = [("Claude", "guide-3.html", "spark"), ("Claude Code", "guide-4.html", "term"), ("GitHub", "guide-5.html", "branch"), ("4CODE", "guide-19.html", "cloud"),
         ("Connectors", "guide-13.html", "plug"), ("Skills", "guide-14.html", "box"), ("Plugins", "guide-15.html", "layers"), ("Google Drive", "article-github-backup.html", "drive")]


def do_tools(sec, n_ch, n_art):
    h2 = sec.find("h2"); put(h2, f'כל <strong class="font-medium text-text-main">{len(TOOLS)} הכלים</strong> שתפגשו בדרך, בעברית ובחינם.')
    a = h2.find_next("a"); a["href"] = "guide-1.html"; a.contents[0].replace_with("למדריך המלא")
    cards = sec.find_all("div", class_="group/card")
    for card, (name, href, ic) in zip(cards, TOOLS):
        logo = card.find_all("span", recursive=False)[1]
        put(logo, f'<span class="inline-flex items-center gap-2 text-[17px] font-medium text-text-main" dir="ltr">{icon(ic, "size-5 text-brand")}{name}</span>')
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
    for grp in rows.find_all("div", class_="gap-8"):
        for span, (lab, val) in zip(grp.find_all("span", recursive=False), items):
            s = span.find_all("span", recursive=False)
            put(s[0], lab); put(s[1], f'<span dir="ltr">{val}</span>')


# ---------------------------------------------------------------- כותרת מקטע (קו ירוק + שתי שורות + כפתור)
def do_head(sec, title, sub, href=None, label=None):
    h2 = sec.find("h2")
    put(h2, f'{title}<span class="block text-foreground-tertiary">{sub}</span>')
    if href:
        a = sec.find("header").find("a")
        a["href"] = href; a.contents[0].replace_with(label)


def carousel_buttons(sec, what):
    for b in sec.find("header").find_all("button"):
        b["aria-label"] = ("הקודם: " if "Previous" in b["aria-label"] else "הבא: ") + what
        b["data-car"] = "-1" if b["aria-label"].startswith("הקודם") else "1"


import copy

STORIES = [
    ("#0F5C3F", "אתר לעסק", 'ככה <span class="text-white">הודעה אחת בעברית</span> הופכת לאתר עם גלריה וטופס', [("1", "הודעה בעברית"), ("0", "שורות קוד שאתם כותבים")],
     "article-what-is-claude-code.html", "assets/images/claude/build-site.jpg"),
    ("#4763D6", "גיבוי אוטומטי", 'ככה <span class="text-white">כל הפרויקטים</span> נשמרים לבד בגוגל דרייב, כל לילה', [("03:00", "כל לילה"), ("₪0", "עלות")],
     "article-github-backup.html", "assets/images/guide/backup-1.png"),
    ("#C8553A", "מעלים לאוויר", 'ככה האתר מקבל <span class="text-white">כתובת אמיתית</span> שאפשר לשלוח לכל אחד', [("1", "כתובת לשתף"), ("30", "ימים בחינם עם הקופון")],
     "guide-18.html", "assets/images/guide/claude-map.png"),
    ("#7A3FC4", "סקילים", 'ככה <span class="text-white">יכולת מוכנה</span> נכנסת לקלוד בלחיצה אחת', [("1", "לחיצה להורדה"), ("₪0", "מחיר")],
     "work.html", "assets/images/home2/skills.webp"),
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


RIVES = [("agent-native-platform", "agent-native-platform-mobile"), ("self-updating-knowledge", None), ("control-who-has-access", None),
         ("connect-with-your-systems", None), ("collaborate-with-your-team-and-agents", None), ("build-on-top-of-your-existing-setup", "build-on-top-of-your-existing-setup-mobile")]


def do_bento(sec):
    """הכרטיסים המקוריים שלהם עם אנימציות ה-Rive המקוריות, והכותרות בעברית."""
    do_head(sec, "כל מה שצריך לאתר הראשון.", "בלי לכתוב שורת קוד.", "service.html", "התחל ללמוד")
    titles = [t for t, _ in bento_mocks()]
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
def do_scale(sec, n_ch):
    do_head(sec, "לומדים בקצב שלכם.", "פרקים קצרים, צעד אחד בכל פעם.", "guide-1.html", "לפרק הראשון")
    cv = sec.find("canvas"); cv["data-rib"] = "wave"; cv["data-flip"] = "1"; cv["aria-hidden"] = "true"
    stats = [(str(n_ch), "פרקים קצרים במדריך"), ("8", "שיעורי וידאו לפי הסדר"), ("₪0", "מחיר הקורס, תמיד")]
    for blk, (n, lab) in zip(sec.find_all("div", class_="gap-6"), stats):
        ps = blk.find_all("p"); put(ps[0], f'<span dir="ltr">{n}</span>'); put(ps[1], lab)


# ---------------------------------------------------------------- כרטיסים צבעוניים
STARTS = [("הקורס", "8 שיעורי וידאו, לפי הסדר.", "service.html", "לקורס"),
          ("המדריך", "{n} פרקים לקריאה, צעד אחרי צעד.", "guide-1.html", "למדריך"),
          ("סקילים", "יכולות מוכנות לקלוד, להורדה בחינם.", "work.html", "לסקילים"),
          ("מאמרים", "מדריכים קצרים שאפשר לעשות היום.", "articles.html", "למאמרים"),
          ("הפרק הראשון", "שלושה דברים להכין, ואפשר לצאת לדרך.", "guide-1.html", "לפרק 1")]


def do_starts(sec, n_ch):
    do_head(sec, "מאיפה מתחילים.", "חמש דרכים להיכנס לחומר.", "service.html", "התחל ללמוד")
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
        imgs[0]["src"] = f"assets/images/home2/start-{k}.webp"; imgs[0]["alt"] = ""
        for x in ("srcset", "sizes"): imgs[0].attrs.pop(x, None)
        imgs[1].decompose()
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
        img = a.find("img"); img["src"] = f"assets/images/home2/post-{k}.webp"; img["alt"] = ""
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
FAQ = [("צריך מנוי בתשלום לקלוד?", "כן. קלוד Pro ומעלה.", None),
       ("צריך ידע קודם?", "לא. מתחילים מאפס.", ("guide-1.html", "לפרק הראשון")),
       ("כמה זמן לוקח הקורס?", "8 שיעורים קצרים, בקצב שלכם.", ("service.html", "לקורס")),
       ("למה צריך להירשם?", "כדי לצפות, להוריד קבצים ולקבל תעודה.", None),
       ("מה זה קלוד קוד?", "כלי של Anthropic שבונה אתרים ומערכות לפי מה שכותבים לו.", ("article-what-is-claude-code.html", "הסבר פשוט על קלוד קוד")),
       ("קלוד קוד עובד בעברית?", "כן. כותבים לו בעברית רגילה, והוא בונה גם אתרים בעברית.", None)]


def do_faq(sec):
    put(sec.find("h2"), "שאלות נפוצות")
    items = sec.find_all("div", attrs={"data-slot": "accordion-item"})
    for k, it in enumerate(items):
        if k >= len(FAQ):
            it.decompose(); continue
        q, a, link = FAQ[k]
        b = it.find("button"); svg = b.find("svg"); put(b, q); b.append(svg)
        b["data-faq"] = ""
        body = it.find("div", attrs={"data-slot": "accordion-content"}).find("div")
        put(body, f"<p>{a}</p>" + (f'<p><a class="faq-link" href="{link[0]}">{link[1]}</a></p>' if link else ""))


# ---------------------------------------------------------------- פוטר
def do_footer(soup, arts):
    f = soup.find("footer")
    f.find("canvas")["data-sectiondots"] = ""; f.find("canvas")["data-clip"] = ""; f.find("canvas")["data-feather"] = ".06"
    logo = f.find("a", attrs={"aria-label": "Go to homepage"}); logo["href"] = "index.html"; logo["aria-label"] = "Free AI, לדף הבית"
    put(logo, '<img src="assets/images/logo/logo.svg" alt="Free AI" style="height:34px;width:auto">')
    for st in f.find_all("a", href="https://status.mintlify.com/"):
        st["href"] = "guide-1.html"; st.attrs.pop("target", None); st.attrs.pop("rel", None)
        st.find_all("span", recursive=False)[1].string = "23 פרקים זמינים לקריאה"
    cols = [("לומדים", [("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]),
            ("המדריך", [("guide-1.html", "לפני שמתחילים"), ("guide-3.html", "פותחים חשבון קלוד"), ("guide-5.html", "פותחים GitHub"), ("guide-7.html", "היכרות ראשונה עם קלוד"), ("guide-18.html", "מעלים לאוויר")]),
            ("מאמרים", [(h, t.split("?")[0] + ("?" if "?" in t else "")) for h, t in arts[:4]]),
            ("כלים", [("guide-4.html", "Claude Code"), ("guide-13.html", "Connectors"), ("guide-14.html", "Skills"), ("guide-19.html", "4CODE")]),
            ("מידע", [("privacy.html", "פרטיות"), ("terms.html", "תנאי שימוש")])]
    for div, (h, links) in zip(f.find("div", class_="lg:grid-cols-5").find_all("div", recursive=False), cols):
        div.find("h3").string = h
        ul = div.find("ul"); tpl = ul.find("a"); cls = tpl["class"]; ul.clear()
        for href, t in links:
            ul.append(frag(f'<li><a class="{" ".join(cls)}" href="{href}">{t}</a></li>'))
    bottom = f.find(attrs={"aria-label": "Theme switcher"}).find_parent("div", class_="justify-between")
    put(bottom, '<span class="text-sm/5 text-neutral-500">© 2026 Free AI. כל הזכויות שמורות.</span><a class="text-sm/5 font-medium text-text-main hover:text-brand" href="#">חזרה למעלה ↑</a>')



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


def transform(s):
    n_ch, arts = counts()
    soup = BeautifulSoup(s, "html.parser")
    do_header(soup)
    do_mobile_header(soup)
    secs = [x for x in soup.find("main").find_all("section") if x.find_parent("section") is None]
    do_hero(secs[0], n_ch)
    do_tools(secs[1], n_ch, len(arts))
    do_bento(secs[2])
    do_stories(secs[3])
    do_scale(secs[4], n_ch)
    do_starts(secs[5], n_ch)
    do_prompts(secs[6])
    do_posts(secs[7], arts)
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
    open(os.path.join(SITE, "home-2.html"), "w").write(out)
    print("home-2.html done")


if __name__ == "__main__":
    build()
