/* ==========================================================================
   CADD Centre Gurugram — site behaviour
   No dependencies. Progressive enhancement: every control degrades to a link
   or a native form control if this file fails to load.
   ========================================================================== */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- Mega menu
     Opens on click (not hover) so it works on touch and for keyboard users. */
  function initMega() {
    var triggers = $$('[data-mega-trigger]');
    var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    function panelOf(t) { return document.getElementById(t.getAttribute('aria-controls')); }

    function closeAll(except) {
      triggers.forEach(function (t) {
        if (t === except) return;
        t.setAttribute('aria-expanded', 'false');
        var p = panelOf(t);
        if (p) p.setAttribute('data-open', 'false');
      });
    }
    function open(t) {
      var p = panelOf(t);
      if (!p) return;
      closeAll(t);
      t.setAttribute('aria-expanded', 'true');
      p.setAttribute('data-open', 'true');
    }

    triggers.forEach(function (t) {
      var panel = panelOf(t);
      if (!panel) return;
      var item = t.closest('.nav__item') || t;

      if (canHover) {
        // Hover opens it; the click is left alone so the link can do its job.
        item.addEventListener('mouseenter', function () { open(t); });
        item.addEventListener('mouseleave', function () { closeAll(); });
        panel.addEventListener('mouseenter', function () { open(t); });
        panel.addEventListener('mouseleave', function () { closeAll(); });
        t.addEventListener('focus', function () { open(t); });
      } else {
        // No hover to give on a touch screen: first tap opens the panel,
        // a second tap on the same item follows the link.
        t.addEventListener('click', function (e) {
          if (t.getAttribute('aria-expanded') !== 'true') {
            e.preventDefault();
            open(t);
          }
        });
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      var openT = triggers.filter(function (t) { return t.getAttribute('aria-expanded') === 'true'; })[0];
      if (openT) { closeAll(); openT.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-mega-trigger]') || e.target.closest('.mega')) return;
      closeAll();
    });
  }

  /* --------------------------------------------------------------- Back control
     The Back control is a real link to the parent section, so it still goes
     somewhere sensible with JavaScript off. With JavaScript on it prefers the
     browser's own history, which is what "back" means to a visitor who has been
     clicking around. Someone who landed straight on this page from search has
     no in-site history to return to, so for them the link's own href — the
     parent section — is the right destination, and we leave the click alone. */
  function initBack() {
    $$('[data-back]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var ref = document.referrer;
        var internal = !!ref && ref.indexOf(location.origin + '/') === 0 && ref !== location.href;
        // Opened from disk: origin is "null" and the referrer is blank, so the
        // only signal left is whether this tab has navigated at all.
        if (location.protocol === 'file:') internal = history.length > 1;
        if (!internal) return;
        e.preventDefault();
        e.stopPropagation();   // the preview's hash router must not also handle it
        history.back();
      });
    });
  }

  /* ------------------------------------------------------ Certificate viewer
     Opens the full authorisation certificate over the page. The trigger is a
     real button rather than a link because there is no separate page to land
     on; with JavaScript off the button simply does not appear, and the claim
     it sits beside still reads correctly on its own. */
  function initCertViewer() {
    var triggers = $$('[data-cert]');
    if (!triggers.length) return;

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.hidden = true;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.innerHTML = '<button class="lightbox__x" type="button" aria-label="Close certificate">&times;</button>'
                  + '<img class="lightbox__img" alt="">';
    document.body.appendChild(box);

    var img = box.querySelector('.lightbox__img');
    var closeBtn = box.querySelector('.lightbox__x');
    var lastFocus = null;

    function open(t) {
      lastFocus = document.activeElement;
      img.src = t.getAttribute('data-cert');
      img.alt = t.getAttribute('data-cert-alt') || '';
      var w = t.getAttribute('data-cert-w'), h = t.getAttribute('data-cert-h');
      if (w && h) { img.width = w; img.height = h; }
      box.hidden = false;
      document.body.classList.add('is-locked');
      closeBtn.focus();
    }
    function close() {
      box.hidden = true;
      document.body.classList.remove('is-locked');
      img.removeAttribute('src');
      if (lastFocus) lastFocus.focus();
    }

    triggers.forEach(function (t) {
      t.addEventListener('click', function () { open(t); });
    });
    closeBtn.addEventListener('click', close);
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !box.hidden) close();
    });
    box.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); }
    });
  }

  /* --------------------------------------------------------- Hero slideshow
     Cross-fades the hero photograph. The markup ships with only the first
     slide loadable; the rest carry their URLs in data-srcset/data-src so the
     preload scanner never queues them and the first slide stays the
     uncontested LCP candidate. Slides are fetched one ahead of where the
     viewer is, so a visitor who scrolls straight past pays for two images
     rather than the whole set.

     Nothing here is required for the hero to work: with this file absent, or
     with reduced motion requested, the first slide is a static hero. */
  function initHeroSlides() {
    var box = $('[data-hero-slides]');
    if (!box) return;
    var slides = $$('[data-hero-slide]', box);
    if (slides.length < 2) return;
    if (reduced) return;              // honour prefers-reduced-motion

    var INTERVAL = 3500;
    var i = 0, timer = null, started = false;

    function promote(n) {
      var sl = slides[n];
      if (!sl || sl.getAttribute('data-loaded') === 'true') return;
      sl.setAttribute('data-loaded', 'true');
      $$('source[data-srcset]', sl).forEach(function (so) {
        so.setAttribute('srcset', so.getAttribute('data-srcset'));
        so.removeAttribute('data-srcset');
      });
      $$('img[data-src]', sl).forEach(function (im) {
        im.setAttribute('src', im.getAttribute('data-src'));
        im.removeAttribute('data-src');
      });
    }

    function show(n) {
      slides.forEach(function (sl, k) {
        if (k === n) sl.setAttribute('data-active', 'true');
        else sl.removeAttribute('data-active');
      });
    }
    function advance() {
      i = (i + 1) % slides.length;
      show(i);
      promote((i + 1) % slides.length);   // get the next one ready in good time
    }
    function start() { if (!timer) timer = setInterval(advance, INTERVAL); }
    function stop() { clearInterval(timer); timer = null; }

    function begin() {
      if (started) return;
      started = true;
      promote(1);
      start();
    }
    if (document.readyState === 'complete') begin();
    else window.addEventListener('load', begin);

    // A slideshow animating in a tab nobody is looking at is wasted work.
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop();
      else if (started) start();
    });
  }

  /* ------------------------------------------------- Learner testimonials
     An interactive gallery rather than a wall of moving thumbnails.

       resting     the tile shows its own poster, nothing loaded
       hover       that one clip plays, silent, and fades up over the poster
       leave       it pauses, rewinds and fades back to the poster
       click       plays the full video with sound and holds it there until
                   clicked again

     Only ever one video runs at a time: starting any tile stops whichever was
     playing before. Nothing is fetched until a pointer actually arrives, so a
     gallery of any size costs nothing to load.

     Touch screens have no hover to give, so there tiles stay on their poster
     and a tap plays — which is the behaviour a phone user expects anyway. */
  function initTestimonials() {
    var tiles = $$('[data-testi]');
    if (!tiles.length) return;

    var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var current = null;          // the tile that owns playback right now

    function video(tile) { return tile.querySelector('video'); }

    // Every start gets a ticket. A play promise that settles after something
    // else has taken over finds its ticket stale and does nothing — without
    // this, a late-resolving fallback can restart a video that was stopped,
    // and two clips end up running at once.
    var ticket = 0;

    function source(tile, full) {
      var v = video(tile);
      var want = full ? (tile.getAttribute('data-full') || tile.getAttribute('data-src'))
                      : tile.getAttribute('data-src');
      if (v.getAttribute('src') !== want) v.setAttribute('src', want);
      return v;
    }

    function stop(tile) {
      if (!tile) return;
      ticket++;                       // invalidate anything still in flight
      var v = video(tile);
      v.pause();
      try { v.currentTime = 0; } catch (e) {}
      v.muted = true;
      tile.removeAttribute('data-playing');
      tile.removeAttribute('data-holding');
      if (current === tile) current = null;
    }

    function start(tile, full) {
      if (current && current !== tile) stop(current);   // one at a time
      current = tile;
      // Marked synchronously: clicking a button fires focus first, and if this
      // waited on the play promise the focus handler would still think the
      // tile was free and clobber the click.
      if (full) tile.setAttribute('data-holding', 'true');
      var mine = ++ticket;
      var v = source(tile, full);
      v.muted = !full;                                  // sound only on a click
      var pr = v.play();
      if (pr && pr.then) {
        pr.then(function () {
          if (mine !== ticket) return;                  // superseded
          tile.setAttribute('data-playing', 'true');
        }).catch(function () {
          if (mine !== ticket) return;
          // Autoplay refused (usually an unmuted play without a gesture).
          // Fall back to the silent preview rather than leaving a dead tile.
          if (full) {
            v.muted = true;
            v.play().then(function () {
              if (mine === ticket) tile.setAttribute('data-playing', 'true');
            }).catch(function () {});
          }
        });
      } else {
        tile.setAttribute('data-playing', 'true');      // very old browsers
      }
    }

    tiles.forEach(function (tile) {
      var v = video(tile);
      if (!v) return;
      v.setAttribute('playsinline', '');

      if (canHover) {
        tile.addEventListener('mouseenter', function () {
          if (tile.hasAttribute('data-holding')) return;   // a click owns it
          start(tile, false);
        });
        tile.addEventListener('mouseleave', function () {
          if (tile.hasAttribute('data-holding')) return;
          stop(tile);
        });
        // Keyboard users get the same preview when they tab onto a tile.
        tile.addEventListener('focus', function () {
          if (!tile.hasAttribute('data-holding')) start(tile, false);
        });
        tile.addEventListener('blur', function () {
          if (!tile.hasAttribute('data-holding')) stop(tile);
        });
      }

      // Click toggles the real thing, with sound, and keeps it running.
      tile.addEventListener('click', function () {
        if (tile.hasAttribute('data-holding')) { stop(tile); return; }
        start(tile, true);
      });

      // When a clicked video reaches its end, hand the tile back to its poster.
      v.addEventListener('ended', function () { stop(tile); });
    });

    // Anything that scrolls fully out of view has no business still playing.
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting && en.target === current) stop(en.target);
        });
      }, { threshold: 0 });
      tiles.forEach(function (t) { io.observe(t); });
    }
  }

  /* ------------------------------------------------------------ Mobile drawer */
  function initDrawer() {
    var burger = $('[data-burger]');
    var drawer = $('[data-drawer]');
    if (!burger || !drawer) return;
    var lastFocus = null;

    function set(open) {
      burger.setAttribute('aria-expanded', String(open));
      drawer.setAttribute('data-open', String(open));
      drawer.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('is-locked', open);
      if (open) { lastFocus = document.activeElement; var f = drawer.querySelector('a,button'); if (f) f.focus(); }
      else if (lastFocus) { lastFocus.focus(); }
    }
    burger.addEventListener('click', function () { set(burger.getAttribute('aria-expanded') !== 'true'); });
    $$('[data-drawer-close]').forEach(function (b) { b.addEventListener('click', function () { set(false); }); });
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.getAttribute('data-open') === 'true') set(false);
    });
    // Focus trap
    drawer.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || drawer.getAttribute('data-open') !== 'true') return;
      var f = $$('a[href],button:not([disabled]),input,select,textarea', drawer)
              .filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* -------------------------------------------------------------- Accordions */
  function initAccordions() {
    $$('[data-acc-trigger]').forEach(function (t) {
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (!panel) return;
      t.addEventListener('click', function () {
        var open = t.getAttribute('aria-expanded') === 'true';
        t.setAttribute('aria-expanded', String(!open));
        panel.setAttribute('data-open', String(!open));
      });
    });
  }

  /* ----------------------------------------------------------- Scroll reveal */
  function initReveal() {
    var els = $$('.rv');
    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var d = Math.round(parseInt(en.target.getAttribute('data-delay') || '0', 10) * 0.5);
        setTimeout(function () { en.target.classList.add('is-in'); }, d);
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------- Statistic count-up */
  function initCounters() {
    var els = $$('[data-count]');
    if (!els.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.textContent = el.getAttribute('data-count') + (el.getAttribute('data-suffix') || ''); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var dec = (el.getAttribute('data-count').split('.')[1] || '').length;
        var t0 = null, dur = 900;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = (target * eased).toFixed(dec) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        io.unobserve(el);
      });
    }, { threshold: 0.5 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------ Card filters */
  function initFilters() {
    $$('[data-filter-group]').forEach(function (group) {
      var targetSel = group.getAttribute('data-filter-target');
      var list = $(targetSel);
      if (!list) return;
      var empty = $(group.getAttribute('data-filter-empty') || '#nope');
      var countEl = $(group.getAttribute('data-filter-count') || '#nope');

      group.addEventListener('click', function (e) {
        var chip = e.target.closest('.chip');
        if (!chip) return;
        $$('.chip', group).forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        var val = chip.getAttribute('data-filter');
        var shown = 0;
        $$('[data-tags]', list).forEach(function (item) {
          var match = val === 'all' || item.getAttribute('data-tags').split(' ').indexOf(val) > -1;
          item.classList.toggle('is-hidden', !match);
          if (match) shown++;
        });
        // A grouping wrapper with nothing left visible inside it would
        // otherwise leave its heading stranded above an empty space.
        $$('[data-group]', list).forEach(function (g) {
          var any = $$('[data-tags]', g).some(function (it) {
            return !it.classList.contains('is-hidden');
          });
          g.classList.toggle('is-hidden', !any);
        });
        if (empty) empty.classList.toggle('is-hidden', shown !== 0);
        if (countEl) countEl.textContent = shown;
      });
    });
  }

  /* --------------------------------------------------------- Floating advisor */
  function initAdvisor() {
    var btn = $('[data-advisor]');
    var panel = $('[data-advisor-panel]');
    if (!btn || !panel) return;
    function close() {
      btn.setAttribute('aria-expanded', 'false');
      panel.setAttribute('data-open', 'false');
    }
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      panel.setAttribute('data-open', String(!open));
    });
    document.addEventListener('click', function (e) {
      if (e.target.closest('.advisor')) return;
      close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    /* Keep the dock clear of the header at the top of the page and of the
       footer at the bottom: visible only through the body of the page. */
    var dock = btn.closest('.advisor');
    var footer = $('.footer');
    var atTop = true, atFooter = false, ticking = false;
    function apply() {
      var hide = atTop || atFooter;
      dock.setAttribute('data-hide', String(hide));
      if (hide) close();
    }
    function update() {
      atTop = window.scrollY < 400;
      apply();
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    if (footer && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        atFooter = entries[0].isIntersecting;
        apply();
      }, { threshold: 0 });
      io.observe(footer);
    }
    update();
  }

  /* ======================================================================
     CAREER PATH FINDER
     Logic mirrors the approved mapping table in Document 2, Section 12.4.
     Rule: no answer combination may return an empty result.
     ====================================================================== */

  var PATHS = {
    bim: {
      name: 'BIM & Digital Construction',
      href: 'career-paths/bim-digital-construction/',
      roadmap: ['AutoCAD', 'Revit Architecture', 'Revit Structure / MEP', 'Navisworks', 'Coordination', 'Live project'],
      roles: ['BIM Modeller', 'BIM Engineer', 'BIM Coordinator'],
      why: 'BIM is where building design and coordination actually happen now, and it is the fastest-growing shortage in the market you are entering.'
    },
    civil: {
      name: 'Civil & Infrastructure Design',
      href: 'career-paths/',
      roadmap: ['AutoCAD Civil', 'Surfaces & terrain', 'Alignments', 'Corridor modelling', 'Quantity take-off', 'Live project'],
      roles: ['Civil Design Engineer', 'Highway Design Engineer', 'Quantity Engineer'],
      why: 'Infrastructure work rewards accuracy, and corridor modelling with quantity extraction is the specific skill consultancies and contractors recruit for.'
    },
    arch: {
      name: 'Architecture & Visualisation',
      href: 'career-paths/',
      roadmap: ['SketchUp / Revit', 'Materials & lighting', 'V-Ray', 'Lumion', '3ds Max', 'Portfolio project'],
      roles: ['Architectural Designer', '3D Visualiser', 'Design Technician'],
      why: 'Your design sense is already the hard part. Visualisation gives you the craft to make a client believe a building that does not exist yet.'
    },
    mech: {
      name: 'Mechanical & Product Design',
      href: 'career-paths/',
      roadmap: ['AutoCAD Mechanical', 'SolidWorks', 'Assemblies', 'GD&T', 'CATIA / NX CAD', '3D printed prototype'],
      roles: ['Design Engineer', 'Product Design Engineer', 'CAD Engineer'],
      why: 'The manufacturing belt around Gurugram, Manesar and Bhiwadi hires exactly this skill set, and the drawing matters as much as the model.'
    },
    struct: {
      name: 'Structural Engineering & Analysis',
      href: 'career-paths/',
      roadmap: ['AutoCAD', 'Structural modelling', 'STAAD.Pro', 'ETABS', 'Code checks', 'Revit Structure detailing'],
      roles: ['Structural Design Engineer', 'Analysis Engineer', 'Detailing Engineer'],
      why: 'You want the calculation as well as the geometry. This path keeps both, and detailing is where the two meet.'
    },
    mep: {
      name: 'Electrical & MEP Design',
      href: 'career-paths/',
      roadmap: ['AutoCAD Electrical', 'Schematics & panels', 'Revit MEP', 'Services coordination', 'Navisworks clash'],
      roles: ['MEP Design Engineer', 'Electrical Design Engineer', 'MEP BIM Coordinator'],
      why: 'MEP is chronically under-supplied. Coordinators in particular are among the hardest roles for firms to fill.'
    },
    pm: {
      name: 'Project Planning & Management',
      href: 'career-paths/',
      roadmap: ['PM fundamentals', 'MS Project', 'Primavera P6', 'Cost & resource', '4D / 5D concepts', 'Planning project'],
      roles: ['Planning Engineer', 'Project Coordinator', 'Cost Engineer'],
      why: 'Planning experience compounds into seniority faster than most technical routes, and Gulf EPC contractors hire for it continuously.'
    }
  };

  var TIERS = {
    studying:  { name: 'Short-term or professional certificate', note: 'Fits alongside your degree.' },
    fresher:   { name: 'Master programme',                       note: 'The complete route, with a live project and portfolio.' },
    upskill:   { name: 'Professional certificate',                note: 'Depth in one discipline, without a career break.' },
    switch:    { name: 'Master programme',                        note: 'A full stack, because you are changing direction.' }
  };

  // Q3 interest → path. Q1 background modifies "unsure" and one alternate.
  function recommend(a) {
    var key;
    switch (a.interest) {
      case 'buildings': key = (a.background === 'arch') ? 'arch' : 'bim'; break;
      case 'infra':     key = 'civil'; break;
      case 'products':  key = 'mech'; break;
      case 'analysis':  key = (a.background === 'mech') ? 'mech' : 'struct'; break;
      case 'planning':  key = 'pm'; break;
      default:
        key = ({ civil: 'bim', mech: 'mech', arch: 'arch', elec: 'mep' })[a.background] || 'bim';
    }
    var path = PATHS[key];
    var tier = TIERS[a.stage] || TIERS.fresher;
    var intl = a.goal === 'abroad';
    return { key: key, path: path, tier: tier, intl: intl };
  }

  function initFinder() {
    var root = $('[data-finder]');
    if (!root) return;

    var panels = $$('.panel', root);
    var fill = $('[data-steps-fill]', root);
    var stepLabel = $('[data-step-label]', root);
    var answers = {};
    var idx = 0;

    function show(i) {
      idx = i;
      panels.forEach(function (p, n) { p.setAttribute('data-active', String(n === i)); });
      var total = panels.length - 1; // last panel is the result
      if (fill) fill.style.width = Math.min(((i) / total) * 100, 100) + '%';
      if (stepLabel) {
        stepLabel.textContent = i < total ? 'Step ' + (i + 1) + ' of ' + total : 'Your result';
      }
      var h = $('h2, h3', panels[i]);
      if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
      root.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
      // Only touch the hash on the multi-page build. In the single-file
      // preview the hash is the page route, so writing step state into it
      // would clobber navigation.
      if (history.replaceState && $$('[data-page]').length < 2) {
        history.replaceState(null, '', '#finder-' + i);
      }
    }

    root.addEventListener('change', function (e) {
      var input = e.target.closest('input[type="radio"]');
      if (!input) return;
      answers[input.name] = input.value;
      var next = input.closest('.panel').getAttribute('data-next');
      if (next === 'result') { render(); show(panels.length - 1); }
      else { setTimeout(function () { show(idx + 1); }, 160); }
    });

    $$('[data-finder-back]', root).forEach(function (b) {
      b.addEventListener('click', function () { if (idx > 0) show(idx - 1); });
    });
    $$('[data-finder-restart]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        answers = {};
        $$('input[type="radio"]', root).forEach(function (i) { i.checked = false; });
        show(0);
      });
    });

    function render() {
      var r = recommend(answers);
      $('[data-r-name]', root).textContent = r.path.name;
      $('[data-r-why]', root).textContent = r.path.why;
      $('[data-r-tier]', root).textContent = r.tier.name;
      $('[data-r-tiernote]', root).textContent = r.tier.note;

      var rm = $('[data-r-roadmap]', root);
      rm.innerHTML = '';
      r.path.roadmap.forEach(function (s, i) {
        if (i) {
          var a = document.createElement('span');
          a.className = 'roadmap__arrow'; a.textContent = '→'; a.setAttribute('aria-hidden', 'true');
          rm.appendChild(a);
        }
        var el = document.createElement('span');
        el.className = 'roadmap__step'; el.textContent = s;
        rm.appendChild(el);
      });

      var rl = $('[data-r-roles]', root);
      rl.innerHTML = '';
      r.path.roles.forEach(function (role) {
        var li = document.createElement('li'); li.textContent = role; rl.appendChild(li);
      });

      var link = $('[data-r-link]', root);
      if (link) link.setAttribute('href', (root.getAttribute('data-base') || '') + r.path.href);

      var intl = $('[data-r-intl]', root);
      if (intl) intl.classList.toggle('is-hidden', !r.intl);
    }

    show(0);
  }

  /* ======================================================================
     CONVERSATIONAL LEAD FORM + SCHEDULER
     ====================================================================== */

  function initLeadForm() {
    var root = $('[data-leadform]');
    if (!root) return;

    var panels = $$('.panel', root);
    var fill = $('[data-steps-fill]', root);
    var stepLabel = $('[data-step-label]', root);
    var idx = 0;
    var data = {};

    function show(i) {
      idx = i;
      panels.forEach(function (p, n) { p.setAttribute('data-active', String(n === i)); });
      var total = panels.length - 2; // last two panels are reward + scheduled
      if (fill) fill.style.width = Math.min((i / total) * 100, 100) + '%';
      if (stepLabel) stepLabel.textContent = i < total ? 'Step ' + (i + 1) + ' of ' + total : '';
      var h = $('h2, h3', panels[i]);
      if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    }

    root.addEventListener('change', function (e) {
      var input = e.target.closest('input[type="radio"]');
      if (!input) return;
      data[input.name] = input.value;
      if (input.closest('.panel').getAttribute('data-next') !== 'manual') {
        setTimeout(function () { show(idx + 1); }, 160);
      }
    });

    $$('[data-lead-back]', root).forEach(function (b) {
      b.addEventListener('click', function () { if (idx > 0) show(idx - 1); });
    });

    // Field-level validation on blur (Doc 1, 5.3)
    function validate(field) {
      var input = $('input', field);
      if (!input) return true;
      var v = input.value.trim();
      var ok = true;
      if (input.hasAttribute('required') && !v) ok = false;
      if (ok && input.type === 'tel' && v && !/^[0-9]{10}$/.test(v.replace(/\D/g, ''))) ok = false;
      if (ok && input.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) ok = false;
      field.setAttribute('data-invalid', String(!ok));
      input.setAttribute('aria-invalid', String(!ok));
      return ok;
    }
    $$('.field', root).forEach(function (f) {
      var input = $('input', f);
      if (!input) return;
      input.addEventListener('blur', function () { validate(f); });
      input.addEventListener('input', function () {
        if (f.getAttribute('data-invalid') === 'true') validate(f);
      });
    });

    var submit = $('[data-lead-submit]', root);
    if (submit) {
      submit.addEventListener('click', function () {
        var fields = $$('.panel[data-active="true"] .field', root);
        var allOk = fields.map(validate).every(Boolean);
        if (!allOk) { var bad = $('.field[data-invalid="true"] input', root); if (bad) bad.focus(); return; }

        data.name = ($('[name="lead_name"]', root) || {}).value || '';
        data.phone = ($('[name="lead_phone"]', root) || {}).value || '';

        submit.disabled = true;
        var original = submit.textContent;
        submit.textContent = 'Just a moment…';

        // Posts to /api/leads. If no backend is deployed the request fails
        // and we still show the recommendation — the visitor is never blocked
        // by our infrastructure.
        function finish() {
          submit.disabled = false;
          submit.textContent = original;
          var r = recommend({
            background: data.lead_background,
            stage: data.lead_stage,
            interest: data.lead_interest || 'unsure',
            goal: data.lead_goal
          });
          var nameEl = $('[data-reward-name]', root);
          if (nameEl) nameEl.textContent = data.name ? data.name.split(' ')[0] : 'there';
          var p = $('[data-reward-path]', root); if (p) p.textContent = r.path.name;
          var t = $('[data-reward-tier]', root); if (t) t.textContent = r.tier.name;
          var rmEl = $('[data-reward-roadmap]', root);
          if (rmEl) {
            rmEl.innerHTML = '';
            r.path.roadmap.forEach(function (s, i) {
              if (i) { var a = document.createElement('span'); a.className = 'roadmap__arrow'; a.textContent = '→'; rmEl.appendChild(a); }
              var el = document.createElement('span'); el.className = 'roadmap__step'; el.textContent = s; rmEl.appendChild(el);
            });
          }
          show(panels.length - 2);
        }

        postLead({
          source: 'contact_form',
          name: data.name, phone: data.phone,
          email: (root.querySelector('[name="lead_email"]') || {}).value || '',
          stage: data.lead_stage, background: data.lead_background,
          goal: data.lead_goal, interest: data.lead_interest
        }).then(finish, finish);
      });
    }

    // Scheduler
    var sched = { day: null, time: null, channel: null };
    root.addEventListener('click', function (e) {
      var chip = e.target.closest('[data-sched]');
      if (!chip) return;
      var kind = chip.getAttribute('data-sched');
      var scope = chip.closest('[data-sched-group]');
      $$('[data-sched]', scope).forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      sched[kind] = chip.textContent.trim();
      var confirmBtn = $('[data-sched-confirm]', root);
      if (confirmBtn) confirmBtn.disabled = !(sched.day && sched.time && sched.channel);
    });
    // Scheduling choices are appended to the lead record
    var confirmSched = null;
    var confirm = $('[data-sched-confirm]', root);
    if (confirm) {
      confirm.addEventListener('click', function () {
        postLead({ source: 'contact_form_slot', name: data.name || '', phone: data.phone || '',
                   slot_day: sched.day, slot_time: sched.time, slot_channel: sched.channel });
        var out = $('[data-sched-summary]', root);
        if (out) out.textContent = sched.day + ', ' + sched.time + ', by ' + sched.channel + '.';
        show(panels.length - 1);
      });
    }

    show(0);
  }

  /* --------------------------------------------------- Simple hash routing
     Used by the single-file preview only. Multi-page build ignores this. */
  function initRouter() {
    var pages = $$('[data-page]');
    if (pages.length < 2) return;

    function go(id, push) {
      var target = pages.filter(function (p) { return p.getAttribute('data-page') === id; })[0] || pages[0];
      pages.forEach(function (p) { p.hidden = p !== target; });
      $$('[data-route]').forEach(function (a) {
        var on = a.getAttribute('data-route') === target.getAttribute('data-page');
        if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      });
      var pb = $('[data-pagebar]');
      if (pb) pb.hidden = target.getAttribute('data-page') === 'home';
      window.scrollTo({ top: 0, behavior: 'auto' });
      document.title = (target.getAttribute('data-title') || 'CADD Centre Gurugram');
      // Re-run view-dependent behaviour for the newly shown page
      $$('.rv', target).forEach(function (el) { el.classList.remove('is-in'); });
      initReveal();
      initCounters();
      if (push && history.pushState) history.pushState({ p: id }, '', '#' + id);
    }

    document.addEventListener('click', function (e) {
      var a = e.target.closest('[data-route]');
      if (!a) return;
      e.preventDefault();
      go(a.getAttribute('data-route'), true);
      var drawer = $('[data-drawer]');
      if (drawer && drawer.getAttribute('data-open') === 'true') {
        drawer.setAttribute('data-open', 'false');
        var b = $('[data-burger]'); if (b) b.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('is-locked');
      }
      $$('[data-mega-trigger]').forEach(function (t) {
        t.setAttribute('aria-expanded', 'false');
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.setAttribute('data-open', 'false');
      });
    });

    window.addEventListener('popstate', function () { go(routeFromHash(), false); });
    window.addEventListener('hashchange', function () { go(routeFromHash(), false); });

    function routeFromHash() {
      var raw = decodeURIComponent((location.hash || '').replace(/^#/, ''));
      if (!raw) return 'home';
      // Tolerate a trailing path someone appended by hand, e.g. '#x/admin'
      var parts = raw.split('/').filter(Boolean);
      var known = pages.map(function (p) { return p.getAttribute('data-page'); });
      for (var i = parts.length - 1; i >= 0; i--) {
        if (known.indexOf(parts[i]) > -1) return parts[i];
      }
      // Legacy finder step hashes, and anything else unrecognised
      return 'home';
    }
    go(routeFromHash(), false);
  }

  /* ------------------------------------------------------------ Enquiry modal */
  function initModal() {
    var modal = $('[data-modal]');
    if (!modal) return;
    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      modal.hidden = false;
      document.body.classList.add('is-locked');
      var f = modal.querySelector('input, button');
      if (f) f.focus();
    }
    function close() {
      modal.hidden = true;
      document.body.classList.remove('is-locked');
      if (lastFocus) lastFocus.focus();
    }

    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-enquire]')) { e.preventDefault(); open(); }
      else if (e.target.closest('[data-modal-close]')) { close(); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) close();
    });
    modal.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || modal.hidden) return;
      var f = $$('a[href],button:not([disabled]),input,select,textarea', modal)
              .filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }


  /* --------------------------------------------------- Reading progress bar
     Orientation on long programme pages. Cheap: rAF-throttled scroll. */
  function initProgress() {
    var bar = $('[data-progress]');
    if (!bar) return;
    var ticking = false;
    function update() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? Math.min((h.scrollTop / max) * 100, 100) : 0) + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ------------------------------------------------ Sticky sub-nav scrollspy
     Highlights the section you are actually reading. */
  function initSubnav() {
    var nav = $('[data-subnav]');
    if (!nav) return;
    var links = $$('a[href^="#"]', nav);
    var targets = links.map(function (a) {
      return document.getElementById(a.getAttribute('href').slice(1));
    }).filter(Boolean);
    if (!targets.length) return;

    function setActive(id) {
      links.forEach(function (a) {
        var on = a.getAttribute('href') === '#' + id;
        if (on) { a.setAttribute('aria-current', 'true');
                  if (a.offsetLeft < nav.scrollLeft || a.offsetLeft > nav.scrollLeft + nav.clientWidth - 120) {
                    nav.scrollTo({ left: Math.max(a.offsetLeft - 24, 0), behavior: reduced ? 'auto' : 'smooth' });
                  } }
        else a.removeAttribute('aria-current');
      });
    }
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) setActive(en.target.id); });
    }, { rootMargin: '-140px 0px -65% 0px', threshold: 0 });
    targets.forEach(function (t) { io.observe(t); });
  }

  /* ----------------------------------------------------- Sticky conversion bar
     Reappears once the hero CTA has scrolled out of view. */
  function initStickyCta() {
    var bar = $('[data-stickycta]');
    var sentinel = $('[data-cta-sentinel]');
    if (!bar || !sentinel || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      bar.setAttribute('data-show', String(!entries[0].isIntersecting));
    }, { threshold: 0 });
    io.observe(sentinel);
  }

  /* ------------------------------------------------------------- Back to top */
  function initToTop() {
    var btn = $('[data-totop]');
    if (!btn) return;
    var ticking = false;
    function update() {
      btn.setAttribute('data-show', String(window.scrollY > 900));
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
      var skip = $('.skip-link'); if (skip) skip.focus();
    });
    update();
  }

  /* ------------------------------------------- Roadmap progressive reveal */
  function initRoadmaps() {
    var maps = $$('.roadmap');
    if (!maps.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      maps.forEach(function (m) { m.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var steps = $$('.roadmap__step, .roadmap__arrow', en.target);
        steps.forEach(function (el, i) {
          el.style.transitionDelay = (i * 30) + 'ms';   // skill rule: 20-40ms
        });
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { threshold: 0.25 });
    maps.forEach(function (m) { io.observe(m); });
  }

  /* ------------------------------------------------ Google review carousel
     The cards are in the HTML already (written from src/data/reviews.json at
     build time), so the section is complete before this runs. Added here:
       - live refresh from /api/reviews, which reads the Business Profile
         server-side so the key is never in the page. A failure changes
         nothing — the visitor keeps the markup they were served.
       - the arrows, and a "Read more" toggle on quotes that actually clip.
     The track itself scrolls natively: swipe, trackpad and arrow keys work
     with this file absent. */

  // Ignore an overflow of a few pixels: three cards that fill the row exactly
  // still round to a stray pixel or two, and arrows that scroll nothing are
  // worse than no arrows.
  var GRR_SLACK = 24;

  function grrAvatarHue(name) {
    var h = 0;
    for (var i = 0; i < name.length; i++) h += name.charCodeAt(i) * (i + 7);
    return h % 360;
  }

  function grrStars(rating) {
    var full = Math.max(1, Math.min(5, Math.round(rating || 5)));
    return new Array(full + 1).join('★') + new Array(6 - full).join('☆');
  }

  /* Rebuild one card, reusing the markup the build script emits so the two
     stay visually identical. The Google mark and tick are cloned from the
     card that was served rather than duplicated as strings here. */
  function grrCard(review, template) {
    var card = template.cloneNode(true);
    var name = review.author || 'Google reviewer';
    var face = $('.grr__avatar', card);
    var g = $('.grr__g', face);

    face.style.setProperty('--grr-av', 'hsl(' + grrAvatarHue(name) + ' 45% 70%)');
    face.textContent = '';
    if (review.photo) {
      var img = document.createElement('img');
      img.src = review.photo;
      img.alt = '';
      img.width = 56; img.height = 56;
      img.loading = 'lazy';
      img.referrerPolicy = 'no-referrer';
      face.appendChild(img);
    } else {
      face.appendChild(document.createTextNode(name.charAt(0).toUpperCase()));
    }
    if (g) face.appendChild(g);

    $('.grr__name', card).textContent = name;
    $('.grr__when', card).textContent = review.when || 'on Google';
    var stars = $('.grr__stars', card);
    stars.textContent = grrStars(review.rating);
    stars.setAttribute('aria-label', Math.round(review.rating || 5) + ' out of 5');
    var text = $('[data-grr-text]', card);
    text.textContent = review.text;
    text.classList.remove('is-open');
    var more = $('.grr__more', card);
    if (more) more.parentNode.removeChild(more);
    card.classList.add('is-in');            // already on screen: no reveal delay
    card.removeAttribute('data-delay');
    return card;
  }

  function initReviews() {
    $$('[data-grr]').forEach(function (root) {
      var track = $('[data-grr-track]', root);
      if (!track) return;
      var prev = $('[data-grr-prev]', root);
      var next = $('[data-grr-next]', root);
      var template = $('.grr__card', track);

      function step() {
        var card = track.firstElementChild;
        if (!card) return track.clientWidth;
        var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return card.getBoundingClientRect().width + gap;
      }

      // The arrows are part of the design and stay on screen. They are never
      // hidden and never disabled, because they always do something: when the
      // cards overflow they scroll, and when they all fit (three reviews on a
      // wide screen) they rotate the running order instead. Either way a click
      // visibly moves the reviews, which is what the control promises.
      function fits() {
        return track.scrollWidth - track.clientWidth <= GRR_SLACK;
      }

      function sync() {
        [prev, next].forEach(function (b) {
          if (!b) return;
          b.hidden = false;
          b.disabled = false;
        });
      }

      function rotate(forward) {
        var kids = track.children;
        if (kids.length < 2) return;
        if (forward) track.appendChild(kids[0]);
        else track.insertBefore(kids[kids.length - 1], kids[0]);
        // Re-run the clamp so a newly shown card gets its Read more control.
        readMore();
      }

      function move(forward) {
        if (fits()) rotate(forward);
        else scrollBy(forward ? step() : -step());
      }

      function scrollBy(delta) {
        if (track.scrollBy) track.scrollBy({ left: delta, behavior: reduced ? 'auto' : 'smooth' });
        else track.scrollLeft += delta;
      }

      function readMore() {
        $$('[data-grr-text]', track).forEach(function (text) {
          if ($('.grr__more', text.parentNode)) return;
          if (text.scrollHeight - text.clientHeight < 4) return;
          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'grr__more';
          btn.textContent = 'Read more';
          btn.setAttribute('aria-expanded', 'false');
          btn.addEventListener('click', function () {
            var open = text.classList.toggle('is-open');
            btn.textContent = open ? 'Show less' : 'Read more';
            btn.setAttribute('aria-expanded', String(open));
            sync();
          });
          text.parentNode.appendChild(btn);
        });
      }

      if (prev) prev.addEventListener('click', function () { move(false); });
      if (next) next.addEventListener('click', function () { move(true); });
      track.addEventListener('scroll', sync, { passive: true });
      window.addEventListener('resize', sync);
      sync();
      readMore();

      /* --- live refresh ------------------------------------------------- */
      if (!template || !window.fetch) return;
      var section = root.parentNode;

      fetch('/api/reviews', { headers: { Accept: 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!d || !d.reviews || !d.reviews.length) return;

          var frag = document.createDocumentFragment();
          d.reviews.forEach(function (rev) { frag.appendChild(grrCard(rev, template)); });
          track.textContent = '';
          track.appendChild(frag);

          if (d.rating) {
            var score = $('[data-grr-rating]', section);
            if (score) score.textContent = String(Math.round(d.rating * 10) / 10);
            var sum = $('.grsum .grr__stars', section);
            if (sum) {
              sum.textContent = grrStars(d.rating);
              sum.setAttribute('aria-label', d.rating + ' out of 5');
            }
          }
          if (d.ratingCount) {
            $$('[data-grr-count]', section).forEach(function (el) {
              el.textContent = String(d.ratingCount);
            });
          }
          if (d.reviewsUrl) {
            var link = $('[data-grr-link]', section);
            if (link) link.href = d.reviewsUrl;
          }
          var stamp = $('[data-grr-stamp]', section);
          if (stamp) stamp.textContent = 'Reviews and rating live from Google';

          track.scrollLeft = 0;
          sync();
          readMore();
        })
        .catch(function () { /* keep the pre-rendered cards */ });
    });
  }

  /* ------------------------------------------- Curriculum expand / collapse */
  function initAccTools() {
    $$('[data-acc-all]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var scope = document.getElementById(btn.getAttribute('data-acc-all'));
        if (!scope) return;
        var open = btn.getAttribute('data-state') !== 'open';
        $$('[data-acc-trigger]', scope).forEach(function (t) {
          t.setAttribute('aria-expanded', String(open));
          var p = document.getElementById(t.getAttribute('aria-controls'));
          if (p) p.setAttribute('data-open', String(open));
        });
        btn.setAttribute('data-state', open ? 'open' : 'closed');
        btn.textContent = open ? 'Collapse all' : 'Expand all';
      });
    });
  }


  /* --------------------------------------------------- Announcement ribbon
     Rendered hidden and revealed by JS, so a dismissed ribbon never flashes
     on the next page load. Dismissal is per session. */
  function initRibbon() {
    var bar = document.querySelector('[data-ribbon]');
    if (!bar) return;
    var KEY = 'cadd-ribbon-dismissed';
    var dismissed = false;
    try { dismissed = sessionStorage.getItem(KEY) === '1'; } catch (e) {}
    if (!dismissed) bar.hidden = false;

    var x = bar.querySelector('[data-ribbon-close]');
    if (x) x.addEventListener('click', function () {
      bar.hidden = true;
      try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
      // the sticky header measures from the top; nudge it to recompute
      window.dispatchEvent(new Event('resize'));
    });
  }

  /* ------------------------------------------------------------- Lead POST
     Single place where the site talks to the backend. Fails soft: a network
     or backend error must never stop the visitor seeing their result. */
  function utmParams() {
    var out = {};
    try {
      new URLSearchParams(location.search).forEach(function (v, k) {
        if (/^utm_|^gclid$|^fbclid$/.test(k)) out[k] = v;
      });
    } catch (e) {}
    return out;
  }

  function postLead(payload) {
    payload.utm = utmParams();
    payload.page = location.pathname;
    return fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).catch(function () { /* fail soft */ });
  }

  /* Enquiry modal + corporate form -> same endpoint */
  function initFormPosts() {
    var modal = $('[data-modal]');
    if (modal) {
      var btn = modal.querySelector('button[type="submit"]');
      if (btn) btn.addEventListener('click', function () {
        var n = modal.querySelector('#eq-n'), p = modal.querySelector('#eq-p'),
            c = modal.querySelector('#eq-c');
        if (!n || !p || !n.value.trim() || p.value.replace(/\D/g, '').length < 10) return;
        postLead({ source: 'enquiry_modal', name: n.value, phone: p.value,
                   course: c ? c.value : '' });
        btn.textContent = 'Sent — we will be in touch';
        btn.disabled = true;
      });
    }
    var mentor = document.querySelector('#mentor-form form');
    if (mentor) {
      var mb = mentor.querySelector('button[type="submit"]');
      if (mb) mb.addEventListener('click', function () {
        var g = function (id) { var e = mentor.querySelector(id); return e ? e.value : ''; };
        if (!g('#m1').trim() || g('#m2').replace(/\D/g, '').length < 10) return;
        // Mapped onto the existing lead columns so applications show up in the
        // same dashboard as everything else — filter on source.
        postLead({ source: 'mentor_application',
                   name: g('#m1'), phone: g('#m2'), email: g('#m3'),
                   interest: g('#m4'),
                   background: g('#m5') + ' years — ' + g('#m6'),
                   goal: g('#m7'),
                   message: g('#m8') });
        mb.textContent = 'Application sent';
        mb.disabled = true;
      });
    }

    var corp = document.querySelector('#corp-form form');
    if (corp) {
      var cb = corp.querySelector('button[type="submit"]');
      if (cb) cb.addEventListener('click', function () {
        var g = function (id) { var e = corp.querySelector(id); return e ? e.value : ''; };
        if (!g('#c1').trim() || !g('#c4').trim()) return;
        postLead({ source: 'corporate', name: g('#c1'), phone: g('#c5'), email: g('#c4'),
                   course: g('#c3'), message: g('#c7') });
        cb.textContent = 'Request sent';
        cb.disabled = true;
      });
    }
  }

  /* ------------------------------------------------------------------- Init */
  function boot() {
    initMega();
    initModal();
    initRibbon();
    initFormPosts();
    initProgress();
    initSubnav();
    initStickyCta();
    initToTop();
    initRoadmaps();
    initReviews();
    initAccTools();
    initDrawer();
    initBack();
    initCertViewer();
    initTestimonials();
    initHeroSlides();
    initAccordions();
    initFilters();
    initAdvisor();
    initFinder();
    initLeadForm();
    initRouter();
    initReveal();
    initCounters();
    document.documentElement.setAttribute('data-js', 'on');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
