"""YouTube thumbnails for the Lovable course lessons 04-24 (style of lessons 01-07).
Run: python3 tools/thumbnails/lovable_thumbs.py [04 07 ...]  -> site/assets/images/lovable-thumbs/NN.jpg
Needs: persons/person{1..5}.png (cutouts), fonts/, lucide-static (npm i --prefix tools/thumbnails lucide-static)."""
import json, os, subprocess, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
ICONS = pathlib.Path(os.environ.get("LUCIDE", HERE / "node_modules/lucide-static/icons"))
OUT = ROOT / "site/assets/images/lovable-thumbs"
KOBI = ROOT / "site/assets/fonts/files/kobi/Kobi-Black.woff2"
MONT = HERE / "fonts/montserrat-latin-900-italic.woff2"

# ---------- drawing helpers (positions in px inside the 940x500 scene box) ----------
TINT = {"p": ("#ffffff", "#f0b8ff", "#c45bff"), "o": ("#ffffff", "#ffd28a", "#ff8a1f"),
        "w": ("#ffffff", "#efe6ff", "#b57bff"), "d": ("#2a1a05", "#2a1a05", None),
        "g": ("#eaffea", "#7dff8a", "#2fe05a")}
_uid = [0]

def icon(name, c="o", sw=2.1):
    s = (ICONS / f"{name}.svg").read_text()
    body = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
    a, b, glow = TINT[c]
    _uid[0] += 1; u = _uid[0]
    glow_l = "" if not glow else (
        f'<g stroke="{glow}" stroke-width="{sw*2}" opacity=".9" filter="url(#b{u})">{body}</g>'
        f'<g stroke="{glow}" stroke-width="{sw*1.6}" opacity=".5">{body}</g>')
    return f"""<svg viewBox="-1 -1 26 26" width="100%" height="100%" fill="none" stroke-linecap="round" stroke-linejoin="round" style="overflow:visible">
<defs><linearGradient id="g{u}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="24"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<filter id="b{u}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.1"/></filter></defs>
{glow_l}<g stroke="url(#g{u})" stroke-width="{sw}">{body}</g></svg>"""

def pos(x, y, w=None, h=None, rot=0, z=None):
    s = f"left:{x}px;top:{y}px;"
    if w is not None: s += f"width:{w}px;"
    if h is not None: s += f"height:{h}px;"
    if rot: s += f"transform:rotate({rot}deg);"
    if z is not None: s += f"z-index:{z};"
    return s

def W(x, y, w, h, inner="", rot=0, z=2, tone="po", bar=True):
    """browser window with glowing gradient border"""
    b = '<div class="tbar"><i class="r"></i><i class="y"></i><i class="gr"></i></div>' if bar else ""
    return f'<div class="win {tone}" style="{pos(x,y,w,h,rot,z)}">{b}<div class="wb">{inner}</div></div>'

def L(x, y, w, c="", h=18):  # text line
    return f'<div class="ln {c}" style="{pos(x,y,w,h)}"></div>'

def lines(x, y, ws, gap=34, c=""):
    return "".join(L(x, y + i * gap, w, c if i else c + " hi") for i, w in enumerate(ws))

def BTN(x, y, w, h=52, text="", c="o"):
    return f'<div class="btn {c}" style="{pos(x,y,w,h)}">{text}</div>'

def IMG(x, y, w, h):
    return (f'<div class="img" style="{pos(x,y,w,h)}"><svg viewBox="0 0 100 70" preserveAspectRatio="none">'
            '<circle cx="74" cy="22" r="8" fill="#e9c8ff"/><path d="M0 70 L30 30 L52 56 L66 42 L100 70Z" fill="#c78bff" opacity=".9"/>'
            '<path d="M0 70 L30 30 L45 48Z" fill="#fff" opacity=".18"/></svg></div>')

def WF(x, y, w, h):  # wireframe placeholder (box with X)
    return (f'<div class="wf" style="{pos(x,y,w,h)}"><svg viewBox="0 0 100 60" preserveAspectRatio="none">'
            '<path d="M4 4 L96 56 M96 4 L4 56" stroke="#a77cf0" stroke-width="2.5" vector-effect="non-scaling-stroke"/></svg></div>')

def CHK(x, y, on=True, s=50, c="g"):
    inner = f'<div class="ci">{icon("check", c, 3)}</div>' if on else ""
    return f'<div class="chk" style="{pos(x,y,s,s)}">{inner}</div>'

def NOTE(x, y, ic, rot=6, s=170):
    return (f'<div class="note" style="{pos(x,y,s,s,rot,6)}"><div class="pin"></div>'
            f'<div class="ni">{icon(ic, "d", 1.7)}</div></div>')

def TILE(x, y, s, ic, c="p", rot=0, z=6):
    return f'<div class="tile {c}" style="{pos(x,y,s,s*0.86,rot,z)}"><div class="ti">{icon(ic, c)}</div></div>'

def ICON(x, y, s, name, c="p", sw=2.1, z=3):
    return f'<div class="bi" style="{pos(x,y,s,s,0,z)}">{icon(name, c, sw)}</div>'

def T(x, y, text, size=40, c="#fff", cls="lat", extra=""):
    return f'<div class="t {cls}" style="{pos(x,y)}font-size:{size}px;color:{c};{extra}">{text}</div>'

def BOX(x, y, w, h, inner="", c="", rot=0, z=3):
    return f'<div class="box {c}" style="{pos(x,y,w,h,rot,z)}">{inner}</div>'

def DOT(x, y, s, c="p", inner=""):
    return f'<div class="dot {c}" style="{pos(x,y,s,s)}">{inner}</div>'

def ARROW(x1, y1, x2, y2, c="#ffb34d", curve=0):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - curve
    return (f'<svg class="arr" viewBox="0 0 940 500"><defs><marker id="ah{x1}{y1}" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto">'
            f'<path d="M0 0 L6 4 L0 8" fill="none" stroke="{c}" stroke-width="1.6"/></marker></defs>'
            f'<path d="M{x1} {y1} Q {mx} {my} {x2} {y2}" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round" marker-end="url(#ah{x1}{y1})"/></svg>')

def BARS(x, y, w, h, vals, c="#c87bff"):
    n = len(vals); bw = w / (n * 1.6)
    out = "".join(
        f'<rect x="{i*w/n + (w/n-bw)/2:.0f}" y="{h - v*h:.0f}" width="{bw:.0f}" height="{v*h:.0f}" rx="6" fill="{"url(#bo)" if i == n-1 else "url(#bp)"}"/>'
        for i, v in enumerate(vals))
    return (f'<svg class="abs" style="{pos(x,y,w,h)}" viewBox="0 0 {w} {h}"><defs>'
            '<linearGradient id="bp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a6ff"/><stop offset="1" stop-color="#7a3fd0"/></linearGradient>'
            '<linearGradient id="bo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd08a"/><stop offset="1" stop-color="#ff7f11"/></linearGradient></defs>'
            f'{out}</svg>')

def CURVE(x, y, w, h, pts, c="#ffb34d"):
    d = "M" + " L".join(f"{px*w:.0f} {h-py*h:.0f}" for px, py in pts)
    dots = "".join(f'<circle cx="{px*w:.0f}" cy="{h-py*h:.0f}" r="7" fill="#1a1024" stroke="{c}" stroke-width="4"/>' for px, py in pts)
    return (f'<svg class="abs" style="{pos(x,y,w,h)};overflow:visible" viewBox="0 0 {w} {h}">'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="6" stroke-linejoin="round" style="filter:drop-shadow(0 0 8px {c})"/>{dots}</svg>')

def CARD(x, y, w=300, h=190, rot=-6, z=6):  # credit card
    return (f'<div class="ccard" style="{pos(x,y,w,h,rot,z)}"><div class="chip"></div>'
            f'<div class="cnum">•••• •••• •••• 4242</div><div class="cbr"><i></i><i></i></div></div>')

def AV(x, y, s=56, c="p"):
    return f'<div class="av {c}" style="{pos(x,y,s,s)}"><div class="avi">{icon("user-round", "w" if c=="p" else "o", 2)}</div></div>'

def FIELD(x, y, w, h=56, inner=""):
    return f'<div class="field" style="{pos(x,y,w,h)}">{inner}</div>'

# ---------- scenes ----------
def s04():  # Supabase database
    rows = ""
    for r in range(4):
        yy = 92 + r * 62
        rows += L(30, yy, 110, "o" if r == 0 else "") + L(180, yy, 150) + L(370, yy, 120) + f'<div class="hr" style="{pos(20,yy+40,560,3)}"></div>'
    inner = rows + f'<div class="vr" style="{pos(160,70,3,260)}"></div><div class="vr" style="{pos(350,70,3,260)}"></div>' + BOX(20, 20, 560, 50, "", "head")
    return (W(230, 40, 620, 420, inner, rot=-2) + TILE(40, 250, 210, "database", "o", -7) + TILE(770, 10, 150, "key-round", "p", 6))

def s05():  # templates
    cards = ""
    for i in range(4):
        cx, cy = 30 + (i % 2) * 290, 22 + (i // 2) * 175
        sel = " sel" if i == 1 else ""
        cards += BOX(cx, cy, 260, 155, IMG(14, 14, 232, 72) + L(14, 100, 170) + L(14, 128, 110, "s"), "mini" + sel)
    cards += f'<div class="ck" style="{pos(530,6,54,54)}">{icon("check", "w", 3)}</div>'
    return W(210, 30, 630, 450, cards, rot=-2) + TILE(30, 270, 180, "layout-template", "o", -8) + TILE(790, 300, 140, "sparkles", "p", 7)

def s06():  # product blueprint
    br = f'<div class="brk" style="{pos(30,30,190,190)}"></div>'
    cube = ICON(65, 62, 120, "box", "p", 1.7)
    chk = "".join(CHK(250, 40 + i * 70, True, 46) + L(315, 46 + i * 70, 190, "hi") + L(315, 74 + i * 70, 130, "s") for i in range(3))
    back = W(40, 60, 260, 330, IMG(20, 90, 140, 90) + WF(20, 20, 90, 60) + lines(125, 25, [100, 80], 26) + lines(175, 100, [70, 60, 70], 28) + WF(20, 200, 210, 60), rot=-8, z=1, tone="pp")
    return back + W(250, 40, 580, 400, br + cube + chk, rot=-2) + NOTE(760, 210, "lightbulb", 8)

def s07():  # first prompt
    inp = FIELD(30, 30, 640, 90, ICON(24, 22, 46, "sparkles", "w") + T(90, 18, "/ prompt...<span class='cur'>|</span>", 44, "#fff") + BTN(520, 10, 104, 70, f'<div class="bti">{icon("send", "w", 2.4)}</div>'))
    chips = "".join(BOX(30 + i * 218, 160, 196, 64, L(26, 23, 140), "chip") for i in range(3))
    return W(150, 40, 720, 400, inp + chips + lines(30, 260, [380, 260], 40), rot=-2) + TILE(720, 300, 170, "wand-sparkles", "p", 6)

def s08():  # prompt mastery - chat + sliders
    chat = (BOX(260, 26, 330, 70, L(24, 26, 270, "w"), "bub me")
            + BOX(30, 120, 420, 110, lines(24, 24, [360, 290, 200], 28), "bub ai")
            + BOX(300, 254, 290, 64, L(24, 23, 230, "w"), "bub me"))
    sl = "".join(f'<div class="sld" style="{pos(28, 34 + i*62, 200, 8)}"><i style="left:{p}%"></i></div>' for i, p in enumerate([70, 35, 85]))
    return (W(250, 50, 620, 400, chat, rot=-2) + BOX(20, 150, 260, 230, sl, "panel", rot=-6, z=6)
            + TILE(790, 0, 140, "brain", "o", 7))

def s09():  # build the system
    side = f'<div class="side" style="{pos(0,0,130,330)}"></div>' + "".join(L(22, 30 + i * 44, 86, "s" if i else "o") for i in range(6))
    main = (BOX(160, 24, 200, 120, ICON(20, 20, 50, "users", "p") + L(20, 86, 120), "kpi") + BOX(380, 24, 200, 120, ICON(20, 20, 50, "chart-column", "o") + L(20, 86, 120), "kpi")
            + BOX(160, 166, 420, 150, lines(24, 26, [330, 280, 360, 220], 30), "kpi"))
    flow = "".join(DOT(30 + i * 90, 40, 56, "o" if i == 2 else "p") for i in range(3)) + ARROW(0, 0, 0, 0, "#0000")
    flowbox = BOX(690, 330, 250, 140, flow + f'<div class="flowar" style="{pos(88,58,40,6)}"></div><div class="flowar" style="{pos(178,58,40,6)}"></div>' + L(30, 108, 70, "s") + L(120, 108, 70, "s"), "panel", rot=5, z=6)
    return W(170, 30, 640, 400, side + main, rot=-2) + TILE(20, 280, 180, "boxes", "o", -7) + flowbox

def s10():  # design part 1 - palette + type
    sw = "".join(f'<div class="sw" style="{pos(30 + i*92, 30, 74, 74)};background:{c}"></div>' for i, c in enumerate(["#ff8a1f", "#ffb86b", "#c45bff", "#7a3fd0", "#f4ecff"]))
    typ = T(30, 120, "Aa", 150, "#fff", "lat") + lines(250, 160, [260, 200, 230], 36)
    btns = BTN(30, 320, 180, 54) + BTN(230, 320, 180, 54, "", "ghost")
    return W(220, 30, 600, 420, sw + typ + btns, rot=-2) + TILE(30, 250, 180, "palette", "o", -8) + TILE(780, 10, 140, "brush", "p", 7)

def s11():  # design part 2 - selection on canvas
    content = IMG(30, 30, 260, 170) + lines(320, 40, [220, 180, 200], 36) + BTN(320, 160, 170, 50) + "".join(BOX(30 + i * 180, 230, 160, 100, L(18, 60, 110, "s"), "mini") for i in range(3))
    sel = f'<div class="selbox" style="{pos(304,24,248,200)}"><i class="h1"></i><i class="h2"></i><i class="h3"></i><i class="h4"></i></div>'
    cur = ICON(520, 190, 70, "mouse-pointer-2", "o", 2.2, z=8)
    return W(200, 30, 620, 410, content + sel + cur, rot=-2) + TILE(30, 280, 170, "pen-tool", "p", -8) + TILE(790, 280, 140, "layers", "o", 7)

def s12():  # free vs pro
    free = BOX(110, 70, 330, 380, ICON(30, 30, 64, "gift", "p") + T(110, 34, "Free", 54) + lines(30, 140, [240, 200, 220], 42) + BTN(30, 300, 270, 56, "", "ghost"), "plan", rot=-5, z=3)
    pro = BOX(470, 20, 370, 450, ICON(30, 30, 76, "crown", "o") + T(125, 36, "Pro", 66, "#ffd28a") + "".join(CHK(30, 150 + i * 60, True, 40, "o") + L(90, 160 + i * 60, 220, "hi") for i in range(3)) + BTN(30, 360, 310, 62), "plan pro", rot=3, z=4)
    return free + pro

def s13():  # payments checkout
    inner = (FIELD(30, 40, 300, 56, L(20, 19, 180)) + FIELD(30, 116, 300, 56, L(20, 19, 220)) + FIELD(30, 192, 140, 56, L(20, 19, 80)) + FIELD(190, 192, 140, 56, L(20, 19, 70))
             + BTN(30, 280, 300, 66, f'<div class="bti" style="width:34px;height:34px">{icon("lock", "w", 2.6)}</div>'))
    return W(330, 40, 560, 410, inner + lines(370, 60, [130, 100, 120], 40) + T(370, 220, "₪", 90, "#ffd28a", "lat"), rot=-2) + CARD(60, 230, 330, 205, -9) + TILE(800, 0, 130, "receipt", "p", 7)

def s14():  # login with google
    inner = (AV(250, 30, 100) + FIELD(90, 160, 420, 56, ICON(16, 12, 32, "mail", "w", 2) + L(66, 19, 200)) + FIELD(90, 232, 420, 56, ICON(16, 12, 32, "key-round", "w", 2) + L(66, 19, 160))
             + BTN(90, 310, 420, 66, T(0, 0, "Continue with Google", 30, "#1a0d02", "lat", "position:relative;font-style:normal;font-weight:900"), "o"))
    return W(230, 20, 600, 420, inner, rot=-2) + TILE(30, 280, 170, "log-in", "o", -8) + TILE(790, 300, 140, "shield-check", "p", 7)

def s15():  # custom domain
    addr = FIELD(30, 30, 620, 76, ICON(20, 18, 40, "lock", "g", 2.4) + T(80, 14, "www.mybrand.co.il", 40, "#fff"))
    return (W(170, 40, 690, 400, addr + IMG(30, 140, 300, 190) + lines(360, 150, [260, 200, 230, 150], 40) + BTN(360, 300, 180, 50), rot=-2)
            + TILE(20, 280, 180, "globe", "o", -8) + TILE(800, 0, 130, "link", "p", 7))

def s16():  # lead form to mail
    form = (L(30, 30, 260, "hi") + FIELD(30, 80, 420, 56, L(20, 19, 160)) + FIELD(30, 152, 420, 56, L(20, 19, 220)) + FIELD(30, 224, 420, 56, L(20, 19, 130))
            + BTN(30, 300, 420, 62, f'<div class="bti" style="width:36px;height:36px">{icon("send", "w", 2.4)}</div>'))
    env = TILE(690, 150, 230, "mail", "o", 6, z=7) + f'<div class="badge1" style="{pos(880,135,62,62)}">1</div>'
    return W(60, 30, 500, 420, form, rot=-3) + ARROW(560, 300, 690, 260, "#ffb34d", 60) + env

def s17():  # final touches
    site = IMG(30, 30, 330, 190) + lines(390, 40, [180, 150, 170], 36) + BTN(390, 170, 160, 50) + "".join(BOX(30 + i * 180, 250, 160, 90, L(18, 50, 110, "s"), "mini") for i in range(3))
    sp = ICON(-30, -40, 80, "sparkles", "o", 2) + ICON(560, 260, 70, "sparkles", "p", 2)
    chk = "".join(CHK(24, 26 + i * 62, True, 40) + L(80, 36 + i * 62, 120, "hi") for i in range(4))
    return W(270, 30, 600, 410, site + sp, rot=-2) + BOX(20, 120, 260, 280, chk, "panel", rot=-6, z=6) + TILE(800, 330, 130, "rocket", "o", 7)

def s18():  # users management / hand off
    rows = "".join(AV(30, 30 + i * 80, 52, "o" if i == 0 else "p") + L(100, 40 + i * 80, 180, "hi") + L(100, 66 + i * 80, 110, "s")
                   + BOX(380, 40 + i * 80, 120, 40, "", "role o" if i == 0 else "role") for i in range(4))
    return (W(90, 30, 560, 420, rows, rot=-2) + ARROW(650, 240, 740, 200, "#ffb34d", 50)
            + TILE(720, 90, 210, "handshake", "o", 6, z=7) + TILE(760, 330, 140, "key-round", "p", -6))

def s19():  # self hosting - terminal
    code = (T(30, 24, "<span style='color:#7dff8a'>$</span> npm run build", 34, "#fff", "mono")
            + T(30, 80, "<span style='color:#7dff8a'>$</span> deploy --prod", 34, "#fff", "mono")
            + T(30, 136, "<span style='color:#ffb34d'>✓</span> Live", 34, "#ffd28a", "mono")
            + lines(30, 210, [420, 300, 360], 38, "s"))
    return (W(70, 40, 560, 400, code, rot=-3, tone="pp") + ARROW(630, 220, 720, 180, "#ffb34d", 50)
            + TILE(700, 80, 230, "server", "o", 6, z=7) + TILE(760, 330, 140, "upload", "p", -6))

def s20():  # analytics
    kp = "".join(BOX(30 + i * 200, 24, 180, 100, L(18, 22, 90, "s") + L(18, 58, 120, "o" if i == 0 else "hi", 22), "kpi") for i in range(3))
    return (W(170, 30, 660, 420, kp + BARS(40, 150, 360, 180, [.35, .55, .45, .7, .62, .9]) + CURVE(420, 160, 180, 160, [(0, .2), (.35, .45), (.6, .35), (1, .9)]), rot=-2)
            + TILE(20, 280, 180, "chart-column", "o", -8) + TILE(790, 0, 140, "trending-up", "p", 7))

def s21():  # cloudflare
    inner = (ICON(40, 40, 230, "shield-check", "o", 1.6) + T(300, 70, "Protected", 50, "#fff") + lines(300, 150, [240, 180], 38)
             + BOX(300, 250, 260, 60, ICON(14, 12, 36, "zap", "o", 2.2) + L(64, 21, 160), "chip"))
    return W(200, 40, 620, 400, inner, rot=-2) + TILE(20, 260, 190, "cloud", "o", -8) + TILE(780, 300, 150, "globe", "p", 7)

def s22():  # stripe account setup
    steps = "".join(DOT(40 + i * 170, 30, 70, "o" if i < 2 else "p", f'<div class="di">{icon("check" if i < 2 else "landmark", "w", 2.6 if i < 2 else 2)}</div>') for i in range(3))
    bars = f'<div class="flowar" style="{pos(120,62,80,6)}"></div><div class="flowar" style="{pos(290,62,80,6)}"></div>'
    form = FIELD(40, 140, 440, 56, L(20, 19, 220)) + FIELD(40, 212, 440, 56, L(20, 19, 160)) + BTN(40, 296, 440, 60, T(0, 0, "Stripe", 32, "#1a0d02", "lat", "position:relative"))
    return W(300, 30, 540, 410, steps + bars + form, rot=-2) + CARD(30, 250, 320, 200, -10) + TILE(790, 0, 140, "badge-check", "p", 7)

def s23():  # advanced design - layers + bezier
    lay = "".join(BOX(40 + i * 40, 40 + i * 50, 300, 190, IMG(16, 16, 268, 110) + L(16, 144, 160), "mini" + (" sel" if i == 2 else "")) for i in range(3))
    bez = (f'<svg class="abs" style="{pos(400,40,200,300)};overflow:visible" viewBox="0 0 200 300">'
           '<path d="M20 260 C 20 120, 180 180, 180 30" stroke="#ffb34d" stroke-width="6" fill="none" style="filter:drop-shadow(0 0 8px #ff8a1f)"/>'
           '<path d="M20 260 L20 120 M180 30 L180 180" stroke="#d9a6ff" stroke-width="3" stroke-dasharray="6 6"/>'
           '<rect x="8" y="248" width="24" height="24" rx="4" fill="#1a1024" stroke="#ffb34d" stroke-width="4"/><rect x="168" y="18" width="24" height="24" rx="4" fill="#1a1024" stroke="#ffb34d" stroke-width="4"/>'
           '<circle cx="20" cy="120" r="10" fill="#d9a6ff"/><circle cx="180" cy="180" r="10" fill="#d9a6ff"/></svg>')
    return W(210, 30, 640, 420, lay + bez, rot=-2) + TILE(20, 270, 180, "wand-sparkles", "o", -8) + TILE(790, 0, 140, "pen-tool", "p", 7)

def s24():  # admin dashboard
    side = f'<div class="side" style="{pos(0,0,120,330)}"></div>' + "".join(L(22, 30 + i * 44, 76, "s" if i else "o") for i in range(6))
    kp = "".join(BOX(150 + i * 160, 22, 145, 96, L(16, 20, 70, "s") + L(16, 54, 100, "o" if i == 0 else "hi", 22), "kpi") for i in range(3))
    tbl = "".join(AV(166, 150 + i * 56, 40, "p") + L(222, 160 + i * 56, 170) + BOX(420, 156 + i * 56, 90, 30, "", "role o" if i == 1 else "role") for i in range(3))
    return W(190, 30, 640, 400, side + kp + tbl, rot=-2) + TILE(20, 270, 180, "layout-dashboard", "o", -8) + TILE(790, 300, 140, "settings", "p", 7)

# num, Hebrew title (white), English pill, scene
L_ = [
 (4, "דאטה בייס", "Supabase", s04), (5, "תבניות", "Templates", s05), (6, "אפיון מוצר", "Product Blueprint", s06),
 (7, "הפרומפט הראשון", "First Prompt", s07), (8, "שליטה בפרומפטים", "Prompt Mastery", s08), (9, "בניית מערכת", "Build the App", s09),
 (10, "עיצוב - חלק א'", "Design Basics", s10), (11, "עיצוב - חלק ב'", "Design Details", s11), (12, "מסלולים", "Free vs Pro", s12),
 (13, "חיבור לתשלומים", "Payments", s13), (14, "התחברות מהירה", "Google Login", s14), (15, "חיבור דומיין", "Custom Domain", s15),
 (16, "טופס לידים למייל", "Lead Form", s16), (17, "הפינישים האחרונים", "Final Touches", s17), (18, "העברה ללקוח", "Client Handoff", s18),
 (19, "העלאה לשרת חיצוני", "Self Hosting", s19), (20, "מדידת תנועה", "Google Analytics", s20), (21, "אבטחה ומהירות", "Cloudflare", s21),
 (22, "פתיחת חשבון", "Stripe Setup", s22), (23, "עיצוב מתקדם", "Advanced Design", s23), (24, "מערכת ניהול", "Admin Dashboard", s24),
]
PERSON_ORDER = [3, 1, 4, 2, 5]

CSS = """
@font-face{font-family:K;src:url('file://%(kobi)s') format('woff2');font-weight:900}
@font-face{font-family:M;src:url('file://%(mont)s') format('woff2');font-weight:900;font-style:italic}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1672px;height:941px;overflow:hidden;background:#07050c;font-family:K,sans-serif}
.c{position:absolute;inset:0;overflow:hidden;
 background:radial-gradient(520px 420px at 330px 260px,rgba(170,60,220,.55),transparent 70%),
  radial-gradient(380px 520px at 80px 300px,rgba(230,60,120,.40),transparent 70%),
  radial-gradient(700px 420px at 1250px 760px,rgba(255,120,30,.16),transparent 70%),
  radial-gradient(600px 400px at 1000px 600px,rgba(150,60,255,.14),transparent 70%),
  linear-gradient(90deg,#140a1e 0%,#0b0712 55%,#08060c 100%)}
.stripes{position:absolute;left:0;top:0;width:700px;height:600px;
 background:repeating-linear-gradient(90deg,rgba(255,120,190,.10) 0 10px,rgba(0,0,0,.18) 10px 22px);
 -webkit-mask:radial-gradient(500px 420px at 220px 200px,#000 20%,transparent 75%)}
.person{position:absolute;inset:0;width:1672px;height:941px;z-index:1}
.frame{position:absolute;inset:14px;border:3px solid rgba(255,255,255,.88);border-radius:30px;box-shadow:0 0 18px rgba(255,255,255,.18);z-index:20}
.badge{position:absolute;left:34px;top:40px;width:172px;height:104px;border-radius:26px;background:#050307;z-index:21;
 border:5px solid #ff8a1f;box-shadow:0 0 18px rgba(255,138,31,.55);color:#fff;font:900 italic 72px/94px M,sans-serif;text-align:center;direction:ltr}
.title{position:absolute;right:46px;width:940px;top:40px;display:flex;flex-direction:column;align-items:center;gap:6px;z-index:10}
.top{color:#fff;font-size:150px;line-height:1.08;font-weight:900;white-space:nowrap;text-shadow:0 6px 0 rgba(0,0,0,.45),0 0 30px rgba(0,0,0,.4)}
.pill{background:linear-gradient(180deg,#ffa63e,#ff8414);border-radius:34px;padding:8px 54px 16px;
 box-shadow:0 0 40px rgba(255,140,30,.5),0 8px 0 #b54e00;transform:rotate(-1deg)}
.pill span{display:block;color:#0a0606;font:900 italic 108px/1.12 M,sans-serif;white-space:nowrap;letter-spacing:-2px}
.scene{position:absolute;left:690px;top:410px;width:940px;height:500px;z-index:5}
.scene>*,.wb>*,.box>*{position:absolute}
.win{border-radius:34px;border:4px solid transparent;
 background:linear-gradient(170deg,#1d1330,#0f0a19 60%,#0b0812) padding-box,linear-gradient(120deg,#c46bff 0%,#9a5cff 40%,#ff8a1f 100%) border-box;
 box-shadow:-16px -6px 50px rgba(180,90,255,.55),18px 16px 60px rgba(255,140,30,.6),0 14px 0 #2a160c,0 40px 60px rgba(0,0,0,.6)}
.win.pp{background:linear-gradient(170deg,#21143a,#120b20) padding-box,linear-gradient(120deg,#c46bff,#7d4bff) border-box;box-shadow:0 0 50px rgba(180,90,255,.55),0 12px 0 #24113d}
.tbar{position:absolute;left:0;right:0;top:0;height:60px;border-bottom:2px solid rgba(255,255,255,.07);background:rgba(255,255,255,.03);border-radius:30px 30px 0 0;direction:ltr}
.tbar i{position:absolute;top:20px;width:22px;height:22px;border-radius:50%}
.tbar .r{left:26px;background:#ff5f6d;box-shadow:0 0 10px #ff5f6d}.tbar .y{left:60px;background:#ffd23f;box-shadow:0 0 10px #ffd23f}.tbar .gr{left:94px;background:#3ddc5a;box-shadow:0 0 10px #3ddc5a}
.wb{position:absolute;left:0;right:0;top:60px;bottom:0;direction:ltr}
.win:not(:has(.tbar)) .wb{top:0}
.ln{border-radius:10px;background:linear-gradient(90deg,#b99cf0,#8c6ad8);opacity:.75}
.ln.hi{background:linear-gradient(90deg,#efe4ff,#c7b0f5);opacity:.95}
.ln.s{opacity:.45}.ln.o{background:linear-gradient(90deg,#ffd08a,#ff8a1f);opacity:1}.ln.w{background:#fff;opacity:.95}
.btn{border-radius:16px;background:linear-gradient(180deg,#ffae4e,#ff8414);box-shadow:0 0 24px rgba(255,140,30,.7),0 6px 0 #a34800;display:flex;align-items:center;justify-content:center}
.btn.ghost{background:transparent;border:3px solid #a77cf0;box-shadow:0 0 16px rgba(170,110,255,.4)}
.bti{width:44px;height:44px}
.img{border-radius:16px;overflow:hidden;background:linear-gradient(160deg,#7b45d9,#4a2496);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12)}
.img svg,.wf svg{width:100%;height:100%;display:block}
.wf{border:3px solid #a77cf0;border-radius:10px;background:rgba(150,100,255,.12)}
.chk{border:4px solid #ffb34d;border-radius:12px;background:#1a1024;box-shadow:0 0 14px rgba(255,150,40,.6)}
.chk .ci{position:absolute;left:-2px;top:-10px;width:60px;height:60px}
.note{background:linear-gradient(160deg,#ffe36b,#ffc93a);border-radius:6px;box-shadow:0 18px 30px rgba(0,0,0,.5),0 0 30px rgba(255,210,60,.35)}
.note .ni{position:absolute;left:22%;top:22%;width:56%;height:56%}
.note .pin{position:absolute;left:50%;top:-22px;width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#e9a6ff,#9b3ff0);box-shadow:0 0 12px #b65cff}
.tile{border-radius:34px;display:flex;align-items:center;justify-content:center}
.tile::before{content:"";position:absolute;inset:3px;border-radius:30px;background:linear-gradient(180deg,rgba(255,255,255,.16),rgba(255,255,255,0) 45%)}
.tile .ti{width:58%;height:66%;position:relative}
.tile.p{background:radial-gradient(120% 90% at 30% 15%,#5a2a88,#1d0c31 60%,#12081d);border:4px solid #d58bff;
 box-shadow:0 0 30px rgba(196,107,255,.9),0 0 90px rgba(160,60,255,.5),0 4px 0 #8a3fc9,0 8px 0 #6c2aa3,0 12px 0 #521d80,0 16px 0 #3b145d,0 30px 40px rgba(0,0,0,.6)}
.tile.o{background:linear-gradient(180deg,#ffb44f,#ff8414);border:4px solid #ffd08a;
 box-shadow:0 0 30px rgba(255,150,40,.9),0 0 90px rgba(255,120,20,.5),0 4px 0 #d06a10,0 8px 0 #a5520a,0 12px 0 #7c3d06,0 16px 0 #572a03,0 30px 40px rgba(0,0,0,.6)}
.bi{}
.t{white-space:nowrap;line-height:1.2}.t.lat{font-family:M,sans-serif;font-style:italic;font-weight:900}
.t.mono{font-family:"DejaVu Sans Mono",monospace;font-weight:700}
.cur{color:#ffb34d;font-style:normal}
.box{border-radius:20px}
.box.head{background:rgba(255,140,30,.12);border:2px solid rgba(255,160,60,.5);border-radius:12px;z-index:0}
.hr{background:rgba(255,255,255,.08)}.vr{background:rgba(255,255,255,.08)}
.box.mini{background:#1a1129;border:3px solid rgba(190,140,255,.45)}
.box.mini.sel{border-color:#ffb34d;box-shadow:0 0 26px rgba(255,150,40,.7)}
.ck{border-radius:50%;background:linear-gradient(180deg,#ffae4e,#ff8414);box-shadow:0 0 20px #ff8a1f;padding:8px}
.box.chip{background:#231736;border:2px solid rgba(190,140,255,.35);border-radius:22px}
.field{border-radius:22px;background:#140d20;border:3px solid #a46cff;box-shadow:0 0 22px rgba(170,100,255,.55),inset 0 0 16px rgba(170,100,255,.15)}
.field>*{position:absolute}
.box.bub{border-radius:24px}.box.bub.me{background:linear-gradient(180deg,#ffae4e,#ff8414);box-shadow:0 0 22px rgba(255,140,30,.6)}
.box.bub.ai{background:#22163a;border:2px solid rgba(190,140,255,.4)}
.box.panel{background:linear-gradient(170deg,#25163d,#140c22);border:4px solid #c46bff;border-radius:28px;
 box-shadow:0 0 34px rgba(196,107,255,.8),0 12px 0 #3b145d,0 30px 40px rgba(0,0,0,.5)}
.sld{border-radius:6px;background:rgba(200,160,255,.35)}
.sld i{position:absolute;top:-12px;width:32px;height:32px;border-radius:50%;background:linear-gradient(180deg,#ffd08a,#ff8414);box-shadow:0 0 14px #ff8a1f;transform:translateX(-50%)}
.side{background:rgba(255,255,255,.04);border-right:2px solid rgba(255,255,255,.06)}
.box.kpi{background:#1b112b;border:2px solid rgba(190,140,255,.35)}
.dot{border-radius:50%;background:#1a1024;border:5px solid #c46bff;box-shadow:0 0 18px rgba(196,107,255,.8)}
.dot.o{border-color:#ffb34d;background:linear-gradient(180deg,#ffae4e,#ff8414);box-shadow:0 0 22px #ff8a1f}
.dot .di{position:absolute;left:20%;top:20%;width:60%;height:60%}
.flowar{background:#ffb34d;border-radius:4px;box-shadow:0 0 10px #ff8a1f}
.sw{border-radius:50%;box-shadow:0 0 20px rgba(255,255,255,.15),inset 0 -6px 0 rgba(0,0,0,.2)}
.selbox{border:3px dashed #ffb34d;border-radius:8px;box-shadow:0 0 18px rgba(255,150,40,.5)}
.selbox i{position:absolute;width:18px;height:18px;background:#fff;border:3px solid #ff8a1f;border-radius:4px}
.selbox .h1{left:-11px;top:-11px}.selbox .h2{right:-11px;top:-11px}.selbox .h3{left:-11px;bottom:-11px}.selbox .h4{right:-11px;bottom:-11px}
.box.plan{background:linear-gradient(170deg,#21143a,#120b20);border:4px solid #b57bff;border-radius:34px;box-shadow:0 0 40px rgba(180,90,255,.6),0 14px 0 #2a1450,0 40px 50px rgba(0,0,0,.5)}
.box.plan.pro{background:linear-gradient(170deg,#3a2210,#170c05);border-color:#ffb34d;box-shadow:0 0 50px rgba(255,140,30,.75),0 14px 0 #5a2a03,0 40px 50px rgba(0,0,0,.5)}
.box.plan>.t{position:absolute}
.ccard{border-radius:24px;background:linear-gradient(135deg,#ffb44f 0%,#ff7a1a 45%,#b14cff 100%);box-shadow:0 0 40px rgba(255,140,30,.6),0 20px 40px rgba(0,0,0,.5);direction:ltr}
.ccard .chip{position:absolute;left:28px;top:40px;width:56px;height:42px;border-radius:8px;background:linear-gradient(135deg,#fff3c4,#d9b45a)}
.ccard .cnum{position:absolute;left:28px;bottom:34px;color:#fff;font:900 italic 24px M,sans-serif;letter-spacing:2px;text-shadow:0 2px 0 rgba(0,0,0,.2)}
.ccard .cbr{position:absolute;right:24px;top:30px}.ccard .cbr i{display:inline-block;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.7);margin-left:-14px}
.av{border-radius:50%;background:#2a1a44;border:3px solid #c46bff;box-shadow:0 0 16px rgba(196,107,255,.7)}.av .avi{position:absolute;left:20%;top:18%;width:60%;height:60%}
.av.o{border-color:#ffb34d;background:#3a2210;box-shadow:0 0 16px rgba(255,150,40,.7)}
.box.role{background:rgba(190,140,255,.25);border-radius:20px}.box.role.o{background:linear-gradient(180deg,#ffae4e,#ff8414);box-shadow:0 0 14px #ff8a1f}
.brk{border:5px solid #d9b8ff;border-radius:6px;-webkit-mask:linear-gradient(#000,#000) 0 0/34px 34px no-repeat,linear-gradient(#000,#000) 100% 0/34px 34px no-repeat,linear-gradient(#000,#000) 0 100%/34px 34px no-repeat,linear-gradient(#000,#000) 100% 100%/34px 34px no-repeat;box-shadow:0 0 14px #b57bff}
.badge1{border-radius:50%;background:#ff3d5a;color:#fff;font:900 italic 36px/56px M,sans-serif;text-align:center;border:3px solid #fff;box-shadow:0 0 20px #ff3d5a;z-index:9}
svg.arr{position:absolute;left:0;top:0;width:940px;height:500px;overflow:visible;z-index:8;filter:drop-shadow(0 0 8px #ff8a1f)}
svg.abs{position:absolute}
"""

def page(num, top, pill, scene, person):
    css = CSS.replace('%(kobi)s', str(KOBI)).replace('%(mont)s', str(MONT))
    return f"""<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c">
<div class="stripes"></div>
<img class="person" src="file://{HERE}/persons/person{person}.png">
<div class="title"><div class="top fit" data-max="900">{top}</div><div class="pill"><span class="fit" data-max="800">{pill}</span></div></div>
<div class="scene">{scene()}</div>
<div class="frame"></div><div class="badge">{num:02d}</div>
</div><script>
window.fit=()=>document.querySelectorAll('.fit').forEach(e=>{{let s=parseFloat(getComputedStyle(e).fontSize);const m=+e.dataset.max;
 while(e.scrollWidth>m&&s>50){{s-=3;e.style.fontSize=s+'px'}}}});
</script></body></html>"""

def main():
    only = set(int(a) for a in sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = HERE / "_html"; tmp.mkdir(exist_ok=True)
    jobs = []
    for k, (num, top, pill, scene) in enumerate(L_):
        if only and num not in only: continue
        p = tmp / f"{num:02d}.html"
        p.write_text(page(num, top, pill, scene, PERSON_ORDER[k % 5]), encoding="utf-8")
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
