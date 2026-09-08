#!/usr/bin/env python3
"""p=14953, "All you've ever wanted to know about absolute values".

Eleven lost figures: eight typeset piecewise definitions, two graphs, one
number line. Every expression and every region below is stated verbatim in the
post; the ordering of the rows follows the order the post then discusses them
in ("Looking at the first one we have x^2-2x-3<0", and so on).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, cases, save, axes, check

D = "2019/02/"
half3 = r"\frac{3}{2}"

# --- 1. definition of |x| -------------------------------------------------
cases(r"|x|",
      [(r"x", r"x \ge 0"),
       (r"-x", r"x < 0")],
      D + "Screenshot-2019-02-22-11.32.47.png")

# --- 3. |2x-3|, conditions still on the inside ----------------------------
cases(r"|2x-3|",
      [(r"2x-3", r"2x-3 \ge 0"),
       (r"-(2x-3)", r"2x-3 < 0")],
      D + "Screenshot-2019-02-22-11.36.53.png")

# --- 4. the same, conditions solved for x ---------------------------------
cases(r"|2x-3|",
      [(r"2x-3", r"x \ge " + half3),
       (r"-(2x-3)", r"x < " + half3)],
      D + "Screenshot-2019-02-22-11.37.23.png")

# --- 6. f(x)=|2x-3|-|x-2| in three pieces, unsimplified --------------------
cases(r"f(x)",
      [(r"-(2x-3)+(x-2)", r"x < " + half3),
       (r"(2x-3)+(x-2)", half3 + r" \le x < 2"),
       (r"(2x-3)-(x-2)", r"x \ge 2")],
      D + "Screenshot-2019-02-22-12.53.30.png")

# --- 7. simplified ---------------------------------------------------------
cases(r"f(x)",
      [(r"-x+1", r"x < " + half3),
       (r"3x-5", half3 + r" \le x < 2"),
       (r"x-1", r"x \ge 2")],
      D + "Screenshot-2019-02-22-13.00.25.png")

# --- 8. f(x)=|x^2-2x-3|-1, conditions on the quadratic --------------------
cases(r"f(x)",
      [(r"-(x^2-2x-3)-1", r"x^2-2x-3 < 0"),
       (r"(x^2-2x-3)-1", r"x^2-2x-3 \ge 0")],
      D + "Screenshot-2019-02-22-15.06.59.png")

# --- 9. the same, regions resolved into intervals -------------------------
cases(r"f(x)",
      [(r"-(x^2-2x-3)-1", r"x \in (-1,3)"),
       (r"(x^2-2x-3)-1", r"x \in (-\infty,-1]\cup[3,\infty)")],
      D + "Screenshot-2019-02-22-15.15.02.png")

# --- 10. simplified --------------------------------------------------------
cases(r"f(x)",
      [(r"-x^2+2x+2", r"x \in (-1,3)"),
       (r"x^2-2x-4", r"x \in (-\infty,-1]\cup[3,\infty)")],
      D + "Screenshot-2019-02-22-15.16.04.png")

# --- 2. graph of |x| (shown 546x369) --------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.4))
x = np.linspace(-5, 5, 601)
ax.plot(x, np.abs(x), color=BLUE, lw=2)
axes(ax, (-5, 5), (-0.6, 5.2), spines="cross", ylabel="y")
ax.set_title(r"$f(x)=|x|$")
save(fig, D + "Screenshot-2019-02-22-11.35.21.png")

# --- 5. graph of |2x-3| (shown 396x408, and the text later reads y>4 off it)
fig, ax = plt.subplots(figsize=(4.2, 4.3))
x = np.linspace(-2, 5.5, 751)
ax.plot(x, np.abs(2 * x - 3), color=BLUE, lw=2)
ax.plot([1.5], [0], "o", color=RED, ms=5, zorder=4)
ax.annotate(r"$x=\frac{3}{2}$", (1.5, 0), textcoords="offset points",
            xytext=(8, 10), fontsize=11, color=RED)
axes(ax, (-2, 5.5), (-0.8, 8.2), spines="cross", ylabel="y")
ax.set_title(r"$f(x)=|2x-3|$")
save(fig, D + "Screenshot-2019-02-22-11.41.00.png")

# --- 11. number line for (-1,3) intersect ((-inf,1-sqrt3) U (1+sqrt3,inf))
a, b = 1 - np.sqrt(3), 1 + np.sqrt(3)
fig, ax = plt.subplots(figsize=(6.0, 2.6))
ax.set_xlim(-2.4, 4.4)
ax.set_ylim(-0.75, 3.15)

# the number line itself, along the bottom
ax.plot([-2.3, 4.3], [0, 0], color="#666666", lw=1.0)
for t in (-2, -1, 0, 1, 2, 3, 4):
    ax.plot([t, t], [-0.08, 0.08], color="#666666", lw=1.0)
    ax.text(t, -0.20, str(t), ha="center", va="top", fontsize=9)

for v, lab in ((a, r"$1-\sqrt{3}$"), (b, r"$1+\sqrt{3}$")):
    ax.plot([v, v], [0, 2.75], color=GREY, lw=0.8, ls=":", zorder=1)
    ax.text(v, 2.98, lab, ha="center", va="center", fontsize=9, color=GREY)

def band(y, segs, color, label):
    for lo, hi in segs:
        ax.plot([lo, hi], [y, y], color=color, lw=5,
                solid_capstyle="butt", zorder=3)
    ax.text(-2.3, y + 0.26, label, fontsize=9, color=color, va="center")

band(0.62, [(-1, 3)], BLUE, r"$(-1,3)$")
band(1.42, [(-2.3, a), (b, 4.3)], RED,
     r"$(-\infty,1-\sqrt{3})\,\cup\,(1+\sqrt{3},\infty)$")
band(2.22, [(-1, a), (b, 3)], GREEN,
     r"overlap: $(-1,1-\sqrt{3})\,\cup\,(1+\sqrt{3},3)$")
ax.set_axis_off()
save(fig, D + "Screenshot-2019-02-22-15.49.02.png")

# --- verification against the post's own arithmetic ------------------------
print("  p=14953 checks:")
f2 = lambda x: abs(2 * x - 3) - abs(x - 2)
check("f(1) via -x+1 branch", f2(1.0), -1.0 + 1)
check("f(1.75) via 3x-5 branch", f2(1.75), 3 * 1.75 - 5)
check("f(3) via x-1 branch", f2(3.0), 3.0 - 1)
g = lambda x: abs(x ** 2 - 2 * x - 3) - 1
check("g(0) via -x^2+2x+2 branch", g(0.0), 2.0)
check("g(4) via x^2-2x-4 branch", g(4.0), 4.0)
check("roots of -x^2+2x+2 (post: 1+-sqrt3)", 1 + np.sqrt(3),
      float(np.roots([-1, 2, 2]).max()), tol=1e-12)
check("roots of x^2-2x-4 (post: 1+-sqrt5)", 1 + np.sqrt(5),
      float(np.roots([1, -2, -4]).max()), tol=1e-12)
print("  p=14953: 11 figures written")
