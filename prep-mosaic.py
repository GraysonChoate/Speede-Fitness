"""
Build the science-section backdrop: a mosaic of stills from Speede's own
"WORK FOR IT." film.

Why a composited file instead of a CSS grid of images: the seams need to be
feathered into each other so it reads as one dark field rather than eight
pasted rectangles, and that is far easier to control here than in CSS.

Two constraints drive the composition:

* The film has "WORK FOR IT." burned in at ~54% of every frame's height, so
  nothing below y=0.50 of a source frame is usable.
* The two live cards cover x 205–1305 of a 1512-wide section. Anything placed
  mid-canvas is invisible. The faces are therefore pushed into the outer
  columns, which is the only part the viewer ever sees, and the middle column
  carries quiet texture (brick, cable, equipment) that loses nothing by being
  covered.

Run after prep-layers.py. Needs the frames ffmpeg drops in frames/.
"""
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import pathlib
import subprocess

SRC = pathlib.Path("source-media")
FRAMES = pathlib.Path(".frames")               # scratch, outside build/
OUT = pathlib.Path("build/assets/img/layer")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1240, 1680                                # canvas; section is ~1512x2000
TEXT_SAFE = 0.50                                 # usable top fraction of a frame


def extract():
    """One frame per second from the two black-and-white clips."""
    FRAMES.mkdir(parents=True, exist_ok=True)
    if list(FRAMES.glob("clip1-*.jpg")):
        return
    for clip in ("clip1", "clip2"):
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", str(SRC / f"{clip}.mov"),
             "-vf", "fps=1", "-q:v", "2", str(FRAMES / f"{clip}-%02d.jpg")],
            check=True)


def tile(name, box, focus=(.5, .5)):
    """Crop `name` above the burned-in line and cover-fit it to box (w, h)."""
    im = Image.open(FRAMES / f"{name}.jpg").convert("RGB")
    im = im.crop((0, 0, im.width, int(im.height * TEXT_SAFE)))
    bw, bh = box
    scale = max(bw / im.width, bh / im.height)
    im = im.resize((max(bw, round(im.width * scale)), max(bh, round(im.height * scale))),
                   Image.LANCZOS)
    x = round((im.width - bw) * focus[0])
    y = round((im.height - bh) * focus[1])
    return im.crop((x, y, x + bw, y + bh))


def feather(size, edge=54):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rectangle((edge, edge, size[0] - edge - 1, size[1] - edge - 1),
                                fill=255)
    return m.filter(ImageFilter.GaussianBlur(edge * .62))


# (frame, x, y, w, h, focus) — outer columns carry the faces, middle carries
# texture. Tiles overlap by ~40px so the feathering has something to blend into.
PLAN = [
    # left column
    ("clip1-08", -30,  -30, 470, 640, (.34, .40)),   # the eye
    ("clip2-09", -30,  560, 470, 640, (.42, .30)),   # back and shoulder
    ("clip1-03", -30, 1130, 470, 580, (.46, .35)),   # forearm, carabiner
    # middle column — sits behind the cards
    ("clip1-07", 420, -30, 440, 900, (.50, .45)),
    ("clip1-10", 420,  840, 440, 870, (.50, .45)),
    # right column
    ("clip2-04", 800,  -30, 470, 600, (.62, .45)),   # face, mid-effort
    ("clip1-07", 800,  540, 470, 620, (.72, .40)),   # bar against brick
    ("clip1-05", 800, 1100, 470, 610, (.60, .45)),   # the spot
]


def main():
    extract()
    canvas = Image.new("RGB", (W, H), "#07090a")
    for name, x, y, w, h, focus in PLAN:
        t = tile(name, (w, h), focus)
        canvas.paste(t, (x, y), feather((w, h)))

    canvas = ImageEnhance.Color(canvas).enhance(0)
    canvas = ImageEnhance.Contrast(canvas).enhance(1.10)
    canvas = ImageEnhance.Brightness(canvas).enhance(.42)

    for w in (1240, 900, 600):
        r = canvas.resize((w, round(H * w / W)), Image.LANCZOS)
        r.save(OUT / f"mosaic-{w}.webp", "WEBP", quality=80, method=6)
        r.save(OUT / f"mosaic-{w}.jpg", "JPEG", quality=78, optimize=True,
               progressive=True)
        print(f"  mosaic-{w}  {r.size}")


if __name__ == "__main__":
    main()
