#!/usr/bin/env python3
"""p=11619, "MAM1000 part 48, linear algebra part i".

Four lost figures:

  matrices.001  the diagram of "these three methods which we will utilise in
                detail in the coming sections", which the text characterises
                one by one: methods we know well but which are inefficient,
                methods that are graphically intuitive but not calculationally
                useful, and methods that are computationally powerful but
                appear abstract. Drawn as those three with the translations
                between them, which is what the surrounding text promises to
                show. The .001 suffix says the original was a slide export.
  la1           x+y=3 and 2x-y=4 crossing at (7/3, 2/3)
  la2           the same with the solved pair x=7/3 and y=2/3 added, "two new
                lines ... horizontal and vertical, where before we had
                intersecting slanted lines"
  la3           x+y=1 and x+y=-1, parallel, the system with no solution
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=11619.html")
SX, SY = 7 / 3, 2 / 3


def lines(dest, specs, extra=None, title=""):
    fig, ax = plt.subplots(figsize=(5.8, 5.9))
    x = np.linspace(-2, 5, 400)
    for (a, b, c), col, lab in specs:
        if b != 0:
            ax.plot(x, (c - a * x) / b, color=col, lw=2, label=lab)
        else:
            ax.axvline(c / a, color=col, lw=2, label=lab)
    if extra:
        for (a, b, c), col, lab in extra:
            if b == 0:
                ax.axvline(c / a, color=col, lw=2, ls="--", label=lab)
            else:
                ax.axhline(c / b, color=col, lw=2, ls="--", label=lab)
        ax.plot([SX], [SY], "o", color="black", ms=7, zorder=6)
    axes(ax, (-2, 5), (-3, 5), xlabel=None, ylabel=None)
    ax.legend(fontsize=10, frameon=False, loc="upper right")
    if title:
        ax.set_title(title, fontsize=11)
    save(fig, dest)


lines(P["la1.png"],
      [((1, 1, 3), BLUE, "$x+y=3$"), ((2, -1, 4), RED, "$2x-y=4$")],
      title=r"crossing at $\left(\frac{7}{3},\frac{2}{3}\right)$")

lines(P["la2.png"],
      [((1, 1, 3), BLUE, "$x+y=3$"), ((2, -1, 4), RED, "$2x-y=4$")],
      extra=[((1, 0, SX), GREEN, r"$x=\frac{7}{3}$"),
             ((0, 1, SY), GREY, r"$y=\frac{2}{3}$")],
      title="the same solution, as horizontal and vertical lines")

lines(P["la3.png"],
      [((1, 1, 1), BLUE, "$x+y=1$"), ((1, 1, -1), RED, "$x+y=-1$")],
      title="parallel: the system has no solution")

# --- matrices.001: the three formalisms and the translations between them --
BOXES = [(0.5, 0.78, "algebraic\nelimination",
          "familiar, but\ninefficient"),
         (0.21, 0.26, "geometric\npicture", "intuitive, but not\ncalculational"),
         (0.79, 0.26, "matrices", "powerful, but\nlooks abstract")]
fig = plt.figure(figsize=(6.4, 4.8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1); ax.set_ylim(0.10, 1.0); ax.set_axis_off()
for x, y, name, note in BOXES:
    ax.add_patch(FancyBboxPatch((x - 0.155, y - 0.075), 0.31, 0.15,
                                boxstyle="round,pad=0.012",
                                facecolor="#eaf2f8", edgecolor=BLUE, lw=1.6))
    ax.text(x, y + 0.028, name, ha="center", va="center", fontsize=12,
            color="#123", linespacing=1.25)
    ax.text(x, y - 0.045, note, ha="center", va="center", fontsize=8.5,
            color=GREY, linespacing=1.2)
for (x1, y1, *_), (x2, y2, *_) in ((BOXES[0], BOXES[1]), (BOXES[1], BOXES[2]),
                                   (BOXES[0], BOXES[2])):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.4,
                                shrinkA=48, shrinkB=48))
ax.text(0.5, 0.985, "three ways to solve a linear system", ha="center",
        va="top", fontsize=12)
save(fig, P["matrices.001.png"])

# --- the arithmetic the post carries out ---------------------------------
print("  p=11619 checks:")
check("x from the post's elimination (7/3)", SX, 7 / 3)
check("y from the post's elimination (2/3)", SY, 3 - 7 / 3)
check("  ... satisfies x+y=3", SX + SY, 3)
check("  ... and 2x-y=4", 2 * SX - SY, 4)
v = np.array([2.0, 1.0, -1.0])
A = np.array([[1.0, 2, -1], [-1, 3, 1], [2, -1, -2]])
for i, rhs in enumerate([5.0, 0.0, 5.0], start=1):
    check(f"(2,1,-1) satisfies the post's equation {i}", A[i - 1] @ v, rhs)
check("x+y=1 and x+y=-1 are parallel",
      float(np.linalg.det(np.array([[1.0, 1], [1, 1]]))), 0.0)
check("  ... so the system is inconsistent (1 = -1)", 1 == -1, False)
print("  p=11619: 4 figures written")
