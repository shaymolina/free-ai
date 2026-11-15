"""Free AI brand marks: header logo, square mark, favicon, footer wordmark."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "..", "site", "assets", "images", "logo")
FONT = TTFont(os.path.join(HERE, "fonts", "Urbanist-SemiBold.ttf"))
GS, CMAP, UPM = FONT.getGlyphSet(), FONT.getBestCmap(), FONT["head"].unitsPerEm

ORANGE, ORANGE_D, INK = "#FF5A1F", "#E63E0C", "#09090B"


def text_path(text, size, x0, baseline, tracking=0.0):
    s = size / UPM
    x, parts = x0, []
    for ch in text:
        g = CMAP[ord(ch)]
        pen = SVGPathPen(GS)
        GS[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        parts.append(pen.getCommands())
        x += GS[g].width * s + tracking * size
    return " ".join(parts), x


LENS = [1, .78, .93, .7, .98, .8, .9, .72, 1, .76]
WIDTH = [.11, .1, .12, .09, .11, .1, .12, .09, .11, .1]
JITTER = [0, 4, -3, 5, -2, 3, -4, 2, -3, 4]


def mark(x, y, size, uid=None, color=ORANGE):
    """Free AI spark: ten soft rays of uneven length."""
    import math
    cx, cy, R = x + size / 2, y + size / 2, size / 2 * 0.94
    out = []
    for i, (L, w, j) in enumerate(zip(LENS, WIDTH, JITTER)):
        a = math.radians(-90 + 36 * i + j)
        ux, uy = math.cos(a), math.sin(a)
        px, py = -uy, ux
        r1, W = L * R, w * R
        m = r1 / 2
        tx, ty = cx + ux * r1, cy + uy * r1
        mx, my = cx + ux * m, cy + uy * m
        out.append(f"M{cx:.2f} {cy:.2f} Q{mx+px*W:.2f} {my+py*W:.2f} {tx:.2f} {ty:.2f} "
                   f"Q{mx-px*W:.2f} {my-py*W:.2f} {cx:.2f} {cy:.2f}Z")
    return (f'<path d="{" ".join(out)}" fill="{color}" stroke="{color}" '
            f'stroke-width="{R*0.07:.2f}" stroke-linejoin="round"/>')


def lockup(color_word, fname, h=30):
    size = 22
    free, x = text_path("Free", size, h + 6, 22)
    ai, x2 = text_path("AI", size, x + 5, 22)
    w = int(x2 + 2)
    svg = f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
{mark(0, 0, h, fname)}
<path d="{free}" fill="{color_word}"/>
<path d="{ai}" fill="{ORANGE}"/>
</svg>'''
    open(os.path.join(OUT, fname), "w").write(svg)


def square(fname, size):
    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" xmlns="http://www.w3.org/2000/svg">
{mark(0, 0, size, fname)}
</svg>'''
    open(os.path.join(OUT, fname), "w").write(svg)


if __name__ == "__main__":
    lockup(INK, "logo.svg")
    lockup("#FFFFFF", "logo-1.svg")
    square("logo-2.svg", 86)
    square("favicon.svg", 64)
    print("ok")
