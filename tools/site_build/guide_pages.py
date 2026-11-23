"""המדריך המלא ל-Claude Code – בסגנון קורס: רשימת פרקים בצד, פרק קצר באמצע.

עמוד לכל פרק (guide-N.html). נבנה מתוך site/service-single.html כדי לרשת תפריט, פוטר ועיצוב.
ההתקדמות נשמרת כרגע בדפדפן של הגולש (localStorage) עד שיחובר אזור משתמשים.
הרצה: cd tools/site_build && python3 guide_pages.py
"""
from clean_urls import clean
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
COUPON = "RVJ34jcn4j1"

# שם קצר לתפריט הצד, ושם קובץ לפרקים שכבר עלו
CHAPTERS = [
    "לפני שמתחילים",
    "Claude מול Claude Code",
    "פותחים חשבון Claude",
    "מתקינים את האפליקציה",
    "פותחים GitHub",
    "פותחים 4CODE",
    "Supabase הוא בעצם דאטה בייס (מסד נתונים)",
    "הפרויקט הראשון",
    "מעלים לאוויר",
    "איך מדברים עם Claude Code",
    "סדר ובטיחות",
    "כשמשהו נתקע",
    "השלב הבא",
]
READY = {1}  # פרקים שכבר כתובים

CSS = '''
        .guide-course { padding: 150px 0 72px; }
        .guide-wrap { display: grid; grid-template-columns: 340px minmax(0, 1fr); gap: 24px; align-items: start; }
        .guide-card { background: var(--neutral-100, #F4F4F5); border-radius: 32px; box-shadow: 0px 7.77px 16px 0px rgba(0,0,0,.06), 0px 3px 3px 0px rgba(0,0,0,.1), 0px -8px 0px 0px rgba(0,0,0,.05) inset, 0px 4px 0px 0px rgba(255,255,255,.6) inset; }
        .guide-side { padding: 24px 20px 28px; position: sticky; top: 24px; }
        .guide-side h2 { font-size: 19px; line-height: 1.3; font-weight: 700; margin: 0 6px 12px; letter-spacing: 0; }
        .guide-bar { height: 8px; border-radius: 99px; background: #DAD7D2; overflow: hidden; margin: 0 6px 6px; }
        .guide-bar i { display: block; height: 100%; width: 0; border-radius: 99px; background: var(--brand, #D97757); transition: width .4s; }
        .guide-count { font-size: 13px; color: #8d8985; margin: 0 6px 12px; font-weight: 600; }
        .guide-chapters { list-style: none; margin: 0; padding: 0; display: grid; gap: 4px; }
        .guide-ch { display: flex; align-items: center; gap: 12px; padding: 11px 12px; border-radius: 14px; font-size: 16px; font-weight: 600; color: #8d8985; text-decoration: none; }
        a.guide-ch:hover { color: #1F1E1D; }
        .guide-ch.is-on { background: #fff; color: #1F1E1D; box-shadow: 0 4px 12px rgba(0,0,0,.07); }
        .guide-ch.is-done { color: #1F1E1D; }
        .guide-dot { flex: 0 0 auto; width: 24px; height: 24px; border-radius: 50%; border: 2px solid #CFCBC5; display: flex; align-items: center; justify-content: center; font-size: 13px; line-height: 1; color: transparent; }
        .guide-ch.is-on .guide-dot { border-color: var(--brand, #D97757); }
        .guide-ch.is-done .guide-dot { border-color: var(--brand, #D97757); background: var(--brand, #D97757); color: #fff; }
        .guide-soon { margin-inline-start: auto; font-size: 12px; font-weight: 600; opacity: .7; white-space: nowrap; }
        .guide-main { padding: 48px 52px; display: flex; flex-direction: column; gap: 22px; min-height: 640px; }
        .guide-tag { align-self: flex-start; font-size: 14px; font-weight: 700; color: var(--brand, #D97757); background: #fff; border-radius: 10px; padding: 6px 14px; box-shadow: 0 2px 0 rgba(0,0,0,.08); }
        .guide-main h1 { font-size: 56px; line-height: 1.1; font-weight: 700; letter-spacing: -.02em; margin: 0; }
        .guide-sub { font-size: 21px; line-height: 1.5; color: #6b6763; margin: 0; }
        .guide-rows { list-style: none; margin: 4px 0 0; padding: 0; display: grid; gap: 12px; }
        .guide-row { display: flex; align-items: center; gap: 16px; background: #fff; border-radius: 18px; padding: 14px 18px; font-size: 19px; font-weight: 600; }
        .guide-row small { margin-inline-start: auto; font-size: 16px; font-weight: 500; color: #8d8985; text-align: end; }
        .guide-num { flex: 0 0 auto; width: 52px; height: 52px; border-radius: 15px; background: var(--brand, #D97757); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700; box-shadow: 0 -3px 0 rgba(0,0,0,.18) inset, 0 10px 18px rgba(217,119,87,.35); }
        .guide-coupon { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; border: 1px dashed rgba(127,127,127,.5); border-radius: 18px; padding: 14px 18px; font-size: 16px; font-weight: 600; }
        .guide-coupon code { direction: ltr; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 17px; font-weight: 700; color: #1F1E1D; background: #fff; border-radius: 8px; padding: 5px 12px; user-select: all; }
        .guide-coupon button { border: 0; cursor: pointer; font-family: inherit; font-size: 14px; font-weight: 600; padding: 7px 16px; border-radius: 999px; background: #1F1E1D; color: #fff; }
        .guide-foot { margin-top: auto; padding-top: 12px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px; }
        .guide-foot .guide-note { font-size: 16px; color: #6b6763; }
        .guide-foot .tf-btn { cursor: pointer; border: 0; font-family: inherit; }
        .guide-foot .tf-btn.is-done { opacity: .55; pointer-events: none; }
        @media (max-width: 991px) {
            .guide-course { padding: 128px 0 48px; }
            .guide-wrap { grid-template-columns: minmax(0, 1fr); }
            .guide-side { position: static; order: 2; }
            .guide-main { padding: 28px 22px; min-height: 0; border-radius: 24px; }
            .guide-main h1 { font-size: 38px; }
            .guide-sub { font-size: 18px; }
            .guide-row { flex-wrap: wrap; font-size: 18px; gap: 6px 14px; }
            .guide-row small { flex-basis: 100%; margin-inline-start: 62px; text-align: start; font-size: 15px; margin-top: -14px; }
            .guide-num { width: 46px; height: 46px; font-size: 20px; }
            .guide-foot .tf-btn { width: 100%; justify-content: center; }
        }'''

JS = '''<script>
(function () {
    var KEY = 'freeai-guide-done', TOTAL = %(total)d, CURRENT = %(current)d;
    function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
    function save(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }
    var btn = document.getElementById('guide-done');
    function paint() {
        var done = load();
        document.querySelectorAll('.guide-ch').forEach(function (el) {
            el.classList.toggle('is-done', done.indexOf(+el.dataset.ch) > -1);
        });
        document.getElementById('guide-fill').style.width = Math.round(done.length / TOTAL * 100) + '%%';
        document.getElementById('guide-count').textContent = done.length + ' מתוך ' + TOTAL + ' פרקים';
        if (btn && done.indexOf(CURRENT) > -1 && !btn.dataset.next) { btn.textContent = 'סיימתם ✓ הפרק הבא בקרוב'; btn.classList.add('is-done'); }
    }
    if (btn) btn.addEventListener('click', function () {
        var done = load();
        if (done.indexOf(CURRENT) < 0) { done.push(CURRENT); save(done); }
        if (btn.dataset.next) location.href = btn.dataset.next; else paint();
    });
    var copy = document.getElementById('guide-copy');
    if (copy) copy.addEventListener('click', function () {
        navigator.clipboard.writeText(copy.dataset.code);
        copy.textContent = 'הועתק ✓';
    });
    paint();
})();
</script>'''


def sub1(html, pattern, repl):
    new, n = re.subn(pattern, repl, html, count=1, flags=re.S)
    assert n == 1, pattern
    return new


def sidebar(current):
    rows = []
    for i, name in enumerate(CHAPTERS, 1):
        cls = "guide-ch" + (" is-on" if i == current else "")
        inner = f'<span class="guide-dot">✓</span>{i}. {name}'
        if i in READY:
            rows.append(f'                        <li><a href="guide-{i}.html" class="{cls}" data-ch="{i}">{inner}</a></li>')
        else:
            rows.append(f'                        <li><span class="{cls}" data-ch="{i}">{inner}<span class="guide-soon">בקרוב</span></span></li>')
    return f'''<aside class="guide-card guide-side">
                    <h2>המדריך ל-Claude Code</h2>
                    <div class="guide-bar"><i id="guide-fill"></i></div>
                    <div class="guide-count" id="guide-count"></div>
                    <ol class="guide-chapters">
{chr(10).join(rows)}
                    </ol>
                </aside>'''


def build(n, minutes, sub, rows, note, extra=""):
    title = CHAPTERS[n - 1]
    html = (SITE / "service-single.html").read_text()
    html = sub1(html, r"<title>.*?</title>", lambda m: f"<title>{title} – המדריך ל-Claude Code | Free AI</title>")
    html = sub1(html, r'<meta name="description" content="[^"]*">',
                lambda m: f'<meta name="description" content="פרק {n} במדריך ל-Claude Code למי שלא מתכנת: {sub}">')
    html = html.replace("    </style>\n</head>", CSS + "\n    </style>\n</head>", 1)
    html = html.replace('class="item-link link1 active"', 'class="item-link link1"')
    html = html.replace('<a href="guide-1.html" class="item-link link1">', '<a href="guide-1.html" class="item-link link1 active">', 1)

    row_html = "\n".join(
        f'                        <li class="guide-row"><span class="guide-num">{i}</span>{name}<small>{detail}</small></li>'
        for i, (name, detail) in enumerate(rows, 1))
    nxt = f"guide-{n + 1}.html" if (n + 1) in READY else ""
    btn_attr = f' data-next="{nxt}"' if nxt else ""
    main = f'''<!-- guide -->
        <div class="guide-course">
            <div class="container">
                <div class="guide-wrap">
                {sidebar(n)}
                <article class="guide-card guide-main">
                    <span class="guide-tag">פרק {n} · {minutes}</span>
                    <h1>{title}</h1>
                    <p class="guide-sub">{sub}</p>
                    <ol class="guide-rows">
{row_html}
                    </ol>{extra}
                    <div class="guide-foot">
                        <span class="guide-note">{note}</span>
                        <button type="button" class="tf-btn" id="guide-done"{btn_attr}>סיימתי, לפרק הבא ←</button>
                    </div>
                </article>
                </div>
            </div>
        </div>
        <!-- /guide -->'''
    # כל התוכן בין התפריט לפוטר מוחלף בפריסת הקורס
    html = sub1(html, r"<!-- Hero Banner -->.*?<!-- /section-contact -->", lambda m: main)
    html = html.replace("\n</body>", "\n    " + JS % {"total": len(CHAPTERS), "current": n} + "\n</body>", 1)
    (SITE / f"guide-{n}.html").write_text(clean(html))
    print(f"guide-{n}.html done")


# =====================================================================
# פרק 1 – לפני שמתחילים
# =====================================================================
build(
    1, "2 דקות",
    "שלושה דברים להכין, ואפשר לצאת לדרך.",
    [
        ("מחשב", "Mac או Windows"),
        ("מייל", "אחד לכל השירותים"),
        ("כרטיס אשראי", "כ-20 דולר לחודש ל-Claude"),
    ],
    "כל השאר בחינם להתחלה",
    extra=f'''
                    <div class="guide-coupon">
                        <span>קופון לחודש ראשון בחינם ב-4CODE, האחסון של האתר:</span>
                        <code>{COUPON}</code>
                        <button type="button" id="guide-copy" data-code="{COUPON}">העתקה</button>
                    </div>''',
)
