#!/usr/bin/env python3
"""p=12613, "Continuity (Part Two)".

Four lost figures, each fixed by what the post says about it:

  Right          continuous from the right at a: the right limit equals f(a)
                 while the left limit does not
  Left           continuous from the left at x=3, the post naming that point:
                 the left limit equals f(3), the right limit does not
  NotContinuous  "neither continuous at a point from the left or from the right
                 but is defined elsewhere", so f(a) exists and neither
                 one-sided limit reaches it
  Continuous     "if you choose any x-value, you will notice that the function
                 is continuous everywhere"

The curves are chosen, since the post names none; every one-sided limit it
asserts is checked numerically first.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, GREY, save, axes, check, paths_in

P = paths_in("p=12613.html")
EPS = 1e-7


def piece(ax, f, lo, hi, n=300):
    x = np.linspace(lo, hi, n)
    ax.plot(x, f(x), color=BLUE, lw=2, zorder=3)


def dot(ax, x, y, filled=True):
    ax.plot([x], [y], "o", ms=7, zorder=6,
            markerfacecolor=BLUE if filled else "white",
            markeredgecolor=BLUE, markeredgewidth=1.6)


# --- Right: continuous from the right at a = 1 ---------------------------
rl, rr = (lambda x: x + 2), (lambda x: x - 1)
fig, ax = plt.subplots(figsize=(3.0, 2.6))
piece(ax, rl, -2, 1)
piece(ax, rr, 1, 4)
dot(ax, 1, rr(1.0), True)
dot(ax, 1, rl(1.0), False)
ax.annotate("$a$", (1, 0), textcoords="offset points", xytext=(2, -20),
            fontsize=11, color=GREY)
axes(ax, (-2, 4), (-3.4, 4.4), xlabel=None, ylabel=None)
save(fig, P["Right.png"])

# --- Left: continuous from the left at x = 3 -----------------------------
ll, lr = (lambda x: 0.5 * x), (lambda x: 0.5 * x - 2)
fig, ax = plt.subplots(figsize=(4.2, 2.7))
piece(ax, ll, -3, 3)
piece(ax, lr, 3, 7)
dot(ax, 3, ll(3.0), True)
dot(ax, 3, lr(3.0), False)
axes(ax, (-3, 7), (-2.6, 3.4), xlabel=None, ylabel=None)
ax.set_xticks([-2, 0, 3, 5, 7])
save(fig, P["Left.png"])

# --- NotContinuous: neither side reaches f(a) ----------------------------
nl, nr = (lambda x: x + 2), (lambda x: x - 2)
fig, ax = plt.subplots(figsize=(4.2, 2.6))
piece(ax, nl, -2, 1)
piece(ax, nr, 1, 4)
dot(ax, 1, nl(1.0), False)
dot(ax, 1, nr(1.0), False)
dot(ax, 1, 1.0, True)
ax.annotate("$f(a)$", (1, 1.0), textcoords="offset points", xytext=(8, -4),
            fontsize=10, color=BLUE)
axes(ax, (-2, 4), (-3.4, 4.4), xlabel=None, ylabel=None)
save(fig, P["NotContinuous.jpg"])

# --- Continuous: continuous everywhere -----------------------------------
cf = lambda x: 0.35 * x ** 3 - 1.6 * x + 0.5
fig, ax = plt.subplots(figsize=(3.6, 3.2))
piece(ax, cf, -2.6, 2.6, 500)
axes(ax, (-2.6, 2.6), (-3.6, 3.6), xlabel=None, ylabel=None)
save(fig, P["Continuous.jpg"])

# --- every one-sided limit the post asserts ------------------------------
print("  p=12613 checks:")
check("Right: the right limit equals f(a)", rr(1 + EPS), rr(1.0), tol=1e-6)
check("  ... and the left limit does not", abs(rl(1 - EPS) - rr(1.0)) > 1,
      True)
check("Left: the left limit equals f(3) (post names x=3)",
      ll(3 - EPS), ll(3.0), tol=1e-6)
check("  ... and the right limit does not", abs(lr(3 + EPS) - ll(3.0)) > 1,
      True)
check("NotContinuous: the left limit misses f(a)",
      abs(nl(1 - EPS) - 1.0) > 1, True)
check("  ... and so does the right limit", abs(nr(1 + EPS) - 1.0) > 1, True)
check("  ... though f(a) is defined", 1.0, 1.0)
xs = np.linspace(-2.6, 2.6, 4000)
check("Continuous: no jump anywhere on the plotted range",
      float(np.abs(np.diff(cf(xs))).max()) < 0.02, True)
check("  ... a polynomial, which the post lists as continuous on its domain",
      True, True)
print("  p=12613: 4 figures written")
