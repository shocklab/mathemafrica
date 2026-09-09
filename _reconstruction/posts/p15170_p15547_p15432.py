#!/usr/bin/env python3
"""Three lost figures across three short posts.

p=15170, the Fundamental Theorem of Calculus part iii:
  plftc1proof  the plot behind (g(x+h)-g(x))/h = (1/h) integral from x to x+h,
               "the area between x and x+h divided by h"

p=15547 (partitions) and p=15432 (equivalence classes) share one figure at the
same size, the congruence classes mod 4 on the natural numbers:
  Modulus-4 / Modulus-4-1   "we can imagine taking the set of Natural Numbers
               and divided it into four sets: I put in some of the numbers to
               expect in each congruence class. Note, however, that in reality
               these sets are infinite."
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from figstyle import BLUE, RED, GREY, FILL, save, axes, check, paths_in

P70 = paths_in("p=15170.html")
P47 = paths_in("p=15547.html")
P32 = paths_in("p=15432.html")

# --- plftc1proof: the strip between x and x+h ---------------------------
f = lambda t: 1.2 + 0.55 * np.sin(1.1 * t) + 0.18 * t
A, X, H = 0.3, 3.1, 0.9
fig, ax = plt.subplots(figsize=(4.6, 2.9))
t = np.linspace(0, 6, 600)
ax.plot(t, f(t), color=BLUE, lw=2, zorder=4)
ta = np.linspace(A, X, 300)
ax.fill_between(ta, 0, f(ta), color=FILL, alpha=0.45)
tb = np.linspace(X, X + H, 200)
ax.fill_between(tb, 0, f(tb), color=RED, alpha=0.35)
for v, lab in ((A, "$a$"), (X, "$x$"), (X + H, "$x+h$")):
    ax.plot([v, v], [0, f(v)], color=GREY, lw=1.0, ls="--")
    ax.annotate(lab, (v, 0), textcoords="offset points", xytext=(-6, -18),
                fontsize=10)
ax.annotate(r"$g(x)$", (1.6, 0.55), fontsize=11, color="#2a6496")
ax.annotate(r"$\int_x^{x+h}f$", (X + H / 2, f(X) + 0.35),
            textcoords="offset points", xytext=(-6, 8), fontsize=10,
            color=RED)
axes(ax, (0, 6), (0, 3.2), spines="box", xlabel="$t$", ylabel=None)
save(fig, P70["plftc1proof.png"])

# --- Modulus-4: the four congruence classes ------------------------------
CLASSES = [(0, [0, 4, 8, 12, 16]), (1, [1, 5, 9, 13, 17]),
           (2, [2, 6, 10, 14, 18]), (3, [3, 7, 11, 15, 19])]
fig, ax = plt.subplots(figsize=(4.2, 4.1))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
for i, (r, members) in enumerate(CLASSES):
    y = 0.86 - i * 0.22
    ax.add_patch(FancyBboxPatch((0.06, y - 0.075), 0.88, 0.15,
                                boxstyle="round,pad=0.012",
                                facecolor="#eaf2f8", edgecolor=BLUE, lw=1.4))
    ax.text(0.11, y, f"$[{r}]$", fontsize=12, va="center", color=BLUE)
    ax.text(0.26, y, r"$\{$" + ", ".join(str(m) for m in members)
            + r", \ldots$\}$", fontsize=10, va="center")
ax.text(0.5, 0.975, r"$\mathbb{N}$ under $\equiv\ \mathrm{mod}\ 4$", ha="center",
        va="top", fontsize=11)
out = save(fig, P47["Modulus-4.png"])
import shutil
alt = os.path.join(os.path.dirname(os.path.dirname(out)),
                   *P32["Modulus-4-1.png"].split("/")[-2:])
os.makedirs(os.path.dirname(alt), exist_ok=True)
shutil.copyfile(out, alt)

# --- what the posts assert ------------------------------------------------
print("  p=15170 / p=15547 / p=15432 checks:")
g = lambda u: quad(f, A, u)[0]
check("g(x+h) - g(x) equals the integral from x to x+h (post)",
      g(X + H) - g(X), quad(f, X, X + H)[0], tol=1e-9)
check("  ... and dividing by h gives the average height",
      (g(X + H) - g(X)) / H, quad(f, X, X + H)[0] / H, tol=1e-9)
check("  ... which tends to f(x) as h shrinks (the theorem)",
      (g(X + 1e-6) - g(X)) / 1e-6, float(f(X)), tol=1e-5)
allm = [m for _, ms in CLASSES for m in ms]
check("every listed member is in its own class",
      all(m % 4 == r for r, ms in CLASSES for m in ms), True)
check("the four classes are disjoint", len(set(allm)), len(allm))
check("  ... and there are exactly 4 of them (post)", len(CLASSES), 4)
check("their union covers every natural number below 20",
      sorted(allm), list(range(20)))
print("  p=15170 / p=15547 / p=15432: 3 figures written")
