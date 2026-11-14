"""אייקונים של Claude לדף הבית (במקום לוגואים של התבנית)."""
from pathlib import Path
D = Path(__file__).resolve().parents[2] / "site/assets/images/item"
C = "#D97757"
G = {
    "spark": "M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6L5.6 18.4",
    "chat": "M4 5h16v11H10l-5 4v-4H4z",
    "doc": "M7 3h7l4 4v14H7zM14 3v4h4M10 12h5M10 16h5",
    "term": "M3 5h18v14H3zM7 10l3 2-3 2M12 15h5",
    "laptop": "M5 5h14v10H5zM2 19h20",
    "phone": "M8 2h8a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zM11 18h2",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7z",
}
def glyph(name, cx, cy, size, rot=0):
    s = size / 24
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s}) translate(-12 -12)">'
            f'<path d="{G[name]}" fill="none" stroke="{C}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')
def hero(file, W, tile, rot, name):
    c = W / 2
    (D / file).write_text(f'''<svg width="{W}" height="{W}" viewBox="0 0 {W} {W}" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs><filter id="s" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity=".14"/></filter></defs>
<g filter="url(#s)"><rect x="{c-tile/2}" y="{c-tile/2}" width="{tile}" height="{tile}" rx="8" transform="rotate({rot} {c} {c})" fill="white"/></g>
{glyph(name, c, c, tile*0.55, rot)}
</svg>''')
hero("hero-1.svg", 110, 72, 30, "spark")
hero("hero-2.svg", 115, 64, -15, "chat")
hero("hero-3.svg", 105, 56, 15, "doc")
for f, name in [("item-4.svg", "chat"), ("item-5.svg", "laptop"), ("item-6.svg", "phone"), ("item-7.svg", "term"), ("item-8.svg", "doc"), ("item-9.svg", "bolt")]:
    W = float(open(D / f).read().split('width="')[1].split('"')[0])
    (D / f).write_text(f'''<svg width="{W:g}" height="{W:g}" viewBox="0 0 {W:g} {W:g}" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="{W:g}" height="{W:g}" fill="white"/>{glyph(name, W/2, W/2, W*0.5)}
</svg>''')
print("icons done")
