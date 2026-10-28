#!/usr/bin/env python3
"""Make web-sized copies of the photos in a folder of originals.

Usage: python3 site-src/make-web-images.py <folder-with-originals>
Reads every *.jpg/*.jpeg/*.JPG whose basename (without extension) is a slug from site-src/photos.txt,
auto-orients it, applies any options from the manifest, and writes site-src/img/<slug>-2400.jpg and
<slug>-1200.jpg (progressive JPEG, metadata stripped).

Manifest options (third field on a photos.txt line, space-separated):
  crop-bottom:22   trim the bottom 22% of the frame (removes a date/location stamp)
  crop-top:10      trim the top 10%
"""
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "img")


def manifest():
    """Return {slug: {option: value}} from photos.txt."""
    out = {}
    for line in open(os.path.join(ROOT, "photos.txt"), encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        opts = {}
        if len(parts) > 2:
            for tok in parts[2].split():
                k, _, v = tok.partition(":")
                opts[k] = float(v) if v else True
        out[parts[0]] = opts
    return out


def apply_options(im, opts):
    w, h = im.size
    top = int(h * opts.get("crop-top", 0) / 100)
    bottom = h - int(h * opts.get("crop-bottom", 0) / 100)
    if top or bottom != h:
        im = im.crop((0, top, w, bottom))
    return im


def write_sizes(im, slug):
    for width, q in ((2400, 82), (1200, 80)):
        copy = im.copy()
        copy.thumbnail((width, width), Image.LANCZOS)
        copy.save(os.path.join(OUT, f"{slug}-{width}.jpg"), "JPEG", quality=q, optimize=True, progressive=True)


def main(src):
    os.makedirs(OUT, exist_ok=True)
    wanted = manifest()
    done, missing = [], []
    files = {os.path.splitext(f)[0].lower(): os.path.join(src, f) for f in os.listdir(src)
             if f.lower().endswith((".jpg", ".jpeg"))}
    for slug in sorted(wanted):
        path = files.get(slug.lower())
        if not path:
            missing.append(slug)
            continue
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        im = apply_options(im, wanted[slug])
        write_sizes(im, slug)
        done.append(f"{slug} {im.size[0]}x{im.size[1]}")
    print("made:", len(done))
    for d in done:
        print("  ", d)
    if missing:
        print("missing:", ", ".join(missing))


if __name__ == "__main__":
    main(sys.argv[1])
