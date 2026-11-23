"""קליפ לפרק 18: "בוחרים את הריפו ומפרסמים". הרצה: python3 fourcode_clips3.py <הקלטה.mp4>
טשטוש עדין (פיקסלים קטנים) על המייל, השם ושמות הריפו."""
import sys
from pathlib import Path
import clips
from clips import make
clips.PIX = 5
B = sys.argv[1]
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
W = (0, 146, 1920, 1020)               # תוכן הדפדפן, בלי לשוניות, כתובת וסימניות
MAIL = (1630, 156, 1895, 208)          # המייל והתמונה למעלה
NAME = (1735, 950, 1895, 1008)         # השם למטה
REPOS = [(880, 790, 1265, 1012, 3.5, 4.8), (880, 430, 1265, 1012, 4.8, 10.6)]  # שמות הריפו ברשימה
OWNER = (395, 416, 520, 454)           # "shaymolina/" ליד הריפו שנבחר
SRC = (1265, 855, 1410, 890)           # המאגר בעמוד הפריסה
MANUAL = (1030, 570, 1340, 695)        # "פריסה ידנית של..."
make(B, [(1, 10.6, 2, W, [MAIL, NAME] + REPOS),
         (10.6, 17, 2.5, W, [MAIL, NAME, OWNER]),
         (17, 26, 8, W, [MAIL, NAME, OWNER]),
         (27, 242.5, 60, W, [MAIL, NAME, SRC]),
         (243, 249, 1.5, W, [MAIL, NAME, MANUAL])], str(OUT / '4code-repo.mp4'), 1280, 608)
