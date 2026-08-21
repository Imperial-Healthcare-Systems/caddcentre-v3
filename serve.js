#!/usr/bin/env node
/**
 * Local development server.
 *
 * The production admin runs on serverless functions + Postgres. That needs a
 * deploy. This script gives you the identical admin experience on your own
 * machine with no database, no hosting account and no dependencies — it stores
 * data in a JSON file instead of Postgres.
 *
 *   ADMIN_PASSWORD='VGT@2026' node serve.js
 *   -> http://localhost:8080/admin
 *
 * Node 18+ required (uses the built-in crypto and http modules only).
 */

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
// This package IS the built site — pages live at the root. When the build is
// run from src/ it emits a dist/ alongside; prefer that if it is present.
const DIST = fs.existsSync(path.join(ROOT, 'dist', 'index.html'))
  ? path.join(ROOT, 'dist')
  : ROOT;
const DB_FILE = path.join(ROOT, 'data', 'local-db.json');
const UPLOADS = path.join(ROOT, 'data', 'uploads');
const MAX_UPLOAD = 20 * 1024 * 1024;   // 20 MB
const PORT = process.env.PORT || 8080;

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';
const SESSION_SECRET = process.env.SESSION_SECRET || crypto.randomBytes(32).toString('hex');

// The marketing site needs no password. Only /admin does — so serve the site
// either way and refuse the login rather than refusing to start.
if (!ADMIN_PASSWORD) {
  console.warn('\n  ADMIN_PASSWORD is not set — the site will serve, /admin will not sign in.');
  console.warn('  To enable the admin:\n');
  console.warn("      ADMIN_PASSWORD='choose-one' npm run dev");
  console.warn("      $env:ADMIN_PASSWORD='choose-one'; npm run dev   (PowerShell)");
}

/* ------------------------------------------------------------------- store */
function loadDb() {
  try { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); }
  catch { return { leads: [], posts: [], syllabi: {}, media: [], videos: [], nextLead: 1, nextVideo: 1 }; }
}
function saveDb(db) {
  fs.mkdirSync(path.dirname(DB_FILE), { recursive: true });
  fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2));
}
let db = loadDb();
for (const k of ['leads','posts','media','videos']) if (!db[k]) db[k] = [];
if (!db.syllabi) db.syllabi = {};
if (!db.nextVideo) db.nextVideo = 1;

/* ----------------------------------------------------------------- session */
const COOKIE = 'cadd_admin';
const sign = p => {
  const b = Buffer.from(JSON.stringify(p)).toString('base64url');
  return b + '.' + crypto.createHmac('sha256', SESSION_SECRET).update(b).digest('base64url');
};
function valid(tok) {
  if (!tok || !tok.includes('.')) return false;
  const [b, mac] = tok.split('.');
  const exp = crypto.createHmac('sha256', SESSION_SECRET).update(b).digest('base64url');
  const x = Buffer.from(mac), y = Buffer.from(exp);
  if (x.length !== y.length || !crypto.timingSafeEqual(x, y)) return false;
  try { return JSON.parse(Buffer.from(b, 'base64url').toString()).exp > Date.now(); }
  catch { return false; }
}
const authed = req => {
  const m = (req.headers.cookie || '').match(new RegExp(COOKIE + '=([^;]+)'));
  return m ? valid(m[1]) : false;
};

/* ------------------------------------------------------------------ helpers */
const MIME = { '.pdf':'application/pdf', '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8',
  '.js':'text/javascript; charset=utf-8', '.json':'application/json',
  '.svg':'image/svg+xml', '.webp':'image/webp', '.avif':'image/avif',
  '.png':'image/png', '.jpg':'image/jpeg', '.ico':'image/x-icon',
  '.csv':'text/csv; charset=utf-8', '.xml':'application/xml', '.md':'text/markdown' };

const json = (res, code, obj, extra = {}) => {
  res.writeHead(code, { 'Content-Type': 'application/json', ...extra });
  res.end(JSON.stringify(obj));
};

function rawBody(req, limit, res) {
  return new Promise((resolve, reject) => {
    const chunks = []; let total = 0, done = false;
    req.on('data', c => {
      if (done) return;
      total += c.length;
      if (total > limit) {
        done = true;
        // Answer first, then drain, so the client gets a readable error
        // rather than a dropped connection.
        if (res && !res.headersSent) {
          res.writeHead(413, { 'Content-Type': 'application/json', 'Connection': 'close' });
          res.end(JSON.stringify({ error: 'File exceeds the 20 MB limit' }));
        }
        req.resume();
        reject(Object.assign(new Error('too large'), { code: 'SIZE', answered: true }));
        return;
      }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function body(req) {
  return new Promise(r => {
    let d = '';
    req.on('data', c => d += c);
    req.on('end', () => { try { r(JSON.parse(d || '{}')); } catch { r({}); } });
  });
}

/* --------------------------------------------------------------------- API */
async function api(req, res, url) {
  const route = url.pathname;

  if (route === '/api/login') {
    if (req.method === 'DELETE') {
      return json(res, 200, { ok: true },
        { 'Set-Cookie': `${COOKIE}=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0` });
    }
    if (req.method !== 'POST') return json(res, 405, { error: 'method' });
    // Without a configured password there is nothing to authenticate against —
    // and two empty buffers compare equal, which would be an open door.
    if (!ADMIN_PASSWORD) {
      return json(res, 503, { error: 'Admin is disabled: start the server with ADMIN_PASSWORD set.' });
    }
    const { password } = await body(req);
    const a = Buffer.from(String(password || '')), b = Buffer.from(ADMIN_PASSWORD);
    const ok = a.length === b.length && crypto.timingSafeEqual(a, b);
    if (!ok) { await new Promise(r => setTimeout(r, 400)); return json(res, 401, { error: 'invalid password' }); }
    const tok = sign({ u: 'admin', exp: Date.now() + 8 * 3600 * 1000 });
    return json(res, 200, { ok: true },
      { 'Set-Cookie': `${COOKIE}=${tok}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800` });
  }

  if (route === '/api/leads') {
    if (req.method === 'POST') {
      const b = await body(req);
      if (b.company_website) return json(res, 200, { ok: true });
      const phone = String(b.phone || '').replace(/\D/g, '');
      if (!b.name || phone.length < 10) return json(res, 400, { error: 'name and 10-digit mobile required' });
      const row = { id: db.nextLead++, created_at: new Date().toISOString(),
        status: 'new', notes: '', ...b, phone };
      db.leads.unshift(row); saveDb(db);
      return json(res, 201, { ok: true, id: row.id });
    }
    if (!authed(req)) return json(res, 401, { error: 'unauthorised' });

    if (req.method === 'GET') {
      const q = (url.searchParams.get('q') || '').toLowerCase();
      const src = url.searchParams.get('source') || '';
      const st = url.searchParams.get('status') || '';
      let rows = db.leads.filter(l =>
        (!q || [l.name, l.phone, l.email, l.course].some(v => String(v || '').toLowerCase().includes(q))) &&
        (!src || l.source === src) && (!st || l.status === st));
      if (url.searchParams.get('format') === 'csv') {
        const cols = ['id','created_at','source','name','phone','email','stage','background',
                      'goal','course','recommended','slot_day','slot_time','slot_channel','status','notes'];
        const esc = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
        const csv = [cols.join(','), ...rows.map(r => cols.map(c => esc(r[c])).join(','))].join('\n');
        res.writeHead(200, { 'Content-Type': 'text/csv; charset=utf-8',
          'Content-Disposition': 'attachment; filename="cadd-leads.csv"' });
        return res.end('\uFEFF' + csv);
      }
      return json(res, 200, { rows });
    }
    if (req.method === 'PATCH') {
      const { id, status, notes } = await body(req);
      const l = db.leads.find(x => String(x.id) === String(id));
      if (l) { if (status) l.status = status; if (notes !== undefined) l.notes = notes; saveDb(db); }
      return json(res, 200, { ok: true });
    }
  }

  /* ---- upload: syllabus (PDF only) and article media, both capped at 20 MB */
  if (route === '/api/upload') {
    if (!authed(req)) return json(res, 401, { error: 'unauthorised' });
    if (req.method !== 'POST') return json(res, 405, { error: 'method' });
    const kind = url.searchParams.get('kind') || 'media';
    const slug = url.searchParams.get('slug') || '';
    const filename = (url.searchParams.get('filename') || 'file').replace(/[^\w.\-]/g, '_');

    if (kind === 'syllabus') {
      if (!slug) return json(res, 400, { error: 'course slug required' });
      if (!/\.pdf$/i.test(filename)) return json(res, 415, { error: 'Syllabus must be a PDF' });
    }
    let buf;
    try { buf = await rawBody(req, MAX_UPLOAD, res); }
    catch (e) {
      if (e.code === 'SIZE') return;          // already answered with 413
      throw e;
    }
    if (!buf.length) return json(res, 400, { error: 'empty file' });
    if (kind === 'syllabus' && buf.subarray(0, 5).toString('latin1') !== '%PDF-') {
      return json(res, 415, { error: 'That file is not a valid PDF' });
    }

    fs.mkdirSync(UPLOADS, { recursive: true });
    const stored = kind === 'syllabus' ? `syllabus-${slug}.pdf` : `${Date.now()}-${filename}`;
    fs.writeFileSync(path.join(UPLOADS, stored), buf);
    const publicUrl = '/uploads/' + stored;

    if (kind === 'syllabus') {
      db.syllabi[slug] = { course_slug: slug, filename, size_bytes: buf.length,
                           storage_url: publicUrl, uploaded_at: new Date().toISOString() };
    } else {
      db.media.unshift({ filename, mime: req.headers['content-type'] || '',
                         size_bytes: buf.length, storage_url: publicUrl,
                         uploaded_at: new Date().toISOString() });
    }
    saveDb(db);
    return json(res, 201, { ok: true, url: publicUrl, size: buf.length });
  }

  /* ---- syllabus: public download, admin listing and delete --------------- */
  if (route === '/api/syllabus') {
    if (req.method === 'GET' && url.searchParams.get('all') === '1') {
      if (!authed(req)) return json(res, 401, { error: 'unauthorised' });
      return json(res, 200, { rows: Object.values(db.syllabi) });
    }
    if (req.method === 'GET') {
      const slug = url.searchParams.get('slug');
      const row = db.syllabi[slug];
      if (!row) return json(res, 404, { error: 'No syllabus uploaded for this course yet' });
      res.writeHead(302, { Location: row.storage_url });
      return res.end();
    }
    if (!authed(req)) return json(res, 401, { error: 'unauthorised' });
    if (req.method === 'DELETE') {
      delete db.syllabi[url.searchParams.get('slug')]; saveDb(db);
      return json(res, 200, { ok: true });
    }
  }

  /* ---- videos for Life @ CADD ------------------------------------------- */
  if (route === '/api/videos') {
    if (req.method === 'GET' && url.searchParams.get('published') === '1') {
      return json(res, 200, { rows: db.videos.filter(v => v.status === 'published')
                                             .sort((a, b) => a.position - b.position) });
    }
    if (!authed(req)) return json(res, 401, { error: 'unauthorised' });
    if (req.method === 'GET') return json(res, 200, { rows: db.videos });
    if (req.method === 'POST') {
      const b = await body(req);
      if (!b.title || !b.url) return json(res, 400, { error: 'title and URL required' });
      if (!/^https:\/\//i.test(b.url)) return json(res, 400, { error: 'URL must start with https://' });
      db.videos.push({ id: db.nextVideo++, title: b.title, url: b.url,
                       caption: b.caption || '', position: Number(b.position) || 0,
                       status: b.status || 'published', created_at: new Date().toISOString() });
      saveDb(db);
      return json(res, 201, { ok: true });
    }
    if (req.method === 'DELETE') {
      db.videos = db.videos.filter(v => String(v.id) !== url.searchParams.get('id'));
      saveDb(db);
      return json(res, 200, { ok: true });
    }
  }

  if (route === '/api/posts') {
    if (req.method === 'GET' && url.searchParams.get('published') === '1') {
      return json(res, 200, { rows: db.posts.filter(p => p.status === 'published') });
    }
    if (!authed(req)) return json(res, 401, { error: 'unauthorised' });
    if (req.method === 'GET') return json(res, 200, { rows: db.posts });
    if (req.method === 'POST' || req.method === 'PUT') {
      const b = await body(req);
      if (!b.slug || !b.title || !b.body_md) return json(res, 400, { error: 'slug, title and body required' });
      const slug = b.slug.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-|-$/g, '');
      const i = db.posts.findIndex(p => p.slug === slug);
      const row = { ...b, slug, updated_at: new Date().toISOString(),
        published_at: b.status === 'published' ? new Date().toISOString() : null };
      if (i >= 0) db.posts[i] = { ...db.posts[i], ...row }; else db.posts.unshift(row);
      saveDb(db);
      return json(res, 200, { ok: true, slug, status: row.status });
    }
    if (req.method === 'DELETE') {
      db.posts = db.posts.filter(p => p.slug !== url.searchParams.get('slug'));
      saveDb(db);
      return json(res, 200, { ok: true });
    }
  }

  return json(res, 404, { error: 'no such endpoint' });
}

/* ------------------------------------------------------------------ static */
function serveStatic(req, res, url) {
  let p = decodeURIComponent(url.pathname);

  // locally-uploaded syllabi and media
  if (p.startsWith('/uploads/')) {
    const f = path.join(UPLOADS, path.basename(p));
    if (fs.existsSync(f)) {
      res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream',
                           'Content-Disposition': 'inline; filename="' + path.basename(f) + '"' });
      return fs.createReadStream(f).pipe(res);
    }
    res.writeHead(404); return res.end('not found');
  }
  if (p.endsWith('/')) p += 'index.html';
  let file = path.join(DIST, p);
  if (!file.startsWith(DIST)) { res.writeHead(403); return res.end('forbidden'); }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) {
    // try the directory form, then 404
    const alt = path.join(DIST, p, 'index.html');
    if (fs.existsSync(alt)) file = alt;
    else {
      const f404 = path.join(DIST, '404.html');
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(fs.existsSync(f404) ? fs.readFileSync(f404) : 'Not found');
    }
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
}

/* ------------------------------------------------------------------- server */
http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  try {
    if (url.pathname.startsWith('/api/')) return await api(req, res, url);
    serveStatic(req, res, url);
  } catch (e) {
    console.error(e); json(res, 500, { error: 'server error' });
  }
}).listen(PORT, () => {
  console.log(`\n  CADD Centre Gurugram — local server\n`);
  console.log(`  Site   http://localhost:${PORT}/`);
  console.log(`  Admin  http://localhost:${PORT}/admin/`);
  console.log(`  Data   ${path.relative(ROOT, DB_FILE)} (JSON, no database needed)\n`);
});
