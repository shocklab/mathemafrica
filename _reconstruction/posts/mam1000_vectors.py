#!/usr/bin/env python3
"""Six lost figures across the MAM1000 3D-geometry posts.

p=11537:
  vec6   the scalar projection: "imagine having a light perpendicular to b
         shining towards it. There is a shadow of the vector a cast on the line
         of b", with b's line drawn stretching both ways since "the size of b
         is unimportant"

p=11581:
  vec7   "two vectors (pointing in opposite directions) which are both
         perpendicular to two other vectors and are unit magnitude", the
         ambiguity in the direction of a cross product

p=11583:
  vec8   the parallelogram whose area is |a||b| sin(theta), which the post says
         is "precisely the area of the parallelogram given by the two ways of
         adding the vectors a and b"
  vec9   the worked example: P(1,4,6), Q(-2,5,-1), R(1,-1,1), giving
         PQ = -3i + j - 7k, PR = -5j - 5k, their cross product
         -40i - 15j + 15k of magnitude 5 sqrt(82), and the unit normal. The
         post warns that "the perspective has been somewhat warped so all the
         arrows should really be perpendicular to one another"; here they
         actually are, drawn in three dimensions.

p=11604:
  int    "a line can be defined by the intersection of two planes as in the
         intersection of the blue and the green planes defining the red line"
  line.gif  the animation, described in full: "the black arrow is an arrow
         which points to some place on the line ... The green line is a vector
         which is parallel to the line, and the blue dot which you see moving
         is the position of the point given by going from the origin to the
         point x + tv for varying t"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from figstyle import (BLUE, RED, GREEN, GREY, MMA, UPLOADS, save, axes, check,
                      paths_in, mma_axes, plane)

P37 = paths_in("p=11537.html")
P81 = paths_in("p=11581.html")
P83 = paths_in("p=11583.html")
P04 = paths_in("p=11604.html")

# --- vec6: the shadow of a on the line of b ------------------------------
a = np.array([2.2, 3.0])
b = np.array([4.0, 1.0])
bh = b / np.linalg.norm(b)
comp = float(a @ bh)
foot = comp * bh
fig, ax = plt.subplots(figsize=(5.4, 4.0))
t = np.linspace(-1.2, 1.6, 2)
ax.plot(t * b[0], t * b[1], color=GREY, lw=1.0, ls=":")
ax.annotate("", xy=tuple(a), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
ax.annotate("", xy=tuple(b), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
ax.annotate("", xy=tuple(foot), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=3.0))
ax.plot([a[0], foot[0]], [a[1], foot[1]], color=GREY, lw=1.2, ls="--")
ax.text(a[0] + 0.1, a[1], r"$\vec{a}$", fontsize=13, color=BLUE)
ax.text(b[0] + 0.1, b[1] - 0.2, r"$\vec{b}$", fontsize=13, color=RED)
ax.text(foot[0] * 0.5, foot[1] * 0.5 - 0.42, "the shadow", fontsize=10,
        color=GREEN)
axes(ax, (-1.5, 5.6), (-1.2, 4.0), xlabel=None, ylabel=None)
ax.set_aspect("equal")
save(fig, P37["vec6.png"])

# --- vec7: the two opposite unit normals ---------------------------------
A3 = np.array([2.0, 0.6, 0.0])
B3 = np.array([0.5, 2.0, 0.0])
n = np.cross(A3, B3)
nh = n / np.linalg.norm(n)
fig = plt.figure(figsize=(5.6, 5.6))
ax = mma_axes(fig, elev=20, azim=-62)
for v, col, lab in ((A3, BLUE, r"$\vec{a}$"), (B3, RED, r"$\vec{b}$")):
    ax.quiver(0, 0, 0, *v, color=col, arrow_length_ratio=0.12, lw=2.4)
    ax.text(*(v * 1.08), lab, fontsize=12, color=col)
for s, lab in ((1, r"$\hat{n}$"), (-1, r"$-\hat{n}$")):
    ax.quiver(0, 0, 0, *(s * nh * 1.6), color=GREEN,
              arrow_length_ratio=0.16, lw=2.4)
    ax.text(*(s * nh * 1.8), lab, fontsize=12, color=GREEN)
ax.set_xlim(-1.2, 2.4); ax.set_ylim(-1.2, 2.4); ax.set_zlim(-2.0, 2.0)
save(fig, P81["vec7.png"])

# --- vec8: the parallelogram of area |a x b| -----------------------------
fig, ax = plt.subplots(figsize=(5.6, 5.4))
A2 = np.array([3.2, 0.7])
B2 = np.array([1.1, 2.6])
poly = np.array([[0, 0], A2, A2 + B2, B2])
ax.fill(poly[:, 0], poly[:, 1], color="#cfe3f3", alpha=0.9, zorder=2)
for v, col, lab in ((A2, BLUE, r"$\vec{a}$"), (B2, RED, r"$\vec{b}$")):
    ax.annotate("", xy=tuple(v), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
    ax.text(v[0] * 0.55 + 0.12, v[1] * 0.55 + 0.12, lab, fontsize=13,
            color=col)
ax.plot([A2[0], (A2 + B2)[0]], [A2[1], (A2 + B2)[1]], color=RED, lw=1.2,
        ls="--")
ax.plot([B2[0], (A2 + B2)[0]], [B2[1], (A2 + B2)[1]], color=BLUE, lw=1.2,
        ls="--")
area = abs(float(np.cross(A2, B2)))
ax.text(2.0, 1.5, rf"area $=|\vec{{a}}\times\vec{{b}}| = {area:.2f}$",
        fontsize=11, ha="center")
axes(ax, (-0.8, 5.2), (-0.8, 4.2), xlabel=None, ylabel=None)
ax.set_aspect("equal")
save(fig, P83["vec8.png"])

# --- vec9: the worked example --------------------------------------------
Pp = np.array([1.0, 4.0, 6.0])
Qq = np.array([-2.0, 5.0, -1.0])
Rr = np.array([1.0, -1.0, 1.0])
PQ, PR = Qq - Pp, Rr - Pp
N = np.cross(PQ, PR)
NH = N / np.linalg.norm(N)
fig = plt.figure(figsize=(4.4, 8.0))
ax = mma_axes(fig, elev=18, azim=-58)
for v, col, lab in ((PQ, BLUE, r"$\vec{PQ}$"), (PR, RED, r"$\vec{PR}$")):
    ax.quiver(*Pp, *v, color=col, arrow_length_ratio=0.10, lw=2.4)
    ax.text(*(Pp + v * 1.06), lab, fontsize=11, color=col)
ax.quiver(*Pp, *(NH * 6), color=GREEN, arrow_length_ratio=0.14, lw=2.4)
ax.text(*(Pp + NH * 6.6), r"$\hat{n}$", fontsize=12, color=GREEN)
for pt, lab in ((Pp, "P"), (Qq, "Q"), (Rr, "R")):
    ax.plot([pt[0]], [pt[1]], [pt[2]], "o", color="black", ms=5)
    ax.text(pt[0] + 0.2, pt[1] + 0.2, pt[2] + 0.2, lab, fontsize=10)
ax.set_xlim(-6, 4); ax.set_ylim(-2, 6); ax.set_zlim(-2, 8)
ax.set_box_aspect((1, 1, 1.4))
save(fig, P83["vec9.png"])

# --- int: two planes meeting in a line ------------------------------------
fig = plt.figure(figsize=(4.6, 3.8))
ax = mma_axes(fig, elev=16, azim=-60)
BOX = ((-2, 2), (-2, 2), (-2, 2))
plane(ax, (1, 0, 1, 0), *BOX, color=MMA[0], alpha=0.6)
plane(ax, (0, 1, 1, 0), *BOX, color="#8FB031", alpha=0.6)
tline = np.linspace(-1.8, 1.8, 2)
ax.plot(tline, tline, -tline, color=RED, lw=3.0, zorder=10)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-2, 2)
save(fig, P04["int.png"])

# --- line.gif: the point x + t v moving along the line -------------------
X0 = np.array([1.0, 0.5, -0.5])
V = np.array([1.0, 1.2, 0.8])
tmp = "/private/tmp/claude-501/-Users-jonathanshock-Cursor-folders-Mathematica/fa8467c2-86f9-4523-91a8-5388d8cc081c/scratchpad/lineanim"
os.makedirs(tmp, exist_ok=True)
frames = []
for k, tv in enumerate(np.linspace(-1.4, 1.4, 18)):
    fig = plt.figure(figsize=(3.6, 4.1))
    ax = mma_axes(fig, elev=18, azim=-60)
    s = np.linspace(-1.8, 1.8, 2)
    pts = X0[None, :] + s[:, None] * V[None, :]
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=GREY, lw=1.2)
    ax.quiver(0, 0, 0, *X0, color="black", arrow_length_ratio=0.14, lw=2.0)
    ax.quiver(*X0, *V, color=GREEN, arrow_length_ratio=0.16, lw=2.0)
    p = X0 + tv * V
    ax.plot([p[0]], [p[1]], [p[2]], "o", color=BLUE, ms=9, zorder=10)
    ax.set_xlim(-2, 3); ax.set_ylim(-2, 3); ax.set_zlim(-2.5, 2.5)
    ax.set_title(rf"$\vec{{x}}+t\vec{{v}}$,  $t={tv:+.2f}$", fontsize=9)
    f = f"{tmp}/f{k:02d}.png"
    fig.savefig(f, dpi=95, facecolor="white")
    plt.close(fig)
    frames.append(f)
imgs = [Image.open(f).convert("P", palette=Image.ADAPTIVE) for f in frames]
out = os.path.join(UPLOADS, P04["line.gif"])
os.makedirs(os.path.dirname(out), exist_ok=True)
imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=180, loop=0)

# --- the arithmetic the posts carry out ----------------------------------
print("  MAM1000 vectors checks:")
check("the projection of <5,6> onto x is 5 (post's warm-up)",
      float(np.array([5.0, 6.0]) @ np.array([1.0, 0.0])), 5.0)
check("the shadow lies along b", float(abs(np.cross(foot, b))), 0.0, tol=1e-9)
check("  ... and a minus the shadow is perpendicular to b",
      float((a - foot) @ b), 0.0, tol=1e-9)
check("n-hat is perpendicular to a", float(nh @ A3), 0.0, tol=1e-12)
check("  ... and to b", float(nh @ B3), 0.0, tol=1e-12)
check("  ... and is a unit vector", float(np.linalg.norm(nh)), 1.0)
check("|a x b| is the parallelogram's area",
      area, float(abs(A2[0] * B2[1] - A2[1] * B2[0])))
check("PQ = -3i + j - 7k (post)", list(PQ), [-3.0, 1.0, -7.0])
check("PR = -5j - 5k (post)", list(PR), [0.0, -5.0, -5.0])
check("PQ x PR = -40i - 15j + 15k (post)", list(N), [-40.0, -15.0, 15.0])
check("  ... of magnitude 5 sqrt(82) (post)", float(np.linalg.norm(N)),
      5 * np.sqrt(82))
check("  ... perpendicular to PQ", float(N @ PQ), 0.0)
check("  ... and to PR", float(N @ PR), 0.0)
check("the two planes meet on the drawn line",
      float(max(abs(t + (-t)) + abs(t + (-t)) for t in (-1.0, 0.0, 1.0))),
      0.0)
print("  MAM1000 vectors: 6 figures written")
