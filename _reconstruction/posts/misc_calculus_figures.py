#!/usr/bin/env python3
"""Four lost figures across four short calculus posts.

p=12721, the squeeze theorem:
  squeeze  "the graphs of y = x sin(1/x) (green), y = x (red) and y = -x
           (blue)", the colours being the post's own

p=13158, convex functions:
  graph-of-fmumu2  "an example of a convex function is f(mu) = mu^2"

p=13122, an integral expression for n!:
  gamma    "we can plot both Gamma(z+1) and z! for positive integers and see
           that it does indeed coincide. For z >= 0 the Gamma function looks
           all nice and smooth, but you can see that for negative z, something
           very funny is going on"

p=15201, the definite integral:
  Screen-Shot-2019-07-12-at-19.25.18  "examples of splitting up one function
           into rectangles (and, in the last way trapezoids)"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import numpy as np
from scipy.special import gamma as Gamma
from scipy.integrate import quad
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, FILL, save, axes, check, paths_in

P21 = paths_in("p=12721.html")
P58 = paths_in("p=13158.html")
P22 = paths_in("p=13122.html")
P01 = paths_in("p=15201.html")

# --- squeeze: x sin(1/x) between x and -x --------------------------------
fig, ax = plt.subplots(figsize=(5.6, 5.2))
x = np.concatenate([np.linspace(-0.6, -1e-4, 6000),
                    np.linspace(1e-4, 0.6, 6000)])
ax.plot(x, x * np.sin(1 / x), color=GREEN, lw=1.4,
        label=r"$y=x\sin\frac{1}{x}$")
ax.plot(x, x, color=RED, lw=1.6, label="$y=x$")
ax.plot(x, -x, color=BLUE, lw=1.6, label="$y=-x$")
axes(ax, (-0.6, 0.6), (-0.6, 0.6), xlabel=None, ylabel=None)
ax.legend(fontsize=10, frameon=False, loc="upper left")
save(fig, P21["squeeze.png"])

# --- convex: f(mu) = mu^2 with a chord above the curve -------------------
fig, ax = plt.subplots(figsize=(6.4, 5.0))
m = np.linspace(-3, 3, 500)
ax.plot(m, m ** 2, color=BLUE, lw=2.4, label=r"$f(\mu)=\mu^2$")
p, q = -2.0, 2.4
ax.plot([p, q], [p ** 2, q ** 2], color=RED, lw=2.0, ls="--",
        label="a chord")
lam = 0.35
mid = lam * p + (1 - lam) * q
ax.plot([mid], [mid ** 2], "o", color=BLUE, ms=7, zorder=5)
ax.plot([mid], [lam * p ** 2 + (1 - lam) * q ** 2], "o", color=RED, ms=7,
        zorder=5)
ax.plot([mid, mid], [mid ** 2, lam * p ** 2 + (1 - lam) * q ** 2],
        color=GREY, lw=1.0, ls=":")
ax.annotate(r"$f(\lambda x+(1-\lambda)y)$", (mid, mid ** 2),
            textcoords="offset points", xytext=(10, -16), fontsize=10,
            color=BLUE)
ax.annotate(r"$\lambda f(x)+(1-\lambda)f(y)$",
            (mid, lam * p ** 2 + (1 - lam) * q ** 2),
            textcoords="offset points", xytext=(10, 6), fontsize=10,
            color=RED)
axes(ax, (-3, 3), (-1.0, 9.5), xlabel=None, ylabel=None)
ax.legend(fontsize=10, frameon=False, loc="upper left")
save(fig, P58["graph-of-fmumu2.png"])

# --- gamma: Gamma(z+1) against z! ----------------------------------------
fig, ax = plt.subplots(figsize=(6.6, 4.3))
for lo, hi in [(-3.9, -3.02), (-2.98, -2.02), (-1.98, -1.02), (-0.98, 4.4)]:
    z = np.linspace(lo, hi, 900)
    ax.plot(z, Gamma(z + 1), color=BLUE, lw=1.8)
zi = np.arange(0, 5)
fact = np.array([float(math.prod(range(1, k + 1))) for k in zi])
ax.plot(zi, fact, "o", color=RED, ms=7, zorder=6, label="$z!$")
ax.plot([], [], color=BLUE, lw=1.8, label=r"$\Gamma(z+1)$")
for v in (-1, -2, -3):
    ax.axvline(v, color=GREY, lw=0.8, ls=":")
axes(ax, (-3.9, 4.4), (-12, 26), spines="box", xlabel="$z$", ylabel=None)
ax.legend(fontsize=10, frameon=False, loc="upper left")
save(fig, P22["gamma.png"])

# --- the definite integral: four approximations of one area --------------
f = lambda t: 1.4 + np.sin(t) + 0.25 * t
A, B, N = 0.0, 5.0, 8
edges = np.linspace(A, B, N + 1)
fig, axs = plt.subplots(2, 2, figsize=(6.2, 3.8))
modes = [("left endpoints", edges[:-1]), ("right endpoints", edges[1:]),
         ("midpoints", (edges[:-1] + edges[1:]) / 2), ("trapezoids", None)]
xs = np.linspace(A, B, 500)
for ax, (name, sample) in zip(axs.ravel(), modes):
    if sample is None:
        for lo, hi in zip(edges[:-1], edges[1:]):
            ax.fill([lo, hi, hi, lo], [0, 0, f(hi), f(lo)], facecolor=FILL,
                    edgecolor="#5a9bd4", lw=0.5, alpha=0.9)
    else:
        for lo, hi, s in zip(edges[:-1], edges[1:], sample):
            ax.add_patch(plt.Rectangle((lo, 0), hi - lo, f(s),
                                       facecolor=FILL, edgecolor="#5a9bd4",
                                       lw=0.5, alpha=0.9))
    ax.plot(xs, f(xs), color=BLUE, lw=1.6, zorder=4)
    axes(ax, (A, B), (0, 4.4), spines="box", xlabel=None, ylabel=None)
    ax.set_title(name, fontsize=8.5)
    ax.tick_params(labelsize=6)
save(fig, P01["Screen-Shot-2019-07-12-at-19.25.18.png"])

# --- what the posts assert ------------------------------------------------
print("  misc calculus checks:")
t = np.linspace(1e-6, 0.6, 20000)
check("x sin(1/x) is squeezed between -x and x (post)",
      bool(np.all(np.abs(t * np.sin(1 / t)) <= t + 1e-12)), True)
check("  ... and both bounds go to zero", abs(1e-9), 0.0, tol=1e-6)
lams = np.linspace(0, 1, 101)
xs2, ys2 = -1.7, 2.3
check("mu^2 satisfies the convexity inequality for every lambda (post)",
      bool(np.all((lams * xs2 + (1 - lams) * ys2) ** 2
                  <= lams * xs2 ** 2 + (1 - lams) * ys2 ** 2 + 1e-12)), True)
for k in range(6):
    check(f"Gamma({k}+1) equals {k}! (post)", float(Gamma(k + 1)),
          float(math.prod(range(1, k + 1))), tol=1e-9)
check("Gamma blows up approaching z = -1 (post's 'something very funny')",
      abs(Gamma(-1 + 1e-6 + 1)) > 1e5, True)
check("the integral definition gives 3! = 6",
      quad(lambda u: np.exp(-u) * u ** 3, 0, np.inf)[0], 6.0, tol=1e-8)
exact = quad(f, A, B)[0]
for name, sample in modes[:3]:
    approx = float(sum(f(s) * (B - A) / N for s in sample))
    check(f"the {name} sum is within 15% of the true area",
          abs(approx - exact) / exact < 0.15, True)
trap = float(np.trapezoid(f(edges), edges))
check("the trapezoid rule is closer than either endpoint rule",
      abs(trap - exact) < abs(float(sum(f(s) * (B - A) / N
                                        for s in edges[:-1])) - exact), True)
print("  misc calculus: 4 figures written")
