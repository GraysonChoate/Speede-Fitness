"""
Prepare the two photographs hung on the science section — the "wall".

Not a backdrop and not a mosaic. Two framed pictures on an otherwise clean
wall, hung on a diagonal: the woman high on the right, the man low on the left.
Everything before this was one image stretched across the whole wall, which
read as texture, not as a picture of anything.

Both are graded dark in the file so nothing dims them a second time downstream.

  athlete-w  — the bent-over row (source screenshot). A standing figure, so it
               gets a tall portrait crop for the tall right-hand spot.
  athlete-m  — the SPEEDE-shirt athlete from the film, cropped above the
               burned-in "WORK FOR IT." title. The pendant to her: standing
               where she bends, and carrying the logo.
"""
from PIL import Image, ImageEnhance
import pathlib
import subprocess

SRC = pathlib.Path("source-media")
FRAMES = pathlib.Path(".frames")
OUT = pathlib.Path("build/assets/img/layer")
OUT.mkdir(parents=True, exist_ok=True)


def src(stamp):
    hits = [p for p in SRC.glob("Screenshot*.png") if stamp in p.name]
    if len(hits) != 1:
        raise SystemExit(f"{stamp}: expected 1 match, got {hits}")
    return hits[0]


def frame(name):
    """Pull one still out of the film if it isn't already cached."""
    out = FRAMES / f"{name}.jpg"
    if not out.exists():
        FRAMES.mkdir(parents=True, exist_ok=True)
        clip, idx = name.rsplit("-", 1)          # clip1-009 -> clip1, 009
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", str(SRC / f"{clip}.mov"),
             "-vf", f"select=eq(n\\,{int(idx) * 15})", "-frames:v", "1", str(out)],
            check=True)
    return out


def save(im, stem, widths):
    for w in widths:
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f"{stem}-{w}.webp", "WEBP", quality=82, method=6)
        r.save(OUT / f"{stem}-{w}.jpg", "JPEG", quality=80, optimize=True,
               progressive=True)
    print(f"  {stem}  {im.size}")


# ── athlete-w: the bent-over row, hung high-right ────────────────────────────
# Native 702x898. Trim a little headroom and floor so she fills a tall frame
# from the bar up to her shoulders.
w = Image.open(src("12.15.35")).convert("RGB")
w = w.crop((0, int(w.height * .02), w.width, int(w.height * .90)))
w = ImageEnhance.Color(w).enhance(0)
w = ImageEnhance.Contrast(w).enhance(1.06)
w = ImageEnhance.Brightness(w).enhance(.56)
save(w, "athlete-w", (760, 560, 380))

# ── athlete-m: the SPEEDE-shirt athlete, hung low-left ───────────────────────
# He stands in the left third of the frame against a lot of empty brick. Crop
# to his figure so *he* is the picture, not the wall behind him. The film burns
# "WORK FOR IT." in at ~54% height, so the bottom stops above it — head,
# shoulders, the logo and the handle in his hand.
m = Image.open(frame("clip1-009")).convert("RGB")
m = m.crop((0, 0, int(m.width * .52), int(m.height * .505)))
m = ImageEnhance.Color(m).enhance(0)
m = ImageEnhance.Contrast(m).enhance(1.06)
m = ImageEnhance.Brightness(m).enhance(.54)
save(m, "athlete-m", (620, 460, 320))
