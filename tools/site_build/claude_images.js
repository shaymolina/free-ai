// יוצר תמונות ממשק של Claude לדף הבית (מוקאפים בעברית)
// הרצה: NODE_PATH=$(npm root -g) node tools/site_build/claude_images.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const OUT = path.join(ROOT, 'site/assets/images/claude');
fs.mkdirSync(OUT, { recursive: true });
const FONTS = 'file://' + path.join(ROOT, 'site/assets/fonts/fonts.css');

const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%}
body{font-family:'Urbanist',sans-serif;color:#1F1E1D;direction:rtl;overflow:hidden;
 background:radial-gradient(60% 80% at 85% 10%,#F2C7B3 0%,rgba(242,199,179,0) 60%),
 radial-gradient(50% 70% at 10% 95%,#E8D9C6 0%,rgba(232,217,198,0) 70%),#F4EFE7;
 display:flex;align-items:center;justify-content:center}
.win{background:#FAF9F5;border-radius:22px;box-shadow:0 40px 80px -30px rgba(80,50,30,.35),0 0 0 1px rgba(0,0,0,.06);overflow:hidden;display:flex;flex-direction:column}
.bar{height:46px;display:flex;align-items:center;gap:8px;padding:0 18px;border-bottom:1px solid #ECE8E0;background:#F5F3EE;direction:ltr}
.bar i{width:12px;height:12px;border-radius:50%;background:#E3DED5;display:block}
.bar span{margin-left:auto;margin-right:auto;font-size:15px;color:#8A8580;font-weight:600}
.spark{color:#D97757;font-weight:700}
.muted{color:#8A8580}
.user{align-self:flex-start;background:#EFEBE3;border-radius:18px;padding:14px 18px;max-width:78%;font-size:19px;line-height:1.5}
.ai{font-size:19px;line-height:1.6;max-width:92%}
.ai b{font-weight:700}
.input{border:1px solid #E3DED5;background:#fff;border-radius:18px;padding:18px 20px;font-size:18px;color:#8A8580;display:flex;justify-content:space-between;align-items:center}
.send{width:36px;height:36px;border-radius:10px;background:#D97757;color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px}
.chat{flex:1;padding:28px 34px;display:flex;flex-direction:column;gap:20px}
.file{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #ECE8E0;border-radius:12px;padding:12px 14px;font-size:16px;font-weight:600}
.ficon{width:30px;height:36px;border-radius:6px;background:#F3E3DA;color:#B85C3E;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;direction:ltr}
.term{background:#1C1B19;color:#E9E5DD;font-family:ui-monospace,Menlo,monospace}
.term .bar{background:#262522;border-color:#33312D}
.term .bar i{background:#45423D}
.term .bar span{color:#8F8A82}
.tl{font-size:19px;line-height:1.9;font-family:'Urbanist',ui-monospace,monospace}
.ok{color:#7DC08A}.warn{color:#E8B45A}.bad{color:#E26D5A}
`;

const page = (w, h, body) => `<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<link rel="stylesheet" href="${FONTS}"><style>${CSS}</style></head><body style="width:${w}px;height:${h}px">${body}</body></html>`;

const win = (w, h, title, inner, cls = '') =>
  `<div class="win ${cls}" style="width:${w}px;height:${h}px"><div class="bar"><i></i><i></i><i></i><span>${title}</span></div>${inner}</div>`;

// ---------- מסלול Claude (832x480) ----------
const S = {
  'claude-start': win(640, 380, 'Claude', `
    <div class="chat" style="justify-content:center;align-items:center;gap:26px">
      <div style="font-size:34px;font-weight:600"><span class="spark">✻</span> ערב טוב. במה נתחיל?</div>
      <div class="input" style="width:100%"><span>תשאלו כל דבר…</span><span class="send">↑</span></div>
    </div>`),
  'claude-prompt': win(660, 400, 'Claude', `
    <div class="chat" style="gap:16px;padding:24px 30px">
      <div class="user" style="font-size:16px"><b>תפקיד:</b> יועץ שיווק<br><b>משימה:</b> 3 כותרות לדף נחיתה של סטודיו לפילאטיס<br><b>סגנון:</b> קצר, חם, בלי סימני קריאה</div>
      <div class="ai" style="font-size:16px"><span class="spark">✻</span> הנה שלוש אפשרויות:<br>1. הגוף שלך יודה לך מחר בבוקר<br>2. חזקה יותר, גמישה יותר, רגועה יותר<br>3. 50 דקות שהן רק שלך</div>
    </div>`),
  'claude-projects': win(680, 400, 'Claude · פרויקט: העסק שלי', `
    <div style="display:flex;flex:1">
      <div style="width:250px;border-left:1px solid #ECE8E0;padding:20px;display:flex;flex-direction:column;gap:10px;background:#F7F5F0">
        <div class="muted" style="font-size:14px;font-weight:600">ידע בפרויקט</div>
        <div class="file"><span class="ficon">PDF</span>מחירון 2026</div>
        <div class="file"><span class="ficon">DOC</span>שאלות של לקוחות</div>
        <div class="file"><span class="ficon">TXT</span>טון הכתיבה שלי</div>
      </div>
      <div class="chat" style="padding:22px 24px;gap:16px">
        <div class="user" style="font-size:16px">כמה עולה חבילת זוגות?</div>
        <div class="ai" style="font-size:16px"><span class="spark">✻</span> לפי המחירון: <b>₪1,200</b> לחבילת זוגות, 8 מפגשים. רוצה שאנסח תשובה ללקוחה?</div>
      </div>
    </div>`),
  'claude-artifacts': win(700, 410, 'Claude · Artifact', `
    <div style="display:flex;flex:1">
      <div class="chat" style="flex:0 0 250px;padding:22px 20px;border-left:1px solid #ECE8E0;gap:14px">
        <div class="user" style="font-size:15px;max-width:100%">תבנה לי גרף של ההכנסות לפי חודש</div>
        <div class="ai" style="font-size:15px"><span class="spark">✻</span> הנה הגרף. החודש החזק ביותר: יוני.</div>
      </div>
      <div style="flex:1;padding:24px;background:#fff">
        <div style="font-size:18px;font-weight:700;margin-bottom:6px">הכנסות לפי חודש</div>
        <div class="muted" style="font-size:13px;margin-bottom:18px">ינואר – יוני 2026</div>
        <div style="display:flex;align-items:flex-end;gap:16px;height:210px;direction:ltr;border-bottom:1px solid #ECE8E0">
          ${[46, 58, 52, 70, 64, 92].map((v, i) => `<div style="flex:1;height:${v}%;border-radius:8px 8px 0 0;background:${i === 5 ? '#D97757' : '#EBC9B8'}"></div>`).join('')}
        </div>
      </div>
    </div>`),
  'claude-code': win(660, 390, 'Claude Code', `
    <div style="padding:24px 30px" class="tl">
      <div><span class="spark">✻</span> מה נבנה היום?</div>
      <div style="color:#fff">› תבדוק את האתר שלי ותתקן מה שצריך</div>
      <div class="muted">● מפעיל סקיל: בדיקת אבטחה</div>
      <div class="ok">✓ 31 בדיקות עברו</div>
      <div class="warn">! 2 המלצות לשיפור</div>
      <div class="ok">✓ תוקן ועלה לאוויר</div>
    </div>`, 'term'),
};

// ---------- מה תבנו (1908x990) ----------
const site = `
  <div style="flex:1;background:#fff;display:flex;flex-direction:column">
    <div style="display:flex;justify-content:space-between;align-items:center;padding:22px 44px;border-bottom:1px solid #F0ECE5">
      <div style="font-size:26px;font-weight:700">מאפיית <span class="spark">שקד</span></div>
      <div style="display:flex;gap:30px;font-size:18px" class="muted"><span>תפריט</span><span>הזמנות</span><span>צרו קשר</span></div>
    </div>
    <div style="flex:1;display:flex;align-items:center;padding:0 60px;gap:50px;background:linear-gradient(180deg,#FBF7F1,#fff)">
      <div style="flex:1">
        <div style="font-size:64px;font-weight:700;line-height:1.1">לחם טרי<br>כל בוקר מ-6:00</div>
        <div class="muted" style="font-size:22px;margin:20px 0 30px">מאפים בעבודת יד, משלוח עד הבית בכל העיר.</div>
        <span style="background:#1F1E1D;color:#fff;border-radius:40px;padding:16px 34px;font-size:20px;font-weight:600">להזמנה</span>
      </div>
      <div style="flex:0 0 420px;height:360px;border-radius:28px;background:radial-gradient(circle at 40% 40%,#F3D2A8,#D99A5B 60%,#B5713A)"></div>
    </div>
  </div>`;

const F = {
  'build-site': `<div style="position:relative;width:1500px;height:800px">
      ${win(1300, 760, 'shaked-bakery.co.il', site)}
      <div style="position:absolute;left:-40px;bottom:-20px">${win(560, 300, 'Claude Code', `
        <div style="padding:22px 28px" class="tl">
          <div style="color:#fff">› תעלה את האתר לאוויר</div>
          <div class="muted">● בונה ומעלה…</div>
          <div class="ok">✓ האתר באוויר</div>
          <div class="ok" style="direction:ltr;text-align:right">shaked-bakery.co.il</div>
        </div>`, 'term')}</div>
    </div>`,
  'security-skill': win(1300, 780, 'דוח בדיקת אבטחה', `
    <div style="padding:40px 50px;flex:1;display:flex;flex-direction:column;gap:28px;background:#fff">
      <div style="display:flex;justify-content:space-between;align-items:end">
        <div><div style="font-size:40px;font-weight:700">בדיקת אבטחה לאתר</div><div class="muted" style="font-size:20px;margin-top:6px">34 בדיקות · נוצר עם סקיל ל-Claude</div></div>
        <div style="font-size:72px;font-weight:700" class="spark">88<span style="font-size:30px" class="muted">/100</span></div>
      </div>
      <div style="display:flex;gap:20px">
        ${[['#E7F4EA', '#2F8A47', '31', 'תקין'], ['#FBF0DC', '#B07A1C', '2', 'לשיפור'], ['#FBE3DF', '#C0432F', '1', 'דחוף']].map(([b, c, n, t]) => `<div style="flex:1;background:${b};border-radius:18px;padding:24px 28px"><div style="font-size:48px;font-weight:700;color:${c}">${n}</div><div style="font-size:20px;font-weight:600;color:${c}">${t}</div></div>`).join('')}
      </div>
      ${[['bad', '✗', 'טופס יצירת הקשר לא מוגן מספאם'], ['warn', '!', 'חסרה כותרת אבטחה בשרת'], ['ok', '✓', 'החיבור מוצפן (HTTPS)']].map(([c, s, t]) => `<div style="display:flex;gap:16px;align-items:center;font-size:22px;border-bottom:1px solid #F0ECE5;padding-bottom:16px"><span class="${c}" style="font-weight:700;font-size:26px;width:26px">${s}</span>${t}</div>`).join('')}
    </div>`),
  'projects-assistant': win(1300, 780, 'Claude · פרויקט: הסטודיו', `
    <div style="display:flex;flex:1">
      <div style="width:380px;border-left:1px solid #ECE8E0;padding:30px;display:flex;flex-direction:column;gap:14px;background:#F7F5F0">
        <div class="muted" style="font-size:18px;font-weight:600">הוראות</div>
        <div style="font-size:18px;line-height:1.6;background:#fff;border:1px solid #ECE8E0;border-radius:12px;padding:16px">עונים ללקוחות בנימוס, קצר, ורק לפי הקבצים.</div>
        <div class="muted" style="font-size:18px;font-weight:600;margin-top:10px">קבצים</div>
        <div class="file" style="font-size:18px"><span class="ficon">PDF</span>מחירון 2026</div>
        <div class="file" style="font-size:18px"><span class="ficon">DOC</span>מערכת שעות</div>
        <div class="file" style="font-size:18px"><span class="ficon">TXT</span>מדיניות ביטולים</div>
      </div>
      <div class="chat" style="padding:40px 50px;gap:26px">
        <div class="user" style="font-size:24px">אפשר לבטל שיעור ביום של השיעור?</div>
        <div class="ai" style="font-size:24px"><span class="spark">✻</span> לפי מדיניות הביטולים, ביטול עד <b>12 שעות</b> לפני השיעור הוא בלי חיוב. אחרי זה השיעור נספר. רוצה שאשלח לה את השעות הפנויות השבוע?</div>
        <div class="user" style="font-size:24px">כן, תשלח</div>
        <div style="flex:1"></div>
        <div class="input" style="font-size:22px"><span>תשאלו על העסק…</span><span class="send">↑</span></div>
      </div>
    </div>`),
  'artifact-tool': `<div style="display:flex;gap:40px;align-items:center">
      ${win(520, 700, 'Claude', `<div class="chat" style="padding:30px;gap:22px">
        <div class="user" style="font-size:22px;max-width:100%">תבנה לי מחשבון הצעת מחיר לשיפוצים</div>
        <div class="ai" style="font-size:22px"><span class="spark">✻</span> בניתי מחשבון: בוחרים סוג עבודה ושטח, ומקבלים מחיר מיידי. אפשר לשתף אותו עם לקוחות בקישור.</div>
      </div>`)}
      ${win(780, 700, 'Artifact · מחשבון הצעת מחיר', `
        <div style="flex:1;background:#fff;padding:40px 46px;display:flex;flex-direction:column;gap:24px">
          <div style="font-size:36px;font-weight:700">הצעת מחיר לשיפוץ</div>
          <div><div class="muted" style="font-size:18px;margin-bottom:8px">סוג עבודה</div><div class="input" style="color:#1F1E1D;font-size:22px">צביעת דירה <span class="muted">▾</span></div></div>
          <div><div class="muted" style="font-size:18px;margin-bottom:8px">שטח (מ"ר)</div><div class="input" style="color:#1F1E1D;font-size:22px">85</div></div>
          <div style="background:#FBEDE6;border-radius:18px;padding:26px 30px;display:flex;justify-content:space-between;align-items:center;margin-top:auto">
            <span style="font-size:22px;font-weight:600">מחיר משוער</span><span style="font-size:48px;font-weight:700" class="spark">₪6,800</span>
          </div>
        </div>`)}
    </div>`,
};


// ---------- תמונות בעמודים הפנימיים (מחליפות את תמונות התבנית, באותו גודל) ----------
const lessonList = (cur) => ['מה זה Claude ואיך מתחילים', 'איך מבקשים נכון', 'פרויקטים וקבצים', 'Artifacts', 'סקילים', 'חיבור לכלים', 'Claude Code', 'מעלים לאוויר']
  .map((t, i) => `<div style="display:flex;gap:12px;align-items:center;padding:12px 14px;border-radius:12px;font-size:17px;${i === cur ? 'background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.06);font-weight:700' : ''}">
     <span style="width:24px;height:24px;border-radius:50%;flex:0 0 24px;display:flex;align-items:center;justify-content:center;font-size:13px;${i < cur ? 'background:#D97757;color:#fff' : i === cur ? 'border:2px solid #D97757' : 'border:2px solid #E3DED5'}">${i < cur ? '✓' : ''}</span>
     <span class="${i > cur ? 'muted' : ''}">${i + 1}. ${t}</span></div>`).join('');
const video = (label) => `<div style="flex:1;border-radius:18px;background:linear-gradient(135deg,#2A2622,#3B2F28 60%,#5A3B2C);position:relative;display:flex;align-items:center;justify-content:center">
     <div style="position:absolute;top:18px;right:22px;color:rgba(255,255,255,.7);font-size:16px">${label}</div>
     <div style="width:84px;height:84px;border-radius:50%;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;direction:ltr">▶</div>
     <div style="position:absolute;bottom:18px;left:22px;right:22px;height:5px;border-radius:5px;background:rgba(255,255,255,.2)"><div style="width:38%;height:100%;border-radius:5px;background:#D97757"></div></div></div>`;
const skillsSettings = (big) => win(big ? 1200 : 1100, big ? 760 : 720, 'Claude · הגדרות · סקילים', `
    <div style="display:flex;flex:1">
      <div style="width:260px;border-left:1px solid #ECE8E0;padding:26px;display:flex;flex-direction:column;gap:6px;background:#F7F5F0;font-size:18px">
        ${['פרופיל', 'יכולות', 'סקילים', 'חיבורים', 'פרטיות'].map(t => `<div style="padding:10px 14px;border-radius:10px;${t === 'סקילים' ? 'background:#fff;font-weight:700' : ''}" class="${t === 'סקילים' ? '' : 'muted'}">${t}</div>`).join('')}
      </div>
      <div style="flex:1;padding:36px 44px;display:flex;flex-direction:column;gap:20px;background:#fff">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div><div style="font-size:30px;font-weight:700">סקילים</div><div class="muted" style="font-size:17px;margin-top:4px">יכולות חדשות ש-Claude משתמש בהן כשצריך</div></div>
          <span style="background:#1F1E1D;color:#fff;border-radius:30px;padding:12px 24px;font-size:17px;font-weight:600">+ העלאת סקיל</span>
        </div>
        ${[['בדיקת אבטחה לאתר', '34 בדיקות · דוח בעברית', true], ['בדיקת מהירות לאתר', '69 בדיקות · פרומפט לכל תיקון', true], ['כתיבת פוסטים', 'בסגנון שלכם', false]].map(([t, d, on]) => `
        <div style="display:flex;align-items:center;gap:18px;border:1px solid #ECE8E0;border-radius:16px;padding:18px 22px">
          <span class="ficon" style="width:44px;height:44px;font-size:22px;border-radius:12px">✻</span>
          <div style="flex:1"><div style="font-size:20px;font-weight:700">${t}</div><div class="muted" style="font-size:16px">${d}</div></div>
          <span style="width:52px;height:30px;border-radius:30px;background:${on ? '#D97757' : '#E3DED5'};position:relative;direction:ltr"><span style="position:absolute;top:3px;${on ? 'right:3px' : 'left:3px'};width:24px;height:24px;border-radius:50%;background:#fff"></span></span>
        </div>`).join('')}
      </div>
    </div>`);

const P = {
  // עמוד הקורס – שיעור עם סרטון ורשימת שיעורים
  'section/service-single-1': [1914, 1092, `<div style="transform:scale(1.35)">${win(1300, 700, 'free-ai.co.il · Claude מאפס', `
    <div style="display:flex;flex:1;gap:24px;padding:24px;background:#F7F5F0">
      <div style="flex:1;display:flex;flex-direction:column;gap:16px">
        ${video('שיעור 3 · פרויקטים וקבצים')}
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div><div style="font-size:26px;font-weight:700">פרויקטים וקבצים</div><div class="muted" style="font-size:16px">מלמדים את Claude על העסק שלכם פעם אחת – והוא זוכר.</div></div>
          <span style="background:#1F1E1D;color:#fff;border-radius:30px;padding:12px 22px;font-size:16px;font-weight:600">סיימתי ✓</span>
        </div>
      </div>
      <div style="width:330px;background:#EFEBE3;border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:2px">
        <div style="font-size:18px;font-weight:700;padding:6px 14px 10px">Claude מאפס · 2/8</div>${lessonList(2)}
      </div>
    </div>`)}</div>`],
  // סיכום שיעור וקבצים להורדה
  'section/service-single-2': [1284, 807, `<div style="transform:scale(1.25)">${win(900, 560, 'free-ai.co.il · שיעור 3', `
    <div style="flex:1;background:#fff;padding:30px 36px;display:flex;gap:30px">
      <div style="flex:1;display:flex;flex-direction:column;gap:12px">
        <div style="font-size:24px;font-weight:700">סיכום השיעור</div>
        ${['פותחים פרויקט חדש ב-Claude', 'מעלים מחירון, שאלות נפוצות וטון כתיבה', 'כותבים הוראות קצרות לפרויקט', 'שואלים – ו-Claude עונה רק לפי הקבצים'].map((t, i) => `<div style="display:flex;gap:12px;font-size:17px;line-height:1.5"><span class="spark" style="font-weight:700">${i + 1}.</span>${t}</div>`).join('')}
      </div>
      <div style="width:290px;display:flex;flex-direction:column;gap:12px">
        <div style="font-size:20px;font-weight:700">קבצים להורדה</div>
        ${[['PDF', 'צ\'קליסט לפרויקט'], ['TXT', 'פרומפט הוראות מוכן'], ['DOC', 'תבנית שאלות לקוחות']].map(([e, t]) => `<div class="file"><span class="ficon">${e}</span><span style="flex:1">${t}</span><span class="spark">↓</span></div>`).join('')}
      </div>
    </div>`)}</div>`],
  // Claude בטלפון
  'section/service-single-3': [624, 807, `<div style="width:330px;height:680px;border-radius:52px;background:#1F1E1D;padding:12px;box-shadow:0 40px 80px -30px rgba(80,50,30,.5)">
    <div style="width:100%;height:100%;border-radius:42px;background:#FAF9F5;display:flex;flex-direction:column;overflow:hidden">
      <div style="height:54px;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;border-bottom:1px solid #ECE8E0"><span class="spark">✻</span>&nbsp;Claude</div>
      <div class="chat" style="padding:18px;gap:14px">
        <div class="user" style="font-size:15px">תכתוב לי הודעה ללקוחה שהשיעור עבר ליום רביעי</div>
        <div class="ai" style="font-size:15px"><span class="spark">✻</span> היי נועה 🙂 רק עדכון קטן – השיעור של השבוע עובר ליום רביעי, באותה שעה. נתראה!</div>
        <div style="flex:1"></div>
        <div class="input" style="font-size:14px;padding:12px 14px"><span>הודעה ל-Claude…</span><span class="send" style="width:30px;height:30px">↑</span></div>
      </div>
    </div></div>`],
  // תעודת סיום
  'section/service-single-4': [804, 903, `<div style="width:620px;height:760px;background:#fff;border-radius:22px;box-shadow:0 40px 80px -30px rgba(80,50,30,.35);padding:22px">
    <div style="height:100%;border:2px solid #EBC9B8;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:18px;padding:40px">
      <div style="font-size:52px" class="spark">✻</div>
      <div class="muted" style="font-size:18px;letter-spacing:2px">תעודת סיום</div>
      <div style="font-size:42px;font-weight:700;line-height:1.2">קורס Claude מאפס</div>
      <div class="muted" style="font-size:18px">מוענקת בזאת ל</div>
      <div style="font-size:34px;font-weight:700;border-bottom:2px solid #1F1E1D;padding:0 30px 8px">השם שלכם</div>
      <div class="muted" style="font-size:16px;line-height:1.6">על השלמת 8 שיעורים: מהשאלה הראשונה<br>ועד אתר שנבנה עם Claude Code</div>
      <div style="display:flex;justify-content:space-between;width:100%;margin-top:30px;font-size:16px"><span style="font-weight:700">Free AI</span><span class="muted">2026</span></div>
    </div></div>`],
  // עמוד "עליי" – ציטוט
  'section/service-3': [832, 480, win(640, 370, 'Claude', `
    <div class="chat" style="gap:18px;padding:26px 30px">
      <div class="user" style="font-size:18px">כמה עולה ללמוד Claude מאפס?</div>
      <div class="ai" style="font-size:18px"><span class="spark">✻</span> ב-Free AI – <b>₪0</b>. כל הקורס, הקבצים והתעודה פתוחים לכולם, בעברית.</div>
      <div style="flex:1"></div>
      <div class="input" style="font-size:16px;padding:14px 16px"><span>תשאלו כל דבר…</span><span class="send">↑</span></div>
    </div>`)],
  // סקיל בדיקת מהירות
  'section/featured-works-2': [1272, 660, `<div style="transform:scale(.95)">${win(1180, 620, 'דוח בדיקת מהירות', `
    <div style="padding:34px 42px;flex:1;display:flex;flex-direction:column;gap:22px;background:#fff">
      <div style="display:flex;justify-content:space-between;align-items:end">
        <div><div style="font-size:36px;font-weight:700">בדיקת מהירות לאתר</div><div class="muted" style="font-size:18px;margin-top:6px">69 בדיקות · נוצר עם סקיל ל-Claude</div></div>
        <div style="text-align:left"><div style="font-size:60px;font-weight:700" class="spark">3.8<span style="font-size:24px" class="muted"> שנ׳</span></div><div class="muted" style="font-size:16px">זמן טעינה בישראל</div></div>
      </div>
      ${[['תמונות כבדות בדף הבית', '−1.6 שנ׳', 'bad'], ['השרת רחוק מהגולשים בישראל', '−0.9 שנ׳', 'warn'], ['פונטים נטענים לפני הטקסט', '−0.4 שנ׳', 'warn']].map(([t, n, c]) => `
      <div style="display:flex;align-items:center;gap:16px;font-size:21px;border:1px solid #F0ECE5;border-radius:14px;padding:16px 20px">
        <span class="${c}" style="font-weight:700;font-size:24px">●</span><span style="flex:1">${t}</span><span style="font-weight:700;direction:ltr">${n}</span>
        <span style="background:#FBEDE6;color:#B85C3E;border-radius:20px;padding:6px 14px;font-size:15px;font-weight:600">פרומפט לתיקון</span></div>`).join('')}
    </div>`)}</div>`],
  // עמוד סקיל: Claude מריץ את הסקיל
  'section/work-single-1': [1914, 1092, `<div style="transform:scale(1.4)">${win(1240, 700, 'Claude', `
    <div class="chat" style="padding:34px 60px;gap:22px">
      <div class="user" style="font-size:22px">תבדוק לי את האבטחה של האתר</div>
      <div class="muted" style="font-size:17px;display:flex;gap:10px;align-items:center"><span class="ficon" style="width:26px;height:26px;font-size:13px">✻</span>משתמש בסקיל: בדיקת אבטחה לאתר ולאפליקציה</div>
      <div class="ai" style="font-size:21px"><span class="spark">✻</span> סיימתי לבדוק 34 דברים. הנה מה שמצאתי, לפי סדר דחיפות:</div>
      ${[['bad', '✗', 'דחוף', 'טופס יצירת הקשר לא מוגן מספאם'], ['warn', '!', 'לשיפור', 'חסרה כותרת אבטחה בשרת'], ['ok', '✓', 'תקין', 'החיבור מוצפן (HTTPS) ועוד 30 בדיקות']].map(([c, s, l, t]) => `
      <div style="display:flex;gap:14px;align-items:center;font-size:20px;background:#fff;border:1px solid #ECE8E0;border-radius:14px;padding:14px 18px"><span class="${c}" style="font-weight:700;font-size:22px;width:22px">${s}</span><b style="width:70px">${l}</b>${t}</div>`).join('')}
    </div>`)}</div>`],
  // עמוד סקיל: התקנת הסקיל
  'section/work-single-2': [1914, 1092, `<div style="transform:scale(1.35)">${skillsSettings(true)}</div>`],
  // בלוג
  'blog/blog-1': [1554, 1120, `<div style="transform:scale(1.15)">${skillsSettings(false)}</div>`],
  'blog/blog-2': [1554, 1120, `<div style="transform:scale(1.45)">${win(900, 560, 'Claude', `
    <div class="chat" style="justify-content:center;align-items:center;gap:30px">
      <div style="font-size:42px;font-weight:600"><span class="spark">✻</span> ערב טוב. במה נתחיל?</div>
      <div class="input" style="width:100%;font-size:20px"><span>תשאלו כל דבר…</span><span class="send">↑</span></div>
      <div style="display:flex;gap:12px;font-size:16px">${['לכתוב', 'ללמוד', 'לתכנן', 'לנתח קובץ'].map(t => `<span style="border:1px solid #E3DED5;border-radius:20px;padding:8px 16px;background:#fff">${t}</span>`).join('')}</div>
    </div>`)}</div>`],
  'blog/blog-3': [1554, 1120, `<div style="transform:scale(.95);position:relative;width:1400px;height:900px;display:flex;align-items:center;justify-content:center">
      ${win(1200, 760, 'shaked-bakery.co.il', site)}
      <div style="position:absolute;left:0;bottom:20px">${win(600, 320, 'Claude Code', `
        <div style="padding:22px 28px" class="tl">
          <div style="color:#fff">› תחבר את האתר לאחסון ולדומיין</div>
          <div class="muted">● מעלה לשרת…</div>
          <div class="ok">✓ האתר באוויר 24/7</div>
          <div class="ok" style="direction:ltr;text-align:right">shaked-bakery.co.il</div>
        </div>`, 'term')}</div>
    </div>`],
  'blog/blog-4': [1588, 1120, `<div style="display:flex;gap:40px;align-items:center;transform:scale(1.05)">
      ${win(560, 760, 'Claude', `<div class="chat" style="padding:30px;gap:20px">
        <div class="user" style="font-size:20px;max-width:100%">איך מתקינים סקיל?</div>
        <div class="ai" style="font-size:20px;line-height:1.7"><span class="spark">✻</span> שלושה צעדים:<br><b>1.</b> מורידים את קובץ ה-zip<br><b>2.</b> הגדרות ← סקילים ← העלאת סקיל<br><b>3.</b> מפעילים, ופותחים שיחה חדשה</div>
      </div>`)}
      ${win(720, 760, 'העלאת סקיל', `
        <div style="flex:1;background:#fff;padding:40px;display:flex;flex-direction:column;gap:24px">
          <div style="font-size:30px;font-weight:700">העלאת סקיל</div>
          <div style="border:2px dashed #EBC9B8;border-radius:20px;height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;background:#FDF8F5">
            <span class="ficon" style="width:64px;height:76px;font-size:16px">ZIP</span>
            <div style="font-size:20px;font-weight:600">website-security.zip</div>
            <div class="ok" style="font-size:18px;font-weight:600">✓ הועלה</div>
          </div>
          <div style="display:flex;align-items:center;gap:16px;border:1px solid #ECE8E0;border-radius:16px;padding:18px 22px">
            <div style="flex:1;font-size:20px;font-weight:700">בדיקת אבטחה לאתר</div>
            <span style="width:52px;height:30px;border-radius:30px;background:#D97757;position:relative;direction:ltr"><span style="position:absolute;top:3px;right:3px;width:24px;height:24px;border-radius:50%;background:#fff"></span></span>
          </div>
        </div>`)}
    </div>`],
};

(async () => {
  const browser = await chromium.launch();
  const shot = async (name, w, h, body, scale) => {
    const p = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    const tmp = path.join(OUT, `_${name}.html`);
    fs.writeFileSync(tmp, page(w, h, body));
    await p.goto('file://' + tmp);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(OUT, `${name}.jpg`), type: 'jpeg', quality: 88 });
    fs.unlinkSync(tmp);
    await p.close();
  };
  for (const [k, v] of Object.entries(S)) await shot(k, 832, 480, v, 2);
  for (const [k, v] of Object.entries(F)) await shot(k, 1908, 990, `<div style="transform:scale(1.18)">${v}</div>`, 1);
  const IMG = path.join(ROOT, 'site/assets/images');
  for (const [k, [w, h, body]] of Object.entries(P)) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    const tmp = path.join(OUT, '_tmp.html');
    fs.writeFileSync(tmp, page(w, h, body));
    await p.goto('file://' + tmp);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(IMG, `${k}.jpg`), type: 'jpeg', quality: 88 });
    fs.unlinkSync(tmp);
    await p.close();
  }
  // סקיל האבטחה בעמוד הסקילים – אותה תמונה כמו בדף הבית
  fs.copyFileSync(path.join(OUT, 'security-skill.jpg'), path.join(IMG, 'section/featured-works-1.jpg'));
  await browser.close();
  console.log('done', fs.readdirSync(OUT));
})();
