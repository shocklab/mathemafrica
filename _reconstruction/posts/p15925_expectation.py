#!/usr/bin/env python3
"""p=15925, "What did you expect? Some notes on the Expectation operator."

Five lost figures, all 300x163 as displayed and all built to the recipe the
post states outright: "the density/mass function for a random variable is
shown in black. The red function is the function over which we will integrate
in order to find the appropriate expectation ... The value of the expectation
is therefore the area under the red curve."

  Normal_mean       standard normal, g(x) = x
  Std_normal_x2     standard normal, g(x) = x^2
  Normal_x2         normal with standard deviation 2, g(x) = x^2
  Exponential_mean  exponential, lambda = 3, g(x) = x
  poisson_mean      Poisson, lambda = 4, g(x) = x, drawn as points because the
                    post says the expectation is "found by summing the
                    distances from the red points to the horizontal axis"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy import stats
from scipy.integrate import quad
import matplotlib.pyplot as plt
from figstyle import RED, GREY, save, axes, check, paths_in

P = paths_in("p=15925.html")
SIZE = (4.2, 2.3)          # 300x163 as displayed


def continuous(dens, g, lo, hi, dest, title, gl):
    x = np.linspace(lo, hi, 800)
    fig, ax = plt.subplots(figsize=SIZE)
    ax.plot(x, dens(x), color="black", lw=1.6, label="density")
    ax.plot(x, g(x) * dens(x), color=RED, lw=1.6, label=gl)
    ax.fill_between(x, 0, g(x) * dens(x), color=RED, alpha=0.16)
    axes(ax, (lo, hi), None)
    ax.legend(fontsize=7.5, frameon=False, loc="upper right")
    ax.set_title(title, fontsize=9)
    save(fig, dest)


phi = stats.norm(0, 1).pdf
phi2 = stats.norm(0, 2).pdf

continuous(phi, lambda x: x, -4, 4, P["Normal_mean.png"],
           r"standard normal, $g(x)=x$:  $\mathbb{E}[X]=0$", r"$x\,f(x)$")
continuous(phi, lambda x: x ** 2, -4, 4, P["Std_normal_x2.png"],
           r"standard normal, $g(x)=x^2$:  $\mathbb{E}[X^2]=1$",
           r"$x^2f(x)$")
continuous(phi2, lambda x: x ** 2, -8, 8, P["Normal_x2.png"],
           r"normal, $\sigma=2$, $g(x)=x^2$:  $\mathbb{E}[X^2]=4$",
           r"$x^2f(x)$")
continuous(stats.expon(scale=1 / 3).pdf, lambda x: x, 0, 2.5,
           P["Exponential_mean.png"],
           r"exponential, $\lambda=3$:  $\mathbb{E}[X]=\frac{1}{3}$",
           r"$x\,f(x)$")

# --- Poisson, lambda = 4 ---------------------------------------------------
k = np.arange(0, 16)
pmf = stats.poisson(4).pmf(k)
fig, ax = plt.subplots(figsize=SIZE)
ax.vlines(k, 0, pmf, color="black", lw=1.0)
ax.plot(k, pmf, "o", color="black", ms=3.4, label="mass")
ax.vlines(k + 0.14, 0, k * pmf, color=RED, lw=1.0)
ax.plot(k + 0.14, k * pmf, "o", color=RED, ms=3.4, label=r"$x\,p(x)$")
axes(ax, (-0.6, 15.6), None)
ax.legend(fontsize=7.5, frameon=False, loc="upper right")
ax.set_title(r"Poisson, $\lambda=4$:  $\mathbb{E}[X]=4$", fontsize=9)
save(fig, P["poisson_mean.png"])

# --- the numbers the post states ------------------------------------------
print("  p=15925 checks:")
check("standard normal mean is 0 (red area)",
      quad(lambda x: x * phi(x), -40, 40)[0], 0.0, tol=1e-8)
check("standard normal E[X^2] is 1",
      quad(lambda x: x ** 2 * phi(x), -40, 40)[0], 1.0, tol=1e-6)
check("sigma=2 gives E[X^2]=4, four times greater (post's claim)",
      quad(lambda x: x ** 2 * phi2(x), -60, 60)[0], 4.0, tol=1e-5)
check("exponential lambda=3 mean is 1/3 (post's opening example)",
      stats.expon(scale=1 / 3).mean(), 1 / 3)
check("Poisson lambda=4 mean is 4", stats.poisson(4).mean(), 4.0)
check("15*p(15) is negligible (post's closing point)",
      15 * stats.poisson(4).pmf(15) < 0.001, True)
check("sample mean of 70, 80, 90 (post: 80)", (70 + 80 + 90) / 3, 80)
check("entrance-fee example (post: 88)", 60 * 0.3 + 100 * 0.7, 88)
print("  p=15925: 5 figures written")
