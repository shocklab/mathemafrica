#!/usr/bin/env python3
"""p=14753, "A tricky complex numbers problem".

Three lost figures, building the construction that solves
arg(z+a) = pi/6, arg(z-a) = 2pi/3, a real:

  pl1-3  the two rays from the origin at pi/6 and 2pi/3, the loci the two
         argument conditions allow
  pl2-1  plus the horizontal segment joining them, "which clearly has length
         2a", drawn "at some random position, so don't take the height here to
         mean anything"
  pl3    plus the angles and the length r from the origin to z+a

The post's own arithmetic follows: r = 2a cos(pi/6) = sqrt(3) a, so
z+a = 3a/2 + i sqrt(3) a/2 and z = a e^{i pi/3}. All of it is asserted below,
including that the triangle is right-angled because 2pi/3 - pi/6 = pi/2.

Drawn at a = 2, which puts z+a at (3, sqrt(3)) and z-a at (-1, sqrt(3)).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=14753.html")
A = 2.0
TH1, TH2 = np.pi / 6, 2 * np.pi / 3
ZPA = complex(3 * A / 2, np.sqrt(3) * A / 2)     # z + a
ZMA = ZPA - 2 * A                                # z - a
Z = ZPA - A
R = abs(ZPA)


def base(ax):
    t = np.linspace(0, 4.6, 2)
    for th, col in ((TH1, RED), (TH2, GREEN)):
        ax.plot(t * np.cos(th), t * np.sin(th), color=col, lw=2)
    ax.annotate(r"$\arg=\frac{\pi}{6}$", (4.4 * np.cos(TH1), 4.4 * np.sin(TH1)),
                textcoords="offset points", xytext=(-28, 12), fontsize=10,
                color=RED)
    ax.annotate(r"$\arg=\frac{2\pi}{3}$", (3.4 * np.cos(TH2), 3.4 * np.sin(TH2)),
                textcoords="offset points", xytext=(-24, 8), fontsize=10,
                color=GREEN)
    axes(ax, (-3.6, 4.6), (-1.6, 4.4), xlabel=None, ylabel=None)
    ax.set_aspect("equal")


fig, ax = plt.subplots(figsize=(5.2, 5.2))
base(ax)
save(fig, P["pl1-3.png"])

fig, ax = plt.subplots(figsize=(5.4, 5.4))
base(ax)
ax.plot([ZMA.real, ZPA.real], [ZMA.imag, ZPA.imag], color=BLUE, lw=2.2,
        zorder=5)
for pt, lab, ha in ((ZPA, "$z+a$", "left"), (ZMA, "$z-a$", "right")):
    ax.plot([pt.real], [pt.imag], "o", color=BLUE, ms=7, zorder=6)
    ax.annotate(lab, (pt.real, pt.imag), textcoords="offset points",
                xytext=(8 if ha == "left" else -40, 8), fontsize=11,
                color=BLUE)
ax.annotate("$2a$", ((ZMA.real + ZPA.real) / 2, ZPA.imag),
            textcoords="offset points", xytext=(-8, 8), fontsize=11,
            color=BLUE)
save(fig, P["pl2-1.png"])

fig, ax = plt.subplots(figsize=(5.2, 5.2))
base(ax)
ax.plot([ZMA.real, ZPA.real], [ZMA.imag, ZPA.imag], color=BLUE, lw=2.2,
        zorder=5)
ax.plot([0, ZPA.real], [0, ZPA.imag], color=RED, lw=2.4, zorder=5)
ax.plot([0, ZMA.real], [0, ZMA.imag], color=GREEN, lw=2.4, zorder=5)
for pt, lab, off in ((ZPA, "$z+a$", (10, -18)), (ZMA, "$z-a$", (-46, -18))):
    ax.plot([pt.real], [pt.imag], "o", color=BLUE, ms=7, zorder=6)
    ax.annotate(lab, (pt.real, pt.imag), textcoords="offset points",
                xytext=off, fontsize=11, color=BLUE)
ax.add_patch(Arc((0, 0), 1.8, 1.8, theta1=0, theta2=30, color=RED, lw=1.4))
ax.text(1.05, 0.16, r"$\frac{\pi}{6}$", fontsize=11, color=RED)
ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=120, color=GREEN, lw=1.4))
ax.text(-0.42, 0.72, r"$\frac{2\pi}{3}$", fontsize=11, color=GREEN)
ax.annotate("$r$", (ZPA.real / 2, ZPA.imag / 2), textcoords="offset points",
            xytext=(6, -14), fontsize=12, color=RED)
ax.annotate("$2a$", ((ZMA.real + ZPA.real) / 2, ZPA.imag),
            textcoords="offset points", xytext=(-8, 8), fontsize=11,
            color=BLUE)
save(fig, P["pl3.png"])

# --- every step the post takes -------------------------------------------
print("  p=14753 checks:")
check("arg(z+a) is pi/6 (the problem's condition)", float(np.angle(ZPA)),
      TH1)
check("arg(z-a) is 2pi/3 (the other condition)", float(np.angle(ZMA)), TH2)
check("z+a and z-a share an imaginary part (post's first observation)",
      ZPA.imag, ZMA.imag)
check("  ... and differ by 2a", ZPA.real - ZMA.real, 2 * A)
check("the triangle is right-angled: 2pi/3 - pi/6 = pi/2 (post)",
      TH2 - TH1, np.pi / 2)
check("r = 2a cos(pi/6) = sqrt(3) a (post)", R, np.sqrt(3) * A)
check("Re(z+a) = 3a/2 (post)", ZPA.real, 3 * A / 2)
check("Im(z+a) = sqrt(3)a/2 (post)", ZPA.imag, np.sqrt(3) * A / 2)
check("z = a(1/2 + i sqrt(3)/2) (post)", Z, A * (0.5 + 1j * np.sqrt(3) / 2))
check("  ... which has modulus a", abs(Z), A)
check("  ... and argument pi/3", float(np.angle(Z)), np.pi / 3)
check("so z = a e^{i pi/3} (post's final form)", Z,
      A * np.exp(1j * np.pi / 3))
print("  p=14753: 3 figures written")
