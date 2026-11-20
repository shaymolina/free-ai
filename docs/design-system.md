# Design System - מפרט עיצוב מלא (גרסה כללית לכל אתר)

> מסמך זה מיועד למנוע AI (Claude או אחר) שמעצב מערכת או אתר בשפת עיצוב אחת קבועה:
> ממשק ניהול ניטרלי ואפור בסגנון **Supabase Dashboard**, עם טוקנים בסגנון **shadcn/ui**, תמיכה מלאה בעברית (RTL) ובמצב כהה/בהיר.
> כל הערכים נמדדו ממערכת חיה שנבנתה בשפה הזו, ולכן הם מדויקים. **כשיש סתירה בין המסמך לבין "מה שנראה הגיוני" - המסמך קובע.**
> **בקשה מפורשת של בעל האתר גוברת על המסמך.**

---

## א. איך עובדים עם המסמך (חובה לקרוא לפני כל שינוי)

1. **לקרוא את כל המסמך** לפני שמתחילים, כולל רשימת הבדיקה (סעיף 16).
2. **לשנות רק עיצוב.** לא לשנות פונקציונליות, לוגיקה, נתונים, ניתוב, שמות שדות או טקסטים - אלא אם התבקש במפורש.
3. **להכיר את הפרויקט קודם:** איזה סגנונות יש (Tailwind / shadcn/ui / CSS רגיל / ספריית רכיבים אחרת), איפה מוגדרים הצבעים, איזה רכיבים משותפים קיימים (כפתור, כרטיס, שדה, טבלה, תפריט).
4. **סדר העבודה:**
   1. טוקנים - סעיף 17 (קובץ מוכן) לתוך קובץ ה-CSS הגלובלי. אם הפרויקט משתמש ב-shadcn/ui: להחליף את ערכי המשתנים הקיימים שלו בערכים מכאן (אם הם כתובים בפורמט HSL בלי `hsl()` - להמיר את הערכים לפורמט הזה, לא לשנות את הפורמט).
   2. גופנים (סעיף 2) ומצב כהה/בהיר (סעיף 15).
   3. מעטפת: תפריט צד, טופבר, אזור תוכן (סעיפים 4-6).
   4. רכיבים משותפים: כפתור, שדה, מתג, כרטיס, טבלה, תג, התראה, מודאל, תפריט נפתח (סעיפים 7-11).
   5. רק אחר כך - כל עמוד ועמוד (סעיף 18 = דפוסי עמודים נפוצים).
5. **לתקן ברכיב המשותף, לא בכל מקום בנפרד.** אם יש `<Button>` משותף - משנים אותו, ולא דורסים מחלקות בכל עמוד.
6. **אין צבע קשיח ברכיבים.** כל צבע = משתנה מסעיף 17. צבע חדש = להוסיף לו גם גרסה כהה.
7. **שמות המחלקות במסמך הם דוגמה.** אפשר לממש באותם ערכים עם מחלקות Tailwind או בשמות שכבר קיימים בפרויקט. מה שקובע זה הערכים (מידות, צבעים, צללים, רדיוסים, מעברים).
8. **רכיב שלא מופיע במסמך** - לבנות אותו מהטוקנים ומהעקרונות של סעיף 0, בדומה לרכיב הקרוב ביותר שכן מופיע. לא להמציא סגנון חדש.
9. **לא להוסיף** רכיבים, עמודים, אנימציות או קישוטים שלא התבקשו.
10. **בסוף:** לעבור על רשימת הבדיקה (סעיף 16) ולצלם כל עמוד ב-390px ובמחשב, בכהה ובבהיר. לבדוק שאין גלילה לרוחב.

## ב. התאמה למותג של האתר

כל המסמך ניטרלי. מה שמשתנה מאתר לאתר הוא **רק**:
- **הצבע הראשי** - `--primary`, `--primary-hover`, `--ring`, `--info` (בבהיר ובכהה). ברירת המחדל כחול (`#2080e8` בהיר / `#3d92f0` כהה). אם למותג יש צבע אחר: הגרסה הבהירה בגוון כהה מספיק לניגודיות AA עם טקסט לבן, הגרסה הכהה בהירה בכ-8%, וה-hover בהיר עוד כ-4% מהבסיס (hover **מתבהר**, לא מתכהה).
- **הלוגו ושם המערכת** בתפריט הצד (סעיף 6.1) ובעמוד ההתחברות (סעיף 14). לוגו בהיר למצב כהה אם צריך.
- **השפה** - עברית (RTL) כברירת מחדל; אם האתר באנגלית בלבד, כל כללי ה-RTL פשוט לא חלים, והמאפיינים הלוגיים עובדים לבד.

כל השאר (אפורים, רדיוסים, ריווח, צללים, גופן, צפיפות) **לא משתנה**.

---

## 0. עקרונות על (חובה, לפני הכל)

1. **ניטרלי ואפור.** אין כחול בריחוף, בהדגשה, בפריט פעיל או ברקע של שום דבר. כחול מופיע רק ב: כפתור ראשי, מתג במצב פעיל, קישור טקסט, טבעת פוקוס, תג ספירה (badge) קטן, כפתור החץ בפינת כרטיס, וי ברשימת פיצ'רים.
2. **אייקונים בלי מסגרת אף פעם.** לא border, לא outline, ולא טבעת אחרי לחיצת עכבר. ריחוף/פעיל = רקע אפור עדין בלבד. **חריג לנגישות:** בניווט מקלדת (`:focus-visible` בלבד) - טבעת פוקוס כמו בכפתורים.
3. **רווח אחיד בין כרטיסים**: אותו רווח בדיוק בין כרטיסים זה לצד זה, זה מעל זה, ומשולי העמוד. 24px בדסקטופ, 16px מתחת ל-992px.
4. **כרטיסים בלי border.** במקום border: קו דק (hairline) כצל `0 0 0 1px` + צל קל.
5. **שדה קלט = צבע רקע הדף** (לא צבע הכרטיס). בכהה השדה שחור #0a0a0a בתוך כרטיס #131313.
6. **אסור "AI slop":** אסור פס צבעוני בצד אחד/למעלה של כרטיס (border-left/right/top לציון מצב), אסור גרדיאנטים על כרטיסים, אסור צללים כבדים צבעוניים, אסור אימוג'י כאייקונים.
7. **גופן אחד: Noto Sans** (+ Noto Sans Hebrew לעברית). מונו: JetBrains Mono. שום גופן אחר.
8. **RTL מלא** (עברית ברירת מחדל) + LTR לאנגלית. משתמשים במאפיינים לוגיים (`inset-inline-start`, `margin-inline-end`, `padding-inline` וכו'), לא left/right.
9. **צפיפות Supabase:** שדות 32px, כפתורים 28px, טקסט פקדים 13px.

---

## 1. צבעים (Design Tokens)

### 1.1 מצב כהה

| טוקן | ערך | שימוש |
|---|---|---|
| `--background` | `#0a0a0a` | רקע הדף, תפריט הצד, פאנל הצד, רקע שדות קלט, רקע כפתור משני |
| `--foreground` | `#ededed` | טקסט ראשי, אייקונים |
| `--card` | `#131313` | רקע כרטיס |
| `--card-foreground` | `#ededed` | |
| `--popover` | `#171717` | חלונות קופצים, תפריטים נפתחים, שורת שמירה צפה, מודאל |
| `--secondary` | `#1c1c1c` | רקע תגיות ניטרליות |
| `--muted` | `#101010` | רקע שקט (שדה מושבת) |
| `--muted-foreground` | `oklch(71.55% 0 0)` ≈ `#a3a3a3` | טקסט משני, תיאורים, כותרות עמודות |
| `--border` / `--hairline` | `#232323` | קווי הפרדה, קו דק של כרטיס |
| `--input` | `#2e2e2e` | מסגרת שדה, מסגרת כפתור משני, מתג כבוי |
| `--primary` | `#3d92f0` | כחול מוביל |
| `--primary-hover` | `#449eff` | |
| `--primary-foreground` | `#ffffff` | |
| `--ring` | `#3d92f0` | פוקוס |
| `--accent` (ריחוף) | `color-mix(in oklch, #ededed 8%, transparent)` | רקע ריחוף כללי - אפור שקוף |
| `--nav-fg` | `#ededed` ב-68% שקיפות | טקסט פריט תפריט רגיל |
| `--nav-hover` | `#ededed` ב-6% שקיפות | ריחוף בתפריט |
| `--nav-active` | `#ededed` ב-10% שקיפות | פריט תפריט פעיל |
| `--destructive` | `oklch(72% .15 25.33)` (אדום-ורדרד) | |
| `--warning` | `oklch(82.8% .15 84.43)` (צהוב-ענבר) | |
| `--success` | `oklch(76% .14 155)` (ירוק) | |
| `--info` | `#3d92f0` | |
| קו פנימי בכרטיס תוכנית | `#2e2e2e` | `--plan-line` בכהה (בבהיר `#e6e6e6`) |

### 1.2 מצב בהיר

| טוקן | ערך |
|---|---|
| `--background` | `#fafafa` (גם תפריט צד, פאנל, טופבר) |
| `--foreground` | `#171717` |
| `--card` | `#ffffff` |
| `--popover` | `#ffffff` |
| `--secondary` | `#f6f6f6` |
| `--muted` | `#f9f9f9` |
| `--muted-foreground` | `#6b6b6b` |
| `--border` / `--hairline` / `--sidebar-border` | `#e6e6e6` |
| `--input` | `#dedede` |
| `--accent` / `--nav-hover` / `--nav-active` | `#f0f0f0` (ריחוף ופעיל - אותו אפור) |
| `--primary` | `#2080e8` |
| `--primary-hover` | `#278cfa` |
| `--ring` | `#2080e8` |
| `--destructive` | `oklch(55% .2 25.33)` |
| `--warning` | `oklch(66.6% .15 58.32)` |
| `--success` | `oklch(56% .13 155)` |
| ראש טבלה | רקע `#fafafa` |
| פס גלילה | thumb `#e2e2e2` (ריחוף `#d2d2d2`), 8px, פינות 8px, track שקוף |

### 1.3 צללים

```css
/* כהה */
--shadow-xs: 0 1px 3px 0 #0000000d;
--shadow-md: 0 1px 3px 0 #0000001a, 0 2px 4px -1px #0000001a;
--shadow-lg: 0 1px 3px 0 #0000001a, 0 4px 6px -1px #0000001a;
/* בהיר */
--shadow-xs: 0 1px 2px 0 #1a1f2c0a, 0 0 0 1px #1a1f2c05;
--shadow-md: 0 1px 2px 0 #1a1f2c0d, 0 4px 12px -4px #1a1f2c14;
--shadow-lg: 0 2px 4px 0 #1a1f2c0d, 0 12px 28px -8px #1a1f2c1f;
```

### 1.4 צבעי מצב (status) - תמיד "רך": רקע שקוף מהגוון + טקסט בגוון

| מצב | רקע | טקסט |
|---|---|---|
| פעיל / שולם / הושלם | `color-mix(in oklch, var(--success) 16%, transparent)` | `var(--success)` |
| ממתין / לא שולם / בטיפול | `color-mix(in oklch, var(--warning) 18%, transparent)` | `var(--warning)` |
| מושעה / באיחור / בוטל-שגיאה | `color-mix(in oklch, var(--destructive) 14%, transparent)` | `var(--destructive)` |
| סגור / בוטל / הוחזר | `var(--secondary)` + border 1px `var(--border)` | `var(--muted-foreground)` |

### 1.5 בחירת טקסט
`::selection { background: color-mix(in oklch, var(--primary) 35%, transparent); }` (בבהיר 22%).

---

## 2. טיפוגרפיה

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@100..900&family=Noto+Sans:wght@100..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

```css
--font-sans: "Noto Sans", "Noto Sans Hebrew", ui-sans-serif, sans-serif, system-ui;
--font-mono: "JetBrains Mono", ui-monospace, monospace;
body { font-size: 15px; line-height: 1.5; -webkit-font-smoothing: antialiased; }
```

| אלמנט | גודל | משקל | צבע |
|---|---|---|---|
| טקסט גוף | 15px (.9375rem) | 400 | foreground |
| כותרת עמוד (h1) | 22px (1.375rem) | 600 | foreground |
| כותרת סעיף מעל כרטיס | 18px (1.125rem) | 500 | foreground |
| כותרת כרטיס | 15px (.9375rem) | 600 | foreground |
| תווית שדה בשורת הגדרות | 14px | 500 | foreground |
| טקסט עזר מתחת לתווית | 13px | 400 | muted-foreground |
| שדות קלט וכפתורים | 13px (.8125rem) | 400 / 500 | |
| כותרות עמודות טבלה | 13px | 500 | muted-foreground |
| תאי טבלה | 14px | 400 | |
| תג (badge) | 12px | 500 | |
| פוטר | 12px | 400 | muted-foreground |
| מספר גדול בכרטיס סטטיסטיקה | 22px, line-height 1.2 | 600 | foreground |
| מחיר גדול בכרטיס תוכנית | 34px (2.125rem), line-height 1.1, letter-spacing -.01em | 600 | foreground |
| שם המערכת בתפריט | 16px | 600 | |

- כל הכותרות: `letter-spacing: 0`, `text-wrap: balance`.
- מספרים בטבלאות ובתגים: `font-variant-numeric: tabular-nums`.
- מחירים: `direction: ltr; unicode-bidi: isolate;` גם בעברית.
- טקסט מעורב עברית/אנגלית בשורה: `unicode-bidi: plaintext`.
- שדות שהתוכן שלהם לטיני (email, url, tel, password, דומיין, מספר כרטיס): `direction: ltr` גם בעמוד עברי, `text-align: right` בעברית.
- **אסור** text-transform uppercase בעברית. כותרות קבוצה במונו+אותיות גדולות רק באנגלית (ראו 6.3).

---

## 3. עיגול פינות

| רכיב | רדיוס |
|---|---|
| כרטיס, כרטיס סטטיסטיקה, כרטיס תוכנית, מודאל, קופסת טבלה, כרטיס סעיף | **12px** (.75rem) |
| כפתור (כל גודל), שדה קלט, select, textarea, כפתור החץ בכרטיס | **8px** (.5rem) |
| חלון קופץ, תפריט נפתח, שורת שמירה צפה, התראה (alert) | **6px** (.375rem) |
| פריט בתוך תפריט, פריט תפריט ניווט, כפתור אייקון בטופבר | **4.8px** (.3rem) |
| תג / badge / סטטוס, מתג (switch) | 999px (גלולה) |
| אייקון עגול בכרטיס (chip) | 50% |
| דגל בתפריט שפה | 2px |

---

## 4. ריווח ופריסה

### 4.1 רווח כרטיסים (החוק החשוב ביותר)
```css
.app { --card-gap: 1.5rem; }                 /* 24px */
@media (max-width: 991.98px) { .app { --card-gap: 1rem; } }  /* 16px */
```
- padding של אזור התוכן = `var(--card-gap)` (24px מכל צד).
- gap בגרידים של כרטיסים = `var(--card-gap)`.
- margin-bottom של כל כרטיס = `var(--card-gap)`.
- כרטיסים באותה שורה = אותו גובה (`align-items: stretch`, הכרטיס האחרון בעמודה `flex: 1`).

### 4.2 מעטפת האפליקציה
```
┌──────────┬─────────────────────────────────────────────┐
│ תפריט    │ טופבר (56px, sticky)                        │
│ צד       ├─────────┬───────────────────────────────────┤
│ 212px    │ פאנל    │ תוכן (padding 24px)               │
│ (ניתן    │ 192px   │                                   │
│ לגרירה)  │ (אופציה)│                                   │
└──────────┴─────────┴───────────────────────────────────┘
```
(ב-RTL התפריט מימין.)

- תפריט צד: רוחב 212px (`--sidebar-width`, ניתן לשנות בגרירה ונשמר ב-localStorage), `position: fixed`, רקע `--background`, קו `border-inline-end: 1px solid var(--border)`.
- מצב "מכווץ" (rail) בדסקטופ: 54px (3.375rem), רק אייקונים. מעבר: `.5s cubic-bezier(.45,0,.2,1)`. הטקסטים נעלמים ב-opacity .22s.
- פאנל צד של עמוד (`.panel`): 192px (12rem), גובה מלא `calc(100vh - 56px)`, sticky מתחת לטופבר, רקע `--background`, `border-inline-end` 1px.
- רוחב תוכן: מלא (אין max-width), מתחת ל-992px התפריט הופך ל-off-canvas עם overlay `#0008`.
- פוטר: מתחת לתוכן, `margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 12px; color: muted`.

### 4.3 נקודות שבירה
`576px` (טלפון) · `768px` · `992px` (מובייל/דסקטופ - תפריט, רווח כרטיסים) · `1200px` · `1400px`.
בדיקת מובייל ב-390px. מתחת ל-576px בטלפון: breadcrumb מציג רק את העמוד הנוכחי, טבלאות מסתירות עמודות משניות, אין גלילה אופקית לעולם.

---

## 5. הטופבר (Header) ואייקוני הפעולה

```css
.topbar {
  position: sticky; top: 0; z-index: 1020;
  display: flex; align-items: center; gap: 8px;
  height: 56px; padding: 8px 16px;
  background: color-mix(in oklch, var(--background) 85%, transparent);  /* בבהיר: #fafafa אטום */
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
```

**סדר בטופבר (RTL)** - רק האייקונים שיש להם תפקיד במערכת, לפי הסדר: בצד ההתחלה (ימין) - כפתור המבורגר (רק במובייל) + קו מפריד אנכי (1px × 16px, צבע border) + breadcrumb. בצד הסוף (שמאל) קבוצת אייקונים עם `gap: 4px`, לפי הסדר:

1. **שפה** - אייקון כדור הארץ (`earth`). פותח תפריט עם דגל (20×14.4px, רדיוס 2px, קו `0 0 0 1px hairline`) + שם שפה + וי בשפה הנוכחית. התפריט ברוחב התוכן (`width: max-content`).
2. **(אופציונלי) מטבע / הגדרה מהירה** - אייקון מתאים (למשל `circle-dollar-sign`).
3. **התראות** - אייקון פעמון (`bell`). אם יש התראות: עיגול ספירה כחול בפינה (ראו להלן). תפריט רחב 320px עם כותרת "התראות", כל פריט עם נקודה צבעונית 8px לפי חומרה (info כחול, warning, danger, success), ריק: "אין התראות" בצבע muted.
4. **מצב כהה/בהיר** - ירח במצב בהיר, שמש במצב כהה. שני האייקונים באותו מקום; המעבר: האייקון היוצא `opacity:0; transform: scale(.55) rotate(±25deg)`, מעבר `.33s`. לכפתור הזה **אין** רקע ריחוף בכלל. הבחירה נשמרת ב-localStorage (`light`/`dark`/`system`), ברירת מחדל לפי מערכת ההפעלה, נטען לפני רינדור (בלי הבהוב).
5. **(אופציונלי) פעולה נוספת** (עגלה, הודעות וכו') - אייקון + עיגול ספירה כשיש פריטים.

**כפתור אייקון (`.icon-btn`):**
```css
.icon-btn {
  width: 32px; height: 32px; padding: 0;
  display: inline-flex; align-items: center; justify-content: center;
  border: 0; border-radius: 4.8px; outline: none; box-shadow: none;
  background: transparent; color: var(--foreground);
}
.icon-btn:hover, .dropdown.open > .icon-btn { background: var(--accent); }  /* אפור שקוף, לא כחול */
.icon-btn:focus, .icon-btn:active { outline: none; box-shadow: none; border: 0; }
.icon-btn:focus-visible { outline: none; box-shadow: 0 0 0 2px color-mix(in oklch, var(--ring) 60%, transparent); }  /* מקלדת בלבד */
.icon-btn svg { width: 16px; height: 16px; }
```

**עיגול ספירה (`.dot-badge`):**
```css
position: absolute; top: -2px; inset-inline-end: -2px;
min-width: 16px; height: 16px; padding: 0 4px; border-radius: 999px;
font-size: 10px; font-weight: 600; line-height: 1;
background: var(--primary); color: #fff;
```

**Breadcrumb:** 14px, פריטים קודמים `muted-foreground` (ריחוף: foreground), נוכחי `foreground`, מפריד `/` בצבע muted עם 8px מכל צד. בטלפון רק הפריט האחרון.

**תפריט נפתח מהטופבר:** נפתח למטה (`top: calc(100% + 6px)`), מיושר לקצה הסוף. אנימציית פתיחה: `from { opacity:0; transform: translateY(4px) scale(.98) } to { none }` במשך `.12s ease-out`. בטלפון התפריט הרחב נפרש לרוחב המסך עם 16px שוליים.

---

## 6. תפריטים (סגנון Supabase)

### 6.1 תפריט צד ראשי
- כותרת: גובה 56px, `border-bottom: 1px solid var(--border)`, לוגו 24×24 + שם המערכת (16px/600), ריחוף על המותג `--nav-hover`, רדיוס 4.8px.
- אזור הקישורים: padding 8px, קבוצות מופרדות בקו 1px לכל רוחב התפריט.
- **פריט תפריט:**
```css
.nav-link {
  display: flex; align-items: center; gap: 10px;
  height: 36px; padding: 8px 10px; border-radius: 4.8px;
  font-size: 15px; font-weight: 400;
  color: var(--nav-fg);            /* foreground ב-68% */
  background: transparent;
  transition: background-color .12s, color .12s;
}
.nav-link svg { width: 18px; height: 18px; }
.nav-link:hover  { background: var(--nav-hover);  color: var(--foreground); }   /* 6% */
.nav-link.active { background: var(--nav-active); color: var(--foreground); font-weight: 500; } /* 10% */
```
- בתחתית התפריט: קישורים משניים (למשל "הגדרות"), מופרדים בקו מהקבוצות הראשיות.
- **פוטר התפריט:** `border-top: 1px`, שורה: אייקון אדם + שם המשתמש (מוביל לפרטי חשבון, בלי תפריט נפתח) + כפתור כיווץ (אייקון `panel-left-open`, 36×36, צבע nav-fg, מתהפך ב-RTL).
- אין תפריט נפתח למשתמש.

### 6.2 תת-תפריט
`margin-inline-start: 19px; padding-inline-start: 14px; border-inline-start: 1px solid var(--border);` פריטים 32px גובה, אותם צבעים.

### 6.3 פאנל צד של עמוד (הפאנל השני)
```css
.panel { width: 192px; background: var(--background); border-inline-end: 1px solid var(--border); }
.panel-title { height: 48px; padding: 0 20px; border-bottom: 1px solid var(--border); font-size: 15px; font-weight: 500; }
.panel-group { padding: 14px 0 12px; border-bottom: 1px solid var(--border); }
.panel-group-title {             /* אנגלית */
  padding: 0 20px 8px; font-family: var(--font-mono); font-size: 12px; font-weight: 400;
  letter-spacing: .06em; text-transform: uppercase; color: var(--muted-foreground);
}
[dir=rtl] .panel-group-title { font-family: var(--font-sans); font-weight: 600; letter-spacing: 0; text-transform: none; }
.panel-item {
  min-height: 32px; padding: 5px 12px; margin: 0 8px; border-radius: 4.8px;
  font-size: 14px; color: var(--nav-fg); background: transparent;
}
.panel-item:hover  { background: var(--nav-hover);  color: var(--foreground); }
.panel-item.active { background: var(--nav-active); color: var(--foreground); font-weight: 400; }
.panel-sep { height: 1px; margin: 6px 12px; background: var(--border); }
```
- בפאנל אין אייקונים ליד הפריטים. ספירות בפאנל: תג שקוף עם קו 1px ובמונו 11px.
- כותרת הכרטיס הראשון של הפאנל משמשת ככותרת הפאנל.
- מתחת ל-992px הפאנל נהיה בלוק מעל התוכן (בלי כותרת), הקבוצות נפתחות/נסגרות בלחיצה על הכותרת.
- דוגמה: פאנל "חשבון" = כללי, משתמשים, אנשי קשר, [קו הפרדה], פרופיל, התנתקות. הגדרות קטנות (סיסמה וכו') הן סעיפים בתוך עמוד, לא פריטים נפרדים בפאנל.
- פאנל עם טקסט הסבר (למשל "טעינת כסף"): הטקסט 13px בצבע nav-fg, padding 0 20px, ואחריו קבוצת קישורים.

### 6.4 תפריט נפתח (dropdown / popover)
```css
.menu {
  min-width: 240px; padding: 4px;
  background: var(--popover); color: var(--foreground);
  border-radius: 6px; box-shadow: var(--shadow-lg); outline: 1px solid var(--hairline);
}
.menu-item {
  display: flex; align-items: center; gap: 8px; min-height: 32px; padding: 6px 8px;
  border-radius: 4.8px; font-size: 14px;
}
.menu-item:hover { background: var(--accent); }        /* אפור */
.menu-sep { height: 1px; margin: 4px -4px; background: var(--border); }
.menu-title { padding: 6px 8px; font-size: 12px; font-weight: 500; color: var(--muted-foreground); }
.menu-item .check { margin-inline-start: auto; width: 16px; height: 16px; }  /* וי בפריט הנבחר */
```
רשימות ארוכות (מדינות, קידומות טלפון): גובה מקס' 240px, גלילה, פריטים 13px עם רדיוס 4.8px, צל `0 8px 24px rgba(0,0,0,.18)`.

---

## 7. כרטיסים

### 7.1 כרטיס רגיל
```css
.card {
  background: var(--card); color: var(--card-foreground);
  border: 0; border-radius: 12px;
  box-shadow: var(--shadow-xs), 0 0 0 1px var(--hairline);   /* כהה: rgba(0,0,0,.05) 0 1px 3px, #232323 0 0 0 1px */
  margin-bottom: var(--card-gap);
}
.card-header { padding: 10px 20px; min-height: 56px; display: flex; align-items: center; gap: 8px; background: transparent; }
.card-title  { font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 8px; margin: 0; }
.card-title > svg { color: var(--muted-foreground); width: 16px; height: 16px; }
.card-body   { padding: 20px; }
.card-footer { padding: 12px 20px; border-top: 1px solid var(--border); background: transparent; }
```
- **אין** border, **אין** פס צבעוני, **אין** גרדיאנט.
- שורות בתוך כרטיס (list): padding `10px 20px`, קו הפרדה 1px border, טקסט 14px.

### 7.2 כרטיס סטטיסטיקה (4 בשורה בדף הבית)
```css
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(10rem,100%), 1fr)); gap: var(--card-gap); }
.tile {
  position: relative; display: flex; align-items: flex-start; gap: 12px; padding: 20px;
  background: var(--card); border-radius: 12px; box-shadow: var(--shadow-xs), 0 0 0 1px var(--hairline);
  transition: box-shadow .15s, background-color .15s;
}
.tile:hover { background: color-mix(in oklch, var(--card) 94%, var(--foreground)); box-shadow: var(--shadow-xs), 0 0 0 1px var(--border); }
/* בבהיר: hover = #fafafa */
.tile-icon {               /* עיגול האייקון */
  width: 40px; height: 40px; border-radius: 50%; border: 0;
  background: color-mix(in oklch, var(--foreground) 6%, transparent);
  display: flex; align-items: center; justify-content: center; color: var(--foreground);
}
.tile-stat  { font-size: 22px; font-weight: 600; line-height: 1.2; }
.tile-label { font-size: 13px; font-weight: 500; color: var(--muted-foreground); }
.tile-go    { width: 16px; height: 16px; color: var(--muted-foreground); }  /* חץ בפינה */
.tile:hover .tile-go { color: var(--foreground); }
```
- כל הכרטיס הוא קישור. אייקון עגול בצד ההתחלה, מספר מעל תווית, וחץ אלכסוני דק בפינה העליונה בצד הסוף.
- **החץ:** heroicons `arrow-up-right` (path `m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25`), `stroke-width: 1.5`. ב-RTL מתהפך (`transform: scaleX(-1)`) כך שמצביע למעלה-שמאלה. בריחוף הקו "מצטייר" (אנימציה), החץ לא זז.

### 7.3 כפתור החץ הכחול בפינת כרטיס (מעבר מכרטיס סיכום לעמוד המלא)
```css
.card { position: relative; }
.card-corner-btn {
  position: absolute; top: 16px; inset-inline-end: 16px;
  width: 28px; height: 28px; padding: 0;
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--primary);         /* #3d92f0 כהה / #2080e8 בהיר */
  color: #fff; border: 0; border-radius: 8px; box-shadow: none; outline: 0;
}
.card-corner-btn svg { width: 16px; height: 16px; color: #fff; transition: transform .15s; }  /* arrow-up-right */
[dir=rtl] .card-corner-btn svg { transform: scaleX(-1); }
.card-corner-btn:hover { background: color-mix(in srgb, var(--primary) 92%, #000); }
.card-corner-btn:hover svg { transform: translate(2px,-2px); }
[dir=rtl] .card-corner-btn:hover svg { transform: scaleX(-1) translate(2px,-2px); }
```

### 7.4 כרטיס תוכנית / מחיר
```css
.plans { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(12rem,100%), 1fr)); gap: var(--card-gap); }
.plan {
  position: relative; display: flex; flex-direction: column; align-items: flex-start;
  padding: 20px 20px 0; background: var(--card); border: 0; border-radius: 12px;
  box-shadow: var(--shadow-xs), 0 0 0 1px var(--hairline);
}
.plan:hover { background: color-mix(in oklch, var(--card) 94%, var(--foreground)); }
.plan.current { box-shadow: var(--shadow-xs), 0 0 0 1px color-mix(in oklch, var(--foreground) 35%, transparent); }
.plan-name  { font-size: 13px; font-weight: 500; color: var(--muted-foreground); display:flex; gap:8px; align-items:center; }
.plan-price strong { font-size: 34px; font-weight: 600; line-height: 1.1; letter-spacing: -.01em; direction: ltr; }
.plan-price span   { font-size: 13px; color: var(--muted-foreground); }   /* "/ לחודש" */
.plan-desc { align-self: stretch; margin: 16px -20px 0; padding: 16px 20px 20px; border-top: 1px solid var(--plan-line); }
.plan-badge { /* "התוכנית הנוכחית" */
  height: 16px; padding: 0 8px; border-radius: 999px; font-size: 11px;
  background: transparent; color: var(--primary); border: 1px solid color-mix(in srgb, var(--primary) 45%, transparent);
}
.plan-features { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 5px 12px; font-size: 13px; color: var(--muted-foreground); }
.plan-features li::before { content: "\2713"; color: var(--primary); font-weight: 600; margin-inline-end: 8px; }
```

### 7.5 כרטיס "סעיף הגדרות" (Supabase) - עמודי טפסים
מבנה: **כותרת מעל הכרטיס** (18px/500, margin-bottom 12px), ואז כרטיס אחד עם שורה לכל הגדרה.
```css
.sec-title { margin: 0 0 12px; font-size: 18px; font-weight: 500; }
.sec-body  { background: var(--card); border: 0; border-radius: 12px; box-shadow: var(--shadow-xs), 0 0 0 1px var(--hairline); }
.sec-row {
  display: grid; grid-template-columns: minmax(0,1fr) minmax(0,22rem); column-gap: 24px; align-items: center;
  padding: 14px 24px; border-bottom: 1px solid var(--border);
}
.sec-row:last-child { border-bottom: 0; }
.sec-row > label { font-size: 14px; font-weight: 500; }           /* צד התחלה */
.sec-row > small { font-size: 13px; color: var(--muted-foreground); line-height: 1.4; }  /* מתחת לתווית */
.sec-row > .control { grid-column: 2; }                             /* שדה בצד הסוף, 352px */
@media (max-width: 767px) { .sec-row { grid-template-columns: 1fr; row-gap: 8px; padding-inline: 16px; } }
```
- שורת כותרת תחתונה של כרטיס עם כפתורים: `justify-content: flex-end; gap: 8px`, הערה בצד ההתחלה בצבע muted 13px.
- כל בחירת כן/לא = **מתג**, לא checkbox.

### 7.6 קופסת טבלה
`background: var(--card); border-radius: 12px; box-shadow: var(--shadow-xs), 0 0 0 1px var(--hairline); padding: 0; overflow: visible;`

### 7.7 מודאל (חלון פרטים)
- הקופסה היא **כרטיס רגיל**: רקע `--card` (#131313), רדיוס 12px, hairline + shadow-xs, padding 28px, רוחב עד 672px, ממורכז.
- רקע מאחור: `rgba(0,0,0,.6)`, בלי טשטוש.
- כפתור X: 32×32 בפינה העליונה (16px מהקצוות), שקוף, צבע muted, בריחוף foreground, בלי רקע ובלי מסגרת.
- תוכן: שם 28px/500 + תגית סטטוס (13px, padding `3px 12px`, גלולה) באותה שורה וממורכזים; מתחת שורת משנה muted 15px.
- רשימת פרטים בשתי עמודות: כל שורה `display:flex; justify-content:space-between; padding:10px 0; border-top:1px solid var(--border)`, תווית muted 15px, ערך 15px/500.
- שורת פעולות: כפתורים ברוחב שווה (`flex:1`), ראשי, משני, וקישור מחיקה אדום (טקסט בלבד).
- Esc סוגר.

---

## 8. כפתורים

### 8.1 כללי (כל הכפתורים)
```css
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  min-height: 28px; padding: 4px 12px;
  font-family: inherit; font-size: 13px; font-weight: 500; line-height: 1.25;
  border: 1px solid transparent; border-radius: 8px;
  transition: background-color .15s, color .15s, border-color .15s, box-shadow .15s;
  cursor: pointer;
}
.btn:active   { transform: translateY(1px); }               /* לחיצה מורידה פיקסל */
.btn:focus-visible { outline: none; box-shadow: 0 0 0 3px color-mix(in oklch, var(--ring) 50%, transparent); }
.btn:disabled { opacity: .5; pointer-events: none; }
```
אין גדלים שונים: גם "גדול" וגם "קטן" = 28px/13px.

### 8.2 כפתור ראשי (כחול) - כולל ה"גימור" עם הצבע במסגרת
זה הכפתור עם "קצת צבע במסגרת": מסגרת פנימית דקה (inset) + הדגשה עליונה + צל רך + טקסט עם גוון כחלחל. מבוסס Supabase.
```css
:root      { --btn-finish: 0 1px 3px 0 rgb(0 0 0 / .04), inset 0 1px 0 0 rgb(0 0 0 / .024), inset 0 0 0 1px rgb(0 0 0 / .036), inset 0 -1px 0 0 rgb(0 0 0 / .036), inset 0 0 0 1px rgb(0 0 0 / .06); }
:root.dark { --btn-finish: 0 1px 3px 0 rgb(0 0 0 / .2), inset 0 1px 0 0 rgb(255 255 255 / .04), inset 0 0 0 1px rgb(255 255 255 / .06), inset 0 0 0 1px rgb(255 255 255 / .1); }

.btn-primary {
  background-color: var(--primary);                 /* #3d92f0 כהה, #2080e8 בהיר */
  background-image: linear-gradient(rgb(255 255 255 / .016), rgb(0 0 0 / .01));
  border-color: transparent;
  color: color-mix(in oklch, #fff 94%, var(--primary));   /* לבן עם נגיעת כחול */
  box-shadow: var(--btn-finish);
  transition: background-color .2s cubic-bezier(.22,1,.36,1), box-shadow .2s cubic-bezier(.22,1,.36,1), transform .2s cubic-bezier(.22,1,.36,1);
}
.btn-primary:hover  { background-color: var(--primary-hover); }   /* #449eff / #278cfa */
.btn-primary:focus-visible { box-shadow: var(--btn-finish), 0 0 0 3px color-mix(in oklch, var(--ring) 50%, transparent); }
.btn-primary:active { transform: scale(.97); }
```

### 8.3 כפתור משני (ביטול)
```css
.btn-secondary { background: var(--background); color: var(--foreground); border: 1px solid var(--input); }
/* כהה: רקע #0a0a0a, מסגרת #2e2e2e. בהיר: רקע #fafafa, מסגרת #dedede + צל shadow-xs */
.btn-secondary:hover { background: color-mix(in oklch, var(--foreground) 8%, transparent); }  /* בהיר: #f0f0f0 */
```

### 8.4 כפתור מחיקה / הרסני
```css
.btn-danger { background: color-mix(in oklch, var(--destructive) 12%, transparent); color: var(--destructive); border-color: transparent; }
.btn-danger:hover { background: color-mix(in oklch, var(--destructive) 22%, transparent); }
```
גרסת טקסט בלבד: רקע שקוף, טקסט אדום, בריחוף רקע אדום שקוף עדין.

### 8.5 כפתור הצלחה (רך)
`background: color-mix(in oklch, var(--success) 14%, transparent); color: var(--success);` ריחוף 24%.

### 8.6 כפתור קישור
רקע ומסגרת שקופים, צבע `--primary`, 13px.

### 8.7 כפתור אייקון בלבד בתוך תוכן
28×28 (או 32×32 בטופבר), רקע שקוף, **בלי מסגרת**, ריחוף `color-mix(in oklch, var(--foreground) 8%, transparent)`, רדיוס 8px (4.8px בטופבר/תפריט). אייקון 16px.

### 8.8 כפתור מלא ליד שדה (חוק "2 פיקסל")
שדה 32px ⇒ הכפתור **30px** (`height: calc(2rem - 2px)`), `align-self: center`, כלומר 1px מכל צד. הסיבה: המסגרת הדקה של השדה נבלעת בעין והכפתור המלא נראה גבוה יותר. לבדוק במדידה.

### 8.9 כפתור "+" עגול גדול (פתיחת תוכניות)
56×56, עיגול, כחול (`#3d92f0` כהה / `#2080e8` בהיר), אייקון + לבן 28px, ריחוף `#3687e0` / `#1d74d3`, בפתיחה ה-+ מסתובב 135° (`.4s cubic-bezier(.2,.8,.2,1)`), לחיצה מורידה פיקסל.

---

## 9. שדות קלט

```css
.input, select, textarea {
  min-height: 32px; padding: 4px 10px;
  font-family: inherit; font-size: 13px; line-height: 1.5; color: var(--foreground);
  background-color: var(--background);        /* צבע הדף! כהה #0a0a0a, בהיר #fafafa */
  border: 1px solid var(--input);              /* כהה #2e2e2e, בהיר #dedede */
  border-radius: 8px; box-shadow: none;
  transition: border-color .15s, box-shadow .15s;
}
textarea { min-height: 64px; }
.input::placeholder { color: var(--muted-foreground); }
/* פוקוס בסגנון Supabase: המסגרת מתבהרת + טבעת כחולה דקה עם רווח */
.input:focus {
  outline: none;
  border-color: var(--muted-foreground);
  box-shadow: 0 0 0 2px var(--card), 0 0 0 4px color-mix(in oklch, var(--primary) 55%, transparent);
}
.input:disabled, .input[readonly] { background: var(--muted); color: var(--muted-foreground); }
.input.invalid { border-color: var(--destructive); }
.label { font-size: 13px; font-weight: 500; }
.help  { font-size: 13px; color: var(--muted-foreground); }
.error { color: var(--destructive); }
```
- **iOS:** במכשירי iPhone/iPad מתחת ל-992px שדות ב-16px (אחרת הדפדפן עושה זום).
- **select:** אותו עיצוב; חץ = chevron-down (lucide) בצבע `#a3a3a3`, 16px, 10px מהקצה.
- **שדה חיפוש:** אייקון זכוכית מגדלת (stroke `#999`, 16px) בצד ההתחלה, `padding-inline-start: 36px`.
- **שדה עם אייקון בתוכו (למשל מחולל סיסמה):** כפתור 24×24 צמוד לקצה הסוף (4px), שקוף, צבע muted, ריחוף רקע accent, רדיוס 6px.
- **טלפון:** דגל + קידומת בתוך אותו שדה בצד ההתחלה, המספר LTR.
- **checkbox/radio:** `accent-color: var(--primary)`, 16×16.

### 9.1 מתג (Switch) - במקום כל checkbox של כן/לא
```css
.switch {
  appearance: none; position: relative; flex: none;
  width: 36px; height: 20px; margin: 0; border-radius: 999px;
  background: var(--input); cursor: pointer; transition: background-color .15s;
}
.switch::before {
  content: ""; position: absolute; top: 2px; inset-inline-start: 2px;
  width: 16px; height: 16px; border-radius: 50%;
  background: #fff; box-shadow: 0 1px 2px rgba(0,0,0,.3);
  transition: inset-inline-start .15s;
}
.switch:checked { background: var(--primary); }
.switch:checked::before { inset-inline-start: calc(100% - 18px); }
.switch:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
```
שורת מתג: טקסט (כותרת 500 + תיאור muted 13px) בצד ההתחלה, המתג בסוף, padding `14px 24px`, קו 1px בין שורות.

### 9.2 שורת שמירה צפה (Save bar)
מופיעה **רק** אחרי שינוי בטופס, נעלמת בביטול.
```css
.savebar {
  position: sticky; bottom: 16px; z-index: 5;
  display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;
  padding: 10px 12px 10px 16px;
  background: var(--popover); border: 1px solid var(--border); border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,.25);
}
.savebar-text { font-size: 14px; color: var(--muted-foreground); }   /* "יש שינויים שלא נשמרו" */
.savebar-actions { display: flex; gap: 8px; }                         /* ביטול (משני) + שמירה (ראשי) */
```

### 9.3 בורר בסגנון Supabase (select-button)
`height: 32px; min-width: 224px; padding: 0 10px; border: 1px solid var(--input); border-radius: 8px; background: transparent; font-size: 13px;` חץ chevrons-up-down בצבע muted. ריחוף/פתוח: מסגרת בצבע muted-foreground + רקע accent. התפריט מתחת ב-4px, רדיוס 6px (כמו כל תפריט נפתח).

---

## 10. טבלאות

```css
.table { width: 100%; font-size: 14px; color: var(--foreground); }
.table thead th {
  padding: 10px 16px; font-size: 13px; font-weight: 500; color: var(--muted-foreground);
  white-space: nowrap; background: transparent; border-bottom: 1px solid var(--border);
}   /* בבהיר: רקע ראש #fafafa */
.table tbody td { padding: 12px 16px; border-top: 1px solid var(--border); vertical-align: middle; }
.table tbody tr { cursor: pointer; }   /* כל השורה לחיצה */
.table tbody tr:hover > td { background: color-mix(in oklch, var(--foreground) 5%, transparent); transition: background-color .12s; }
.table td strong { font-weight: 600; }
.table td small  { display: block; font-size: 12px; color: var(--muted-foreground); }
```
- **מיון:** אין אייקון במנוחה. בריחוף על כותרת: רקע `foreground 4%` סביב התווית (padding `4px 8px`, רדיוס 4.8px) + חץ chevron 16px ב-60%. עמודה ממוינת: החץ קבוע ב-100%.
- **סרגל כלים מעל הטבלה:** גריד 3 עמודות, חיפוש באמצע (עד 352px), אייקון סינון (`sliders-horizontal`, 36×36, צבע muted) בקצה. כשיש סינון פעיל: האייקון כחול + נקודה כחולה 8px בפינה עם טבעת בצבע הכרטיס.
- **עימוד:** כפתורים 32×32 (קודם/הבא 36×36 עם chevron בלבד, בלי מסגרת), רדיוס 4.8px, דף פעיל בבהיר: רקע foreground וטקסט background.
- **בטלפון:** עמודות משניות מוסתרות, או כל שורה הופכת לכרטיס קומפקטי (גריד), בלי גלילה אופקית.

---

## 11. תגים, התראות, הודעות

### 11.1 תג (Badge / Status)
```css
.badge {
  display: inline-flex; align-items: center; height: 20px; padding: 0 8px;
  border-radius: 999px; font-size: 12px; font-weight: 500; line-height: 1; white-space: nowrap;
  background: var(--secondary); color: var(--foreground); border: 1px solid transparent;
}
```
צבעים לפי 1.4. דוגמה - "פעיל": רקע `oklch(0.76 0.14 155 / .16)`, טקסט `oklch(0.76 0.14 155)`.

### 11.2 כרטיסי מצב (Alert) - סגנון Supabase
**מסגרת מלאה בגוון + רקע מוכהה באותו גוון + טקסט רגיל.** לעולם לא פס צבעוני בצד.
```css
.alert { padding: 12px 16px; border-radius: 6px; font-size: 14px; border: 1px solid var(--border); background: var(--card); color: var(--foreground); }
.alert-info    { border-color: color-mix(in oklch, var(--info) 40%, transparent);        background: color-mix(in oklch, var(--info) 10%, var(--card)); }
.alert-success { border-color: color-mix(in oklch, var(--success) 40%, transparent);     background: color-mix(in oklch, var(--success) 10%, var(--card)); }
.alert-warning { border-color: color-mix(in oklch, var(--warning) 45%, transparent);     background: color-mix(in oklch, var(--warning) 12%, var(--card)); }
.alert-danger  { border-color: color-mix(in oklch, var(--destructive) 40%, transparent); background: color-mix(in oklch, var(--destructive) 10%, var(--card)); }
.alert a { color: inherit; text-decoration: underline; }
```
הודעה דחופה (למשל "יש תשלום שממתין"): אותו סגנון אדום, אייקון אדום 18px בהתחלה, טקסט מודגש + משני, כפתור פעולה אדום מלא בסוף.

### 11.3 Tooltip
רקע `--foreground`, טקסט `--background`, 12px, רדיוס 4.8px.

### 11.4 Progress
מסילה `var(--muted)`, רדיוס 999px; מד סיסמה: גובה 4px, רדיוס 2px.

### 11.5 טאבים
קו תחתון 2px בצבע primary לטאב פעיל, טאבים לא פעילים בצבע muted, ריחוף foreground, בלי רקע.

---

## 12. אייקונים

- **ספרייה ראשית: [lucide-animated](https://lucide-animated.com)** (Lucide עם אנימציה בריחוף, מבוסס motion/React). אם אין אפשרות להנפשה - **Lucide** רגיל, באותם שמות.
- **ספרייה משנית: Heroicons (Outline)** - לאייקונים שאין להם מקבילה (והחלפת Font Awesome).
- **אסור Font Awesome** כמראה סופי, אסור אייקונים ממולאים, אסור אימוג'י.
- עובי קו: `stroke-width: 1.85` לאייקוני ממשק, `1.5` לחצים בפינות כרטיסים. `stroke-linecap/linejoin: round`. צבע `currentColor`.
- גדלים: 16px רגיל (טופבר, כותרות כרטיס, כפתורים), 18px בתפריט הצד, 20px באייקון סינון, 18px בתוך עיגול 40px.
- **אייקונים מתהפכים ב-RTL:** כל חץ, chevron, arrow-up-right, reply, share, login/logout, sidebar toggle (`transform: scaleX(-1)`).
- אין טקסט/אייקון "מהבהב" לפני טעינה: האייקונים מוסתרים עד שה-JS מחליף אותם (עד 4 שניות מקסימום).

**מפת אייקונים בשימוש:**

| תפקיד | lucide |
|---|---|
| ראשי | `home` |
| מוצרים / שירותים | `server` (בתפריט), `box` |
| דומיינים / שפה | `earth` |
| חשבוניות / תשלום | `credit-card` |
| תמיכה / פניות | `circle-help`, `message-square`, `ticket` |
| משתמשים | `users`, `user`, `user-plus` |
| עגלה / חנות | `cart` |
| התראות | `bell` |
| מצב בהיר/כהה | `sun` / `moon` |
| פרויקטים | `layout-grid` |
| כיווץ תפריט | `panel-left-open` |
| המבורגר | `menu` (אנימציה: מסתובב 45° והופך ל-X ב-500ms) |
| סינון | `sliders-horizontal` |
| בורר | `chevrons-up-down`, `chevron-down` |
| נבחר | `check` |
| סגירה | `x` |
| אבטחה | `shield-check` |
| הגדרות | `settings` |
| התנתקות | `logout` |
| מטבע | `circle-dollar-sign` |
| דואר | `mail-check` |
| חץ פינה | Heroicons `arrow-up-right` (stroke 1.5) |

---

## 13. תנועה ואנימציה

| מה | ערך |
|---|---|
| ריחוף צבע/רקע | `.12s`-`.15s` |
| כפתור ראשי | `.2s cubic-bezier(.22,1,.36,1)` |
| פתיחת תפריט נפתח | `.12s ease-out`, מ-`translateY(4px) scale(.98)` |
| כיווץ תפריט צד | `.5s cubic-bezier(.45,0,.2,1)` |
| פתיחת אזור מתקפל | `grid-template-rows: 0fr → 1fr` ב-`.5s cubic-bezier(.2,.8,.2,1)` + opacity `.35s` |
| כרטיסים שנכנסים בדירוג | `translateY(20px) → 0`, השהיה 80ms בין כרטיס לכרטיס |
| החלפת מצב כהה/בהיר | אייקון: `.33s` scale+rotate |
| מעבר בין עמודים | cross-fade `.12s` (`@view-transition { navigation: auto }`) |

תמיד לכבד `prefers-reduced-motion: reduce` (לבטל מעברים).

---

## 14. עמודים מיוחדים

- **התחברות / הרשמה:** רקע `--muted`, כרטיס ממורכז ברוחב 384px (הרשמה ארוכה עד 896px), לוגו 48px ממורכז מעל, מתחתיו אייקון שפה/מצב כהה בלבד. כותרת 24px, תיאור muted 14px, תוויות ושדות ממורכזים, כפתור ראשי ברוחב מלא, קישור "הרשמה" כטקסט עם קו תחתון (offset 3px).
- **מסמכים להדפסה (חשבונית, קבלה, הצעת מחיר, דוח):** **תמיד בהירות כמו נייר**, גם כשהאתר כהה. רקע `oklch(96.14% .0028 84.31)`, מסמך לבן ברדיוס 12px עם קו `0 0 0 1px #0000001a`, padding 40px. בהדפסה: רקע לבן בלי צל.
- **עמוד "הפעולה הושלמה" (הזמנה, הרשמה, שליחה):** כרטיס ממורכז 544px, עיגול ירוק 56px (`rgba(34,197,94,.14)` רקע, `#22c55e` אייקון), מספר אסמכתא 28px tabular-nums בתוך קופסה בצבע הדף עם מסגרת input, כפתור העתקה שקוף 28px.
- **טופס ארוך עם סיכום (קופה, הזמנה, אשף):** פרטים 2/3 בצד ההתחלה, סיכום 1/3 בצד הסוף, sticky. כל קבוצת שדות בכרטיס 12px עם כותרת 14px/600 וקו מתחתיה לכל רוחב הכרטיס. מתחת ל-992px: עמודה אחת, הסיכום ראשון.

---

## 15. מצב כהה/בהיר - מימוש

```html
<script>/* בראש ה-head, לפני CSS, כדי שלא יהבהב */
(function(){var m='system';try{m=localStorage.getItem('theme')||'system'}catch(e){}
var d=m==='dark'||(m==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);
document.documentElement.classList.toggle('dark',d);})();
</script>
```
טוקנים ב-`:root` (בהיר) וב-`.dark` (כהה). אין שום צבע קשיח ברכיבים - רק משתנים.

---

## 16. בדיקה לפני מסירה (Checklist)

לכל עמוד, במצב **כהה**, **בהיר** ו**מובייל 390px**:
- [ ] גופן Noto Sans בכל מקום.
- [ ] שדות 32px, רדיוס 8px, רקע = רקע הדף, מסגרת 1px.
- [ ] כפתורים 28px, 13px/500, רדיוס 8px. כפתור מלא ליד שדה = 30px.
- [ ] כרטיסים 12px, בלי border, hairline + shadow-xs.
- [ ] רווח בין כרטיסים = 24px (16px במובייל), זהה בכל הכיוונים ובשולי העמוד.
- [ ] אף אייקון/כפתור אייקון עם מסגרת, ואין טבעת אחרי לחיצת עכבר (רק במקלדת).
- [ ] אין כחול בריחוף/הדגשה/פריט פעיל.
- [ ] אין פס צבעוני בצד כרטיס, אין גרדיאנטים על כרטיסים.
- [ ] RTL: חצים מתהפכים, מחירים ואימיילים LTR.
- [ ] אין גלילה אופקית בטלפון.

---

## 17. נספח: קובץ טוקנים מוכן להעתקה

```css
:root {
  --background:#fafafa; --foreground:#171717; --card:#fff; --card-foreground:#171717;
  --popover:#fff; --popover-foreground:#171717;
  --primary:#2080e8; --primary-hover:#278cfa; --primary-foreground:#fff;
  --secondary:#f6f6f6; --muted:#f9f9f9; --muted-foreground:#6b6b6b;
  --accent:#f0f0f0; --border:#e6e6e6; --hairline:#e6e6e6; --input:#dedede; --ring:#2080e8; --plan-line:#e6e6e6;
  --sidebar:#fafafa; --nav-fg:color-mix(in oklch,#171717 68%,transparent); --nav-hover:#f0f0f0; --nav-active:#f0f0f0;
  --destructive:oklch(55% .2 25.33); --warning:oklch(66.6% .15 58.32); --success:oklch(56% .13 155); --info:#2080e8;
  --shadow-xs:0 1px 2px 0 #1a1f2c0a,0 0 0 1px #1a1f2c05;
  --shadow-md:0 1px 2px 0 #1a1f2c0d,0 4px 12px -4px #1a1f2c14;
  --shadow-lg:0 2px 4px 0 #1a1f2c0d,0 12px 28px -8px #1a1f2c1f;
  --btn-finish:0 1px 3px 0 rgb(0 0 0/.04),inset 0 1px 0 0 rgb(0 0 0/.024),inset 0 0 0 1px rgb(0 0 0/.036),inset 0 -1px 0 0 rgb(0 0 0/.036),inset 0 0 0 1px rgb(0 0 0/.06);
  --radius-card:12px; --radius-control:8px; --radius-popover:6px; --radius-item:4.8px;
  --card-gap:1.5rem; --sidebar-width:212px; --panel-width:192px; --rail-width:54px; --topbar-height:56px;
  --font-sans:"Noto Sans","Noto Sans Hebrew",ui-sans-serif,sans-serif,system-ui;
  --font-mono:"JetBrains Mono",ui-monospace,monospace;
  color-scheme:light;
}
.dark {
  --background:#0a0a0a; --foreground:#ededed; --card:#131313; --card-foreground:#ededed;
  --popover:#171717; --popover-foreground:#ededed;
  --primary:#3d92f0; --primary-hover:#449eff; --primary-foreground:#fff;
  --secondary:#1c1c1c; --muted:#101010; --muted-foreground:#a3a3a3;
  --accent:color-mix(in oklch,#ededed 8%,transparent);
  --border:#232323; --hairline:#232323; --input:#2e2e2e; --ring:#3d92f0; --plan-line:#2e2e2e;
  --sidebar:#0a0a0a; --nav-fg:color-mix(in oklch,#ededed 68%,transparent);
  --nav-hover:color-mix(in oklch,#ededed 6%,transparent); --nav-active:color-mix(in oklch,#ededed 10%,transparent);
  --destructive:oklch(72% .15 25.33); --warning:oklch(82.8% .15 84.43); --success:oklch(76% .14 155); --info:#3d92f0;
  --shadow-xs:0 1px 3px 0 #0000000d;
  --shadow-md:0 1px 3px 0 #0000001a,0 2px 4px -1px #0000001a;
  --shadow-lg:0 1px 3px 0 #0000001a,0 4px 6px -1px #0000001a;
  --btn-finish:0 1px 3px 0 rgb(0 0 0/.2),inset 0 1px 0 0 rgb(255 255 255/.04),inset 0 0 0 1px rgb(255 255 255/.06),inset 0 0 0 1px rgb(255 255 255/.1);
  color-scheme:dark;
}
@media (max-width:991.98px){ :root{ --card-gap:1rem; } }
body { font-family:var(--font-sans); font-size:15px; line-height:1.5; background:var(--background); color:var(--foreground); -webkit-font-smoothing:antialiased; }
```

---

---

## 18. דפוסי עמודים נפוצים

### 18.1 הבדל בין כהה לבהיר בכרטיסים
- בכהה: כל כרטיס = hairline `#232323` + shadow-xs.
- בבהיר: hairline `#e6e6e6` + shadow-xs הבהיר. לשמור על אחידות - hairline לכל הכרטיסים.
- עיגול האייקון בבהיר: `#171717` ב-6% שקיפות.

### 18.2 דף הבית / לוח בקרה
- שורת כרטיסי סטטיסטיקה (7.2) למעלה, ומתחתיה כרטיסי סיכום (7.1) בגריד של 2 עמודות במחשב, עמודה אחת מתחת ל-992px.
- כרטיס סיכום שמוביל לעמוד מלא - כפתור החץ הכחול בפינה (7.3).
- **שורת פריט ברשימה בתוך כרטיס:** תגית סטטוס בצד ההתחלה, שם הפריט 14px, וכפתור chevron שקוף 28×28 בצד הסוף (בלי רקע ובלי מסגרת, ריחוף אפור 8%). ה-chevron מצביע קדימה (ימינה ב-LTR, שמאלה ב-RTL). padding `10px 20px`, קו הפרדה 1px.

### 18.3 עמוד רשימה (טבלה)
- כותרת עמוד 22px/600, ובקצה הסוף של אותה שורה כפתורי הפעולה של העמוד (`.page-actions`: gap 8px, משני ואז ראשי, למשל "ייצוא" + "הוספה").
- קופסת טבלה (7.6) עם סרגל כלים:
  - בפינה אחת: אייקון זכוכית מגדלת 32×32 שנפתח לשדה חיפוש (רוחב עד 256px, מעבר `.25s`). כשהחיפוש הוא הפעולה העיקרית - שדה פתוח תמיד וממורכז, עם אייקון בתוכו.
  - בפינה השנייה: אייקון סינון 36×36 בצבע muted.
- עמודות: פריט ראשי מודגש עם שורת משנה muted 12px, ערכים, סטטוס (גלולה), ופעולות בקצה הסוף (כפתורים 28px, gap 8px).
- טבלה שיש בה כפתורים בכל שורה - **בלי** ריחוף על השורה. טבלה שהשורה כולה לחיצה - עם ריחוף (סעיף 10).
- מצב ריק: "לא נמצאו רשומות" ממורכז, 13px muted.
- למטה: חיצי עימוד (chevron בלבד, 36×36, בלי מסגרת, מושבת = 40% שקיפות) ו-select של מספר שורות (32×32, טקסט ממורכז, בלי חץ).

### 18.4 כרטיסי פעולה בשורה
- 2-3 כרטיסים בשורה, גובה שווה, כותרת 16px/600, תיאור muted 13px, תוויות 13px/500, שדות 32px, וכפתור **ברוחב מלא בתחתית** הכרטיס (`margin-top: auto`). כפתור בכרטיס שאין בו מה לעשות כרגע = משני.

### 18.5 חיפוש מרכזי + טבלת מחירים / השוואה
- תיבת חיפוש ממורכזת, רוחב עד 640px: גובה 44px, רקע `--card`, רדיוס 12px, padding 4px, מסגרת 1px; בפוקוס מסגרת בצבע הראשי. בתוכה שדה שקוף 16px וכפתור ראשי ריבועי 36×36 עם זכוכית מגדלת 18px, רדיוס 6px, צמוד לקצה.
- טבלה בלי קופסה: שורות 44px, תאים `padding: 8px 20px`, 16px; כותרות 14px/600.
- **עמודה מודגשת:** רקע `color-mix(in srgb, var(--primary) 10%, transparent)` לכל גובה העמודה, הערכים בה בצבע הראשי 17px/600.
- תגית הערה קטנה ליד ערך ("מבצע", "ל-2 שנים"): רקע warning ב-18%, טקסט warning, 12px, **רדיוס 4.8px** (לא גלולה).
- ערך חסר = טקסט muted.

### 18.6 עמוד קטלוג / מסלולים
- סעיפים עם כותרת 18px/500 מעל ובלי קווי הפרדה, רווח כרטיס ביניהם.
- מסלולים = כרטיסי תוכנית (7.4), כפתור ראשי ברוחב מלא בתחתית.
- שירות/תוסף = כרטיס שורה: עיגול אייקון 40px, שם 14px/500 + תיאור muted 13px, מחיר 24px/600, כפתור משני ("מה כלול") + ראשי ("הוספה").

### 18.7 מצב ריק (עמוד שלם)
- כותרת עמוד 22px, כרטיס ברוחב מלא עם הודעה ממורכזת ("אין עדיין פריטים") וכפתור ראשי לפעולה הבאה מתחתיה (gap 16px, padding 40px 16px).

### 18.8 עמוד משתמשים
- כרטיס רשימה: כל משתמש בשורה `padding: 14px 24px` - עיגול 32px עם ראשי תיבות (11px/600, רקע accent), אימייל, תגית תפקיד ("בעלים", 11px, מסגרת 1px border, רקע accent, גלולה), אייקון מגן קטן אם יש אימות דו-שלבי, ומתחת "כניסה אחרונה" muted 13px. בצד הסוף טקסט ההרשאה muted.
- מתחת: סעיף "הזמנת משתמש" בשורות הגדרות (7.5) וכפתור ראשי בשורה התחתונה.

### 18.9 עמוד טופס / הגדרות / פרופיל
- כותרת עליונה, ואחריה סעיפים בסגנון 7.5 (כותרת מעל, כרטיס עם שורה לכל הגדרה).
- בורר בסגנון Supabase (9.3) כשבוחרים איזה פריט עורכים.
- שדה טלפון: דגל + קידומת בתוך השדה, המספר LTR.
- שדה סיסמה: כפתור מחולל/הצגה בתוך השדה, פס חוזק 4px מתחת וטיפים 12px muted.
- textarea ברוחב מלא בשורה נפרדת.
- שמירה: או שורת שמירה צפה (9.2), או כפתורים בשורה התחתונה של הסעיף (ראשי "שמירת שינויים" + משני "ביטול"). **לפני שינוי - הכפתור הראשי מושבת (50% שקיפות).**

### 18.10 הודעת מצב ברוחב מלא
- כשאפשרות כבויה / יש בעיה: כרטיס alert (11.2) ברוחב מלא, טקסט ממורכז 14px.

### 18.11 עמוד 404
- ממורכז: אייקון סימן קריאה בעיגול בקו (כ-80px, צבע foreground, לא בצבע הראשי), "אופס!" 22px/600, כותרת משנה 16px/600, הסבר 14px, ושני כפתורים ("דף הבית", "יצירת קשר") עם gap 8px.

### 18.12 מאמרים / בסיס ידע
- שדה חיפוש ברוחב מלא (32px, אייקון בהתחלה), מתחתיו גריד של 3 כרטיסי מאמר (2 ב-768px, 1 בטלפון).
- כרטיס מאמר: כרטיס 12px בלי padding, תמונה 16:9 עם 8px מרווח מכל צד, כותרת 21px/900 (שתי שורות), תקציר 15px muted עם line-height 28px וחיתוך לשתי שורות, ובתחתית זמן קריאה muted + קישור בצבע הראשי "לקריאה" עם חץ.
- כפתורי שיתוף בלי מסגרת.

### 18.13 תפריטי הטופבר
- תפריט שפה: רוחב לפי התוכן (~125px), רקע popover, רדיוס 6px, outline 1px hairline, צל shadow-lg; פריט 33px, padding `6px 12px 6px 8px`, gap 10px: דגל, שם, וי בקצה.
- כשתפריט פתוח, הכפתור שלו בטופבר מקבל את הרקע האפור של ריחוף.
- תפריט התראות: כותרת 12px/500 muted, ריק: "אין התראות כרגע" 14px muted.

---

## 19. מה אסור (סיכום)

- גרדיאנטים על כרטיסים או רקעים, גרדיאנט סגול-כחול, זכוכית/blur דקורטיבי, הילות, כתמים מטושטשים.
- פס צבעוני בצד או בראש כרטיס/התראה/כותרת.
- צללים כבדים או צבעוניים (למשל "זוהר" כחול סביב כפתור).
- פינות מוגזמות (מעל 12px), כפתורים בצורת גלולה (`rounded-full`), `hover:scale` על כפתורים.
- שדות גבוהים מ-32px או ברדיוס 10px+ (חוץ מ-iOS מתחת ל-992px - 16px גופן).
- צבע ראשי בריחוף, בפריט פעיל או ברקע.
- אייקון בתוך ריבוע צבעוני פסטל, אימוג'י כאייקונים, אייקונים ממולאים, Font Awesome.
- גופן נוסף מעבר ל-Noto Sans / Noto Sans Hebrew / JetBrains Mono.
- אנימציית כניסה לכל דבר. תנועה רק לפי סעיף 13.
