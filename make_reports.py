"""Render human-readable SITEMAP.md and INVENTORY.md from the captured JSON."""
import json, os, re, glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
INV = os.path.join(ROOT, "inventory")
pages = json.load(open(os.path.join(INV, "pages.json")))
arch = json.load(open(os.path.join(INV, "archive_pages.json"))) if \
    os.path.exists(os.path.join(INV, "archive_pages.json")) else {}

# ---------------- SITEMAP ----------------
groups = defaultdict(list)
for p in pages:
    path = p["path"]
    if path == "/":
        g = "Home"
    elif path.startswith("/pages/"):
        g = "Marketing & legal pages"
    elif re.match(r"^/blogs/[^/]+$", path):
        g = "Blog indexes"
    elif path.startswith("/blogs/"):
        g = "Blog articles"
    elif path.startswith("/collections"):
        g = "Collections"
    elif path.startswith("/products"):
        g = "Products"
    else:
        g = "Other"
    groups[g].append(p)

L = ["# Speede — Sitemap (captured live site)", "",
     f"Captured from `https://speede.fit` — **{len(pages)} live URLs** in the published sitemap.", "",
     "> **Key finding:** the live site has been stripped down to a single-page *coming soon* teaser.",
     "> Every `/pages/*` marketing page still resolves but renders an empty shell (title only), and the",
     "> product/collection pages are gone. The only substantive live content is the homepage teaser",
     "> and the editorial blog. The pre-teaser brand site is recovered separately in `/original/archive`.", ""]

order = ["Home", "Marketing & legal pages", "Products", "Collections", "Blog indexes", "Blog articles", "Other"]
for g in order:
    if g not in groups:
        continue
    L.append(f"## {g}  ({len(groups[g])})")
    L.append("")
    L.append("| Path | Title | Body text | Status |")
    L.append("|---|---|---|---|")
    for p in sorted(groups[g], key=lambda x: x["path"]):
        n = p["text_len"]
        status = "**empty shell**" if n < 300 else ("thin" if n < 1200 else "content")
        title = re.sub(r"\s+", " ", (p["title"] or "")).replace("|", "/").strip()[:60]
        L.append(f"| `{p['path']}` | {title} | {n:,} ch | {status} |")
    L.append("")

if arch:
    L += ["## Recovered from the Wayback Machine (`/original/archive`)", "",
          "Pages that existed on the full brand site before the teaser replaced it.", "",
          "| Path | Snapshot | Title |", "|---|---|---|"]
    for path, d in sorted(arch.items()):
        L.append(f"| `{path}` | {d['timestamp'][:8]} | {(d.get('title') or '').replace('|','/')[:60]} |")
    L.append("")

open(os.path.join(ROOT, "SITEMAP.md"), "w").write("\n".join(L))

# ---------------- INVENTORY ----------------
def section_md(s, depth=4):
    out = []
    label = s["id"] or s["class"].split()[0] if (s["id"] or s["class"]) else s["tag"]
    out.append(f"{'#'*depth} `{label}`")
    for h in s["headings"][:10]:
        out.append(f"- **{h['lvl'].upper()}** — {h['text']}")
    for c in s["copy"][:8]:
        out.append(f"  - {c[:400]}")
    if s["ctas"]:
        cs = ", ".join(f"**{c['text']}** → `{c['href']}`" for c in s["ctas"][:8])
        out.append(f"  - _CTAs:_ {cs}")
    if s["images"]:
        for im in s["images"][:8]:
            out.append(f"  - _img:_ `{(im['src'] or '')[:110]}` — alt: “{im['alt'] or ''}”")
    out.append("")
    return out


I = ["# Speede — Page-by-page inventory", "",
     "Section-level breakdown of every page with real content. Sections with no headings, copy or",
     "images are omitted. Empty-shell pages are listed at the bottom.", ""]

subst = [p for p in pages if p["text_len"] >= 1200]
empty = [p for p in pages if p["text_len"] < 1200]

home = [p for p in subst if p["path"] == "/"]
rest = [p for p in subst if p["path"] != "/"]

for p in home + sorted(rest, key=lambda x: x["path"]):
    I.append(f"## `{p['path']}` — {re.sub(r'\s+', ' ', p['title'] or '').strip()}")
    I.append("")
    if p.get("meta_description"):
        I.append(f"*Meta description:* {p['meta_description']}")
        I.append("")
    if p["h1"]:
        I.append(f"*H1:* {' / '.join(p['h1'])}")
        I.append("")
    for s in p["sections"]:
        I += section_md(s)
    I.append("")

I += ["## Empty / thin pages (live)", "",
      "These resolve but render only a title — the brand content was removed for the teaser.", ""]
for p in sorted(empty, key=lambda x: x["path"]):
    I.append(f"- `{p['path']}` — {p['text_len']} characters")

open(os.path.join(ROOT, "INVENTORY.md"), "w").write("\n".join(I))
print("wrote SITEMAP.md and INVENTORY.md")
