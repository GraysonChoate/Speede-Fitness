# Speede — Design tokens actually in use

Pulled from the live site (`https://speede.fit`, captured July 2026) — computed styles from a
headless Chromium render plus the teaser section's own `:root` block. These are the real values,
not approximations. Full raw dumps: `inventory/design_tokens.json`, `inventory/teaser_section.css`.

---

## 1. Color

The live teaser declares its own palette in a single `:root` block. This is the authoritative set:

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#080a09` | Page background — near-black with a green bias |
| `--bg2` | `#0e120f` | Alternating band background (marquee, "the number" section) |
| `--card` | `#12160f` | Card / input / list-row surface |
| `--line` | `rgba(255,255,255,.09)` | Hairline borders, dividers |
| `--ink` | `#f4f7f0` | Primary text — off-white, warmed slightly green |
| `--muted` | `#9aa39a` | Secondary text, nav links, captions |
| `--green` | `#b2ff59` | **The brand accent.** Lime. CTAs, kickers, data highlights |
| `--green-d` | `#8fd63f` | Deeper lime (gradient stops, hover) |
| `--blue` | `#3aa0ff` | Rarely used secondary accent |

Derived values found in computed styles:

- `#c8ff7e` — button hover fill (lime, lifted)
- `#0a0d08` — text color **on** lime buttons (near-black, not pure `#000`)
- `rgba(178,255,89,.40)` — pill/chip borders
- `rgba(178,255,89,.16)` — hero glow, `radial-gradient(circle, …, transparent 62%)`
- `rgba(178,255,89,.06)` — "us" row highlight fill in the comparison list
- `rgba(178,255,89,.12)` — input focus ring
- `rgba(8,10,9,.70)` — nav bar fill (with `backdrop-filter: blur(14px)`)
- `linear-gradient(180deg, #fff, #b2ff59)` — the big "500" numeral, clipped to text

**Note:** the palette is *not* neutral black. Every neutral is pulled a few degrees toward green
(`#080a09`, `#12160f`, `#f4f7f0`, `#9aa39a`). That subtle bias is what stops it reading as a
generic dark-mode template, and it should be preserved exactly.

---

## 2. Typography

Loaded from Google Fonts:
`Space+Grotesk:wght@400;500;600;700` and `Inter:wght@400;500;600;700`

| Role | Family | Notes |
|---|---|---|
| Display / headings / numerals / buttons | **Space Grotesk** | `letter-spacing: -.02em`, `line-height: 1.02` on h1–h3 |
| Body / UI / lede | **Inter** | `line-height: 1.55`, `-webkit-font-smoothing: antialiased` |

Weights in use: 400 (body), 500 (nav), 600 (buttons, chips, labels), 700 (headings, kickers, big numbers).

### Type scale (as authored — all fluid)

| Element | Size | Weight | Tracking |
|---|---|---|---|
| Hero H1 | `clamp(44px, 6.4vw, 84px)` | 700 | `-.02em` |
| Big numeral ("500") | `clamp(90px, 17vw, 220px)` | 700 | `-.04em`, `line-height: .85` |
| Section H2 | `clamp(30px, 4.4vw, 52px)` | 700 | `-.02em` |
| Rep figures ("5 → 38") | `clamp(40px, 7vw, 72px)` | 700 | — |
| Final CTA H2 | `clamp(34px, 6vw, 72px)` | 700 | — |
| Hero lede | `clamp(16px, 1.9vw, 20px)` | 400 | — |
| Section lead | `clamp(16px, 1.8vw, 19px)` | 400 | — |
| Body / rows | `15px` | 400 | — |
| Nav links | `14px` | 500 | — |
| Small print / captions | `13px` | 400 | — |
| Kicker (section label) | `12px` | 700 | `.16em`, uppercase, lime |
| Eyebrow (hero label) | `12px` | 600 | `.14em`, uppercase, muted |
| "COMING SOON" badge | `10px` | 700 | `.16em`, uppercase, lime |

The scale's signature move: **very large display numerals set against very small, wide-tracked
uppercase labels.** That contrast — 220px next to 10px — is doing most of the visual work.

---

## 3. Spacing rhythm

- Container: `max-width: 1180px`, `padding: 0 24px`
- Standard section: `padding: 90px 0`
- Hero: `padding: 150px 0 60px` (desktop) / `120px 0 40px` (≤860px)
- Marquee band: `padding: 16px 0`, `margin-top: 50px`
- Card interior: `30px`
- Column gaps: `50px` (two-up feature grids), `40px` (hero), `18px` (card grids)
- Stack gaps: `30px`, `22px`, `18px`, `16px`, `14px`, `12px`, `10px`, `9px` — an 8–10px-ish
  informal ladder, not a strict scale
- Single responsive breakpoint: **`860px`**. Everything collapses to one column there.

---

## 4. Radii

| Value | Used for |
|---|---|
| `18px` (`--radius`) | Hero image, cards, render tiles, graph card |
| `12px` | Inputs, primary buttons, comparison rows |
| `100px` | Pills — nav CTA, badge, chips, hero tag |
| `50%` | Status dot |

---

## 5. Buttons

**Primary** (`.btn`, `.nav-cta`)
```
font-family: 'Space Grotesk'; font-weight: 600;
color: #0a0d08; background: #b2ff59;
padding: 16px 26px;  border-radius: 12px;  border: none;
/* nav variant: 15px→14px, padding 9px 18px, border-radius 100px */
transition: .2s;
:hover { background:#c8ff7e; transform:translateY(-2px);
         box-shadow:0 10px 30px rgba(178,255,89,.2) }
```

**Chip / pill** (`.chip`)
```
font-size:13px; font-weight:600; padding:8px 14px; border-radius:100px;
border:1px solid rgba(255,255,255,.09); color:#9aa39a;
&.on { color:#b2ff59; border-color:rgba(178,255,89,.4) }
```

**Input** (`.form input`)
```
background:#12160f; border:1px solid rgba(255,255,255,.09); color:#f4f7f0;
padding:16px 18px; border-radius:12px; font-size:15px;
:focus { border-color:#b2ff59; box-shadow:0 0 0 3px rgba(178,255,89,.12) }
```

---

## 6. Elevation & effects

- Hero image: `box-shadow: 0 40px 90px rgba(0,0,0,.6)` + `1px solid var(--line)`
- Button hover: `0 10px 30px rgba(178,255,89,.2)`
- Nav: `backdrop-filter: blur(14px)` over `rgba(8,10,9,.7)`
- Hero tag pill: `backdrop-filter: blur(8px)` over `rgba(8,10,9,.78)`
- Hero glow: `radial-gradient(circle, rgba(178,255,89,.16), transparent 62%)`, 70vw square,
  positioned `top:-15%; right:-10%`
- Image bottom scrims: `linear-gradient(transparent 55%, rgba(8,10,9,.35))`

---

## 7. Motion in use

| Where | What |
|---|---|
| Status dot | `pulse` — opacity 1 → .35, 2s infinite |
| Marquee | `scroll` — `translateX(-50%)`, 26s linear infinite |
| Buttons / links | `.2s` transition, `translateY(-1px…-2px)` on hover |
| Render tiles | `.5s` image transition on hover |
| Page | `scroll-behavior: smooth` |

No scroll-triggered reveals exist today. No `prefers-reduced-motion` handling exists today.

---

## 8. Assets captured

- **Logo:** `2-logo-speede-white.svg` — wordmark, letterforms with cut horizontal bars in the
  E's; rendered at `height: 19px` in the nav. Saved to `original/assets/cdn.shopify.com/`.
- **Photography:** 8 JPEGs (`2-image.jpg` … `9-image.jpg`) — real product-in-real-room shots:
  the machine in a sunlit living room, a man folding it under a bed, hands snapping in an
  attachment. Warm concrete/wood interiors, hard directional daylight, muted palette that the
  lime UI sits cleanly on top of.
- All CSS, JS, fonts and images from every captured page are in `original/assets/` (460+ files),
  indexed in `inventory/assets.json`.
