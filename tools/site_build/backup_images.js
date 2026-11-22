// איורי השלבים במאמר הגיבוי מ-GitHub ל-Google Drive (איורים, לא צילומי מסך)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const OUT = path.join(ROOT, 'site/assets/images/guide');
const FONTS = 'file://' + path.join(ROOT, 'site/assets/fonts/fonts.css');
const CSS = `*{box-sizing:border-box;margin:0;padding:0;unicode-bidi:plaintext}
body{width:800px;height:480px;font-family:'Urbanist',sans-serif;color:#1F1E1D;background:#F4EFE7;display:flex;align-items:center;justify-content:center}
.win{width:740px;height:420px;background:#FAF9F5;border-radius:16px;box-shadow:0 20px 50px -20px rgba(80,50,30,.35),0 0 0 1px rgba(0,0,0,.07);overflow:hidden;display:flex;flex-direction:column}
.bar{height:40px;background:#F0ECE4;display:flex;align-items:center;gap:7px;padding:0 14px;direction:ltr}
.bar i{width:11px;height:11px;border-radius:50%;background:#DDD7CC}
.url{flex:1;margin:0 12px;background:#fff;border-radius:8px;height:26px;font-size:14px;color:#6b665f;display:flex;align-items:center;padding:0 12px}
.body{flex:1;display:flex;flex-direction:column;gap:14px;padding:22px 30px;direction:ltr}
h2{font-size:24px;font-weight:700}
.lbl{font-size:15px;font-weight:700;margin-bottom:6px}
.inp{width:360px;padding:11px 13px;border-radius:10px;border:1px solid #DDD7CC;background:#fff;font-size:16px}
.btn{display:inline-block;padding:11px 18px;border-radius:10px;border:1px solid #DDD7CC;background:#fff;font-size:16px;font-weight:600}
.pri{background:#A4572D;color:#fff;border:0}
.blue{background:#1A73E8;color:#fff;border:0}
.hl{outline:4px solid rgba(217,119,87,.55);outline-offset:3px}
.chk{display:flex;gap:10px;align-items:center;font-size:16px}.chk u{width:20px;height:20px;border:2px solid #A4572D;border-radius:5px;background:#A4572D;display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;text-decoration:none}
.chk em{font-style:normal;color:#8a857e;font-size:14px}
.n{position:absolute;width:30px;height:30px;border-radius:50%;background:#D97757;color:#fff;font-size:16px;font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(0,0,0,.2)}
.rel{position:relative}
.code{flex:1;background:#fff;border:1px solid #E5E0D7;border-radius:10px;padding:14px 16px;font-family:ui-monospace,Menlo,monospace;font-size:15px;line-height:1.75;color:#3b3833}
.code .c{color:#8a857e}.code .s{color:#B85C3E}.code .k{color:#7a3fb0}
.line{display:block;padding:0 6px;border-radius:6px;unicode-bidi:normal;text-align:left}.line .he{unicode-bidi:isolate}
.tool{display:flex;gap:12px;align-items:center}
.ico{width:40px;height:40px;border-radius:10px;border:1px solid #DDD7CC;background:#fff;display:flex;align-items:center;justify-content:center;font-size:20px}
.sel{padding:10px 14px;border-radius:10px;border:1px solid #DDD7CC;background:#fff;font-family:ui-monospace,Menlo,monospace;font-size:16px;min-width:140px;display:flex;justify-content:space-between;gap:12px}
.menu{border:1px solid #DDD7CC;background:#fff;border-radius:10px;width:200px;box-shadow:0 10px 24px -10px rgba(0,0,0,.25);font-family:ui-monospace,Menlo,monospace;font-size:15px}
.menu div{padding:9px 14px}.menu .on{background:#FBEDE6}
.dlg{width:430px;align-self:center;background:#fff;border:1px solid #E5E0D7;border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:12px;box-shadow:0 14px 30px -14px rgba(0,0,0,.3)}
.dlg p{font-size:15px;color:#5f5a53}
.lnk{color:#1A73E8;font-size:15px;font-weight:600}
.row{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:10px;background:#fff;border:1px solid #E5E0D7;font-size:16px}
.fold{width:26px;height:20px;border-radius:4px;background:#F2B84B}
.zip{width:22px;height:26px;border-radius:4px;background:#C9C3B8;font-size:9px;font-weight:700;color:#fff;display:flex;align-items:center;justify-content:center}
.crumb{font-size:16px;color:#6b665f}.crumb b{color:#1F1E1D}
.side{width:150px;background:#F5F2EC;border-left:1px solid #E5E0D7;padding:16px;font-size:15px;display:flex;flex-direction:column;gap:12px}`;
const win = (url, inner, style = '') => `<div class="win"><div class="bar"><i></i><i></i><i></i><div class="url">${url}</div></div><div class="body" style="${style}">${inner}</div></div>`;
const n = (x, y, t) => `<span class="n" style="left:${x}px;top:${y}px">${t}</span>`;
const S = {
 1: win('github.com/settings/tokens/new', `
   <h2>New personal access token</h2>
   <div class="rel"><div class="lbl">Note</div><div class="inp hl">גיבוי לדרייב</div>${n(392,34,1)}</div>
   <div class="rel"><div class="lbl">Expiration</div><div class="inp hl" style="width:220px">No expiration ▾</div>${n(252,34,2)}</div>
   <div class="rel"><div class="chk hl" style="width:max-content;padding:4px 8px 4px 4px"><u>✓</u><b>repo</b><em>Full control of private repositories</em></div>${n(380,0,3)}</div>
   <div class="rel" style="margin-top:4px"><span class="btn pri hl">Generate token</span>${n(160,6,4)}</div>`),
 2: win('script.google.com', `
   <div style="display:flex;align-items:center;gap:14px"><h2>Apps Script</h2></div>
   <div class="rel" style="margin-top:6px;width:max-content"><span class="btn blue hl" style="font-size:18px;padding:14px 22px">+ פרויקט חדש</span>${n(-46,10,1)}</div>
   <div class="lbl" style="margin-top:18px;color:#8a857e">הפרויקטים שלי</div>
   <div class="row" style="width:360px;color:#8a857e">עדיין אין פרויקטים</div>`, 'direction:rtl'),
 3: win('script.google.com · Code.gs', `
   <div class="code rel">
    <span class="line c">// <span class="he">שמים כאן מפתח אחד לכל חשבון GitHub</span></span>
    <span class="line"><span class="k">const</span> TOKENS = [</span>
    <span class="line hl" style="background:#FBEDE6">&nbsp;&nbsp;<span class="s">'ghp_A1b2C3d4E5f6G7h8...'</span>,</span>
    <span class="line c">&nbsp;&nbsp;// 'PASTE_TOKEN_ACCOUNT_2',</span>
    <span class="line">];</span>
    <span class="line">&nbsp;</span>
    <span class="line"><span class="k">const</span> ROOT_FOLDER = <span class="s">'GitHub Backups'</span>;</span>
    <span class="line"><span class="k">const</span> RUN_HOUR = 3;</span>
    ${n(640,60,1)}
   </div>`),
 4: win('script.google.com · Code.gs', `
   <div class="tool rel">
     <span class="ico hl">💾</span>
     <span class="btn">▶ הפעלה</span>
     <span class="sel hl"><span>setup</span><span>▾</span></span>
     ${n(-8,-12,1)}${n(330,-12,2)}
   </div>
   <div class="menu" style="margin-left:150px;margin-top:-6px"><div class="on">setup</div><div>backupAll</div><div>continueBackup</div></div>
   <div class="dlg rel" style="margin-top:-40px;margin-left:330px;width:340px;padding:16px">
     <b>נדרשת הרשאה</b><p>הפרויקט מבקש גישה לחשבון שלכם.</p>
     <span class="btn blue hl" style="text-align:center">בדיקת הרשאות</span>
     <span class="lnk" dir="rtl">מתקדם (Advanced) ← מעבר אל... ← אישור</span>
     ${n(306,72,3)}
   </div>`),
 5: win('drive.google.com', `
   <div style="display:flex;flex:1;margin:-22px -30px;direction:rtl">
    <div class="side"><b>הדרייב שלי</b><span>אחרונים</span><span>אשפה</span></div>
    <div style="flex:1;padding:22px 26px;display:flex;flex-direction:column;gap:12px" class="rel">
     <div class="crumb" dir="rtl">הדרייב שלי › <b class="hl" style="padding:2px 6px;border-radius:6px">GitHub Backups</b> › <b>my-account</b></div>
     <div class="row hl"><span class="zip">ZIP</span>my-first-site.zip</div>
     <div class="row"><span class="zip">ZIP</span>free-ai.zip</div>
     <div class="row"><span class="zip">ZIP</span>shop-app.zip</div>
     ${n(4,8,1)}
    </div>
   </div>`),
};
(async () => {
  const b = await chromium.launch();
  for (const [k, v] of Object.entries(S)) {
    const p = await b.newPage({ viewport: { width: 800, height: 480 }, deviceScaleFactor: 2 });
    const t = path.join(OUT, '_t.html');
    fs.writeFileSync(t, `<!doctype html><html lang="he"><head><meta charset="utf-8"><link rel="stylesheet" href="${FONTS}"><style>${CSS}</style></head><body>${v}</body></html>`);
    await p.goto('file://' + t); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(OUT, `backup-${k}.png`) });
    await p.close();
  }
  fs.unlinkSync(path.join(OUT, '_t.html')); await b.close();
})();
