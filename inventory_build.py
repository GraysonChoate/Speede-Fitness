"""Build page inventory offline from /original/pages, plus live design-token extraction."""
import json, os, re, glob
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(ROOT, "original", "pages")
INV = os.path.join(ROOT, "inventory")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

CHROME = re.compile(r"^(skip to content|cart|my account|search|close \(esc\)|loading|"
                    r"buy now on indiegogo|view all|no products found)$", re.I)


def build_pages():
    out = []
    for f in sorted(glob.glob(os.path.join(ORIG, "*.html"))):
        stem = os.path.basename(f)[:-5]
        soup = BeautifulSoup(open(f).read(), "lxml")
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        main = soup.find("main") or soup.body
        if main is None:
            continue
        txt = lambda e: re.sub(r"\s+", " ", e.get_text(" ", strip=True)).strip()
        sections = []
        roots = main.find_all(recursive=False)
        for r in roots:
            heads = [{"lvl": h.name, "text": txt(h)} for h in r.find_all(["h1", "h2", "h3", "h4"]) if txt(h)]
            copy = [txt(p) for p in r.find_all(["p", "li", "blockquote"]) if len(txt(p)) > 2][:50]
            ctas = [{"text": txt(a), "href": a.get("href")} for a in r.find_all(["a", "button"])
                    if txt(a) and len(txt(a)) < 70 and not CHROME.match(txt(a))][:25]
            imgs = [{"src": i.get("src") or i.get("data-src"), "alt": i.get("alt")} for i in r.find_all("img")][:25]
            if not (heads or copy or imgs):
                continue
            sections.append({"tag": r.name, "id": r.get("id"), "class": " ".join(r.get("class") or [])[:90],
                             "headings": heads, "copy": copy, "ctas": ctas, "images": imgs})
        out.append({
            "file": stem,
            "path": "/" + stem.replace("__", "/") if stem != "index" else "/",
            "title": soup.title.get_text(strip=True) if soup.title else None,
            "meta_description": (soup.find("meta", attrs={"name": "description"}) or {}).get("content"),
            "h1": [txt(h) for h in soup.find_all("h1")],
            "sections": sections,
            "text_len": len(main.get_text()),
        })
    json.dump(out, open(os.path.join(INV, "pages.json"), "w"), indent=2)
    print("pages inventoried:", len(out))
    return out


TOKENS_JS = r"""() => {
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
      bump(weights,s.fontWeight); bump(ls,s.letterSpacing); bump(lh,s.lineHeight);
      bump(fams,s.fontFamily.split(',')[0].replace(/["']/g,'')); }
    if (s.backgroundColor!=='rgba(0, 0, 0, 0)') bump(bgs,norm(s.backgroundColor));
    if (s.borderTopWidth!=='0px') bump(borders, s.borderTopWidth+' '+s.borderTopStyle+' '+norm(s.borderTopColor));
    bump(radii,s.borderRadius); bump(shadows,s.boxShadow); });
  const type=[];
  [['h1','h1'],['h2','.sec h2'],['hero-lede','.hero-lede'],['kicker','.kicker'],['eyebrow','.eyebrow'],
   ['body','p'],['btn','.btn'],['nav-cta','.nav-cta'],['chip','.chip'],['badge','.badge'],
   ['bignum','.bignum'],['input','.form input'],['vs-row','.vs-list li'],['nav-link','.nav-links a'],
   ['reps','.reps .r'],['proof-quote','[class*=quote]'],['footer','footer, .foot']].forEach(([name,sel])=>{
    const e=document.querySelector(sel); if(!e) return; const s=getComputedStyle(e);
    type.push({name, sel, font:s.fontFamily.split(',')[0].replace(/["']/g,''), size:s.fontSize,
      weight:s.fontWeight, lh:s.lineHeight, ls:s.letterSpacing, tt:s.textTransform, color:norm(s.color),
      bg:norm(s.backgroundColor), pad:s.padding, radius:s.borderRadius,
      border:s.borderTopWidth+' '+s.borderTopStyle+' '+norm(s.borderTopColor),
      shadow:s.boxShadow, sample:(e.innerText||'').trim().replace(/\s+/g,' ').slice(0,64)});
  });
  const spacing={};
  document.querySelectorAll('section, .sec, main > *').forEach(e=>{ const s=getComputedStyle(e);
    bump(spacing,'pad-block '+s.paddingTop+'/'+s.paddingBottom); });
  const wrap=document.querySelector('.wrap');
  const top=(o,n=28)=>Object.entries(o).sort((a,b)=>b[1]-a[1]).slice(0,n);
  return {cssVars, colors:top(colors), backgrounds:top(bgs), borders:top(borders,14),
    fontFamilies:top(fams,10), fontSizes:top(sizes), fontWeights:top(weights,8), letterSpacing:top(ls,12),
    lineHeights:top(lh,12), radii:top(radii,12), shadows:top(shadows,10), spacing:top(spacing,20),
    typeSamples:type, container: wrap ? getComputedStyle(wrap).maxWidth+' pad '+getComputedStyle(wrap).paddingLeft : null,
    loadedFonts:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status})),
    bodyBg:norm(getComputedStyle(document.body).backgroundColor),
    bodyFont:getComputedStyle(document.body).fontFamily};
}"""


def build_tokens():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_context(user_agent=UA, viewport={"width": 1440, "height": 1000}).new_page()
        p.goto("https://speede.fit/", wait_until="domcontentloaded", timeout=60000)
        p.wait_for_timeout(6000)
        t = p.evaluate(TOKENS_JS)
        json.dump(t, open(os.path.join(INV, "design_tokens.json"), "w"), indent=2)
        b.close()
    print("tokens ok")


if __name__ == "__main__":
    build_pages()
    build_tokens()
