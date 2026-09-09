#!/usr/bin/env python3
"""p=11322, "UCT MAM1000 notes part 24, complex numbers part ii".

Four lost figures:

  comp1    "the complex plane with a load of complex numbers labelled on it",
           axes Re(z) and Im(z)
  length   a point z = a+bi with a along the real axis, b along the imaginary
           axis, and |z| the distance from the origin
  conj     conjugation as reflection in the real axis, using the post's own
           examples 2+4i, 3-2i and -2-5i
  mult     z times its conjugate landing on the positive real axis at |z|^2,
           with |z| and |z-bar| equal

The three square figures share a layout; comp1 is the wide one (913x555) and
the post notes it was posted previously, so it is the survey figure rather than
part of the argument.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=11322.html")


def plane(ax, xr, yr):
    axes(ax, xr, yr, xlabel=None, ylabel=None)
    ax.set_aspect("equal")
    ax.text(xr[1], 0.16, r"$Re(z)$", ha="right", fontsize=11, color="#333333")
    ax.text(0.16, yr[1], r"$Im(z)$", va="top", fontsize=11, color="#333333")


def label(z):
    a, b = z.real, z.imag
    if b == 0:
        return f"${a:g}$"
    if a == 0:
        return f"${b:g}i$" if b not in (1, -1) else ("$i$" if b == 1 else "$-i$")
    sign = "+" if b > 0 else "-"
    m = abs(b)
    return f"${a:g}{sign}{'' if m == 1 else f'{m:g}'}i$"


# --- comp1.png (913x555): the plane with a spread of labelled numbers ----
PTS = [2 + 3j, -3 + 2j, -2 - 2j, 3 - 1j, 1j, -1j, 4 + 0j, -4 + 0j,
       1 + 1j, -1 + 3j, 2 - 3j, -3 - 1j]
fig, ax = plt.subplots(figsize=(7.6, 4.6))
for z in PTS:
    ax.plot([z.real], [z.imag], "o", color=BLUE, ms=6, zorder=4)
    ax.annotate(label(z), (z.real, z.imag), textcoords="offset points",
                xytext=(7, 6), fontsize=10, color=BLUE)
plane(ax, (-5.4, 5.4), (-4.0, 4.0))
save(fig, P["comp1.png"])

# --- length.png (750x720): |z| as the distance from the origin ----------
z = 3 + 2j
fig, ax = plt.subplots(figsize=(5.6, 5.4))
ax.plot([0, z.real], [0, z.imag], color=RED, lw=2, zorder=4)
ax.plot([0, z.real], [0, 0], color=GREEN, lw=2, zorder=3)
ax.plot([z.real, z.real], [0, z.imag], color=GREEN, lw=2, zorder=3)
ax.plot([z.real], [z.imag], "o", color=BLUE, ms=7, zorder=5)
ax.annotate(r"$z=a+bi$", (z.real, z.imag), textcoords="offset points",
            xytext=(8, 6), fontsize=11, color=BLUE)
ax.text(z.real / 2, -0.32, "$a$", ha="center", fontsize=12, color=GREEN)
ax.text(z.real + 0.16, z.imag / 2, "$b$", fontsize=12, color=GREEN)
ax.annotate(r"$|z|=\sqrt{a^2+b^2}$", (z.real / 2, z.imag / 2),
            textcoords="offset points", xytext=(-118, 12), fontsize=11,
            color=RED)
plane(ax, (-4.4, 4.4), (-4.0, 4.0))
save(fig, P["length.png"])

# --- conj.png (750x720): conjugation is reflection in the real axis -----
fig, ax = plt.subplots(figsize=(5.6, 5.4))
for w in (2 + 4j, 3 - 2j, -2 - 5j):
    for pt, col in ((w, BLUE), (w.conjugate(), RED)):
        ax.plot([pt.real], [pt.imag], "o", color=col, ms=6, zorder=4)
        ax.annotate(label(pt), (pt.real, pt.imag), textcoords="offset points",
                    xytext=(8, 5), fontsize=10, color=col)
    ax.plot([w.real, w.real], [w.imag, -w.imag], color=GREY, lw=0.9, ls=":",
            zorder=3)
plane(ax, (-6.4, 6.4), (-6.2, 6.2))
save(fig, P["conj.png"])

# --- mult.png (750x720): z times z-bar is real and positive -------------
# z is not named by the text; 1+2i keeps z-bar-z on screen with the equal
# aspect a complex-plane picture needs, at the square shape the original had
z2 = 1 + 2j
prod = z2 * z2.conjugate()
fig, ax = plt.subplots(figsize=(5.6, 5.4))
for pt, col, lab in ((z2, BLUE, r"$z$"), (z2.conjugate(), RED, r"$\bar{z}$")):
    ax.plot([0, pt.real], [0, pt.imag], color=col, lw=1.6, zorder=3)
    ax.plot([pt.real], [pt.imag], "o", color=col, ms=7, zorder=4)
    ax.annotate(f"{lab} $= {label(pt)[1:-1]}$", (pt.real, pt.imag),
                textcoords="offset points", xytext=(8, 6), fontsize=11,
                color=col)
ax.plot([prod.real], [0], "o", color=GREEN, ms=8, zorder=5)
ax.annotate(rf"$z\bar{{z}}={prod.real:g}=|z|^2$", (prod.real, 0),
            textcoords="offset points", xytext=(-40, 14), fontsize=11,
            color=GREEN)
plane(ax, (-2.6, 6.4), (-4.5, 4.5))
save(fig, P["mult.png"])

# --- the arithmetic the post carries out --------------------------------
print("  p=11322 checks:")
check("(2+3i)(1-2i) (post: 8-i)", complex(2 + 3j) * (1 - 2j), complex(8, -1))
check("conjugate of 2+4i (post: 2-4i)", (2 + 4j).conjugate(), complex(2, -4))
check("conjugate of 3-2i (post: 3+2i)", (3 - 2j).conjugate(), complex(3, 2))
check("conjugate of -2-5i (post: -2+5i)", (-2 - 5j).conjugate(),
      complex(-2, 5))
check("z z-bar is a^2+b^2", (z2 * z2.conjugate()).real,
      z2.real ** 2 + z2.imag ** 2)
check("  ... with zero imaginary part", (z2 * z2.conjugate()).imag, 0.0)
check("|z| equals |z-bar|", abs(z2), abs(z2.conjugate()))
check("|z z-bar| is |z| squared", abs(z2 * z2.conjugate()), abs(z2) ** 2)
check("|1+2i| < |200+142i| (post's example)",
      abs(1 + 2j) < abs(200 + 142j), True)
a, b, c, d = 1.0, 2.0, 3.0, 4.0
check("the division formula's real part",
      ((a + b * 1j) / (c + d * 1j)).real, (a * c + b * d) / (c ** 2 + d ** 2))
check("  ... and its imaginary part",
      ((a + b * 1j) / (c + d * 1j)).imag, (b * c - a * d) / (c ** 2 + d ** 2))
print("  p=11322: 4 figures written")
