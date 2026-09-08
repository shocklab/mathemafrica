#!/usr/bin/env python3
"""p=11169, "Pascal's triangle, fractals and the Sierpinski triangle".

Six lost figures:

  pascal.png   Pascal's triangle, "for the first 9 layers", which the text
               states outright.
  koch2.png    the first Koch replacement, "take each of the sides and cut out
               the middle third of each one, and replace it with two sides of
               another triangle as in". Its recorded aspect, 607x1024 = 0.59,
               is twice a triangle's own 1.15 height-to-width, so the figure is
               two stages stacked: the triangle above, the star below.
  st1..st4     four Sierpinski stages, "removing a quarter of each remaining
               triangle at each iteration".

The surviving animation on this post (ezgif.com-optimize.gif) is the odd/even
Pascal colouring, and the Sierpinski stages are drawn to match it: filled
triangles pointing the same way as the Pascal rows above them.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import comb
from figstyle import BLUE, RED, GREY, FILL, save, check, paths_in

P = paths_in("p=11169.html")
S3 = np.sqrt(3) / 2

# --- pascal.png (360x326): the first nine layers ---------------------------
N = 9
fig, ax = plt.subplots(figsize=(3.9, 3.5))
for n in range(N):
    for k in range(n + 1):
        ax.text(k - n / 2, -n, str(comb(n, k)), ha="center", va="center",
                fontsize=9.5, color=BLUE)
ax.set_xlim(-N / 2 - 0.7, N / 2 + 0.7)
ax.set_ylim(-N + 0.4, 0.9)
ax.set_axis_off()
save(fig, P["pascal.png"])


# --- koch2.png (607x1024): the triangle, then one replacement --------------
def koch(points, n):
    for _ in range(n):
        out = []
        for a, b in zip(points[:-1], points[1:]):
            a, b = np.array(a), np.array(b)
            d = (b - a) / 3.0
            p1, p2 = a + d, a + 2 * d
            ang = np.arctan2(d[1], d[0]) - np.pi / 3
            tip = p1 + np.linalg.norm(d) * np.array([np.cos(ang), np.sin(ang)])
            out += [tuple(a), tuple(p1), tuple(tip), tuple(p2)]
        out.append(points[-1])
        points = out
    return np.array(points)


tri = [(0, 0), (1, 0), (0.5, S3), (0, 0)]
fig, axs = plt.subplots(2, 1, figsize=(4.2, 7.1))
for ax, n in zip(axs, (0, 1)):
    pts = koch(tri, n)
    ax.plot(pts[:, 0], pts[:, 1], color=BLUE, lw=1.8)
    ax.set_aspect("equal")
    ax.set_xlim(-0.32, 1.32); ax.set_ylim(-0.42, 1.15)
    ax.set_axis_off()
    per = 3 * (4 / 3) ** n
    ax.set_title(f"perimeter ${per:g}$" if n else "perimeter $3$", fontsize=10)
save(fig, P["koch2.png"])


# --- st1..st4: successive Sierpinski stages -------------------------------
def sierpinski(depth):
    """Filled sub-triangles left after `depth` removals."""
    tris = [np.array([(0.0, 0.0), (1.0, 0.0), (0.5, S3)])]
    for _ in range(depth):
        nxt = []
        for t in tris:
            a, b, c = t
            ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
            nxt += [np.array([a, ab, ca]), np.array([ab, b, bc]),
                    np.array([ca, bc, c])]
        tris = nxt
    return tris


for i, depth in enumerate((1, 2, 3, 4), start=1):
    # the recorded frames are wide (360x164, and 360x108 for the last), so the
    # triangle sits on a wide canvas rather than filling it
    aspect = 360 / 108 if depth == 4 else 360 / 164
    h = 3.4
    fig, ax = plt.subplots(figsize=(h * aspect / 2.4, h / 2.4 * 1.0))
    for t in sierpinski(depth):
        ax.add_patch(Polygon(t, closed=True, facecolor=BLUE,
                             edgecolor="none"))
    ax.set_aspect("equal")
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, S3 + 0.02)
    ax.set_axis_off()
    ax.set_title(f"{3 ** depth} triangles, area "
                 f"$\\left(\\frac{{3}}{{4}}\\right)^{{{depth}}}$ of the whole",
                 fontsize=9)
    save(fig, P[f"st{i}.png"])

# --- the numbers the post states ------------------------------------------
print("  p=11169 checks:")
check("Koch stage 1 perimeter (post: 3-3(1/3)+6(1/3)=4)",
      3 - 3 * (1 / 3) + 6 * (1 / 3), 4)
check("Koch stage 1 from the formula 3(4/3)^n", 3 * (4 / 3) ** 1, 4)
check("Koch stage 2 (post: 3+3/3+12/9)",
      3 - 3 * (1 / 3) + 6 * (1 / 3) - 12 * (1 / 9) + 24 * (1 / 9),
      3 + 3 / 3 + 12 / 9)
check("Koch stage 3 (post: 3+3/3+12/9+48/27)",
      3 - 3 * (1 / 3) + 6 * (1 / 3) - 12 * (1 / 9) + 24 * (1 / 9)
      - 48 * (1 / 27) + 96 * (1 / 27), 3 + 3 / 3 + 12 / 9 + 48 / 27)
check("Koch area (post: (8/5)(sqrt3/4))", 8 / 5 * np.sqrt(3) / 4,
      2 * np.sqrt(3) / 5)
check("Sierpinski stage 1 leaves 3 triangles", len(sierpinski(1)), 3)
check("Sierpinski stage 4 leaves 81", len(sierpinski(4)), 81)
check("Sierpinski area tends to zero", (3 / 4) ** 30 < 1e-3, True)
check("Pascal row 8 middle entry", comb(8, 4), 70)
print("  p=11169: 6 figures written")
