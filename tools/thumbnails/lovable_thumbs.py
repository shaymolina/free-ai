"""Builds YouTube thumbnails for the Lovable course lessons (same style as 01-03).
Run: python3 tools/thumbnails/lovable_thumbs.py  -> site/assets/images/lovable-thumbs/NN.jpg
Needs: tools/thumbnails/persons/person{1..5}.png (cutouts), lucide-static in node_modules."""
import json, os, subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
ICONS = pathlib.Path(os.environ.get("LUCIDE", HERE / "node_modules/lucide-static/icons"))
OUT = ROOT / "site/assets/images/lovable-thumbs"
FONT = ROOT / "site/assets/fonts/files/kobi/Kobi-Black.woff2"

# num, top line (white, optional), pill (orange), center icon, 4 satellites
L = [
 (4, "דאטה בייס", "Supabase", "database", ["table", "key-round", "cloud", "server"]),
 (5, None, "תבניות", "layout-template", ["copy", "palette", "layout-grid", "sparkles"]),
 (6, "אפיון", "מוצר", "clipboard-list", ["target", "users", "lightbulb", "list-checks"]),
 (7, "הפרומפט", "הראשון", "message-square-text", ["sparkles", "send", "zap", "wand-sparkles"]),
 (8, "שליטה ב-", "Prompting", "sliders-horizontal", ["message-square", "brain", "wand-sparkles", "list-ordered"]),
 (9, "בניית", "מערכת", "boxes", ["workflow", "database", "code", "settings"]),
 (10, "עיצוב", "חלק א'", "palette", ["brush", "type", "layout-dashboard", "pipette"]),
 (11, "עיצוב", "חלק ב'", "pen-tool", ["palette", "square-mouse-pointer", "type", "image"]),
 (12, "חינם מול פרו", "מסלולים", "crown", ["gift", "credit-card", "badge-check", "layers"]),
 (13, "חיבור ל", "תשלומים", "credit-card", ["shopping-cart", "lock", "receipt", "wallet"]),
 (14, "התחברות עם", "Google", "log-in", ["user-round", "shield-check", "key-round", "mail"]),
 (15, "חיבור", "דומיין", "globe", ["link", "server", "shield-check", "at-sign"]),
 (16, "טופס לידים", "למייל", "mail", ["file-text", "send", "user-plus", "bell"]),
 (17, "הפינישים", "האחרונים", "flag", ["sparkles", "circle-check", "wand-sparkles", "rocket"]),
 (18, "ניהול משתמשים", "העברה ללקוח", "users", ["handshake", "user-cog", "key-round", "folder-output"]),
 (19, "העלאה לשרת", "חיצוני", "server", ["upload", "cloud", "github", "terminal"]),
 (20, "חיבור ל", "Analytics", "chart-column", ["trending-up", "users", "mouse-pointer-click", "chart-pie"]),
 (21, "חיבור ל", "Cloudflare", "cloud", ["shield-check", "zap", "globe", "lock"]),
 (22, "פתיחת חשבון", "Stripe", "landmark", ["credit-card", "wallet", "badge-check", "receipt"]),
 (23, "עיצוב", "מתקדם", "wand-sparkles", ["palette", "layers", "pen-tool", "sparkles"]),
 (24, "מערכת", "ניהול", "layout-dashboard", ["users", "chart-column", "settings", "database"]),
]
PERSON_ORDER = [3, 1, 4, 2, 5]

TINT = {"p": ("#ffffff", "#f0b8ff", "#c45bff"), "o": ("#ffffff", "#ffd28a", "#ff8a1f")}

def icon(name, c="o"):
    s = (ICONS / f"{name}.svg").read_text()
    body = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    a, b, glow = TINT[c]
    return f"""<svg viewBox="-1 -1 26 26" width="100%" height="100%" fill="none" stroke-linecap="round" stroke-linejoin="round">
<defs><linearGradient id="g{c}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<linearGradient id="f{c}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{b}" stop-opacity=".55"/><stop offset="1" stop-color="{glow}" stop-opacity=".25"/></linearGradient>
<filter id="b{c}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.1"/></filter></defs>
<g stroke="{glow}" stroke-width="4.2" opacity=".9" filter="url(#b{c})">{body}</g>
<g stroke="{glow}" stroke-width="3.4" opacity=".55">{body}</g>
<g fill="url(#f{c})" stroke="none">{body}</g>
<g stroke="url(#g{c})" stroke-width="2.1">{body}</g></svg>"""

def page(num, top, pill, center, sats, person):
    colors = ["p", "o", "o", "p"]
    sat_html = "".join(
        f'<div class="card sat s{k} {colors[k]}"><div class="ic">{icon(n, colors[k])}</div></div>'
        for k, n in enumerate(sats))
    top_html = f'<div class="top fit">{top}</div>' if top else ""
    return f"""<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:K;src:url('file://{FONT}') format('woff2');font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1672px;height:941px;overflow:hidden;background:#07050c;font-family:K,sans-serif}}
.c{{position:absolute;inset:0;overflow:hidden;
 background:
  radial-gradient(520px 420px at 330px 260px,rgba(170,60,220,.55),transparent 70%),
  radial-gradient(380px 520px at 80px 300px,rgba(230,60,120,.40),transparent 70%),
  radial-gradient(700px 500px at 1250px 700px,rgba(255,120,30,.10),transparent 70%),
  linear-gradient(90deg,#140a1e 0%,#0b0712 55%,#08060c 100%)}}
.stripes{{position:absolute;left:0;top:0;width:700px;height:600px;
 background:repeating-linear-gradient(90deg,rgba(255,120,190,.10) 0 10px,rgba(0,0,0,.18) 10px 22px);
 -webkit-mask:radial-gradient(500px 420px at 220px 200px,#000 20%,transparent 75%)}}
.grid{{position:absolute;left:760px;right:0;top:0;bottom:0;
 background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);
 background-size:56px 56px;-webkit-mask:linear-gradient(90deg,transparent,#000 30%)}}
.person{{position:absolute;inset:0;width:1672px;height:941px}}
.frame{{position:absolute;inset:14px;border:3px solid rgba(255,255,255,.88);border-radius:30px;
 box-shadow:0 0 18px rgba(255,255,255,.18)}}
.badge{{position:absolute;left:34px;top:68px;width:168px;height:98px;border-radius:24px;background:#050307;
 border:4px solid #ff8a1f;box-shadow:0 0 18px rgba(255,138,31,.55);color:#fff;font:900 70px/90px Arial Black,Arial,sans-serif;
 text-align:center;letter-spacing:1px;direction:ltr}}
.title{{position:absolute;right:52px;width:790px;top:{105 if top else 190}px;display:flex;flex-direction:column;align-items:center;gap:14px}}
.top{{color:#fff;font-size:150px;line-height:1.02;font-weight:900;white-space:nowrap;text-shadow:0 6px 0 rgba(0,0,0,.5)}}
.pill{{background:linear-gradient(180deg,#ffa23a,#ff7f11);border-radius:34px;padding:6px 60px 22px;
 box-shadow:0 0 34px rgba(255,140,30,.45),0 8px 0 #b54e00;transform:rotate(-1.5deg)}}
.pill span{{display:block;color:#0a0606;font-size:150px;line-height:1.05;font-weight:900;white-space:nowrap}}
.cl{{position:absolute;right:40px;width:820px;top:{475 if top else 440}px;height:{410 if top else 445}px}}
.card{{position:absolute;border-radius:36px;display:flex;align-items:center;justify-content:center;overflow:visible}}
.card::before{{content:"";position:absolute;inset:3px;border-radius:32px;
 background:linear-gradient(180deg,rgba(255,255,255,.16),rgba(255,255,255,0) 45%);pointer-events:none}}
.card .ic{{width:62%;height:62%;position:relative}}
.card.p{{background:radial-gradient(120% 90% at 30% 15%,#4a2470,#1a0b2b 60%,#10071a);border:4px solid #d58bff;
 box-shadow:0 0 0 2px rgba(255,255,255,.12) inset,0 0 30px rgba(196,107,255,.9),0 0 90px rgba(160,60,255,.5),
 0 4px 0 #8a3fc9,0 8px 0 #6c2aa3,0 12px 0 #521d80,0 16px 0 #3b145d,0 30px 40px rgba(0,0,0,.6)}}
.card.o{{background:radial-gradient(120% 90% at 30% 15%,#4d2a10,#1c0e05 60%,#120904);border:4px solid #ffb34d;
 box-shadow:0 0 0 2px rgba(255,255,255,.12) inset,0 0 30px rgba(255,150,40,.9),0 0 90px rgba(255,120,20,.5),
 0 4px 0 #d06a10,0 8px 0 #a5520a,0 12px 0 #7c3d06,0 16px 0 #572a03,0 30px 40px rgba(0,0,0,.6)}}
.main{{left:50%;top:50%;width:330px;height:300px;transform:translate(-50%,-52%) perspective(900px) rotateX(10deg) rotateY(-8deg) rotate(-2deg)}}
.main .ic{{width:64%;height:64%}}
.sat{{width:210px;height:165px}}.sat .ic{{width:60%;height:60%}}
.s0{{left:30px;top:0;transform:perspective(700px) rotateY(10deg) rotate(-5deg)}}.s1{{right:20px;top:-6px;transform:perspective(700px) rotateY(-10deg) rotate(4deg)}}
.s2{{left:0;bottom:6px;transform:perspective(700px) rotateY(10deg) rotate(4deg)}}.s3{{right:30px;bottom:-4px;transform:perspective(700px) rotateY(-10deg) rotate(-4deg)}}
.floor{{position:absolute;left:50%;bottom:-30px;width:620px;height:120px;transform:translateX(-50%);
 background:radial-gradient(closest-side,rgba(255,130,30,.35),transparent);filter:blur(6px)}}
svg.lines{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
svg.lines path{{fill:none;stroke:#ff9a2e;stroke-width:6;opacity:.85;filter:drop-shadow(0 0 8px #ff8a1f)}}
</style></head><body><div class="c">
<div class="stripes"></div><div class="grid"></div>
<img class="person" src="file://{HERE}/persons/person{person}.png">
<div class="title">{top_html}<div class="pill"><span class="fit">{pill}</span></div></div>
<div class="cl">
<svg class="lines" viewBox="0 0 820 {410 if top else 445}" preserveAspectRatio="none">
<path d="M150 90 C 260 90, 260 {205 if top else 222}, 340 {205 if top else 222}"/>
<path d="M680 80 C 560 80, 560 {205 if top else 222}, 480 {205 if top else 222}"/>
<path d="M120 {320 if top else 355} C 250 {320 if top else 355}, 250 {205 if top else 222}, 340 {205 if top else 222}"/>
<path d="M680 {330 if top else 365} C 560 {330 if top else 365}, 560 {205 if top else 222}, 480 {205 if top else 222}"/>
</svg>
<div class="floor"></div>
{sat_html}
<div class="card main o"><div class="ic">{icon(center, "o")}</div></div>
</div>
<div class="frame"></div>
<div class="badge">{num:02d}</div>
</div>
<script>
window.fit=()=>document.querySelectorAll('.fit').forEach(e=>{{let s=150;const max=e.classList.contains('top')?740:660;
 while(e.scrollWidth>max&&s>60){{s-=4;e.style.fontSize=s+'px'}}}});
</script></body></html>"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = HERE / "_html"; tmp.mkdir(exist_ok=True)
    jobs = []
    for k, (num, top, pill, center, sats) in enumerate(L):
        p = tmp / f"{num:02d}.html"
        p.write_text(page(num, top, pill, center, sats, PERSON_ORDER[k % 5]), encoding="utf-8")
        jobs.append([str(p), str(OUT / f"{num:02d}.png")])
    js = HERE / "_render.js"
    js.write_text("""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const pg=await b.newPage({viewport:{width:1672,height:941}});
for(const [h,o] of JSON.parse(process.argv[2])){await pg.goto('file://'+h);await pg.evaluate(()=>document.fonts.ready);
await pg.evaluate(()=>window.fit());await pg.waitForTimeout(150);await pg.screenshot({path:o});}await b.close();})();""")
    subprocess.run(["node", str(js), json.dumps(jobs)], check=True, cwd=HERE)
    from PIL import Image
    for _, o in jobs:
        Image.open(o).convert("RGB").save(o[:-4] + ".jpg", quality=90); os.remove(o)

if __name__ == "__main__":
    main()
