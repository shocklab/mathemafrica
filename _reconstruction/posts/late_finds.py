#!/usr/bin/env python3
"""Five figures found on a second pass, after the manifest was closed.

The first sweep looked at posts with several lost figures. These are singletons,
which is why they were missed.

p=10311, Aidan Horn on the multiplier effect:
  multiplier1-e1426450380957.png  "Figure 1", the Keynesian cross. The post
      fixes every element of it: the AE function whose y-cut is autonomous
      expenditure and whose gradient is b(1-t); the shift from AE_1 to AE_2 by
      y_1; the staircase, "the income of people in the economy thus increases
      by x_1 until AE=Y", then "AE will rise by y_2", repeating "with smaller
      and smaller increases"; and the total, sum y_n = E_2 - E_1 = y_1*alpha
      with alpha = 1/(1-b(1-t)).

Vectors part ii (2015/09):
  vec1.png  "In the figure below we place the same arrow in several different
      places and they are all the same vector." The post's own page is not in
      the archive, only its excerpt on the September 2015 index, which carries
      that sentence and the image. Its siblings vec6 to vec9 are reconstructed
      already and this matches them.

"Circular base, semi-circular top, triangular cross-section" (2015/08):
  triangcirc2.png  "Remember a single cross-sectional slice looked like:".
      That page is not archived either; the excerpt on the search page carries
      the title, the sentence and the image. The title determines the solid.
      Over a disk of radius r, slices perpendicular to a diameter are isosceles
      triangles standing on a chord of length 2*sqrt(r^2-y^2); their apexes
      trace a semicircle only if the apex height equals half the chord, so the
      cross-section is the isosceles right triangle. Equilateral slices, the
      other common version of this exercise, give a top that is an ellipse of
      height sqrt(3)*r, not a semicircle.

p=14148, Cartesian products:
  download.jpg     "Z^2 = {(m,n): m,n in Z} is the set of all integers in 2D
      space"
  thumbnail_Screen-Shot-2018-04-05-at-10.26.55-PM.png  "Z^3 ... is the set of
      all integers in 3D space"
      Both originals were pictures the author found elsewhere: one is literally
      named download.jpg, the other is a screenshot. What they illustrate is
      the sentence beside them and nothing more, so they are drawn here rather
      than left broken.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from figstyle import (BLUE, RED, GREEN, GREY, MMA, save, axes, check, paths_in,
                      mma_axes)

P11 = paths_in("p=10311.html")
P48 = paths_in("p=14148.html")
PVEC = paths_in("m=201509&paged=2.html")
PTRI = paths_in("s=animation.html")

# --- multiplier1: the Keynesian cross and its staircase -------------------
# b(1-t) is the gradient of AE, alpha the multiplier the post derives.
SLOPE = 0.6                     # b(1-t)
A1 = 20.0                       # autonomous expenditure, the y-cut of AE_1
DY1 = 10.0                      # y_1, the increase in autonomous expenditure
ALPHA = 1 / (1 - SLOPE)
Y1 = A1 / (1 - SLOPE)                   # E_1, where AE_1 = Y
Y2 = (A1 + DY1) / (1 - SLOPE)           # E_2

ae1 = lambda y: A1 + SLOPE * y
ae2 = lambda y: A1 + DY1 + SLOPE * y

# the staircase the post describes, term by term
steps, y_n, cur = [], DY1, Y1
for _ in range(9):
    steps.append((cur, cur, cur + y_n))         # vertical rise y_n onto AE_2
    steps.append((cur, cur + y_n, cur + y_n))   # horizontal x_n = y_n to AE=Y
    cur, y_n = cur + y_n, y_n * SLOPE

fig, ax = plt.subplots(figsize=(6.4, 5.2))
Y = np.linspace(0, 88, 200)
ax.plot(Y, Y, color=GREY, lw=1.2)
ax.plot(Y, ae1(Y), color=BLUE, lw=2)
ax.plot(Y, ae2(Y), color=GREEN, lw=2)
for i in range(0, len(steps), 2):
    xv, y0, y1 = steps[i]
    ax.plot([xv, xv], [y0, y1], color=RED, lw=1.4)
    xa, ya, yb = steps[i + 1]
    ax.plot([xa, ya], [yb, yb], color=RED, lw=1.4)

ax.plot([Y1], [Y1], "o", color="black", ms=5)
ax.plot([Y2], [Y2], "o", color="black", ms=5)
ax.annotate("$E_1$", (Y1, Y1), textcoords="offset points", xytext=(-8, -16),
            fontsize=11)
ax.annotate("$E_2$", (Y2, Y2), textcoords="offset points", xytext=(6, -2),
            fontsize=11)
ax.annotate("AE$_1$", (4, ae1(4)), textcoords="offset points",
            xytext=(2, -14), fontsize=10, color=BLUE)
ax.annotate("AE$_2$", (4, ae2(4)), textcoords="offset points",
            xytext=(2, 5), fontsize=10, color=GREEN)
ax.annotate("AE $=Y$", (26, 26), textcoords="offset points", xytext=(-4, 6),
            fontsize=10, color="#666666", rotation=41)
ax.annotate("$y_1$", (Y1, Y1 + DY1 / 2), textcoords="offset points",
            xytext=(-20, -4), fontsize=10, color=RED)
ax.annotate("$x_1$", (Y1 + DY1 / 2, Y1 + DY1), textcoords="offset points",
            xytext=(-6, 5), fontsize=10, color=RED)
ax.annotate("$y_2$", (Y1 + DY1, Y1 + DY1 + DY1 * SLOPE / 2),
            textcoords="offset points", xytext=(5, -4), fontsize=10, color=RED)
ax.annotate("$x_2$", (Y1 + DY1 + DY1 * SLOPE / 2, Y1 + DY1 + DY1 * SLOPE),
            textcoords="offset points", xytext=(-6, 5), fontsize=10, color=RED)
ax.set_xlim(0, 90); ax.set_ylim(0, 90)
axes(ax, (0, 90), (0, 90), spines="cross")
ax.set_xticks([]); ax.set_yticks([])
ax.text(89, -3.0, "$Y$", fontsize=12, ha="right", va="top")
ax.text(1.5, 89, "AE", fontsize=12, ha="left", va="top")
ax.set_title("the multiplier: $y_1$ raises equilibrium income by "
             r"$y_1\cdot\frac{1}{1-b(1-t)}$", fontsize=10)
save(fig, P11["multiplier1-e1426450380957.png"])

# --- vec1: the same arrow in several places ------------------------------
V = np.array([3.0, 2.0])
BASES = [(0.0, 0.0), (-3.5, 2.5), (1.0, -2.5), (-4.0, -1.0), (3.0, 3.5)]
fig, ax = plt.subplots(figsize=(5.6, 4.2))
for bx, by in BASES:
    ax.annotate("", xy=(bx + V[0], by + V[1]), xytext=(bx, by),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0))
ax.set_xlim(-5.5, 7.0); ax.set_ylim(-3.5, 6.5)
axes(ax, (-5.5, 7.0), (-3.5, 6.5), equal=True)
ax.set_title("the same vector, drawn in five different places", fontsize=10)
save(fig, PVEC["vec1.png"])

# --- triangcirc2: one cross-sectional slice ------------------------------
R, Y0 = 1.0, 0.35
half = np.sqrt(R ** 2 - Y0 ** 2)          # half the chord, and the apex height
fig = plt.figure(figsize=(5.4, 4.6))
ax = mma_axes(fig, elev=22, azim=-62)
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(R * np.cos(th), R * np.sin(th), 0 * th, color=GREY, lw=1.2)
ta = np.linspace(0, np.pi, 120)          # the semicircular ridge
ax.plot(R * np.cos(ta), 0 * ta, R * np.sin(ta), color=GREY, lw=1.0, ls=":")
tri = np.array([[-half, Y0, 0.0], [half, Y0, 0.0], [0.0, Y0, half]])
ax.plot(np.append(tri[:, 0], tri[0, 0]), np.append(tri[:, 1], tri[0, 1]),
        np.append(tri[:, 2], tri[0, 2]), color=RED, lw=2)
ax.add_collection3d(Poly3DCollection([tri], facecolor=MMA[0], alpha=0.55,
                                    edgecolor="none"))
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(0, 1.1)
ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1]); ax.set_zticks([0, 1])
ax.set_title("a single cross-sectional slice", fontsize=11)
save(fig, PTRI["triangcirc2.png"])

# --- the two integer lattices --------------------------------------------
g = np.arange(-3, 4)
X, Yg = np.meshgrid(g, g)
fig, ax = plt.subplots(figsize=(4.6, 4.6))
ax.plot(X.ravel(), Yg.ravel(), "o", color=BLUE, ms=4.5)
axes(ax, (-3.6, 3.6), (-3.6, 3.6), equal=True)
ax.set_title(r"$\mathbb{Z}^2$", fontsize=12)
save(fig, P48["download.jpg"])

g3 = np.arange(-2, 3)
Xa, Ya, Za = np.meshgrid(g3, g3, g3, indexing="ij")
fig = plt.figure(figsize=(4.8, 4.6))
ax = mma_axes(fig, elev=18, azim=-58)
ax.scatter(Xa.ravel(), Ya.ravel(), Za.ravel(), color=BLUE, s=11, depthshade=True)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4); ax.set_zlim(-2.4, 2.4)
ax.set_title(r"$\mathbb{Z}^3$", fontsize=12)
save(fig, P48["thumbnail_Screen-Shot-2018-04-05-at-10.26.55-PM.png"])

# --- what the posts assert ------------------------------------------------
print("  late finds checks:")
check("the multiplier is 1/(1-b(1-t)) (post)", ALPHA, 1 / (1 - SLOPE))
check("  ... which for this figure is 2.5", round(ALPHA, 3), 2.5)
check("y_1 shifts AE vertically, so AE_2(0) - AE_1(0) = y_1 (post)",
      ae2(0) - ae1(0), DY1)
check("x_n = y_n, because AE=Y has gradient 1 (post)",
      [round(steps[i + 1][1] - steps[i + 1][0], 9) for i in (0, 2, 4)],
      [round(steps[i][2] - steps[i][1], 9) for i in (0, 2, 4)])
check("y_{n+1} = y_n b(1-t) (post)",
      round(steps[2][2] - steps[2][1], 9), round(DY1 * SLOPE, 9))
check("sum of y_n = E_2 - E_1 (post)",
      DY1 / (1 - SLOPE), Y2 - Y1)
check("  ... = y_1 * alpha (post)", DY1 * ALPHA, Y2 - Y1)
check("the staircase converges on E_2: after nine terms the gap left is "
      "b(1-t)^9 of the whole rise",
      (Y2 - steps[-1][1]) / (Y2 - Y1), SLOPE ** 9)
check("y_n -> 0 as n -> infinity (post): the ninth term is under 2% of the "
      "first", (steps[-2][2] - steps[-2][1]) / DY1 < 0.02, True)
check("the same arrow in five places is one vector: every copy has the same "
      "components", [tuple(V) for _ in BASES], [(3.0, 2.0)] * 5)
check("the slice's apex height equals half its chord, so apexes lie on "
      "x^2 + z^2 = r^2", round(half ** 2 + Y0 ** 2, 9), R ** 2)
check("  ... an equilateral slice instead would put the apex at "
      "sqrt(3)/2 times the chord, off that circle",
      abs((np.sqrt(3) * half) ** 2 + Y0 ** 2 - R ** 2) > 1e-6, True)
check("Z^2 drawn as all integer pairs in the range", X.size, 7 * 7)
check("Z^3 drawn as all integer triples in the range", Xa.size, 5 ** 3)
print("  late finds: 5 figures written")
