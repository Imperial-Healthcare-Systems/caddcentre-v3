import { sql, requireAuth } from './_lib.js';

/* GET is PUBLIC: it redirects to the stored PDF so the download button works.
   GET ?all=1 and DELETE require an admin session. */
export default async function handler(req, res) {
  if (req.method === 'GET' && req.query.all === '1') {
    if (requireAuth(req, res)) return;
    const rows = await sql`SELECT * FROM syllabi ORDER BY course_slug`;
    return res.status(200).json({ rows });
  }

  if (req.method === 'GET') {
    const slug = req.query.slug;
    if (!slug) return res.status(400).json({ error: 'slug required' });
    const [row] = await sql`SELECT storage_url FROM syllabi WHERE course_slug = ${slug}`;
    if (!row) return res.status(404).json({ error: 'No syllabus uploaded for this course yet' });
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=3600');
    return res.redirect(302, row.storage_url);
  }

  if (requireAuth(req, res)) return;
  if (req.method === 'DELETE') {
    await sql`DELETE FROM syllabi WHERE course_slug = ${req.query.slug}`;
    return res.status(200).json({ ok: true });
  }
  return res.status(405).json({ error: 'method' });
}
