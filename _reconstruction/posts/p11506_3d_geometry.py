#!/usr/bin/env python3
"""p=11506, "MAM1000 part 38, 3D geometry and vectors part i".

Four lost figures:

  3dp1  "A point P(3,4,2) and its distances from the various coordinate
        planes", with the box it defines against the origin and the
        projections the text names: Q(3,4,0), R(3,0,2), S(0,4,2)
  3dp2  "The function z=3 plotted in three dimensions"
  3dp3  "The function x^2+y^2=1 plotted in three dimensions", a cylinder. Its
        recorded shape, 328x891, is a tall narrow frame, which is what a
        cylinder unconstrained in z wants
  3dp4  the distance from the origin to P(3,4,2) "by using Pythagoras with the
        red, green and blue lines", the caption giving
        distance^2 = (sqrt(3^2+4^2))^2 + 2^2

Colours in 3dp4 follow the caption's order of use: green for the leg in the
xy-plane, blue for the rise to P, red for the distance itself.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import (BLUE, RED, GREEN, GREY, FILL, MMA, save, check,
                      paths_in, mma_axes, plane)

P = paths_in("p=11506.html")
PT = np.array([3.0, 4.0, 2.0])


def frame(ax, lim=((0, 5), (0, 5), (0, 4))):
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_zlim(*lim[2])
    ax.set_box_aspect((lim[0][1] - lim[0][0], lim[1][1] - lim[1][0],
                       lim[2][1] - lim[2][0]))


# --- 3dp1: the point, its box and its projections ------------------------
a, b, c = PT
fig = plt.figure(figsize=(5.6, 5.2))
ax = mma_axes(fig, elev=18, azim=-58)
for s, e in [((0, 0, 0), (a, 0, 0)), ((0, 0, 0), (0, b, 0)),
             ((0, 0, 0), (0, 0, c)), ((a, 0, 0), (a, b, 0)),
             ((0, b, 0), (a, b, 0)), ((a, b, 0), (a, b, c)),
             ((0, 0, c), (a, 0, c)), ((0, 0, c), (0, b, c)),
             ((a, 0, c), (a, b, c)), ((0, b, c), (a, b, c)),
             ((a, 0, 0), (a, 0, c)), ((0, b, 0), (0, b, c))]:
    ax.plot(*zip(s, e), color=GREY, lw=0.9, ls="--")
for pt, name, col in [(PT, "$P(3,4,2)$", RED),
                      ((a, b, 0), "$Q(3,4,0)$", MMA[0]),
                      ((a, 0, c), "$R(3,0,2)$", MMA[1]),
                      ((0, b, c), "$S(0,4,2)$", MMA[2])]:
    ax.plot([pt[0]], [pt[1]], [pt[2]], "o", color=col, ms=7, zorder=8)
    ax.text(pt[0] + 0.15, pt[1] + 0.15, pt[2] + 0.15, name, fontsize=9,
            color=col)
frame(ax)
save(fig, P["3dp1.png"])

# --- 3dp2: the plane z = 3 ----------------------------------------------
fig = plt.figure(figsize=(5.6, 2.6))
ax = mma_axes(fig, elev=14, azim=-60)
plane(ax, (0, 0, 1, 3), (-3, 3), (-3, 3), (0, 5), color=MMA[0], alpha=0.75)
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(0, 5)
ax.set_box_aspect((6, 6, 5))
ax.set_title("$z=3$", fontsize=11)
save(fig, P["3dp2.png"])

# --- 3dp3: the cylinder x^2 + y^2 = 1 -----------------------------------
fig = plt.figure(figsize=(3.2, 8.0))
ax = mma_axes(fig, elev=12, azim=-60)
th = np.linspace(0, 2 * np.pi, 90)
TH, ZZ = np.meshgrid(th, np.linspace(-4, 4, 40))
ax.plot_surface(np.cos(TH), np.sin(TH), ZZ, color=MMA[0], alpha=0.75,
                linewidth=0.3, edgecolor="#3a3a3a", shade=False)
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_zlim(-4, 4)
ax.set_box_aspect((1, 1, 3.2))
ax.set_title("$x^2+y^2=1$", fontsize=11)
save(fig, P["3dp3.png"])

# --- 3dp4: Pythagoras in three dimensions -------------------------------
leg = np.hypot(a, b)
dist = np.linalg.norm(PT)
fig = plt.figure(figsize=(6.0, 5.5))
ax = mma_axes(fig, elev=18, azim=-58)
ax.plot([0, a], [0, b], [0, 0], color=GREEN, lw=2.4, zorder=6)
ax.plot([a, a], [b, b], [0, c], color=BLUE, lw=2.4, zorder=6)
ax.plot([0, a], [0, b], [0, c], color=RED, lw=2.4, zorder=7)
ax.plot([0, a], [0, 0], [0, 0], color=GREY, lw=1.0, ls="--")
ax.plot([a, a], [0, b], [0, 0], color=GREY, lw=1.0, ls="--")
ax.plot([a], [b], [c], "o", color=RED, ms=7, zorder=8)
ax.text(a + 0.15, b + 0.15, c + 0.15, "$P(3,4,2)$", fontsize=10, color=RED)
ax.text(a / 2, b / 2 - 0.7, 0, rf"$\sqrt{{3^2+4^2}}={leg:g}$", fontsize=9,
        color=GREEN)
ax.text(a + 0.2, b + 0.2, c / 2, "$2$", fontsize=10, color=BLUE)
ax.text(a / 2 - 0.9, b / 2, c / 2 + 0.5, rf"$\sqrt{{29}}$", fontsize=10,
        color=RED)
frame(ax)
save(fig, P["3dp4.png"])

# --- the arithmetic the post carries out --------------------------------
print("  p=11506 checks:")
check("number of planes in 3d is 3C2", 3 * 2 // 2, 3)
check("  ... 6 in four dimensions", 4 * 3 // 2, 6)
check("  ... 55 in eleven", 11 * 10 // 2, 55)
check("octants in 3d (post: 8)", 2 ** 3, 8)
check("projection of P onto the xy-plane has z=0 (post's Q)", 0.0, 0.0)
check("xy-projection gradient g1 (post: 3)", (4 - 7) / (2 - 3), 3)
check("xy-projection gradient g2 (post: 1)", (3 - 4) / (1 - 2), 1)
check("  ... so the three points are not collinear",
      (4 - 7) / (2 - 3) != (3 - 4) / (1 - 2), True)
check("leg in the xy-plane (post: sqrt(3^2+4^2))", leg, 5.0)
check("distance to P (post: sqrt(leg^2 + 2^2))", dist, np.sqrt(leg ** 2 + 4))
check("  ... which is sqrt(29)", dist, np.sqrt(29))
print("  p=11506: 4 figures written")
