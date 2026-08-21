import { sql, requireAuth } from './_lib.js';

/* GET ?published=1 is PUBLIC — the build pipeline reads it to regenerate
   /news/. Everything else requires an admin session. */
export default async function handler(req, res) {

  if (req.method === 'GET' && req.query.published === '1') {
    const rows = await sql`
      SELECT slug,title,excerpt,body_md,tag,hero_slot,published_at,seo_title,seo_desc
      FROM posts WHERE status = 'published'
      ORDER BY published_at DESC`;
    res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=600');
    return res.status(200).json({ rows });
  }

  if (requireAuth(req, res)) return;

  if (req.method === 'GET') {
    const rows = await sql`SELECT * FROM posts ORDER BY updated_at DESC`;
    return res.status(200).json({ rows });
  }

  if (req.method === 'POST' || req.method === 'PUT') {
    const b = req.body || {};
    if (!b.slug || !b.title || !b.body_md) {
      return res.status(400).json({ error: 'slug, title and body are required' });
    }
    const slug = String(b.slug).toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-|-$/g, '');
    const [row] = await sql`
      INSERT INTO posts (slug,title,excerpt,body_md,tag,hero_slot,status,seo_title,seo_desc,
                         published_at,updated_at)
      VALUES (${slug}, ${b.title}, ${b.excerpt || null}, ${b.body_md}, ${b.tag || null},
              ${b.hero_slot || null}, ${b.status || 'draft'}, ${b.seo_title || null},
              ${b.seo_desc || null},
              ${b.status === 'published' ? new Date().toISOString() : null}, now())
      ON CONFLICT (slug) DO UPDATE SET
        title = EXCLUDED.title, excerpt = EXCLUDED.excerpt, body_md = EXCLUDED.body_md,
        tag = EXCLUDED.tag, hero_slot = EXCLUDED.hero_slot, status = EXCLUDED.status,
        seo_title = EXCLUDED.seo_title, seo_desc = EXCLUDED.seo_desc,
        published_at = COALESCE(posts.published_at, EXCLUDED.published_at),
        updated_at = now()
      RETURNING slug, status`;

    // Publishing or unpublishing changes what the static build should contain.
    if (process.env.DEPLOY_HOOK_URL && (b.status === 'published' || b.rebuild)) {
      try { await fetch(process.env.DEPLOY_HOOK_URL, { method: 'POST' }); } catch (e) {}
    }
    return res.status(200).json({ ok: true, ...row });
  }

  if (req.method === 'DELETE') {
    const { slug } = req.query;
    if (!slug) return res.status(400).json({ error: 'slug required' });
    await sql`DELETE FROM posts WHERE slug = ${slug}`;
    if (process.env.DEPLOY_HOOK_URL) {
      try { await fetch(process.env.DEPLOY_HOOK_URL, { method: 'POST' }); } catch (e) {}
    }
    return res.status(200).json({ ok: true });
  }

  return res.status(405).json({ error: 'method' });
}
