"""קליפים לפרק "הפרויקט הראשון". הרצה: python3 first_project_clips.py <A.mp4> <B.mp4>"""
import sys
from pathlib import Path
from clips import make
A, B = sys.argv[1], sys.argv[2]
OUT = Path(__file__).resolve().parents[2] / "site/assets/images/guide"
M = (262, 50, 1660, 970)          # חלון ההגדרות
BR = (261, 105, 1659, 1025)       # דף בדפדפן, בלי שורת הכתובת
OWNER = (690, 735, 1100, 818)     # שם החשבון ב-GitHub בתוך ההגדרות
ENV = (880, 330, 1325, 662)       # התפריט שבמרכז
CHIP = (745, 975, 890, 1007)      # שם החשבון בכפתור Repo
make(A, [(3.6, 22.5, 1.6, M, []), (26.7, 28.8, 1, BR, [(935, 472, 1040, 505)]), (33.3, 36.5, 1, M, [])],
     str(OUT / 'first-1.mp4'))
make(A, [(136, 147, 1.4, M, [OWNER]), (197.3, 198.9, 0.8, BR, [(655, 172, 815, 212), (1200, 170, 1250, 216)]),
         (221, 223.2, 1, M, [OWNER])], str(OUT / 'first-2.mp4'))
C = (560, 280, 1640, 1012)
make(A, [(243.8, 251, 1, C, [ENV, (728, 862, 850, 895), CHIP])],
     str(OUT / 'first-3.mp4'), 1080, 616)
P = (290, 50, 1460, 1010)
make(B, [(3, 33, 3, (560, 280, 1640, 1012), [ENV, CHIP]), (33, 95, 4, P, [CHIP]), (95, 98, 1, P, [])], str(OUT / 'first-4.mp4'), 1170, 960)
