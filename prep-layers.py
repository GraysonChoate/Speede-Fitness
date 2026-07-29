"""
Prepare the two team-supplied photographs as background layers.

Both are pushed near-monochrome and dark on purpose: they sit *behind* live
content (the 500 numeral, the science cards) and must read as texture, not as a
competing subject. The darkening is baked into the file rather than done with a
CSS overlay so there is only ever one thing dimming the picture — the hero
taught us what three stacked scrims does.
"""
from PIL import Image, ImageEnhance
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
# Crop the Instagram chrome off (hamburger top-right, avatar bottom-left) and
# take a wide band through the figure. The band is deliberately close to the
# band's own 1.8:1 aspect so `object-fit: cover` barely has to zoom — a square
# crop blew the athlete up until he read as wall, not as a person.
#
# The grade is heavy. A headline sits over the top half of this and the
# concrete is the brightest thing in the frame, so the wall has to come down
# far enough that white type on it is never in question.
im = Image.open(src("12.14.41")).convert("RGB")
w, h = im.size
im = im.crop((int(w * .04), int(h * .34), int(w * .97), int(h * .99)))
im = ImageEnhance.Color(im).enhance(.18)
im = ImageEnhance.Contrast(im).enhance(1.14)
im = ImageEnhance.Brightness(im).enhance(.27)
print("effort", im.size)
save(im, "effort", (1600, 1100, 760))

# ── grip: hand on bar, behind the science cards ──────────────────────────────
# Already monochrome. Only needs to lose the last of its colour cast and drop
# far enough that the card gradients sit cleanly on top of it. This one only
# ever shows in slivers around the cards, right next to near-black panel edges,
# so the blurred wall behind the bar has to go darker than feels right in
# isolation — at full strength it reads as a hole punched in the section.
im2 = Image.open(src("12.15.23")).convert("RGB")
im2 = ImageEnhance.Color(im2).enhance(0)
im2 = ImageEnhance.Contrast(im2).enhance(1.16)
im2 = ImageEnhance.Brightness(im2).enhance(.40)
print("grip", im2.size)
save(im2, "grip", (1600, 1100, 760))
