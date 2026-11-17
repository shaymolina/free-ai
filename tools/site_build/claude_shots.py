"""צילומי המסך של אפליקציית Claude (פרקים 7-11): טשטוש מידע פרטי, מספרים ומסגרות.
הרצה: python3 tools/site_build/claude_shots.py <תיקיית המקור עם 8.png..12.png>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
BR = (217, 119, 87)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
ENV_MENU = (880, 335, 1322, 542)  # התפריט במרכז: Auto / 4CODE / free ai


def pix(im, box):
    reg = im.crop(box); w, h = reg.size
    reg = reg.resize((max(1, w // 12), max(1, h // 12)), Image.BILINEAR).resize((w, h), Image.NEAREST)
    im.paste(reg, box[:2])


def dot(d, x, y, n, r=19):
    d.ellipse((x - r, y - r, x + r, y + r), fill=BR, outline=(255, 255, 255), width=3)
    d.text((x, y), str(n), font=F, fill=(255, 255, 255), anchor='mm')


def ring(d, box):
    d.rounded_rectangle(box, radius=12, outline=BR, width=5)


# מפת המסך (פרק 7)
im = Image.open(SRC / '8.png').convert('RGB')
for b in [(0, 375, 284, 735), (0, 955, 284, 1010), (883, 558, 1320, 610), ENV_MENU]:
    pix(im, b)
W, H = im.size
c = Image.new('RGB', (W, H + 60), (31, 31, 31)); c.paste(im, (0, 0)); im = c
d = ImageDraw.Draw(im)
dot(d, 300, 80, 1); dot(d, 300, 138, 2); dot(d, 555, 930, 3)
for n, x in [(4, 645), (5, 762), (6, 1425), (7, 1545), (8, 1597)]:
    d.line((x, 1000, x, 1022), fill=BR, width=3); dot(d, x, 1040, n)
im.save(OUT / 'claude-map.png', optimize=True)

# צילום לכל כפתור, עם מסגרת על מה שלוחצים
jobs = {'8': ('claude-code-cloud', [(883, 558, 1320, 610)], (588, 968, 700, 1008)),
        '9': ('claude-code-local', [(883, 558, 1320, 610)], (585, 968, 780, 1008)),
        '12': ('claude-models', [(885, 560, 1112, 610)], (1340, 970, 1512, 1012)),
        '11': ('claude-permissions', [(883, 558, 1320, 610)], (1512, 968, 1576, 1010)),
        '10': ('claude-usage', [(883, 558, 1320, 610)], (1578, 968, 1616, 1010))}
for k, (name, blurs, rg) in jobs.items():
    im = Image.open(SRC / f'{k}.png').convert('RGB')
    for b in blurs + [ENV_MENU]:
        pix(im, b)
    ring(ImageDraw.Draw(im), rg)
    im.crop((290, 285, 1660, im.size[1])).save(OUT / f'{name}.png', optimize=True)
print('done')
