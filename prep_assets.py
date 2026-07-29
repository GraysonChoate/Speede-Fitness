"""Normalize athlete portraits + optimize product photography into build/assets."""
import os, glob
from PIL import Image, ImageEnhance, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_ATH = os.path.join(ROOT, "original", "athletes")
SRC_IMG = os.path.join(ROOT, "build", "assets", "img")
OUT_ATH = os.path.join(ROOT, "build", "assets", "athletes")
os.makedirs(OUT_ATH, exist_ok=True)

# name -> source file
ATHLETES = {
    "chandler":   "MichaelChandler.jpg",
    "fields":     "JustiinFields.jpg",
    "kmet":       "ColeKmet.png",
    "simmons":    "justinsimmons.jpg",
    "mvs":        "Marquez-Valdes-Scantling.png",
    "johnson":    "JaylonJohnson.png",
    "sesselmann": "Athlete_LaurenSesselmann.jpg",
    "plumlee":    "MasonPlumlee.jpg",
}

TARGET = (400, 600)          # 2:3, ~2x a 200px display slot


def lift_shadows_green(im, amount=0.055):
    """Nudge the darkest tones toward the brand's green-biased black (#080a09)
    so the portraits sit inside the page background instead of on top of it."""
    im = im.convert("RGB")
    r, g, b = im.split()
    # raise green fractionally, drop blue fractionally — matches #080a09 / #12160f bias
    g = g.point(lambda v: min(255, int(v + 255 * amount * (1 - v / 255) ** 2)))
    b = b.point(lambda v: max(0, int(v - 255 * (amount * 0.5) * (1 - v / 255) ** 2)))
    return Image.merge("RGB", (r, g, b))


def process_portrait(src, dst_stem):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (8, 10, 9))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    im = im.convert("RGB")
    im = ImageOps.fit(im, TARGET, method=Image.LANCZOS, centering=(0.5, 0.32))
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Brightness(im).enhance(0.97)
    im = lift_shadows_green(im)
    im.save(os.path.join(OUT_ATH, dst_stem + ".webp"), "WEBP", quality=86, method=6)
    im.save(os.path.join(OUT_ATH, dst_stem + ".jpg"), "JPEG", quality=84, optimize=True,
            progressive=True)
    return im.size


for stem, fn in ATHLETES.items():
    p = os.path.join(SRC_ATH, fn)
    if not os.path.exists(p):
        print("missing", fn); continue
    print("portrait", stem, process_portrait(p, stem))

# ---- product photography: webp + responsive widths -------------------------
WIDTHS = [640, 1024, 1600]
for f in sorted(glob.glob(os.path.join(SRC_IMG, "*.jpg"))):
    stem = os.path.splitext(os.path.basename(f))[0]
    if "-" in stem:
        continue
    im = Image.open(f).convert("RGB")
    w0 = im.width
    # always emit the native width too, so a srcset can never point at a file
    # we declined to generate (this is what broke the hero <picture> on retina)
    todo = sorted({w for w in WIDTHS if w <= w0} | {w0})
    for w in todo:
        h = round(im.height * w / w0)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(os.path.join(SRC_IMG, f"{stem}-{w}.webp"), "WEBP", quality=82, method=6)
        r.save(os.path.join(SRC_IMG, f"{stem}-{w}.jpg"), "JPEG", quality=82,
               optimize=True, progressive=True)
    print("photo", stem, im.size)

print("done")
