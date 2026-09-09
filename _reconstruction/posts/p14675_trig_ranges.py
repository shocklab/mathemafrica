#!/usr/bin/env python3
"""p=14675, "Why did we choose that range for theta when doing trig
substitutions?". Three lost figures, and the post determines all three.

The argument is that a substitution must be invertible and must let the
surviving square root simplify without an absolute value. Each figure shows the
substituted function and the one that has to stay positive, with the usable
range shaded:

  sincos  "Let's look at the graph of sin(theta) (in red) and cos(theta) (in
          blue) to convince ourselves of that fact ... In the darker regions
          sin is one to one and cos is positive", for x = a sin(theta) and
          -pi/2 <= theta <= pi/2
  tansec  "For x = a tan(theta) we have -pi/2 < theta < pi/2", where the root
          is sqrt(1 + tan^2) = sec
  sectan  "And for x = a sec(theta) we have 0 <= theta < pi/2 or
          pi <= theta < 3pi/2", where the root is sqrt(sec^2 - 1) = |tan|

The filenames give the colour order: the substitution first, in red, then the
function that must be positive, in blue. Each is drawn at the 644x413 the
archive's resize parameters record.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, save, axes, check, paths_in

P = paths_in("p=14675.html")
PI = np.pi


def masked(f, x, jump=8.0):
    """Values with the asymptotic jumps of tan and sec cut out."""
    y = f(x)
    y = np.where(np.abs(y) > jump, np.nan, y)
    return y


def figure(dest, red, blue, red_lab, blue_lab, bands, title, ylim=(-4.2, 4.2),
           xr=(-2 * PI, 2 * PI)):
    x = np.linspace(*xr, 4000)
    fig, ax = plt.subplots(figsize=(6.44, 4.13))
    for lo, hi in bands:
        ax.axvspan(lo, hi, color="#dfe6ee", zorder=0)
    ax.plot(x, masked(red, x), color=RED, lw=2, label=red_lab)
    ax.plot(x, masked(blue, x), color=BLUE, lw=2, label=blue_lab)
    axes(ax, xr, ylim)
    # after axes(), which installs its own tick formatter in cross mode
    ax.set_xticks([-2 * PI, -3 * PI / 2, -PI, -PI / 2, 0, PI / 2, PI,
                   3 * PI / 2, 2 * PI])
    ax.set_xticklabels([r"$-2\pi$", r"$-\frac{3\pi}{2}$", r"$-\pi$",
                        r"$-\frac{\pi}{2}$", "", r"$\frac{\pi}{2}$", r"$\pi$",
                        r"$\frac{3\pi}{2}$", r"$2\pi$"])
    ax.legend(fontsize=11, frameon=False, loc="upper left",
              bbox_to_anchor=(1.01, 1.0))
    ax.set_title(title, fontsize=10)
    save(fig, dest)


figure(P["sincos.jpg"], np.sin, np.cos, r"$\sin\theta$", r"$\cos\theta$",
       [(-PI / 2, PI / 2)], ylim=(-1.6, 1.6),
       title=r"$x=a\sin\theta$: shaded, $\sin$ is one to one and $\cos\theta\geq0$")
figure(P["tansec.jpg"], np.tan, lambda t: 1 / np.cos(t), r"$\tan\theta$",
       r"$\sec\theta$", [(-PI / 2, PI / 2)],
       title=r"$x=a\tan\theta$: shaded, $\tan$ is one to one and $\sec\theta>0$")
figure(P["sectan.jpg"], lambda t: 1 / np.cos(t), np.tan, r"$\sec\theta$",
       r"$\tan\theta$", [(0, PI / 2), (PI, 3 * PI / 2)],
       title=r"$x=a\sec\theta$: shaded, $\sec$ is one to one and $\tan\theta\geq0$")

# --- what the post asserts ------------------------------------------------
print("  p=14675 checks:")
t = np.linspace(-PI / 2 + 1e-6, PI / 2 - 1e-6, 4001)
check("sin is one to one on [-pi/2, pi/2] (post)",
      bool(np.all(np.diff(np.sin(t)) > 0)), True)
check("  ... and cos is positive there, so sqrt(cos^2) = cos (post)",
      bool(np.all(np.cos(t) > 0)), True)
check("the other candidate range [pi/2, 3pi/2] is invertible too (post)",
      bool(np.all(np.diff(np.sin(np.linspace(PI / 2, 3 * PI / 2, 4001))) < 0)),
      True)
check("  ... but cos is negative on it, which is why it is rejected (post)",
      bool(np.all(np.cos(np.linspace(PI / 2 + 1e-6, 3 * PI / 2 - 1e-6, 401))
                  < 0)), True)
check("tan is one to one on (-pi/2, pi/2) (post)",
      bool(np.all(np.diff(np.tan(t)) > 0)), True)
check("  ... and sec is positive there, so sqrt(1+tan^2) = sec (post)",
      bool(np.all(1 / np.cos(t) > 0)), True)
u = np.concatenate([np.linspace(0, PI / 2 - 1e-6, 2001),
                    np.linspace(PI, 3 * PI / 2 - 1e-6, 2001)])
check("sec is one to one on [0,pi/2) and on [pi,3pi/2) (post): strictly "
      "monotone on each branch, rising on the first and falling on the second",
      bool(np.all(np.diff(1 / np.cos(u[:2001])) > 0)
           and np.all(np.diff(1 / np.cos(u[2001:])) < 0)), True)
check("  ... and tan >= 0 on both, so sqrt(sec^2-1) = tan (post)",
      bool(np.all(np.tan(u) >= -1e-12)), True)
check("  ... the two branches do not overlap in sec's values",
      bool(np.all(1 / np.cos(u[:2001]) >= 1)
           and np.all(1 / np.cos(u[2001:]) <= -1)), True)
print("  p=14675: 3 figures written")
