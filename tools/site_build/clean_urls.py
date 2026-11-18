"""כתובות נקיות: מסיר .html מכל הקישורים הפנימיים (index.html -> /).
הרצה ידנית על כל האתר: cd tools/site_build && python3 clean_urls.py"""
import re
from pathlib import Path

_RE = re.compile(r'href="(?!https?:|//|mailto:|tel:)([^"#?]*?)\.html([#?][^"]*)?"')


def _sub(m):
    name, rest = m.group(1), m.group(2) or ""
    if name in ("index", "/index", "./index"):
        return f'href="/{rest}"'
    return f'href="{name}{rest}"'


def clean(html: str) -> str:
    return _RE.sub(_sub, html)


if __name__ == "__main__":
    site = Path(__file__).resolve().parents[2] / "site"
    for f in site.glob("*.html"):
        old = f.read_text()
        new = clean(old)
        if new != old:
            f.write_text(new)
