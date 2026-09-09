#!/usr/bin/env python3
"""MAM1000 parts 7 and 8, improper integrals. Three lost figures.

p=10918:
  overx2   the area under 1/x^2 from 1 to 4, which the post evaluates as 3/4

p=10933:
  sqrtxm4  f(x) = 1/sqrt(x-4), "continuous on the interval (4, infinity)"
  comp     "the graphs of e^{-x} in red and e^{-x^2} in blue", the comparison
           the post uses to show that the integral of e^{-x^2} from 1 to
           infinity converges, e^{-x} being "always greater than e^{-x^2}
           between 1 and infinity (but not between 0 and 1 which is why we made
           the split)"

The colours in `comp` are the post's own, so they override the usual convention
here.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREY, FILL, save, axes, check, paths_in

P7 = paths_in("p=10918.html")
P8 = paths_in("p=10933.html")

# --- overx2: the area under 1/x^2 from 1 to 4 ---------------------------
fig, ax = plt.subplots(figsize=(7.0, 5.0))
x = np.linspace(0.55, 5.2, 700)
ax.plot(x, 1 / x ** 2, color=BLUE, lw=2.2)
xf = np.linspace(1, 4, 400)
ax.fill_between(xf, 0, 1 / xf ** 2, color=FILL, alpha=0.7)
for v in (1, 4):
    ax.plot([v, v], [0, 1 / v ** 2], color=GREY, lw=1.0, ls="--")
ax.annotate(r"$\int_1^4\frac{1}{x^2}dx=\frac{3}{4}$", (2.2, 0.30),
            fontsize=13, color=BLUE)
axes(ax, (0.5, 5.2), (-0.25, 3.4), xlabel=None, ylabel=None)
ax.set_title(r"$y=\frac{1}{x^2}$", fontsize=12)
save(fig, P7["overx2.png"])

# --- sqrtxm4: 1/sqrt(x-4) on (4, infinity) ------------------------------
fig, ax = plt.subplots(figsize=(4.4, 3.0))
x = np.linspace(4.02, 14, 700)
ax.plot(x, 1 / np.sqrt(x - 4), color=BLUE, lw=2.2)
ax.axvline(4, color=RED, lw=1.2, ls="--")
ax.annotate("$x=4$", (4, 3.2), textcoords="offset points", xytext=(6, 0),
            fontsize=10, color=RED)
axes(ax, (2, 14), (0, 4.2), spines="box", xlabel="$x$", ylabel=None)
ax.set_title(r"$f(x)=\frac{1}{\sqrt{x-4}}$", fontsize=11)
save(fig, P8["sqrtxm4.png"])

# --- comp: e^{-x} in red against e^{-x^2} in blue ------------------------
fig, ax = plt.subplots(figsize=(4.4, 2.9))
x = np.linspace(0, 3, 600)
ax.plot(x, np.exp(-x), color=RED, lw=2, label=r"$e^{-x}$")
ax.plot(x, np.exp(-x ** 2), color=BLUE, lw=2, label=r"$e^{-x^2}$")
ax.axvline(1, color=GREY, lw=1.0, ls="--")
ax.annotate("$x=1$", (1, 0.92), textcoords="offset points", xytext=(5, 0),
            fontsize=9, color=GREY)
axes(ax, (0, 3), (0, 1.08), spines="box", xlabel="$x$", ylabel=None)
ax.legend(fontsize=10, frameon=False, loc="upper right")
save(fig, P8["comp.png"])

# --- the post's own arithmetic -------------------------------------------
print("  p=10918 / p=10933 checks:")
check("integral of 1/x^2 from 1 to 4 (post: 3/4)",
      quad(lambda t: 1 / t ** 2, 1, 4)[0], 0.75)
check("  ... matching the antiderivative -1/x", (-1 / 4) - (-1 / 1), 0.75)
check("1/sqrt(x-4) is finite everywhere on (4, inf)",
      bool(np.all(np.isfinite(1 / np.sqrt(np.linspace(4.001, 100, 500) - 4)))),
      True)
check("  ... and blows up as x approaches 4 from above",
      1 / np.sqrt(4.000001 - 4) > 900, True)
xs = np.linspace(1.0001, 20, 5000)
check("e^{-x} exceeds e^{-x^2} for x > 1 (post's comparison)",
      bool(np.all(np.exp(-xs) > np.exp(-xs ** 2))), True)
xs2 = np.linspace(0.01, 0.99, 500)
check("  ... but not on (0,1), which is why the post splits the integral",
      bool(np.all(np.exp(-xs2) < np.exp(-xs2 ** 2))), True)
check("the comparison integral converges", quad(lambda t: np.exp(-t), 1,
      np.inf)[0], np.exp(-1))
check("  ... so the integral of e^{-x^2} from 1 to infinity does too",
      quad(lambda t: np.exp(-t ** 2), 1, np.inf)[0]
      < quad(lambda t: np.exp(-t), 1, np.inf)[0], True)
print("  p=10918 / p=10933: 3 figures written")
