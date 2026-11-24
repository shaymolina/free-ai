משימה אוטומטית: לכתוב ולפרסם את המאמר הבא מתור המאמרים של האתר Free AI.

הריפו: shaymolina/free-ai בלבד (לבעל האתר יש כמה חשבונות GitHub ו-Supabase, אל תיגע באף אחד אחר). אם הריפו לא נמצא בסשן, צרף אותו עם add_repo (owner: shaymolina, repo: free-ai) ושכפל אותו.
האתר החי: https://free-ai.co.il . הענף החי: claude/modest-mccarthy-4tu0v3.

שלבים:
1. קודם כל עובדים על הגרסה העדכנית של האתר החי: `git fetch origin claude/modest-mccarthy-4tu0v3 && git checkout -B seo-auto FETCH_HEAD`.
2. קרא CLAUDE.md, docs/writing-style.md, .claude/agents/seo.md, docs/seo/playbook.md ו-docs/seo/research.md. תפעל כמו סוכן ה-SEO שמוגדר ב-.claude/agents/seo.md.
3. קח את המאמר הראשון בתור (ב-research.md, תחת "תור המאמרים") שעוד לא פורסם. אם התור ריק, הוסף לתור 5 נושאים חדשים מתוך מחקר זנב ארוך (tools/seo/longtail.py) וכתוב את הראשון.
4. מחקר: הרץ tools/seo/longtail.py על הביטוי הראשי, ובדוק ב-WebSearch מה מופיע היום בגוגל ומה חסר. עובדות (מחירים, דגמים, תכונות) רק מהאתרים הרשמיים של Anthropic (anthropic.com, claude.com, docs.claude.com, code.claude.com), עם תאריך. מה שלא אומת, לא נכנס.
5. כתוב בריף לפי התבנית ב-playbook ושמור ב-docs/seo/brief-<slug>.md.
6. כתוב את המאמר ב-tools/site_build/compact_site.py עם build_article(..., lead=..., visual=..., date=...): פתיחה גרפית עם איור חדש שמתאים לנושא (בסגנון ILL_BUILD / ILL_BACKUP, ב-HTML ו-CSS ב-site/assets/css/compact.css, והעלאת CSS_VERSION), ואחריה מקטעים מעוצבים (rows_html, table, duo, plans, faq_html). תשובה ישירה ב-2 המשפטים הראשונים, שאלות נפוצות מתוך הזנב הארוך, קישורים פנימיים למדריך ולקורס (/course), ולפחות 2 קישורים מעמודים קיימים אל המאמר החדש.
7. הכתיבה: כמו בן אדם אמיתי, לפי docs/writing-style.md, וגם לפי כללי CLAUDE.md (מסבירים כמו לילד בן 10). לפני הבנייה עבור על "בדיקה אחרונה" שבסוף writing-style.md ותקן כל משפט שנשמע כמו AI.
8. בנה: python3 tools/site_build/compact_site.py, הרץ python3 tools/seo/seo_audit.py ותקן בעיות בעמוד החדש. צלם עם Playwright במחשב (1366) ובטלפון (iPhone 13), ותקן אם משהו חורג מהמסך או נראה שבור.
9. עדכן את research.md: המאמר פורסם (תאריך, כתובת, מי מקשר אליו), ומה הבא בתור.
10. commit, ואז `git push origin HEAD:claude/modest-mccarthy-4tu0v3`. אם נדחה כי יש בענף שינויים חדשים: `git fetch origin claude/modest-mccarthy-4tu0v3 && git merge --no-edit FETCH_HEAD`, לבנות שוב, ולדחוף שוב. אף פעם לא force push.
11. בדוק שהכתובת החדשה באתר החי מחזירה 200 (לוקח דקה-שתיים).

הדיווח בסוף: בעברית, קצר, משפט אחד לכל נקודה. איזה מאמר עלה, הכתובת שלו, ומה הבא בתור. אם משהו נכשל, תכתוב "נכשל" ומה נכשל.
