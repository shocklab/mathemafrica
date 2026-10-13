#!/usr/bin/env python3
"""Replace the s0.wp.com/latex.php equation images with MathJax source.

Every equation on the blog was an <img> whose URL carried the LaTeX, rendered
by WordPress.com's latex service. This puts that LaTeX back into the page as
\\( ... \\) (or \\[ ... \\] when the equation is the whole paragraph, which is
how the posts set displayed equations) and loads a copy of MathJax 3.2.2 kept
in mathjax/, so the site no longer depends on wordpress.com.

A few constructs WordPress's real LaTeX accepted and MathJax does not are
rewritten on the way (see `adapt`). Mathematica code quoted in posts contains
\\[Pi], which MathJax would read as an opening display delimiter, so the
paragraph holding it is marked tex2jax_ignore.

Usage: latex_to_mathjax.py [files...]   (default: every *.html at the root)
Running it twice changes nothing.
"""
import glob
import html
import os
import re
import sys
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMG = re.compile(r'''<img\b[^>]*?\bsrc=(?P<q>["'])(?:https?:)?//s0\.wp\.com/'''
                 r'''latex\.php\?([^"']*)(?P=q)[^>]*>''')
# a paragraph whose only content is one equation image is a displayed equation
DISPLAY = re.compile(r'(<p\b[^>]*>)(?:\s|&nbsp;|<br\s*/?>)*(' + IMG.pattern
                     + r')(?:\s|&nbsp;|<br\s*/?>)*(</p>)')
SCRIPT = ('<script async id="MathJax-script" '
          'src="mathjax/tex-chtml-full.js"></script>')


def adapt(tex):
    """Rewrite the few WordPress-LaTeX constructs MathJax rejects."""
    # minipage only set a width around an align*; MathJax sizes it itself
    tex = re.sub(r'\\begin\{minipage\}\{[^}]*\}|\\end\{minipage\}', '', tex)
    # \hfill(1) pushed an equation number to the margin
    tex = re.sub(r'\\hfill\s*\(([^)]*)\)', r'\\qquad(\1)', tex)
    tex = re.sub(r'\\hfill', '', tex)
    tex = tex.replace(r'\Big\slash', r'\Big/')
    return tex.strip()


def source(query):
    params = dict(urllib.parse.parse_qsl(html.unescape(query),
                                         keep_blank_values=True))
    return adapt(params.get("latex", ""))


def convert(s):
    n = 0

    def disp(m):
        nonlocal n
        n += 1
        tex = source(m.group(4))
        return f"{m.group(1)}\\[{html.escape(tex, quote=False)}\\]{m.group(5)}"

    def inline(m):
        nonlocal n
        n += 1
        tex = source(m.group(2))
        return f"\\({html.escape(tex, quote=False)}\\)"

    s = DISPLAY.sub(disp, s)
    s = IMG.sub(inline, s)
    return s, n


def guard_mathematica(s):
    """Mark paragraphs quoting Mathematica's \\[Pi] so MathJax skips them."""
    out, last = [], 0
    for m in re.finditer(r'\\\[(?=[A-Z][A-Za-z]*\])', s):
        start = s.rfind("<p", last, m.start())
        tag_end = s.find(">", start)
        if start < 0 or "tex2jax_ignore" in s[start:tag_end]:
            continue
        out.append(s[last:start])
        out.append('<p class="tex2jax_ignore"' + s[start + 2:tag_end])
        last = tag_end
    out.append(s[last:])
    return "".join(out)


def main(paths):
    pages = eqs = 0
    for p in paths:
        s = open(p, encoding="utf-8", errors="surrogateescape").read()
        t, n = convert(s)
        t = guard_mathematica(t)
        if (n or "\\(" in t or "\\[" in t) and SCRIPT not in t \
                and "</head>" in t:
            t = t.replace("</head>", SCRIPT + "\n</head>", 1)
        if t != s:
            open(p, "w", encoding="utf-8", errors="surrogateescape").write(t)
            pages += 1
            eqs += n
    print(f"{eqs} equations converted in {pages} pages")


if __name__ == "__main__":
    main(sys.argv[1:] or sorted(glob.glob(os.path.join(REPO, "*.html"))))
