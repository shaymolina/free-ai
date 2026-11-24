"""קליפים לפרק "מתקינים סקיל ומשתמשים בו". הרצה: python3 skill_use_clips.py <video.mp4>"""
import sys
from pathlib import Path
from clips import make
V = sys.argv[1]
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
BR = (168, 145, 1735, 1020)       # דף הסקיל בדפדפן, בלי שורת הכתובת והסימניות
APP = (0, 0, 1920, 1020)          # אפליקציית קלוד, בלי שורת המשימות
CHAT = (330, 0, 1480, 1020)       # חלון השיחה
make(V, [(4.5, 8, 1, BR, [])], str(OUT / "skilluse-1.mp4"), 1280, 716)
make(V, [(18.7, 24.2, 1, APP, []), (28.2, 37, 1, APP, [])], str(OUT / "skilluse-2.mp4"), 1280, 680)
make(V, [(37, 52, 4, APP, []), (52, 66, 1.5, APP, [])], str(OUT / "skilluse-3.mp4"), 1280, 680)
make(V, [(64, 92, 2, CHAT, []), (92, 680, 45, CHAT, []), (680, 704, 1.2, CHAT, [])], str(OUT / "skilluse-4.mp4"), 1150, 1020)
