# Speede — what changed, and why

The rebuild is one static page: `build/index.html` + `styles.css` + `main.js`.
`/original` is untouched — open both side by side.

```bash
python3 -m http.server 3000 --directory build
```
→ **http://localhost:3000**

---

## Deliberately preserved

**Their copy.** Every headline and body paragraph on the page is Speede's own writing. Nothing was
replaced with agency copy. That includes the lines the brand is actually built on:

- "Stronger starts soon." / "You've never seen this."
- "Five honest reps do what fifteen sloppy ones can't."
- "Pro-grade force. Anyone's living room."
- "Most machines hide their number — or cap out low."
- "We're not showing you everything. Not yet."
- "The whole gym. One mat." / "Folds flat" / "Snap-in precision"
- The four personas: the athlete, the comeback, the 60-year PR, the first-timer
- The full hero lede and the footer fine print, verbatim

**Their design system.** Exact hexes, unchanged: `#080a09` `#0e120f` `#12160f` `#f4f7f0` `#9aa39a`
`#b2ff59` `#8fd63f`. Space Grotesk for display, Inter for body. 18px / 12px / pill radii. The
green-biased neutrals — the thing that stops it reading as a stock dark theme — are intact.

**Their structure.** The teaser's narrative spine was already good and is still here: hook → the
number → the science → the tease → who it's for → proof → waitlist.

**Their assets.** All eight photographs and the logo are Speede's own files.

---

## What changed

### 1. Proof moved up, and got faces
**Was:** one anonymous quote — *"— Pro athlete, first session"* — under four flat league pills, in
section five.
**Now:** a named roster strip sits directly under the hero, before the number. The full proof wall
sits after the mechanism with six named athletes, their portraits, and their own words.
**Why:** six professional athletes is the most credible thing Speede owns, and it was the smallest
thing on the page. Evidence should land before the claim it supports.

The portraits came from Speede's own CDN — they belonged to the deleted `/pages/athlete-full`.
They're black-and-white on black, shot as a consistent set, so they sit inside the palette.

### 2. A running order built on evidence
**Now:** hook + proof strip → 500 → mechanism → machine → who it's for → proof wall → waitlist.
**Why:** the number only means something once you believe they're serious. Proof first, then the
number as the reason for the reaction.

### 3. The science went deep; the product stayed teased
**Was:** the mechanism got 60 words and a small chart.
**Now:** a full instrument readout plus a second diagram explaining *why* a fixed weight fails.
The product photography is still withheld — darkened, vignetted, cropped.
**Why:** "we're not showing you everything" should never mean "we're vague about why it works."
The science is what earns the tease.

### 4. Two new assets
**The force readout.** Speede's line "5 reps = 38" is a literal transcription of their own screen
(`38.6 LB/CABLE — 5/6`, visible in `9-image.jpg`). So it's built as an instrument, not a chart:
tabular numerals, live dot, concentric/eccentric split, curve drawing on as you reach it.

**The sticking-point diagram.** A fixed weight is a flat line set at your weakest point; everything
above it is capacity you never load. Speede's line tracks the curve. Nobody has drawn this —
not Speede, not Tonal. It's the clearest answer to "why does this work."

Both use only Speede's real numbers. Nothing longitudinal was invented.

### 4b. Typography
**Space Mono added — for data only.** Same designer and skeleton as Space Grotesk, so it introduces
no new identity, but it makes `38.6 lb/cable` read as machine output instead of marketing. Confined
to the readout, rep counter, comparison values, league marks and the hero chip. 19KB, self-hosted.

Also: a **tracking ladder** tied to size (`-.052em` on the 500 → `+.17em` on labels) instead of one
flat value; **section numbering** (`01`, `02`, `02.1`…) in mono; **mixed-weight headlines** with the
setup at 500 and the payload at 700; **slashed-zero tabular figures** on every number; **hanging
quote marks** on the athlete cards; `text-wrap: pretty` on body copy.

### 4c. The hero broke the container
**Was:** the image sat in a card inside the 1180px grid — the same shape as their current site,
which is why the rebuild still read as familiar.
**Now:** the media runs off the right edge of the viewport, no border on that side, radius on the
left only. Copy and form are untouched on the 1180 grid. The readout chip straddles the media's
bottom edge, giving the hero a foreground plane instead of one flat card.

### 4d. Motion in the hero
A **9.3-second loop** now sits where the still was: a slow push-in through the room, crossfading to
the machine folding flat and sliding under the bed. Both clips were generated from Speede's own
photographs — the camera moves, the hardware doesn't. Both ends fade through black so the loop wrap
is seamless. 890KB, WebM + MP4, poster fallback.

It pauses when scrolled off-screen, and under `prefers-reduced-motion` it never plays at all —
the poster frame holds.

### 4e. Grain and surface
Fine film grain over the whole page (inline SVG turbulence, no request) to break up flat digital
black. The band sections pick up a speckled texture derived from the mat itself. One slow specular
sweep across the 500 and the CTAs, once, on entry.

### 4f. Living portraits
All eight athlete stills are now **subtle looping portraits** — the person breathes, blinks, and a
small real smile forms. Generated from Speede's own photographs, so likeness, grayscale, lighting,
background and framing are unchanged. Each is a **ping-pong loop** (forward then reversed) so
neutral → smile → neutral cycles with no visible jump.

The still remains the poster and the clip fades in only once it can actually play, so a slow or
missing video never leaves a hole — you just get the photograph. Sources attach only when the card
nears the viewport, and everything pauses off-screen. Under `prefers-reduced-motion` the videos
don't render at all.

**42–114KB each, ~700KB for all eight** — several are smaller than the JPEG they sit over.
Sesselmann took three attempts; the first two failed outright at the model.

### 4g. The film became live modules
The data film was deleted — video of a UI is blurry where the UI itself is not. Its four chapters
now exist as coded elements beside the copy they explain:
- **01 It reads you** → the HUD in the science section
- **02 Eccentric overload** → a live module: white lifting curve into green lowering curve, `38.6`
  holding while the lowering figure travels to `59.0` and `+53`
- **03 The number** → the counting 500 with its scroll-filled comparison bars
- **04 Five, not fifteen** → five green blocks lighting fast against fifteen greys crawling in

### 4h. Hero framing and cache-busting
The hero panel is roughly square but the clips are 16:9, so `object-fit: cover` was discarding 44%
of every frame. The montage is now rendered to **fit the whole frame inside the square**, letterboxed
against the page black — invisible in place, and nothing is cropped.

Video URLs now carry a build hash. Re-rendering under the same filename meant browsers served a
cached copy, which hid several rounds of changes.

### 4i. Atmospheric treatments, built to the supplied specs
Each section in `design-reference/section-references/` has its own instruction
file. All five are built, and each is anchored to measured geometry rather than a
stretched overlay, so nothing drifts onto copy at other widths.

- **Hero** — the supplied `hero-board-mapped-overlay.svg` used verbatim: angular
  smoked exposure, broken calibration rail, dot-matrix blocks, registration marks
  and lime glints. Fitted to the real perimeter, since the art's field is 19% of
  its width but the copy column starts at 13.6%.
- **The number** — compression frame: open corner brackets with inset echoes,
  six pressure bands from the left gutter, shorter bands and load bars in the
  central 72px gutter, calibration rail, dot field, one lime node.
- **The science** — one continuous signal in three CSS-anchored pieces. Traces
  enter from both margins, converge below the readout, run the spine between the
  two cards, split, and frame the curve card from outside. A glint travels the
  whole route over 14s.
- **The machine** — upper exposure haze, staggered edge scan stacks in both
  gutters, an incomplete bracket frame around the photo row (35px clear top,
  59px bottom), and lower scan residue.
- **Built for athletes** — one continuous textured surface feathered away from
  the headline and cards, an incomplete perimeter, registration corners, gutter
  guides and a shared baseline with four anchor nodes.
- **Final CTA** — force event: upper canopy, seven pressure rails per side,
  broken brackets, activation field, convergence release. Entry sequence plays
  once and holds; only one faint side pulse repeats. Hover or focus the form and
  a pulse runs the lower convergence.

Every treatment idles when its section is off screen and renders a composed
static state under `prefers-reduced-motion`.

### 4j. Hover-activated motion
Both the athlete portraits and the four persona cards play only on hover or
keyboard focus. Sources aren't fetched until first hover, the clip fades in only
once it can play, and it resets on mouse-out — the photograph is always the
resting state.

The persona clips run **full length, forward only**: each contains a complete rep
that returns to its start, so it loops on its own. An earlier ping-pong version
reversed the action and read as a rewind.

### 4k. Proof strip leads with the marks
The strip under the hero now opens with **Pro Level Training. Built Around You.**
beside the four league marks, then the eight-athlete roster. The proof section
headline changed to the same line.

⚠️ The league marks are supplied by the client and are protected trademarks —
the Olympic symbol under 36 U.S.C. 220506. Speede's own site uses text instead.
They should confirm permission before this goes anywhere public.

### 5. Vertical rhythm
**Was:** `padding: 90px 0` on every section.
**Now:** a five-step scale, `--sp-xs` through `--sp-xl`. The hero and the final CTA own the most
space; utility rows own the least.
**Why:** when everything gets the same room, nothing reads as more important than anything else.

### 6. The hero stopped competing with itself
**Was:** "Stronger starts soon." and "You've never seen this." stacked in one H1, the second in
grey — reading as an afterthought.
**Now:** the H1 is the promise; the tease is a separate, lighter line beneath it.
**Why:** two hooks doing two jobs need two weights.

### 7. A middle type register
**Was:** the scale jumped from 220px to 15px with almost nothing between, so body copy read as
small print.
**Now:** `--t-lead` at 18–23px carries every lede and explanatory paragraph.

### 8. One CTA label
**Was:** "Get early access" / "Notify me" / "Join the waitlist" — three labels, one action.
**Now:** **Get early access** everywhere. It was already their nav label, and it says what you get
rather than what you do.

### 9. Motion
**Now:** staggered scroll reveals, the force curve drawing on in view, the 500 counting up once,
hover states throughout. The marquee slowed from 26s to 34s and gained edge masks.
**Why:** nothing moved on scroll before, and the marquee was the busiest thing on the page.
Backwards.

### 10. Accessibility
- `prefers-reduced-motion` fully honored — **absent entirely before**
- Alt text written for all eight photographs — **four shipped with empty `alt`**
- Body copy lifted to `--muted-2` (`#b6bdb4`) for AA contrast on `#0e120f`
- Skip link, visible focus rings, semantic landmarks, labelled form inputs
- Mode chips are real buttons with `aria-pressed`; SVGs carry descriptive labels

### 11. Responsive
**Was:** one breakpoint at 860px, where the nav links simply vanished.
**Now:** 1080 / 940 / 620, each doing real work. Verified with no horizontal overflow at 1440 and 390.

### 12. Weight
**Was:** a Shopify page loading 60+ third-party scripts — Affirm, TalkShopLive, Facebook Pixel,
GTM, a GDPR widget, the full theme bundle — to render one static page with one email field.
**Now:** three files, two self-hosted variable fonts, zero third-party requests, no framework.
**Why:** the company is called Speede.

---

## Verified

Rendered headless at 1440×900 and 390×844: **no console errors, no failed requests, no broken
images, no horizontal overflow.** Screenshots in `shots/`.

---

## Flags for you

**The waitlist form is front-end only.** Their live page posts to Klaviyo (company `U89tzB`,
list `U9q2ZP`). Wire the endpoint back in on handoff — noted in `main.js`.

**Old-product language was kept out on purpose.** No "2,000 lbs", no Nemesis or Excentric™, no
$5,995, no 32" screen. All of that belongs to the discontinued Challenger. See Appendix 0 of
`BRAND-BRIEF.md`.

**Quotes were filtered.** Every athlete quote is Speede's own, and any quote naming a discontinued
mode was excluded — including Simmons' strongest line, which named Nemesis Mode.

**"Backed by", not "owns equity in".** The equity claim is from a 2022 press release, pre-Hydrow.
Treated as historical.

**NBA and Olympic are backed on-page.** Lauren Sesselmann and Mason Plumlee appear in the roster
strip and are named beneath the league row, so no pill claims something the page can't show.

**A third clip was generated and deliberately left out.** A macro of the snap-in detail
(`gen/clipB-snap.mp4`) came out beautifully — but it renders the **`Hydrow Link` wordmark and `h`
logo large and legible**, because they are on the actual hardware in Speede's own source photo
(`5.jpg`). The generation was faithful; the branding is real. Cropping can't remove it — the mark
sits on the attachment itself.

Worth raising with Speede regardless: **their current site is already publishing photography of
Hydrow-branded hardware.** It's small and dark in the existing card, so it passes unnoticed; in
motion at macro scale it does not. The static "Snap-in precision" card is unchanged from their own
site, so we amplify nothing.

---

## Photography layered into the data sections

Simon asked for the team's own stills to be woven into the two vector-heavy
sections, with the caveat that nothing already built there gets disrupted. Both
photographs are graded down **in the file** rather than under a CSS scrim, so
there is only ever one thing dimming each picture. `prep-layers.py` regenerates
them at 760/1100/1600.

**The 500 — `effort`.** The bench-press still sits behind the band, masked to
nothing across the left half so the numeral never lands on the picture. The
athlete reads in the right half, where the comparison rows are opaque and crop
into him. Two passes were needed: the first crop was near-square, so
`object-fit: cover` blew him up until he read as wall rather than a person, and
the concrete was bright enough to flatten the headline. The band-shaped crop and
a much heavier grade fixed both. Below 940px there is no "opposite the numeral"
left to aim at, so the side fade becomes a vertical wash.

**The science — `grip`.** The B&W hand-on-bar macro is anchored to a `.mods-bed`
wrapper around the two live cards, so it is positioned off their real geometry
rather than a guessed offset. It bleeds past all four edges and the cards —
which are opaque — crop it back to slivers: the bar enters from the left margin
and disappears behind the first card. The deco, HUD, tally and curve diagram are
all untouched.
