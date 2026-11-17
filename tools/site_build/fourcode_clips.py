"""קליפים לפרק "פותחים 4CODE". הרצה: python3 fourcode_clips.py <B.mp4>"""
import sys
from pathlib import Path
from clips import make
B = sys.argv[1]
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
W = (0, 110, 1920, 1020)            # תוכן הדפדפן, בלי לשוניות וכתובת
NAME = (1700, 945, 1915, 1008)      # השם למטה בפלטפורמה
AUTH_NAME = (740, 735, 1160, 780)   # "אתם מחוברים בתור..."
make(B, [(103.5, 113, 1.3, W, [])], str(OUT / '4code-1.mp4'), 1280, 608)
make(B, [(171, 182, 1.2, W, [AUTH_NAME, NAME])], str(OUT / '4code-2.mp4'), 1280, 608)
make(B, [(182, 197.5, 1.3, W, [NAME])], str(OUT / '4code-3.mp4'), 1280, 608)
