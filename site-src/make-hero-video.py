#!/usr/bin/env python3
"""Cut the home-page hero loop from raw and edited clips.

Usage: python3 site-src/make-hero-video.py <folder-with-clips> [hero-1080.mp4|hero-720.mp4]
Needs ffmpeg. Reads the clips named in SEGMENTS from the folder and writes
  site-src/video/hero-1080.mp4   1920x1080 loop for screens 900px and wider
  site-src/video/hero-720.mp4    1280x720 loop for phones (the phone hero box is 4:3, so landscape fits it)
  site-src/video/hero-poster.jpg a frame from the loop
Muted, no audio track, H.264 high profile, faststart. The page plays it inline, looping.

Source clips (Dropbox, GCI Admin/Videos and Photos):
  2022/2022_07/Osgood Park New Britain/DJI_0157.MP4            -> osgood-dozer.MP4
  Edited Videos & Photos/Tradewind November 2025/Videos/
    GCI.251106.AberdeenEstates.h0040.101.mp4                   -> tw-aberdeen-estates.mp4
    GCI.251120.350BarbourSiteUpdate.h0031.102.mp4              -> tw-350-barbour.mp4
    GCI.251121.GoodwinIndustryUpdate.h0026.101.mp4             -> tw-goodwin.mp4
    GCI.251121.AbbottRdSiteUpdate.h0033.102.mp4                -> tw-abbott-rd.mp4
    GCI.251121.WestHartfordCenterUpdate.h0032.102.mp4          -> tw-west-hartford-center.mp4
    GCI.251106.183StateSt.h0038.101.mp4                        -> tw-183-state-st.mp4
  The Tradewind cuts end with a Gerber logo card (last 3-4 s); none of that is used. The 2023 compilation
  (GCI.230418.Compilation) was rejected: motion-graphics text and colored blocks throughout.

Evan's order (Oct 28): open on the red Gerber truck being loaded (two Gerber logos in frame), the haul truck
being loaded second to last, the dozer pushing dirt last.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "video")

# (file, start seconds, length seconds, grade[, crossfade into the next segment]).
# grade=True lifts the overcast Tradewind footage a little. The default crossfade is FADE; the opener uses quick cuts.
# Order is the order in the loop.
SEGMENTS = [
    ("tw-350-barbour.mp4", 1.0, 1.0, True, 0.3),       # red Gerber truck passing, GERBER on the box (open)
    ("tw-350-barbour.mp4", 4.0, 1.5, True, 0.3),       # excavator and the red truck, two Gerber logos
    ("tw-350-barbour.mp4", 7.4, 1.6, True),            # Komatsu dumping into the red bed
    ("tw-goodwin.mp4", 16.0, 4.0, True),               # crew with the mini excavator, laying pipe
    ("tw-abbott-rd.mp4", 8.0, 5.0, True),              # bucket dumping, crew at the excavation
    ("tw-west-hartford-center.mp4", 8.8, 4.2, True),   # raking asphalt, paving crew (8.0-8.7 is a torch flame; 13+ shows a sub's roller)
    ("tw-west-hartford-center.mp4", 22.0, 3.0, True),  # roller, steam, then the drone over the paving
    ("tw-183-state-st.mp4", 27.0, 6.0, True),          # drone straight down on the street trench and truck
    ("tw-350-barbour.mp4", 23.6, 3.3, True),           # excavator digging, then GERBER on the boom
    ("tw-aberdeen-estates.mp4", 4.0, 6.0, True),       # excavator loading the haul truck (second to last)
    ("osgood-dozer.MP4", 8.0, 6.0, False),             # dozer pushing, dust rolling (last)
]
FADE = 0.8  # crossfade between segments, seconds
SEAM = 0.5  # fade through brand green at the loop point, seconds
GREEN = "0x0B422E"
GRADE = "eq=brightness=0.035:contrast=1.07:saturation=1.10"
CLEAN = "hqdn3d=1.2:1.2:3:3"  # light temporal/spatial denoise: less grain, better compression

OUTPUTS = [  # name, width, height, crf
    ("hero-1080.mp4", 1920, 1080, 31),
    ("hero-720.mp4", 1280, 720, 29),
]


def run(cmd):
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def graph(width, height):
    """Per-input trim/scale/grade, chained xfade, then the loop-seam fades."""
    parts = []
    for i, seg in enumerate(SEGMENTS):
        grade = seg[3]
        vf = ["fps=30", f"scale={width}:{height}:force_original_aspect_ratio=increase", f"crop={width}:{height}", CLEAN]
        if grade:
            vf.append(GRADE)
        vf += ["setpts=PTS-STARTPTS", "format=yuv420p"]
        parts.append(f"[{i}:v]{','.join(vf)}[v{i}]")
    prev = "v0"
    offset = 0.0
    for i in range(1, len(SEGMENTS)):
        fade = SEGMENTS[i - 1][4] if len(SEGMENTS[i - 1]) > 4 else FADE
        offset += SEGMENTS[i - 1][2] - fade
        parts.append(f"[{prev}][v{i}]xfade=transition=fade:duration={fade}:offset={offset:.3f}[x{i}]")
        prev = f"x{i}"
    total = offset + SEGMENTS[-1][2]
    parts.append(f"[{prev}]fade=t=in:st=0:d={SEAM}:color={GREEN},fade=t=out:st={total - SEAM:.3f}:d={SEAM}:color={GREEN}[out]")
    return ";".join(parts)


def make(src, name, width, height, crf):
    inputs = []
    for seg in SEGMENTS:
        f, start, length = seg[0], seg[1], seg[2]
        path = os.path.join(src, f)
        if not os.path.exists(path):
            sys.exit(f"missing clip: {path}")
        inputs += ["-ss", f"{start}", "-t", f"{length}", "-i", path]
    out = os.path.join(OUT, name)
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph(width, height), "-map", "[out]", "-an",
         "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-preset", "slow", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", "30", out])
    print(f"wrote {out} ({os.path.getsize(out) // 1024} KB, {width}x{height})")
    return out


def main(src, only=None):
    os.makedirs(OUT, exist_ok=True)
    for name, w, h, crf in OUTPUTS:
        if only and name != only:
            continue
        out = make(src, name, w, h, crf)
        if name == OUTPUTS[0][0]:
            run(["ffmpeg", "-y", "-v", "error", "-ss", "1.5", "-i", out, "-frames:v", "1", "-q:v", "3",
                 os.path.join(OUT, "hero-poster.jpg")])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
