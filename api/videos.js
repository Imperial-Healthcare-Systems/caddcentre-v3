import { sql, requireAuth } from './_lib.js';

export default async function handler(req, res) {
  if (req.method === 'GET' && req.query.published === '1') {
    const rows = await sql`SELECT id,title,url,caption,position FROM videos
                           WHERE status = 'published' ORDER BY position, id`;
    res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=600');
    return res.status(200).json({ rows });
  }
  if (requireAuth(req, res)) return;

  if (req.method === 'GET') {
    const rows = await sql`SELECT * FROM videos ORDER BY position, id`;
    return res.status(200).json({ rows });
  }
  if (req.method === 'POST') {
    const b = req.body || {};
    if (!b.title || !b.url) return res.status(400).json({ error: 'title and URL required' });
    if (!/^https:\/\//i.test(b.url)) return res.status(400).json({ error: 'URL must start with https://' });
    await sql`INSERT INTO videos (title,url,caption,position,status)
              VALUES (${b.title}, ${b.url}, ${b.caption || null},
                      ${b.position || 0}, ${b.status || 'published'})`;
    if (process.env.DEPLOY_HOOK_URL) { try { await fetch(process.env.DEPLOY_HOOK_URL, { method: 'POST' }); } catch {} }
    return res.status(201).json({ ok: true });
  }
  if (req.method === 'DELETE') {
    await sql`DELETE FROM videos WHERE id = ${req.query.id}`;
    if (process.env.DEPLOY_HOOK_URL) { try { await fetch(process.env.DEPLOY_HOOK_URL, { method: 'POST' }); } catch {} }
    return res.status(200).json({ ok: true });
  }
  return res.status(405).json({ error: 'method' });
}
