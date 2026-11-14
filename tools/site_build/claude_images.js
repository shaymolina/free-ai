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
  await browser.close();
  console.log('done', fs.readdirSync(OUT));
})();
