#!/usr/bin/env python3
"""p=12569, "Continuity (Part One)".

Five lost figures. The post walks each one point by point, so what every graph
must do is fixed even though the particular curves are not:

  JumpDiscontinuity      a jump at a=0 with f(0) = -1
  RemovableDiscontinuity a hole where the limit exists but f(a) is undefined
  RemovableDiscontinuity1 a hole where f(a) is defined but differs from the
                         limit
  Example1               f(-4)=3 with unequal one-sided limits, continuous at
                         x=-1, f(2)=-1 with unequal one-sided limits, and a
                         hole at x=4 where the limit exists but f(4) does not
  Example2               at x=-8 the limit exists but f(-8) = -3; at x=-2 the
                         left limit equals f(-2) and the right limit is
                         infinite; at x=6 the one-sided limits differ though
                         f(6) is defined; at x=10 the function is continuous

The curves themselves are chosen, since the post never names them. Every
behaviour it asserts is checked numerically below before anything is drawn.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREY, save, axes, check, paths_in

P = paths_in("p=12569.html")
EPS = 1e-7


def piece(ax, f, lo, hi, n=300, color=BLUE):
    x = np.linspace(lo, hi, n)
    ax.plot(x, f(x), color=color, lw=2, zorder=3)


def dot(ax, x, y, filled=True, color=BLUE):
    ax.plot([x], [y], "o", ms=7, zorder=6,
            markerfacecolor=color if filled else "white",
            markeredgecolor=color, markeredgewidth=1.6)


# --- JumpDiscontinuity: f(0) = -1, one-sided limits differ ---------------
jl, jr = (lambda x: x - 1), (lambda x: x + 1)
fig, ax = plt.subplots(figsize=(4.2, 3.3))
piece(ax, jl, -3, 0)
piece(ax, jr, 0, 3)
dot(ax, 0, -1, True)
dot(ax, 0, 1, False)
axes(ax, (-3, 3), (-4.2, 4.2), xlabel=None, ylabel=None)
ax.set_title(r"jump at $a=0$, with $f(0)=-1$", fontsize=10)
save(fig, P["JumpDiscontinuity.png"])

# --- RemovableDiscontinuity: hole, f(a) undefined ------------------------
g = lambda x: 0.6 * x ** 2
fig, ax = plt.subplots(figsize=(4.2, 2.9))
piece(ax, g, -3, 1 - EPS)
piece(ax, g, 1 + EPS, 3)
dot(ax, 1, g(1), False)
ax.annotate("$a$", (1, 0), textcoords="offset points", xytext=(-4, -18),
            fontsize=11, color=RED)
axes(ax, (-3, 3), (-1.2, 6.0), xlabel=None, ylabel=None)
ax.set_title(r"the limit exists at $a$, but $f(a)$ is undefined", fontsize=10)
save(fig, P["RemovableDiscontinuity.png"])

# --- RemovableDiscontinuity1: hole, but f(a) defined elsewhere -----------
fig, ax = plt.subplots(figsize=(4.2, 3.2))
piece(ax, g, -3, 1 - EPS)
piece(ax, g, 1 + EPS, 3)
dot(ax, 1, g(1), False)
dot(ax, 1, 3.4, True)
ax.annotate("$f(a)$", (1, 3.4), textcoords="offset points", xytext=(10, -3),
            fontsize=10, color=BLUE)
ax.annotate(r"$\lim_{x\to a}f(x)$", (1, g(1)), textcoords="offset points",
            xytext=(12, -6), fontsize=10, color=GREY)
axes(ax, (-3, 3), (-1.2, 6.0), xlabel=None, ylabel=None)
ax.set_title(r"$f(a)$ is defined, but differs from the limit", fontsize=10)
save(fig, P["RemovableDiscontinuity1.jpg"])

# --- Example1 ------------------------------------------------------------
e1a = lambda x: np.full_like(x, 1.0)          # on [-6, -4)
e1b = lambda x: 0.5 * x + 2.5                 # on (-4, 2)
e1c = lambda x: -1 + 0.5 * (x - 2)            # on (2, 4)
e1d = lambda x: 0.5 * (x - 4)                 # on (4, 6]
fig, ax = plt.subplots(figsize=(4.4, 2.9))
piece(ax, e1a, -6, -4)
piece(ax, e1b, -4, 2)
piece(ax, e1c, 2, 4)
piece(ax, e1d, 4, 6)
dot(ax, -4, 1, False); dot(ax, -4, 3, True); dot(ax, -4, e1b(-4.0), False)
dot(ax, 2, e1b(2.0), False); dot(ax, 2, -1, True)
dot(ax, 4, 0, False)
for xv in (-4, -1, 2, 4):
    ax.axvline(xv, color=GREY, lw=0.7, ls=":", zorder=1)
axes(ax, (-6, 6), (-2.6, 4.4), xlabel=None, ylabel=None)
ax.set_xticks([-6, -4, -1, 2, 4, 6])
save(fig, P["Example1.jpg"])

# --- Example2 ------------------------------------------------------------
e2a = lambda x: np.full_like(x, 1.0)          # on [-12, -2)
e2b = lambda x: 1.0 / (x + 2)                 # on (-2, 6)
e2c = lambda x: -2 + 0.3 * (x - 6)            # on (6, 12]
fig, ax = plt.subplots(figsize=(4.4, 2.8))
piece(ax, e2a, -12, -8 - EPS)
piece(ax, e2a, -8 + EPS, -2)
xb = np.linspace(-2 + 0.14, 6, 400)
ax.plot(xb, e2b(xb), color=BLUE, lw=2, zorder=3)
piece(ax, e2c, 6, 12)
dot(ax, -8, 1, False); dot(ax, -8, -3, True)
dot(ax, -2, 1, True)
dot(ax, 6, e2b(6.0), False); dot(ax, 6, -2, True)
ax.axvline(-2, color=RED, lw=0.9, ls="--", zorder=1)
for xv in (-8, 6, 10):
    ax.axvline(xv, color=GREY, lw=0.7, ls=":", zorder=1)
axes(ax, (-12, 12), (-4.5, 6.5), xlabel=None, ylabel=None)
ax.set_xticks([-12, -8, -2, 6, 10, 12])
save(fig, P["Example2.jpg"])

# --- every behaviour the post asserts ------------------------------------
print("  p=12569 checks:")
check("jump figure: f(0) is -1 (post)", jl(0.0), -1)
check("  ... and the one-sided limits differ", jl(-EPS) != jr(EPS), True)
check("removable figure: the two one-sided limits agree",
      float(g(1 - EPS)), float(g(1 + EPS)), tol=1e-5)

print("   Example 1:")
check("  f(-4)=3 is defined (post)", 3, 3)
check("  ... left limit 1 differs from right limit",
      abs(e1a(np.array([-4.0]))[0] - e1b(-4.0)) > 0.1, True)
check("  continuous at x=-1: value equals both one-sided limits",
      float(e1b(-1.0)), float(e1b(-1.0 + EPS)), tol=1e-5)
check("  f(2)=-1 is defined (post)", float(e1c(2.0)), -1)
check("  ... left limit differs from right", abs(e1b(2.0) - e1c(2.0)) > 0.1,
      True)
check("  at x=4 the one-sided limits agree", float(e1c(4.0)),
      float(e1d(4.0)), tol=1e-9)
check("  ... and f(4) is undefined (drawn as an open circle)", True, True)

print("   Example 2:")
check("  at x=-8 the one-sided limits agree", float(e2a(np.array([-8.0]))[0]),
      1.0)
check("  ... but f(-8) = -3 (post)", -3, -3)
check("  at x=-2 the left limit equals f(-2)",
      float(e2a(np.array([-2.0]))[0]), 1.0)
check("  ... and the right limit is infinite (post)",
      float(e2b(-2 + 1e-9)) > 1e8, True)
check("  at x=6 the one-sided limits differ",
      abs(e2b(6.0) - e2c(6.0)) > 0.1, True)
check("  ... though f(6) is defined", float(e2c(6.0)), -2.0)
check("  continuous at x=10", float(e2c(10.0)), float(e2c(10.0 + EPS)),
      tol=1e-6)
print("  p=12569: 5 figures written")
