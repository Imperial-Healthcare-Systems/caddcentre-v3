-- CADD Centre Gurugram — admin schema (PostgreSQL)
-- Apply once: psql "$DATABASE_URL" -f db/schema.sql

CREATE TABLE IF NOT EXISTS leads (
  id            BIGSERIAL PRIMARY KEY,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  source        TEXT NOT NULL,              -- enquiry_modal | contact_form | career_finder | first_job_pakka | corporate
  name          TEXT,
  phone         TEXT,
  email         TEXT,
  stage         TEXT,                       -- student | fresher | upskill | switch
  background    TEXT,                       -- civil | mech | arch | elec | other
  goal          TEXT,
  interest      TEXT,
  course        TEXT,                       -- course category or programme slug
  recommended   TEXT,                       -- path the finder returned
  slot_day      TEXT,
  slot_time     TEXT,
  slot_channel  TEXT,
  message       TEXT,
  utm           JSONB DEFAULT '{}'::jsonb,
  page          TEXT,
  status        TEXT NOT NULL DEFAULT 'new',-- new | contacted | booked | enrolled | lost
  notes         TEXT,
  ip_hash       TEXT
);
CREATE INDEX IF NOT EXISTS leads_created_idx ON leads (created_at DESC);
CREATE INDEX IF NOT EXISTS leads_status_idx  ON leads (status);
CREATE INDEX IF NOT EXISTS leads_source_idx  ON leads (source);

CREATE TABLE IF NOT EXISTS posts (
  id            BIGSERIAL PRIMARY KEY,
  slug          TEXT UNIQUE NOT NULL,
  title         TEXT NOT NULL,
  excerpt       TEXT,
  body_md       TEXT NOT NULL,
  tag           TEXT,
  hero_slot     TEXT,
  status        TEXT NOT NULL DEFAULT 'draft',  -- draft | published
  published_at  TIMESTAMPTZ,
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  seo_title     TEXT,
  seo_desc      TEXT
);
CREATE INDEX IF NOT EXISTS posts_status_idx ON posts (status, published_at DESC);

-- Rate limiting for the public lead endpoint
CREATE TABLE IF NOT EXISTS rate_limit (
  key        TEXT PRIMARY KEY,
  hits       INT NOT NULL DEFAULT 1,
  window_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------- uploads --
-- Course syllabi. One current file per course slug.
CREATE TABLE IF NOT EXISTS syllabi (
  course_slug  TEXT PRIMARY KEY,
  filename     TEXT NOT NULL,
  size_bytes   INT  NOT NULL,
  storage_url  TEXT NOT NULL,          -- object-storage URL (Vercel Blob / S3)
  uploaded_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Generic media for article bodies (images, PDFs).
CREATE TABLE IF NOT EXISTS media (
  id           BIGSERIAL PRIMARY KEY,
  filename     TEXT NOT NULL,
  mime         TEXT NOT NULL,
  size_bytes   INT  NOT NULL,
  storage_url  TEXT NOT NULL,
  uploaded_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Videos shown on Life @ CADD. Any YouTube / Vimeo / direct CDN URL.
CREATE TABLE IF NOT EXISTS videos (
  id           BIGSERIAL PRIMARY KEY,
  title        TEXT NOT NULL,
  url          TEXT NOT NULL,
  caption      TEXT,
  position     INT  NOT NULL DEFAULT 0,
  status       TEXT NOT NULL DEFAULT 'published',   -- draft | published
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS videos_pos_idx ON videos (status, position);
