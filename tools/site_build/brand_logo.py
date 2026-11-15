"""Free AI brand marks: app-icon tile ("Free / AI") + header lockups + favicon.

Colour: #D97757 tile, cream text. Font: Hanken Grotesk SemiBold (OFL).
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "..", "site", "assets", "images", "logo")
FONT = TTFont(os.path.join(HERE, "fonts", "HankenGrotesk-SemiBold.woff2"))
GS, CMAP, UPM = FONT.getGlyphSet(), FONT.getBestCmap(), FONT["head"].unitsPerEm

BRAND, CREAM, INK = "#D97757", "#FAF3EE", "#1F1F1E"


def text_path(text, size):
    s = size / UPM
    x, parts, bp = 0.0, [], BoundsPen(GS)
    for ch in text:
        g = CMAP[ord(ch)]
        t = (s, 0, 0, -s, x, 0)
        pen = SVGPathPen(GS)
        GS[g].draw(TransformPen(pen, t))
        GS[g].draw(TransformPen(bp, t))
        parts.append(pen.getCommands())
        x += GS[g].width * s
    return " ".join(parts), bp.bounds


def tile(x, y, size):
    """Rounded square with 'Free' over 'AI', centred."""
    k = size / 100
    fs, lead = 34 * k, 1.05
    cap = fs * 0.72
    total = cap * 2 + fs * (lead - 0.72)
    y0 = y + size / 2 - total / 2 + cap
    out = f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{22*k:.2f}" fill="{BRAND}"/>'
    for i, line in enumerate(["Free", "AI"]):
        d, b = text_path(line, fs)
        tx = x + size / 2 - (b[2] - b[0]) / 2 - b[0]
        out += f'<path transform="translate({tx:.2f} {y0 + i*fs*lead:.2f})" d="{d}" fill="{CREAM}"/>'
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
