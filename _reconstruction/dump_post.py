#!/usr/bin/env python3
"""Print an archived post as readable prose, ready for figure reconstruction.

Images are replaced by [[[FIGURE ...]]] markers carrying the filename, whether
the file is present or lost, and the width the page displays it at. Equations
are decoded out of the latex.php URLs back into $...$ source. Usage:

    python3 dump_post.py p=14953.html
"""
import html as H
import os
import re
import sys
import textwrap
import urllib.parse

REPO = "/Users/jonathanshock/Cursor folders/Mathemafrica"

LATEX = re.compile(r'<img[^>]*?latex\.php\?latex=(.*?)(?:&|")[^>]*?>')
IMG = re.compile(r'<img[^>]*?src="(wp-content/uploads/[^"]+)"[^>]*?>')


def detex(s):
    return urllib.parse.unquote(H.unescape(s).replace("+", " ")).strip()


def main(name):
    path = os.path.join(REPO, name)
    h = open(path, encoding="utf-8", errors="replace").read()
    title = re.search(r"<title>([^<]*)</title>", h)
    print("POST:", H.unescape(title.group(1)) if title else name)

    m = re.search(r'<div class="post-content"(.*?)<div class="fusion-meta-info"',
                  h, re.S)
    body = m.group(1) if m else h

    def figure(mo):
        raw = mo.group(1)
        p = urllib.parse.unquote(raw.split("?")[0])
        w = re.search(r"(?:resize|fit)=(\d+)%2C(\d+)", mo.group(0))
        dims = f" shown {w.group(1)}x{w.group(2)}" if w else ""
        state = "PRESENT" if os.path.exists(os.path.join(REPO, p)) else "LOST"
        cap = ""
        return f"\n\n[[[FIGURE {state}: {os.path.basename(p)}{dims}]]]{cap}\n\n"

    # Stash equations and figures behind angle-bracket-free placeholders BEFORE
    # stripping tags: decoded LaTeX often contains "<", which the tag stripper
    # would otherwise eat along with the inequality it belongs to.
    stash = []

    def keep(text):
        stash.append(text)
        return f" \x00{len(stash) - 1}\x00 "

    body = LATEX.sub(lambda mo: keep("$" + detex(mo.group(1)) + "$"), body)
    body = IMG.sub(lambda mo: keep(figure(mo)), body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\x00(\d+)\x00", lambda mo: stash[int(mo.group(1))], body)
    txt = re.sub(r"[ \t]+", " ", H.unescape(body))
    txt = re.sub(r"\n\s*\n+", "\n\n", txt).strip()
    print("=" * 96)
    for para in txt.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.startswith("[[["):
            print("\n" + para + "\n")
        else:
            print(textwrap.fill(para, 94))


if __name__ == "__main__":
    main(sys.argv[1])
