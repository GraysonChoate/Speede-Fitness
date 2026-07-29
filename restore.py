"""Restore the markup a bad regex deleted: the faces container, the marquee,
the whole number section, and the science section's opening (copy + HUD)."""
import re

P = "build/index.html"
h = open(P).read()

# ---- 1. the faces container, back inside the proof strip -------------------
lead_close = h.find('        </div>\n      </div>\n\n\n    </div>')
assert lead_close != -1, "proof strip shape not as expected"
h = h.replace('        </div>\n      </div>\n\n\n    </div>',
              '        </div>\n      </div>\n      <div class="faces" data-faces></div>\n    </div>\n  </div>', 1)

REBUILT = '''
<!-- ====================== MARQUEE ====================== -->
<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <span>500 lbs React Mode</span><span>5 reps = 38</span><span>Folds flat</span><span>No guesswork</span><span>Athlete-built</span><span>Real-time force</span>
    <span>500 lbs React Mode</span><span>5 reps = 38</span><span>Folds flat</span><span>No guesswork</span><span>Athlete-built</span><span>Real-time force</span>
  </div>
</div>

<!-- ====================== THE NUMBER ====================== -->
<section class="sec sec--band" id="number">
  <!-- Compression frame. Abstract atmosphere only. Geometry is anchored to the
       real column grid: the box runs from just outside the container to the
       centre of the 72px gutter, so it never reaches the copy or the rows. -->
  <div class="num-deco" data-numdeco aria-hidden="true">
    <svg class="nd-frame" viewBox="0 0 606 368" preserveAspectRatio="none">
      <g fill="none" stroke-linecap="square" shape-rendering="crispEdges">
        <g stroke="rgba(214,224,208,.52)" stroke-width="1.6">
          <path d="M2 2h92 M2 2v58"/>
          <path d="M604 2h-92 M604 2v58"/>
          <path d="M2 366h92 M2 366v-58"/>
          <path d="M604 366h-92 M604 366v-58"/>
        </g>
        <g stroke="rgba(150,178,138,.27)" stroke-width="1.2">
          <path d="M22 22h54 M22 22v34"/>
          <path d="M584 22h-54 M584 22v34"/>
          <path d="M22 346h54 M22 346v-34"/>
          <path d="M584 346h-54 M584 346v-34"/>
        </g>
      </g>
      <circle class="nd-node" cx="604" cy="366" r="3.4" fill="#b2ff59"/>
    </svg>

    <svg class="nd-bands" viewBox="0 0 150 620" preserveAspectRatio="none">
      <g class="nd-band-l" stroke="rgba(196,214,186,.42)" stroke-width="1.4" stroke-linecap="round">
        <line x1="0" y1="96"  x2="104" y2="96"/>
        <line x1="0" y1="168" x2="82"  y2="168"/>
        <line x1="0" y1="240" x2="118" y2="240"/>
        <line x1="0" y1="330" x2="74"  y2="330"/>
        <line x1="0" y1="402" x2="110" y2="402"/>
        <line x1="0" y1="474" x2="90"  y2="474"/>
      </g>
    </svg>

    <svg class="nd-gutter" viewBox="0 0 72 620" preserveAspectRatio="none">
      <g class="nd-band-c" stroke="rgba(196,214,186,.34)" stroke-width="1.2" stroke-linecap="round">
        <line x1="10" y1="150" x2="54" y2="150"/>
        <line x1="10" y1="212" x2="38" y2="212"/>
        <line x1="10" y1="274" x2="60" y2="274"/>
        <line x1="10" y1="336" x2="34" y2="336"/>
      </g>
      <g class="nd-loads" stroke="rgba(178,255,89,.26)" stroke-width="2" stroke-linecap="round">
        <line x1="20" y1="452" x2="20" y2="512"/>
        <line x1="32" y1="470" x2="32" y2="512"/>
        <line x1="44" y1="438" x2="44" y2="512"/>
        <line x1="56" y1="482" x2="56" y2="512"/>
      </g>
    </svg>

    <svg class="nd-rail" viewBox="0 0 60 620" preserveAspectRatio="none">
      <g stroke="rgba(214,224,208,.30)" stroke-width="1" shape-rendering="crispEdges">
        <line x1="12" y1="60"  x2="12" y2="230"/>
        <line x1="12" y1="262" x2="12" y2="392"/>
        <line x1="12" y1="428" x2="12" y2="566"/>
      </g>
      <g stroke="rgba(214,224,208,.44)" stroke-width="1" shape-rendering="crispEdges">
        <line x1="12" y1="76"  x2="34" y2="76"/><line x1="12" y1="100" x2="21" y2="100"/>
        <line x1="12" y1="124" x2="28" y2="124"/><line x1="12" y1="148" x2="21" y2="148"/>
        <line x1="12" y1="172" x2="38" y2="172"/><line x1="12" y1="196" x2="21" y2="196"/>
        <line x1="12" y1="278" x2="26" y2="278"/><line x1="12" y1="302" x2="21" y2="302"/>
        <line x1="12" y1="326" x2="33" y2="326"/><line x1="12" y1="350" x2="21" y2="350"/>
        <line x1="12" y1="444" x2="30" y2="444"/><line x1="12" y1="468" x2="21" y2="468"/>
        <line x1="12" y1="492" x2="36" y2="492"/><line x1="12" y1="516" x2="21" y2="516"/>
        <line x1="12" y1="540" x2="25" y2="540"/>
      </g>
      <circle class="nd-runner" cx="12" cy="0" r="1.9" fill="#b2ff59"/>
    </svg>

    <span class="nd-dots"></span>
    <svg class="nd-dust" viewBox="0 0 606 368" preserveAspectRatio="none">
      <g fill="rgba(214,224,208,.19)">
        <circle cx="58"  cy="46"  r="1.3"/><circle cx="146" cy="118" r="1.1"/>
        <circle cx="42"  cy="242" r="1.4"/><circle cx="556" cy="88"  r="1.2"/>
        <circle cx="520" cy="292" r="1.1"/><circle cx="188" cy="330" r="1.3"/>
        <circle cx="574" cy="196" r="1.2"/><circle cx="96"  cy="308" r="1.1"/>
      </g>
    </svg>
  </div>

  <div class="wrap number-grid">
    <div class="reveal">
      <p class="kicker">One number nobody else will say</p>
      <p class="bignum sheen reveal" data-count="500">500<small>lbs · React Mode</small></p>
    </div>
    <div class="reveal" style="--d:120ms">
      <h2><span class="hw">More resistance than</span><br>anything you're comparing it to.</h2>
      <p class="lead" style="margin-top:20px">
        Most machines hide their number — or cap out low. Ours is clean, ownable,
        and heavier. Here's the honest board:
      </p>
      <ul class="vs-list">
        <li class="us"><span class="vs-bar" style="--w:100%" aria-hidden="true"></span>
          <span class="who">SPEEDE — React Mode</span><span class="val">500 lbs</span></li>
        <li><span class="vs-bar" style="--w:50%" aria-hidden="true"></span>
          <span class="who">Tonal</span><span class="val">250 lbs</span></li>
        <li><span class="vs-bar" style="--w:20%" aria-hidden="true"></span>
          <span class="who">AMP</span><span class="val">100 lbs</span></li>
      </ul>
    </div>
  </div>
</section>

<div class="seam" data-seam aria-hidden="true"></div>
<!-- ====================== THE SCIENCE ====================== -->
<section class="sec" id="science">
  <!-- One continuous signal routed through the section's own gutters: it enters
       from both margins, converges below the readout, runs the spine between the
       two cards, splits, and frames the curve card from outside. -->
  <div class="sci-deco" data-scideco aria-hidden="true">
    <svg class="sci-l" viewBox="0 0 166 2000" preserveAspectRatio="none">
      <defs>
        <linearGradient id="scWashL" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#172119" stop-opacity=".72"/>
          <stop offset="1" stop-color="#080A09" stop-opacity="0"/>
        </linearGradient>
        <pattern id="scDotsL" width="26" height="26" patternUnits="userSpaceOnUse">
          <circle cx="3" cy="3" r="1.7" fill="#9AA39A" fill-opacity=".26"/>
          <circle cx="16" cy="16" r="1.3" fill="#8FD63F" fill-opacity=".22"/>
        </pattern>
        <pattern id="scHatchL" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
          <path d="M0 0V18" stroke="#9AA39A" stroke-opacity=".2" stroke-width="1.6"/>
        </pattern>
      </defs>
      <rect x="0" y="60" width="166" height="1880" fill="url(#scWashL)"/>
      <rect class="sci-dotfield" x="6" y="180" width="120" height="1560" fill="url(#scDotsL)" opacity=".7"/>
      <rect x="0" y="1720" width="112" height="210" fill="url(#scHatchL)" opacity=".5"/>
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M166 90H120Q88 90 88 122V560" stroke="#9AA39A" stroke-opacity=".40" stroke-width="2.4"/>
        <path d="M166 1178H128Q96 1178 96 1210V1930" stroke="#9AA39A" stroke-opacity=".40" stroke-width="2.4"/>
        <path d="M166 1178H140Q116 1178 116 1206V1902" stroke="#8FD63F" stroke-opacity=".30" stroke-width="2"/>
        <path d="M166 1178H112Q76 1178 76 1214V1954" stroke="#9AA39A" stroke-opacity=".24" stroke-width="1.8" stroke-dasharray="3 12"/>
      </g>
      <circle class="sci-node" cx="96" cy="1930" r="4" fill="#B2FF59" fill-opacity=".6"/>
    </svg>

    <svg class="sci-c" viewBox="0 0 1180 2000" preserveAspectRatio="none">
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M0 90H556Q616 90 616 150V596" stroke="#9AA39A" stroke-opacity=".40" stroke-width="2.4"/>
        <path d="M1180 90H676Q616 90 616 150" stroke="#9AA39A" stroke-opacity=".34" stroke-width="2.2"/>
        <path d="M0 118H528Q590 118 590 178V584" stroke="#8FD63F" stroke-opacity=".28" stroke-width="2"/>
        <path d="M1180 118H704Q642 118 642 178V584" stroke="#9AA39A" stroke-opacity=".24" stroke-width="1.8" stroke-dasharray="3 12"/>
        <path class="sci-route" d="M616 596V640Q616 668 604 690Q592 712 590 736V1146"
              stroke="#9AA39A" stroke-opacity=".42" stroke-width="2.6"/>
        <path d="M642 584V648Q642 676 620 700" stroke="#8FD63F" stroke-opacity=".26" stroke-width="1.8"/>
        <path d="M590 1146V1150Q590 1178 558 1178H0" stroke="#9AA39A" stroke-opacity=".40" stroke-width="2.4"/>
        <path d="M590 1146V1150Q590 1178 622 1178H1180" stroke="#9AA39A" stroke-opacity=".40" stroke-width="2.4"/>
        <path d="M590 1160Q590 1196 552 1196H0" stroke="#9AA39A" stroke-opacity=".22" stroke-width="1.6" stroke-dasharray="3 12"/>
        <path d="M590 1160Q590 1196 628 1196H1180" stroke="#9AA39A" stroke-opacity=".22" stroke-width="1.6" stroke-dasharray="3 12"/>
      </g>
      <circle class="sci-conv" cx="616" cy="640" r="5" fill="#B2FF59" fill-opacity=".72"/>
      <circle class="sci-glint" r="4.5" fill="#B2FF59"/>
    </svg>

    <svg class="sci-r" viewBox="0 0 166 2000" preserveAspectRatio="none">
      <defs>
        <linearGradient id="scWashR" x1="1" y1="0" x2="0" y2="0">
          <stop offset="0" stop-color="#172119" stop-opacity=".68"/>
          <stop offset="1" stop-color="#080A09" stop-opacity="0"/>
        </linearGradient>
        <pattern id="scDotsR" width="26" height="26" patternUnits="userSpaceOnUse">
          <circle cx="3" cy="3" r="1.7" fill="#9AA39A" fill-opacity=".24"/>
          <circle cx="16" cy="16" r="1.3" fill="#8FD63F" fill-opacity=".2"/>
        </pattern>
        <pattern id="scHatchR" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)">
          <path d="M0 0V18" stroke="#9AA39A" stroke-opacity=".2" stroke-width="1.6"/>
        </pattern>
      </defs>
      <rect x="0" y="60" width="166" height="1880" fill="url(#scWashR)"/>
      <rect class="sci-dotfield" x="40" y="180" width="120" height="1560" fill="url(#scDotsR)" opacity=".62"/>
      <rect x="54" y="1720" width="112" height="210" fill="url(#scHatchR)" opacity=".5"/>
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M0 90H46Q78 90 78 122V560" stroke="#9AA39A" stroke-opacity=".36" stroke-width="2.4"/>
        <path d="M0 1178H38Q70 1178 70 1210V1930" stroke="#9AA39A" stroke-opacity=".40" stroke-width="2.4"/>
        <path d="M0 1178H26Q50 1178 50 1206V1902" stroke="#8FD63F" stroke-opacity=".30" stroke-width="2"/>
        <path d="M0 1178H54Q90 1178 90 1214V1954" stroke="#9AA39A" stroke-opacity=".24" stroke-width="1.8" stroke-dasharray="3 12"/>
      </g>
      <circle class="sci-node" cx="70" cy="1930" r="4" fill="#B2FF59" fill-opacity=".6"/>
    </svg>
  </div>

  <div class="wrap">
    <div class="mech-grid">

      <div class="reveal">
        <p class="kicker">The science, simplified</p>
        <h2><span class="hw">Strength that</span><br>answers back.</h2>
        <p class="reps" aria-hidden="true">
          <span class="r">5</span><span class="arrow">&#8594;</span><span class="r">38</span>
        </p>
        <p class="lead">
          The machine reads how hard you push and matches it — every inch of every rep.
          Lift at 38 lbs of force, lower against 59. That's
          <b>isokinetic + eccentric overload</b>: more real work in fewer reps, without a
          rack of plates or a guess about the weight.
          <b>Five honest reps do what fifteen sloppy ones can't.</b>
        </p>
      </div>

      <!-- Speede's own interface, rebuilt in code so every figure is exact -->
      <div class="hud reveal" style="--d:120ms">
        <div class="hud-top">
          <span class="hud-move">Bent Over Rows</span>
          <span class="hud-mode"><i class="live-dot" aria-hidden="true"></i>React Mode</span>
        </div>

        <div class="hud-stage">
          <svg class="hud-graph" viewBox="0 0 560 220" role="img"
               aria-label="Live force trace for a set of bent over rows, running between 38.6 and 59 pounds per cable.">
            <defs>
              <linearGradient id="hudFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#b2ff59" stop-opacity=".30"/>
                <stop offset="100%" stop-color="#b2ff59" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <g stroke="rgba(255,255,255,.055)">
              <line x1="0" y1="45" x2="560" y2="45"/><line x1="0" y1="95" x2="560" y2="95"/>
              <line x1="0" y1="145" x2="560" y2="145"/><line x1="0" y1="195" x2="560" y2="195"/>
            </g>
            <path data-hud-fill fill="url(#hudFill)" d=""/>
            <path data-hud-trace fill="none" stroke="#e9f2df" stroke-width="2.2"
                  stroke-linecap="round" stroke-linejoin="round" d=""/>
            <g data-hud-head>
              <line y1="0" y2="220" stroke="rgba(178,255,89,.2)" stroke-width="1"/>
              <circle r="11" fill="#b2ff59" opacity=".16"/>
              <circle r="4.5" fill="#b2ff59"/>
            </g>
          </svg>

          <div class="hud-bar" aria-hidden="true"><i data-hud-bar></i></div>
        </div>

        <div class="hud-badge" data-hud-badge>&#9670; <b>55.3</b></div>

        <div class="hud-figs">
          <div class="hud-fig hud-fig--main">
            <span class="hud-v" data-hud-load>38.6</span><span class="hud-u">lb/cable</span>
          </div>
          <div class="hud-fig">
            <span class="hud-v"><b data-rep-count>5</b><span class="hud-u">/6</span></span>
            <span class="hud-k">Reps</span>
          </div>
          <div class="hud-fig">
            <span class="hud-v hud-v--g">59.0</span><span class="hud-k">Eccentric</span>
          </div>
        </div>
      </div>

    </div>
'''

marker = '\n    <!-- The two remaining chapters from the film, rebuilt live.'
i = h.find(marker)
assert i != -1, "mods marker not found"
h = h[:i] + REBUILT + h[i:]

open(P, "w").write(h)
print("restored")
