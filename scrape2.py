"""Archival scrape of speede.fit -> /original (untouched reference). Pass 2: full page coverage."""
import html as htmllib
import json, os, re
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(ROOT, "original")
INV = os.path.join(ROOT, "inventory")
BASE = "https://speede.fit"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

for d in (ORIG, INV):
    os.makedirs(d, exist_ok=True)

captured = {}

EXTRACT = r"""() => {
  const txt = e => (e.innerText||'').trim().replace(/\s+/g,' ');
  const inSec = (root) => ({
    tag: root.tagName.toLowerCase(),
    id: root.id || null,
    cls: (typeof root.className === 'string' ? root.className : '') || null,
    headings: [...root.querySelectorAll('h1,h2,h3,h4')].map(h=>({lvl:h.tagName, text:txt(h)})).filter(h=>h.text),
    copy: [...root.querySelectorAll('p,li,blockquote')].map(txt).filter(t=>t.length>2).slice(0,60),
    ctas: [...root.querySelectorAll('a,button,input[type=submit]')].map(a=>({
        text: txt(a)||a.value||a.getAttribute('aria-label')||'', href:a.getAttribute('href')||null
    })).filter(c=>c.text).slice(0,30),
    images: [...root.querySelectorAll('img')].map(i=>({src:i.currentSrc||i.src, alt:i.alt, w:i.naturalWidth, h:i.naturalHeight})),
    videos: [...root.querySelectorAll('video')].map(v=>({src:v.currentSrc||v.src, poster:v.poster,
        sources:[...v.querySelectorAll('source')].map(s=>s.src)}))
  });
  const roots = [...document.querySelectorAll('main > *')];
  const sections = (roots.length?roots:[...document.querySelectorAll('body > section, body > div')].slice(0,25)).map(inSec);
  return {
    title: document.title, url: location.href,
    meta: [...document.querySelectorAll('meta')].map(m=>({name:m.name||m.getAttribute('property'), content:m.content})).filter(m=>m.name),
    h1: [...document.querySelectorAll('h1')].map(txt),
    sections,
    allText: document.body.innerText,
    links: [...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href))].filter(u=>u.includes('speede.fit')),
    forms: [...document.querySelectorAll('form')].map(f=>({action:f.getAttribute('action'), method:f.method,
        fields:[...f.querySelectorAll('input,select,textarea')].map(i=>({name:i.name,type:i.type,ph:i.placeholder}))}))
  };
}"""


def safe_path(url, subdir):
    p = urlparse(url)
    name = unquote(p.path.strip("/")) or "index"
    name = re.sub(r"[^A-Za-z0-9._/-]", "_", name)
    if p.query:
        name += "__" + re.sub(r"[^A-Za-z0-9._-]", "_", p.query)[:60]
    if not os.path.splitext(name)[1]:
        name += ".bin"
    out = os.path.join(ORIG, subdir, p.netloc, name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return out


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 1000}, locale="en-US")
        page = ctx.new_page()

        def on_response(resp):
            url = resp.url
            if url.startswith("data:") or url in captured:
                return
            ct = (resp.headers.get("content-type") or "").split(";")[0]
            if not any(k in ct for k in ("css", "javascript", "image", "font", "svg", "video")):
                return
            try:
                body = resp.body()
            except Exception:
                return
            try:
                with open(safe_path(url, "assets"), "wb") as f:
                    f.write(body)
            except Exception:
                return
            captured[url] = {"status": resp.status, "content_type": ct, "bytes": len(body)}

        page.on("response", on_response)

        # ---- discover every URL, following nested sitemaps ------------------
        seen_sm, locs, queue = set(), set(), [BASE + "/sitemap.xml"]
        while queue:
            sm_url = htmllib.unescape(queue.pop(0))
            if sm_url in seen_sm:
                continue
            seen_sm.add(sm_url)
            try:
                page.goto(sm_url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print("sitemap fail", sm_url, e); continue
            c = page.content()
            fn = re.sub(r"[^A-Za-z0-9._-]", "_", urlparse(sm_url).path + urlparse(sm_url).query)
            with open(os.path.join(ORIG, "sitemaps_" + fn.strip("_") + ".xml"), "w") as f:
                f.write(c)
            for u in re.findall(r"<loc>([^<]+)</loc>", c):
                u = htmllib.unescape(u)
                if "sitemap" in u and u.split("?")[0].endswith(".xml"):
                    queue.append(u)
                elif "speede.fit" in u:
                    locs.add(u)

        paths = sorted({urlparse(u).path or "/" for u in locs})
        # priority: brand/marketing first, then commerce, then editorial
        def rank(p):
            if p == "/": return 0
            if p.startswith("/pages/"): return 1
            if p.startswith("/products/"): return 2
            if p.startswith("/collections"): return 3
            if re.match(r"^/blogs/[^/]+$", p): return 4
            return 5
        ordered = ["/"] + [p for p in sorted(paths, key=lambda p: (rank(p), p)) if p != "/"]
        json.dump({"all_urls": sorted(locs), "visit_order": ordered},
                  open(os.path.join(INV, "sitemap_urls.json"), "w"), indent=2)
        print(f"discovered {len(locs)} urls / {len(ordered)} paths", flush=True)

        results = []
        for i, path in enumerate(ordered):
            url = BASE + path
            deep = rank(path) <= 4          # full treatment (scroll, screenshot) for non-article pages
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print("FAIL", url, e, flush=True); continue
            page.wait_for_timeout(1200 if deep else 500)
            if deep:
                page.evaluate("""async () => {
                    const h = document.body.scrollHeight;
                    for (let y=0; y<h; y+=700){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,70)); }
                    window.scrollTo(0,0);
                }""")
                page.wait_for_timeout(1200)

            stem = (path.strip("/") or "index").replace("/", "__")
            with open(os.path.join(ORIG, "pages", stem + ".html"), "w") as f:
                os.makedirs(os.path.join(ORIG, "pages"), exist_ok=True)
                f.write(page.content())
            with open(os.path.join(ORIG, "pages", stem + ".txt"), "w") as f:
                f.write(page.evaluate("() => document.body.innerText"))
            if deep:
                sdir = os.path.join(ORIG, "screenshots"); os.makedirs(sdir, exist_ok=True)
                try:
                    page.screenshot(path=os.path.join(sdir, stem + ".png"), full_page=True)
                except Exception:
                    pass
            try:
                results.append(page.evaluate(EXTRACT))
            except Exception as e:
                print("extract fail", url, e, flush=True)
            print(f"{i+1}/{len(ordered)} {path}", flush=True)

        # ---- design tokens ---------------------------------------------------
        page.goto(BASE + "/", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)
        tokens = page.evaluate(r"""() => {
          const norm = c => { const m=(c||'').match(/rgba?\(([^)]+)\)/); if(!m) return c;
            const p=m[1].split(',').map(s=>parseFloat(s.trim()));
            const hex='#'+p.slice(0,3).map(v=>('0'+Math.round(v).toString(16)).slice(-2)).join('');
            return (p.length>3 && p[3]<1) ? hex+' @'+p[3] : hex; };
          const cssVars={};
          for (const sheet of document.styleSheets){ let rules; try{rules=sheet.cssRules}catch(e){continue}
            for (const r of rules||[]) if (r.style && /:root|^html$/.test(r.selectorText||''))
              for (const p of r.style) if (p.startsWith('--')) cssVars[p]=r.style.getPropertyValue(p).trim(); }
          const colors={},bgs={},borders={},fams={},sizes={},weights={},radii={},shadows={},ls={},lh={};
          const bump=(o,k)=>{ if(!k||k==='none'||k==='normal') return; o[k]=(o[k]||0)+1 };
          document.querySelectorAll('*').forEach(e=>{ const s=getComputedStyle(e);
            if (e.children.length===0 && e.textContent.trim()) { bump(colors,norm(s.color)); bump(sizes,s.fontSize);
              bump(weights,s.fontWeight); bump(ls,s.letterSpacing); bump(lh,s.lineHeight); bump(fams,s.fontFamily); }
            if (s.backgroundColor!=='rgba(0, 0, 0, 0)') bump(bgs,norm(s.backgroundColor));
            if (s.borderTopWidth!=='0px') bump(borders, s.borderTopWidth+' '+s.borderTopStyle+' '+norm(s.borderTopColor));
            bump(radii,s.borderRadius); bump(shadows,s.boxShadow); });
          const type=[];
          ['h1','h2','h3','h4','p','a','button','[class*=eyebrow]','[class*=kicker]','[class*=label]',
           '[class*=btn]','[class*=button]','[class*=pill]','[class*=stat]','input'].forEach(sel=>{
            document.querySelectorAll(sel).forEach((e,i)=>{ if(i>1) return; const s=getComputedStyle(e);
              type.push({sel, cls:(typeof e.className==='string'?e.className:'').slice(0,80), font:s.fontFamily,
                size:s.fontSize, weight:s.fontWeight, lh:s.lineHeight, ls:s.letterSpacing, tt:s.textTransform,
                color:norm(s.color), bg:norm(s.backgroundColor), pad:s.padding, radius:s.borderRadius,
                border:s.border, sample:(e.innerText||'').trim().slice(0,60)}); });
          });
          const spacing={};
          document.querySelectorAll('section, main > *, [class*=section]').forEach(e=>{ const s=getComputedStyle(e);
            bump(spacing, 'pad-block:'+s.paddingTop+'/'+s.paddingBottom); bump(spacing,'max-w:'+s.maxWidth); });
          const top=(o,n=30)=>Object.entries(o).sort((a,b)=>b[1]-a[1]).slice(0,n);
          return {cssVars, colors:top(colors), backgrounds:top(bgs), borders:top(borders,15),
                  fontFamilies:top(fams,10), fontSizes:top(sizes), fontWeights:top(weights,8),
                  letterSpacing:top(ls,12), lineHeights:top(lh,12), radii:top(radii,12), shadows:top(shadows,10),
                  spacing:top(spacing,25), typeSamples:type,
                  loadedFonts:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status})),
                  bodyBg:norm(getComputedStyle(document.body).backgroundColor)};
        }""")
        json.dump(tokens, open(os.path.join(INV, "design_tokens.json"), "w"), indent=2)
        json.dump(results, open(os.path.join(INV, "pages.json"), "w"), indent=2)
        json.dump(captured, open(os.path.join(INV, "assets.json"), "w"), indent=2)
        browser.close()
    print("DONE pages:", len(results), "assets:", len(captured), flush=True)


if __name__ == "__main__":
    run()
