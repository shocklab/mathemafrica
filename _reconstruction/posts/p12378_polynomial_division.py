#!/usr/bin/env python3
"""p=12378, "Polynomial division".

step0.png ... step9.png are ten frames of one long-division tableau for
(2x^4 - 6x) / (x^2 + 3x - 2), each adding what the numbered step in the text
says it adds. The post's recorded display heights are

    79, 138, 195, 258, 258, 309, 369, 369, 417, 466

which grow by about one row per frame and by nothing at all at steps 4 and 7,
exactly where the text only extends the quotient line rather than writing a new
row. That is what fixes the frame contents below.

The post takes the short route deliberately: at step 4 it divides only the
-6x^3 term, "we could also have divided the 4x^2 term ... but we chose here the
highest power of x", so the quotient is 2x^2 - 6x + 22 and not the 2x^2 - 6x + 4
+ 18 of the long route worked earlier in the same post.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import NOTE, UPLOADS, check, paths_in

P = paths_in("p=12378.html")
DPI = 110
COL_W = 60          # one column per power of x
ROW_H = 52          # matches the ~55px per row the recorded heights grow by
LEFT = 14
FS = 13

# columns are powers x^4 ... x^0
def term(c, p, lead=False):
    """A single cell, e.g. '+6x^3'. Empty string for a column with no term."""
    if c is None:
        return ""
    s = ""
    if not lead:
        s += "+" if c >= 0 else "-"
        c = abs(c)
    body = ""
    if p == 0 or c != 1 or (c == 1 and p == 0):
        body += f"{c:g}"
    if p >= 1:
        body += "x" if p == 1 else f"x^{p}"
    return f"${s}{body}$" if s else f"${body}$"


def row(coeffs, first_col):
    """Cells for a polynomial, placed from column index `first_col`."""
    out = [None] * 5
    for i, c in enumerate(coeffs):
        out[first_col + i] = c
    return out


DIVISOR = r"$x^2+3x-2$"
DIVIDEND = row([2, 0, 0, -6, 0], 0)
PROD1 = row([2, 6, -4], 0)
RES1 = row([-6, 4, -6, 0], 1)
PROD2 = row([-6, -18, 12], 1)
RES2 = row([22, -18, 0], 2)
PROD3 = row([22, 66, -44], 2)
RES3 = row([-84, 44], 3)
QUOT = [None, None, 2, -6, 22]      # 2x^2 above x^2, -6x above x, 22 above 1


def frame(step, dest):
    """Draw the tableau as it stands after the numbered step in the post."""
    show_q = [False, False, True, True, True, True, True, True, True, True]
    # how many of the quotient's three terms are written yet
    nq = {0: 0, 1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3}[step]
    body = []                       # (kind, cells) below the bar
    body.append(("plain", DIVIDEND))
    if step >= 2: body.append(("sub", PROD1))
    if step >= 3: body.append(("plain", RES1))
    if step >= 5: body.append(("sub", PROD2))
    if step >= 6: body.append(("plain", RES2))
    if step >= 8: body.append(("sub", PROD3))
    if step >= 9: body.append(("plain", RES3))

    has_q = nq > 0
    n_rows = len(body) + (1 if has_q else 0)
    W = LEFT + 150 + 5 * COL_W + 20
    H = n_rows * ROW_H + 34
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)

    def put(xpx, ypx, s, ha="center", size=FS, color="black"):
        fig.text(xpx / W, ypx / H, s, fontsize=size, ha=ha, va="center",
                 color=color)

    def line(x0, x1, ypx, lw=1.0):
        fig.add_artist(plt.Line2D([x0 / W, x1 / W], [ypx / H, ypx / H],
                                  color="black", lw=lw))

    col_x = [LEFT + 150 + COL_W * (i + 0.5) for i in range(5)]
    y = H - 18
    if has_q:
        for i in range(5):
            if QUOT[i] is not None and i >= 5 - nq:
                lead = (i == 5 - nq)
                put(col_x[i], y, term(QUOT[i], 4 - i, lead=lead))
        y -= ROW_H

    # the division bracket: divisor, a vertical stroke, and the overbar
    bar_top = y + ROW_H / 2
    put(LEFT, bar_top - ROW_H / 2, DIVISOR, ha="left")
    xv = LEFT + 142
    fig.add_artist(plt.Line2D([xv / W, xv / W],
                              [(bar_top - ROW_H) / H, bar_top / H],
                              color="black", lw=1.0))
    line(xv, LEFT + 150 + 5 * COL_W, bar_top)

    for kind, cells in body:
        first = next(i for i, c in enumerate(cells) if c is not None)
        for i, c in enumerate(cells):
            if c is not None:
                put(col_x[i], y, term(c, 4 - i, lead=(i == first)))
        if kind == "sub":
            put(col_x[first] - COL_W * 0.62, y, r"$-$")
            line(col_x[first] - COL_W * 0.72, LEFT + 150 + 5 * COL_W,
                 y - ROW_H / 2 + 3)
        y -= ROW_H

    fig.text(1 - 6 / W, 4 / H, NOTE, ha="right", va="bottom",
             fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)


print("  p=12378 checks:")
num, den = np.array([2., 0, 0, -6, 0]), np.array([1., 3, -2])
q, r = np.polydiv(num, den)
check("quotient x^2 coefficient", q[0], 2)
check("quotient x coefficient", q[1], -6)
check("quotient constant (post: 22)", q[2], 22)
check("remainder x coefficient (post: -84)", r[0], -84)
check("remainder constant (post: 44)", r[1], 44)
check("division identity holds",
      float(np.abs(np.polysub(np.polyadd(np.polymul(q, den), r), num)).max()), 0.0)

for s in range(10):
    frame(s, P[f"step{s}.png"])
print("  p=12378: 10 figures written")
