"""רץ אחרון, אחרי shorten.py: תיאורי טקסט לתמונות התוכן (לקוראי מסך ולגוגל).
תמונות קישוטיות נשארות עם alt ריק בכוונה."""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"
ALT = {
    "claude/claude-start.jpg": "מסך הפתיחה של Claude עם שדה לשאלה הראשונה",
    "claude/claude-prompt.jpg": "דוגמה לבקשה טובה ל-Claude",
    "claude/claude-projects.jpg": "פרויקט ב-Claude עם קבצים של העסק",
    "claude/claude-artifacts.jpg": "Artifact שנבנה בתוך השיחה עם Claude",
    "claude/claude-code.jpg": "בניית אתר עם Claude Code",
}
for f in sorted(SITE.glob("*.html")):
    html = f.read_text()
    new = html
    for img, alt in ALT.items():
        new = new.replace(f'src="assets/images/{img}" alt=""', f'src="assets/images/{img}" alt="{alt}"')
    if new != html:
        f.write_text(new)
print("alt texts done")
