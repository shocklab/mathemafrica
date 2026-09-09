#!/usr/bin/env python3
"""p=13659, "Guidelines for visualising and calculating volumes of revolution".

Four lost figures, a sequence building one worked visualisation:

  pl1    the region between two curves, "drawn here in red and blue"
  pl2    the same with the line of rotation, y = -1, drawn in
  pl3    the same with the curves reflected about that line
  pl4-1  the same, sliced, "we will use the disk/annulus/washer method"

The post states that "the equations don't matter for the visualisation, but of
course for the integral itself it would be very important", so the identity of
the curves is deliberately not fixed by the text. The pair used here is
y = x^2 (red, lower) and y = 4 - x^2 (blue, upper), following the red-below,
blue-above convention the archive uses elsewhere (p=10985 captions its
parabolic faces that way). Both sit strictly above y = -1, so the slices are
annuli rather than disks, which is what the post goes on to describe.

Two animations on this post, movie1-1.gif and movie.gif, are also lost and are
not reconstructed: they are animations, and a still would misrepresent them.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREY, FILL, save, axes, check, paths_in

P = paths_in("p=13659.html")

TOP = lambda x: 4 - x ** 2
BOT = lambda x: x ** 2
AXIS = -1.0
XI = np.sqrt(2.0)                      # the curves meet at x = +- sqrt(2)
XR, YR = (-2.6, 2.6), (-6.6, 5.2)


def base(ax, reflect=False):
    x = np.linspace(-XI, XI, 400)
    ax.fill_between(x, BOT(x), TOP(x), color=FILL, alpha=0.6, zorder=2)
    xs = np.linspace(XR[0], XR[1], 500)
    ax.plot(xs, TOP(xs), color=BLUE, lw=2, zorder=3)
    ax.plot(xs, BOT(xs), color=RED, lw=2, zorder=3)
    if reflect:
        ax.fill_between(x, 2 * AXIS - TOP(x), 2 * AXIS - BOT(x),
                        color=FILL, alpha=0.35, zorder=2)
        ax.plot(xs, 2 * AXIS - TOP(xs), color=BLUE, lw=1.4, ls="--", zorder=3)
        ax.plot(xs, 2 * AXIS - BOT(xs), color=RED, lw=1.4, ls="--", zorder=3)
    axes(ax, XR, YR)


def rotation_line(ax):
    ax.axhline(AXIS, color=GREY, lw=1.6, ls="-.", zorder=4)
    ax.text(XR[0] + 0.1, AXIS - 0.62, "$y=-1$", ha="left", fontsize=10,
            color=GREY)


# --- pl1: just the region -------------------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.2))
base(ax)
save(fig, P["pl1.png"])

# --- pl2: with the line of rotation --------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.2))
base(ax)
rotation_line(ax)
save(fig, P["pl2.png"])

# --- pl3: with the region reflected about it -----------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.05))
base(ax, reflect=True)
rotation_line(ax)
save(fig, P["pl3.png"])

# --- pl4-1: sliced, showing one annulus in cross-section -----------------
fig, ax = plt.subplots(figsize=(5.0, 3.05))
base(ax, reflect=True)
rotation_line(ax)
xc, dx = 0.55, 0.16
for sign in (1, -1):
    lo = AXIS + sign * (BOT(xc) - AXIS)
    hi = AXIS + sign * (TOP(xc) - AXIS)
    ax.add_patch(plt.Rectangle((xc - dx / 2, min(lo, hi)), dx, abs(hi - lo),
                               facecolor="#f2b8b8", edgecolor=RED, lw=1.0,
                               zorder=5))
# guide slices run across the region and its mirror, not across the hole
for x0 in np.arange(-XI + 0.10, XI, 0.16):
    for sign in (1, -1):
        lo = AXIS + sign * (BOT(x0) - AXIS)
        hi = AXIS + sign * (TOP(x0) - AXIS)
        ax.plot([x0, x0], [lo, hi], color="#9dc3e0", lw=0.6, zorder=3)
ax.annotate(r"width $\Delta x$", (xc, TOP(xc)), textcoords="offset points",
            xytext=(14, 10), fontsize=9, color=RED)
save(fig, P["pl4-1.png"])

# --- what the text does fix ----------------------------------------------
print("  p=13659 checks:")
check("the curves meet where x^2 = 4-x^2", TOP(XI), BOT(XI))
check("  ... at x = sqrt(2)", XI, np.sqrt(2))
check("the region lies strictly above the line of rotation, so the "
      "slices are annuli not disks",
      bool(np.all(BOT(np.linspace(-XI, XI, 200)) > AXIS)), True)
check("outer radius at x is TOP(x) - (-1)", TOP(0.5) - AXIS, 4 - 0.25 + 1)
check("inner radius at x is BOT(x) - (-1)", BOT(0.5) - AXIS, 0.25 + 1)
print("  p=13659: 4 figures written (movie1-1.gif and movie.gif left missing, "
      "they are animations)")
