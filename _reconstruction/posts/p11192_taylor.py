#!/usr/bin/env python3
"""p=11192, "MAM1000 part 20 iii", approximating a function by polynomials.

Four lost figures, each showing f(x) = 2 sin x + cos(3x)/2 against a successive
Taylor approximation about x = 2.5:

  zerothapprox  the constant y = f(2.5), which the post gives as "about 1.37"
  firstapproxc  the tangent, f(2.5) + f'(2.5)(x-2.5), "the purple line"
  firstapproxb  the quadratic, with c_2 = f''(2.5)/2 as the post derives
  fourteenthb   the fourteenth-order polynomial

approxfunc.png survives on this post and is the same f plotted alone, so the
range and the style here are taken from it rather than chosen: x from 0 to 4, a
thick blue curve, Mathematica axes. The function is confirmed against it too:
f(0)=0.5, a peak of 2.31 near x=1.9, f(2.5)=1.370 exactly as the post says, a
zero just before x=2.93, and f(4)=-1.09, all of which the surviving plot shows.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import numpy as np
import matplotlib.pyplot as plt
from figstyle import PURPLE, save, axes, check, paths_in

P = paths_in("p=11192.html")
A = 2.5
BLUE_MMA = "#0000ff"          # the surviving figure uses a saturated blue


def f(x):
    return 2 * np.sin(x) + np.cos(3 * x) / 2


def deriv(n, x):
    """nth derivative of 2 sin x + cos(3x)/2, in closed form."""
    return (2 * np.sin(x + n * np.pi / 2)
            + 3 ** n / 2 * np.cos(3 * x + n * np.pi / 2))


def taylor(N, x):
    return sum(deriv(n, A) / math.factorial(n) * (x - A) ** n
               for n in range(N + 1))


def figure(N, dest, label):
    x = np.linspace(0, 4, 800)
    fig, ax = plt.subplots(figsize=(7.4, 4.7))
    ax.plot(x, f(x), color=BLUE_MMA, lw=2.6, zorder=3)
    ax.plot(x, taylor(N, x), color=PURPLE, lw=2.0, zorder=4)
    ax.plot([A], [f(A)], "o", color=PURPLE, ms=6, zorder=5)
    axes(ax, (0, 4), (-1.6, 2.6), xlabel=None, ylabel=None)
    ax.set_title(label, fontsize=11)
    save(fig, dest)


figure(0, P["zerothapprox.png"],
       r"$f(x)=2\sin x+\frac{\cos 3x}{2}$ and $y=f(2.5)$")
figure(1, P["firstapproxc.png"],
       r"... and $y=f(2.5)+f'(2.5)(x-2.5)$")
figure(2, P["firstapproxb.png"],
       r"... and the quadratic, matching $f''(2.5)=2c_2$")
figure(14, P["fourteenthb.png"], r"... and the 14th-order polynomial")

# --- the numbers the post states, and the ones its surviving figure shows -
print("  p=11192 checks:")
check("f(2.5) (post: about 1.37)", round(float(f(A)), 2), 1.37)
check("f(0) matches the surviving plot", round(float(f(0)), 2), 0.5)
check("the peak near x=1.9 matches it", round(float(f(1.9)), 2), 2.31)
check("f(4) matches it", round(float(f(4)), 2), -1.09)
check("zeroth approximation is constant",
      float(taylor(0, 0.0)), float(taylor(0, 4.0)))
check("  ... and equals f(2.5) there", float(taylor(0, 1.0)), float(f(A)))
check("first approximation has gradient f'(2.5)",
      float((taylor(1, A + 1e-6) - taylor(1, A - 1e-6)) / 2e-6),
      float(deriv(1, A)), tol=1e-5)
check("quadratic's second derivative is f''(2.5) (post: f''=2c_2)",
      float((taylor(2, A + 1e-4) - 2 * taylor(2, A) + taylor(2, A - 1e-4))
            / 1e-8), float(deriv(2, A)), tol=1e-3)
# The post's claim is about behaviour *close to* x=2.5, not globally: for this
# function the third derivative is large (3^3/2 in the cosine term), so the
# quadratic is actually worse than the tangent by x=2.8. Test what is claimed.
errs = [float(abs(taylor(N, A + 0.1) - f(A + 0.1))) for N in (0, 1, 2, 14)]
check("close to x=2.5, each order improves on the last",
      all(a > b for a, b in zip(errs, errs[1:])), True)
check("  ... and the 14th order is essentially exact there",
      errs[3] < 1e-12, True)
check("the 14th order stays excellent across the plotted range near 2.5",
      float(max(abs(taylor(14, x) - f(x))
                for x in np.linspace(1.5, 3.5, 200))) < 1e-3, True)
check("the quadratic is not uniformly better than the tangent far out, "
      "which is why the post says 'close to x=2.5'",
      abs(taylor(2, 3.0) - f(3.0)) > abs(taylor(1, 3.0) - f(3.0)), True)
print("  p=11192: 4 figures written")
