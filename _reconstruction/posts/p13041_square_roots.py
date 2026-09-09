#!/usr/bin/env python3
"""p=13041, "Square roots: in your head".

Two lost figures. 11.png survives on this post and is plainly old-default
matplotlib (boxed axes, a red line through round markers, "Error of square root
approximations"), which fits: the author says "I wrote some Python code". Its
two siblings are drawn in that same style rather than this project's usual one.

  22.png      "let's compare the accuracy of these methods", the forward method
              against the backward one
  linear.png  "we're drawing the tangent line to the square root curve at a
              point, and then approximating its neighbours using the tangent
              line instead of the curve"

The surviving figure also pins the forward method's definition: for n, take the
largest perfect square k^2 below it and add (n - k^2)/(2k). Its visible peaks
match that exactly, 0.268 at n=3 and 0.127 at n=15, which is checked below.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import numpy as np
import matplotlib.pyplot as plt
from figstyle import save, check, paths_in

P = paths_in("p=13041.html")
CLASSIC = {"axes.grid": False, "axes.spines.top": True,
           "axes.spines.right": True, "font.size": 12,
           "xtick.direction": "in", "ytick.direction": "in",
           "xtick.top": True, "ytick.right": True}


def forward(n):
    k = math.isqrt(n)
    return k + (n - k * k) / (2 * k) if k else float("nan")


def backward(n):
    k = math.isqrt(n)
    if k * k != n:
        k += 1
    return k - (k * k - n) / (2 * k)


N = np.arange(1, 101)
ef = np.array([abs(forward(int(n)) - math.sqrt(n)) for n in N])
eb = np.array([abs(backward(int(n)) - math.sqrt(n)) for n in N])

# --- 22.png: the two methods compared ------------------------------------
with plt.rc_context(CLASSIC):
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.plot(N, ef, "-o", color="red", ms=3.4, lw=1.0, label="forward")
    ax.plot(N, eb, "-o", color="blue", ms=3.4, lw=1.0, label="backward")
    ax.set_xlabel("Square root input")
    ax.set_ylabel("Error")
    ax.set_title("Error of square root approximations, both directions")
    ax.set_xlim(0, 100)
    ax.legend(loc="upper right", frameon=False)
    save(fig, P["22.png"])

# --- linear.png: the tangent line to sqrt(x) at a perfect square ---------
with plt.rc_context(CLASSIC):
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    x = np.linspace(20, 56, 500)
    ax.plot(x, np.sqrt(x), color="red", lw=2, label=r"$\sqrt{x}$")
    a = 36.0
    ax.plot(x, math.sqrt(a) + (x - a) / (2 * math.sqrt(a)), color="blue",
            lw=1.6, ls="--", label="tangent at $x=36$")
    ax.plot([a], [math.sqrt(a)], "o", color="black", ms=6)
    ax.plot([40], [forward(40)], "o", color="blue", ms=7)
    ax.plot([40], [math.sqrt(40)], "o", color="red", ms=7)
    ax.annotate(r"$\sqrt{40}\approx 6\frac{1}{3}$", (40, forward(40)),
                textcoords="offset points", xytext=(10, -4), fontsize=11,
                color="blue")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("the trick is a tangent-line approximation")
    ax.legend(loc="upper left", frameon=False)
    save(fig, P["linear.png"])

# --- the post's own numbers ----------------------------------------------
print("  p=13041 checks:")
check("sqrt(40) forward gives 6+1/3 (post)", forward(40), 6 + 1 / 3)
check("  ... which is 6.33 to 2 dp, against the true 6.32 (post)",
      (round(forward(40), 2), round(math.sqrt(40), 2)), (6.33, 6.32))
check("sqrt(96) backward gives 9.80 (post)", backward(96), 9.8)
check("  ... which is the true value to 2 dp (post)",
      round(math.sqrt(96), 2), 9.8)
check("the surviving figure's peak at n=3 is 0.268", round(float(ef[2]), 3),
      0.268)
check("  ... and at n=15 is 0.127", round(float(ef[14]), 3), 0.127)
check("the error is zero at perfect squares (post)",
      float(max(ef[k * k - 1] for k in range(1, 11))), 0.0, tol=1e-12)
check("bigger numbers approximate better (post)",
      float(ef[N > 60].max()) < float(ef[N < 20].max()), True)
check("sqrt(3) is the worst case (post)", int(N[ef.argmax()]), 3)
check("the forward method is the tangent line at the perfect square below",
      forward(40), math.sqrt(36) + (40 - 36) / (2 * math.sqrt(36)))
check("backward beats forward for 96, which is near the square above (post)",
      abs(backward(96) - math.sqrt(96)) < abs(forward(96) - math.sqrt(96)),
      True)
print("  p=13041: 2 figures written")
