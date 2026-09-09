#!/usr/bin/env python3
"""p=13671, "Some more volume visualisations". Three lost animations.

The post says what each one shows, and the third in unusual detail:

  movie3-1  "an animation which may help you imaging a shape which has a
            circular base, with parallel slices perpendicular to the base being
            equilateral triangles"
  movie4    "The same thing, where the slices are squares."
  movie5    "the region in the (x,y) plane between y = sqrt(x), the x-axis and
            the line x=1, rotated about the y-axis. Here a thin shell is drawn
            in the volume, then pulled out. Then it is replaced, then the
            volume is filled with shells, and each of them is pulled out of the
            volume vertically. This is to give you an idea about how to
            visualise the method of cylindrical shells."

So movie5 runs in four acts, and it is built here in those four acts. The other
two sweep a slice across the disk while the solid it generates accumulates
behind it, since a still of the finished solid is what the sibling post already
shows and the animation's job is to make the slicing visible.

The volumes are the ones the method gives, and both are checked against the
integrals below before anything is drawn.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from figstyle import BLUE, RED, GREY, FILL, MMA, animate, check, paths_in

P = paths_in("p=13671.html")
R = 1.0
NSLAB = 15


def half_chord(y):
    return float(np.sqrt(max(R ** 2 - y ** 2, 0.0)))


def slab(y, dy, kind):
    """One slice standing on the chord at height y, as polygon faces."""
    s = 2 * half_chord(y)                      # the chord, the slice's base
    if s <= 1e-9:
        return []
    h = s * np.sqrt(3) / 2 if kind == "triangle" else s
    x0 = half_chord(y)
    if kind == "triangle":
        pts = [(-x0, 0.0), (x0, 0.0), (0.0, h)]
    else:
        pts = [(-x0, 0.0), (x0, 0.0), (x0, h), (-x0, h)]
    front = [(x, y, z) for x, z in pts]
    back = [(x, y + dy, z) for x, z in pts]
    faces = [front, back]
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        faces.append([front[i], front[j], back[j], back[i]])
    return faces


def cross_section_gif(dest, kind):
    ys = np.linspace(-R, R, NSLAB + 1)
    dy = ys[1] - ys[0]
    top = R * (np.sqrt(3) if kind == "triangle" else 2.0)

    def draw(ax, i):
        th = np.linspace(0, 2 * np.pi, 160)
        ax.plot(R * np.cos(th), R * np.sin(th), 0 * th, color=GREY, lw=1.2)
        done, cur = [], []
        for k in range(i + 1):
            fs = slab(ys[k], dy, kind)
            (cur if k == i else done).extend(fs)
        if done:
            ax.add_collection3d(Poly3DCollection(
                done, facecolor=MMA[0], alpha=0.45, edgecolor="#2f4b6e",
                lw=0.35))
        if cur:
            ax.add_collection3d(Poly3DCollection(
                cur, facecolor=RED, alpha=0.85, edgecolor="#7a0000", lw=0.6))
        ax.view_init(elev=20, azim=-58)
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(0, top)
        ax.set_box_aspect((1, 1, 0.9))
        ax.set_axis_off()
        ax.set_title(f"circular base, {kind} cross-sections", fontsize=9)

    animate(draw, NSLAB, dest, figsize=(3.7, 4.1), ms=140, three_d=True)


cross_section_gif(P["movie3-1.gif"], "triangle")
cross_section_gif(P["movie4.gif"], "square")

# --- movie5: cylindrical shells, in the post's four acts ------------------
# region between y = sqrt(x), the x-axis and x = 1, turned about the y-axis
NSHELL = 12
EDGES = np.linspace(0.0, 1.0, NSHELL + 1)
ACT = [18, 16, 14, 26]                 # draw one, pull it out, refill, pull all


def shell_faces(r0, r1, h, lift=0.0, n=40):
    th = np.linspace(0, 2 * np.pi, n)
    faces = []
    for r in (r0, r1):
        x, y = r * np.cos(th), r * np.sin(th)
        for k in range(n - 1):
            faces.append([(x[k], y[k], lift), (x[k + 1], y[k + 1], lift),
                          (x[k + 1], y[k + 1], lift + h), (x[k], y[k], lift + h)])
    xo, yo = r1 * np.cos(th), r1 * np.sin(th)
    xi, yi = r0 * np.cos(th), r0 * np.sin(th)
    for k in range(n - 1):
        faces.append([(xi[k], yi[k], lift + h), (xo[k], yo[k], lift + h),
                      (xo[k + 1], yo[k + 1], lift + h), (xi[k + 1], yi[k + 1], lift + h)])
    return faces


def solid_surface(ax):
    """The solid itself: y = sqrt(x) turned about the y-axis, so z = sqrt(r).

    Its top curves up from the centre to z = 1 at the rim, so the outer wall
    and the base are drawn as well; without them the shape reads as a saucer
    rather than as something a shell could sit inside.
    """
    r = np.linspace(0, 1, 40)
    th = np.linspace(0, 2 * np.pi, 60)
    Rr, TH = np.meshgrid(r, th)
    ax.plot_surface(Rr * np.cos(TH), Rr * np.sin(TH), np.sqrt(Rr),
                    color=MMA[0], alpha=0.30, linewidth=0, shade=True)
    Z, TH2 = np.meshgrid(np.linspace(0, 1, 12), th)
    ax.plot_surface(np.cos(TH2), np.sin(TH2), Z, color=MMA[0], alpha=0.20,
                    linewidth=0, shade=True)
    ax.plot_surface(Rr * np.cos(TH), Rr * np.sin(TH), 0 * Rr, color=MMA[0],
                    alpha=0.22, linewidth=0, shade=True)


def draw_shells(ax, i):
    acts = np.cumsum(ACT)
    ax.view_init(elev=18, azim=-58 + 40 * i / sum(ACT))
    if i < acts[0]:                                   # act 1: one shell drawn
        solid_surface(ax)
        k = NSHELL // 2
        h = float(np.sqrt(EDGES[k + 1]))
        ax.add_collection3d(Poly3DCollection(
            shell_faces(EDGES[k], EDGES[k + 1], h), facecolor=RED, alpha=0.85,
            edgecolor="none"))
        note = "one thin shell, inside the solid"
    elif i < acts[1]:                                 # act 2: pull it out
        solid_surface(ax)
        k = NSHELL // 2
        h = float(np.sqrt(EDGES[k + 1]))
        lift = 1.15 * (i - acts[0]) / ACT[1]
        ax.add_collection3d(Poly3DCollection(
            shell_faces(EDGES[k], EDGES[k + 1], h, lift=lift), facecolor=RED,
            alpha=0.85, edgecolor="none"))
        note = "the same shell, pulled out"
    elif i < acts[2]:                                 # act 3: fill with shells
        m = int(NSHELL * (i - acts[1] + 1) / ACT[2])
        # the outer shell is the tallest, so it would hide every inner one:
        # they are drawn see-through, with their rims picked out
        for k in range(min(m, NSHELL)):
            ax.add_collection3d(Poly3DCollection(
                shell_faces(EDGES[k], EDGES[k + 1], float(np.sqrt(EDGES[k + 1]))),
                facecolor=MMA[k % len(MMA)], alpha=0.28,
                edgecolor="#44506080", lw=0.3))
        note = "the volume filled with shells"
    else:                                             # act 4: pull them all
        f = (i - acts[2] + 1) / ACT[3]
        for k in range(NSHELL):
            ax.add_collection3d(Poly3DCollection(
                shell_faces(EDGES[k], EDGES[k + 1], float(np.sqrt(EDGES[k + 1])),
                            lift=1.5 * f * (k + 1) / NSHELL),
                facecolor=MMA[k % len(MMA)], alpha=0.7, edgecolor="none"))
        note = "each shell pulled out vertically"
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15); ax.set_zlim(0, 2.7)
    ax.set_box_aspect((1, 1, 1.25))
    ax.set_axis_off()
    ax.set_title(note, fontsize=9)


animate(draw_shells, sum(ACT), P["movie5.gif"], figsize=(3.6, 4.0), ms=120,
        three_d=True)

# --- what the post asserts ------------------------------------------------
print("  p=13671 checks:")
tri = quad(lambda y: np.sqrt(3) * (R ** 2 - y ** 2), -R, R)[0]
check("equilateral slices on a circular base give volume 4 sqrt(3) r^3 / 3",
      round(tri, 9), round(4 * np.sqrt(3) / 3, 9))
sq = quad(lambda y: 4 * (R ** 2 - y ** 2), -R, R)[0]
check("square slices give 16 r^3 / 3", round(sq, 9), round(16 / 3, 9))
check("  ... which is 4/sqrt(3) times the triangular one, the ratio of the "
      "areas of a square and an equilateral triangle on the same base",
      round(sq / tri, 9), round(4 / np.sqrt(3), 9))
check("the slice at y is an equilateral triangle on the chord, so its height "
      "is sqrt(3)/2 times the chord", round(slab(0.5, 0.01, "triangle")[0][2][2],
      9), round(np.sqrt(3) * half_chord(0.5), 9))
shells = quad(lambda r: 2 * np.pi * r * np.sqrt(r), 0, 1)[0]
check("shells give the volume 2 pi int_0^1 r sqrt(r) dr = 4 pi / 5",
      round(shells, 9), round(4 * np.pi / 5, 9))
washers = quad(lambda y: np.pi * (1 - y ** 4), 0, 1)[0]
check("  ... and washers in y give the same, which is the point of the method",
      round(washers, 9), round(shells, 9))
check("the region is bounded by y = sqrt(x), the x-axis and x = 1 (post): its "
      "corner is at (1,1)", (1.0, float(np.sqrt(1.0))), (1.0, 1.0))
check("turning it about the y-axis makes the surface z = sqrt(r)",
      round(float(np.sqrt(0.49)), 9), 0.7)
print("  p=13671: 3 animations written")
