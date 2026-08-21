import { sql, requireAuth, hashIp } from './_lib.js';

/* POST is PUBLIC — every lead-capture point on the site posts here.
   GET / PATCH are gated behind an admin session. */
export default async function handler(req, res) {

  // ------------------------------------------------------------ capture
  if (req.method === 'POST') {
    const b = req.body || {};
    if (b.company_website) return res.status(200).json({ ok: true });   // honeypot

    const key = hashIp(req);
    const [rl] = await sql`
      INSERT INTO rate_limit (key) VALUES (${key})
      ON CONFLICT (key) DO UPDATE SET
        hits = CASE WHEN rate_limit.window_at < now() - interval '10 minutes'
                    THEN 1 ELSE rate_limit.hits + 1 END,
        window_at = CASE WHEN rate_limit.window_at < now() - interval '10 minutes'
                    THEN now() ELSE rate_limit.window_at END
      RETURNING hits`;
    if (rl.hits > 12) return res.status(429).json({ error: 'rate limited' });

    const phone = String(b.phone || '').replace(/\D/g, '');
    if (!b.name || phone.length < 10) {
      return res.status(400).json({ error: 'name and a 10-digit mobile are required' });
    }

    const [row] = await sql`
      INSERT INTO leads (source,name,phone,email,stage,background,goal,interest,course,
                         recommended,slot_day,slot_time,slot_channel,message,utm,page,ip_hash)
      VALUES (${b.source || 'unknown'}, ${b.name}, ${phone}, ${b.email || null},
              ${b.stage || null}, ${b.background || null}, ${b.goal || null},
              ${b.interest || null}, ${b.course || null}, ${b.recommended || null},
              ${b.slot_day || null}, ${b.slot_time || null}, ${b.slot_channel || null},
              ${b.message || null}, ${JSON.stringify(b.utm || {})}, ${b.page || null},
              ${key})
      RETURNING id, created_at`;
    return res.status(201).json({ ok: true, id: row.id });
  }

  if (requireAuth(req, res)) return;

  // -------------------------------------------------------------- listing
  if (req.method === 'GET') {
    const { q = '', source = '', status = '', from = '', to = '', format = '' } = req.query;
    const rows = await sql`
      SELECT * FROM leads
      WHERE (${q} = '' OR name ILIKE ${'%' + q + '%'} OR phone ILIKE ${'%' + q + '%'}
             OR email ILIKE ${'%' + q + '%'} OR course ILIKE ${'%' + q + '%'})
        AND (${source} = '' OR source = ${source})
        AND (${status} = '' OR status = ${status})
        AND (${from} = '' OR created_at >= ${from}::timestamptz)
        AND (${to} = ''   OR created_at <= ${to}::timestamptz)
      ORDER BY created_at DESC LIMIT 2000`;

    if (format === 'csv') {
      const cols = ['id','created_at','source','name','phone','email','stage','background',
                    'goal','course','recommended','slot_day','slot_time','slot_channel','status','notes'];
      const esc = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
      const csv = [cols.join(','), ...rows.map(r => cols.map(c => esc(r[c])).join(','))].join('\n');
      res.setHeader('Content-Type', 'text/csv; charset=utf-8');
      res.setHeader('Content-Disposition',
        `attachment; filename="cadd-leads-${new Date().toISOString().slice(0,10)}.csv"`);
      return res.status(200).send('\uFEFF' + csv);   // BOM so Excel reads UTF-8
    }
    return res.status(200).json({ rows });
  }

  // ------------------------------------------------------------- updating
  if (req.method === 'PATCH') {
    const { id, status, notes } = req.body || {};
    if (!id) return res.status(400).json({ error: 'id required' });
    await sql`UPDATE leads SET status = COALESCE(${status}, status),
                               notes  = COALESCE(${notes}, notes)
              WHERE id = ${id}`;
    return res.status(200).json({ ok: true });
  }

  return res.status(405).json({ error: 'method' });
}
