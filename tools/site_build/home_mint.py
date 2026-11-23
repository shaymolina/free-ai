"""דף הבית בכיוון העיצובי של Mintlify: כל המקטעים, הרקעים הגרפיים (חוטים, נקודות) והפוטר.

נקרא מתוך compact_site.py (build_home). העיצוב: site/assets/css/home.css, שנשען על tokens.css.
"""
import math
import random


# ---------------------------------------------------------------------
# גרפיקה: חוטים, גל, נקודות
# ---------------------------------------------------------------------
def _grad(gid, x1, x2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="0" x2="{x2}" y2="0">{s}</linearGradient>'


GREEN = [(0, "#D43B2D", 0), (.45, "#F0A27F", .75), (1, "#E6BB35", .35)]


def strands(gid, w, h, n, f, stops=GREEN, cls="", width=.9):
    """צרור עקומות: f(t) מחזיר את ה-d של כל קו, t בין -0.5 ל-0.5."""
    paths = "".join(f'<path d="{f(i / (n - 1) - .5)}"/>' for i in range(n))
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<defs>{_grad(gid, 0, w, stops)}</defs><g fill="none" stroke="url(#{gid})" stroke-width="{width}">{paths}</g></svg>')


def wave(gid, w=1088, h=300, n=26):
    """גל של חוטים שמתלפפים זה בזה (המקטע 'לומדים בקצב שלכם')."""
    def line(i):
        k = i / (n - 1)
        amp = 34 + 70 * math.sin(k * math.pi)
        ph = k * 2.4
        pts = []
        for j in range(0, 49):
            x = j / 48 * w
            y = h / 2 + amp * math.sin(x / w * 2 * math.pi * 1.15 + ph) * (0.35 + 0.65 * math.sin(x / w * math.pi))
            pts.append(f"{x:.0f} {y:.1f}")
        return "M " + " L ".join(pts)
    a = "".join(f'<path d="{line(i)}"/>' for i in range(0, n, 2))
    b = "".join(f'<path d="{line(i)}"/>' for i in range(1, n, 2))
    stops = [(0, "#D43B2D", .05), (.3, "#D35234", .75), (.7, "#E6BB35", .75), (1, "#D43B2D", .1)]
    return (f'<svg class="wave" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<defs>{_grad(gid, 0, w, stops)}</defs>'
            f'<g class="w-a" fill="none" stroke="url(#{gid})" stroke-width=".9">{a}</g>'
            f'<g class="w-b" fill="none" stroke="url(#{gid})" stroke-width=".9">{b}</g></svg>')


def dots(seed, w, h, n, cls="dither"):
    """רשת נקודות קטנות בגושים (אפור, עם מעט ירוק), כמו ברקע של הפוטר."""
    r = random.Random(seed)
    centers = [(r.uniform(.2, .8) * w, r.uniform(.15, .85) * h, r.uniform(.18, .3) * w) for _ in range(2 + n // 60)]
    out = []
    for gy in range(4, h, 14):
        for gx in range(4, w, 14):
            p = max(2.718 ** (-((gx - cx) ** 2 + (gy - cy) ** 2) / (2 * sg * sg)) for cx, cy, sg in centers)
            if r.random() > p * .85:
                continue
            c = r.choices(["#D6D4D0", "#B9B8B5", "#D97757", "#CC9E16"], [72, 16, 8, 4])[0]
            out.append(f'<rect x="{gx}" y="{gy}" width="1.6" height="1.6" fill="{c}"/>')
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false">{"".join(out)}</svg>'


def card_strings(gid):
    """חוטים עדינים לרקע של כרטיסי הבנטו."""
    return strands(gid, 600, 360, 18,
                   lambda t: f"M -40 {250 + 90 * t:.1f} C 160 {120 - 160 * t:.1f}, 380 {330 + 120 * t:.1f}, 660 {90 + 200 * t:.1f}",
                   stops=[(0, "#D43B2D", .1), (.5, "#F0A27F", .55), (1, "#E6BB35", .2)], cls="b-str", width=.8)


def art_strings(gid, color="#FFFFFF"):
    """חוטים לבנים לכרטיסים הצבעוניים."""
    return strands(gid, 400, 460, 30,
                   lambda t: f"M -40 {420 + 240 * t:.1f} C 120 {300 - 260 * t:.1f}, 260 {200 + 300 * t:.1f}, 440 {40 + 160 * t:.1f}",
                   stops=[(0, color, .05), (.5, color, .55), (1, color, .15)], cls="art-str", width=.8)


ICONS = {  # אייקונים פשוטים בקו (24x24)
    "play": '<path d="M8 5.5v13l10-6.5z"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20"/>',
    "spark": '<path d="M12 3v5M12 16v5M3 12h5M16 12h5M6 6l3 3M15 15l3 3M18 6l-3 3M9 15l-3 3"/>',
    "file": '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>',
    "chart": '<path d="M5 20V10M10 20V4M15 20v-7M20 20v-4"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "coin": '<circle cx="12" cy="12" r="8.5"/><path d="M14.5 9.2c-.5-.8-1.4-1.2-2.5-1.2-1.6 0-2.7.8-2.7 2s1.1 1.7 2.7 2 2.7.8 2.7 2-1.1 2-2.7 2c-1.2 0-2.1-.5-2.6-1.3M12 6.5v1.5M12 16v1.5"/>',
    "arrow": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chev-l": '<path d="M15 6l-6 6 6 6"/>',
    "chev-r": '<path d="M9 6l6 6-6 6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "send": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "cut": '<circle cx="6" cy="7" r="2.5"/><circle cx="6" cy="17" r="2.5"/><path d="M8 8.5 19 18M8 15.5 19 6"/>',
    "cake": '<path d="M4 20h16v-7H4zM4 15c2 1.5 4 1.5 5.3 0 1.3 1.5 4 1.5 5.4 0 1.3 1.5 3.3 1.5 5.3 0M12 13V9M12 6.5v-.5"/>',
    "home": '<path d="M4 11 12 4l8 7v9H4zM10 20v-5h4v5"/>',
    "bag": '<path d="M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2"/>',
    "dumbbell": '<path d="M4 9v6M7 7v10M17 7v10M20 9v6M7 12h10"/>',
    "camera": '<path d="M4 8h3l2-2.5h6L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "chev-d": '<path d="M6 9l6 6 6-6"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    "rocket": '<path d="M5 15c-1 1-1.5 3.5-1.5 5.5 2 0 4.5-.5 5.5-1.5M9 15l-2-2c1-4 4.5-9 12-9.5-.5 7.5-5.5 11-9.5 12z"/><circle cx="14.5" cy="9.5" r="1.5"/>',
    "box": '<path d="M12 3 4 7.5v9L12 21l8-4.5v-9zM4 7.5 12 12l8-4.5M12 12v9"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v4a6 6 0 0 1-12 0zM12 18v3"/>',
    "shield": '<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "chat": '<path d="M5 5h14v10H9l-4 4z"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M5.6 18.4l1.8-1.8M16.6 7.4l1.8-1.8"/>',
    "layers": '<path d="M12 4 3 9l9 5 9-5zM3 14l9 5 9-5"/>',
    "term": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M12 15h5"/>',
    "branch": '<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="8" r="2"/><path d="M6 7v10M18 10c0 4-6 3-11 7"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9.5 4.3 4.3 0 0 0 7 18z"/>',
    "drive": '<path d="M8 4h8l5 9-4 7H7l-4-7z"/><path d="M8 4l9 16M16 4 7 20M3 13h18"/>',
}


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def head(line1, line2, btn_href=None, btn_text=None, extra=""):
    """כותרת מקטע בשני צבעים (שורה כהה + שורה אפורה), עם כפתור בצד."""
    b = f'<a href="{btn_href}" class="btn">{btn_text} <span class="arr">←</span></a>' if btn_href else ""
    return f'<div class="m-head"><h2>{line1}<span>{line2}</span></h2><div class="m-head-act">{extra}{b}</div></div>'


# ---------------------------------------------------------------------
# המקטעים (כל אחד מקביל למקטע באתר המקור)
# ---------------------------------------------------------------------
def canvas(kind, cls, flip=False, rib=""):
    return f'<canvas class="{cls}" data-kind="{kind}"{" data-flip=\"1\"" if flip else ""}{f" data-rib=\"{rib}\"" if rib else ""} aria-hidden="true"></canvas>'


def hero_preview(chapters):
    side = [("chat", "שאלו את קלוד", ""), ("rocket", "מתחילים", "on"), ("gear", "הגדרות", ""), ("plug", "חיבורים", ""),
            ("box", "סקילים", ""), ("layers", "חבילות", ""), (None, None, None),
            ("shield", "הרשאות", "dim"), ("book", "בחירת המודל", "dim"), ("file", "מיקום הפרויקט", "dim"), ("clock", "כמה נשאר מהמנוי", "dim"),
            (None, None, None), ("send", "מעלים לאוויר", "dim2"), ("home", "פותחים 4CODE", "dim2")]
    side_html = "".join('<li class="sep"></li>' if i is None else f'<li class="{c}">{icon(i)}<span>{t}</span></li>' for i, t, c in side)
    cards = [("rocket", "מתחילים", "שלושה דברים להכין, ואפשר לצאת לדרך"),
             ("box", "התקנה", "מתקינים את האפליקציה במחשב, Windows או Mac"),
             ("layers", "ריפו ראשון", "פותחים מקום לפרויקט ב-GitHub"),
             ("send", "מעלים לאוויר", "האתר מקבל כתובת שאפשר לשלוח לכל אחד")]
    cards_html = "".join(f'<li><span class="pv-art">{icon(i)}</span><b>{t}</b><small>{d}</small></li>' for i, t, d in cards)
    return f"""<div class="hero-stage"><div class="pv" aria-hidden="true">
        <aside class="pv-side"><div class="pv-logo"><img src="assets/images/logo/favicon.svg" alt=""><b>Free AI</b></div><ul>{side_html}</ul></aside>
        <div class="pv-main">
            <div class="pv-top"><nav><span class="on">המדריך</span><span>הקורס</span><span>סקילים</span></nav><span class="pv-search">{icon("search")}חיפוש או שאלה</span></div>
            <span class="pv-crumb">מתחילים</span>
            <b class="pv-h">המדריך לקלוד קוד</b>
            <small class="pv-sub">{len([1 for _ in chapters])} פרקים קצרים, מהחשבון הראשון ועד אתר באוויר</small>
            <ul class="pv-cards">{cards_html}</ul>
        </div>
        <span class="pv-ask">{icon("chat")}שאלו את קלוד</span>
    </div></div>"""


def sec_tools(n_chapters, n_minutes, n_articles):
    tools = [("Claude", "guide-3.html", "spark"), ("Claude Code", "guide-4.html", "term"), ("GitHub", "guide-5.html", "branch"), ("4CODE", "guide-18.html", "cloud"),
             ("Connectors", "guide-13.html", "plug"), ("Skills", "guide-14.html", "box"), ("Plugins", "guide-15.html", "layers"), ("Google Drive", "article-github-backup.html", "drive")]
    tiles = "".join(f'<li><a class="tool" href="{h}"><b dir="ltr">{icon(i)}{a}</b><span class="tool-go">{icon("chev-l")}</span></a></li>' for a, h, i in tools)
    items = [("פרקים במדריך", n_chapters), ("שיעורי וידאו", 8), ("דקות קריאה", n_minutes), ("מאמרים", n_articles),
             ("מחיר", "₪0"), ("שורות קוד שתכתבו", 0), ("בעברית", "100%")]
    run = "".join(f'<span class="tk">{a} <b>{b}</b></span>' for a, b in items)
    return f"""
    <section class="m-sec m-tools">
        <div class="m-in tools-in">
            <div class="tools-txt">
                <p>כל <b>{len(tools)} הכלים</b> שתפגשו בדרך, <b>בעברית ובחינם</b>.</p>
                <a href="guide-1.html" class="btn">למדריך המלא <span class="arr">‹</span></a>
            </div>
            <ul class="tools-grid">{tiles}</ul>
        </div>
    </section>
    <section class="m-sec m-ticker" aria-label="הקורס במספרים">
        <div class="m-in ticker-in">
            <span class="tk-label">מה מחכה לכם</span>
            <div class="tk-view"><div class="tk-run">{run}<span class="tk-dup" aria-hidden="true">{run}</span></div></div>
        </div>
    </section>"""


def sec_bento():
    ask = f'<div class="mk-ask"><span class="spark">✦</span><span class="t"><span class="ty">תבנה לי אתר לנגרייה, עם גלריה וטופס</span></span><span class="go">{icon("send")}</span></div>'
    check = '<ul class="mk-list">' + "".join(
        f'<li style="--i:{n}"><i>{icon("check")}</i><span>{t}</span></li>'
        for n, t in enumerate(["פותחים חשבון קלוד", "מתקינים את האפליקציה", "פותחים GitHub", "בונים אתר ראשון"])) + '</ul>'
    roles = '<ul class="mk-roles">' + "".join(
        f'<li style="--i:{n}"><i></i><span>{t}</span><em>{e}</em></li>'
        for n, (t, e) in enumerate([("שואל לפני כל שינוי", "זהיר"), ("עורך קבצים לבד", "מומלץ"), ("עושה הכול בלי לשאול", "מהיר")])) + '</ul>'
    conn = ('<div class="mk-conn"><span class="c1" dir="ltr">GH</span><i></i><span class="c0">'
            '<img src="assets/images/logo/favicon.svg" alt=""></span><i></i><span class="c2" dir="ltr">SB</span></div>')
    chips = '<div class="mk-doc"><div class="dl w1"></div><div class="dl w2"><em class="tg a">קלוד</em></div><div class="dl w3"></div><div class="dl w2 hl"><em class="tg b">אתם</em></div><div class="dl w1"></div></div>'
    site = ('<div class="mk-site"><div class="bar"><span></span><span></span><span></span><em dir="ltr">nagariya.co.il</em>'
            '<b class="live"><i></i>באוויר</b></div><div class="body"><div class="hero"><b>נגרות יוסי</b><small>רהיטים בהזמנה אישית</small>'
            '<em>צרו קשר</em></div><div class="gal"><i></i><i></i><i></i><i></i></div></div></div>')
    cards = [
        ("w2", "כותבים בעברית, קלוד קוד בונה", ask),
        ("", "מדריך שזוכר איפה עצרתם", check),
        ("", "מחליטים כמה קלוד עושה לבד", roles),
        ("", "מתחברים לשירותים", conn),
        ("", "עובדים ביחד עם קלוד", chips),
        ("w3", "מהרעיון לאתר שעובד באוויר", site),
    ]
    html = "".join(f'<li class="bento-c {w}">{canvas("card", "b-cv")}<div class="mk">{m}</div><h3>{t}</h3></li>' for w, t, m in cards)
    return f"""
    <section class="m-sec">
        <div class="m-in">
            {head("כל מה שצריך לאתר הראשון.", "בלי לכתוב שורת קוד.", "service.html", "התחל ללמוד")}
            <ul class="bento">{html}</ul>
        </div>
    </section>"""


def car_nav():
    return (f'<div class="car-nav"><button type="button" class="btn-2 ic" data-car="-1" aria-label="הקודם">{icon("chev-r")}</button>'
            f'<button type="button" class="btn-2 ic" data-car="1" aria-label="הבא">{icon("chev-l")}</button></div>')


def sec_stories():
    stories = [
        ("green", "אתר לעסק", 'ככה <b>הודעה אחת בעברית</b> הופכת לאתר עם גלריה וטופס', [("1", "הודעה בעברית"), ("0", "שורות קוד שאתם כותבים")],
         "article-what-is-claude-code.html", "assets/images/claude/build-site.jpg"),
        ("ink", "גיבוי אוטומטי", 'ככה <b>כל הפרויקטים</b> נשמרים לבד בגוגל דרייב, כל לילה', [("03:00", "כל לילה"), ("₪0", "עלות")],
         "article-github-backup.html", "assets/images/guide/backup-1.png"),
        ("orange", "מעלים לאוויר", 'ככה האתר מקבל <b>כתובת אמיתית</b> שאפשר לשלוח לכל אחד', [("1", "כתובת לשתף"), ("30", "ימים בחינם עם הקופון")],
         "guide-18.html", "assets/images/guide/claude-map.png"),
    ]
    cards = "".join(f"""<li class="story s-{c}">
                <div class="st-l"><span class="st-dots d1" aria-hidden="true"></span><span class="st-dots d2" aria-hidden="true"></span><span class="st-dots d3" aria-hidden="true"></span>
                    <span class="st-tag">{tag}</span><h3>{t}</h3>
                    <div class="st-nums">{"".join(f'<div><strong dir="ltr" data-roll>{a}</strong><small>{b}</small></div>' for a, b in nums)}</div>
                    <a href="{href}" class="btn-2">לסיפור המלא <span class="arr">‹</span></a></div>
                <div class="st-img"><img src="{img}" alt="{tag}" loading="lazy"></div>
            </li>""" for c, tag, t, nums, href, img in stories)
    return f"""
    <section class="m-sec m-stories" data-carousel data-dim>
        <div class="m-in">{head("מה בונים עם קלוד קוד.", "שלוש דוגמאות מהמדריך ומהמאמרים.", "articles.html", "לכל המאמרים", car_nav())}</div>
        <div class="car"><ul class="car-track">{cards}</ul></div>
    </section>"""


def sec_scale(n_chapters):
    stats = [("chart", str(n_chapters), "פרקים קצרים במדריך"), ("play", "8", "שיעורי וידאו לפי הסדר"), ("coin", "₪0", "מחיר הקורס, תמיד")]
    st = "".join(f'<li>{icon(i)}<strong dir="ltr" data-roll>{a}</strong><span>{b}</span></li>' for i, a, b in stats)
    return f"""
    <section class="m-sec m-scale">
        <div class="m-in">
            {head("לומדים בקצב שלכם.", "פרקים קצרים, צעד אחד בכל פעם.", "guide-1.html", "לפרק הראשון")}
            <div class="wave-box">{canvas("wave", "wave", flip=True)}</div>
            <ul class="stats">{st}</ul>
        </div>
    </section>"""


def sec_start(n_chapters):
    items = [("p-pink", "play", "הקורס", "8 שיעורי וידאו, לפי הסדר.", "service.html", "לקורס"),
             ("p-mint", "book", "המדריך", f"{n_chapters} פרקים לקריאה, צעד אחרי צעד.", "guide-1.html", "למדריך"),
             ("p-night", "spark", "סקילים", "יכולות מוכנות לקלוד, להורדה בחינם.", "work.html", "לסקילים"),
             ("p-fire", "file", "מאמרים", "מדריכים קצרים שאפשר לעשות היום.", "articles.html", "למאמרים"),
             ("p-sky", "rocket", "הפרק הראשון", "שלושה דברים להכין, ואפשר לצאת לדרך.", "guide-1.html", "לפרק 1")]
    cards = "".join(f"""<li class="start">
                <a href="{h}" class="start-art {c}" tabindex="-1" aria-hidden="true">{canvas(("art", "art2", "art3")[n % 3], "art-cv")}<span class="start-tile">{icon(i)}</span></a>
                <p><b>{t}</b> {d}</p><a href="{h}" class="start-go">{g} <span class="arr">‹</span></a>
            </li>""" for n, (c, i, t, d, h, g) in enumerate(items))
    return f"""
    <section class="m-sec m-starts" data-carousel>
        <div class="m-in">{head("מאיפה מתחילים.", "חמש דרכים להיכנס לחומר.", "service.html", "התחל ללמוד", car_nav())}</div>
        <div class="car"><ul class="car-track starts">{cards}</ul></div>
    </section>"""


PROMPTS = [("cut", "מספרה", "יומן תורים", "תבנה לי יומן תורים למספרה, שהלקוחות יקבעו לבד ויקבלו תזכורת בוואטסאפ."),
           ("cake", "קונדיטוריה", "אתר עם הזמנות", "תבנה אתר לקונדיטוריה שלי עם תפריט עוגות, תמונות וטופס הזמנה לאירועים."),
           ("home", "שיפוצים", "עמוד נחיתה", "תכין עמוד אחד לקבלן שיפוצים: לפני ואחרי, המלצות וכפתור וואטסאפ."),
           ("bag", "חנות קטנה", "קטלוג מוצרים", "תבנה קטלוג ל-30 מוצרים עם מחירים, חיפוש וכפתור 'להזמנה'."),
           ("dumbbell", "מאמן כושר", "מעקב מתאמנים", "תבנה מערכת קטנה שאני רושם בה אימונים של כל מתאמן ורואה התקדמות."),
           ("camera", "צלמת", "גלריה ללקוחות", "תבנה גלריה שכל לקוח נכנס עם קוד ורואה רק את התמונות שלו."),
           ("chat", "רואת חשבון", "טופס קליטת לקוח", "תבנה טופס שלקוח חדש ממלא, ואני מקבלת את הפרטים במייל מסודרים."),
           ("file", "מורה פרטי", "דף שיעורים", "תבנה עמוד שבו התלמידים רואים את השיעורים הבאים ומורידים דפי עבודה."),
           ("layers", "גן ילדים", "לוח הודעות להורים", "תבנה לוח הודעות קטן לגן, שההורים רואים בו תמונות ועדכונים מהיום.")]


def sec_prompts():
    def card(i, a, b, t):
        return f'<li class="pr"><div class="pr-h"><span class="pr-ic">{icon(i)}</span><div><b>{a}</b><small>{b}</small></div></div><p>"{t}"</p></li>'
    cols = []
    for c in range(3):
        group = [PROMPTS[k] for k in range(c, len(PROMPTS), 3)]
        one = "".join(card(*x) for x in group)
        dup = "".join(card(*x) for x in group).replace('<li class="pr">', '<li class="pr" aria-hidden="true">')
        cols.append(f'<ul class="pr-col c{c}">{one}{dup}</ul>')
    return f"""
    <section class="m-sec">
        <div class="m-in">
            {head("מה כותבים לקלוד קוד.", "הודעות אמיתיות, בעברית רגילה.", "guide-16.html", "איך כותבים בקשה טובה")}
            <div class="pr-bar"><button type="button" class="pr-pause" id="pr-pause" aria-pressed="false" aria-controls="prompts">עצירת הדוגמאות</button></div>
            <div class="prompts" id="prompts">{"".join(cols)}</div>
        </div>
    </section>"""


def sec_posts(articles):
    arts = ["p-forest", "p-deep", "p-sand"]
    icons_ = ["file", "clock", "book"]
    posts = [(n, t) for n, t, d, m in articles][:2] + [("articles.html", "כל המאמרים במקום אחד")]
    cards = "".join(f"""<li class="post"><a href="{n}">
                <span class="post-art {arts[k]}">{canvas("art", "art-cv")}<span class="start-tile">{icon(icons_[k])}</span></span>
                <span class="post-meta"><em>{"מאמר" if k < 2 else "מאמרים"}</em>{"נובמבר 2026" if k < 2 else ""}</span>
                <b>{t}</b></a></li>""" for k, (n, t) in enumerate(posts))
    return f"""
    <section class="m-sec">
        <div class="m-in">
            {head("מאמרים אחרונים.", "קצרים, ואפשר לעשות אותם היום.", "articles.html", "לכל המאמרים")}
            <ul class="posts">{cards}</ul>
        </div>
    </section>"""


def sec_cta():
    return f"""
    <section class="m-sec m-cta">
        <div class="m-in cta-in">
            {canvas("cta", "cta-cv", flip=True)}
            <h2>קורס קלוד קוד, בחינם ובעברית</h2>
            <div class="btns"><a href="guide-1.html" class="btn-3">למדריך הכתוב</a><a href="service.html" class="btn">התחל ללמוד <span class="arr">‹</span></a></div>
        </div>
    </section>"""


def sec_faq(faq_html):
    return f"""
    <section class="m-sec">
        <div class="m-in faq-in">
            <h2 class="faq-t">שאלות נפוצות</h2>
            {faq_html}
        </div>
    </section>"""


def footer(chapters, articles, ready):
    cols = [
        ("לומדים", [("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]),
        ("המדריך", [(f"guide-{i}.html", chapters[i - 1][0]) for i in (1, 3, 5, 16, 18) if i in ready]),
        ("מאמרים", [(n, t.split("?")[0] + ("?" if "?" in t else "")) for n, t, d, m in articles]),
        ("מידע", [("privacy.html", "פרטיות"), ("terms.html", "תנאי שימוש")]),
    ]
    c = "".join(f'<div class="f-col"><h3>{h}</h3><ul>{"".join(f"<li><a href=\"{a}\">{b}</a></li>" for a, b in links)}</ul></div>' for h, links in cols)
    return f"""
    <footer class="m-foot">
        {dots(7, 160, 420, 90, "dither f-d1")}{dots(11, 160, 420, 90, "dither f-d2")}{dots(5, 160, 420, 50, "dither f-d3")}
        <div class="m-in foot-in">
            <div class="f-brand"><a href="index.html" class="c-logo"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>
                <div class="f-tag"><p class="f-tag-h">קלוד קוד בחינם</p><p class="f-tag-p">קורס Claude Code למתחילים, בלי ידע בתכנות. שיעורי וידאו, מדריך כתוב וסקילים.</p></div>
                <a class="f-ok" href="mailto:hello@free-ai.co.il">hello@free-ai.co.il</a></div>
            <nav class="f-cols" aria-label="קישורים בפוטר">{c}</nav>
        </div>
        <div class="m-in f-bot">
            <span>© 2026 Free AI. כל הזכויות שמורות.</span>
            <a href="#top" class="f-top">חזרה למעלה {icon("up")}</a>
        </div>
    </footer>"""


HOME_JS = '<script src="assets/js/mint.js?v=12" defer></script>'


def body(header_html, hero_demo, strings, chapters, ready, articles, faq_html):
    n_ch = len(ready)
    mins = sum(m for _, m in chapters)
    need = "".join(f"<li>{icon('check')}<span><b>{a}</b> {b}</span></li>" for a, b in [
        ("מחשב", "Mac או Windows"), ("מייל", "אחד לכל השירותים"), ("מנוי Claude Pro", "כ-20 דולר לחודש")])
    return f"""    <div class="wrap full" id="top">
        <section class="c-hero m-hero">
        {canvas("hero", "hero-cv", flip=True, rib="hero")}
        {header_html}
            <div class="hero-in">
                <div class="hero-text">
                    <a href="guide-1.html" class="chip">המדריך הכתוב <b><span data-roll>{n_ch}</span> פרקים</b><span class="chip-go">‹</span></a>
                    <h1 class="hero-title">קורס קלוד קוד<br>בחינם ובעברית</h1>
                    <p>קורס Claude Code למתחילים, בלי ידע בתכנות. <b>שיעורי וידאו</b>, <b>מדריך כתוב</b> ו<b>סקילים</b>.</p>
                    <div class="btns"><a href="service.html" class="btn">התחל ללמוד <span class="arr">‹</span></a><a href="guide-1.html" class="btn-2">{icon("book")}למדריך הכתוב</a></div>
                    <details class="need"><summary><span class="need-ic">{icon("home")}{icon("chat")}{icon("spark")}</span>מה צריך כדי להתחיל{icon("chev-d")}</summary><ul>{need}</ul></details>
                </div>
                {hero_preview(ready)}
            </div>
        </section>
    </div>
    <main class="m-home">
{sec_tools(n_ch, mins, len(articles))}
{sec_bento()}
{sec_stories()}
{sec_scale(n_ch)}
{sec_start(n_ch)}
{sec_prompts()}
{sec_posts(articles)}
{sec_cta()}
{sec_faq(faq_html)}
    </main>
{footer(chapters, articles, ready)}"""
