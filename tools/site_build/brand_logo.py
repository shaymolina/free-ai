"""Free AI brand marks: app-icon tile with the word "חינם".

Colour: #D97757 tile, cream text. Font: 4Kobi Black (Fontly).
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "..", "site", "assets", "images", "logo")
FONT = TTFont(os.path.join(HERE, "fonts", "4Kobi-Black.ttf"))
GS, CMAP = FONT.getGlyphSet(), FONT.getBestCmap()

BRAND, CREAM = "#D97757", "#FAF3EE"
WORD = "חינם"


def word_path():
    """Hebrew is drawn right-to-left: lay glyphs out in reverse order."""
    x, parts, bp = 0.0, [], BoundsPen(GS)
    for ch in reversed(WORD):
        g = CMAP[ord(ch)]
        t = (1, 0, 0, -1, x, 0)
        pen = SVGPathPen(GS)
        GS[g].draw(TransformPen(pen, t))
        GS[g].draw(TransformPen(bp, t))
        parts.append(pen.getCommands())
        x += GS[g].width
    return " ".join(parts), bp.bounds


def tile(size):
    k = size / 100
    d, b = word_path()
    s = 64 * k / (b[2] - b[0])
    tx = size / 2 - (b[2] - b[0]) * s / 2 - b[0] * s
    ty = size / 2 - (b[1] + b[3]) * s / 2
    return (f'<rect width="{size}" height="{size}" rx="{22*k:.2f}" fill="{BRAND}"/>'
            f'<path transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})" d="{d}" fill="{CREAM}"/>')


def square(name, size):
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" '
           f'xmlns="http://www.w3.org/2000/svg">{tile(size)}</svg>')
    open(os.path.join(OUT, name), "w").write(svg)


if __name__ == "__main__":
    square("logo.svg", 44)
    square("logo-1.svg", 44)
    square("logo-2.svg", 86)
    square("favicon.svg", 64)
    print("ok")
