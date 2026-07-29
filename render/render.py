"""Render the code-built data montage to frames, then encode to mp4.
Deterministic: we drive window.frame(p) per frame rather than relying on rAF,
so every number on screen is exactly what the code says it is."""
import os, subprocess, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))

FPS, SECONDS = 30, 11.0
TOTAL = int(FPS * SECONDS)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_context(viewport={"width": 1280, "height": 720},
                      device_scale_factor=1).new_page()
    p.goto("file://" + os.path.join(HERE, "montage.html"))
    p.wait_for_timeout(900)          # let the fonts land
    for i in range(TOTAL):
        p.evaluate("window.frame(%f)" % (i / (TOTAL - 1)))
        p.screenshot(path=os.path.join(OUT, "f%04d.png" % i))
        if i % 30 == 0:
            print("frame", i, "/", TOTAL, flush=True)
    b.close()

mp4 = os.path.join(HERE, "data-montage.mp4")
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-framerate", str(FPS),
    "-i", os.path.join(OUT, "f%04d.png"),
    "-c:v", "libx264", "-crf", "20", "-preset", "slow",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4
], check=True)
print("wrote", mp4)
