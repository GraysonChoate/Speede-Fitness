"""Render the build and capture proof shots + console/network errors."""
import sys, os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "shots")
os.makedirs(OUT, exist_ok=True)
URL = "http://localhost:3000/"

def run():
    errs, failed = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for label, w, h in [("desktop", 1440, 900), ("mobile", 390, 844)]:
            ctx = b.new_context(viewport={"width": w, "height": h},
                                device_scale_factor=2 if label == "mobile" else 1)
            p = ctx.new_page()
            p.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
            p.on("requestfailed", lambda r: failed.append(r.url + " :: " + str(r.failure)))
            p.goto(URL, wait_until="networkidle", timeout=45000)
            # guard: every srcset candidate must actually exist. A missing
            # candidate only shows up at the DPR that selects it, so check all.
            if label == "desktop":
                import urllib.request, urllib.error
                cands = p.evaluate("""() => {
                  const out = new Set();
                  document.querySelectorAll('source[srcset], img[srcset], img[src]').forEach(e => {
                    (e.getAttribute('srcset') || '').split(',').forEach(s => {
                      const u = s.trim().split(/\\s+/)[0]; if (u) out.add(u);
                    });
                    const src = e.getAttribute('src'); if (src) out.add(src);
                  });
                  return [...out];
                }""")
                for c in cands:
                    if c.startswith('data:'):
                        continue
                    try:
                        urllib.request.urlopen(URL + c.lstrip('/'), timeout=10).read(1)
                    except Exception as ex:
                        failed.append("SRCSET MISSING: " + c + " :: " + str(ex))
            p.wait_for_timeout(900)
            # walk the page so every reveal/observer fires
            p.evaluate("""async () => {
                const h = document.body.scrollHeight;
                for (let y = 0; y < h; y += 500) {
                  window.scrollTo(0, y); await new Promise(r => setTimeout(r, 110));
                }
                window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
            }""")
            p.wait_for_timeout(700)
            p.screenshot(path=os.path.join(OUT, f"{label}-full.png"), full_page=True)
            p.screenshot(path=os.path.join(OUT, f"{label}-hero.png"))
            if label == "desktop":
                for name, sel in [("science", "#science"), ("proof", "#proof"),
                                  ("number", "#number"), ("machine", "#machine"),
                                  ("join", "#join")]:
                    el = p.query_selector(sel)
                    if el:
                        el.scroll_into_view_if_needed()
                        p.wait_for_timeout(1400)
                        p.screenshot(path=os.path.join(OUT, f"sec-{name}.png"))
                dims = p.evaluate("""() => ({
                    doc: document.documentElement.scrollWidth,
                    win: window.innerWidth,
                    revealsIn: document.querySelectorAll('.reveal.in').length,
                    reveals: document.querySelectorAll('.reveal').length,
                    athletes: document.querySelectorAll('.athlete').length,
                    faces: document.querySelectorAll('.face').length,
                    imgsBroken: [...document.images].filter(i => !i.complete || i.naturalWidth === 0)
                                 .map(i => i.currentSrc || i.src)
                })""")
                print("DIMS", dims)
            ctx.close()
        b.close()
    print("CONSOLE ERRORS:", errs or "none")
    print("FAILED REQUESTS:", failed or "none")

run()
