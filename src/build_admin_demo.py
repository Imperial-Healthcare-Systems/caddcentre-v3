# -*- coding: utf-8 -*-
"""
Demo admin for the single-file preview.

The preview has no server, so the real admin cannot run in it. This is a
faithful VISUAL demo of the admin, driven by sample data held in memory.

It is explicitly NOT a security boundary and never pretends to be one:
  - any password is accepted, and the screen says so
  - the data is invented and labelled as such
  - nothing is stored, sent or retrieved

The real admin (dist/admin/ + api/) verifies the password server-side against
an environment variable. That is the version that gets deployed.
"""


def page_admin_demo(mode, depth=0):
    return """
<main id="main">
<section class="section section--tight">
  <div class="wrap">

    <div class="note mb-6" style="border-left-color:var(--c-accent)">
      <strong>Demo view.</strong> This is the admin interface running inside the offline preview,
      so you can see how it works without deploying anything. The data below is invented, nothing
      is saved, and <strong>any password is accepted here</strong>. The live admin verifies the
      password on the server and reads real submissions from the database &mdash; see
      <code>RUN-LOCALLY.md</code> to run that version.
    </div>

    <!-- LOGIN -->
    <section id="dlogin" style="max-width:min(380px,100%)">
      <p class="label label--accent">CADD Centre Gurugram</p>
      <h1 class="t-h2 mt-2 mb-3">Admin</h1>
      <div class="field">
        <label for="dpw">Password</label>
        <input id="dpw" type="password" placeholder="anything works in this demo">
      </div>
      <button class="btn btn--primary btn--wide" id="dlogin-btn" type="button">Sign in</button>
      <p class="t-small t-muted mt-3">Live version: 8-hour signed session, password checked
        server-side against an environment variable.</p>
    </section>

    <!-- APP -->
    <div id="dapp" hidden>
      <div class="flex jcb aic wrapf gap-2 mb-4" style="border-bottom:1px solid var(--c-border);padding-bottom:var(--s-2)">
        <div class="flex gap-1">
          <button class="chip" data-dtab="leads" aria-pressed="true">Leads</button>
          <button class="chip" data-dtab="posts" aria-pressed="false">Articles</button>
          <button class="chip" data-dtab="syllabus" aria-pressed="false">Syllabi</button>
          <button class="chip" data-dtab="videos" aria-pressed="false">Videos</button>
        </div>
        <div class="flex gap-2 aic">
          <span class="label" id="dstat"></span>
          <button class="btn btn--ghost" id="dlogout" type="button">Sign out</button>
        </div>
      </div>

      <!-- LEADS -->
      <section data-dpanel="leads">
        <div class="filters mb-3">
          <input id="dq" type="search" placeholder="Search name, phone, course"
                 style="min-height:40px;padding:8px 10px;border:1px solid var(--c-border);border-radius:var(--r-sm);font:inherit">
          <button class="chip" data-dfilter="all" aria-pressed="true">All</button>
          <button class="chip" data-dfilter="contact_form" aria-pressed="false">Contact form</button>
          <button class="chip" data-dfilter="career_finder" aria-pressed="false">Career finder</button>
          <button class="chip" data-dfilter="enquiry_modal" aria-pressed="false">Enquiry modal</button>
          <button class="chip" data-dfilter="corporate" aria-pressed="false">Corporate</button>
          <button class="btn btn--secondary" id="dcsv" type="button">Export CSV</button>
        </div>
        <table class="tbl">
          <thead><tr><th>When</th><th>Name</th><th>Phone</th><th>Source</th>
            <th>Background</th><th>Recommended</th><th>Slot</th><th>Status</th></tr></thead>
          <tbody id="drows"></tbody>
        </table>
      </section>

      <!-- POSTS -->
      <section data-dpanel="posts" hidden>
        <div class="grid g-2">
          <div>
            <div class="field"><label for="dpt">Title</label>
              <input id="dpt" type="text" value="BIM engineer salary in India"></div>
            <div class="field"><label for="dpb">Body (Markdown)</label>
              <textarea id="dpb" rows="14" style="font-family:var(--f-mono);font-size:.8125rem">## What the numbers actually look like

Salary data for BIM roles in India is noisy, because the job title covers
three quite different levels of responsibility...</textarea></div>
          </div>
          <div>
            <div class="field"><label for="dps">Slug</label>
              <input id="dps" type="text" value="bim-engineer-salary-india"></div>
            <div class="field"><label for="dpg">Tag</label><input id="dpg" type="text" value="BIM"></div>
            <div class="field"><label for="dpe">Excerpt</label>
              <textarea id="dpe" rows="3">What BIM roles actually pay in India, by level.</textarea></div>
            <div class="field">
              <label for="dpf">Attach a file (max 20 MB)</label>
              <input id="dpf" type="file">
              <span class="field__help">Uploads and inserts a Markdown link into the body.</span>
            </div>
            <div class="flex fcol gap-1">
              <button class="btn btn--ghost btn--wide" type="button" data-dupload>Upload file</button>
              <button class="btn btn--ghost btn--wide" type="button" data-dsave="draft">Save draft</button>
              <button class="btn btn--primary btn--wide" type="button" data-dsave="published">Publish</button>
            </div>
            <p class="t-small t-muted mt-3">Live version: publishing writes to the database and
              triggers a rebuild, so the article appears on News in a minute or two.</p>
            <div class="note mt-3" id="dpmsg" hidden></div>
          </div>
        </div>
      </section>

      <!-- SYLLABI -->
      <section data-dpanel="syllabus" hidden>
        <div class="filters mb-3">
          <input id="dsq" type="search" placeholder="Filter courses"
                 style="min-height:40px;padding:8px 10px;border:1px solid var(--c-border);border-radius:var(--r-sm);font:inherit">
          <span class="label" id="dsstat"></span>
        </div>
        <div class="note mb-3" id="dsmsg" hidden></div>
        <table class="tbl"><thead><tr>
          <th>Course</th><th>Current syllabus</th><th>Size</th><th>Uploaded</th>
          <th>Replace (PDF, max 20&nbsp;MB)</th></tr></thead>
          <tbody id="dsrows"></tbody></table>
      </section>

      <!-- VIDEOS -->
      <section data-dpanel="videos" hidden>
        <div class="filters mb-3">
          <input id="dvt" type="text" placeholder="Title, e.g. CADD Quest 2026 highlights"
                 style="min-height:40px;padding:8px 10px;border:1px solid var(--c-border);border-radius:var(--r-sm);font:inherit;min-width:240px">
          <input id="dvu" type="url" placeholder="https://youtube.com/watch?v=... or any https CDN URL"
                 style="min-height:40px;padding:8px 10px;border:1px solid var(--c-border);border-radius:var(--r-sm);font:inherit;min-width:300px">
          <button class="btn btn--primary" id="dvadd" type="button">Add video</button>
        </div>
        <div class="note mb-3" id="dvmsg" hidden></div>
        <p class="t-small t-muted mb-3">YouTube, Vimeo and direct MP4 URLs are all accepted, and are
          detected automatically. These appear on Life&nbsp;@&nbsp;CADD after the next rebuild.</p>
        <table class="tbl"><thead><tr><th>#</th><th>Title</th><th>URL</th><th>Type</th><th>Status</th><th></th></tr></thead>
          <tbody id="dvrows"></tbody></table>
      </section>
    </div>

  </div>
</section>
</main>

<script>
(function () {
  var LEADS = [
    {t:'13 Aug, 11:42', n:'Rohit Sharma',  p:'98••••3210', s:'career_finder', b:'Civil',      r:'BIM & Digital Construction', d:'Tomorrow, 4–6 pm, WhatsApp', st:'new'},
    {t:'13 Aug, 10:18', n:'Ananya Verma',  p:'99••••4471', s:'contact_form',  b:'Architecture', r:'Architecture & Visualisation', d:'Today, 2–4 pm, Phone', st:'contacted'},
    {t:'12 Aug, 18:05', n:'Imran Qureshi', p:'70••••8890', s:'enquiry_modal', b:'Mechanical', r:'Mechanical & Product Design', d:'—', st:'booked'},
    {t:'12 Aug, 16:33', n:'Priya Nair',    p:'88••••1204', s:'career_finder', b:'Civil',      r:'Civil & Infrastructure Design', d:'This weekend, 10–12, Visit', st:'new'},
    {t:'12 Aug, 12:57', n:'L&T — team of 14', p:'A. Menon', s:'corporate',   b:'—',          r:'Corporate: 2D to BIM migration', d:'—', st:'new'},
    {t:'11 Aug, 19:12', n:'Sahil Batra',   p:'96••••5518', s:'contact_form', b:'Electrical', r:'Electrical & MEP Design', d:'Tomorrow, 6–7 pm, WhatsApp', st:'enrolled'}
  ];
  var filter = 'all', q = '';

  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  function render() {
    var rows = LEADS.filter(function (l) {
      var okF = filter === 'all' || l.s === filter;
      var okQ = !q || (l.n + l.p + l.r).toLowerCase().indexOf(q) > -1;
      return okF && okQ;
    });
    var st = document.getElementById('dstat');
    if (st) st.textContent = rows.length + ' leads';
    var tb = document.getElementById('drows');
    if (!tb) return;
    tb.innerHTML = rows.map(function (l) {
      return '<tr>' +
        '<td data-l="When">' + esc(l.t) + '</td>' +
        '<td data-l="Name"><strong>' + esc(l.n) + '</strong></td>' +
        '<td data-l="Phone">' + esc(l.p) + '</td>' +
        '<td data-l="Source"><span class="tag">' + esc(l.s) + '</span></td>' +
        '<td data-l="Background">' + esc(l.b) + '</td>' +
        '<td data-l="Recommended">' + esc(l.r) + '</td>' +
        '<td data-l="Slot">' + esc(l.d) + '</td>' +
        '<td data-l="Status"><span class="tag">' + esc(l.st) + '</span></td>' +
      '</tr>';
    }).join('');
  }

  document.addEventListener('click', function (e) {
    var b;
    if ((b = e.target.closest('#dlogin-btn'))) {
      document.getElementById('dlogin').hidden = true;
      document.getElementById('dapp').hidden = false;
      render(); renderSyl(); renderVid();
    }
    if ((b = e.target.closest('#dlogout'))) {
      document.getElementById('dapp').hidden = true;
      document.getElementById('dlogin').hidden = false;
    }
    if ((b = e.target.closest('[data-dtab]'))) {
      var t = b.getAttribute('data-dtab');
      Array.prototype.forEach.call(document.querySelectorAll('[data-dtab]'), function (x) {
        x.setAttribute('aria-pressed', String(x === b)); });
      Array.prototype.forEach.call(document.querySelectorAll('[data-dpanel]'), function (p) {
        p.hidden = p.getAttribute('data-dpanel') !== t; });
      if (t === 'syllabus') renderSyl();
      if (t === 'videos') renderVid();
    }
    if ((b = e.target.closest('[data-dfilter]'))) {
      filter = b.getAttribute('data-dfilter');
      Array.prototype.forEach.call(document.querySelectorAll('[data-dfilter]'), function (x) {
        x.setAttribute('aria-pressed', String(x === b)); });
      render();
    }
    if ((b = e.target.closest('#dcsv'))) {
      alert('In the live admin this downloads a CSV of the filtered leads.\\n\\n' +
            'The preview has no server, so the export is disabled here.');
    }
    if ((b = e.target.closest('[data-dupload]'))) {
      var m2 = document.getElementById('dpmsg'); m2.hidden = false;
      var f2 = (document.getElementById('dpf') || {}).files;
      if (!f2 || !f2[0]) { m2.innerHTML = '<strong>Choose a file first.</strong>'; return; }
      if (f2[0].size > 20 * 1024 * 1024) {
        m2.innerHTML = '<strong>Rejected:</strong> ' + (f2[0].size / 1048576).toFixed(1) +
          ' MB exceeds the 20 MB limit.';
        return;
      }
      m2.innerHTML = '<strong>Demo:</strong> ' + esc(f2[0].name) + ' passed the 20 MB check. ' +
        'In the live admin this uploads and inserts a Markdown link into the body.';
      return;
    }
    if ((b = e.target.closest('#dvadd'))) {
      var mv = document.getElementById('dvmsg'); mv.hidden = false;
      var t = document.getElementById('dvt').value, u = document.getElementById('dvu').value;
      if (!t || !u) { mv.innerHTML = '<strong>Title and URL are both required.</strong>'; return; }
      if (!/^https:\/\//i.test(u)) { mv.innerHTML = '<strong>Rejected:</strong> the URL must start with https://'; return; }
      VIDEOS.push({ i: VIDEOS.length + 1, t: t, u: u, k: vkind(u) });
      renderVid();
      document.getElementById('dvt').value = ''; document.getElementById('dvu').value = '';
      mv.innerHTML = '<strong>Added</strong> as ' + esc(vkind(u)) +
        '. In the live admin this appears on Life @ CADD after the next rebuild.';
      return;
    }
    if ((b = e.target.closest('[data-dsave]'))) {
      var m = document.getElementById('dpmsg');
      m.hidden = false;
      m.innerHTML = b.getAttribute('data-dsave') === 'published'
        ? '<strong>Demo:</strong> in the live admin this publishes the article and triggers a rebuild.'
        : '<strong>Demo:</strong> in the live admin this saves a draft.';
    }
  });

  /* ---- syllabi ---- */
  var COURSES = [
    ['revit-architecture','Revit Architecture','revit-architecture-syllabus.pdf','1.8 MB','12 Aug 2026'],
    ['civil-3d','Civil 3D','civil-3d-syllabus.pdf','2.4 MB','12 Aug 2026'],
    ['solidworks','SolidWorks',null,null,null],
    ['staad-pro','STAAD.Pro','staad-pro-syllabus.pdf','1.1 MB','09 Aug 2026'],
    ['catia','CATIA',null,null,null],
    ['primavera-ppm','Primavera P6 with PPM',null,null,null],
    ['autocad-electrical','AutoCAD Electrical','autocad-electrical-syllabus.pdf','980 KB','08 Aug 2026'],
    ['3d-printing','3D Printing & Prototyping',null,null,null]
  ];
  function renderSyl() {
    var f = (document.getElementById('dsq') || {}).value || '';
    f = f.toLowerCase();
    var list = COURSES.filter(function (c) { return !f || c[1].toLowerCase().indexOf(f) > -1; });
    var have = COURSES.filter(function (c) { return c[2]; }).length;
    var st = document.getElementById('dsstat');
    if (st) st.textContent = have + ' of ' + COURSES.length + ' shown courses have a syllabus';
    var tb = document.getElementById('dsrows');
    if (!tb) return;
    tb.innerHTML = list.map(function (c) {
      return '<tr>' +
        '<td data-l="Course"><strong>' + esc(c[1]) + '</strong><br><span class="t-muted">' + esc(c[0]) + '</span></td>' +
        '<td data-l="Syllabus">' + (c[2] ? '<a href="#admin">' + esc(c[2]) + '</a>' : '<span class="tag">none</span>') + '</td>' +
        '<td data-l="Size">' + (c[3] || '—') + '</td>' +
        '<td data-l="Uploaded">' + (c[4] || '—') + '</td>' +
        '<td data-l="Replace"><input type="file" accept="application/pdf" class="dsup" data-slug="' + esc(c[0]) + '"></td>' +
      '</tr>';
    }).join('');
    Array.prototype.forEach.call(document.querySelectorAll('.dsup'), function (i) {
      i.onchange = function () {
        var m = document.getElementById('dsmsg'); m.hidden = false;
        var fl = i.files[0];
        if (!fl) return;
        if (fl.size > 20 * 1024 * 1024) {
          m.innerHTML = '<strong>Rejected:</strong> ' + esc(fl.name) + ' is ' +
            (fl.size / 1048576).toFixed(1) + ' MB. The limit is 20 MB.';
          return;
        }
        if (!/\.pdf$/i.test(fl.name)) {
          m.innerHTML = '<strong>Rejected:</strong> the syllabus must be a PDF.';
          return;
        }
        m.innerHTML = '<strong>Demo:</strong> ' + esc(fl.name) + ' (' +
          (fl.size / 1048576).toFixed(1) + ' MB) passed the PDF and size checks. ' +
          'In the live admin this uploads and the Download syllabus button for this course goes live.';
      };
    });
  }

  /* ---- videos ---- */
  var VIDEOS = [
    {i:1, t:'Hear from our learners', u:'https://www.youtube.com/watch?v=FbJY_AvsFIk', k:'YouTube'},
    {i:2, t:'Inside the 3D printing lab', u:'https://cdn.example.com/media/lab-tour.mp4', k:'Direct MP4'}
  ];
  function vkind(u) {
    if (/youtube\.com|youtu\.be/i.test(u)) return 'YouTube';
    if (/vimeo\.com/i.test(u)) return 'Vimeo';
    if (/\.(mp4|webm|mov|m3u8)(\?|$)/i.test(u)) return 'Direct MP4';
    return 'Unrecognised';
  }
  function renderVid() {
    var tb = document.getElementById('dvrows');
    if (!tb) return;
    tb.innerHTML = VIDEOS.map(function (v) {
      return '<tr><td data-l="#">' + v.i + '</td>' +
        '<td data-l="Title"><strong>' + esc(v.t) + '</strong></td>' +
        '<td data-l="URL" style="overflow-wrap:anywhere">' + esc(v.u) + '</td>' +
        '<td data-l="Type"><span class="tag">' + esc(v.k) + '</span></td>' +
        '<td data-l="Status"><span class="tag">published</span></td>' +
        '<td><button class="btn btn--ghost dvdel" data-i="' + v.i + '" type="button">Remove</button></td></tr>';
    }).join('') || '<tr><td colspan="6" class="t-muted">No videos yet.</td></tr>';
    Array.prototype.forEach.call(document.querySelectorAll('.dvdel'), function (b) {
      b.onclick = function () {
        VIDEOS = VIDEOS.filter(function (v) { return String(v.i) !== b.dataset.i; });
        renderVid();
      };
    });
  }

  var qi = document.getElementById('dq');
  if (qi) qi.addEventListener('input', function () { q = this.value.toLowerCase(); render(); });
  var sq = document.getElementById('dsq');
  if (sq) sq.addEventListener('input', renderSyl);
})();
</script>
"""
