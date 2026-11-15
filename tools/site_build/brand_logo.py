"""Free AI brand marks: app-icon tile (big "AI", "free" running up the left side) + header lockups + favicon.

Colour: #D97757 tile, cream text. Font: Hanken Grotesk Bold (OFL).
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "..", "site", "assets", "images", "logo")
FONT = TTFont(os.path.join(HERE, "fonts", "HankenGrotesk-Bold.woff2"))
GS, CMAP, UPM = FONT.getGlyphSet(), FONT.getBestCmap(), FONT["head"].unitsPerEm

BRAND, CREAM, INK = "#D97757", "#FAF3EE", "#1F1F1E"


def text_path(text, size, track=0.0):
    s = size / UPM
    x, parts, bp = 0.0, [], BoundsPen(GS)
    for ch in text:
        g = CMAP[ord(ch)]
        t = (s, 0, 0, -s, x, 0)
        pen = SVGPathPen(GS)
        GS[g].draw(TransformPen(pen, t))
        GS[g].draw(TransformPen(bp, t))
        parts.append(pen.getCommands())
        x += GS[g].width * s + track * size
    return " ".join(parts), bp.bounds


def tile(x, y, size):
    """Rounded square, 'AI' centred, 'free' rotated up the left edge."""
    k = size / 100
    out = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{22*k:.2f}" fill="{BRAND}"/>'
    d, b = text_path("AI", 54 * k, -0.04)
    ax = x + size / 2 - (b[2] - b[0]) / 2 - b[0]
    ay = y + size / 2 - (b[1] + b[3]) / 2
    out += f'<path transform="translate({ax:.2f} {ay:.2f})" d="{d}" fill="{CREAM}"/>'
    d, b = text_path("free", 13 * k, 0.04)
    fx = x + 20 * k
    fy = y + size / 2 + (b[2] - b[0]) / 2 + b[0]
    out += f'<path transform="translate({fx:.2f} {fy:.2f}) rotate(-90)" d="{d}" fill="{CREAM}"/>'
    return out


def save(name, svg):
    open(os.path.join(OUT, name), "w").write(svg)


def lockup(name, word_color, h=32):
    d, b = text_path("Free AI", 22)
    x = h + 9
    w = int(x + (b[2] - b[0]) + 2)
    save(name, f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">'
               f'{tile(0, 0, h)}<path transform="translate({x - b[0]:.2f} {h/2 + 8:.2f})" d="{d}" fill="{word_color}"/></svg>')


def square(name, size):
    save(name, f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" '
               f'xmlns="http://www.w3.org/2000/svg">{tile(0, 0, size)}</svg>')


if __name__ == "__main__":
    square("logo.svg", 44)
    square("logo-1.svg", 44)
    square("logo-2.svg", 86)
    square("favicon.svg", 64)
    print("ok")
