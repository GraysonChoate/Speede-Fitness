"""
Prepare the two team-supplied photographs as background layers.

Both are pushed near-monochrome and dark on purpose: they sit *behind* live
content (the 500 numeral, the science cards) and must read as texture, not as a
competing subject. The darkening is baked into the file rather than done with a
CSS overlay so there is only ever one thing dimming the picture — the hero
taught us what three stacked scrims does.
"""
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import pathlib

SRC = pathlib.Path("source-media")
OUT = pathlib.Path("build/assets/img/layer")
OUT.mkdir(parents=True, exist_ok=True)


def src(stamp):
    """macOS puts a narrow no-break space before AM/PM, so match on the stamp."""
    hits = [p for p in SRC.glob("Screenshot*.png") if stamp in p.name]
    if len(hits) != 1:
        raise SystemExit(f"{stamp}: expected 1 match, got {hits}")
    return hits[0]


def save(im, stem, widths):
    for w in widths:
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f"{stem}-{w}.webp", "WEBP", quality=82, method=6)
        r.save(OUT / f"{stem}-{w}.jpg", "JPEG", quality=80, optimize=True,
               progressive=True)
        print(f"  {stem}-{w}  {r.size}")


# ── effort: bench press, behind the 500 ──────────────────────────────────────
# The whole point of this frame is the hand at the top gripping the handle and
# the cable running down the arm, so the crop has to keep the full height — a
# wide band through the torso threw all of that away. It is placed as a tall
# panel on the right of the band rather than a full-bleed backdrop, which is
# also the only way a ~1:1 composition survives without being blown up.
#
# The Instagram hamburger sits top-right at almost exactly the same height as
# the hand, so it can't be cropped off without losing the hand too. It gets
# patched out with clean wall lifted from directly below it instead.
im = Image.open(src("12.14.41")).convert("RGB")
w, h = im.size
BOX = (1505, 35, 1665, 215)                       # the hamburger, with margin
donor = im.crop((BOX[0], BOX[1] + 210, BOX[2], BOX[3] + 210))   # wall below it
donor = donor.filter(ImageFilter.GaussianBlur(28))              # kill its detail
feather = Image.new("L", donor.size, 0)                         # soft-edged alpha
ImageDraw.Draw(feather).rectangle((14, 14, donor.width - 15, donor.height - 15),
                                  fill=255)
im.paste(donor, BOX[:2], feather.filter(ImageFilter.GaussianBlur(11)))
im = im.crop((int(w * .06), int(h * .01), int(w * .99), int(h * .99)))
im = ImageEnhance.Color(im).enhance(.18)
im = ImageEnhance.Contrast(im).enhance(1.14)
im = ImageEnhance.Brightness(im).enhance(.34)
print("effort", im.size)
save(im, "effort", (1200, 900, 620))

# The science section's backdrop is built separately — see prep-mosaic.py.
