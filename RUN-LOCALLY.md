# Running the site and admin locally

The marketing site is static and opens by double-clicking. **The admin portal
is not** — it needs a server, because authentication that lives in client
JavaScript can be read with View Source.

`serve.js` gives you the full admin on your own machine: no database, no
hosting account, no npm install. Data is stored in `data/local-db.json`.

## Start it

Requires Node 18 or newer.

```bash
cd cadd-centre-gurugram
ADMIN_PASSWORD='VGT@2026' node serve.js
```

Windows PowerShell:

```powershell
$env:ADMIN_PASSWORD='VGT@2026'; node serve.js
```

Then open:

| | |
|---|---|
| Site | http://localhost:8080/ |
| **Admin** | **http://localhost:8080/admin/** |

Sign in with whatever you set `ADMIN_PASSWORD` to.

## Why `/admin` did not work before

1. **No password existed.** `ADMIN_PASSWORD` is read from the environment at
   runtime. Nothing is hardcoded — that is deliberate, and it is why the
   password has to be supplied when starting the server.
2. **No server was running.** `/admin` calls `/api/login`. Opening the files
   from disk or from a static host means those endpoints return 404.
3. **`preview.html` has no `/admin` route at all.** It is the single-file
   marketing preview only.

## What works locally

- Sign in / sign out, 8-hour signed session cookie
- Leads dashboard: search, filters, inline status and notes, CSV export
- Lead capture from every form on the site writes straight to the dashboard
- Article create / edit / publish / unpublish

Verified end to end:

```
login wrong password        401
login VGT@2026              200  + session cookie
/api/leads no session       401
/api/leads with session     200
public lead capture         201
short phone rejected        400
honeypot silently dropped   200 (not stored)
CSV export                  headers + row, UTF-8 BOM
publish article             200, appears in published feed
pages /, /admin/, course    200   unknown path 404
```

## Going to production

Local storage is a JSON file — fine for testing, not for live. For production
follow `ADMIN-SETUP.md`: Vercel Functions + Neon Postgres, with
`ADMIN_PASSWORD`, `SESSION_SECRET`, `DATABASE_URL` and `DEPLOY_HOOK_URL` set as
environment variables. The `api/*.js` files are already written for that.

**Choose a stronger password for production**, set it only as an environment
variable, and never commit it.
