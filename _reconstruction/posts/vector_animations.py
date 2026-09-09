#!/usr/bin/env python3
"""Three lost animations: two 3D vector figures and one conformal map.

p=11592, "3D geometry and vectors part vii":

  try.gif    "Below is a plot of three points on a line. The points are
             P(2, 4, 0), Q(3, 3, 2) and R(4, 2, 4). We can form vectors between
             them", which the post then uses to show PQ x PR = 0. A single
             viewpoint cannot show that three points in space are collinear,
             which is why the original turns; this one turns too.
  try21.gif  "Let's take three vectors, and put them all at the origin. We can
             form a parallelpiped (like a skewed box) with these three vectors
             ... The red vector is a = <6,0,0>, the green is b = <0,6,2> and
             the blue is c = <2,1,5>. The box is formed by using the three
             vectors end to end in the appropriate sequences."

p=11387, "complex numbers part vii":

  l2.gif     "this is the mapping of lines in the complex plane under the
             Cosine function". Its sibling l1.gif survives on p=11369, for the
             exponential, and fixes the whole design: a grid of horizontal
             lines in green and vertical lines in red and black, bending
             continuously into their images, on Mathematica axes crossing at
             the origin. That post says what the in-between frames are for:
             "What happens in the middle isn't too important, but it allows you
             to track what's happening to each point in the complex plane as
             you exponentiate it." So the frames here interpolate too,
             (1-t)z + t cos(z).

             One difference from the exponential is worth knowing before you
             look at it. cos(-x + iy) is the conjugate of cos(x + iy), so the
             lines at x and -x land on the two halves of one hyperbola: the red
             and the black families, distinct all through the animation, come
             down on the same curves at the end.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, animate, axes, check, paths_in

P92 = paths_in("p=11592.html")
P87 = paths_in("p=11387.html")

# --- try.gif: three collinear points, turning ----------------------------
Pp, Q, R = np.array([2, 4, 0]), np.array([3, 3, 2]), np.array([4, 2, 4])
PQ, PR = Q - Pp, R - Pp
FRAMES = 36


def arrow3(ax, tail, head, color, lw=2.0):
    ax.quiver(*tail, *(np.array(head) - np.array(tail)), color=color, lw=lw,
              arrow_length_ratio=0.12)


def draw_points(ax, i):
    ax.view_init(elev=18, azim=-70 + 360 * i / FRAMES)
    t = np.linspace(-0.4, 1.4, 2)
    line = Pp[None, :] + t[:, None] * PR[None, :]
    ax.plot(line[:, 0], line[:, 1], line[:, 2], color=GREY, lw=1.0, ls=":")
    # PQ lies along PR, so one arrow sits exactly on top of the other. The
    # shorter one is drawn solid and the longer one dashed over it, which is
    # the only way both stay visible without moving either off the line.
    arrow3(ax, Pp, Q, RED, lw=3.0)
    ax.plot(*zip(Pp, R), color=BLUE, lw=1.6, ls=(0, (5, 4)), zorder=6)
    arrow3(ax, Pp + 0.94 * PR, R, BLUE, lw=1.6)
    for name, p in (("P", Pp), ("Q", Q), ("R", R)):
        ax.scatter(*p, color="black", s=22)
        ax.text(*(p + np.array([0.12, 0.12, 0.25])), name, fontsize=11)
    ax.set_xlim(1.4, 4.6); ax.set_ylim(1.4, 4.6); ax.set_zlim(-0.6, 4.6)
    ax.set_title(r"$\vec{PQ}=\langle 1,-1,2\rangle$ and "
                 r"$\vec{PR}=\langle 2,-2,4\rangle$", fontsize=9)


animate(draw_points, FRAMES, P92["try.gif"], figsize=(3.6, 3.6), ms=110,
        three_d=True, elev=18, azim=-70)

# --- try21.gif: the parallelepiped, turning ------------------------------
a = np.array([6, 0, 0]); b = np.array([0, 6, 2]); c = np.array([2, 1, 5])
CORNERS = [np.zeros(3), a, b, c, a + b, a + c, b + c, a + b + c]
EDGES = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 4), (2, 6), (3, 5),
         (3, 6), (4, 7), (5, 7), (6, 7)]


def draw_box(ax, i):
    ax.view_init(elev=20, azim=-64 + 360 * i / FRAMES)
    for u, v in EDGES:
        p0, p1 = CORNERS[u], CORNERS[v]
        ax.plot(*zip(p0, p1), color="#8fa6bd", lw=1.0)
    for vec, col, lab in ((a, RED, "a"), (b, GREEN, "b"), (c, BLUE, "c")):
        arrow3(ax, np.zeros(3), vec, col, lw=2.6)
        ax.text(*(vec * 1.06), f"${lab}$", fontsize=12, color=col)
    ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.set_zlim(0, 8)
    ax.set_title(r"the parallelepiped on $\vec a$, $\vec b$, $\vec c$",
                 fontsize=9)


animate(draw_box, FRAMES, P92["try21.gif"], figsize=(3.56, 4.32), ms=110,
        three_d=True, elev=20, azim=-64)

# --- l2.gif: a grid of lines mapped under the cosine ---------------------
# The grid is kept close to the real axis: cosh y and sinh y converge as |y|
# grows, so far-out lines map to near-circles and the confocal structure the
# picture is for stops being visible.
XS = np.arange(-1.0, 1.001, 0.125) * np.pi     # vertical lines, x constant
YS = np.arange(-1.8, 1.81, 0.3)                # horizontal lines, y constant
STEPS = 29
LIM = 3.6


def draw_map(ax, i):
    t = i / (STEPS - 1)
    for y0 in YS:                                # horizontals, green
        z = np.linspace(-np.pi, np.pi, 500) + 1j * y0
        w = (1 - t) * z + t * np.cos(z)
        ax.plot(w.real, w.imag, color="#1a7a1a", lw=1.1)
    for k, x0 in enumerate(XS):                  # verticals, red and black
        z = x0 + 1j * np.linspace(-1.8, 1.8, 500)
        w = (1 - t) * z + t * np.cos(z)
        ax.plot(w.real, w.imag, color=("#b00000" if x0 >= 0 else "#202020"),
                lw=1.1)
    axes(ax, (-LIM, LIM), (-LIM, LIM), equal=True)
    ax.set_xticks([-3, -1, 0, 1, 3]); ax.set_yticks([-3, -1, 0, 1, 3])


animate(draw_map, STEPS, P87["l2.gif"], figsize=(3.6, 3.6), ms=130)

# --- what the posts assert ------------------------------------------------
print("  vector and mapping animation checks:")
check("PQ = <1,-1,2> (post)", list(PQ), [1, -1, 2])
check("PR = <2,-2,4> (post)", list(PR), [2, -2, 4])
check("their cross product vanishes, so P, Q and R are collinear (post)",
      list(np.cross(PQ, PR)), [0, 0, 0])
check("  ... and the drawn line passes through all three",
      [bool(np.allclose(np.cross(p - Pp, PR), 0)) for p in (Pp, Q, R)],
      [True, True, True])
vol = abs(float(np.dot(a, np.cross(b, c))))
check("the box's volume is |a . (b x c)| (post)", vol, 168.0)
base = float(np.linalg.norm(np.cross(b, c)))          # area of the base
nhat = np.cross(b, c) / base
height = abs(float(np.dot(a, nhat)))                  # a's component along it
check("  ... which is the base area |b x c| times the height, computed "
      "separately (post)", round(base * height, 6), round(vol, 6))
check("the box has eight corners and twelve edges", (len(CORNERS), len(EDGES)),
      (8, 12))
zc = 0.7 + 1.1j
check("cos maps horizontal lines to ellipses: (u/cosh y)^2 + (v/sinh y)^2 = 1",
      round(float((np.cos(zc).real / np.cosh(zc.imag)) ** 2
                  + (np.cos(zc).imag / np.sinh(zc.imag)) ** 2), 9), 1.0)
check("  ... and vertical lines to hyperbolas: (u/cos x)^2 - (v/sin x)^2 = 1",
      round(float((np.cos(zc).real / np.cos(zc.real)) ** 2
                  - (np.cos(zc).imag / np.sin(zc.real)) ** 2), 9), 1.0)
check("  ... all confocal, with foci at plus and minus 1",
      [round(float(np.cosh(y) ** 2 - np.sinh(y) ** 2), 9) for y in (0.4, 1.2)],
      [1.0, 1.0])
check("the animation starts on the plain grid and ends on the image",
      (0 / (STEPS - 1), (STEPS - 1) / (STEPS - 1)), (0.0, 1.0))
check("cos folds x and -x onto one hyperbola, so the red and black families "
      "meet at the last frame",
      complex(np.cos(-0.9 + 1.3j)), complex(np.conj(np.cos(0.9 + 1.3j))),
      tol=1e-12)
print("  vector and mapping animations: 3 written")
