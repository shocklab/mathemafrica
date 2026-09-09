#!/usr/bin/env python3
"""Four lost figures across the MAM1000 complex-numbers posts in polar form.

p=11330, part iii:
  argmod  "a complex number of modulus 2, and angle pi/4 anti-clockwise from
          the x-axis"
  mult2   multiplication in polar form: "moduli multiply, arguments add"

p=11345, part iv:
  spiral  "(1+0.1i)^n for different n. In the graph below we plot the first 100
          n. The first one, ie. (1+0.1i) is just above the real axis, and is
          red, and as n increases the points go from red to green. The lines
          joining the points to the origin are just for reference. The complex
          numbers are themselves the points."

p=11407, part viii:
  argfifth  the five solutions of z^5 = 1+i, which the post derives as
            z = 2^{1/10} e^{i(pi/20 + 2n pi/5)} for n = 0..4, "plotted in the
            Argand plane"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.colors import LinearSegmentedColormap
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P30 = paths_in("p=11330.html")
P45 = paths_in("p=11345.html")
P07 = paths_in("p=11407.html")


def plane(ax, xr, yr):
    axes(ax, xr, yr, xlabel=None, ylabel=None)
    ax.set_aspect("equal")
    ax.text(xr[1], 0.12 * (yr[1] - yr[0]) / 4, r"$Re(z)$", ha="right",
            fontsize=10, color="#333333")
    ax.text(0.10 * (xr[1] - xr[0]) / 4, yr[1], r"$Im(z)$", va="top",
            fontsize=10, color="#333333")


# --- argmod: modulus 2, argument pi/4 ------------------------------------
z = 2 * np.exp(1j * np.pi / 4)
fig, ax = plt.subplots(figsize=(5.4, 5.2))
ax.plot([0, z.real], [0, z.imag], color=RED, lw=2.4, zorder=4)
ax.plot([z.real], [z.imag], "o", color=BLUE, ms=8, zorder=5)
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(2 * np.cos(th), 2 * np.sin(th), color=GREY, lw=1.0, ls=":")
ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=0, theta2=45, color=RED, lw=1.4))
ax.text(0.80, 0.22, r"$\frac{\pi}{4}$", fontsize=12, color=RED)
ax.annotate(r"$|z|=2$", (z.real / 2, z.imag / 2), textcoords="offset points",
            xytext=(-52, 6), fontsize=11, color=RED)
ax.annotate(rf"$z=\sqrt{{2}}+i\sqrt{{2}}$", (z.real, z.imag),
            textcoords="offset points", xytext=(8, 6), fontsize=11,
            color=BLUE)
plane(ax, (-2.8, 3.4), (-2.8, 3.0))
save(fig, P30["argmod.png"])

# --- mult2: moduli multiply, arguments add -------------------------------
z1 = 1.6 * np.exp(1j * 0.5)
z2 = 1.4 * np.exp(1j * 0.85)
zp = z1 * z2
fig, ax = plt.subplots(figsize=(5.4, 5.3))
for w, col, lab in ((z1, BLUE, r"$z_1$"), (z2, GREEN, r"$z_2$"),
                    (zp, RED, r"$z_1z_2$")):
    ax.plot([0, w.real], [0, w.imag], color=col, lw=2.2, zorder=4)
    ax.plot([w.real], [w.imag], "o", color=col, ms=7, zorder=5)
    ax.annotate(lab, (w.real, w.imag), textcoords="offset points",
                xytext=(8, 6), fontsize=12, color=col)
ax.text(-2.6, 2.5, r"$|z_1z_2|=|z_1||z_2|$" "\n"
        r"$\arg(z_1z_2)=\arg z_1+\arg z_2$", fontsize=10, va="top")
plane(ax, (-2.8, 3.4), (-1.6, 3.4))
save(fig, P30["mult2.png"])

# --- spiral: (1+0.1i)^n for n = 1..100 -----------------------------------
n = np.arange(1, 101)
pts = (1 + 0.1j) ** n
cmap = LinearSegmentedColormap.from_list("rg", ["#d02020", "#2e9e2e"])
fig, ax = plt.subplots(figsize=(5.4, 5.2))
lim = float(np.abs(pts).max()) * 1.12
for k, p in enumerate(pts):
    ax.plot([0, p.real], [0, p.imag], color=cmap(k / (len(pts) - 1)),
            lw=0.5, alpha=0.55, zorder=2)
ax.scatter(pts.real, pts.imag, c=np.arange(len(pts)), cmap=cmap, s=16,
           zorder=4)
plane(ax, (-lim, lim), (-lim, lim))
ax.set_title(r"$(1+0.1i)^n$ for $n=1\ldots100$", fontsize=11)
save(fig, P45["spiral.png"])

# --- argfifth: the five fifth roots of 1+i -------------------------------
roots = np.array([2 ** 0.1 * np.exp(1j * (np.pi / 20 + 2 * k * np.pi / 5))
                  for k in range(5)])
fig, ax = plt.subplots(figsize=(5.6, 5.6))
r = 2 ** 0.1
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(r * np.cos(th), r * np.sin(th), color=GREY, lw=1.0, ls=":")
for k, w in enumerate(roots):
    ax.plot([0, w.real], [0, w.imag], color=BLUE, lw=1.2, zorder=3)
    ax.plot([w.real], [w.imag], "o", color=RED, ms=8, zorder=5)
    ax.annotate(f"$n={k}$", (w.real, w.imag), textcoords="offset points",
                xytext=(9, 6), fontsize=10, color=RED)
plane(ax, (-1.7, 1.9), (-1.7, 1.9))
ax.set_title(r"$z^5=1+i$:  $z=2^{1/10}e^{i(\pi/20+2n\pi/5)}$", fontsize=11)
save(fig, P07["argfifth.png"])

# --- the arithmetic the posts carry out ----------------------------------
print("  MAM1000 complex polar checks:")
check("modulus 2 at pi/4 is sqrt(2)+i sqrt(2) (post)", z,
      complex(np.sqrt(2), np.sqrt(2)))
check("moduli multiply", abs(zp), abs(z1) * abs(z2))
check("  ... and arguments add", float(np.angle(zp)),
      float(np.angle(z1) + np.angle(z2)))
check("(1+0.1i) lies just above the real axis (post)",
      0 < float(np.angle(1 + 0.1j)) < 0.11, True)
check("  ... and the powers spiral outwards", abs(pts[-1]) > abs(pts[0]),
      True)
check("1+i has modulus sqrt(2) and argument pi/4 (post)",
      (round(abs(1 + 1j), 12), round(float(np.angle(1 + 1j)), 12)),
      (round(np.sqrt(2), 12), round(np.pi / 4, 12)))
for k, w in enumerate(roots):
    check(f"  root n={k} satisfies z^5 = 1+i", w ** 5, complex(1, 1),
          tol=1e-12)
check("the five roots are distinct (post: n=5 repeats n=0)",
      len({complex(round(w.real, 9), round(w.imag, 9)) for w in roots}), 5)
check("  ... and n=5 does repeat n=0",
      2 ** 0.1 * np.exp(1j * (np.pi / 20 + 2 * 5 * np.pi / 5)), roots[0],
      tol=1e-12)
check("all five have modulus 2^{1/10}",
      float(max(abs(abs(w) - 2 ** 0.1) for w in roots)), 0.0, tol=1e-12)
print("  MAM1000 complex polar: 4 figures written")
