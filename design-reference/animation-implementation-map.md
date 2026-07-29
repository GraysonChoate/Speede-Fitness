# Speede ambient motion implementation map

## Non-negotiable rules

- Use only Speede's palette: `#080A09`, `#0E120F`, `#B2FF59`, `#8FD63F`, `#F4F7F0`, and `#9AA39A`.
- Keep copy, numbers, faces, product details, forms, and graphs completely clear.
- Place ambient effects in gutters, outer edges, image boundaries, and section transitions.
- Most traces should be muted gray or dark olive at 4-12% opacity.
- Lime is reserved for tiny pulse nodes and very short accents. Never draw long bright lime routes.
- No fluid waves, glowing ribbons, random particle storms, cyberpunk HUD decoration, or invented data.
- Pause repeating animation while its section is off screen.
- Honor `prefers-reduced-motion` with a static, fully legible composition.

## Navigation

The navigation is smoked glass rather than a flat black bar. It becomes slightly denser and shorter after scrolling.

- A one-pixel lime progress trace runs along the bottom edge.
- The current section receives a short underline and a tiny pulse point.
- Hover states stay restrained: no large pills, bouncing links, or expanding backgrounds.
- The CTA may lift by one pixel and gain a soft lime shadow.
- Keep the logo and navigation aligned to the same page grid as the content.

## Hero

Treatment: optical image falloff plus sensor residue.

- Keep the existing video full bleed on the right.
- Feather its left and bottom edges into `#080A09`.
- Place sparse, tiny measurement dots beneath the lower-right media edge.
- Add a nearly invisible vertical scan falloff that drifts downward over 10 seconds.
- Never place traces over the headline, body copy, form, or the athlete/product subject.

## Athlete proof strip and ticker

Treatment: registration rhythm.

- The portrait chips remain the content.
- Use the existing horizontal ticker as the movement bridge.
- Registration dots and separators should repeat mechanically and move at one constant speed.
- Avoid an additional decorative animation above or below the ticker.

## The Number

Treatment: incomplete calibration frame.

- Keep the large number as the dominant object.
- Place partial measurement brackets around the section perimeter.
- Use two or three broad, low-opacity calibration echoes behind the outer left edge.
- One tiny pulse node may breathe at the lower-left bracket.
- Nothing may pass behind or through the number or comparison rows.

## Science

Treatment: gutter-routed ghost telemetry.

- Confine parallel trace paths to the vertical gap between copy and the instrument panel.
- Paths arrive from the outside, turn with controlled-radius corners, collect in the gutter, and fade vertically.
- Use one small pulse travelling down the gutter over approximately seven seconds.
- On stacked tablet and mobile layouts, remove the gutter telemetry entirely.

## Strength curve

Treatment: graph afterimages and capacity hatch.

- Keep the real graph unchanged.
- Place three progressively fainter horizontal or curve echoes beneath the card.
- Allow fine diagonal hatching only outside the graph's plotting area.
- The existing measurement sweep remains the primary animation.
- Never add another competing moving line inside the graph.

## Machine tease

Treatment: scan reveal residue.

- Keep Speede's existing photography.
- Run one narrow, low-opacity scan reflection down each image at staggered intervals.
- Add stepped masking traces only at the far left and right section edges.
- The scan should reveal texture, not make the image flash brighter.

## Built for everyone

Treatment: offset frame echoes.

- Keep the four image apertures and their current photography.
- Add a very faint offset border behind each frame to reinforce the sequence.
- Run an occasional soft scanner residue down the images, staggered from left to right.
- Do not add extra imagery, colors, labels, or portrait effects.

## Proof

Treatment: documentary registration field.

- Keep the portrait cards and exact league logos as the evidence.
- Place fine sensor grain and a horizontal registration residue behind the card grid.
- The residue must stop before entering the cards.
- League marks should use original vector artwork. Do not redraw them as text.

## Final CTA

Treatment: resolution into stillness.

- Keep the form area completely black and calm.
- Place sparse telemetry dots around the far perimeter.
- Reduce density and contrast toward the center.
- The final visible trace should fade out before it reaches the form.
- This section should move less than every section above it.

## Timing

- Ambient loops: 7-12 seconds.
- Image scan: 8-9 seconds, with long inactive pauses.
- Pulse node: 3-4 seconds.
- Scroll reveals: 600-800 milliseconds.
- Use `cubic-bezier(.22, .61, .36, 1)` for entrances and linear timing only for continuous registration movement.
