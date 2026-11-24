"""קליפים לפרק "מחברים קונקטור ומשתמשים בו". הרצה: python3 connector_clips.py <video.mp4>"""
import sys
from pathlib import Path
from clips import make
V = sys.argv[1]
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
APP = (0, 0, 1920, 1020)          # אפליקציית קלוד, בלי שורת המשימות
BR = (0, 145, 1920, 1020)         # הדפדפן, בלי שורת הכתובת והסימניות
CHAT = (330, 0, 1480, 1020)       # חלון השיחה
FONTLY = (10, 392, 310, 430)      # שם פרויקט אחר בתפריט הצד
EMAIL = (10, 502, 392, 552, 0, 3.2)          # המייל בתפריט החשבון
ACCOUNTS = (280, 340, 930, 925, 27.4, 33.2)  # רשימת חשבונות הגוגל
GMAIL = (1290, 595, 1650, 680, 32.5, 38.5)   # המייל במסך האישור של גוגל
make(V, [(0, 21.5, 1.3, APP, [FONTLY, EMAIL])], str(OUT / "connect-1.mp4"), 1280, 680)
make(V, [(21.5, 24.4, 1, APP, [FONTLY]), (24.4, 38, 1, BR, [ACCOUNTS, GMAIL]), (38, 41, 1, APP, [FONTLY])], str(OUT / "connect-2.mp4"), 1280, 680)
make(V, [(42, 74, 8, APP, [FONTLY]), (74, 102, 2, APP, [FONTLY])], str(OUT / "connect-3.mp4"), 1280, 680)
make(V, [(102, 143, 4, CHAT, []), (143, 166, 1, CHAT, [])], str(OUT / "connect-4.mp4"), 1150, 1020)
