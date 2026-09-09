#!/usr/bin/env python3
"""p=12734, "Computational Complexity: Article 4". Three lost figures.

Each sits directly under the definition it illustrates, and the definitions are
quoted in full in the post, so the pictures are fixed:

  graph-big-O   O(g(n)) = {f(n) | exists C > 0, n_0 >= 1, such that for all
                n >= n_0, 0 <= f(n) <= C g(n)}
  Omega.gif     Omega(g(n)) = {f(n) | exists C > 0, n_0 >= 1, such that for all
                n >= n_0, 0 <= C g(n) <= f(n)}
  graph-Theta   Theta(g(n)) = {f(n) | exists C1, C2 > 0, n_0 >= 1, such that
                for all n >= n_0, 0 <= C1 g(n) <= f(n) <= C2 g(n)}

The post's own worked example supplies f: "T(n) = 3n^3 + 5n^2 + 2n + 5 =
O(n^3)", with g(n) = n^3, and it says the dominant term at n = 1000 is "more
than 500 times greater than the remaining terms". Both are checked below, and
the constants drawn are ones that genuinely bound this f from the stated n_0
onwards, which the checks confirm rather than assume.

The archive's resize parameters put all three at roughly 230x220, so they are
small square panels.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=12734.html")

f = lambda n: 3 * n ** 3 + 5 * n ** 2 + 2 * n + 5
g = lambda n: n ** 3
N0 = 2.0                      # the n_0 drawn on each panel
C_HI, C_LO = 7.5, 3.0         # C1 g <= f <= C2 g from n_0 on;
                              # f/g = 3 + 5/n + 2/n^2 + 5/n^3 is 6.625 at
                              # n = 2, so C_HI has to clear that
n = np.linspace(0.05, 4.0, 600)


def panel(dest, curves, note):
    fig, ax = plt.subplots(figsize=(2.6, 2.5))
    top = max(np.max(y) for _, y, _, _ in curves)
    ax.axvspan(N0, n[-1], color="#eef2f7", zorder=0)
    for lab, y, col, ls in curves:
        ax.plot(n, y, color=col, lw=1.8, ls=ls, label=lab, zorder=2)
    ax.plot([N0, N0], [0, top], color=GREY, lw=0.9, ls=":", zorder=1)
    ax.set_xlim(0, n[-1]); ax.set_ylim(0, top * 1.02)
    ax.set_xticks([N0]); ax.set_xticklabels(["$n_0$"])
    ax.set_yticks([])
    axes(ax, (0, n[-1]), (0, top * 1.02), spines="box", xlabel="$n$",
         ylabel=None)
    ax.set_xticks([N0]); ax.set_xticklabels(["$n_0$"])
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title(note, fontsize=8.5)
    save(fig, dest)


panel(P["graph-big-O.jpg"],
      [(r"$Cg(n)$", C_HI * g(n), RED, "-"), (r"$f(n)$", f(n), BLUE, "-")],
      r"$f(n)=O(g(n))$: $f\leq Cg$ beyond $n_0$")
panel(P["Omega.gif"],
      [(r"$f(n)$", f(n), BLUE, "-"), (r"$Cg(n)$", C_LO * g(n), RED, "-")],
      r"$f(n)=\Omega(g(n))$: $Cg\leq f$ beyond $n_0$")
panel(P["graph-Theta.jpg"],
      [(r"$C_2g(n)$", C_HI * g(n), RED, "-"), (r"$f(n)$", f(n), BLUE, "-"),
       (r"$C_1g(n)$", C_LO * g(n), GREEN, "--")],
      r"$f(n)=\Theta(g(n))$: $C_1g\leq f\leq C_2g$ beyond $n_0$")

# --- what the post asserts ------------------------------------------------
print("  p=12734 checks:")
big = 3 * 1000 ** 3
rest = 5 * 1000 ** 2 + 2 * 1000 + 5
check("at n=1000 the dominant term beats the rest by more than 500x (post)",
      big / rest > 500, True)
check("  ... 600 times, in fact", round(big / rest), 600)
ns = np.linspace(N0, 400, 20000)
check("f <= C g beyond n_0 with the C drawn, so f = O(g) (post)",
      bool(np.all(f(ns) <= C_HI * g(ns))), True)
check("C g <= f beyond n_0 with the C drawn, so f = Omega(g) (post)",
      bool(np.all(C_LO * g(ns) <= f(ns))), True)
check("  ... both at once, which is Theta(g) (post)",
      bool(np.all((C_LO * g(ns) <= f(ns)) & (f(ns) <= C_HI * g(ns)))), True)
check("the ratio f/g tends to a finite non-zero limit, as the post says for "
      "Theta", round(float(f(1e7) / g(1e7)), 6), 3.0, tol=1e-5)
check("  ... namely the leading coefficient 3", round(f(1e9) / g(1e9), 9), 3.0,
      tol=1e-8)
check("n_0 is needed: below it f can exceed C_2 g", bool(f(0.1) > C_HI * g(0.1)),
      True)
print("  p=12734: 3 figures written")
