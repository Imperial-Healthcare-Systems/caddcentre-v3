# Admin portal — stack, security and setup

The marketing site stays a zero-dependency static build. **Only `/admin` and
`/api/*` move off static hosting.** Nothing else changes.

## Why this cannot be done client-side

A password check in client JavaScript on a static site is bypassed by
View Source. Authentication has to happen somewhere the visitor cannot read,
which means a server. That is the only reason a backend is introduced.

## Minimal stack

| Layer | Choice | Why |
|---|---|---|
| Hosting | **Vercel** (or Netlify) | Already the deploy target; serverless functions need no separate server |
| Functions | Vercel Functions (Node 20) | `api/*.js` deploys automatically, no config |
| Database | **Neon** serverless Postgres | HTTP driver works from serverless with no connection pooling problem. Free tier is ample |
| Auth | Signed HTTP-only cookie, HMAC-SHA256 | No dependency, no user table — one operator |
| Rebuilds | Vercel Deploy Hook | Publishing an article triggers the static rebuild |

Total added dependencies: **one** (`@neondatabase/serverless`).

## Setup

```bash
npm i @neondatabase/serverless
psql "$DATABASE_URL" -f db/schema.sql
```

Environment variables (Vercel → Settings → Environment Variables):

| Variable | Notes |
|---|---|
| `DATABASE_URL` | Neon connection string |
| `ADMIN_PASSWORD` | The admin password. **Never committed, never in client JS** |
| `SESSION_SECRET` | 32+ random bytes: `openssl rand -base64 32` |
| `DEPLOY_HOOK_URL` | Vercel deploy hook, fired on publish |

Add to `vercel.json` so `/admin` is never indexed:

```json
{ "headers": [ { "source": "/admin(.*)",
    "headers": [{ "key": "X-Robots-Tag", "value": "noindex, nofollow" }] } ] }
```

## Security posture

- Password is compared in **constant time** against an environment variable
- Session cookie: `HttpOnly; Secure; SameSite=Strict`, 8-hour expiry, HMAC-signed
- Login is rate limited (8 attempts / 15 min) with a 400ms delay on failure
- `POST /api/leads` is public by necessity — protected by a honeypot field,
  a per-IP-hash rate limit (12 / 10 min) and server-side validation
- IPs are stored **hashed**, never raw
- All queries are parameterised via the driver's tagged templates
- `/admin` and `/api` are excluded from `sitemap.xml` and marked `noindex`

## Leads dashboard

Captures from every lead point: enquiry modal, contact form multi-step,
counselling scheduler, corporate form, and Career Path Finder (including the
recommended path). Search by name/phone/email/course; filter by source, status
and date range; inline status and notes editing; **CSV export** with a UTF-8
BOM so Excel opens it correctly.

Client-side capture fails soft — if the API is unreachable the visitor still
sees their recommendation. A lead is never lost to a broken form.

## Blog: static regeneration, not dynamic serving

**Decision: statically regenerated through the existing `build.py`.**

Reasoning: `/insights/` is an SEO surface. Serving it dynamically from the
database would add per-request latency and cost the Core Web Vitals margin the
whole build is designed around. Articles change rarely; visitors read them
constantly. Static wins on both.

Flow:

```
Publish in /admin
   -> POST /api/posts writes to the database
   -> fires DEPLOY_HOOK_URL
   -> Vercel rebuilds
   -> build.py fetches GET /api/posts?published=1
   -> generates /insights/<slug>/ as static HTML
   -> live in 1-2 minutes
```

`build_pages3.py` reads `ARTICLES` from that endpoint when `POSTS_API` is set,
merging published posts ahead of the built-in ones. With no `POSTS_API`, or if
the API is unreachable, the build logs a notice and continues with the
built-in articles — a broken backend can never break a deploy.

Set it on the build:

```
POSTS_API=https://caddcentregurugram.com/api/posts?published=1
```

Verified end to end locally: publish in `/admin` -> `POSTS_API` rebuild ->
`/insights/<slug>/` generated, listed on `/insights/`, present in
`sitemap.xml`, with its own title and meta description.

Trade-off, stated plainly: **publishing is not instant.** If the client needs
instant publishing, the alternative is a dynamic route with ISR
(`revalidate: 60`), which requires moving `/insights/` to a framework-rendered
route. That is a larger change and, for a centre publishing a couple of
articles a month, not worth it.

## What is NOT included

- Multi-user accounts or roles — one operator, one password
- WYSIWYG editing — Markdown, because it round-trips cleanly into the build
- Media uploads — images go through `build_images.py`; adding uploads means
  adding object storage, which should be a separate decision
- Email/WhatsApp notification on new lead — trivial to add as a webhook in
  `api/leads.js`, but needs the client's provider chosen first

---

## Uploads (syllabi and article media)

**20 MB cap, enforced in three places:** the browser checks `file.size` before
sending, the local server streams with a hard limit and answers `413`, and the
production token is issued with `maximumSizeInBytes`.

**Syllabi are PDF-only, verified by content not filename.** A file called
`x.pdf` whose bytes do not start with `%PDF-` is rejected `415`.

### Vercel's body limit

Serverless functions cap request bodies at roughly **4.5 MB**, so a 20 MB file
cannot be proxied through one. `api/upload.js` therefore uses **client-direct
upload**: the browser requests a short-lived token, uploads straight to Blob
storage, and the function records the result. The function never handles the
bytes — it authorises, constrains and records.

```bash
npm i @vercel/blob
# Vercel -> Storage -> create a Blob store; BLOB_READ_WRITE_TOKEN is set for you
```

The local `serve.js` accepts the bytes directly and writes to `data/uploads/`,
so the flow is testable without any cloud account.

### Download behaviour

Every "Download syllabus" button points at `/api/syllabus?slug=<course>`, which
302-redirects to the stored PDF. A course with no syllabus returns a clear
`404` message rather than a broken file.

## Videos on Life @ CADD

Add a title and any `https` URL in the admin's **Videos** tab. Recognised:

| Pasted | Rendered as |
|---|---|
| `youtube.com/watch?v=…`, `youtu.be/…`, `/shorts/…` | privacy-enhanced YouTube embed |
| `vimeo.com/…` | Vimeo player |
| `….mp4` / `.webm` / `.mov` / `.m3u8` on any CDN | native `<video>` |

Build with `VIDEOS_API=https://…/api/videos?published=1`. With no
`VIDEOS_API`, the page falls back to the existing testimonial film.
