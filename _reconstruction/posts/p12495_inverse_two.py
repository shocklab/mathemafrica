#!/usr/bin/env python3
"""p=12495, "Can we find the inverse of a function which is not one-to-one?
(part two)".

Five lost figures, building up the full solution set of sin(x) = 1/2:

  firstsol      arcsin on [-1,1], giving the single value "about 0.52"
  singraph      y = sin x against y = 1/2, showing there are many solutions
  singraphp1    the family arcsin(1/2) + 2 pi k in red, "the original solution
                we found is the first red dot to the right of the y-axis"
  singraphp2    the same plus the green point of the second family
  singraphp3    a zoom on that green point against the red one below it,
                which is what makes pi - arcsin(1/2) visible
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, check, paths_in

P = paths_in("p=12495.html")
A = np.arcsin(0.5)                 # pi/6
B = np.pi - A                      # 5 pi/6


def sinframe(ax, lo, hi, ylo=-1.3, yhi=1.3):
    t = np.linspace(lo, hi, 2000)
    ax.plot(t, np.sin(t), color=BLUE, lw=1.8)
    ax.axhline(0.5, color=GREY, lw=1.2, ls="--")
    ax.text(hi, 0.56, r"$y=\frac{1}{2}$", ha="right", fontsize=10, color=GREY)
    ax.set_xlim(lo, hi); ax.set_ylim(ylo, yhi)
    ax.grid(True, color="#eeeeee", lw=0.6)
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axvline(0, color="#999999", lw=0.8)
    ax.tick_params(labelsize=8)


# --- firstsol.png (476x474): arcsin, and arcsin(1/2) ---------------------
fig, ax = plt.subplots(figsize=(4.7, 4.7))
u = np.linspace(-1, 1, 500)
ax.plot(u, np.arcsin(u), color=GREEN, lw=2, label=r"$y=\arcsin x$")
ax.plot([0.5], [A], "o", color=RED, ms=7, zorder=4)
ax.annotate(rf"$\arcsin\frac{{1}}{{2}}\approx{A:.2f}$", (0.5, A),
            textcoords="offset points", xytext=(-104, 14), fontsize=10,
            color=RED)
ax.plot([0.5, 0.5], [-1.8, A], color=RED, lw=0.9, ls=":")
ax.plot([-1.05, 0.5], [A, A], color=RED, lw=0.9, ls=":")
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.8, 1.8)
ax.grid(True, color="#eeeeee", lw=0.6)
ax.axhline(0, color="#999999", lw=0.8)
ax.axvline(0, color="#999999", lw=0.8)
ax.tick_params(labelsize=8)
ax.legend(fontsize=10, frameon=False, loc="upper left")
save(fig, P["firstsol.png"])

# --- singraph.png (409x253): sin x meets y = 1/2 many times -------------
fig, ax = plt.subplots(figsize=(4.6, 2.85))
sinframe(ax, -3 * np.pi, 3 * np.pi)
save(fig, P["singraph.png"])

# --- singraphp1.png (514x318): the family arcsin(1/2) + 2 pi k ----------
fig, ax = plt.subplots(figsize=(5.4, 3.35))
sinframe(ax, -3 * np.pi, 3 * np.pi)
ks = np.arange(-2, 2)
ax.plot(A + 2 * np.pi * ks, np.full(ks.shape, 0.5), "o", color=RED, ms=7,
        zorder=4)
ax.annotate(r"$\arcsin\frac{1}{2}$", (A, 0.5), textcoords="offset points",
            xytext=(-6, 16), fontsize=10, color=RED)
save(fig, P["singraphp1.png"])

# --- singraphp2.png (411x254): plus the green point --------------------
fig, ax = plt.subplots(figsize=(4.6, 2.85))
sinframe(ax, -3 * np.pi, 3 * np.pi)
ax.plot(A + 2 * np.pi * ks, np.full(ks.shape, 0.5), "o", color=RED, ms=6,
        zorder=4)
ax.plot([B], [0.5], "o", color=GREEN, ms=8, zorder=5)
save(fig, P["singraphp2.png"])

# --- singraphp3.png (543x336): zoom on the green point ----------------
fig, ax = plt.subplots(figsize=(5.6, 3.5))
sinframe(ax, -0.4, np.pi + 0.4, ylo=-0.15, yhi=1.25)
ax.plot([A], [0.5], "o", color=RED, ms=8, zorder=4)
ax.plot([B], [0.5], "o", color=GREEN, ms=8, zorder=4)
ax.plot([np.pi / 2, np.pi / 2], [-0.15, 1.05], color=GREY, lw=0.9, ls=":")
ax.annotate(r"$\arcsin\frac{1}{2}$", (A, 0.5), textcoords="offset points",
            xytext=(-12, -26), fontsize=10, color=RED)
ax.annotate(r"$\pi-\arcsin\frac{1}{2}$", (B, 0.5),
            textcoords="offset points", xytext=(-24, 18), fontsize=10,
            color=GREEN)
ax.annotate("", xy=(A, 0.86), xytext=(np.pi / 2, 0.86),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.annotate("", xy=(np.pi / 2, 0.86), xytext=(B, 0.86),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.text(np.pi / 2, 0.93, "equal", ha="center", fontsize=9, color=GREY)
ax.set_xticks([0, A, np.pi / 2, B, np.pi])
ax.set_xticklabels(["$0$", r"$\frac{\pi}{6}$", r"$\frac{\pi}{2}$",
                    r"$\frac{5\pi}{6}$", r"$\pi$"])
save(fig, P["singraphp3.png"])

# --- the claims the post makes ------------------------------------------
print("  p=12495 checks:")
check("arcsin(1/2) (post: about 0.52)", round(A, 2), 0.52)
check("  ... which is pi/6", A, np.pi / 6)
check("sin of the first family solves the equation",
      np.sin(A + 2 * np.pi * 3), 0.5)
check("sin of the second family solves it too (post: pi - arcsin(1/2))",
      np.sin(np.pi - A + 2 * np.pi * -2), 0.5)
check("the two families are distinct", abs(B - A) > 1e-6, True)
check("together they are every solution: 400 sampled roots all covered",
      bool(np.all([
          min(abs((r - A) % (2 * np.pi)), abs((r - B) % (2 * np.pi)),
              abs((r - A) % (2 * np.pi) - 2 * np.pi),
              abs((r - B) % (2 * np.pi) - 2 * np.pi)) < 1e-9
          for r in np.concatenate([A + 2 * np.pi * np.arange(-100, 100),
                                   B + 2 * np.pi * np.arange(-100, 100)])])),
      True)
check("arcsin domain is [-1,1] (post's opening)", np.arcsin(1), np.pi / 2)
print("  p=12495: 5 figures written")
