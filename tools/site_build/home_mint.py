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


GREEN = [(0, "#2DD4BF", 0), (.45, "#4ADE80", .75), (1, "#A3E635", .35)]


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
    stops = [(0, "#2DD4BF", .05), (.3, "#34D399", .75), (.7, "#A3E635", .75), (1, "#2DD4BF", .1)]
    return (f'<svg class="wave" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<defs>{_grad(gid, 0, w, stops)}</defs>'
            f'<g class="w-a" fill="none" stroke="url(#{gid})" stroke-width=".9">{a}</g>'
            f'<g class="w-b" fill="none" stroke="url(#{gid})" stroke-width=".9">{b}</g></svg>')


def dots(seed, w, h, n, cls="dither"):
    """ענני נקודות קטנות (אפור, עם מעט ירוק וצהוב), כמו ברקע של הפוטר."""
    r = random.Random(seed)
    out = []
    for _ in range(n):
        cx, cy = r.gauss(w / 2, w / 4), r.gauss(h / 2, h / 3)
        if not (0 < cx < w and 0 < cy < h):
            continue
        x, y = round(cx / 8) * 8, round(cy / 8) * 8
        c = r.choices(["#C9C7C3", "#9B9C9E", "#4ADE80", "#FACC15"], [70, 18, 8, 4])[0]
        out.append(f'<rect x="{x}" y="{y}" width="2" height="2" fill="{c}"/>')
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false">{"".join(out)}</svg>'


def card_strings(gid):
    """חוטים עדינים לרקע של כרטיסי הבנטו."""
    return strands(gid, 600, 360, 18,
                   lambda t: f"M -40 {250 + 90 * t:.1f} C 160 {120 - 160 * t:.1f}, 380 {330 + 120 * t:.1f}, 660 {90 + 200 * t:.1f}",
                   stops=[(0, "#2DD4BF", .1), (.5, "#4ADE80", .55), (1, "#A3E635", .2)], cls="b-str", width=.8)


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
}


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def head(line1, line2, btn_href=None, btn_text=None, extra=""):
    """כותרת מקטע בשני צבעים (שורה כהה + שורה אפורה), עם כפתור בצד."""
    b = f'<a href="{btn_href}" class="btn">{btn_text} <span class="arr">←</span></a>' if btn_href else ""
    return f'<div class="m-head"><h2>{line1}<span>{line2}</span></h2><div class="m-head-act">{extra}{b}</div></div>'


# ---------------------------------------------------------------------
# המקטעים
# ---------------------------------------------------------------------
def sec_tools(n_chapters, n_minutes, n_articles):
    tools = [("Claude", "המוח שעונה וחושב"), ("Claude Code", "הבנאי שבונה בשבילכם"), ("GitHub", "המחסן של הפרויקטים"),
             ("4CODE", "איפה שהאתר גר"), ("Supabase", "מאגר המידע"), ("Google Drive", "הגיבוי של הלילה"),
             ("Skills", "יכולות מוכנות"), ("Connectors", "חיבור לשירותים")]
    tiles = "".join(f'<li class="tool"><b dir="ltr">{a}</b><small>{b}</small></li>' for a, b in tools)
    items = [("פרקים במדריך", n_chapters), ("שיעורי וידאו", 8), ("דקות קריאה", n_minutes), ("מאמרים", n_articles),
             ("מחיר", "₪0"), ("שורות קוד שתכתבו", 0), ("בעברית", "100%")]
    run = "".join(f'<span class="tk">{a} <b>{b}</b></span>' for a, b in items)
    return f'''
    <section class="m-sec m-tools">
        <div class="m-in tools-in">
            <div class="tools-txt">
                <p>כל <b>הכלים</b> שתפגשו בדרך, <b>ומה כל אחד</b> עושה.</p>
                <a href="guide-1.html" class="btn">למדריך המלא <span class="arr">←</span></a>
            </div>
            <ul class="tools-grid">{tiles}</ul>
        </div>
    </section>
    <section class="m-sec m-ticker" aria-label="הקורס במספרים">
        <div class="m-in ticker-in">
            <span class="tk-label">מה מחכה לכם</span>
            <div class="tk-view"><div class="tk-run">{run}{run.replace('class="tk"', 'class="tk" aria-hidden="true"')}</div></div>
        </div>
    </section>'''


def sec_bento():
    ask = f'<div class="mk-ask"><span class="spark">✦</span><span class="t">תבנה לי אתר לנגרייה, עם גלריה וטופס</span><span class="go">{icon("send")}</span></div>'
    check = '<ul class="mk-list">' + "".join(
        f'<li class="{c}"><i>{icon("check") if c == "done" else ""}</i><span>{t}</span></li>'
        for c, t in [("done", "פותחים חשבון קלוד"), ("done", "מתקינים את האפליקציה"), ("now", "פותחים GitHub"), ("", "בונים אתר ראשון")]) + '</ul>'
    roles = '<ul class="mk-roles">' + "".join(
        f'<li class="{c}"><i></i><span>{t}</span><em>{e}</em></li>'
        for c, t, e in [("", "שואל לפני כל שינוי", "זהיר"), ("on", "עורך קבצים לבד", "מומלץ"), ("", "עושה הכול בלי לשאול", "מהיר")]) + '</ul>'
    conn = ('<div class="mk-conn"><span class="c1" dir="ltr">GH</span><i></i><span class="c0">'
            '<img src="assets/images/logo/favicon.svg" alt=""></span><i></i><span class="c2" dir="ltr">SB</span></div>'
            '<div class="mk-conn-l"><span>GitHub</span><span>Free AI</span><span>Supabase</span></div>')
    chips = '<div class="mk-chips">' + "".join(f'<span class="{c}">{t}</span>' for c, t in [
        ("on", "/בדיקת-אבטחה"), ("", "/מאמר-חדש"), ("", "/תמונות"), ("on", "/קידום-בגוגל"), ("", "/גיבוי")]) + '</div>'
    site = ('<div class="mk-site"><div class="bar"><span></span><span></span><span></span><em dir="ltr">nagariya.co.il</em>'
            '<b class="live"><i></i>באוויר</b></div><div class="body"><div class="hero"><b>נגרות יוסי</b><small>רהיטים בהזמנה אישית</small>'
            '<em>צרו קשר</em></div><div class="gal"><i></i><i></i><i></i><i></i></div></div></div>')
    cards = [
        ("w2", "כותבים בעברית, קלוד קוד בונה", ask, "b1"),
        ("", "מדריך שזוכר איפה עצרתם", check, "b2"),
        ("", "מחליטים כמה קלוד עושה לבד", roles, "b3"),
        ("", "מחברים לשירותים שאתם כבר משתמשים בהם", conn, "b4"),
        ("", "סקילים: יכולות מוכנות להורדה", chips, "b5"),
        ("w3", "מהרעיון לאתר שעובד באוויר", site, "b6"),
    ]
    html = "".join(f'<li class="bento-c {w}">{card_strings(g)}<div class="mk">{m}</div><h3>{t}</h3></li>' for w, t, m, g in cards)
    return f'''
    <section class="m-sec">
        <div class="m-in">
            {head("כל מה שצריך לאתר הראשון.", "בלי לכתוב שורת קוד.", "service.html", "התחל ללמוד")}
            <ul class="bento">{html}</ul>
        </div>
    </section>'''


def sec_stories():
    stories = [
        ("green", "אתר לעסק", 'כותבים <b>הודעה אחת בעברית</b> ומקבלים אתר עם גלריה וטופס', [("1", "הודעה בעברית"), ("0", "שורות קוד שאתם כותבים")],
         "article-what-is-claude-code.html", "assets/images/claude/build-site.jpg"),
        ("ink", "גיבוי אוטומטי", '<b>כל הפרויקטים</b> נשמרים לבד בגוגל דרייב, כל לילה', [("03:00", "כל לילה"), ("₪0", "עלות")],
         "article-github-backup.html", "assets/images/guide/backup-1.png"),
        ("orange", "מעלים לאוויר", 'האתר מקבל <b>כתובת אמיתית</b> שאפשר לשלוח לכל אחד', [("1", "כתובת לשתף"), ("30", "ימים בחינם עם הקופון")],
         "guide-18.html", "assets/images/guide/claude-map.png"),
    ]
    cards = "".join(f'''<li class="story s-{c}">
                <div class="st-l"><span class="st-dots" aria-hidden="true"></span><span class="st-tag">{tag}</span><h3>{t}</h3>
                    <div class="st-nums">{"".join(f'<div><strong dir="ltr">{a}</strong><small>{b}</small></div>' for a, b in nums)}</div>
                    <a href="{href}" class="btn-2">לסיפור המלא <span class="arr">←</span></a></div>
                <div class="st-img"><img src="{img}" alt="{tag}" loading="lazy"></div>
            </li>''' for c, tag, t, nums, href, img in stories)
    nav = (f'<div class="car-nav"><button type="button" class="btn-2 ic" data-car="-1" aria-label="הקודם">{icon("chev-r")}</button>'
           f'<button type="button" class="btn-2 ic" data-car="1" aria-label="הבא">{icon("chev-l")}</button></div>')
    return f'''
    <section class="m-sec m-stories">
        <div class="m-in">{head("מה בונים עם קלוד קוד.", "שלוש דוגמאות מהמדריך ומהמאמרים.", "articles.html", "לכל המאמרים", nav)}</div>
        <div class="car" id="car"><ul class="car-track">{cards}</ul></div>
    </section>'''


def sec_scale(n_chapters):
    stats = [("chart", str(n_chapters), "פרקים קצרים במדריך"), ("play", "8", "שיעורי וידאו לפי הסדר"), ("coin", "₪0", "מחיר הקורס, תמיד")]
    st = "".join(f'<li>{icon(i)}<strong dir="ltr">{a}</strong><span>{b}</span></li>' for i, a, b in stats)
    return f'''
    <section class="m-sec m-scale">
        <div class="m-in">
            {head("לומדים בקצב שלכם.", "פרקים קצרים, צעד אחד בכל פעם.", "guide-1.html", "לפרק הראשון")}
            <div class="wave-box">{wave("wv")}</div>
            <ul class="stats">{st}</ul>
        </div>
    </section>'''


def sec_start(n_chapters):
    items = [("p-pink", "play", "הקורס", "8 שיעורי וידאו, לפי הסדר.", "service.html", "לקורס"),
             ("p-mint", "book", "המדריך", f"{n_chapters} פרקים לקריאה, צעד אחרי צעד.", "guide-1.html", "למדריך"),
             ("p-night", "spark", "סקילים", "יכולות מוכנות לקלוד, להורדה בחינם.", "work.html", "לסקילים"),
             ("p-fire", "file", "מאמרים", "מדריכים קצרים שאפשר לעשות היום.", "articles.html", "למאמרים")]
    cards = "".join(f'''<li class="start">
                <a href="{h}" class="start-art {c}">{art_strings("as" + str(k))}<span class="start-tile">{icon(i)}</span></a>
                <p><b>{t}</b> {d}</p><a href="{h}" class="start-go">{g} <span class="arr">←</span></a>
            </li>''' for k, (c, i, t, d, h, g) in enumerate(items))
    return f'''
    <section class="m-sec">
        <div class="m-in">
            {head("מאיפה מתחילים.", "ארבע דרכים להיכנס לחומר.", "service.html", "התחל ללמוד")}
            <ul class="starts">{cards}</ul>
        </div>
    </section>'''


def sec_prompts():
    items = [("cut", "מספרה", "יומן תורים", "תבנה לי יומן תורים למספרה, שהלקוחות יקבעו לבד ויקבלו תזכורת בוואטסאפ."),
             ("cake", "קונדיטוריה", "אתר עם הזמנות", "תבנה אתר לקונדיטוריה שלי עם תפריט עוגות, תמונות וטופס הזמנה לאירועים."),
             ("home", "שיפוצים", "עמוד נחיתה", "תכין עמוד אחד לקבלן שיפוצים: לפני ואחרי, המלצות וכפתור וואטסאפ."),
             ("bag", "חנות קטנה", "קטלוג מוצרים", "תבנה קטלוג ל-30 מוצרים עם מחירים, חיפוש וכפתור 'להזמנה'."),
             ("dumbbell", "מאמן כושר", "מעקב מתאמנים", "תבנה מערכת קטנה שאני רושם בה אימונים של כל מתאמן ורואה התקדמות."),
             ("camera", "צלמת", "גלריה ללקוחות", "תבנה גלריה שכל לקוח נכנס עם קוד ורואה רק את התמונות שלו.")]
    cards = "".join(f'''<li class="pr"><div class="pr-h"><span class="pr-ic">{icon(i)}</span><div><b>{a}</b><small>{b}</small></div></div>
                <p>"{t}"</p></li>''' for i, a, b, t in items)
    return f'''
    <section class="m-sec">
        <div class="m-in">
            {head("מה כותבים לקלוד קוד.", "הודעות אמיתיות, בעברית רגילה.", "guide-16.html", "איך כותבים בקשה טובה")}
            <ul class="prompts">{cards}</ul>
        </div>
    </section>'''


def sec_posts(articles):
    arts = ["p-forest", "p-deep", "p-sand"]
    icons_ = ["file", "clock", "book"]
    posts = [(n, t) for n, t, d, m in articles][:2] + [("articles.html", "כל המאמרים במקום אחד")]
    cards = "".join(f'''<li class="post"><a href="{n}">
                <span class="post-art {arts[k]}">{art_strings("ps" + str(k))}<span class="start-tile">{icon(icons_[k])}</span></span>
                <span class="post-meta"><em>{"מאמר" if k < 2 else "מאמרים"}</em>{"2026" if k < 2 else ""}</span>
                <b>{t}</b></a></li>''' for k, (n, t) in enumerate(posts))
    return f'''
    <section class="m-sec">
        <div class="m-in">
            {head("מאמרים אחרונים.", "קצרים, ואפשר לעשות אותם היום.", "articles.html", "לכל המאמרים")}
            <ul class="posts">{cards}</ul>
        </div>
    </section>'''


def sec_cta():
    s = strands("cta", 760, 260, 22,
                lambda t: f"M -20 {250 + 30 * t:.1f} C 200 {230 - 120 * t:.1f}, 420 {120 + 140 * t:.1f}, 780 {20 + 120 * t:.1f}", cls="cta-str")
    return f'''
    <section class="m-sec m-cta">
        <div class="m-in cta-in">
            {s}
            <h2>קורס קלוד קוד, בחינם ובעברית</h2>
            <div class="btns"><a href="guide-1.html" class="btn-2">למדריך הכתוב</a><a href="service.html" class="btn">התחל ללמוד <span class="arr">←</span></a></div>
        </div>
    </section>'''


def sec_faq(faq_html):
    return f'''
    <section class="m-sec">
        <div class="m-in faq-in">
            <h2 class="faq-t">שאלות נפוצות</h2>
            {faq_html}
        </div>
    </section>'''


def footer(chapters, articles, ready):
    cols = [
        ("לומדים", [("service.html", "הקורס"), ("guide-1.html", "המדריך"), ("work.html", "סקילים"), ("articles.html", "מאמרים")]),
        ("המדריך", [(f"guide-{i}.html", chapters[i - 1][0]) for i in (1, 3, 5, 16, 18) if i in ready]),
        ("מאמרים", [(n, t.split("?")[0] + ("?" if "?" in t else "")) for n, t, d, m in articles]),
        ("מידע", [("privacy.html", "פרטיות"), ("terms.html", "תנאי שימוש")]),
    ]
    c = "".join(f'<div class="f-col"><h3>{h}</h3><ul>{"".join(f"<li><a href=\"{a}\">{b}</a></li>" for a, b in links)}</ul></div>' for h, links in cols)
    return f'''
    <footer class="m-foot">
        {dots(7, 160, 420, 90, "dither f-d1")}{dots(11, 160, 420, 90, "dither f-d2")}
        <div class="m-in foot-in">
            <div class="f-brand"><a href="index.html" class="c-logo"><img src="assets/images/logo/logo.svg" alt="Free AI"></a>
                <span class="f-ok">{len(ready)} פרקים זמינים לקריאה</span></div>
            <nav class="f-cols" aria-label="קישורים בפוטר">{c}</nav>
        </div>
        <div class="m-in f-bot">
            <span>© 2026 Free AI. כל הזכויות שמורות.</span>
            <a href="#top" class="f-top">חזרה למעלה {icon("up")}</a>
        </div>
    </footer>'''


HOME_JS = '''<script>
(function () {
  var car = document.getElementById('car');
  if (!car) return;
  document.querySelectorAll('[data-car]').forEach(function (b) {
    b.addEventListener('click', function () {
      var card = car.querySelector('.story');
      var step = card ? card.getBoundingClientRect().width + 12 : 600;
      car.scrollBy({ left: -step * +b.dataset.car, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    });
  });
})();
</script>'''


def body(header_html, hero_demo, strings, chapters, ready, articles, faq_html):
    n_ch = len(chapters)
    mins = sum(m for _, m in chapters)
    return f'''    <div class="wrap full" id="top">
        <section class="c-hero">
        {strings}
        {header_html}
            <div class="hero-in">
                <div class="hero-text">
                    <span class="chip">המדריך הכתוב <b>{n_ch} פרקים</b></span>
                    <h1 class="hero-title"><span class="hero-line"><span class="grad">קורס קלוד קוד בחינם</span></span></h1>
                    <p>קורס Claude Code בעברית למתחילים, בלי ידע בתכנות: <b>שיעורי וידאו</b>, <b>מדריך כתוב</b> צעד אחרי צעד ו<b>סקילים</b> מוכנים להורדה.</p>
                    <div class="btns"><a href="service.html" class="btn">התחל ללמוד <span class="arr">←</span></a><a href="guide-1.html" class="btn-2">למדריך הכתוב</a></div>
                    <span class="hero-note"><i></i>חינם ובעברית, בלי לדעת לתכנת</span>
                </div>
                {hero_demo}
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
{footer(chapters, articles, ready)}'''
