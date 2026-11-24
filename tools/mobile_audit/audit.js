const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  /* בדיקת טלפון: מוצאת כל אלמנט שנחתך או יוצא מהמסך, בכל העמודים.
   הרצה (השרת צריך לרוץ: PORT=3000 node server.js):  node tools/mobile_audit/audit.js all 375
   הרשימה של תפריט המדריך הסגור (ds-side) תקינה: הוא מחוץ למסך עד שפותחים אותו. */
  const fs0 = require('fs'), path0 = require('path');
  const pages = process.argv[2] === 'all' || !process.argv[2] ? fs0.readdirSync(path0.join(__dirname, '../../site')).filter(f => f.endsWith('.html')).map(f => f === 'index.html' ? '' : f.slice(0, -5)) : process.argv[2].split(',');
  const W = +(process.argv[3] || 375);
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: W, height: 800 }, isMobile: true, hasTouch: true });
  const out = {};
  for (const pg of pages) {
    const p = await ctx.newPage(); await p.addInitScript(() => { const s = () => { const st = document.createElement('style'); st.textContent = '#ag{display:none!important} html.ag-lock body>*{filter:none!important;pointer-events:auto!important} html.ag-lock,html.ag-lock body{overflow:visible!important}'; (document.head||document.documentElement).appendChild(st); }; if (document.documentElement) s(); else addEventListener('DOMContentLoaded', s); });
    try { await p.goto('http://localhost:3000/' + pg, { waitUntil: 'networkidle', timeout: 30000 }); } catch (e) {}
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
    await p.waitForTimeout(600);
    out[pg] = await p.evaluate((W) => {
      const res = { docOverflow: document.documentElement.scrollWidth - W, items: [] };
      const isHidden = el => { for (let e = el; e && e !== document.body; e = e.parentElement) { if (e.getAttribute && e.getAttribute('aria-hidden') === 'true') return true; const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return true; if (e.hidden) return true; } return false; };
      const path = el => { const a = []; for (let e = el; e && e !== document.body && a.length < 4; e = e.parentElement) a.unshift(e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '')); return a.join(' > '); };
      const scrollerOf = el => { for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) { const cs = getComputedStyle(e); if (/(auto|scroll)/.test(cs.overflowX) && e.scrollWidth > e.clientWidth + 2) return e; } return null; };
      const clipOf = el => { for (let e = el.parentElement; e && e !== document.documentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (/(hidden|clip)/.test(cs.overflowX) || /(hidden|clip)/.test(cs.overflow)) return e; } return null; };
      const cand = [...document.querySelectorAll('img,video,iframe,canvas,svg,button,input,textarea,select,table,pre,code,a,h1,h2,h3,h4,p,li,td,th,span,label,figure,blockquote')];
      const seen = new Set();
      for (const el of cand) {
        if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
        if (el.closest('header.gh, footer.sf, #a11y-toolbar, [class*="a11y"]')) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 4 || r.height < 4) continue;
        if (isHidden(el)) continue;
        if (scrollerOf(el)) continue;
        let bad = null;
        if (r.left < -1 || r.right > W + 1) bad = `viewport L${Math.round(r.left)} R${Math.round(r.right)}`;
        else { const c = clipOf(el); if (c) { const cr = c.getBoundingClientRect(); if (r.left < cr.left - 1 || r.right > cr.right + 1) bad = `clip(${path(c).split(' > ').pop()}) L${Math.round(r.left - cr.left)} R${Math.round(cr.right - r.right)}`; } }
        // text truncated by its own box
        if (!bad && /^(p|h1|h2|h3|h4|span|a|li|td|th|label|button)$/i.test(el.tagName) && el.scrollWidth > el.clientWidth + 2 && /(hidden|clip)/.test(getComputedStyle(el).overflowX)) bad = `self-trunc ${el.scrollWidth}>${el.clientWidth}`;
        if (bad) { const k = path(el); if (seen.has(k + bad)) continue; seen.add(k + bad); res.items.push({ y: Math.round(r.top + scrollY), bad, el: k, txt: (el.innerText || el.alt || el.src || '').trim().slice(0, 40) }); }
      }
      return res;
    }, W);
    await p.close();
  }
  await b.close();
  
  for (const [k, v] of Object.entries(out)) { const it = v.items.filter(i => !/ds-side|ds-scroll|ds-group|ds-profile|tk-item/.test(i.el)); if (v.docOverflow > 0 || it.length) { console.log(`== ${k || 'index'} גלילה לצד=${v.docOverflow}`); it.forEach(i => console.log('  ', i.bad, '|', i.el, '|', i.txt)); } }
  console.log('done');
})();
