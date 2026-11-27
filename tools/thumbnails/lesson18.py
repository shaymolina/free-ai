"""Lesson 18 thumbnail in the style of the owner's own 13-17 covers.
Run: python3 tools/thumbnails/lesson18.py -> site/assets/images/lovable-thumbs/18.jpg"""
import json, subprocess, os
import lovable_thumbs as M
from lovable_thumbs import icon, pos, W, L, AV, BOX, T

def rows():
    out = ""
    roles = [("Admin", "o"), ("User", ""), ("User", ""), ("User", "")]
    for i, (r, c) in enumerate(roles):
        y = 26 + i * 82
        out += (AV(34, y, 64, "o" if i == 0 else "p") + L(120, y + 10, 210, "hi") + L(120, y + 40, 130, "s")
                + BOX(380, y + 10, 150, 46, T(0, 0, r, 26, "#1a0d02" if c else "#efe4ff", "lat", "position:relative;width:100%;text-align:center;line-height:46px"), "role " + c))
    return out

scene = (
    W(40, 20, 600, 420, rows(), rot=-2)
    + '<svg class="arr" viewBox="0 0 940 500" style="filter:drop-shadow(0 0 10px #ff8a1f)">'
      '<path d="M640 230 C 700 230, 690 120, 760 120" stroke="#ffb34d" stroke-width="6" fill="none"/>'
      '<path d="M640 230 C 700 230, 690 360, 760 360" stroke="#ffb34d" stroke-width="6" fill="none"/>'
      '<circle cx="760" cy="120" r="11" fill="#fff4e0"/><circle cx="760" cy="360" r="11" fill="#fff4e0"/></svg>'
    + f'<div class="side" style="{pos(745,30,190,170,0,7)}"><div class="si">{icon("handshake", "p", 1.8)}</div></div>'
    + f'<div class="side" style="{pos(745,280,190,170,0,7)}"><div class="si">{icon("key-round", "p", 1.8)}</div></div>'
    + f'<div class="gchk" style="{pos(880,0,76,76,0,9)}">{icon("check", "w", 3.4)}</div>'
    + f'<div class="cursor" style="{pos(470,62,90,90,0,9)}">{icon("mouse-pointer-2", "w", 1.6)}</div>'
    + '<svg class="arr" viewBox="0 0 940 500" style="filter:drop-shadow(0 0 6px #ffcf3a);z-index:9">'
      '<path d="M498 50 l-8 -26 M524 44 l10 -24 M546 62 l24 -10" stroke="#ffd23f" stroke-width="7" stroke-linecap="round"/></svg>'
)

EXTRA = """
.top{font-size:160px;transform:skewX(-9deg)}
.pill span{font-family:K,sans-serif;font-style:normal;font-size:150px;line-height:1.02;letter-spacing:0;transform:skewX(-9deg)}
.pill{padding:4px 60px 18px}
.box.role{border-radius:24px}
.scene{top:385px;transform:scale(1.1);transform-origin:right top}
.side{border-radius:30px;background:linear-gradient(170deg,#25163d,#140c22);border:4px solid #c46bff;
 box-shadow:0 0 34px rgba(196,107,255,.9),0 0 80px rgba(160,60,255,.4),0 12px 0 #3b145d;position:absolute}
.side .si{position:absolute;left:22%;top:16%;width:56%;height:68%}
.gchk{border-radius:50%;background:linear-gradient(180deg,#3ee06a,#12a43a);border:4px solid #b9ffc9;box-shadow:0 0 24px #2fe05a;padding:12px}
.cursor{filter:drop-shadow(0 4px 6px rgba(0,0,0,.5))}
.cursor svg path{fill:#fff}
"""

def main():
    css = M.CSS.replace('%(kobi)s', str(M.KOBI)).replace('%(mont)s', str(M.MONT)) + EXTRA
    html = f"""<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c">
<div class="stripes"></div>
<img class="person" src="file://{M.HERE}/persons/person6.png">
<div class="title"><div class="top fit" data-max="900">ניהול משתמשים</div><div class="pill"><span class="fit" data-max="780">העברה ללקוח</span></div></div>
<div class="scene">{scene}</div>
<div class="frame"></div><div class="badge">18</div>
</div><script>
window.fit=()=>document.querySelectorAll('.fit').forEach(e=>{{let s=parseFloat(getComputedStyle(e).fontSize);const m=+e.dataset.max;
 while(e.scrollWidth>m&&s>50){{s-=3;e.style.fontSize=s+'px'}}}});
</script></body></html>"""
    tmp = M.HERE / "_html"; tmp.mkdir(exist_ok=True)
    h = tmp / "18.html"; h.write_text(html, encoding="utf-8")
    o = M.OUT / "18.png"
    js = M.HERE / "_render.js"
    js.write_text("""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const pg=await b.newPage({viewport:{width:1672,height:941}});
for(const [h,o] of JSON.parse(process.argv[2])){await pg.goto('file://'+h);await pg.evaluate(()=>document.fonts.ready);
await pg.evaluate(()=>window.fit());await pg.waitForTimeout(150);await pg.screenshot({path:o});}await b.close();})();""")
    subprocess.run(["node", str(js), json.dumps([[str(h), str(o)]])], check=True, cwd=M.HERE)
    from PIL import Image
    Image.open(o).convert("RGB").save(str(o)[:-4] + ".jpg", quality=92); os.remove(o)

if __name__ == "__main__":
    main()
