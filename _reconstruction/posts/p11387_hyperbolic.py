#!/usr/bin/env python3
"""p=11387, "MAM1000 part 29, complex numbers part vii".

Two lost figures:

  CoshSinh   cosh and sinh plotted together, the post's point being that "they
             don't behave at all like the normal sine and cosine functions that
             we are used to"
  hypcirc1   "the differences between hyperbolic functions and circular
             functions, which are very close, up to a single sign in their
             definitions, but have completely different behaviours". Its
             recorded 826x431 is two square panels side by side, which is the
             natural pairing: (cos t, sin t) tracing the unit circle against
             (cosh t, sinh t) tracing the unit hyperbola.

The post's third lost image, l2.gif, is an animation of lines mapped under the
cosine, and is left missing.

One slip in the post, left as it is: it calls cosh and sinh "hypergeometric"
cosine and sine. They are hyperbolic; hypergeometric functions are a different
thing entirely.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=11387.html")

# --- CoshSinh -------------------------------------------------------------
b = np.linspace(-3, 3, 600)
fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.plot(b, np.cosh(b), color=BLUE, lw=2.2, label=r"$\cosh b$")
ax.plot(b, np.sinh(b), color=RED, lw=2.2, label=r"$\sinh b$")
axes(ax, (-3, 3), (-10, 10), xlabel=None, ylabel=None)
ax.legend(fontsize=11, frameon=False, loc="upper left")
save(fig, P["CoshSinh.png"])

# --- hypcirc1: the circle against the hyperbola --------------------------
fig, axs = plt.subplots(1, 2, figsize=(8.2, 4.3))
t = np.linspace(0, 2 * np.pi, 500)
axs[0].plot(np.cos(t), np.sin(t), color=BLUE, lw=2.2)
T = np.linspace(-2.2, 2.2, 400)
for s in (1, -1):
    axs[1].plot(s * np.cosh(T), np.sinh(T), color=RED, lw=2.2)
for ax, lab, pt in ((axs[0], r"$x^2+y^2=1$:  $(\cos t,\sin t)$",
                     (np.cos(0.9), np.sin(0.9))),
                    (axs[1], r"$x^2-y^2=1$:  $(\cosh t,\sinh t)$",
                     (np.cosh(0.9), np.sinh(0.9)))):
    ax.plot([0, pt[0]], [0, pt[1]], color=GREEN, lw=1.6, zorder=4)
    ax.plot([pt[0]], [pt[1]], "o", color=GREEN, ms=6, zorder=5)
    axes(ax, (-2.6, 2.6), (-2.6, 2.6), xlabel=None, ylabel=None)
    ax.set_aspect("equal")
    ax.set_title(lab, fontsize=10)
save(fig, P["hypcirc1.png"])

# --- the identities and values the post states ---------------------------
print("  p=11387 checks:")
x = np.linspace(-3, 3, 400)
check("cosh^2 - sinh^2 = 1 (post's identity)",
      float(np.abs(np.cosh(x) ** 2 - np.sinh(x) ** 2 - 1).max()), 0.0,
      tol=1e-9)
check("cos^2 + sin^2 = 1, the sign the post contrasts it with",
      float(np.abs(np.cos(x) ** 2 + np.sin(x) ** 2 - 1).max()), 0.0,
      tol=1e-12)
bb = 1.3
check("cos(ib) = (e^-b + e^b)/2 (post)", complex(np.cos(1j * bb)).real,
      (np.exp(-bb) + np.exp(bb)) / 2)
check("  ... which is cosh b", complex(np.cos(1j * bb)).real, np.cosh(bb))
check("  ... and is purely real", abs(complex(np.cos(1j * bb)).imag), 0.0,
      tol=1e-12)
check("sin(ib) is purely imaginary (post)",
      abs(complex(np.sin(1j * bb)).real), 0.0, tol=1e-12)
check("-i sin(ib) = sinh b (post)",
      complex(-1j * np.sin(1j * bb)).real, np.sinh(bb))
check("cos and sin of a real theta come back real (post's first check)",
      complex(np.cos(0.7 + 0j)).real, np.cos(0.7))
check("both grow large for large |b|, unlike sin and cos (post)",
      np.cosh(5.0) > 70 and abs(np.sinh(-5.0)) > 70, True)
check("the circle point lies on x^2+y^2=1",
      np.cos(0.9) ** 2 + np.sin(0.9) ** 2, 1.0)
check("the hyperbola point lies on x^2-y^2=1",
      np.cosh(0.9) ** 2 - np.sinh(0.9) ** 2, 1.0)
print("  p=11387: 2 figures written (l2.gif left, it is an animation)")
