# Where this left off — 29 Jul 2026

## Start the preview

```bash
cd "/Users/graysonchoate/Documents/speede-fit-rebuild" && python3 -m http.server 3000 --directory build
```
→ **http://localhost:3000** (hard-refresh with ⌘+Shift+R after any video change)

---

## Done in this round

**The hero is full-bleed**, WHOOP-style — video across the whole section, nav floating over
it, copy overlaid. Same five beats as before, re-exported at 1600×900 instead of the old
1000×1000 letterboxed square, because a square file can't fill a wide background.

The scrim was tuned by sampling every second across the full loop and measuring against the
**worst** frame: background behind the copy peaks at 36 (page black is 8).

---

## Next, in order — from the 29 Jul huddle with Simon

1. **Centre the tagline, logos beneath it.**
   `Pro Level Training. / Built Around You.` on its own line, centred, with the four league
   marks below it. Then the carousel full-width under both — three tiers, each wider than the
   last, funnelling into the motion.
   It should be the **only** centred block on the page; one reads as deliberate, two reads as
   indecision.

2. **Kill the marquee, promote the athlete chips.**
   Simon on the marquee: *"it's a little gimmick, it's very AI."* Delete it. The eight athlete
   chips take that slot instead — bigger, running as an endless carousel. Eight is enough to
   read as continuous.

3. **Layer photography into the data sections.**
   The note from Simon is that the data sections feel synthetic without a human element —
   WHOOP puts the numbers *on* an image rather than on black.
   - **The 500 section** — the bench-press shot, large, heavily darkened, figure opposite the
     numeral. A presence you half-see; the 500 stays the hero.
   - **The science section** — the B&W hand-on-bar macro, woven *behind* the cards so they
     partly occlude it. Grayson's phrasing: *"impressions of an image around them."*
     It's the right pick because it's abstract and low-detail — the bent-over row has too much
     going on and would fight the readouts.
   - Keep motion in the hero only. Those sections already have four things animating.

---

## Source media triage (`source-media/`)

**Use:**
- `Screenshot …12.14.41 PM.png` — bench press, tattooed arm, Speede cap, concrete. The "hard rep".
- `Screenshot …12.15.23 PM.png` — B&W macro, hand on the bar. Abstract, low-detail, ideal behind cards.
- `Screenshot …12.15.35 PM.png` — B&W bent-over row against brick. Clean silhouette.
- `clip1.mov` / `clip2.mov` — Speede's own brand film. B&W, gritty, already the site's palette.
  ⚠️ `WORK FOR IT.` is burned into the footage through most of it; only the last ~1.5s is clean.
  Any use needs a crop above the type line, or careful segment selection.

**Don't use:**
- `Screenshot …12.26.54 PM.png`, `Screenshot …12.29.34 PM.png` and `clip4.mov` — all shot on a
  trade-show floor. Lanyards, booths, expo carpet, someone filming on a phone. Documentation,
  not brand photography.
- `clip3.mov` — usable but warm/brown, a different grade from clips 1 and 2. Won't sit beside
  them without work.

No audio from any clip.

---

## Still open from earlier

- **The waitlist form is front-end only.** Klaviyo company `U89tzB`, list `U9q2ZP` — noted in `main.js`.
- **League marks need Speede's sign-off.** Protected trademarks; the Olympic symbol under
  36 U.S.C. 220506. Speede's own site uses text instead.
- **Speede's current site publishes Hydrow-branded hardware** (visible in `5-image.jpg` and
  `9-image.jpg`). Small and dark on their build so it passes unnoticed — but worth raising.

---

## A note on how to work in these files

Two stylesheet blowups this session, both the same cause: slicing CSS or HTML by index using
`str.find()` as an anchor. When the anchor no longer exists `find()` returns -1 and the slice
runs to the end of the file. The first cost a manual reconstruction; the second was recovered
with one `git checkout`.

**Use exact-string replacement with an assertion on every edit.** Commit before any structural
change.
