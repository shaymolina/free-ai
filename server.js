// שרת סטטי קטן ל-Free AI: מגיש את התיקייה site, בלי תלויות.
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');

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


// ---- חשבונות משתמשים: מייל וסיסמה, וגוגל ----
// החשבונות נשמרים בקובץ users.json בתיקייה DATA_DIR (ברירת מחדל: data ליד השרת). הסיסמאות נשמרות מוצפנות (scrypt).
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
const USERS_FILE = path.join(DATA_DIR, 'users.json');
fs.mkdirSync(DATA_DIR, { recursive: true });
function loadUsers() { try { return JSON.parse(fs.readFileSync(USERS_FILE, 'utf8')); } catch { return {}; } }
let users = loadUsers();
function saveUsers() { const tmp = USERS_FILE + '.tmp'; fs.writeFileSync(tmp, JSON.stringify(users, null, 1)); fs.renameSync(tmp, USERS_FILE); }
const SECRET = process.env.AUTH_SECRET || (() => {
  const f = path.join(DATA_DIR, 'secret');
  try { return fs.readFileSync(f, 'utf8'); } catch { const k = crypto.randomBytes(32).toString('hex'); fs.writeFileSync(f, k); return k; }
})();
const COOKIE = 'fa_s', MAX_AGE = 60 * 60 * 24 * 180;
function sign(email) {
  const v = Buffer.from(email).toString('base64url') + '.' + Date.now();
  return v + '.' + crypto.createHmac('sha256', SECRET).update(v).digest('base64url');
}
function readSession(req) {
  const m = (req.headers.cookie || '').match(/(?:^|;\s*)fa_s=([^;]+)/);
  if (!m) return null;
  const [e, t, h] = m[1].split('.');
  if (!h || crypto.createHmac('sha256', SECRET).update(e + '.' + t).digest('base64url') !== h) return null;
  const u = users[Buffer.from(e, 'base64url').toString()];
  return u || null;
}
function json(res, status, obj, cookie) {
  const h = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' };
  if (cookie !== undefined) h['Set-Cookie'] = cookie === null
    ? `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`
    : `${COOKIE}=${cookie}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`;
  res.writeHead(status, h); res.end(JSON.stringify(obj));
}
function body(req) {
  return new Promise((ok, bad) => {
    let d = ''; req.on('data', c => { d += c; if (d.length > 10000) { bad(new Error('big')); req.destroy(); } });
    req.on('end', () => { try { ok(JSON.parse(d || '{}')); } catch (e) { bad(e); } });
  });
}
const pub = u => ({ email: u.email, name: u.name || '', picture: u.picture || '' });
const hash = (pw, salt) => crypto.scryptSync(pw, salt, 64).toString('hex');
// הגבלת ניסיונות: עד 10 טעויות סיסמה ל-15 דקות מאותה כתובת
const fails = new Map();
function limited(ip) { const f = fails.get(ip); return f && f.n >= 10 && Date.now() - f.t < 15 * 60e3; }
function failed(ip) { const f = fails.get(ip); fails.set(ip, f && Date.now() - f.t < 15 * 60e3 ? { n: f.n + 1, t: f.t } : { n: 1, t: Date.now() }); }
function googleUser(token) {
  return new Promise((ok, bad) => {
    https.get('https://www.googleapis.com/oauth2/v3/userinfo', { headers: { Authorization: 'Bearer ' + token } }, r => {
      let d = ''; r.on('data', c => d += c); r.on('end', () => { try { const p = JSON.parse(d); p.email && p.email_verified !== false ? ok(p) : bad(); } catch (e) { bad(e); } });
    }).on('error', bad);
  });
}
async function authApi(req, res, p) {
  const ip = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '').split(',')[0].trim();
  if (p === '/api/auth/me') { const u = readSession(req); return json(res, u ? 200 : 401, u ? { user: pub(u) } : { error: 'signed_out' }); }
  if (req.method !== 'POST') return json(res, 405, { error: 'method' });
  if (p === '/api/auth/logout') return json(res, 200, { ok: true }, null);
  let b; try { b = await body(req); } catch { return json(res, 400, { error: 'bad_request' }); }
  if (p === '/api/auth/email') {
    if (limited(ip)) return json(res, 429, { error: 'too_many' });
    const email = String(b.email || '').trim().toLowerCase(), pw = String(b.password || '');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200 || pw.length < 8 || pw.length > 200) return json(res, 400, { error: 'invalid' });
    let u = users[email];
    if (u && !u.hash) return json(res, 409, { error: 'google_account' });
    if (u) {
      if (!crypto.timingSafeEqual(Buffer.from(hash(pw, u.salt), 'hex'), Buffer.from(u.hash, 'hex'))) { failed(ip); return json(res, 401, { error: 'wrong_password' }); }
    } else {
      const salt = crypto.randomBytes(16).toString('hex');
      u = users[email] = { email, name: email.split('@')[0], salt, hash: hash(pw, salt), via: 'email', created: new Date().toISOString() };
    }
    u.last = new Date().toISOString(); saveUsers();
    return json(res, 200, { user: pub(u) }, sign(email));
  }
  if (p === '/api/auth/google') {
    let g; try { g = await googleUser(String(b.access_token || '')); } catch { return json(res, 401, { error: 'google_failed' }); }
    const email = g.email.toLowerCase();
    const u = users[email] || (users[email] = { email, via: 'google', created: new Date().toISOString() });
    u.name = g.name || u.name || ''; u.picture = g.picture || ''; u.google = g.sub; u.last = new Date().toISOString(); saveUsers();
    return json(res, 200, { user: pub(u) }, sign(email));
  }
  return json(res, 404, { error: 'not_found' });
}

http.createServer((req, res) => {
  let p;
  try { p = decodeURIComponent(new URL(req.url, 'http://x').pathname); } catch { p = '/'; }
  if (p.startsWith('/api/auth/')) return authApi(req, res, p).catch(() => json(res, 500, { error: 'server' }));
  if (p.endsWith('.html')) {
    const u = new URL(req.url, 'http://x');
    const clean = p === '/index.html' || p.endsWith('/index.html') ? p.slice(0, -10) || '/' : p.slice(0, -5);
    res.writeHead(301, { Location: clean + u.search });
    return res.end();
  }
  // הקורס בשיפוצים: עמודי הקורס (לא המדריך) מראים את עמוד "תכף חוזרים"
  if (/^\/(service|service-single)\/?$/.test(p)) return send(res, path.join(ROOT, 'soon.html'));
  let file = path.normalize(path.join(ROOT, p));
  if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (p.endsWith('/')) file = path.join(file, 'index.html');
  else if (!path.extname(file) && fs.existsSync(file + '.html')) file += '.html';
  send(res, file);
}).listen(PORT, '0.0.0.0', () => console.log(`Free AI on port ${PORT}`));
