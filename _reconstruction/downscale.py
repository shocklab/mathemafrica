#!/usr/bin/env python3
"""Downscale the recovered camera originals to a sane web size.

Only JPEGs whose longest side exceeds MAXSIDE are touched. GIFs are left
alone (two are animated), and no PNG in the set is large enough to qualify,
so plots and screenshots keep their lossless pixels. EXIF orientation is
baked into the pixels before the metadata is dropped, so nothing rotates.
"""
import glob, os
from PIL import Image, ImageOps

R = "/Users/jonathanshock/Cursor folders/Mathemafrica"
MAXSIDE, QUALITY, FLOOR = 1600, 85, 1_500_000

before = after = 0
done = skipped = 0
log = []
for p in sorted(glob.glob(R + "/wp-content/uploads/**/*", recursive=True)):
    if not os.path.isfile(p): continue
    sz = os.path.getsize(p)
    if sz <= FLOOR: continue
    try:
        im = Image.open(p)
        if im.format != "JPEG" or max(im.width, im.height) <= MAXSIDE:
            skipped += 1; im.close(); continue
        w0, h0 = im.width, im.height
        im = ImageOps.exif_transpose(im)
        im.thumbnail((MAXSIDE, MAXSIDE), Image.LANCZOS)
        im.convert("RGB").save(p, "JPEG", quality=QUALITY,
                               optimize=True, progressive=True)
        im.close()
    except Exception as e:
        log.append(f"ERROR {p}: {e}"); continue
    sz2 = os.path.getsize(p)
    before += sz; after += sz2; done += 1
    log.append(f"{w0}x{h0} -> {MAXSIDE}px   {sz/1048576:5.2f}MB -> {sz2/1048576:5.2f}MB   {os.path.basename(p)}")

print(f"resized {done} files, skipped {skipped}")
print(f"{before/1048576:.0f} MB -> {after/1048576:.0f} MB  ({100*(1-after/before):.0f}% smaller)")
open(SP_LOG := "/private/tmp/claude-501/-Users-jonathanshock-Cursor-folders-Mathematica/fa8467c2-86f9-4523-91a8-5388d8cc081c/scratchpad/downscale.log", "w").write("\n".join(log))
