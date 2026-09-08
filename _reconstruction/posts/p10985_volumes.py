#!/usr/bin/env python3
"""p=10985, "UCT MAM1000 lecture notes part 10" (volumes by cross-section).

Eight lost figures, all of them solids the text describes explicitly:

  toblerone     a tube with a constant triangular cross-section
  cross         the parabolic-faced cylinder, "the red curve y=x^2-2 and the
                blue curve y=-x^2+2 drawn both at z=0 and z=5"
  1csphere      "the smallest circular cylinder we could fit around a sphere
                of radius r would have height 2r and a circular face radius r"
  3cyl          "an approximation with 4, 8 and 16 cylinders"
  sphereslice   one thin disk at position x through a sphere of radius 1, with
                the right-angled triangle giving y = sqrt(r^2 - x^2)
  sqrtfunc1     the region under y=sqrt(x) up to x=1, and that region swept
                about the x axis
  yrot          the same region swept about the y axis instead
  segments      "what would happen if we approximated the shape by five disks
                and then pulled them apart for effect"

Colours in `cross` follow the caption exactly: red for y=x^2-2, blue for
y=-x^2+2, which is the opposite way round from this project's usual
convention, so it is set explicitly there.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from figstyle import (BLUE, RED, GREEN, GREY, FILL, save, axes, check,
                      paths_in, solid3d, revolve, disk_stack)

P = paths_in("p=10985.html")


def tidy(ax, lim=None, labels=True):
    if lim:
        ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_zlim(*lim[2])
    if labels:
        ax.set_xlabel("x", labelpad=-4)
        ax.set_ylabel("y", labelpad=-4)
        ax.set_zlabel("z", labelpad=-4)
    ax.tick_params(labelsize=7, pad=-2)


# --- toblerone.png (562x346): a constant triangular cross-section -----------
fig = plt.figure(figsize=(5.4, 3.4))
ax = solid3d(fig, elev=20, azim=-62, box=(1.6, 1, 1))
tri = np.array([[0.0, 1.0], [-0.9, -0.6], [0.9, -0.6]])
h = 3.2
faces, verts = [], []
for z in (0, h):
    verts.append([(x, y, z) for x, y in tri])
faces += verts
for i in range(3):
    j = (i + 1) % 3
    faces.append([(tri[i][0], tri[i][1], 0), (tri[j][0], tri[j][1], 0),
                  (tri[j][0], tri[j][1], h), (tri[i][0], tri[i][1], h)])
ax.add_collection3d(Poly3DCollection(faces, facecolor=FILL, alpha=0.62,
                                     edgecolor=BLUE, linewidths=1.2))
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, h)
ax.set_title("a cylinder with a constant triangular cross-section", fontsize=10)
ax.set_axis_off()
save(fig, P["toblerone.png"])

# --- cross.png (295x432): parabolic-faced cylinder, faces at z=0 and z=5 ----
xs = np.linspace(-np.sqrt(2), np.sqrt(2), 120)
lower, upper = xs ** 2 - 2, -xs ** 2 + 2
fig = plt.figure(figsize=(3.4, 4.9))
ax = solid3d(fig, elev=16, azim=-70, box=(1, 1, 1.5))
for z in (0.0, 5.0):
    ax.plot(xs, lower, zs=z, color=RED, lw=1.8)
    ax.plot(xs, upper, zs=z, color=BLUE, lw=1.8)
side = []
for a, b in zip(xs[:-1], xs[1:]):
    for f in (lambda t: t ** 2 - 2, lambda t: -t ** 2 + 2):
        side.append([(a, f(a), 0), (b, f(b), 0), (b, f(b), 5), (a, f(a), 5)])
ax.add_collection3d(Poly3DCollection(side, facecolor=FILL, alpha=0.35,
                                     edgecolor="none"))
for z in (0.0, 5.0):
    ax.add_collection3d(Poly3DCollection(
        [list(zip(xs, upper, np.full_like(xs, z)))
         + list(zip(xs[::-1], lower[::-1], np.full_like(xs, z)))],
        facecolor=FILL, alpha=0.5, edgecolor="none"))
tidy(ax, ((-1.6, 1.6), (-2.4, 2.4), (0, 5)))
ax.set_title(r"$h=5$", fontsize=10)
save(fig, P["cross.png"])

# --- 1csphere.png (434x471): sphere in its smallest bounding cylinder -------
fig = plt.figure(figsize=(4.3, 4.7))
ax = solid3d(fig, elev=16, azim=-58)
u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 70), np.linspace(0, np.pi, 40))
ax.plot_surface(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v),
                color="#f4a6a6", alpha=0.95, linewidth=0, shade=True)
th = np.linspace(0, 2 * np.pi, 80)
TH, ZZ = np.meshgrid(th, np.array([-1.0, 1.0]))
ax.plot_surface(np.cos(TH), np.sin(TH), ZZ, color=FILL, alpha=0.25,
                linewidth=0, shade=False)
for z in (-1, 1):
    ax.plot(np.cos(th), np.sin(th), zs=z, color=BLUE, lw=1.4)
tidy(ax, ((-1.1, 1.1), (-1.1, 1.1), (-1.1, 1.1)))
ax.set_title(r"radius $r$, height $2r$:  $V=2\pi r^3$", fontsize=10)
save(fig, P["1csphere.png"])

# --- 3cyl.png (913x374): approximations with 4, 8 and 16 cylinders ---------
fig = plt.figure(figsize=(9.4, 3.9))
for k, n in enumerate((4, 8, 16)):
    ax = solid3d(fig, pos=(1, 3, k + 1), elev=14, azim=-58)
    disk_stack(ax, np.linspace(-1, 1, n + 1),
               lambda x: np.sqrt(max(0.0, 1 - x ** 2)), axis="x")
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
    ax.set_axis_off()
    ax.set_title(f"{n} cylinders", fontsize=10, y=0.94)
fig.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0, wspace=0.0)
save(fig, P["3cyl.png"])

# --- sphereslice.png (439x440): one thin disk at position x ----------------
x0, dx = 0.45, 0.09
fig = plt.figure(figsize=(4.4, 4.4))
ax = solid3d(fig, elev=14, azim=-62)
ax.plot_surface(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v),
                color="#f2c4c4", alpha=0.28, linewidth=0, shade=True)
disk_stack(ax, [x0 - dx / 2, x0 + dx / 2],
           lambda x: np.sqrt(max(0.0, 1 - x ** 2)), axis="x", alpha=0.85)
yv = np.sqrt(1 - x0 ** 2)
ax.plot([0, x0], [0, 0], [0, 0], color=GREEN, lw=2)
ax.plot([x0, x0], [0, yv], [0, 0], color=GREEN, lw=2)
ax.plot([0, x0], [0, yv], [0, 0], color=RED, lw=2)
ax.text(x0 / 2, -0.16, 0, "$x$", color=GREEN, fontsize=12)
ax.text(x0 + 0.05, yv / 2, 0, "$y$", color=GREEN, fontsize=12)
ax.text(x0 / 2 - 0.1, yv / 2 + 0.12, 0, "$r$", color=RED, fontsize=12)
tidy(ax, ((-1.1, 1.1), (-1.1, 1.1), (-1.1, 1.1)))
ax.set_title(r"$y=\sqrt{r^2-x^2}$,  slice volume $\Delta x\,\pi(r^2-x^2)$",
             fontsize=9)
save(fig, P["sphereslice.png"])

# --- sqrtfunc1.png (592x309): the region, and it swept about the x axis ----
fig = plt.figure(figsize=(6.0, 3.2))
ax1 = fig.add_subplot(1, 2, 1)
xr = np.linspace(0, 1, 300)
ax1.plot(xr, np.sqrt(xr), color=BLUE, lw=2)
ax1.fill_between(xr, 0, np.sqrt(xr), color=FILL, alpha=0.6)
ax1.plot([1, 1], [0, 1], color=RED, lw=1.6)
axes(ax1, (-0.05, 1.15), (-0.05, 1.15))
ax1.set_title(r"$y=\sqrt{x}$, $x\leq 1$", fontsize=10)
ax2 = solid3d(fig, pos=(1, 2, 2), elev=16, azim=-60)
revolve(ax2, np.linspace(0, 1, 60), np.sqrt, axis="x")
ax2.set_xlim(0, 1.05); ax2.set_ylim(-1.05, 1.05); ax2.set_zlim(-1.05, 1.05)
ax2.set_axis_off()
ax2.set_title(r"swept about the $x$ axis:  $V=\frac{\pi}{2}$", fontsize=10)
save(fig, P["sqrtfunc1.png"])

# --- yrot.png (525x510): the same region swept about the y axis ------------
fig = plt.figure(figsize=(5.2, 5.0))
ax = solid3d(fig, elev=16, azim=-58, box=(1, 1, 1))
yv2 = np.linspace(0, 1, 60)
revolve(ax, yv2, lambda y: np.ones_like(y), axis="z", alpha=0.30)
revolve(ax, yv2, lambda y: y ** 2, axis="z", alpha=0.75, color="#f4a6a6")
th = np.linspace(0, 2 * np.pi, 90)
for zz, rad in ((0.0, 1.0), (1.0, 1.0)):
    ax.plot(rad * np.cos(th), rad * np.sin(th), zs=zz, color=BLUE, lw=1.2)
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_zlim(0, 1.05)
ax.set_zlabel("y", labelpad=-4)
ax.tick_params(labelsize=7, pad=-2)
ax.set_title(r"swept about the $y$ axis: annuli of area $\pi(1-y^4)$",
             fontsize=9)
save(fig, P["yrot.png"])

# --- segments.png (443x911): five annuli, pulled apart -------------------
fig = plt.figure(figsize=(4.4, 9.0))
ax = solid3d(fig, elev=14, azim=-58, box=(1, 1, 2.4))
th = np.linspace(0, 2 * np.pi, 80)
gapped = 0.0
for i in range(5):
    y_mid = (i + 0.5) / 5
    inner, outer, t = y_mid ** 2, 1.0, 0.11
    base = gapped
    for rad, col, alp in ((outer, FILL, 0.45), (inner, "#f4a6a6", 0.9)):
        TH, ZZ = np.meshgrid(th, np.array([base, base + t]))
        ax.plot_surface(rad * np.cos(TH), rad * np.sin(TH), ZZ, color=col,
                        alpha=alp, linewidth=0, shade=True)
    rr = np.linspace(inner, outer, 8)
    RR, TH2 = np.meshgrid(rr, th)
    for end in (base, base + t):
        ax.plot_surface(RR * np.cos(TH2), RR * np.sin(TH2),
                        np.full_like(RR, end), color=FILL, alpha=0.55,
                        linewidth=0, shade=True)
    ax.text(1.15, 0, base + t / 2, f"$y={y_mid:.1f}$", fontsize=8, color=GREY)
    gapped += t + 0.16
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(0, gapped)
ax.set_axis_off()
ax.set_title("five annuli, pulled apart", fontsize=10, y=0.97)
fig.subplots_adjust(left=-0.06, right=1.06, bottom=-0.10, top=1.02)
save(fig, P["segments.png"])

# --- the numbers the post states -------------------------------------------
print("  p=10985 checks:")
check("parabolas meet at sqrt(2)", np.sqrt(2), 2 ** 0.5)
check("area between them (post: 16sqrt2/3)",
      quad(lambda x: (-x ** 2 + 2) - (x ** 2 - 2), -np.sqrt(2), np.sqrt(2))[0],
      16 * np.sqrt(2) / 3)
check("one-cylinder approximation (post: 2 pi r^3)", 2 * np.pi, 2 * np.pi)
check("sphere by disks (post: 4/3 pi r^3)",
      quad(lambda x: np.pi * (1 - x ** 2), -1, 1)[0], 4 / 3 * np.pi)
check("sqrt(x) about the x axis (post: pi/2)",
      quad(lambda x: np.pi * x, 0, 1)[0], np.pi / 2)
check("sqrt(x) about the y axis (post: 4pi/5)",
      quad(lambda y: np.pi * (1 - y ** 4), 0, 1)[0], 4 * np.pi / 5)
print("  p=10985: 8 figures written")
