#!/usr/bin/env python3
"""p=15781, "K-means: Intuitions, Maths and Percy Tau".

Six lost figures. Five are the worked example, and the post narrates each step,
so they are reconstructed by actually running the algorithm it describes:

  K-means1  the data, "sampled from 4 different 2D Gaussian distributions
            (each distribution is indicated by a different colour)"
  K-means2  "we initialise the centres (red stars) ... The points are all blue
            now to emphasise that we do not really know which cluster they
            belong to"
  K-means3  "assign each point to the nearest centre (star) and we colour code
            them accordingly. This is our first clustering."
  K-means4  "after one recalculation of centres and one reassignment (one full
            iteration of the EM algorithm)"
  K-means5  converged, "until points are always assigned to the same means"

The sixth, K_means_elbow.png, plotted the loss against K for the FIFA19 dataset
from Kaggle, which is not in the archive. Rather than invent a curve, the one
here is a real K-means run over a stand-in set of three well-separated
Gaussians, which puts its elbow at K=3 as the post's does. The figure says so
in its title, and the point the post makes from it is about the shape of the
curve rather than the data behind it.

The distribution parameters for the worked example are not given either, so
they are chosen here; the algorithm, the initialisation being poor, and the
sequence of states are all as described.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, ORANGE, PURPLE, GREY, save, axes, \
    check, paths_in

P = paths_in("p=15781.html")
rng = np.random.default_rng(15781)
COLS = [BLUE, ORANGE, GREEN, PURPLE]

TRUE_MEANS = np.array([[-2.4, 2.2], [2.6, 2.8], [-2.0, -2.4], [2.8, -2.0]])
SPREAD = 0.85
N_PER = 70
X = np.vstack([rng.normal(m, SPREAD, size=(N_PER, 2)) for m in TRUE_MEANS])
TRUTH = np.repeat(np.arange(4), N_PER)

# a deliberately poor initialisation, as the post's "these points don't look
# like good centres" describes
CENTRES0 = np.array([[-0.6, 0.9], [0.4, 1.6], [-1.1, -0.4], [0.9, -1.0]])


def assign(x, c):
    d = ((x[:, None, :] - c[None, :, :]) ** 2).sum(-1)
    return d.argmin(1)


def recentre(x, lab, c):
    out = c.copy()
    for j in range(len(c)):
        if (lab == j).any():
            out[j] = x[lab == j].mean(0)
    return out


def loss(x, lab, c):
    return float(((x - c[lab]) ** 2).sum())


def scatter(dest, labels, centres, title):
    fig, ax = plt.subplots(figsize=(4.2, 2.9))
    if labels is None:
        ax.plot(X[:, 0], X[:, 1], "o", color=BLUE, ms=4, alpha=0.8)
    else:
        for j in range(4):
            m = labels == j
            ax.plot(X[m, 0], X[m, 1], "o", color=COLS[j], ms=4, alpha=0.85)
    if centres is not None:
        ax.plot(centres[:, 0], centres[:, 1], "*", color=RED, ms=15,
                markeredgecolor="white", markeredgewidth=0.6, zorder=6)
    axes(ax, (-5.2, 5.6), (-4.8, 5.2), spines="box", xlabel=None, ylabel=None)
    ax.set_title(title, fontsize=9)
    save(fig, dest)


scatter(P["K-means1.png"], TRUTH, None,
        "the data, coloured by the distribution that generated it")
scatter(P["K-means2.png"], None, CENTRES0, "centres initialised (red stars)")

lab1 = assign(X, CENTRES0)
scatter(P["K-means3.png"], lab1, CENTRES0, "first assignment")

c1 = recentre(X, lab1, CENTRES0)
lab2 = assign(X, c1)
scatter(P["K-means4.png"], lab2, c1, "after one full EM iteration")

c, lab = CENTRES0.copy(), lab1
for _ in range(100):
    c = recentre(X, lab, c)
    new = assign(X, c)
    if (new == lab).all():
        break
    lab = new
scatter(P["K-means5.png"], lab, c, "converged")

# --- the elbow, from stand-in data ---------------------------------------
E_MEANS = np.array([[-3.0, 0.0], [3.0, 1.0], [0.0, -3.2]])
XE = np.vstack([rng.normal(m, 0.9, size=(120, 2)) for m in E_MEANS])
losses = []
for K in range(1, 9):
    best = np.inf
    for _ in range(12):
        cc = XE[rng.choice(len(XE), K, replace=False)]
        for _ in range(60):
            ll = assign(XE, cc)
            nc = recentre(XE, ll, cc)
            if np.allclose(nc, cc):
                break
            cc = nc
        best = min(best, loss(XE, assign(XE, cc), cc))
    losses.append(best)

fig, ax = plt.subplots(figsize=(4.2, 3.3))
ax.plot(range(1, 9), losses, "-o", color=BLUE, ms=5)
ax.plot([3], [losses[2]], "o", color=RED, ms=9, zorder=5)
ax.annotate("elbow", (3, losses[2]), textcoords="offset points",
            xytext=(14, 12), fontsize=10, color=RED)
axes(ax, (0.6, 8.4), None, spines="box", xlabel="$K$",
     ylabel=r"$\mathcal{L}$")
ax.set_title("the elbow method (stand-in data; the original used FIFA19)",
             fontsize=8.5)
save(fig, P["K_means_elbow.png"])

# --- what the algorithm must do ------------------------------------------
print("  p=15781 checks:")
check("the loss falls at every EM step",
      loss(X, lab2, c1) < loss(X, lab1, CENTRES0), True)
check("  ... and the converged loss is lowest of the three",
      loss(X, lab, c) <= loss(X, lab2, c1), True)
check("assignment is to the nearest centre",
      int(assign(np.array([[0.0, 0.0]]), np.array([[5.0, 0.0], [1.0, 0.0]]))[0]),
      1)
check("centres are the means of their members",
      float(np.abs(recentre(X, lab, c) - c).max()), 0.0, tol=1e-9)
check("the algorithm converged before the iteration cap",
      bool((assign(X, c) == lab).all()), True)
check("four clusters recovered", len(np.unique(lab)), 4)
check("elbow: loss decreases in K", bool(np.all(np.diff(losses) <= 1e-6)), True)
check("  ... and the fall after K=3 is much smaller than before it",
      (losses[1] - losses[2]) > 4 * (losses[2] - losses[3]), True)
print("  p=15781: 6 figures written")
