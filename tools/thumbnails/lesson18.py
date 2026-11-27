"""Lesson 18 thumbnail in the style of the owner's own 13-17 covers.
Run: python3 tools/thumbnails/lesson18.py -> site/assets/images/lovable-thumbs/18.jpg"""
import json, subprocess, os, pathlib
import lovable_thumbs as M
from lovable_thumbs import icon, pos

BG = M.HERE / "persons/bg6.jpg"

SCENE = f"""
<div class="floor"></div>
<div class="win3d"><div class="tbar"><i class="r"></i><i class="y"></i><i class="gr"></i></div><div class="body">
 <div class="fld"><div class="fi">{icon("user-round", "w", 3)}</div><div class="b1"></div><div class="b2"></div>
  <div class="crown">{icon("crown", "o", 2.8)}</div></div>
 <div class="go"><div class="gi">{icon("handshake", "w", 3)}</div></div>
 <div class="cursor">{icon("mouse-pointer-2", "w", 1.4)}</div>
 <svg class="spark" viewBox="0 0 80 80"><path d="M10 26 l-6 -22 M34 20 l10 -20 M50 40 l24 -8" /></svg>
</div></div>
<div class="card" style="{pos(740,110,200,200)}"><div class="ci">{icon("users", "w", 2.8)}</div></div>
"""

EXTRA = """
.c{background:#06040a}
.photo{position:absolute;inset:0;width:1672px;height:941px;object-fit:cover;
 -webkit-mask:linear-gradient(90deg,#000 0,#000 540px,transparent 650px)}
.shade{position:absolute;inset:0;background:radial-gradient(600px 400px at 1200px 760px,rgba(150,60,255,.18),transparent 70%);z-index:0}
.stripes{display:none}
.top{font-size:190px;line-height:1.0;text-shadow:0 8px 0 rgba(0,0,0,.55),0 0 40px rgba(0,0,0,.6);letter-spacing:-2px}
.title{top:22px;gap:2px;right:40px;width:960px}
.pill{padding:0 66px 14px;border-radius:38px;transform:rotate(-1deg);
 background:linear-gradient(180deg,#ffb04a,#ff8a12 60%,#f07400);box-shadow:0 0 50px rgba(255,140,30,.55),0 10px 0 #a94600}
.pill span{font-family:K,sans-serif;font-style:normal;font-size:176px;line-height:1.0;letter-spacing:-2px}
.badge{font-size:76px}
.scene{left:690px;top:350px;width:940px;height:520px;transform:scale(1.08);transform-origin:right top}
.floor{left:40px;top:400px;width:760px;height:120px;background:radial-gradient(closest-side,rgba(255,120,30,.45),rgba(160,60,255,.25) 55%,transparent);filter:blur(10px)}
.win3d{left:40px;top:20px;width:640px;height:440px;border-radius:38px;border:7px solid transparent;
 transform:perspective(1500px) rotateY(-9deg) rotateX(2deg) rotate(-1deg);transform-origin:center;
 background:linear-gradient(165deg,#24143e,#140a26 60%,#100820) padding-box,
  linear-gradient(115deg,#e08bff 0%,#b866ff 30%,#ff6fd0 62%,#ffa030 100%) border-box;
 box-shadow:-20px -14px 60px rgba(190,90,255,.95),-6px 0 24px rgba(220,140,255,.8),24px 26px 80px rgba(255,130,20,.95),8px 10px 26px rgba(255,170,60,.9),0 0 0 2px rgba(255,255,255,.08) inset,
  0 18px 0 #2a1208,0 50px 70px rgba(0,0,0,.7)}
.win3d .tbar{height:66px}
.win3d .tbar i{top:21px;width:26px;height:26px}
.win3d .body{position:absolute;left:0;right:0;top:66px;bottom:0;direction:ltr}
.fld{position:absolute;left:40px;top:44px;width:540px;height:130px;border-radius:34px;border:5px solid #c47bff;
 background:linear-gradient(180deg,rgba(150,80,255,.35),rgba(90,40,180,.25));box-shadow:0 0 34px rgba(190,100,255,.9),inset 0 0 30px rgba(190,120,255,.35)}
.fld .fi{position:absolute;left:30px;top:28px;width:66px;height:66px}
.fld .b1{position:absolute;left:124px;top:36px;width:270px;height:24px;border-radius:12px;background:linear-gradient(90deg,#fff,#e2d2ff)}
.fld .b2{position:absolute;left:124px;top:76px;width:190px;height:20px;border-radius:10px;background:#c9b2ff;opacity:.8}
.fld .crown{position:absolute;right:30px;top:30px;width:64px;height:64px}
.go{position:absolute;left:150px;top:220px;width:340px;height:104px;border-radius:52px;
 background:linear-gradient(180deg,#ffc04f,#ff8a12 60%,#f27300);box-shadow:0 0 40px rgba(255,140,30,.85),0 10px 0 #a34800,inset 0 3px 0 rgba(255,255,255,.35)}
.go .gi{position:absolute;left:50%;top:50%;width:70px;height:70px;transform:translate(-50%,-50%)}
.cursor{position:absolute;left:446px;top:262px;width:110px;height:110px;z-index:5;filter:drop-shadow(0 8px 10px rgba(0,0,0,.6))}
.cursor svg path{fill:#fff}
svg.spark{position:absolute;left:470px;top:196px;width:80px;height:80px;overflow:visible;z-index:5}
svg.spark path{stroke:#ffd23f;stroke-width:8;stroke-linecap:round;fill:none;filter:drop-shadow(0 0 6px #ffc400)}
.wires{position:absolute;left:0;top:0;width:980px;height:520px;overflow:visible}
.wires path{stroke:#ffb34d;stroke-width:6;fill:none;filter:drop-shadow(0 0 8px #ff8a1f)}
.wires circle{fill:#fff3dc;filter:drop-shadow(0 0 8px #ff8a1f)}
.card{position:absolute;border-radius:38px;border:6px solid #e09cff;transform:perspective(800px) rotateY(-14deg) rotate(5deg);
 background:radial-gradient(120% 100% at 30% 10%,#3a1d5e,#160a26 65%);
 box-shadow:0 0 40px rgba(210,120,255,1),0 0 110px rgba(170,70,255,.6),inset 0 0 24px rgba(196,107,255,.35),0 12px 0 #3b145d}
.card .ci{position:absolute;left:19%;top:19%;width:62%;height:62%}
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
