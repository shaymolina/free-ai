// ציורי שלבי ההרשמה ל-Claude (איורים בעברית, לא צילומי מסך)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const OUT = path.join(ROOT, 'site/assets/images/guide');
fs.mkdirSync(OUT, { recursive: true });
const FONTS = 'file://' + path.join(ROOT, 'site/assets/fonts/fonts.css');
const CSS = `*{box-sizing:border-box;margin:0;padding:0}
body{width:800px;height:480px;font-family:'Urbanist',sans-serif;color:#1F1E1D;direction:rtl;background:#F4EFE7;display:flex;align-items:center;justify-content:center}
.win{width:740px;height:420px;background:#FAF9F5;border-radius:16px;box-shadow:0 20px 50px -20px rgba(80,50,30,.35),0 0 0 1px rgba(0,0,0,.07);overflow:hidden;display:flex;flex-direction:column}
.bar{height:40px;background:#F0ECE4;display:flex;align-items:center;gap:7px;padding:0 14px;direction:ltr}
.bar i{width:11px;height:11px;border-radius:50%;background:#DDD7CC}
.url{flex:1;margin:0 12px;background:#fff;border-radius:8px;height:26px;font-size:14px;color:#6b665f;display:flex;align-items:center;padding:0 12px}
.body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:20px}
h2{font-size:26px;font-weight:700;text-align:center}
.sp{color:#D97757}
.btn{width:340px;padding:13px;border-radius:12px;border:1px solid #DDD7CC;background:#fff;text-align:center;font-size:17px;font-weight:600}
.pri{background:#D97757;color:#fff;border:0}
.inp{width:340px;padding:13px;border-radius:12px;border:1px solid #DDD7CC;background:#fff;font-size:17px;color:#9a948b}
.hl{outline:4px solid rgba(217,119,87,.45);outline-offset:3px}
.codes{display:flex;gap:10px;direction:ltr}.codes b{width:46px;height:56px;border:1px solid #DDD7CC;border-radius:10px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:26px}
.plans{display:flex;gap:14px}.plan{width:210px;border:1px solid #DDD7CC;background:#fff;border-radius:14px;padding:16px;text-align:center}
.plan.on{border:2px solid #D97757}.plan b{display:block;font-size:20px;margin-bottom:6px}.plan span{font-size:15px;color:#6b665f}
.chk{display:flex;gap:10px;align-items:center;font-size:15px;color:#6b665f;width:340px}.chk u{width:20px;height:20px;border:2px solid #D97757;border-radius:5px;background:#D97757;display:block}
.in{width:340px;height:50px;border:1px solid #DDD7CC;border-radius:14px;background:#fff;display:flex;justify-content:space-between;align-items:center;padding:0 14px;font-size:16px;color:#9a948b}
.s{width:30px;height:30px;border-radius:8px;background:#D97757;color:#fff;display:flex;align-items:center;justify-content:center}`;
const win = (url, inner) => `<div class="win"><div class="bar"><i></i><i></i><i></i><div class="url">${url}</div></div><div class="body">${inner}</div></div>`;
const S = {
 1: win('claude.ai', `<h2><span class="sp">✻</span> Claude</h2><div class="btn pri hl">התחברות / הרשמה</div>`),
 2: win('claude.ai/login', `<h2>ברוכים הבאים</h2><div class="btn hl">המשך עם Google</div><div style="color:#9a948b">או</div><div class="inp">name@email.com</div><div class="btn pri">המשך עם מייל</div>`),
 3: win('claude.ai/login', `<h2>הקוד נשלח למייל שלכם</h2><div class="codes hl"><b>4</b><b>8</b><b>2</b><b>9</b><b>1</b><b>7</b></div><div class="btn pri">אישור</div>`),
 4: win('claude.ai/onboarding', `<h2>איך לקרוא לכם?</h2><div class="inp hl">השם שלכם</div><div class="chk"><u></u>אני מאשר/ת את התנאים</div><div class="btn pri">המשך</div>`),
 5: win('claude.ai/upgrade', `<h2>בוחרים מסלול</h2><div class="plans"><div class="plan"><b>Free</b><span>להתחיל בחינם</span></div><div class="plan on hl"><b>Pro</b><span>נדרש ל-Claude Code</span></div></div>`),
 6: win('claude.ai/new', `<h2><span class="sp">✻</span> ערב טוב. במה נתחיל?</h2><div class="in hl"><span>תשאלו כל דבר…</span><span class="s">↑</span></div>`),
};
Object.assign(S, {
 'i1': win('claude.com/download', `<h2><span class="sp">✻</span> הורדת Claude</h2><div class="btn pri hl">להורדה</div>`),
 'i2': win('claude.com/download', `<h2>בוחרים מחשב</h2><div style="display:flex;gap:14px"><div class="btn hl" style="width:200px">Mac</div><div class="btn" style="width:200px">Windows</div></div>`),
 'i3': win('הורדות', `<h2>ההתקנה</h2><div class="btn hl">Claude-Setup ⬇ פתיחה</div><div class="btn pri">התקנה</div>`),
 'i4': win('Claude', `<h2><span class="sp">✻</span> התחברות</h2><div class="inp hl">name@email.com</div><div class="btn pri">המשך</div>`),
 'i5': win('Claude', `<div style="display:flex;gap:10px;direction:ltr"><div class="btn" style="width:110px">Chat</div><div class="btn hl pri" style="width:110px">Code</div></div><h2>במה נבנה היום?</h2><div class="in"><span>תארו מה לבנות…</span><span class="s">↑</span></div>`),
});
(async () => {
  const b = await chromium.launch();
  for (const [k, v] of Object.entries(S)) {
    const p = await b.newPage({ viewport: { width: 800, height: 480 }, deviceScaleFactor: 2 });
    const t = path.join(OUT, '_t.html');
    fs.writeFileSync(t, `<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><link rel="stylesheet" href="${FONTS}"><style>${CSS}</style></head><body>${v}</body></html>`);
    await p.goto('file://' + t); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(OUT, (/^\d+$/.test(k)?`claude-signup-${k}.png`:`claude-install-${k.slice(1)}.png`)) });
    await p.close();
  }
  fs.unlinkSync(path.join(OUT, '_t.html')); await b.close();
})();
