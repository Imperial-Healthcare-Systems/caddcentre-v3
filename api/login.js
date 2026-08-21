import { issueCookie, clearCookie, constantTimeEquals } from './_lib.js';

// Brute-force damping, per warm instance.
const attempts = new Map();

export default async function handler(req, res) {
  if (req.method === 'DELETE') {
    res.setHeader('Set-Cookie', clearCookie);
    return res.status(200).json({ ok: true });
  }
  if (req.method !== 'POST') return res.status(405).json({ error: 'method' });

  const ip = (req.headers['x-forwarded-for'] || 'local').split(',')[0];
  const rec = attempts.get(ip) || { n: 0, t: Date.now() };
  if (Date.now() - rec.t > 15 * 60 * 1000) { rec.n = 0; rec.t = Date.now(); }
  if (rec.n >= 8) return res.status(429).json({ error: 'too many attempts' });

  const { password } = req.body || {};
  if (!process.env.ADMIN_PASSWORD || !process.env.SESSION_SECRET) {
    return res.status(500).json({ error: 'server not configured' });
  }
  if (!password || !constantTimeEquals(password, process.env.ADMIN_PASSWORD)) {
    rec.n++; attempts.set(ip, rec);
    await new Promise(r => setTimeout(r, 400));       // slow down guessing
    return res.status(401).json({ error: 'invalid password' });
  }
  attempts.delete(ip);
  res.setHeader('Set-Cookie', issueCookie());
  return res.status(200).json({ ok: true });
}
