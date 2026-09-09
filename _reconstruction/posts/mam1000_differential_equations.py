#!/usr/bin/env python3
"""Five lost figures across four MAM1000 differential-equations posts.

p=11454, the logistic equation:
  log        "what happens when you start with 2, 100, 1000, 5000, 200000 and
             500000 rabbits" at k=13 and a sustainable population of 10,000

p=11471, separable equations:
  allsol     y = sqrt(5 - 4 cos 2t), "along with a number of solutions with
             other initial conditions"
  twosols    y = ln(x^2 - 4x - 4) through (5,0), valid only on x > 2+2sqrt(2),
             "along with several other solutions"

p=11488, second-order equations:
  exptrig    "a few different particular solutions" of the equation whose roots
             give alpha = -1/2, beta = sqrt(3)/2, one of them being
             y = (1/3)e^{-x/2}(9 cos(sqrt(3)x/2) - sqrt(3) sin(sqrt(3)x/2))

p=11565:
  lorenz     the trajectory of the Lorenz system, "a rather beautiful pattern"

`allsol` and `log` both survive as WordPress's cropped 500x383 thumbnails, so
those two are drawn to match what the crops show rather than to taste: for
`allsol`, a heavy solid blue particular solution over a family of thin blue
dashed ones, both the positive and negative branches; for `log`, the six curves
against a P(t) axis with the two over-capacity starts entering from the top.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, SERIES, save, axes, check, paths_in

P54 = paths_in("p=11454.html")
P71 = paths_in("p=11471.html")
P88 = paths_in("p=11488.html")
P65 = paths_in("p=11565.html")

# --- log.png: the logistic equation --------------------------------------
K, M = 13.0, 10000.0
STARTS = [2, 100, 1000, 5000, 200000, 500000]


def logistic(t, p0):
    a = (M - p0) / p0
    return M / (1 + a * np.exp(-K * t))


fig, ax = plt.subplots(figsize=(6.4, 4.0))
t = np.linspace(0, 1, 800)
for p0, col in zip(STARTS, SERIES + [SERIES[0]]):
    ax.plot(t, logistic(t, p0), color=col, lw=1.8, label=f"$P_0={p0}$")
axes(ax, (0, 1), (0, 18000), spines="box", xlabel="$t$", ylabel="$P(t)$")
ax.axhline(M, color="#999999", lw=1.0, ls="--")
ax.annotate("$M=10000$", (0.82, M), textcoords="offset points",
            xytext=(0, 6), fontsize=9, color="#666666")
ax.legend(fontsize=8, frameon=False, ncol=2, loc="upper right")
save(fig, P54["log.png"])

# --- allsol.png: y = sqrt(c - 4 cos 2t) ----------------------------------
fig, ax = plt.subplots(figsize=(6.0, 3.8))
t = np.linspace(0, 9.2, 1400)
for c in (4.6, 5.8, 7.0, 8.4, 10.0, 12.0, 14.5):
    y = np.sqrt(np.maximum(c - 4 * np.cos(2 * t), 0))
    for s in (1, -1):
        ax.plot(t, s * y, color=BLUE, lw=0.9, ls="--", alpha=0.85)
yp = np.sqrt(5 - 4 * np.cos(2 * t))
ax.plot(t, yp, color=BLUE, lw=2.8)
axes(ax, (0, 9.2), (-4.6, 4.6), xlabel=None, ylabel=None)
save(fig, P71["allsol.png"])

# --- twosols.png: y = ln(x^2 - 4x + c) -----------------------------------
fig, ax = plt.subplots(figsize=(5.6, 3.7))
x = np.linspace(2, 12, 1400)
for c in (-10.0, -8.0, -4.0, 0.0, 3.0):
    inside = x ** 2 - 4 * x + c
    y = np.where(inside > 0, np.log(np.abs(inside)), np.nan)
    ax.plot(x, y, color=BLUE, lw=1.0, ls="--", alpha=0.85)
inside = x ** 2 - 4 * x - 4
yp = np.where(inside > 0, np.log(np.abs(inside)), np.nan)
ax.plot(x, yp, color=BLUE, lw=2.8)
ax.plot([5], [0], "o", color=RED, ms=7, zorder=6)
ax.annotate("$(5,0)$", (5, 0), textcoords="offset points", xytext=(8, -14),
            fontsize=10, color=RED)
axes(ax, (2, 12), (-3.0, 5.0), spines="box", xlabel="$x$", ylabel="$y$")
save(fig, P71["twosols.png"])

# --- exptrig.png: damped oscillations ------------------------------------
AL, BE = -0.5, np.sqrt(3) / 2


def sol(x, k1, k2):
    return np.exp(AL * x) * (k1 * np.cos(BE * x) + k2 * np.sin(BE * x))


fig, ax = plt.subplots(figsize=(6.2, 3.6))
x = np.linspace(0, 12, 900)
for (k1, k2), col in zip([(3.0, -np.sqrt(3) / 3), (2.0, 2.0), (-1.5, 1.0),
                          (0.0, 3.0)], SERIES):
    ax.plot(x, sol(x, k1, k2), color=col, lw=1.8,
            label=rf"$k_1={k1:g},\ k_2={k2:.2f}$")
axes(ax, (0, 12), (-2.4, 3.4), xlabel=None, ylabel=None)
ax.legend(fontsize=8, frameon=False, loc="upper right")
save(fig, P88["exptrig.png"])

# --- lorenz.png ----------------------------------------------------------
SIG, RHO, BET = 10.0, 28.0, 8 / 3


def lor(t, s):
    x, y, z = s
    return [SIG * (y - x), x * (RHO - z) - y, x * y - BET * z]


sol_l = solve_ivp(lor, (0, 60), [1.0, 1.0, 1.0], rtol=1e-9, atol=1e-11,
                  dense_output=True)
tt = np.linspace(0, 60, 40000)
X, Y, Z = sol_l.sol(tt)
fig = plt.figure(figsize=(4.6, 5.0))
ax = fig.add_subplot(projection="3d")
ax.plot(X, Y, Z, color=BLUE, lw=0.35)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.tick_params(labelsize=7)
ax.grid(False)
for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
    pane.pane.set_facecolor("white"); pane.pane.set_edgecolor("#c8c8c8")
ax.view_init(elev=22, azim=-62)
save(fig, P65["lorenz.png"])

# --- what the posts state -------------------------------------------------
print("  MAM1000 differential equations checks:")
for p0 in STARTS:
    check(f"logistic starts at P0={p0}", float(logistic(0.0, p0)), float(p0),
          tol=1e-6)
check("  ... and every start converges to M=10000",
      float(max(abs(logistic(3.0, p0) - M) for p0 in STARTS)) < 1e-6, True)
check("starts above M decrease (post's 200000 and 500000)",
      logistic(0.05, 500000) < 500000 and logistic(0.05, 200000) < 200000,
      True)
check("starts below M increase", logistic(0.05, 2) > 2, True)
check("allsol: the particular solution at t=0 is 1 (post's y(0)=1)",
      float(np.sqrt(5 - 4 * np.cos(0.0))), 1.0)
check("  ... and c=5 follows from 1 = sqrt(c-4) (post)", 1 ** 2 + 4, 5)
check("twosols: the particular solution passes through (5,0) (post)",
      float(np.log(5 ** 2 - 4 * 5 - 4)), 0.0)
check("  ... and is real only above 2+2sqrt(2) (post)",
      float(2 + 2 * np.sqrt(2)), float(np.roots([1, -4, -4]).max()))
check("exptrig: y(0)=3 for the post's particular solution",
      float(sol(0.0, 3.0, -np.sqrt(3) / 3)), 3.0)
d = (sol(1e-6, 3.0, -np.sqrt(3) / 3) - sol(-1e-6, 3.0, -np.sqrt(3) / 3)) / 2e-6
check("  ... and y'(0) = -2 (post)", float(d), -2.0, tol=1e-6)
check("  ... alpha = -1/2 and beta = sqrt(3)/2 (post)", (AL, round(BE, 6)),
      (-0.5, round(np.sqrt(3) / 2, 6)))
check("lorenz: the trajectory stays bounded", float(np.abs(Z).max()) < 100,
      True)
check("  ... and is not periodic, revisiting neither lobe on a fixed period",
      float(np.std(X)) > 5, True)
print("  MAM1000 differential equations: 5 figures written")
