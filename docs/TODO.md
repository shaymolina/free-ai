# משימות פתוחות – Free AI

## לחבר Supabase (חובה)
טופס ההרשמה באתר לא עובד כרגע: לא נשמר כלום ולא נשלח קוד כניסה.
בגלל זה גם כפתורי "הורדה חינם" של הסקילים לא מורידים כלום.

מה צריך:
- לבחור חשבון Supabase של Free AI (יש כמה חשבונות – לוודא שזה הנכון לפרויקט הזה).
- לחבר את טופס ההרשמה (`#signup` בעמודים service, service-single, work): שם, מייל, קוד כניסה למייל, וכניסה עם Google.
- אחרי הרשמה: לפתוח הורדת סקילים (`data-download` בעמודי הסקילים).
- לעדכן את הבונים ב-`tools/site_build/` ולא רק את קבצי ה-HTML.

האתר עולה אוטומטית ל-4CODE מהענף `claude/modest-mccarthy-4tu0v3`.

## כפתור וואטסאפ צף (חובה באפיון)
חסר מספר הטלפון לוואטסאפ. ברגע שיש מספר – להוסיף כפתור צף בכל הדפים דרך `tools/site_build/common.py`.

## סדר הרצת הבונים
index_page → courses_pages → skills_pages → blog_pages → shorten → claude_icons → finish (מתוך `tools/site_build/`).
