# Google reviews on the homepage

Two layers, and only one of them needs to work:

1. **Live** — `/api/reviews` ([api/reviews.js](../api/reviews.js)) reads the
   Business Profile through the Places API **server-side**, so the key is never
   in the page. `initReviews()` in `assets/js/main.js` calls it on load and
   replaces the cards, the score, the count and the "All reviews" link with
   whatever Google says right now. Responses are edge-cached for six hours.
2. **Pre-rendered fallback** — the same cards are written into the HTML from
   `src/data/reviews.json` by `src/build_reviews.py`, so the section is complete
   before any JavaScript runs (good for first paint and for crawlers). If the
   API is down, the key is missing, or JS never loads, the visitor sees this and
   nothing looks broken.

Right now `reviews.json` is marked `"source": "seed"` — 4.9 from 207 reviews and
three quotes taken from the listing by hand. Setting `GOOGLE_MAPS_API_KEY` turns
on layer 1 immediately; running `--fetch` refreshes layer 2.

## One-time: get an API key

1. Go to <https://console.cloud.google.com/> and create a project
   (e.g. *caddcentre-website*). A billing account is required even though this
   usage sits inside the free monthly credit.
2. **APIs & Services → Library →** enable **Places API (New)**.
3. **APIs & Services → Credentials → Create credentials → API key.**
4. Click the new key → **Restrict key**:
   - *Application restrictions*: **None** (the key is only used from the
     serverless function and from your machine, never from a browser — do not
     commit it).
   - *API restrictions*: **Restrict key → Places API (New)**.
5. Keep the key in a password manager.

## Turning on the live endpoint

Vercel → project → **Settings → Environment Variables**:

| Variable | Value |
|---|---|
| `GOOGLE_MAPS_API_KEY` | the key from above |
| `GOOGLE_PLACE_ID` | optional; skips the lookup call. The function resolves and caches it otherwise |

Redeploy, then check it:

```bash
curl -s https://<your-domain>/api/reviews | head -c 400
```

Expected: `{"rating":4.9,"ratingCount":…,"reviewsUrl":"…","reviews":[…]}`.
`503` means the env var is missing; `502` means Google rejected the call and the
message says why. Either way the homepage keeps its pre-rendered cards.

Cost: one Places call per six hours per edge region — a few dozen a month,
inside the free credit. Place Details with `reviews` is the Enterprise SKU, so
do not drop the cache header.

## Refreshing the pre-rendered fallback

```bash
# fetch from Google, then write the section into index.html and src/preview.html
GOOGLE_MAPS_API_KEY=AIza... python3 src/build_reviews.py --fetch --render

# re-render from the cached JSON (no network, no key)
python3 src/build_reviews.py --render
```

The first `--fetch` resolves the Place ID for "CADD Centre Gurugram Sector 14"
via Text Search and prints the matched name and address — check it is the
Sector 14 listing. It then stores the ID in `reviews.json`. To pin it yourself:

```bash
GOOGLE_PLACE_ID=ChIJ... GOOGLE_MAPS_API_KEY=AIza... python3 src/build_reviews.py --fetch --render
```

Commit the changed `src/data/reviews.json`, `index.html` and
`src/preview.html` as normal.

### Keeping it current

Google's terms ask that review content is not cached indefinitely and that the
rating, the author and a link back to Google are shown together. A weekly
refresh satisfies that. Either a local cron entry:

```cron
0 6 * * 1 cd /path/to/caddcentre && GOOGLE_MAPS_API_KEY=AIza... python3 src/build_reviews.py --fetch --render
```

…or a GitHub Action with the key in `secrets.GOOGLE_MAPS_API_KEY`:

```yaml
on:
  schedule: [{cron: "0 6 * * 1"}]
  workflow_dispatch:
jobs:
  reviews:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 src/build_reviews.py --fetch --render
        env: {GOOGLE_MAPS_API_KEY: "${{ secrets.GOOGLE_MAPS_API_KEY }}"}
      - run: |
          git config user.name  "reviews-bot"
          git config user.email "bot@users.noreply.github.com"
          git commit -am "Refresh Google reviews" || echo "no change"
          git push
```

## What the section shows

- The rating and review count, and the same numbers in the hero trust strip.
- One card per review in a horizontal carousel: reviewer avatar with the Google
  mark, name, Google's own "1 year ago" phrasing, gold stars, a verified tick,
  and the quote. Every fetched review gets a card — the Places API returns the
  **five most recent** for a place, not all 207, so "Read all N reviews on
  Google" covers the rest.
- The avatar uses the reviewer's Google photo when the API supplies one
  (`photo` in the JSON), otherwise their initial on a colour derived from the
  name.
- Long quotes are clamped to five lines, and `initReviews()` in
  `assets/js/main.js` adds a "Read more" toggle to the ones that actually
  overflow. The track scrolls natively, so swipe, trackpad and keyboard work
  with JS off; the arrows are the enhancement and hide themselves when all the
  cards already fit.

### Styling

`.grr*` rules live at the end of `assets/css/main.css` (mirrored in
`src/assets/css/main.css`). Gold stars and the blue tick are deliberately
Google's colours rather than the site accent, so the rating reads as theirs.

## Deliberately not done

No `aggregateRating` structured data was added. Google's review-snippet
guidelines do not allow a business to mark up its own ratings on its own site,
and doing it risks a manual action against the domain. The visible section is
unaffected.

## If you want all 207 reviews

That needs the **Google Business Profile API** (`accounts.locations.reviews`),
which works on locations you own: it requires OAuth as the profile owner plus
Google's approval of API access for the project, which takes a few days. The
fetch step in `build_reviews.py` is the only piece that would change — the JSON
shape and the rendering stay as they are.
