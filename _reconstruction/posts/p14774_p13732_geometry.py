#!/usr/bin/env python3
"""Three lost figures across two geometry posts.

p=14774, the corridor problem:
  cor   the L-shaped corridor "where a and b are the widths of the sections"
  cor2  "the pipe here is the blue line and theta is the angle that it makes
        with respect to the corner", the configuration whose length is
        l = b/sin(theta) + a/cos(theta)

p=13732, skew lines:
  Untitled-5  the two lines f(t): x = 1+2t, y = 2-3t, z = 3+4t and
              h(s): x = -1+3s, y = 3-s, z = -5+5s, "plotted in 3 space in order
              to justify their skewness i.e. they do not intersect and are not
              parallel"

The corridor post's stated critical point reads arctan(sqrt(3) b/a) in the
recovered LaTeX, but that is the URL decoding losing an optional argument: the
next line writes arctan(cbrt(b/a)), and only the cube root satisfies the
condition b cos^3(theta) = a sin^3(theta) the post derives. The cube root is
what is used and checked here.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, FILL, save, axes, check, \
    paths_in, mma_axes

P74 = paths_in("p=14774.html")
P32 = paths_in("p=13732.html")
A, B = 1.4, 1.0          # the two corridor widths, for drawing


def corridor(ax):
    """The L-shaped corridor: a vertical arm of width a, a horizontal one b."""
    outer = [(0, 0), (0, 5), (A, 5), (A, B), (5, B), (5, 0)]
    ax.fill(*zip(*outer), facecolor=FILL, alpha=0.55, edgecolor="none")
    walls = [[(0, 5), (0, 0), (5, 0)],
             [(A, 5), (A, B), (5, B)]]
    for w in walls:
        ax.plot(*zip(*w), color="black", lw=2.0)
    ax.annotate("", xy=(0, 4.2), xytext=(A, 4.2),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.4))
    ax.text(A / 2, 4.35, "$a$", ha="center", fontsize=13, color=RED)
    ax.annotate("", xy=(4.2, 0), xytext=(4.2, B),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.4))
    ax.text(4.35, B / 2, "$b$", va="center", fontsize=13, color=RED)
    ax.set_xlim(-0.5, 5.2); ax.set_ylim(-0.5, 5.2)
    ax.set_aspect("equal")
    ax.set_axis_off()


fig, ax = plt.subplots(figsize=(4.4, 4.4))
corridor(ax)
save(fig, P74["cor.png"])

# --- cor2: a pipe at angle theta, touching the inner corner --------------
th = 0.72
fig, ax = plt.subplots(figsize=(4.6, 4.6))
corridor(ax)
corner = np.array([A, B])
p1 = corner + np.array([-A, A * np.tan(th)])          # meets the left wall
p2 = corner + np.array([B / np.tan(th), -B])          # meets the bottom wall
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=BLUE, lw=2.6, zorder=6)
ax.plot([corner[0]], [corner[1]], "o", color=RED, ms=6, zorder=7)
ax.plot([p2[0], p2[0] + 1.2], [p2[1], p2[1]], color=GREY, lw=1.0, ls=":")
ang = np.linspace(0, th, 60)
ax.plot(p2[0] + 0.8 * np.cos(ang), p2[1] + 0.8 * np.sin(ang), color=GREEN,
        lw=1.4)
ax.text(p2[0] + 0.95, p2[1] + 0.22, r"$\theta$", fontsize=13, color=GREEN)
ax.annotate(r"$l=\frac{b}{\sin\theta}+\frac{a}{\cos\theta}$",
            ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2),
            textcoords="offset points", xytext=(18, 26), fontsize=12,
            color=BLUE)
save(fig, P74["cor2.png"])

# --- Untitled-5: two skew lines ------------------------------------------
t = np.linspace(-2, 2, 2)
f = np.stack([1 + 2 * t, 2 - 3 * t, 3 + 4 * t], axis=1)
g = np.stack([-1 + 3 * t, 3 - t, -5 + 5 * t], axis=1)
fig = plt.figure(figsize=(2.6, 5.2))
ax = mma_axes(fig, elev=18, azim=-58)
ax.plot(f[:, 0], f[:, 1], f[:, 2], color=BLUE, lw=2.4, label="$f(t)$")
ax.plot(g[:, 0], g[:, 1], g[:, 2], color=RED, lw=2.4, label="$h(s)$")
ax.legend(fontsize=8, frameon=False, loc="upper left")
ax.set_box_aspect((1, 1, 2.0))
save(fig, P32["Untitled-5.png"])

# --- the post's own derivations -------------------------------------------
print("  p=14774 / p=13732 checks:")
length = lambda a, b, x: b / np.sin(x) + a / np.cos(x)
for a, b in ((1.0, 1.0), (1.4, 1.0), (2.0, 0.7), (0.5, 3.0)):
    star = np.arctan((b / a) ** (1 / 3))
    num = minimize_scalar(lambda x: length(a, b, x),
                          bounds=(1e-4, np.pi / 2 - 1e-4), method="bounded")
    check(f"a={a:g}, b={b:g}: the critical point is arctan(cbrt(b/a))",
          float(star), float(num.x), tol=1e-5)
    check("  ... and l there is (a^{2/3}+b^{2/3})^{3/2} (post)",
          float(length(a, b, star)),
          float((a ** (2 / 3) + b ** (2 / 3)) ** 1.5), tol=1e-9)
    check("  ... which satisfies b cos^3 = a sin^3 (post's condition)",
          float(b * np.cos(star) ** 3), float(a * np.sin(star) ** 3),
          tol=1e-12)
check("l diverges at theta = 0 (post's reason for the open interval)",
      length(1.0, 1.0, 1e-6) > 1e5, True)
check("  ... and at pi/2", length(1.0, 1.0, np.pi / 2 - 1e-6) > 1e5, True)

d1, d2 = np.array([2.0, -3, 4]), np.array([3.0, -1, 5])
check("the two lines are not parallel (post)",
      float(np.linalg.norm(np.cross(d1, d2))) > 1e-9, True)
M = np.array([[2.0, -3], [-3.0, 1], [4.0, -5]])
rhs = np.array([-2.0, 1.0, -8.0])
sol, res, *_ = np.linalg.lstsq(M, rhs, rcond=None)
check("  ... and do not intersect: the system has no exact solution",
      float(np.linalg.norm(M @ sol - rhs)) > 1e-6, True)
print("  p=14774 / p=13732: 3 figures written")
