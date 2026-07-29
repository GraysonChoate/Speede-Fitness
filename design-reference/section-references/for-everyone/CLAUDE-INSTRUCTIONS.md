# For Everyone: Structural Frame

Use `for-everyone-frame-reference-v9.png` as the visual target. Preserve the existing section, copy, cards, imagery, and card animation. Add only the surrounding structural treatment.

## Intent

This section should feel like four distinct performance profiles inside a softly textured instrument environment. The texture belongs to the black background, not to the card frame.

## Build

1. Add one absolute, pointer-events-none overlay spanning the entire section.
2. Keep every decorative element behind the heading and cards.
3. Create one incomplete perimeter trace around the complete four-card row.
4. Add four sets of short registration corners just outside the cards.
5. Add one shared horizontal baseline below the cards with four small anchor nodes aligned to the card centers.
6. Put faint dashed vertical guides only in the three gutters between cards.
7. Keep the card frame as thin traces and registration corners only.
8. Spread one continuous dot-grid and granular texture field across the black section background.
9. Use broad graphite-green exposure gradients beneath the texture so the surface has depth.
10. Feather the texture away 60-100px before the headline and card faces. It must not form a border around them.

## Visibility

- Main perimeter and corner traces: 40-50% opacity.
- Baseline: 28-36% opacity.
- Anchor nodes: 70-85% opacity with a restrained 6-10px glow.
- Dot texture: 20-32% opacity at its densest point, fading fully to transparent.
- Ambient dot-grid: use 20-24px spacing with 3.5-4.5px diameter dots; 42-58% opacity at its densest point.
- Graphite weave: 24-36% opacity.
- Ambient grain: 30-42% opacity.
- Graphite-green exposure fields: 14-26% opacity.
- Thin frame traces: 34-46% opacity.
- The treatment must be clearly visible at normal laptop brightness. If it disappears in a full-page screenshot, raise the trace and dot opacity before adding more elements.

## Motion

- Keep background motion minimal because the cards will animate.
- On section entry, reveal the perimeter and baseline once over 700-900ms.
- Let the four anchor nodes rise from 55% to 85% opacity in sequence, 80ms apart.
- After entry, only use a slow 2-4% opacity drift in the grain/exposure layer over 8-12 seconds.
- Do not run traveling pulses, looping line draws, or particles through this section.
- Under `prefers-reduced-motion`, render the final state immediately.

## Protected Zones

- Nothing may cross the eyebrow, headline, card faces, card labels, navigation, or section boundary.
- Maintain at least 24px clearance around each card.
- Keep traces in the outer perimeter, gutters, and lower negative space only.

## Do Not

- No added words, numbers, axes, labels, legends, or annotations.
- No circular target, halo, or large centered graphic.
- No free-flowing curves.
- No bright green box around the entire section.
- No moving background element that competes with the card animation.
- No textured bezel, thick patterned border, or U-shaped texture around the cards.
- No isolated texture patches. The background must read as one continuous material surface.
- Judge visibility at the actual presentation scale, around 40-50% zoom. The texture must remain visible there.
- Do not alter the website copy, imagery, layout, or product claims.
