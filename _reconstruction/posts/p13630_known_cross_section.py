#!/usr/bin/env python3
"""p=13630, "Using integration to calculate the volume of a solid with a known
cross-sectional area".

Seven lost images. Six are the small illustrations of solids the post lines up
to make its point: "You should be able to calculate the volumes of the
cylinders below (yes, they are all cylinders)" and then "The figures below are
not cylinders". The seventh, cone_derive.png, is the derivation figure with a
typical slice at x_i.

The six solids were most likely clipart rather than Jonathan's own plots, and
three of them (cone.jpg, pyramid.jpg, circular-cylinder.gif) fell outside the
PNG triage. They are drawn here anyway, in one consistent style: a cone, a
sphere and a box are generic geometry rather than anyone's creative work, and
restoring only half of each row would leave the comparison the post is drawing
half broken.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from figstyle import (BLUE, RED, GREY, FILL, UPLOADS, NOTE, save, axes,
                      check, paths_in, solid3d)

P = paths_in("p=13630.html")
TH = np.linspace(0, 2 * np.pi, 90)


def blank(ax):
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))


def tube(ax, section, h=2.0, color=FILL, edge=BLUE):
    """Extrude a closed 2-D section along z."""
    n = len(section)
    faces = [[(x, y, 0) for x, y in section], [(x, y, h) for x, y in section]]
    for i in range(n):
        j = (i + 1) % n
        faces.append([(section[i][0], section[i][1], 0),
                      (section[j][0], section[j][1], 0),
                      (section[j][0], section[j][1], h),
                      (section[i][0], section[i][1], h)])
    ax.add_collection3d(Poly3DCollection(faces, facecolor=color, alpha=0.65,
                                         edgecolor=edge, linewidths=1.1))


def circle(n=60, r=1.0):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return list(zip(r * np.cos(t), r * np.sin(t)))


# --- the three cylinders --------------------------------------------------
fig = plt.figure(figsize=(2.0, 3.0))
ax = solid3d(fig, elev=14, azim=-62)
tube(ax, circle(), h=3.0)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, 3.0)
blank(ax)
save(fig, P["circular-cylinder.gif"])

fig = plt.figure(figsize=(3.0, 1.9))
ax = solid3d(fig, elev=18, azim=-60)
tube(ax, [(-1, -0.6), (1, -0.6), (1, 0.6), (-1, 0.6)], h=1.5)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, 1.5)
blank(ax)
save(fig, P["rectangular-cylinder.png"])

fig = plt.figure(figsize=(3.0, 1.8))
ax = solid3d(fig, elev=18, azim=-60)
tube(ax, [(0, 0.9), (-0.85, -0.55), (0.85, -0.55)], h=2.4)
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(0, 2.4)
blank(ax)
save(fig, P["triangular-cylinder.png"])

# --- the three that are not cylinders ------------------------------------
fig = plt.figure(figsize=(2.3, 2.3))
ax = solid3d(fig, elev=14, azim=-60)
t, zz = np.meshgrid(TH, np.linspace(0, 1, 30))
ax.plot_surface(np.cos(t) * (1 - zz), np.sin(t) * (1 - zz), zz * 2.2,
                color=FILL, alpha=0.75, linewidth=0, shade=True)
ax.plot(np.cos(TH), np.sin(TH), zs=0, color=BLUE, lw=1.2)
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, 2.2)
blank(ax)
save(fig, P["cone.jpg"])

fig = plt.figure(figsize=(2.3, 2.3))
ax = solid3d(fig, elev=14, azim=-60)
u, v = np.meshgrid(TH, np.linspace(0, np.pi, 45))
ax.plot_surface(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v),
                color=FILL, alpha=0.8, linewidth=0, shade=True)
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
blank(ax)
save(fig, P["sphere.png"])

fig = plt.figure(figsize=(2.1, 2.1))
ax = solid3d(fig, elev=16, azim=-60)
b = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
apex = (0, 0, 1.9)
faces = [[(x, y, 0) for x, y in b]]
for i in range(4):
    j = (i + 1) % 4
    faces.append([(b[i][0], b[i][1], 0), (b[j][0], b[j][1], 0), apex])
ax.add_collection3d(Poly3DCollection(faces, facecolor=FILL, alpha=0.7,
                                     edgecolor=BLUE, linewidths=1.1))
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, 1.9)
blank(ax)
save(fig, P["pyramid.jpg"])

# --- cone_derive.png: the cone in the plane with a typical slice ---------
h, r = 4.0, 1.6
fig, ax = plt.subplots(figsize=(4.4, 2.95))
x = np.linspace(0, h, 200)
ax.plot(x, r / h * x, color=BLUE, lw=2)
ax.plot(x, -r / h * x, color=BLUE, lw=2)
ax.plot([h, h], [-r, r], color=BLUE, lw=2)
ax.fill_between(x, -r / h * x, r / h * x, color=FILL, alpha=0.45)
xi, dx = 2.4, 0.30
yi = r / h * xi
ax.add_patch(plt.Rectangle((xi - dx / 2, -yi), dx, 2 * yi,
                           facecolor="#f2b8b8", edgecolor=RED, lw=1.2,
                           zorder=4))
ax.plot([xi, xi], [0, yi], color=RED, lw=1.4, zorder=5)
ax.annotate(r"$y_i$", (xi, yi / 2), textcoords="offset points",
            xytext=(6, -2), fontsize=10, color=RED)
ax.annotate(r"$\Delta x$", (xi, -yi), textcoords="offset points",
            xytext=(-6, -18), fontsize=10, color=RED)
ax.plot([h], [r], "o", color=GREY, ms=5)
ax.annotate(r"$(h,r)$", (h, r), textcoords="offset points",
            xytext=(-34, 8), fontsize=10, color=GREY)
ax.annotate(r"$y=\frac{r}{h}x$", (h * 0.72, r / h * h * 0.72),
            textcoords="offset points", xytext=(-64, 16), fontsize=10,
            color=BLUE)
axes(ax, (-0.4, h + 0.7), (-r - 0.6, r + 0.9))
save(fig, P["cone_derive.png"])

# --- the derivation the post carries out --------------------------------
from scipy.integrate import quad
print("  p=13630 checks:")
check("slice radius at x is (r/h)x", r / h * xi, yi)
check("cone volume by the post's integral (post: pi r^2 h / 3)",
      quad(lambda t: np.pi * (r / h * t) ** 2, 0, h)[0],
      np.pi / 3 * r ** 2 * h)
check("  ... and matches the closed form for r=1.6, h=4",
      np.pi / 3 * 1.6 ** 2 * 4, np.pi / 3 * r ** 2 * h)
check("a cylinder is cross-section times length", np.pi * 1 ** 2 * 3.0,
      np.pi * 3.0)
print("  p=13630: 7 figures written")
