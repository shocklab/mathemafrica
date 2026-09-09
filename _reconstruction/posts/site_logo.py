#!/usr/bin/env python3
"""Restore the header logo on the fourteen earliest posts.

`mathemafrica-logo-subline-cut.png` and its retina twin are the header logo on
p=1 and the p=101xx posts, and both are lost, so those pages currently show a
broken image where the masthead should be. The Wayback Machine has no capture
of either, under the site's own host or the Jetpack CDN.

The same artwork did survive, as `2015/06/mathemafirca-logo-2.jpg`: the
wordmark over its subline, which is exactly what "subline" in the filenames
refers to, and it is what the later pages still show in their headers. These
two files are that image transcoded, not a redrawing, so they carry no
reconstruction marker; a marker on a masthead would be odd, and there is
nothing reconstructed about it.

The source is 300x45, and the theme displays the logo at about that size, so
both files are written at native resolution. Upscaling for the retina variant
would add no detail, only softness.
"""
import os
from PIL import Image

REPO = "/Users/jonathanshock/Cursor folders/Mathemafrica"
UPLOADS = os.path.join(REPO, "wp-content", "uploads")
SRC = os.path.join(UPLOADS, "2015", "06", "mathemafirca-logo-2.jpg")
TARGETS = ["2014/12/mathemafrica-logo-subline-cut.png",
           "2014/12/mathemafrica-logo-subline-retina-cut.png"]

src = Image.open(SRC).convert("RGB")
print(f"  source: {SRC.split('uploads/')[1]}  {src.width}x{src.height}")
for t in TARGETS:
    out = os.path.join(UPLOADS, t)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    src.save(out, "PNG")
    print(f"  wrote {t}  {src.width}x{src.height}")
print("  site logo: 2 files written (transcoded from the surviving artwork)")
