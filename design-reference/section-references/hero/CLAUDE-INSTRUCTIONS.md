# Hero Media-Board Treatment

Use the existing hero exactly as built. Do not change its copy, layout, video,
controls, typography, spacing, or media crop. Add decoration only in the empty
black perimeter.

## Protected Zones

- Do not place texture behind or across the eyebrow, headline, supporting copy,
  email form, benefit row, navigation, video, or video badge.
- Keep at least 48px of clear space around every protected element.
- Decorative layers must use `pointer-events: none` and remain below content.

Do not add visible labels, numbers, words, callouts, legends, or annotations to
the hero. The visual treatment is entirely abstract.

## Visual Layers

1. **Diagonal smoked exposure**
   Use a textured graphite-to-desaturated-green exposure sweeping diagonally
   through the upper-left empty field. It should be clearly visible, irregular,
   and grainy, then fade completely before reaching the eyebrow or headline.

2. **Fading dot matrix**
   Place a compact matrix of tiny points in the lower-right of the empty left
   gutter, beside and below the form rather than behind it. Fade the matrix on
   every edge so it dissolves into black.

3. **Calibration rail**
   Add one broken vertical rail at the far-left edge with varied short tick marks.
   This is abstract instrumentation, not a scale: no labels or numerals.

4. **Registration symbols**
   Use three or four very small crosshair fragments and a few dim lime glints
   across the empty field. Keep them sparse.

5. **Sensor dust**
   Add five to eight pin-size particles across the full hero, restricted to the
   far-left and bottom fade. No bokeh and no decorative orbs.

## Motion

- Drift the diagonal exposure by 8-12px over 10-14 seconds.
- Let the dot matrix breathe between 70% and 100% of its resting opacity over
  8-10 seconds; do not move every dot independently.
- Send one tiny glint down the calibration rail every 8-12 seconds.
- Keep the registration symbols static or vary them by no more than 4% opacity.
- Stop all motion when the hero is offscreen.
- Under `prefers-reduced-motion`, show the static texture only.

## Limits

- Texture density: 35-45% inside the empty left field, fading to zero before copy.
- Set the dot matrix and calibration details roughly one visual stop brighter than
  the first reference so they remain legible on ordinary laptop displays.
- Bright lime is reserved for three or four pin-size glints.
- No new numbers, labels, specifications, pricing, or mode names.
- No added words, numerals, legends, captions, or interface-like annotations.
- No fluid waves, neon line networks, topographic fields, or effects over content.
