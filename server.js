// שרת סטטי קטן ל-Free AI: מגיש את התיקייה site, בלי תלויות.
const http = require('http');
const fs = require('fs');
const path = require('path');

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

function send(res, file, status = 200) {
  fs.stat(file, (err, st) => {
    if (err || !st.isFile()) {
      if (status === 404) { res.writeHead(404); return res.end('Not found'); }
      return send(res, path.join(ROOT, 'index.html'), 404);
    }
    res.writeHead(status, {
      'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'Content-Length': st.size,
      'Cache-Control': file.endsWith('.html') ? 'no-cache' : 'public, max-age=86400',
    });
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
  // הקורס בשיפוצים: כל עמודי הקורס מראים את עמוד "תכף חוזרים"
  if (/^\/(service|service-single|guide-\d+)\/?$/.test(p)) return send(res, path.join(ROOT, 'soon.html'));
  let file = path.normalize(path.join(ROOT, p));
  if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (p.endsWith('/')) file = path.join(file, 'index.html');
  else if (!path.extname(file) && fs.existsSync(file + '.html')) file += '.html';
  send(res, file);
}).listen(PORT, '0.0.0.0', () => console.log(`Free AI on port ${PORT}`));
