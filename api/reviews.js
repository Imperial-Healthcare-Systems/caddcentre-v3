/* Public GET /api/reviews — live Google Business Profile rating and reviews.

   The key stays here: the browser never sees it, so the only thing a visitor
   can do with this endpoint is read the same reviews Google shows publicly.
   Responses are edge-cached for six hours, which keeps the numbers current,
   keeps quota to a few calls a day, and satisfies Google's rule against
   caching review content indefinitely.

   Env: GOOGLE_MAPS_API_KEY (required), GOOGLE_PLACE_ID (optional — resolved
   from the business name and cached in module scope when absent).

   The homepage renders its reviews from src/data/reviews.json at build time,
   so a failure here is invisible: the client keeps the markup it was served. */

const PLACE_QUERY = 'CADD Centre Gurugram Sector 14';
const API = 'https://places.googleapis.com/v1';

let cachedPlaceId = process.env.GOOGLE_PLACE_ID || '';

async function call(url, key, fieldMask, body) {
  const r = await fetch(url, {
    method: body ? 'POST' : 'GET',
    headers: {
      'X-Goog-Api-Key': key,
      'X-Goog-FieldMask': fieldMask,
      ...(body ? { 'Content-Type': 'application/json' } : {})
    },
    body: body ? JSON.stringify(body) : undefined
  });
  if (!r.ok) throw new Error(`places ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return r.json();
}

async function placeId(key) {
  if (cachedPlaceId) return cachedPlaceId;
  const res = await call(`${API}/places:searchText`, key, 'places.id',
    { textQuery: PLACE_QUERY, languageCode: 'en', maxResultCount: 1 });
  cachedPlaceId = (res.places && res.places[0] && res.places[0].id) || '';
  if (!cachedPlaceId) throw new Error('place not found');
  return cachedPlaceId;
}

export default async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'method' });

  const key = process.env.GOOGLE_MAPS_API_KEY;
  if (!key) return res.status(503).json({ error: 'GOOGLE_MAPS_API_KEY not configured' });

  try {
    const id = await placeId(key);
    const p = await call(`${API}/places/${id}?languageCode=en`, key,
      'id,rating,userRatingCount,googleMapsUri,reviews');

    const reviews = (p.reviews || []).map((r) => ({
      author: (r.authorAttribution && r.authorAttribution.displayName) || 'Google reviewer',
      photo: (r.authorAttribution && r.authorAttribution.photoUri) || '',
      rating: r.rating || 5,
      when: r.relativePublishTimeDescription || '',
      text: ((r.text || r.originalText || {}).text || '').trim()
    })).filter((r) => r.text);

    // Six hours at the edge; a stale copy is served for a day while it refreshes.
    res.setHeader('Cache-Control', 'public, s-maxage=21600, stale-while-revalidate=86400');
    return res.status(200).json({
      rating: p.rating || null,
      ratingCount: p.userRatingCount || null,
      reviewsUrl: p.googleMapsUri || '',
      reviews
    });
  } catch (e) {
    // Nothing to recover from: the visitor already has the pre-rendered cards.
    return res.status(502).json({ error: String(e.message || e) });
  }
}
