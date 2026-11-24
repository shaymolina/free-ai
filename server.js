// שרת סטטי קטן ל-Free AI: מגיש את התיקייה site, בלי תלויות.
const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const ROOT = path.join(__dirname, 'site');
const PORT = process.env.PORT || 3000;
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.woff2': 'font/woff2',
  '.woff': 'font/woff', '.ttf': 'font/ttf', '.eot': 'application/vnd.ms-fontobject',
};

const OLD = {
  '/service': '/course', '/service-single': '/course-lessons',
  '/work': '/skills', '/work-single': '/skill-security', '/work-site-speed': '/skill-site-speed',
};

// קבצי טקסט נשלחים דחוסים (פי 4-8 קטנים יותר). הדחיסה נשמרת בזיכרון לפי זמן השינוי של הקובץ.
const SQUEEZE = /\.(html|css|js|json|xml|txt|svg)$/i;
const packed = new Map();
function pack(file, st, enc) {
  const key = file + '|' + enc, hit = packed.get(key);
  if (hit && hit.m === st.mtimeMs) return hit.b;
  const raw = fs.readFileSync(file);
  const b = enc === 'br'
    ? zlib.brotliCompressSync(raw, { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 9, [zlib.constants.BROTLI_PARAM_SIZE_HINT]: raw.length } })
    : zlib.gzipSync(raw, { level: 9 });
  packed.set(key, { m: st.mtimeMs, b });
  return b;
}

function send(res, file, status = 200, req = null) {
  fs.stat(file, (err, st) => {
    if (err || !st.isFile()) {
      if (status === 404) { res.writeHead(404); return res.end('Not found'); }
      return send(res, path.join(ROOT, 'index.html'), 404, req);
    }
    const isHtml = file.endsWith('.html');
    // קבצים עם ?v= משתנים רק כשהגרסה משתנה, אז הדפדפן שומר אותם לחודש
    const versioned = req && /[?&]v=/.test(req.url);
    const headers = {
      'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': isHtml ? 'no-cache' : versioned ? 'public, max-age=2592000' : 'public, max-age=86400',
      'Last-Modified': new Date(st.mtime).toUTCString(),
    };
    if (status === 200 && req && req.headers['if-modified-since']) {
      const since = Date.parse(req.headers['if-modified-since']);
      if (since && Math.floor(st.mtimeMs / 1000) <= Math.floor(since / 1000)) { res.writeHead(304, headers); return res.end(); }
    }
    const ae = (req && req.headers['accept-encoding']) || '';
    const enc = SQUEEZE.test(file) && st.size > 1024 ? (/\bbr\b/.test(ae) ? 'br' : /\bgzip\b/.test(ae) ? 'gzip' : null) : null;
    if (SQUEEZE.test(file)) headers['Vary'] = 'Accept-Encoding';
    if (enc) {
      let body;
      try { body = pack(file, st, enc); } catch { body = null; }
      if (body) {
        headers['Content-Encoding'] = enc; headers['Content-Length'] = body.length;
        res.writeHead(status, headers);
        return res.end(req.method === 'HEAD' ? undefined : body);
      }
    }
    headers['Content-Length'] = st.size;
    res.writeHead(status, headers);
    if (req && req.method === 'HEAD') return res.end();
    fs.createReadStream(file).pipe(res);
  });
}

http.createServer((req, res) => {
  let p;
  try { p = decodeURIComponent(new URL(req.url, 'http://x').pathname); } catch { p = '/'; }
  if (p.endsWith('.html')) {
    const u = new URL(req.url, 'http://x');
    const clean = p === '/index.html' || p.endsWith('/index.html') ? p.slice(0, -10) || '/' : p.slice(0, -5);
    res.writeHead(301, { Location: clean + u.search });
    return res.end();
  }
  // כתובות ישנות עוברות לחדשות (301), כדי שקישורים וגוגל לא יישברו
  const moved = OLD[p.replace(/\/$/, '')];
  if (moved) {
    res.writeHead(301, { Location: moved + new URL(req.url, 'http://x').search });
    return res.end();
  }
  // הקורס בשיפוצים: עמודי הקורס (לא המדריך) מראים את עמוד "תכף חוזרים"
  if (/^\/(course|course-lessons)\/?$/.test(p)) return send(res, path.join(ROOT, 'soon.html'), 200, req);
  let file = path.normalize(path.join(ROOT, p));
  if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (p.endsWith('/')) file = path.join(file, 'index.html');
  else if (!path.extname(file) && fs.existsSync(file + '.html')) file += '.html';
  send(res, file, 200, req);
}).listen(PORT, '0.0.0.0', () => console.log(`Free AI on port ${PORT}`));
