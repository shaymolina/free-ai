"""מציאת ביטויי זנב ארוך מההשלמה האוטומטית של גוגל (בעברית, ישראל).
לוקח ביטוי בסיס ומוסיף לו מילות שאלה ואותיות, כמו שמשתמש מקליד בגוגל.
הרצה: python3 tools/seo/longtail.py "קלוד קוד" ["claude code" ...]  [--deep]
--deep מוסיף גם את כל האותיות (עברית + אנגלית) – יותר תוצאות, יותר זמן."""
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import OrderedDict

URL = "https://suggestqueries.google.com/complete/search?client=firefox&hl=he&gl=il&q="
PREFIXES = ["מה זה", "איך", "למה", "האם", "כמה", "מה ההבדל בין", "מדריך", "קורס", "הכי טוב"]
SUFFIXES = ["", "מה זה", "איך", "מחיר", "בחינם", "בעברית", "מדריך", "למתחילים", "קורס", "מול",
            "או", "לעומת", "התקנה", "דוגמאות", "בעיות", "לא עובד", "טיפים", "2026", "windows", "mac",
            "vs", "pricing", "skills", "mcp", "free"]
HE = list("אבגדהוזחטיכלמנסעפצקרשת")
EN = list("abcdefghijklmnopqrstuvwxyz")


def suggest(q):
    try:
        with urllib.request.urlopen(URL + urllib.parse.quote(q), timeout=10) as r:
            return json.loads(r.read().decode("utf-8", "replace"))[1]
    except Exception as e:
        print(f"נכשל: {q} ({e})", file=sys.stderr)
        return []


def expand(seed, deep=False):
    queries = [seed] + [f"{seed} {s}".strip() for s in SUFFIXES] + [f"{p} {seed}" for p in PREFIXES]
    if deep:
        queries += [f"{seed} {c}" for c in HE + EN]
    found = OrderedDict()
    for q in queries:
        for s in suggest(q):
            found.setdefault(s.strip(), q)
        time.sleep(0.15)
    return found


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    deep = "--deep" in sys.argv
    if not args:
        print(__doc__)
        return
    for seed in args:
        found = expand(seed, deep)
        print(f"\n## {seed} – {len(found)} ביטויים")
        for s in found:
            tag = "שאלה" if s.split()[0] in ("מה", "איך", "למה", "האם", "כמה", "what", "how", "why", "is") else ""
            print(f"- {s}" + (f"  ({tag})" if tag else ""))


if __name__ == "__main__":
    main()
