#!/usr/bin/env python3
"""MAM1000 parts 19 and 21, polynomial approximations. Two lost figures.

p=11150:
  quintapprox  "we can see something interesting when we plot the different
               levels of the approximation" of (1+x)^5, meaning the successive
               truncations of its binomial expansion. The post checks its own
               claim numerically first: (1+10^-2)^5 = 1.05101 against the
               two-term approximation 1+5x = 1.05.

p=11203:
  allexp       "how the first six terms in the Maclaurin polynomial add up to
               get a function which is a better and better approximation of the
               exponential function", so the partial sums of sum x^i/i! for
               n = 0 to 5.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, SERIES, save, axes, check, paths_in

P19 = paths_in("p=11150.html")
P21 = paths_in("p=11203.html")
BINOM = [math.comb(5, k) for k in range(6)]      # 1, 5, 10, 10, 5, 1

# --- quintapprox: (1+x)^5 and its truncations ---------------------------
fig, ax = plt.subplots(figsize=(6.6, 4.0))
x = np.linspace(-1.0, 1.0, 700)
ax.plot(x, (1 + x) ** 5, color="black", lw=2.6, label=r"$(1+x)^5$")
for n in range(1, 5):
    y = sum(BINOM[k] * x ** k for k in range(n + 1))
    ax.plot(x, y, color=SERIES[(n - 1) % len(SERIES)], lw=1.8,
            label=f"first {n + 1} terms")
axes(ax, (-1.0, 1.0), (-1.0, 6.0), xlabel=None, ylabel=None)
ax.legend(fontsize=9, frameon=False, loc="upper left")
save(fig, P19["quintapprox.png"])

# --- allexp: partial sums of the exponential series ---------------------
fig, ax = plt.subplots(figsize=(7.4, 4.7))
x = np.linspace(-3, 3, 800)
ax.plot(x, np.exp(x), color="black", lw=2.6, label=r"$e^x$")
for n in range(6):
    y = sum(x ** i / math.factorial(i) for i in range(n + 1))
    ax.plot(x, y, color=SERIES[n % len(SERIES)], lw=1.6, label=f"$n={n}$")
axes(ax, (-3, 3), (-2.0, 8.0), xlabel=None, ylabel=None)
ax.legend(fontsize=9, frameon=False, loc="upper left", ncol=2)
save(fig, P21["allexp.png"])

# --- the post's own numbers ----------------------------------------------
print("  p=11150 / p=11203 checks:")
check("(1+10^-2)^5 (post: 1.05101)", round((1 + 1e-2) ** 5, 5), 1.05101)
check("the two-term approximation 1+5x there (post: 1.05)", 1 + 5 * 1e-2,
      1.05)
check("binomial coefficients of (1+x)^5", BINOM, [1, 5, 10, 10, 5, 1])
check("the full expansion reproduces (1+x)^5 exactly",
      float(max(abs(sum(BINOM[k] * t ** k for k in range(6)) - (1 + t) ** 5)
                for t in np.linspace(-1, 1, 200))), 0.0, tol=1e-12)
prev = None
for n in range(1, 6):
    err = float(max(abs(sum(BINOM[k] * t ** k for k in range(n + 1))
                        - (1 + t) ** 5) for t in np.linspace(-0.3, 0.3, 200)))
    if prev is not None:
        check(f"  adding term {n} improves the (1+x)^5 fit near 0",
              err < prev, True)
    prev = err
check("smaller x gives a better approximation (post's other claim)",
      abs((1 + 0.001) ** 5 - (1 + 5 * 0.001))
      < abs((1 + 0.1) ** 5 - (1 + 5 * 0.1)), True)
prev = None
for n in range(6):
    err = float(max(abs(sum(t ** i / math.factorial(i) for i in range(n + 1))
                        - np.exp(t)) for t in np.linspace(-2, 2, 200)))
    if prev is not None:
        check(f"  the exponential partial sum improves at n={n}", err < prev,
              True)
    prev = err
print("  p=11150 / p=11203: 2 figures written")
