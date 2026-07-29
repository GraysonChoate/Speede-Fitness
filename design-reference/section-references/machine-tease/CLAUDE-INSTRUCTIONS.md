# Machine Tease: Exterior Visual Treatment

Use the supplied reference as the exact art-direction target. Preserve all existing layout, copy, photography, controls, dimensions, and spacing.

## Non-negotiable rules

- Do not add any words, numbers, labels, legends, annotations, icons, or callout markers.
- Do not place decorative effects over the heading, support copy, navigation, photographs, or image captions.
- Do not change or crop the three photographs.
- Do not add people, product renders, or new imagery.
- Use only `#080A09`, `#0E120F`, `#B2FF59`, `#8FD63F`, `#F4F7F0`, and `#9AA39A`.
- The treatment must be clearly visible at normal laptop brightness. Do not reduce it until it disappears.

## Composition

1. **Upper exposure field**
   - Add a broad, low-contrast graphite-to-lime exposure haze inside the large empty band above the copy.
   - Mix fine monochrome grain into it.
   - Keep its strongest point near the horizontal center and fade it completely before it reaches either text block.

2. **Staggered edge scan blocks**
   - Build irregular stacks of hard-edged horizontal rectangles in the far-left and far-right gutters.
   - Vary their width and height. Use a mixture of solid graphite, faint lime, scan-line texture, and dot-matrix texture.
   - The blocks should feel like partial sensor data entering and leaving the frame, not decorative stripes.
   - Fade each stack inward so neither side reaches the content.

3. **Incomplete image-row frame**
   - Treat all three photographs as one grouped reveal.
   - Add broken corner brackets outside the full row, with no line running continuously across the photographs.
   - Add two fainter, offset bracket echoes behind the main frame.
   - Keep at least 32px clearance from every photograph and caption.

4. **Lower scan residue**
   - Below the image row, add a shallow band of horizontal scan lines, broken traces, sparse dots, and graphite grain.
   - It should visually carry the eye into the next section without looking like a divider.

5. **Anchor nodes**
   - Use only five to seven tiny illuminated nodes across the full section.
   - Place them at bracket corners or inside the outer scan stacks.
   - Never scatter them randomly.

## Visibility targets

- Primary brackets and nearest scan blocks: 68-82% effective opacity.
- Secondary bracket echoes: 38-52%.
- Dot and scan textures: 34-48%.
- Grain/exposure field: 24-38%.
- Lime glow must stay tight and controlled; no large neon bloom.
- Judge visibility from a full-page screenshot at 100% scale on an ordinary laptop display. If the scan stacks, upper exposure, and four main brackets are not immediately legible, they are too faint.

## Motion

- Edge scan blocks drift vertically by 4-8px over 10-14 seconds, with different offsets per block.
- A single bright scan passes through one side stack every 7-10 seconds.
- The upper exposure field breathes by no more than 4% opacity over 12-16 seconds.
- One node travels along the incomplete outer bracket every 9-12 seconds, then disappears.
- Lower scan residue shifts horizontally by 6-10px over 14-18 seconds.
- Use linear or restrained ease-in-out timing. No elastic motion, liquid morphing, waves, or continuous glowing everywhere.

## Reduced motion and mobile

- Under `prefers-reduced-motion`, freeze every element at a composed static frame.
- On mobile, remove the secondary bracket echoes, reduce each edge stack to three or four blocks, and retain the top exposure field plus one lower scan band.
- Maintain a minimum 24px clear zone around text and media on mobile.
