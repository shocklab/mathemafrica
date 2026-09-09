#!/usr/bin/env python3
"""p=16848, "Parrondos Paradox".

Seven lost figures. Five are histograms of final wealth over "1000 gambles of
length 50000", with every parameter given in the text: M=3, p=0.495,
p12=0.745, p3=0.095, starting wealth 99. The strategies are Game A alone, Game
B alone, the cycle BBABA, the cycle AABB, and switching randomly with equal
probability.

The other two are the Markov chain diagrams the text captions "Markov Chain for
Game B" and "Markov Chain for Switching randomly between A and B". Their
recorded shapes, 300x87 and 300x73, are wide and short, which is a linear chain
of the seven states -3..3 the text describes, with 3 and -3 absorbing.

The post's arithmetic has one typo, "q_3 = 0.5*495 + 0.5*0.095", which is
plainly 0.495; the value 0.295 it then quotes confirms that reading.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=16848.html")
M, p, p12, p3 = 3, 0.495, 0.745, 0.095
START, RUNS, STEPS = 99, 1000, 50000
rng = np.random.default_rng(16848)


def simulate(pattern):
    """pattern: a string of A/B repeated, or None for a random 50/50 choice."""
    w = np.full(RUNS, START, dtype=np.int64)
    for t in range(STEPS):
        if pattern is None:
            use_b = rng.random(RUNS) < 0.5
        else:
            use_b = np.full(RUNS, pattern[t % len(pattern)] == "B")
        prob = np.where(use_b, np.where(w % M == 0, p3, p12), p)
        w += np.where(rng.random(RUNS) < prob, 1, -1)
    return w


CASES = [("wealth-A.png", "A", "Strategy A"),
         ("wealth-B.png", "B", "Strategy B"),
         ("wealth-BBABA.png", "BBABA", "Strategy BBABA"),
         ("wealth-AABB.png", "AABB", "Strategy AABB"),
         ("wealth-random.png", None, "Switching randomly")]

finals = {}
for name, pattern, title in CASES:
    w = simulate(pattern)
    finals[name] = w
    fig, ax = plt.subplots(figsize=(4.2, 3.3))
    ax.hist(w, bins=40, color=BLUE, alpha=0.85, edgecolor="white", lw=0.4)
    ax.axvline(START, color=RED, lw=1.4, ls="--")
    ax.text(START, ax.get_ylim()[1] * 0.96, " starting wealth", fontsize=8,
            color=RED, va="top")
    axes(ax, None, None, xlabel="final wealth", ylabel="count", spines="box")
    ax.set_title(f"{title}: median {np.median(w):.0f}", fontsize=10)
    save(fig, P[name])


# --- the two Markov chains ------------------------------------------------
def chain(dest, up_at_0, up_elsewhere, labels, title):
    states = list(range(-3, 4))
    fig, ax = plt.subplots(figsize=(6.2, 1.8))
    for s in states:
        absorbing = abs(s) == 3
        ax.add_patch(plt.Circle((s, 0), 0.26, facecolor="white",
                                edgecolor=RED if absorbing else BLUE,
                                lw=1.6, zorder=3))
        ax.text(s, 0, f"${s}$", ha="center", va="center", fontsize=9,
                zorder=4)
    for s in states:
        if abs(s) == 3:
            ax.annotate("", xy=(s, 0.30), xytext=(s + 0.34, 0.62),
                        arrowprops=dict(arrowstyle="->", color=RED, lw=1.1,
                                        connectionstyle="arc3,rad=-1.6"))
            ax.text(s, 0.80, "$1$", ha="center", fontsize=8, color=RED)
            continue
        pu = up_at_0 if s == 0 else up_elsewhere
        ax.annotate("", xy=(s + 0.74, 0.06), xytext=(s + 0.26, 0.06),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
        ax.annotate("", xy=(s - 0.74, -0.06), xytext=(s - 0.26, -0.06),
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=1.1))
        if s in (0, 1):
            ax.text(s + 0.5, 0.20, labels[0] if s == 0 else labels[1],
                    ha="center", fontsize=8, color=GREEN)
            ax.text(s - 0.5, -0.34,
                    labels[2] if s == 0 else labels[3],
                    ha="center", fontsize=8, color=GREY)
    ax.set_xlim(-3.7, 3.7); ax.set_ylim(-0.7, 1.05)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(title, fontsize=9)
    save(fig, dest)


chain(P["Screenshot-2020-11-09-at-13.21.12.png"], p3, p12,
      ["$p_3$", "$p_{12}$", "$1-p_3$", "$1-p_{12}$"], "Game B")
chain(P["Screenshot-2020-11-09-at-13.21.16.png"],
      0.5 * p + 0.5 * p3, 0.5 * p + 0.5 * p12,
      ["$q_3$", "$q_{12}$", "$1-q_3$", "$1-q_{12}$"],
      "switching randomly between A and B")


# --- every number the post states ----------------------------------------
def z0(a, b):
    """Probability of reaching +3 before -3, the post's closed form."""
    return a * b ** 2 / ((1 - a) * (1 - b) ** 2 + a * b ** 2)


print("  p=16848 checks:")
check("crude estimate for game B (post: about 0.53)",
      round(1 / 3 * p3 + 2 / 3 * p12, 2), 0.53)
check("z0 for game B (post: about 0.47)", round(z0(p3, p12), 2), 0.47)
check("  ... so game B is losing", z0(p3, p12) < 0.5, True)
check("q12 (post: 0.62)", 0.5 * p + 0.5 * p12, 0.62)
check("q3 (post: 0.295, its '0.5*495' being a typo for 0.495)",
      0.5 * p + 0.5 * p3, 0.295)
check("z0 when switching randomly (post: about 0.53)",
      round(z0(0.5 * p + 0.5 * p3, 0.5 * p + 0.5 * p12), 2), 0.53)
check("  ... so random switching wins",
      z0(0.5 * p + 0.5 * p3, 0.5 * p + 0.5 * p12) > 0.5, True)
check("game A alone loses in simulation",
      float(np.median(finals["wealth-A.png"])) < START, True)
check("game B alone loses in simulation",
      float(np.median(finals["wealth-B.png"])) < START, True)
check("BBABA wins in simulation",
      float(np.median(finals["wealth-BBABA.png"])) > START, True)
check("AABB wins in simulation",
      float(np.median(finals["wealth-AABB.png"])) > START, True)
check("random switching wins in simulation",
      float(np.median(finals["wealth-random.png"])) > START, True)
print("  p=16848: 7 figures written")
