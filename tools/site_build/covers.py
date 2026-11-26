"""תמונות שער למאמרים: רקע צבעוני עם חוטים, ועליו לוחות זכוכית שקופים (כמו בסקיל העריכה של הרילס).

הרצה: python3 tools/site_build/covers.py  → site/assets/images/articles/<שם>.webp (680x590, בחדות כפולה)
מאמר חדש: מוסיפים רשומה ל-COVERS עם צבע ותוכן הלוחות (HTML).
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent.parent / "site"
OUT = SITE / "assets" / "images" / "articles"
sys.path.insert(0, str(HERE))
import home_mint  # noqa: E402

FONT = (SITE / "assets/fonts/files/kobi").as_uri()
BR = (SITE / "assets/images/brands").as_uri()

CSS = f"""
@font-face {{ font-family: Kobi; src: url({FONT}/Kobi-Regular.woff2); font-weight: 400; }}
@font-face {{ font-family: Kobi; src: url({FONT}/Kobi-SemiBold.woff2); font-weight: 600; }}
@font-face {{ font-family: Kobi; src: url({FONT}/Kobi-Bold.woff2); font-weight: 700; }}
@font-face {{ font-family: Kobi; src: url({FONT}/Kobi-Black.woff2); font-weight: 900; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 680px; height: 590px; overflow: hidden; }}
body {{ font-family: Kobi, sans-serif; direction: rtl; color: #fff; position: relative; background: var(--bg); }}
.bg {{ position: absolute; inset: 0; background: radial-gradient(120% 90% at 85% 10%, var(--hi) 0%, transparent 55%), radial-gradient(90% 80% at 10% 100%, var(--lo) 0%, transparent 60%), var(--bg); }}
.art-str {{ position: absolute; inset: -10% -5%; width: 110%; height: 120%; opacity: .55; }}
.blob {{ position: absolute; border-radius: 50%; filter: blur(40px); opacity: .55; }}
.glass {{ position: absolute; border-radius: 20px; padding: 18px 20px;
  background: linear-gradient(160deg, rgba(255,255,255,.30), rgba(255,255,255,.08));
  border: 1px solid rgba(255,255,255,.45); box-shadow: 0 20px 40px -18px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.35);
  backdrop-filter: blur(16px) saturate(140%); -webkit-backdrop-filter: blur(16px) saturate(140%); }}
.lab {{ font-size: 13px; font-weight: 600; letter-spacing: .02em; opacity: .8; margin-bottom: 8px; }}
.big {{ font-size: 21px; font-weight: 700; line-height: 1.3; }}
.row {{ display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 12px; background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.25); font-size: 15px; font-weight: 600; margin-top: 8px; }}
.row i {{ width: 22px; height: 22px; border-radius: 6px; background: rgba(255,255,255,.85); flex: none; display: grid; place-items: center; color: var(--bg); font-style: normal; font-size: 13px; font-weight: 900; }}
.chip {{ display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 999px; font-size: 15px; font-weight: 700; }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: #9EF0B0; box-shadow: 0 0 10px #9EF0B0; }}
.logo {{ height: 26px; width: auto; filter: brightness(0) invert(1); }}
.bar {{ height: 8px; border-radius: 4px; background: rgba(255,255,255,.35); margin-top: 8px; }}
.arrow {{ position: absolute; font-size: 30px; font-weight: 900; opacity: .9; }}
"""


def page(bg, hi, lo, inner):
    strings = home_mint.art_strings("s", "#FFFFFF")
    return (f'<!doctype html><html lang="he"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body style="--bg:{bg};--hi:{hi};--lo:{lo}"><div class="bg"></div>{strings}{inner}</body></html>')


SEC_ROWS = [("#FF9A8A", "מפתח סודי חשוף בקוד", "לתקן עכשיו"), ("#FFD08A", "אין הגבלה על ניסיונות כניסה", "בקרוב"), ("#A8F0BE", "חיבור מוצפן", "תקין")]
SPEED_ROWS = [("#FF9A8A", "תמונות כבדות בעמוד הבית", "-2.4s"), ("#FFD08A", "השרת רחוק מישראל", "-0.8s"), ("#FFD08A", "פונט נטען לפני הטקסט", "-0.4s")]


def skill_page(bg, hi, lo, prompt, rows, wide=False):
    """שער של סקיל: אותו סגנון כמו שערי המאמרים (רקע בצבעי המותג, חוטים, לוחות זכוכית)."""
    w, h = (1080, 520) if wide else (680, 590)
    rr = "".join(f'<div class="row" style="justify-content:space-between"><span style="display:flex;align-items:center;gap:10px">'
                 f'<span style="width:9px;height:9px;border-radius:50%;background:{c}"></span>{t}</span>'
                 f'<span style="opacity:.85;direction:ltr">{m}</span></div>' for c, t, m in rows)
    if wide:
        a = 'top:70px;right:80px;width:380px'; b = 'top:205px;right:300px;width:400px'
    else:
        a = 'top:60px;right:48px;width:340px'; b = 'top:230px;left:44px;width:390px'
    inner = (f'<div class="blob" style="width:280px;height:280px;background:{hi};top:30px;right:60px"></div>'
             f'<div class="blob" style="width:220px;height:220px;background:#E6BB35;bottom:20px;left:80px;opacity:.3"></div>'
             f'<div class="glass" style="{a}"><div class="lab">אתם כותבים</div><div class="big">{prompt}</div></div>'
             f'<div class="glass" style="{b}"><div class="lab">הדוח</div>{rr}</div>')
    html = page(bg, hi, lo, inner)
    return html.replace("<style>", f"<style>html,body{{width:{w}px!important;height:{h}px!important}}", 1)


COVERS = {
    # מה זה קלוד קוד: הודעה בעברית → אתר שנבנה
    "article-what-is-claude-code": page("#5C1E0F", "#C8553A", "#2A0C05", f"""
<div class="blob" style="width:260px;height:260px;background:#F0A27F;top:40px;right:60px"></div>
<div class="blob" style="width:200px;height:200px;background:#E6BB35;bottom:30px;left:70px;opacity:.35"></div>
<div class="glass" style="top:62px;right:48px;width:330px">
  <div class="lab">אתם כותבים</div>
  <div class="big">תבנה לי אתר לנגרייה, עם תמונות של עבודות וטופס</div>
</div>
<div class="glass chip" style="top:268px;right:120px"><span style="font-size:18px">✦</span>קלוד קוד בונה…</div>
<div class="glass" style="top:215px;left:44px;width:300px;padding:14px">
  <div style="display:flex;gap:6px;margin-bottom:12px"><span style="width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.6)"></span><span style="width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.4)"></span><span style="width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.3)"></span></div>
  <div style="font-size:22px;font-weight:900">נגרות יוסי</div>
  <div style="font-size:13px;opacity:.85;margin-top:2px">רהיטים בהזמנה אישית</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:12px"><span style="height:62px;border-radius:8px;background:rgba(255,255,255,.35)"></span><span style="height:62px;border-radius:8px;background:rgba(255,255,255,.22)"></span><span style="height:62px;border-radius:8px;background:rgba(255,255,255,.3)"></span></div>
  <div class="bar" style="width:70%"></div><div class="bar" style="width:45%"></div>
</div>
<div class="glass chip" style="bottom:46px;right:48px"><span class="dot"></span>האתר באוויר</div>
"""),
    # גיבוי: GitHub → גוגל דרייב כל לילה
    "article-github-backup": page("#2F47B8", "#6C86F0", "#121F5C", f"""
<div class="blob" style="width:260px;height:260px;background:#8FA4FF;top:30px;right:40px"></div>
<div class="blob" style="width:220px;height:220px;background:#7FD8C4;bottom:20px;left:50px;opacity:.35"></div>
<div class="glass" style="top:70px;right:44px;width:270px">
  <img class="logo" src="{BR}/github-mark.svg">
  <div class="row"><i>1</i>אתר הנגרייה</div>
  <div class="row"><i>2</i>יומן תורים</div>
  <div class="row"><i>3</i>חנות</div>
</div>
<div class="glass chip" style="bottom:46px;left:44px"><span style="font-size:19px;font-weight:900;direction:ltr">03:00</span><span style="opacity:.85">כל לילה</span></div>
<div class="glass" style="top:190px;left:44px;width:260px">
  <div style="font-size:19px;font-weight:900">Google Drive</div>
  <div class="row" style="direction:ltr;justify-content:flex-end">site.zip<i>✓</i></div>
  <div class="row" style="direction:ltr;justify-content:flex-end">calendar.zip<i>✓</i></div>
  <div class="row" style="direction:ltr;justify-content:flex-end">shop.zip<i>✓</i></div>
</div>
<div class="glass chip" style="bottom:46px;right:44px"><span class="dot"></span>גיבוי הושלם</div>
"""),
    # מחיר: חשבון חודשי של Pro
    "article-claude-code-price": page("#9A3B22", "#E08A63", "#4A170A", """
<div class="blob" style="width:260px;height:260px;background:#F4B08F;top:30px;right:50px"></div>
<div class="blob" style="width:200px;height:200px;background:#E6BB35;bottom:30px;left:60px;opacity:.35"></div>
<div class="glass" style="top:60px;right:48px;width:330px">
  <div class="lab">החשבון החודשי</div>
  <div class="row" style="justify-content:space-between"><span>מנוי Claude Pro</span><span style="direction:ltr">$20</span></div>
  <div class="row" style="justify-content:space-between"><span>קלוד קוד</span><span>כלול ✓</span></div>
  <div class="row" style="justify-content:space-between"><span>הקורס של Free AI</span><span style="direction:ltr">$0</span></div>
</div>
<div class="glass" style="top:290px;left:44px;width:250px">
  <div class="lab">סה״כ לחודש</div>
  <div style="font-size:54px;font-weight:900;line-height:1;direction:ltr;text-align:end">$20</div>
</div>
<div class="glass chip" style="bottom:46px;right:48px"><span class="dot"></span>Max ‏$100 · Ultra ‏$200</div>
"""),
    # סקילים: כמו שערי המאמרים, בצבעי המותג
    "skill-security": skill_page("#0E4A39", "#2E9B78", "#05261C", "תבדוק לי את האבטחה של האתר", SEC_ROWS),
    "skill-site-speed": skill_page("#1F2766", "#5462D8", "#0D1238", "האתר שלי איטי, תבדוק", SPEED_ROWS),
    "skill-security-wide": skill_page("#0E4A39", "#2E9B78", "#05261C", "תבדוק לי את האבטחה של האתר", SEC_ROWS, wide=True),
    "skill-site-speed-wide": skill_page("#1F2766", "#5462D8", "#0D1238", "האתר שלי איטי, תבדוק", SPEED_ROWS, wide=True),
}



# ---------------------------------------------------------------- שערים בסגנון כרטיסי "לומדים" בדף הבית:
# כל שער צבע אחר וציור קווים אחר, בלי לוחות ובלי טקסט (הכותרת יושבת על הכרטיס עצמו).
import math as _m


def _poly(fn, w, h, steps=80):
    pts = []
    for j in range(steps + 1):
        u = j / steps
        x, y = fn(u)
        pts.append(f"{x * w:.1f} {y * h:.1f}")
    return "M " + " L ".join(pts)


def _bundle(n, line, w, h):
    """n קווים; line(t, u) מחזיר נקודה (x, y) בין 0 ל-1, t בין -0.5 ל-0.5."""
    return "".join(f'<path d="{_poly(lambda u, t=i / (n - 1) - .5: line(t, u), w, h)}"/>' for i in range(n))


PATTERNS = {
    # מניפה: קווים שיורדים מלמעלה ומתכנסים לפינה
    "fan": lambda t, u: (0.38 + 0.5 * t * (1 - u) ** 1.6 + 0.62 * u ** 1.4, -0.05 + 1.1 * u + 0.08 * t * (1 - u)),
    # שדה: קווים מקבילים וגליים על כל השטח
    "field": lambda t, u: (-0.05 + 1.1 * u, 0.5 + 1.4 * t + 0.07 * _m.sin(2 * _m.pi * (u * 1.15 + t * 0.6))),
    # סחיפה: צרור רוחבי שמתכנס באמצע
    "sweep": lambda t, u: (-0.05 + 1.1 * u, 0.42 + 0.18 * _m.sin(_m.pi * u * 1.3) + t * (0.55 * abs(u - 0.55) + 0.03)),
    # אס: צרור שעולה מהפינה התחתונה לפינה העליונה
    "s": lambda t, u: (-0.05 + 1.1 * u, 1.0 - u + 0.16 * _m.sin(2 * _m.pi * u) + t * (0.08 + 0.5 * u ** 2)),
    # שעון חול: קווים שנפרשים למעלה ולמטה ונפגשים באמצע
    "hourglass": lambda t, u: (0.5 + 0.06 * _m.sin(_m.pi * u * 2) + t * 1.4 * abs(u - 0.5) ** 1.2 + t * 0.02, -0.05 + 1.1 * u),
}


def art(bg, pattern, stroke="#FFFFFF", op=(.15, .7, .25), n=44, width=1.0, wide=False):
    w, h = (1080, 520) if wide else (680, 590)
    gid = "g"
    lines = _bundle(n, PATTERNS[pattern], w, h)
    a, b, c = op
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0}}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}</style></head><body>'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}">'
            f'<stop offset="0" stop-color="{stroke}" stop-opacity="{a}"/><stop offset=".5" stop-color="{stroke}" stop-opacity="{b}"/>'
            f'<stop offset="1" stop-color="{stroke}" stop-opacity="{c}"/></linearGradient></defs>'
            f'<g fill="none" stroke="url(#{gid})" stroke-width="{width}">{lines}</g></svg></body></html>')


ART = {
    "article-what-is-claude-code": dict(bg="#FF4300", pattern="fan", stroke="#FFE08A"),
    "article-github-backup": dict(bg="#4BE3AC", pattern="field", stroke="#0B5A3E", op=(.35, .45, .35), n=40, width=.9),
    "article-claude-code-price": dict(bg="linear-gradient(160deg,#A8261C,#7E140E)", pattern="sweep", op=(.05, .5, .15)),
    "article-vibe-coding": dict(bg="linear-gradient(160deg,#E6BB35,#D97757)", pattern="s", stroke="#5A1E0B", op=(.15, .55, .2)),
    "article-claude-skills": dict(bg="linear-gradient(160deg,#2B4C7E,#132544)", pattern="fan", stroke="#BFD6FF", op=(.1, .6, .2)),
    "skill-security": dict(bg="linear-gradient(160deg,#103B2C,#071E16)", pattern="s", op=(.1, .75, .2)),
    "skill-site-speed": dict(bg="linear-gradient(150deg,#FF2D55,#E83EC2 55%,#7C6CF2)", pattern="hourglass", op=(.6, .25, .6)),
    # קורסים
    "course-lovable": dict(bg="linear-gradient(150deg,#FF6A3D,#F2387C 55%,#7A5CF0)", pattern="sweep", op=(.15, .7, .25)),
    "course-claude-code": dict(bg="linear-gradient(160deg,#D97757,#9A3B22)", pattern="fan", stroke="#FFE7D6", op=(.1, .6, .2)),
}
for _k, _v in ART.items():
    COVERS[_k] = art(**_v)
    if _k.startswith(("skill-", "course-")):
        COVERS[_k + "-wide"] = art(**_v, wide=True)

SHOT = """
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:680,height:590},deviceScaleFactor:2});
for(const [src,dst,w,h] of JSON.parse(process.argv[2])){await p.setViewportSize({width:w,height:h});await p.goto('file://'+src);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);await p.screenshot({path:dst});}
await b.close();})();
"""


def build(only=None):
    import json, tempfile
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())
    jobs = []
    for name, html in COVERS.items():
        if only and name not in only:
            continue
        (tmp / f"{name}.html").write_text(html)
        w, h = (1080, 520) if name.endswith("-wide") else (680, 590)
        jobs.append([str(tmp / f"{name}.html"), str(tmp / f"{name}.png"), w, h])
    (tmp / "shot.js").write_text(SHOT)
    subprocess.run(["node", str(tmp / "shot.js"), json.dumps(jobs)], check=True)
    for src, png, *_ in jobs:
        name = Path(src).stem
        Image.open(png).convert("RGB").save(OUT / f"{name}.webp", quality=86, method=6)
        print(f"cover {name}.webp")


def cover(href):
    """הנתיב לתמונת השער של מאמר (או None אם אין)."""
    name = href.removesuffix(".html")
    return f"assets/images/articles/{name}.webp?v=4" if (OUT / f"{name}.webp").exists() else None


if __name__ == "__main__":
    build(sys.argv[1:] or None)
