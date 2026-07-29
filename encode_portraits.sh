#!/bin/bash
# Encode a generated living portrait into a seamless grayscale loop.
# Ping-pong (forward + reversed) so neutral -> smile -> neutral cycles with no jump.
set -e
cd "$(dirname "$0")"
OUT=build/assets/athletes/live
mkdir -p "$OUT"

for name in "$@"; do
  url=$(grep -o 'https[^ ]*\.mp4' "gen/portrait/${name}.url" 2>/dev/null | head -1) || true
  if [ -z "$url" ]; then echo "SKIP $name (no url)"; continue; fi
  raw="gen/portrait/${name}_raw.mp4"
  [ -f "$raw" ] || curl -sL "$url" -o "$raw"

  W=$(ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 "$raw")
  H=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$raw")
  # the seed was padded to 3:4; crop back to the original 2:3 from the centre
  CW=$(python3 -c "print(int(round($H*2/3)))")
  OFF=$(python3 -c "print(max(0,int(round(($W-$CW)/2))))")

  ffmpeg -v error -i "$raw" \
    -vf "crop=${CW}:${H}:${OFF}:0,scale=400:600,hue=s=0,eq=contrast=1.04,fps=25,trim=0:4.2,setpts=PTS-STARTPTS" \
    -an -y "/tmp/${name}_f.mp4"
  ffmpeg -v error -i "/tmp/${name}_f.mp4" -vf reverse -an -y "/tmp/${name}_r.mp4"
  printf "file '/tmp/%s_f.mp4'\nfile '/tmp/%s_r.mp4'\n" "$name" "$name" > "/tmp/${name}_cat.txt"

  ffmpeg -v error -f concat -safe 0 -i "/tmp/${name}_cat.txt" \
    -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart -an -y "$OUT/${name}.mp4"
  ffmpeg -v error -f concat -safe 0 -i "/tmp/${name}_cat.txt" \
    -c:v libvpx-vp9 -crf 38 -b:v 0 -row-mt 1 -an -y "$OUT/${name}.webm"
  echo "ok $name  $(du -h "$OUT/${name}.mp4" | cut -f1)"
done
