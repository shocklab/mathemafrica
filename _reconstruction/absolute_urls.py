#!/usr/bin/env python3
"""Make the og:url, og:image and canonical addresses absolute under a base URL.

Link previews (Facebook, WhatsApp, Slack, X) and search engines read these
tags without resolving them against the page, so a relative value is useless
to them. Every other link on the site stays relative.

Usage: absolute_urls.py https://mathemafrica.org/

Rerun with the new base when the site moves; a value already absolute under
any base this script has written is rewritten to the new one. An og:image
whose file is not in the archive, or that is Jetpack's blank placeholder,
falls back to the site logo.
"""
import glob
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = "wp-content/uploads/2015/06/mathemafirca-logo-2.jpg"
OLD_BASES = ("https://shocklab.github.io/mathemafrica/",
             "https://mathemafrica.org/", "https://www.mathemafrica.org/")
TAG = re.compile(r'(<meta property="og:(?:url|image)" content="|'
                 r'<link rel="canonical" href=")([^"]*)(")')


def relative(v):
    for b in OLD_BASES:
        if v.startswith(b):
            return v[len(b):]
    return None if re.match(r"[a-z]+:|//", v) else v


def fix(base, page, m):
    if m.group(2) == "https://s0.wp.com/i/blank.jpg":  # Jetpack's placeholder
        return m.group(1) + base + LOGO + m.group(3)
    rel = relative(m.group(2))
    if rel is None:                      # points off-site; leave it
        return m.group(0)
    if rel in ("", "./"):
        rel = ""
    if "og:image" in m.group(1):
        f = rel.split("?")[0]
        if not os.path.exists(os.path.join(REPO, f)):
            rel = LOGO
    return m.group(1) + base + rel + m.group(3)


def main(base):
    if not base.endswith("/"):
        base += "/"
    changed = 0
    for p in sorted(glob.glob(os.path.join(REPO, "*.html"))):
        s = open(p, encoding="utf-8", errors="surrogateescape").read()
        t = TAG.sub(lambda m: fix(base, p, m), s)
        if t != s:
            open(p, "w", encoding="utf-8", errors="surrogateescape").write(t)
            changed += 1
    print(f"{changed} pages updated to {base}")


if __name__ == "__main__":
    main(sys.argv[1])
