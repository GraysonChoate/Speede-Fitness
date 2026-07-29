# Speede — capture, understand, elevate

Working directory for the Speede (`speede.fit`) capture and rebuild.

## Status

| Phase | State |
|---|---|
| 1 — Capture | **Complete** |
| 2 — Understand | **Complete — awaiting sign-off** |
| 3 — Elevate | Not started (blocked on Phase 2 approval) |
| 4 — Deliver | Not started |

## Read these

| File | What it is |
|---|---|
| **`BRAND-BRIEF.md`** | Phase 2. The story, audience, differentiators, voice, what to keep, what's holding it back. Appendix A is the verbatim proof library. |
| **`SITEMAP.md`** | All 96 live URLs, grouped, with content status — plus what was recovered from the archive. |
| **`INVENTORY.md`** | Page-by-page, section-by-section: headlines, body copy, CTAs, images. |
| **`DESIGN-TOKENS.md`** | Exact hexes, fonts, type scale, spacing rhythm, button styles, motion — as measured, not guessed. |

## `/original` — untouched reference (111 MB)

```
original/
  pages/         96 live pages: rendered HTML + plain text
  screenshots/   full-page PNGs at 1440px
  assets/        460+ files — CSS, JS, fonts, images, by host
  archive/       19 pre-teaser pages recovered from the Wayback Machine
  sitemaps_*.xml the published sitemap tree
```

Nothing in `/original` is modified by later phases.

## `/inventory` — structured data

`pages.json` · `design_tokens.json` · `archive_pages.json` · `sitemap_urls.json` ·
`assets.json` · `teaser_section.css` (the live page's own stylesheet) · `slices/`

## Reproducing the capture

```bash
python3 -m venv .venv && ./.venv/bin/pip install requests beautifulsoup4 lxml playwright
./.venv/bin/playwright install chromium
./.venv/bin/python scrape2.py         # live site -> original/pages, original/assets
./.venv/bin/python wayback_all.py     # pre-teaser site -> original/archive
./.venv/bin/python inventory_build.py # -> inventory/pages.json, design_tokens.json
./.venv/bin/python make_reports.py    # -> SITEMAP.md, INVENTORY.md
```

**Note:** `speede.fit` is behind Shopify bot protection and returns `429 local_rate_limited` to
plain `requests`/`httpx` regardless of headers. The capture uses Playwright with a real Chromium
for that reason. `web.archive.org` works fine over `requests`.
