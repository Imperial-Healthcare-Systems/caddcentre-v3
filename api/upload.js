import { handleUpload } from '@vercel/blob/client';
import { sql, sessionFrom } from './_lib.js';

/**
 * Client-direct upload.
 *
 * Vercel serverless functions cap request bodies at ~4.5 MB, so a 20 MB
 * syllabus cannot be streamed through a function. Instead the browser asks
 * this endpoint for a short-lived token and uploads straight to Blob storage.
 * This function never sees the bytes — it authorises, constrains and records.
 */
const MAX = 20 * 1024 * 1024;

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'method' });

  try {
    const body = await handleUpload({
      request: req,
      body: req.body,

      // Called before a token is issued. Session is checked HERE, so an
      // anonymous visitor can never obtain upload credentials.
      onBeforeGenerateToken: async (pathname, clientPayload) => {
        if (!sessionFrom(req)) throw new Error('unauthorised');
        const meta = JSON.parse(clientPayload || '{}');
        const isSyllabus = meta.kind === 'syllabus';
        if (isSyllabus && !/\.pdf$/i.test(pathname)) throw new Error('Syllabus must be a PDF');
        return {
          allowedContentTypes: isSyllabus
            ? ['application/pdf']
            : ['application/pdf', 'image/png', 'image/jpeg', 'image/webp',
               'image/avif', 'image/svg+xml'],
          maximumSizeInBytes: MAX,
          tokenPayload: clientPayload || '{}',
        };
      },

      // Called by Blob storage once the upload completes.
      onUploadCompleted: async ({ blob, tokenPayload }) => {
        const meta = JSON.parse(tokenPayload || '{}');
        if (meta.kind === 'syllabus' && meta.slug) {
          await sql`INSERT INTO syllabi (course_slug, filename, size_bytes, storage_url)
                    VALUES (${meta.slug}, ${blob.pathname}, ${blob.size || 0}, ${blob.url})
                    ON CONFLICT (course_slug) DO UPDATE SET
                      filename = EXCLUDED.filename, size_bytes = EXCLUDED.size_bytes,
                      storage_url = EXCLUDED.storage_url, uploaded_at = now()`;
        } else {
          await sql`INSERT INTO media (filename, mime, size_bytes, storage_url)
                    VALUES (${blob.pathname}, ${blob.contentType || ''},
                            ${blob.size || 0}, ${blob.url})`;
        }
      },
    });
    return res.status(200).json(body);
  } catch (e) {
    return res.status(e.message === 'unauthorised' ? 401 : 400)
              .json({ error: e.message || 'upload failed' });
  }
}
