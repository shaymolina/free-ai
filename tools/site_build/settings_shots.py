"""צילומי מסך ההגדרות (Connectors / Skills / Plugins): טשטוש, מספרים, חצים ומסגרות.
הרצה: python3 tools/site_build/settings_shots.py <תיקייה עם 15.png 16.png 17.png>"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
BR = (217, 119, 87)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
PRIVATE = [(0, 380, 258, 900), (0, 960, 205, 1012), (370, 0, 720, 42), (1660, 95, 1910, 1016)]


def pix(im, box):
    reg = im.crop(box); w, h = reg.size
    reg = reg.resize((max(1, w // 14), max(1, h // 14)), Image.BILINEAR).resize((w, h), Image.NEAREST)
    im.paste(reg, box[:2])


def ring(d, box):
    d.rounded_rectangle(box, radius=12, outline=BR, width=5)


def arrow(d, a, b):
    d.line((a, b), fill=BR, width=6)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p = [b, (b[0] - 26 * math.cos(ang - .45), b[1] - 26 * math.sin(ang - .45)),
         (b[0] - 26 * math.cos(ang + .45), b[1] - 26 * math.sin(ang + .45))]
    d.polygon(p, fill=BR)


def dot(d, x, y, n, r=22):
    d.ellipse((x - r, y - r, x + r, y + r), fill=BR, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), font=F, fill=(255, 255, 255), anchor='mm')


def load(k):
    im = Image.open(SRC / f'{k}.png').convert('RGB')
    for b in PRIVATE:
        pix(im, b)
    return im


# מפה: איך מגיעים
im = load('17'); d = ImageDraw.Draw(im)
ring(d, (228, 962, 274, 1008)); arrow(d, (150, 935), (222, 975)); dot(d, 130, 922, 1)
ring(d, (280, 655, 524, 698)); arrow(d, (150, 650), (272, 674)); dot(d, 125, 645, 2)
ring(d, (573, 126, 900, 167)); arrow(d, (712, 84), (735, 122)); dot(d, 690, 70, 3)
ring(d, (936, 126, 1136, 167)); arrow(d, (1012, 84), (1035, 122)); dot(d, 990, 70, 4)
im.save(OUT / 'settings-map.png', optimize=True)

# פרק לכל סוג: מסגרת על הלשונית
for k, name, tab in [('17', 'settings-connectors', (573, 126, 715, 167)),
                     ('16', 'settings-skills', (715, 128, 795, 168)),
                     ('15', 'settings-plugins', (795, 131, 895, 171))]:
    im = load(k); d = ImageDraw.Draw(im)
    ring(d, tab)
    if k in ('17', '16'):
        ring(d, (1484, 124, 1604, 170))
    ring(d, (1020, 128, 1140, 172) if k != '17' else (936, 126, 1024, 167))
    im.crop((256, 44, 1660, 972)).save(OUT / f'{name}.png', optimize=True)
# הפעלת מיומנות עם /
im = load('18'); pix(im, (880, 340, 1320, 662)); d = ImageDraw.Draw(im)
ring(d, (612, 852, 1132, 906)); ring(d, (620, 913, 745, 956))
im.crop((560, 641, 1640, 1016)).save(OUT / 'skill-slash.png', optimize=True)
print('done')
