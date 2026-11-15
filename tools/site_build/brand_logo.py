"""Free AI brand mark: orange circle with "AI" and "חינם" under it.

Colour: #D97757 circle, cream text. Font: Kobi Black (Fontly).
Both lines are centred; "חינם" gets a small optical nudge to the right
(its weight sits on the left), "AI" a smaller nudge to the left.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "..", "site", "assets", "images", "logo")
FONT = TTFont(os.path.join(HERE, "fonts", "Kobi-Black.ttf"))
GS, CMAP = FONT.getGlyphSet(), FONT.getBestCmap()

BRAND, CREAM = "#D97757", "#FAF3EE"


def text_path(text, rtl=False):
    x, parts, bp = 0.0, [], BoundsPen(GS)
    for ch in (reversed(text) if rtl else text):
        g = CMAP[ord(ch)]
        t = (1, 0, 0, -1, x, 0)
        pen = SVGPathPen(GS)
        GS[g].draw(TransformPen(pen, t))
        GS[g].draw(TransformPen(bp, t))
        parts.append(pen.getCommands())
        x += GS[g].width
    return " ".join(parts), bp.bounds


def place(d, b, cx, cy, h, fill):
    s = h / (b[3] - b[1])
    tx = cx - (b[0] + b[2]) * s / 2
    ty = cy - (b[1] + b[3]) * s / 2
    return f'<path transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})" d="{d}" fill="{fill}"/>'


def mark(name, D):
    r = D / 2
    a, ab = text_path("AI")
    w, wb = text_path("חינם", rtl=True)
    ah = D * 0.34
    wh = D * 0.5 * (wb[3] - wb[1]) / (wb[2] - wb[0])
    gap = D * 0.06
    top = r - (ah + gap + wh) / 2
    svg = (f'<svg width="{D}" height="{D}" viewBox="0 0 {D} {D}" fill="none" xmlns="http://www.w3.org/2000/svg">'
           f'<circle cx="{r}" cy="{r}" r="{r}" fill="{BRAND}"/>'
           + place(a, ab, r - D * 0.004, top + ah / 2, ah, CREAM)
           + place(w, wb, r + D * 0.009, top + ah + gap + wh / 2, wh, CREAM)
           + '</svg>')
    open(os.path.join(OUT, name), "w").write(svg)


if __name__ == "__main__":
    mark("logo.svg", 56)
    mark("logo-1.svg", 86)
    mark("logo-2.svg", 96)
    mark("favicon.svg", 64)
    print("ok")
