/* =========================================================================
   SPEEDE — interaction layer
   Motion is opt-out aware: every effect below checks prefers-reduced-motion
   and degrades to a static, fully-legible page.
   ========================================================================= */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- roster data ------------------------------------------------
     Quotes are Speede's own, recovered from their athlete page and blog.
     Deliberately excluded: any quote naming a discontinued mode
     (Nemesis / Excentric), since the relaunch machine uses React Mode.     */
  var ATHLETES = [
    { id: 'chandler', name: 'Michael Chandler', role: 'UFC fighter',
      q: 'Speede caught me off guard with how challenging it was and how effective it was. It was kind of just <b>baffling</b>.' },
    { id: 'fields', name: 'Justin Fields', role: 'NFL quarterback',
      q: 'Within five or 10 minutes on Speede, I feel like I’ve done a 30-minute workout. <b>This is a game changer</b> for strength training.' },
    { id: 'simmons', name: 'Justin Simmons', role: 'NFL safety',
      q: '<b>Intense, crazy, unbeatable</b>… it was unreal.' },
    { id: 'mvs', name: 'Marquez Valdes-Scantling', role: 'NFL wide receiver',
      q: 'With free weights your first few reps are gonna be a lot easier than your last few. But with Speede it’s like <b>a max rep every single time</b>.' },
    { id: 'johnson', name: 'Jaylon Johnson', role: 'NFL defensive back',
      q: 'Speede helps you maximize and push your body the best way you can, to get <b>that physical and mental edge</b> that you need.' },
    { id: 'kmet', name: 'Cole Kmet', role: 'NFL tight end',
      q: 'Speede provides <b>what’s most important</b> to an athlete.' },
    { id: 'plumlee', name: 'Mason Plumlee', role: 'NBA center',
      q: 'The data is amazing. It takes the subjectivity out of it — you can see where you’re at. <b>The numbers won’t lie.</b>' },
    /* No quote from Sesselmann exists anywhere in Speede's own material, so
       hers is a credential rather than an invented testimonial. */
    { id: 'sesselmann', name: 'Lauren Sesselmann', role: 'Olympic medalist',
      credential: 'Olympic <b>bronze medalist</b> with Canada, and a FIFA Women’s World Cup player.' }
  ];

  var STRIP = ATHLETES;

  function pic(id, cls) {
    return '<picture>' +
      '<source type="image/webp" srcset="assets/athletes/' + id + '.webp">' +
      '<img src="assets/athletes/' + id + '.jpg" alt="" width="400" height="600" ' +
      'loading="lazy" decoding="async"' + (cls ? ' class="' + cls + '"' : '') + '>' +
      '</picture>';
  }

  var faces = document.querySelector('[data-faces]');
  if (faces) {
    // rendered twice — the track translates -50%, so the seam never shows
    var chips = STRIP.concat(STRIP);
    faces.innerHTML = chips.map(function (a) {
      return '<div class="face">' +
        '<img src="assets/athletes/' + a.id + '.jpg" alt="" width="34" height="34" loading="lazy" decoding="async">' +
        '<span class="face-txt"><span class="face-name">' + a.name + '</span>' +
        '<span class="face-role">' + a.role + '</span></span></div>';
    }).join('');
  }

  var roster = document.querySelector('[data-roster]');
  if (roster) {
    roster.innerHTML = ATHLETES.map(function (a, i) {
      var body = a.credential
        ? '<p class="athlete-q athlete-q--cred">' + a.credential + '</p>'
        : '<blockquote class="athlete-q">“' + a.q + '”</blockquote>';
      return '<figure class="athlete reveal" style="--d:' + (i % 4) * 80 + 'ms">' +
        '<div class="athlete-img">' + pic(a.id) +
          (a.live === false ? '' :
            '<video class="athlete-live" muted loop playsinline preload="none" ' +
            'aria-hidden="true" data-live="' + a.id + '"></video>') +
        '</div>' +
        '<figcaption class="athlete-body">' + body +
          '<div class="athlete-meta">' +
            '<span class="athlete-name">' + a.name + '</span>' +
            '<span class="athlete-role">' + a.role + '</span>' +
          '</div>' +
        '</figcaption></figure>';
    }).join('');
  }

  /* ---------- section decorations: animate only while on screen ---------- */
  Array.prototype.forEach.call(
    document.querySelectorAll('[data-numdeco], [data-scideco], [data-mtdeco], [data-fedeco]'), function (d) {
      if (reduce) return;
      if (!('IntersectionObserver' in window)) { d.classList.add('is-live'); return; }
      new IntersectionObserver(function (e) {
        d.classList.toggle('is-live', e[0].isIntersecting);
      }, { threshold: 0.04 }).observe(d);
    });

  /* ---------- final CTA: entry sequence, then hold ------------------------ */
  (function () {
    var deco = document.querySelector('[data-ctadeco]');
    var sec = document.getElementById('join');
    if (!deco || !sec) return;
    if (reduce || !('IntersectionObserver' in window)) { deco.classList.add('is-entered'); return; }
    new IntersectionObserver(function (e, obs) {
      if (!e[0].isIntersecting) return;
      obs.disconnect();                      // the entry plays once, then holds
      deco.classList.add('is-entered');
    }, { threshold: 0.2 }).observe(sec);

    // the lower convergence answers the button and the field
    var charge = function () {
      sec.classList.remove('is-charged');
      void sec.offsetWidth;                  // restart the animation
      sec.classList.add('is-charged');
    };
    Array.prototype.forEach.call(
      sec.querySelectorAll('.btn, input[type=email]'), function (el) {
        el.addEventListener('mouseenter', charge);
        el.addEventListener('focus', charge);
      });
  })();

  /* ---------- hero decoration: animate only while on screen -------------- */
  (function () {
    var deco = document.querySelector('[data-deco]');
    if (!deco || reduce) return;
    if (!('IntersectionObserver' in window)) { deco.classList.add('is-live'); return; }
    new IntersectionObserver(function (entries) {
      deco.classList.toggle('is-live', entries[0].isIntersecting);
    }, { threshold: 0.02 }).observe(deco);
  })();

  /* ---------- living portraits ------------------------------------------
     Hover activates the loop. Sources attach on first hover so nothing is
     fetched until it's wanted, and the still is never replaced by a blank
     frame — the clip only fades in once it can actually play.          */
  if (!reduce) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-live]'), function (v) {
      var card = v.closest('.athlete');
      if (!card) return;

      function attach() {
        if (v.dataset.loaded) return;
        v.dataset.loaded = '1';
        var id = v.getAttribute('data-live');
        [['webm', 'video/webm'], ['mp4', 'video/mp4']].forEach(function (f) {
          var s = document.createElement('source');
          s.src = 'assets/athletes/live/' + id + '.' + f[0];
          s.type = f[1];
          v.appendChild(s);
        });
        v.load();
      }

      function start() {
        attach();
        var go = function () { v.classList.add('ready'); };
        if (v.readyState >= 3) go();
        else v.addEventListener('canplay', go, { once: true });
        var pr = v.play(); if (pr) pr.catch(function () {});
      }

      function stop() {
        v.classList.remove('ready');
        v.pause();
        try { v.currentTime = 0; } catch (e) {}
      }

      card.addEventListener('mouseenter', start);
      card.addEventListener('mouseleave', stop);
      // keyboard and touch parity
      card.addEventListener('focusin', start);
      card.addEventListener('focusout', stop);
      card.setAttribute('tabindex', '0');
    });
  }

  /* ---------- persona cards: hover-activated loops ------------------------ */
  if (!reduce) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-plive]'), function (v) {
      var card = v.closest('.persona');
      if (!card) return;
      function start() {
        if (!v.dataset.loaded) {
          v.dataset.loaded = '1';
          var id = v.getAttribute('data-plive');
          [['webm','video/webm'],['mp4','video/mp4']].forEach(function (f) {
            var s = document.createElement('source');
            s.src = 'assets/video/persona/' + id + '.' + f[0];
            s.type = f[1];
            v.appendChild(s);
          });
          v.load();
        }
        var go = function () { v.classList.add('ready'); };
        if (v.readyState >= 3) go(); else v.addEventListener('canplay', go, { once: true });
        var pr = v.play(); if (pr) pr.catch(function () {});
      }
      function stop() {
        v.classList.remove('ready');
        v.pause();
        try { v.currentTime = 0; } catch (e) {}
      }
      card.addEventListener('mouseenter', start);
      card.addEventListener('mouseleave', stop);
      card.addEventListener('focusin', start);
      card.addEventListener('focusout', stop);
      card.setAttribute('tabindex', '0');
    });
  }

  /* ---------- scroll reveals -------------------------------------------- */
  var revealables = function () { return document.querySelectorAll('.reveal'); };

  if (reduce || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealables(), function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    Array.prototype.forEach.call(revealables(), function (el) { io.observe(el); });
  }

  /* ---------- hero video ------------------------------------------------
     Pause when off-screen (saves battery), and hold the poster frame
     entirely when the visitor has asked for reduced motion.             */
  var hv = document.querySelector('[data-hero-video]');
  if (hv) {
    if (reduce) {
      hv.removeAttribute('autoplay');
      hv.pause();
      hv.currentTime = 0.6;
    } else if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { var p = hv.play(); if (p) p.catch(function () {}); }
          else hv.pause();
        });
      }, { threshold: 0.15 }).observe(hv);
    }
  }

  /* the data film only plays while it's on screen */
  var film = document.querySelector('[data-film]');
  if (film && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && !reduce) { var pr = film.play(); if (pr) pr.catch(function(){}); }
        else film.pause();
      });
    }, { threshold: 0.25 }).observe(film);
    if (reduce) { film.removeAttribute('autoplay'); film.pause(); }
  }

  /* ---------- nav shadow on scroll -------------------------------------- */
  var nav = document.getElementById('nav');
  var onScroll = function () {
    if (nav) nav.classList.toggle('is-stuck', window.scrollY > 12);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- comparison bars fill on scroll ------------------------------
     The gap to Tonal and AMP is something you watch open, not something you
     read. Widths are Speede's own figures: 500 / 250 / 100.                */
  var vsRows = document.querySelectorAll('.vs-list li');
  if (vsRows.length) {
    if (reduce || !('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(vsRows, function (r) { r.classList.add('filled'); });
    } else {
      var vsIO = new IntersectionObserver(function (entries, obs) {
        if (!entries[0].isIntersecting) return;
        obs.disconnect();
        Array.prototype.forEach.call(vsRows, function (r, i) {
          setTimeout(function () { r.classList.add('filled'); }, i * 160);
        });
      }, { threshold: 0.4 });
      vsIO.observe(vsRows[0].parentNode);
    }
  }

  /* ---------- seams: gradient fill + one sweep ---------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-seam]'), function (seam) {
    seam.innerHTML = '<i></i>';
    if (reduce || !('IntersectionObserver' in window)) { seam.classList.add('in'); return; }
    // replays every time it enters view, scrolling either direction — it used
    // to disconnect after the first pass and never fire again
    new IntersectionObserver(function (e) {
      seam.classList.toggle('in', e[0].isIntersecting);
    }, { threshold: 0.4 }).observe(seam);
  });

  /* ---------- count-up on the big number -------------------------------- */
  var big = document.querySelector('[data-count]');
  if (big && !reduce && 'IntersectionObserver' in window) {
    var target = parseInt(big.getAttribute('data-count'), 10);
    var small = big.querySelector('small');
    var label = small ? small.outerHTML : '';
    var DUR = 1100;
    new IntersectionObserver(function (entries, obs) {
      if (!entries[0].isIntersecting) return;
      obs.disconnect();
      var t0 = null;
      function step(ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / DUR, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        big.innerHTML = Math.round(target * eased) + label;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }, { threshold: 0.4 }).observe(big);
  }

  /* ---------- draw the force curve when it comes into view -------------- */
  function drawOnView(sel, opts) {
    var line = document.querySelector(sel);
    if (!line) return;
    if (reduce || !('IntersectionObserver' in window)) return;
    var len = line.getTotalLength ? line.getTotalLength() : 0;
    if (!len) return;
    line.style.strokeDasharray = len;
    line.style.strokeDashoffset = len;
    new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        obs.disconnect();
        line.style.transition = 'stroke-dashoffset ' + (opts.dur || 1500) + 'ms cubic-bezier(.22,.61,.36,1)';
        line.style.strokeDashoffset = 0;
        if (opts.then) setTimeout(opts.then, (opts.dur || 1500) * 0.55);
      });
    }, { threshold: 0.35 }).observe(line);
  }

  var fill = document.querySelector('[data-curve-fill]');
  drawOnView('[data-curve-line]', {
    dur: 1600,
    then: function () {
      if (fill) { fill.style.transition = 'opacity 900ms ease'; fill.style.opacity = 1; }
    }
  });

  var waste = document.querySelector('[data-waste]');
  var wasteLabel = document.querySelector('[data-waste-label]');
  drawOnView('[data-speede-line]', {
    dur: 1800,
    then: function () {
      [waste, wasteLabel].forEach(function (el) {
        if (!el) return;
        el.style.transition = 'opacity 1000ms ease';
        el.style.opacity = el === wasteLabel ? 1 : 0.85;
      });
    }
  });
  if (reduce) {
    if (fill) fill.style.opacity = 1;
    if (waste) waste.style.opacity = 0.85;
    if (wasteLabel) wasteLabel.style.opacity = 1;
  }

  /* ---------- module: eccentric overload ---------------------------------
     One rep: 38.6 lb lifting, 59.0 lb lowering — both Speede's own figures.
     The travelling value never leaves that band.                          */
  (function () {
    var up = document.querySelector('[data-ec-up]');
    if (!up) return;
    var dn = document.querySelector('[data-ec-dn]');
    var fill = document.querySelector('[data-ec-fill]');
    var dot = document.querySelector('[data-ec-dot]');
    var lab = document.querySelector('[data-ec-lab]');
    var vEl = document.querySelector('[data-ec-v]');
    var pEl = document.querySelector('[data-ec-p]');
    var UP = 'M18,152 C110,148 160,110 250,98';
    var DN = 'M250,98 C350,84 400,44 502,32';
    up.setAttribute('d', UP); dn.setAttribute('d', DN);
    fill.setAttribute('d', DN + ' L502,190 L250,190 Z');
    var lu = up.getTotalLength(), ld = dn.getTotalLength();
    up.style.strokeDasharray = lu; dn.style.strokeDasharray = ld;
    if (reduce) { up.style.strokeDashoffset = 0; dn.style.strokeDashoffset = 0;
                  fill.setAttribute('opacity', .85); return; }
    up.style.strokeDashoffset = lu; dn.style.strokeDashoffset = ld;
    loopWhileVisible(up, function (p) {
      var e = p < .82 ? p / .82 : 1;                 // draw, then hold
      var u = Math.min(1, e / .42), d = Math.max(0, Math.min(1, (e - .42) / .58));
      up.style.strokeDashoffset = lu * (1 - u);
      dn.style.strokeDashoffset = ld * (1 - d);
      fill.setAttribute('opacity', (d * .85).toFixed(2));
      lab.setAttribute('opacity', d > .35 ? 1 : 0);
      if (d > 0) { var q = dn.getPointAtLength(ld * d);
        dot.setAttribute('cx', q.x); dot.setAttribute('cy', q.y); dot.setAttribute('opacity', 1); }
      else dot.setAttribute('opacity', 0);
      if (vEl) vEl.textContent = (38.6 + (59.0 - 38.6) * d).toFixed(1);
      if (pEl) pEl.textContent = '+' + Math.round(53 * d);
    }, 5200);
  })();

  /* ---------- module: five vs fifteen ------------------------------------
     Both columns cycle one rep at a time across the same period. Five land at
     full effort; fifteen barely register. The rhythm is the argument.      */
  (function () {
    var hosts = document.querySelectorAll('[data-tally]');
    if (!hosts.length) return;
    var cols = [];
    Array.prototype.forEach.call(hosts, function (host) {
      var n = parseInt(host.getAttribute('data-tally'), 10);
      for (var i = 0; i < n; i++) host.appendChild(document.createElement('i'));
      cols.push({ n: n, dots: host.querySelectorAll('i'), last: -1 });
    });

    // everything rests lit; the loop only moves the working rep
    cols.forEach(function (c) {
      Array.prototype.forEach.call(c.dots, function (d) { d.classList.add('lit'); });
    });
    if (reduce) return;

    loopWhileVisible('.tally', function (p) {
      cols.forEach(function (c) {
        var i = Math.min(c.n - 1, Math.floor(p * c.n));
        if (i === c.last) return;
        if (c.last >= 0) c.dots[c.last].classList.remove('hot');
        c.dots[i].classList.add('hot');
        c.last = i;
      });
    }, 5200);
  })();

  /* ---------- looping instrument animations ------------------------------
     Both run continuously while on screen and idle when off screen. The
     machine does reps continuously; a one-shot draw stopped dead and read
     as a static chart.                                                    */
  function loopWhileVisible(hostSel, tick, period) {
    // observe a block-level ancestor — IntersectionObserver on raw SVG
    // children is unreliable and silently stalls the loop
    var host = typeof hostSel === 'string' ? document.querySelector(hostSel) : hostSel;
    if (host && host.ownerSVGElement) host = host.ownerSVGElement.parentNode || host;
    if (!host || reduce) return;
    var raf = null, t0 = null, live = false;
    function frame(ts) {
      if (!live) return;
      if (t0 === null) t0 = ts;
      tick(((ts - t0) % period) / period, ts);
      raf = requestAnimationFrame(frame);
    }
    if (!('IntersectionObserver' in window)) { live = true; raf = requestAnimationFrame(frame); return; }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && !live) { live = true; t0 = null; raf = requestAnimationFrame(frame); }
        else if (!e.isIntersecting && live) { live = false; if (raf) cancelAnimationFrame(raf); }
      });
    }, { threshold: 0.12 }).observe(host);
  }

  /* ---------- the HUD ----------------------------------------------------
     A live rebuild of Speede's own screen. Every figure is theirs: 38.6
     lb/cable and the 5/6 rep counter are read off 9-image.jpg, 59.0 is the
     eccentric figure from their teaser. The travelling value only ever moves
     between those two published anchors — nothing outside their own range. */
  (function () {
    var trace = document.querySelector('[data-hud-trace]');
    if (!trace) return;
    var fillEl = document.querySelector('[data-hud-fill]');
    var head   = document.querySelector('[data-hud-head]');
    var bar    = document.querySelector('[data-hud-bar]');
    var badge  = document.querySelector('[data-hud-badge] b');
    var loadEl = document.querySelector('[data-hud-load]');
    var repEls = document.querySelectorAll('[data-rep-count]');

    var W = 560, H = 220, TOP = 26, BOT = 196;
    var CONCENTRIC = 38.6, ECCENTRIC = 59.0;      // Speede's own figures

    // six reps: each one lifts (concentric) then lowers harder (eccentric)
    var pts = [], N = 240;
    for (var i = 0; i <= N; i++) {
      var t = i / N, phase = (t * 6) % 1;
      var lift = Math.sin(phase * Math.PI);                 // the rep arc
      var ecc  = phase > 0.5 ? Math.pow((phase - 0.5) * 2, 1.4) : 0;
      var v = 0.34 + lift * 0.34 + ecc * 0.30;              // 0..1 of the band
      v += Math.sin(t * 61) * 0.012;                        // fine texture
      pts.push({ x: t * W, y: BOT - v * (BOT - TOP), v: v });
    }
    var d = pts.map(function (p, i) {
      return (i ? 'L' : 'M') + p.x.toFixed(1) + ',' + p.y.toFixed(1);
    }).join('');
    trace.setAttribute('d', d);
    if (fillEl) fillEl.setAttribute('d', d + 'L' + W + ',' + H + 'L0,' + H + 'Z');

    var hLine = head.querySelector('line');
    var hDots = head.querySelectorAll('circle');
    var lastRep = -1;
    loopWhileVisible('[data-hud-trace]', function (p) {
      var idx = Math.min(pts.length - 1, Math.round(p * (pts.length - 1)));
      var pt = pts[idx];
      hLine.setAttribute('x1', pt.x); hLine.setAttribute('x2', pt.x);
      hDots[0].setAttribute('cx', pt.x); hDots[0].setAttribute('cy', pt.y);
      hDots[1].setAttribute('cx', pt.x); hDots[1].setAttribute('cy', pt.y);
      if (bar) bar.style.height = (12 + pt.v * 80).toFixed(1) + '%';
      // interpolate strictly between Speede's two published figures
      var val = CONCENTRIC + (pt.v - 0.34) / 0.64 * (ECCENTRIC - CONCENTRIC);
      val = Math.max(CONCENTRIC, Math.min(ECCENTRIC, val));
      if (badge)  badge.textContent  = val.toFixed(1);
      if (loadEl) loadEl.textContent = val.toFixed(1);
      var rep = 1 + Math.floor(p * 6);
      if (rep !== lastRep) {
        lastRep = rep;
        Array.prototype.forEach.call(repEls, function (el) { el.textContent = rep; });
      }
    }, 9000);
  })();

  /* force readout — playhead rides the curve, rep counter cycles 1/6 → 6/6.
     Every value it passes through is on the curve drawn from Speede's own
     screen. Nothing is invented. */
  var curveLine = document.querySelector('[data-curve-line]');
  var playhead  = document.querySelector('[data-playhead]');
  var repEl     = document.querySelector('[data-rep-count]');
  if (curveLine && playhead && curveLine.getTotalLength) {
    var clen = curveLine.getTotalLength();
    var dot = playhead.querySelector('circle');
    var halo = playhead.querySelectorAll('circle')[1];
    var vline = playhead.querySelector('line');
    var lastRep = -1;
    loopWhileVisible('[data-curve-line]', function (p) {
      // ease in and out at the turnaround so it reads as a rep, not a scan
      var e = p < 0.5 ? (1 - Math.cos(Math.PI * p * 2)) / 2 : (1 + Math.cos(Math.PI * (p - 0.5) * 2)) / 2;
      var pt = curveLine.getPointAtLength(e * clen);
      playhead.setAttribute('opacity', '1');
      dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y);
      halo.setAttribute('cx', pt.x); halo.setAttribute('cy', pt.y);
      vline.setAttribute('x1', pt.x); vline.setAttribute('x2', pt.x);
      if (repEl) {
        var rep = 1 + Math.floor(p * 6);
        if (rep !== lastRep) { repEl.textContent = rep; lastRep = rep; }
      }
    }, 4200);
  }

  /* sticking-point diagram — a measurement sweep that reports the gap
     between what you could handle and what a fixed weight gives you. */
  var capLine  = document.querySelector('[data-speede-line]');
  var sweep    = document.querySelector('[data-sweep]');
  if (capLine && sweep && capLine.getTotalLength) {
    var caplen = capLine.getTotalLength();
    var sLine  = sweep.querySelector('line');
    var sCap   = sweep.querySelector('[data-sweep-cap]');
    var sFlat  = sweep.querySelector('[data-sweep-flat]');
    var sGap   = sweep.querySelector('[data-sweep-gap]');
    var sLabel = sweep.querySelector('[data-sweep-label]');
    var FLAT_Y = 230;                     // the fixed weight, set at the weakest point
    loopWhileVisible('[data-speede-line]', function (p) {
      var e = (1 - Math.cos(Math.PI * p * 2)) / 2;   // sweep out and back
      var pt = capLine.getPointAtLength(e * caplen);
      sweep.setAttribute('opacity', '1');
      sLine.setAttribute('x1', pt.x); sLine.setAttribute('x2', pt.x);
      sCap.setAttribute('cx', pt.x);  sCap.setAttribute('cy', pt.y);
      sFlat.setAttribute('cx', pt.x); sFlat.setAttribute('cy', FLAT_Y);
      sGap.setAttribute('x1', pt.x); sGap.setAttribute('x2', pt.x);
      sGap.setAttribute('y1', pt.y); sGap.setAttribute('y2', FLAT_Y);
      // no invented percentage here — the gap itself is the argument
      sLabel.setAttribute('x', pt.x);
      sLabel.setAttribute('y', Math.max(pt.y - 16, 26));
      sLabel.textContent = (FLAT_Y - pt.y) > 22 ? 'UNUSED' : '';
    }, 7000);
  }

  /* ---------- mode chips ------------------------------------------------- */
  var chips = document.querySelectorAll('.chip');
  Array.prototype.forEach.call(chips, function (c) {
    c.addEventListener('click', function () {
      Array.prototype.forEach.call(chips, function (o) {
        o.classList.remove('on'); o.setAttribute('aria-pressed', 'false');
      });
      c.classList.add('on'); c.setAttribute('aria-pressed', 'true');
    });
  });

  /* ---------- waitlist form ---------------------------------------------
     Front-end only in this build. Speede's live page posts to Klaviyo
     (company U89tzB / list U9q2ZP) — wire the endpoint back in on handoff. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-join]'), function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('input[type=email]');
      if (!input || !input.value || input.value.indexOf('@') < 1) {
        if (input) { input.focus(); input.style.borderColor = '#ff6b6b'; }
        return;
      }
      input.style.borderColor = '';
      var ok = form.parentNode.querySelector('[data-ok]');
      form.hidden = true;
      if (ok) { ok.hidden = false; }
    });
  });
})();
