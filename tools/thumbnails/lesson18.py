"""Lesson 18 thumbnail in the style of the owner's own 13-17 covers.
Run: python3 tools/thumbnails/lesson18.py -> site/assets/images/lovable-thumbs/18.jpg"""
import json, subprocess, os, pathlib
import lovable_thumbs as M
from lovable_thumbs import icon, pos

BG = M.HERE / "persons/bg6.jpg"

def row(i, role, hot):
    y = 22 + i * 84
    crown = f'<div class="rc">{icon("crown", "d", 2.4)}</div>' if hot else ""
    return (f'<div class="row{" hot" if hot else ""}" style="{pos(24,y,560,72)}">'
            f'<div class="av{" o" if hot else ""}"><div class="avi">{icon("user-round", "w", 2.2)}</div></div>'
            f'<div class="b1"></div><div class="b2"></div>'
            f'<div class="role{" o" if hot else ""}">{crown}<span>{role}</span></div></div>')

ROWS = "".join(row(i, r, i == 0) for i, r in enumerate(["Admin", "User", "User", "User"]))

SCENE = f"""
<div class="floor"></div>
<div class="win3d"><div class="tbar"><i class="r"></i><i class="y"></i><i class="gr"></i></div><div class="body">{ROWS}
 <div class="cursor">{icon("mouse-pointer-2", "w", 1.4)}</div>
 <svg class="spark" viewBox="0 0 80 80"><path d="M22 30 l-10 -22 M42 22 l4 -22 M58 34 l20 -12" /></svg>
</div></div>
<svg class="wires" viewBox="0 0 980 520">
 <path d="M668 240 C 735 240, 730 130, 790 130"/><path d="M668 240 C 735 240, 730 380, 790 380"/>
 <circle cx="668" cy="240" r="10"/><circle cx="790" cy="130" r="10"/><circle cx="790" cy="380" r="10"/>
</svg>
<div class="card" style="{pos(790,45,170,170)}"><div class="ci">{icon("handshake", "w", 1.9)}</div></div>
<div class="card" style="{pos(790,295,170,170)}"><div class="ci">{icon("key-round", "w", 1.9)}</div></div>
<div class="gchk" style="{pos(912,14,70,70)}">{icon("check", "w", 3.6)}</div>
<svg class="spark s2" style="{pos(905,268,70,70)}" viewBox="0 0 80 80"><path d="M14 40 l-14 6 M24 22 l-10 -14 M44 14 l2 -16" /></svg>
"""

EXTRA = """
.c{background:#06040a}
.photo{position:absolute;inset:0;width:1672px;height:941px;object-fit:cover;
 -webkit-mask:linear-gradient(90deg,#000 0,#000 540px,transparent 650px)}
.shade{position:absolute;inset:0;background:radial-gradient(600px 400px at 1200px 760px,rgba(150,60,255,.18),transparent 70%);z-index:0}
.stripes{display:none}
.top{font-size:178px;line-height:1.02;transform:skewX(-10deg);text-shadow:0 8px 0 rgba(0,0,0,.55),0 0 40px rgba(0,0,0,.6);letter-spacing:-2px}
.title{top:22px;gap:2px;right:40px;width:960px}
.pill{padding:0 66px 14px;border-radius:38px;transform:rotate(-1deg);
 background:linear-gradient(180deg,#ffb04a,#ff8a12 60%,#f07400);box-shadow:0 0 50px rgba(255,140,30,.55),0 10px 0 #a94600}
.pill span{font-family:K,sans-serif;font-style:normal;font-size:168px;line-height:1.04;letter-spacing:-2px;transform:skewX(-10deg)}
.badge{font-size:76px}
.scene{left:650px;top:400px;width:980px;height:520px}
.floor{left:40px;top:400px;width:760px;height:120px;background:radial-gradient(closest-side,rgba(255,120,30,.45),rgba(160,60,255,.25) 55%,transparent);filter:blur(10px)}
.win3d{left:40px;top:14px;width:620px;height:430px;border-radius:38px;border:5px solid transparent;
 transform:perspective(1500px) rotateY(-9deg) rotateX(2deg) rotate(-1deg);transform-origin:center;
 background:linear-gradient(165deg,#1c1230,#0b0714 60%,#090610) padding-box,
  linear-gradient(115deg,#d77dff 0%,#a45cff 35%,#ff7ad0 60%,#ff8a1f 100%) border-box;
 box-shadow:-24px -10px 70px rgba(180,80,255,.75),26px 24px 90px rgba(255,130,20,.8),0 0 0 2px rgba(255,255,255,.08) inset,
  0 18px 0 #2a1208,0 50px 70px rgba(0,0,0,.7)}
.win3d .tbar{height:64px}
.win3d .tbar i{top:20px;width:24px;height:24px}
.win3d .body{position:absolute;left:0;right:0;top:64px;bottom:0;direction:ltr}
.row{position:absolute;border-radius:22px;background:rgba(255,255,255,.045);border:2px solid rgba(200,160,255,.14)}
.row.hot{background:linear-gradient(90deg,rgba(255,140,30,.16),rgba(255,140,30,.04));border-color:rgba(255,170,70,.55);box-shadow:0 0 26px rgba(255,140,30,.35)}
.row .av{position:absolute;left:12px;top:8px;width:52px;height:52px;border-radius:50%;background:#2c1a48;border:3px solid #cf8bff;box-shadow:0 0 16px rgba(196,107,255,.8)}
.row .av.o{background:linear-gradient(180deg,#ffae4e,#ff8414);border-color:#ffe0b0;box-shadow:0 0 20px #ff8a1f}
.row .avi{position:absolute;left:18%;top:16%;width:64%;height:64%}
.row .b1{position:absolute;left:84px;top:16px;width:220px;height:20px;border-radius:10px;background:linear-gradient(90deg,#fff,#d9c6ff)}
.row .b2{position:absolute;left:84px;top:44px;width:150px;height:14px;border-radius:8px;background:#8f72cc;opacity:.7}
.row .role{position:absolute;right:14px;top:12px;height:46px;padding:0 22px;border-radius:23px;display:flex;align-items:center;gap:8px;
 background:#2d1f47;border:2px solid rgba(200,160,255,.35);color:#e9dcff;font:900 italic 28px M,sans-serif}
.row .role.o{background:linear-gradient(180deg,#ffb04a,#ff8414);border-color:#ffe0b0;color:#1a0d02;box-shadow:0 0 22px #ff8a1f}
.row .rc{width:30px;height:30px}
.cursor{position:absolute;left:520px;top:56px;width:80px;height:80px;z-index:5;filter:drop-shadow(0 6px 8px rgba(0,0,0,.6))}
.cursor svg path{fill:#fff}
svg.spark{position:absolute;left:516px;top:-8px;width:80px;height:80px;overflow:visible;z-index:5}
svg.spark path{stroke:#ffd23f;stroke-width:7;stroke-linecap:round;fill:none;filter:drop-shadow(0 0 6px #ffc400)}
.wires{position:absolute;left:0;top:0;width:980px;height:520px;overflow:visible}
.wires path{stroke:#ffb34d;stroke-width:6;fill:none;filter:drop-shadow(0 0 8px #ff8a1f)}
.wires circle{fill:#fff3dc;filter:drop-shadow(0 0 8px #ff8a1f)}
.card{position:absolute;border-radius:34px;border:5px solid #d58bff;
 background:radial-gradient(120% 100% at 30% 10%,#3a1d5e,#160a26 65%);
 box-shadow:0 0 34px rgba(196,107,255,.95),0 0 90px rgba(160,60,255,.45),inset 0 0 24px rgba(196,107,255,.35),0 12px 0 #3b145d}
.card .ci{position:absolute;left:18%;top:18%;width:64%;height:64%}
.gchk{position:absolute;border-radius:50%;background:linear-gradient(180deg,#45e870,#14a83d);border:4px solid #c9ffd6;box-shadow:0 0 26px #2fe05a;padding:11px;z-index:9}
.s2{z-index:9}
"""

def main():
    css = M.CSS.replace('%(kobi)s', str(M.KOBI)).replace('%(mont)s', str(M.MONT)) + EXTRA
    html = f"""<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c">
<img class="photo" src="file://{BG}"><div class="shade"></div>
<img class="person" src="file://{M.HERE}/persons/person6.png">
<div class="title"><div class="top fit" data-max="960">ניהול משתמשים</div><div class="pill"><span class="fit" data-max="800">העברה ללקוח</span></div></div>
<div class="scene">{SCENE}</div>
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
