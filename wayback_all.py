"""Robust Wayback recovery of the pre-teaser Speede site -> /original/archive."""
import json, os, re, time, glob
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "original", "archive")
INV = os.path.join(ROOT, "inventory")
os.makedirs(OUT, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}
S = requests.Session()
S.headers.update(H)

TARGETS = [
    ("/", "home_full", ("20220101", "20240601")),
    ("/pages/about", "pages__about", None),
    ("/pages/muscle-science", "pages__muscle-science", None),
    ("/pages/leadership", "pages__leadership", ("20220101", "20240601")),
    ("/pages/contact", "pages__contact", None),
    ("/pages/demo", "pages__demo", None),
    ("/pages/standard-mode", "pages__standard-mode", None),
    ("/pages/excentric-mode", "pages__excentric-mode", None),
    ("/pages/nemesismode", "pages__nemesismode", None),
    ("/pages/recovery-mode", "pages__recovery-mode", None),
    ("/pages/scientists-full", "pages__scientists-full", None),
    ("/pages/workouts-page", "pages__workouts-page", None),
    ("/pages/coaches-page-v1", "pages__coaches-page-v1", None),
    ("/pages/trainers-page", "pages__trainers-page", None),
    ("/pages/ptsots-page", "pages__ptsots-page", None),
    ("/products/speede-challenger", "products__speede-challenger", None),
    ("/products/speede-pro", "products__speede-pro", None),
    ("/products/speede-rack-accessory", "products__speede-rack-accessory", None),
    ("/collections/shop-speede", "collections__shop-speede", None),
    ("/blogs/news/ask-the-athletes-what-pro-athletes-are-saying-about-speede-s-science",
     "blog__ask-the-athletes", None),
    ("/blogs/tech/microdosing-strength-training-how-speede-nets-you-more-gains-in-a-fraction-of-the-time",
     "blog__microdosing", None),
]


def get(url, params=None, tries=4, timeout=75):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code in (429, 503):
                time.sleep(8 * (i + 1)); continue
            return None
        except Exception:
            time.sleep(5 * (i + 1))
    return None


def snapshots(path, window):
    p = {"url": "speede.fit" + path, "output": "json", "fl": "timestamp",
         "filter": ["statuscode:200", "mimetype:text/html"]}
    if window:
        p["from"], p["to"] = window
    r = get("http://web.archive.org/cdx/search/cdx", p)
    if not r or not r.text.strip():
        return []
    try:
        return sorted({row[0] for row in r.json()[1:]}, reverse=True)
    except Exception:
        return []


results = {}
p = os.path.join(INV, "archive_pages.json")
if os.path.exists(p):
    try: results = json.load(open(p))
    except Exception: pass

done = {os.path.basename(f).split(".")[0] for f in glob.glob(os.path.join(OUT, "*.txt"))}

for path, stem, window in TARGETS:
    if stem in done:
        print("have", stem, flush=True); continue
    snaps = snapshots(path, window)
    if not snaps and window:
        snaps = snapshots(path, None)
    if not snaps:
        print("NO SNAP", path, flush=True); continue
    got = None
    for ts in snaps[:8]:
        r = get(f"http://web.archive.org/web/{ts}id_/https://speede.fit{path}", tries=2, timeout=90)
        if not r or len(r.text) < 5000:
            continue
        soup = BeautifulSoup(r.text, "lxml")
        for t in soup(["script", "style", "noscript"]):
            t.decompose()
        text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n", strip=True))
        if len(text) < 1200:
            continue
        got = (ts, r.text, text, soup); break
    if not got:
        print("NO USABLE", path, flush=True); continue
    ts, raw, text, soup = got
    open(os.path.join(OUT, f"{stem}.{ts}.html"), "w").write(raw)
    open(os.path.join(OUT, f"{stem}.{ts}.txt"), "w").write(text)
    results[path] = {
        "timestamp": ts, "stem": stem,
        "title": soup.title.get_text(strip=True) if soup.title else None,
        "meta_description": (soup.find("meta", attrs={"name": "description"}) or {}).get("content"),
        "headings": [{"lvl": h.name, "text": h.get_text(" ", strip=True)}
                     for h in soup.find_all(["h1", "h2", "h3", "h4"]) if h.get_text(strip=True)][:100],
        "ctas": [{"text": a.get_text(" ", strip=True), "href": a.get("href")}
                 for a in soup.find_all(["a", "button"])
                 if a.get_text(strip=True) and len(a.get_text(strip=True)) < 60][:80],
        "images": [{"src": i.get("src") or i.get("data-src"), "alt": i.get("alt")}
                   for i in soup.find_all("img")][:80],
        "text_len": len(text),
    }
    print("ok", path, ts, len(text), flush=True)
    time.sleep(1.5)

json.dump(results, open(p, "w"), indent=2)
print("SAVED", len(results))
