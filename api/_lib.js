// Shared helpers. No dependencies beyond @neondatabase/serverless.
import { neon } from '@neondatabase/serverless';
import crypto from 'node:crypto';

export const sql = neon(process.env.DATABASE_URL);

const COOKIE = 'cadd_admin';

/* ---------------------------------------------------------------- sessions
   A signed, HTTP-only cookie. The secret and the password both come from the
   environment — nothing authenticating ever reaches client JavaScript, which
   is the whole reason this cannot be done on the static site alone. */
function sign(payload) {
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const mac = crypto.createHmac('sha256', process.env.SESSION_SECRET)
                    .update(body).digest('base64url');
  return `${body}.${mac}`;
}

export function verify(token) {
  if (!token || !token.includes('.')) return null;
  const [body, mac] = token.split('.');
  const expected = crypto.createHmac('sha256', process.env.SESSION_SECRET)
                         .update(body).digest('base64url');
  const a = Buffer.from(mac), b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  const data = JSON.parse(Buffer.from(body, 'base64url').toString());
  if (!data.exp || data.exp < Date.now()) return null;
  return data;
}

export function issueCookie() {
  const token = sign({ u: 'admin', exp: Date.now() + 8 * 60 * 60 * 1000 });
  return `${COOKIE}=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=28800`;
}

export const clearCookie =
  `${COOKIE}=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0`;

export function sessionFrom(req) {
  const raw = req.headers.cookie || '';
  const m = raw.match(new RegExp(`${COOKIE}=([^;]+)`));
  return m ? verify(m[1]) : null;
}

/** Gate a handler behind a valid session. Returns true if the request was
 *  rejected, so callers can `if (requireAuth(req,res)) return;` */
export function requireAuth(req, res) {
  if (sessionFrom(req)) return false;
  res.status(401).json({ error: 'unauthorised' });
  return true;
}

export function constantTimeEquals(a, b) {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

export function hashIp(req) {
  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim();
  return crypto.createHash('sha256')
               .update(ip + (process.env.SESSION_SECRET || '')).digest('hex').slice(0, 32);
}
