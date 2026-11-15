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


def mark(x, y, size, uid):
    """Rounded square with a terminal prompt '>_'."""
    k = size / 100
    r = 24 * k
    sw = 11 * k
    chev = f"M{x+27*k:.2f} {y+33*k:.2f} L{x+45*k:.2f} {y+50*k:.2f} L{x+27*k:.2f} {y+67*k:.2f}"
    cur = f"M{x+53*k:.2f} {y+67*k:.2f} H{x+74*k:.2f}"
    return f'''<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_D}"/></linearGradient></defs>
<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r:.2f}" fill="url(#g{uid})"/>
<path d="{chev}" stroke="#fff" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<path d="{cur}" stroke="#fff" stroke-width="{sw:.2f}" stroke-linecap="round" fill="none"/>'''


def lockup(color_word, fname, h=30):
    size = 22
    free, x = text_path("Free", size, h + 8, 22)
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
