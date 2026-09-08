#!/usr/bin/env python3
"""p=11427, "Complexity from complex numbers: the beauty of the Mandelbrot set".

Six lost figures, every parameter named in the text:

  MB1   |z_i| for C=0.249 (blue) and C=0.251 (red)
  MB2   |z_i| for C=(1+i)/4 (blue) and C=(1+i)/2.5 (red)
  MB3   100,000 random C in the complex plane, blue in the set, red not
  MB4   the same over Re C in [0.2, 0.5], Im C in [0.25, 0.8]
  MB5   over [0.3, 0.325] x [0.55, 0.62]
  MB6   over [0.315, 0.316] x [0.576, 0.578]

The sampling reproduces the method the post describes rather than a smooth
escape-time render: uniform random C, 100 iterations, in the set if |z| never
exceeds 2. The graininess is the point the post is making.

Mandelset_hires.png is also lost from this post but is deliberately not
reconstructed: the text says it is "an image taken from wikipedia", so it is
someone else's figure, not one of Jonathan's.

Two things the post gets slightly wrong, left as they are and drawn from the
real orbits: it says the C=0.249 orbit "converges to 0.5" when the fixed point
is (1-sqrt(1-4C))/2 = 0.4684, and its C=0.1 table skips z_2=0.11.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREY, save, axes, check, paths_in

P = paths_in("p=11427.html")
rng = np.random.default_rng(11427)


def orbit(C, n):
    z, out = 0j, []
    for _ in range(n):
        z = z * z + C
        out.append(abs(z))
        if abs(z) > 1e8:
            out += [np.nan] * (n - len(out))
            break
    return np.array(out)


def escapes(C, n=100):
    """Vectorised: True where |z| exceeds 2 within n iterations."""
    z = np.zeros_like(C)
    out = np.zeros(C.shape, dtype=bool)
    for _ in range(n):
        z = np.where(out, 0, z * z + C)
        big = np.abs(z) > 2
        out |= big
    return out


def orbit_pair(a, b, la, lb, n, dest, title):
    fig, ax = plt.subplots(figsize=(9.0, 5.9))
    for C, col, lab in ((a, BLUE, la), (b, RED, lb)):
        y = orbit(C, n)
        ax.plot(np.arange(1, n + 1), y, "o", color=col, ms=3.2, label=lab)
    ax.axhline(2, color=GREY, lw=1.0, ls="--")
    ax.text(n * 0.995, 2.06, r"$|z|=2$", ha="right", fontsize=9, color=GREY)
    axes(ax, (0, n), None, xlabel="$i$", ylabel="$|z_i|$")
    ax.set_ylim(0, 4)
    ax.legend(loc="upper left", fontsize=11, frameon=False)
    ax.set_title(title, fontsize=12)
    save(fig, dest)


# --- MB1 and MB2 ----------------------------------------------------------
orbit_pair(0.249, 0.251, "$C=0.249$", "$C=0.251$", 150, P["MB1.png"],
           r"$z_{i+1}=z_i^2+C$ either side of $C=0.25$")
orbit_pair((1 + 1j) / 4, (1 + 1j) / 2.5,
           r"$C=\frac{1+i}{4}$", r"$C=\frac{1+i}{2.5}$", 150, P["MB2.png"],
           r"$z_{i+1}=z_i^2+C$ for two complex $C$")


# --- MB3 to MB6: 100,000 random points in each region ---------------------
def sample(re, im, dest, title, figsize):
    n = 100_000
    C = (rng.uniform(re[0], re[1], n) + 1j * rng.uniform(im[0], im[1], n))
    out = escapes(C)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(C[out].real, C[out].imag, ".", color=RED, ms=0.7, alpha=0.5)
    ax.plot(C[~out].real, C[~out].imag, ".", color=BLUE, ms=0.7, alpha=0.6)
    ax.set_xlim(*re); ax.set_ylim(*im)
    ax.set_xlabel(r"$\mathrm{Re}\,C$"); ax.set_ylabel(r"$\mathrm{Im}\,C$")
    ax.tick_params(labelsize=8)
    ax.set_title(title, fontsize=10)
    save(fig, dest)
    return out


in3 = sample((-2.3, 0.8), (-1.3, 1.3), P["MB3.png"],
             "100,000 random points; blue stays below 2 for 100 iterations",
             (5.6, 3.4))
sample((0.2, 0.5), (0.25, 0.8), P["MB4.png"],
       r"$\mathrm{Re}\,C\in[0.2,0.5]$, $\mathrm{Im}\,C\in[0.25,0.8]$", (5.6, 3.5))
sample((0.3, 0.325), (0.55, 0.62), P["MB5.png"],
       r"$\mathrm{Re}\,C\in[0.3,0.325]$, $\mathrm{Im}\,C\in[0.55,0.62]$", (5.6, 3.3))
sample((0.315, 0.316), (0.576, 0.578), P["MB6.png"],
       r"$\mathrm{Re}\,C\in[0.315,0.316]$, "
       r"$\mathrm{Im}\,C\in[0.576,0.578]$", (5.6, 3.1))

# --- the claims the post makes --------------------------------------------
print("  p=11427 checks:")
o3 = orbit(3, 4)
check("C=3 table row 1 (post: 3)", o3[0], 3)
check("C=3 table row 2 (post: 12)", o3[1], 12)
check("C=3 table row 3 (post: 147)", o3[2], 147)
check("C=3 table row 4 (post: 21612)", o3[3], 21612)
check("C=0.1 fixed point (post: 0.112702)",
      round((1 - np.sqrt(1 - 0.4)) / 2, 6), 0.112702)
check("C=0.249 stays bounded", orbit(0.249, 4000)[-1] < 2, True)
check("C=0.251 escapes, but only after 50 (post's point)",
      int(np.argmax(orbit(0.251, 4000) > 2)) > 50, True)
check("real C in the set exactly on [-2, 0.25] (post's claim), test 0.26",
      bool(escapes(np.array([0.26 + 0j]))[0]), True)
check("  ... and 0.24 is in", bool(escapes(np.array([0.24 + 0j]))[0]), False)
check("  ... and -2.01 is out", bool(escapes(np.array([-2.01 + 0j]))[0]), True)
check("C=(1+i)/4 stays bounded",
      bool(escapes(np.array([(1 + 1j) / 4]))[0]), False)
check("C=(1+i)/2.5 escapes",
      bool(escapes(np.array([(1 + 1j) / 2.5]))[0]), True)
print("  p=11427: 6 figures written (Mandelset_hires.png deliberately skipped, "
      "it is a Wikipedia image)")
