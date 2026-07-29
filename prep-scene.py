"""
Prepare the science-section composition: one wide rectangle over two squares.

  rect  — the hooded triptych (already a 3-panel wide image). Grayscale + the
          dark tint. Kept whole; it is the rectangle.
  sq-m  — the towel athlete, cropped to a clean square around him.
  sq-w  — the cable athlete, cropped to a square tight on her so the trade-show
          crowd behind her falls outside the frame.

All three: grayscale, dark tint, so they read as one family with the rest of
the site.
"""
from PIL import Image, ImageEnhance
import pathlib

SRC = pathlib.Path("source-media")
OUT = pathlib.Path("build/assets/img/layer")
OUT.mkdir(parents=True, exist_ok=True)


def grade(im):
    im = ImageEnhance.Color(im).enhance(0)          # grayscale
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Brightness(im).enhance(.46)   # the dark tint
    return im


def square(im, cx, cy, frac):
    """Crop a square `frac` of the shorter side, centred on (cx, cy) in [0,1]."""
    side = round(min(im.width, im.height) * frac)
    x = round(im.width * cx - side / 2)
    y = round(im.height * cy - side / 2)
    x = max(0, min(x, im.width - side))
    y = max(0, min(y, im.height - side))
    return im.crop((x, y, x + side, y + side))


def save(im, stem, widths):
    for w in widths:
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f"{stem}-{w}.webp", "WEBP", quality=82, method=6)
        r.save(OUT / f"{stem}-{w}.jpg", "JPEG", quality=80, optimize=True,
               progressive=True)
    print(f"  {stem}  {im.size}")


# rectangle — the triptych, whole
rect = grade(Image.open(SRC / "triptych.png").convert("RGB"))
save(rect, "rect", (1350, 1000, 680))

# square — towel athlete, centred on him
m = grade(square(Image.open(SRC / "square-towel.png").convert("RGB"),
                 cx=.57, cy=.52, frac=1.0))
save(m, "sq-m", (700, 500, 340))

# square — cable athlete, tight so the crowd is cropped away
w = grade(square(Image.open(SRC / "square-woman.png").convert("RGB"),
                 cx=.30, cy=.34, frac=.62))
save(w, "sq-w", (700, 500, 340))
