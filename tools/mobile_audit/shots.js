const { chromium } = require('playwright');
(async () => {
  /* צילומי מסך של טלפון, מסך אחרי מסך, לבדיקה בעין: node tools/mobile_audit/shots.js index,guide-1 375 (התמונות ב-shots/) */
  const pages = process.argv[2].split(',').map(p => p === 'index' ? '' : p); require('fs').mkdirSync('shots', { recursive: true }); const W = +(process.argv[3]||375), H = 812;
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: W, height: H }, isMobile: true, hasTouch: true });
  for (const pg of pages) {
    const p = await ctx.newPage(); await p.addInitScript(() => { const s = () => { const st = document.createElement('style'); st.textContent = '#ag{display:none!important} html.ag-lock body>*{filter:none!important;pointer-events:auto!important} html.ag-lock,html.ag-lock body{overflow:visible!important}'; (document.head||document.documentElement).appendChild(st); }; if (document.documentElement) s(); else addEventListener('DOMContentLoaded', s); });
    try { await p.goto('http://localhost:3000/' + pg, { waitUntil: 'networkidle', timeout: 30000 }); } catch (e) {}
    const total = await p.evaluate(() => document.documentElement.scrollHeight);
    let i = 0;
    for (let y = 0; y < total; y += H - 60) {
      await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(900);
      await p.screenshot({ path: `shots/v-${pg||'index'}-${String(i++).padStart(2,'0')}.png` });
    }
    console.log(pg||'index', i);
    await p.close();
  }
  await b.close();
})();
