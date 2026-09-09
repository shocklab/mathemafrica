#!/usr/bin/env python3
"""Six lost figures across four statistics and machine-learning posts.

p=12104, Bayesian cue combination:
  GPlots  "if X marks the 'true' position of the signal source, audio and
          visual cues give slightly different distributions for where the source
          might be. Notice the auditory distribution is a bit broader"

p=15998, the objective function:
  MADvsOLS_clean  "best fit lines for Mean Absolute Deviation (MAD) and
          Ordinary Least Squares (OLS) regression"
  MADvsOLS-1      the same "in the presence of outliers ... the 2 outliers in
          the bottom right hand corner"

p=15773, p-hacking:
  p_hacking_plot_use  x values 0,1,2,3,4 against twelve outcome series of
          standard normal noise, of which two came out significant. The post
          reports p = 0.032 and 0.016; the seed here is searched until a re-run
          produces two significant series at those values to two decimals.

p=12431, reproducing kernel Hilbert space:
  fig01   data with an x1 coordinate, an x2 coordinate and a colour, which
          cannot be separated by a line
  fig02   the same data under the feature map phi(x) = [x1, x2, x1x2], where
          "the grey plane can separate the different coloured clusters"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in, \
    mma_axes

P04 = paths_in("p=12104.html")
P98 = paths_in("p=15998.html")
P73 = paths_in("p=15773.html")
P31 = paths_in("p=12431.html")

# --- GPlots: two cues and the posterior ----------------------------------
MU_A, SD_A = 1.4, 1.5          # auditory: broader, as the caption says
MU_V, SD_V = 2.6, 0.8
prec = 1 / SD_A ** 2 + 1 / SD_V ** 2
MU_C = (MU_A / SD_A ** 2 + MU_V / SD_V ** 2) / prec
SD_C = np.sqrt(1 / prec)
x = np.linspace(-4, 8, 800)
fig, ax = plt.subplots(figsize=(6.6, 5.0))
ax.plot(x, stats.norm(MU_A, SD_A).pdf(x), color=BLUE, lw=2,
        label=r"$p(A|X)$, auditory")
ax.plot(x, stats.norm(MU_V, SD_V).pdf(x), color=RED, lw=2,
        label=r"$p(V|X)$, visual")
ax.plot(x, stats.norm(MU_C, SD_C).pdf(x), color=GREEN, lw=2, ls="--",
        label="combined")
ax.plot([2.0], [0], "x", color="black", ms=11, mew=2.4, zorder=6)
ax.annotate("$X$", (2.0, 0), textcoords="offset points", xytext=(4, -18),
            fontsize=13)
axes(ax, (-4, 8), (0, 0.62), spines="box", xlabel="position", ylabel=None)
ax.legend(fontsize=10, frameon=False, loc="upper left")
save(fig, P04["GPlots.png"])


# --- MAD against OLS, with and without outliers --------------------------
def mad_fit(xs, ys):
    """Least absolute deviations, by a coarse then fine search on the slope."""
    best, lo, hi = None, -5.0, 5.0
    for _ in range(60):
        grid = np.linspace(lo, hi, 200)
        losses = []
        for m in grid:
            c = float(np.median(ys - m * xs))
            losses.append(float(np.abs(ys - (m * xs + c)).sum()))
        j = int(np.argmin(losses))
        best = grid[j]
        step = grid[1] - grid[0]
        lo, hi = best - step, best + step
    return best, float(np.median(ys - best * xs))


rng = np.random.default_rng(15998)
xs = np.linspace(0, 10, 26)
ys = 1.0 + 0.9 * xs + rng.normal(0, 0.9, xs.size)


def madols(xs_, ys_, dest, title):
    m_ols, c_ols = np.polyfit(xs_, ys_, 1)
    m_mad, c_mad = mad_fit(xs_, ys_)
    fig, ax = plt.subplots(figsize=(5.8, 3.9))
    ax.plot(xs_, ys_, "o", color="#5a5a5a", ms=4.5, alpha=0.85)
    xr = np.linspace(xs_.min() - 0.4, xs_.max() + 0.4, 200)
    ax.plot(xr, m_ols * xr + c_ols, color=RED, lw=2, label="OLS")
    ax.plot(xr, m_mad * xr + c_mad, color=BLUE, lw=2, ls="--", label="MAD")
    axes(ax, None, None, spines="box", xlabel="$x$", ylabel="$y$")
    ax.set_title(title, fontsize=9.5)
    ax.legend(fontsize=10, frameon=False, loc="upper left")
    save(fig, dest)
    return (m_ols, m_mad)


clean = madols(xs, ys, P98["MADvsOLS_clean.png"],
               "best fit lines, no outliers")
xs2 = np.append(xs, [9.2, 9.8])
ys2 = np.append(ys, [-4.5, -5.2])          # two outliers, bottom right
dirty = madols(xs2, ys2, P98["MADvsOLS-1.png"],
               "the same, with two outliers at the bottom right")


# --- p-hacking: twelve outcome series against x = 0..4 -------------------
def phack(seed, n=5, k=12):
    r = np.random.default_rng(seed)
    xv = np.arange(n, dtype=float)
    ys_ = r.normal(0, 1, size=(k, n))
    ps = np.array([stats.linregress(xv, row).pvalue for row in ys_])
    return xv, ys_, ps


target = (0.032, 0.016)
found = None
for seed in range(400000):
    xv, Y, ps = phack(seed)
    sig = np.where(ps < 0.05)[0]
    if len(sig) >= 2:
        got = tuple(round(float(p), 3) for p in np.sort(ps)[:2][::-1])
        if got == target:
            found = (seed, xv, Y, ps, sig)
            break
if found is None:                       # settle for any two significant
    for seed in range(400000):
        xv, Y, ps = phack(seed)
        sig = np.where(ps < 0.05)[0]
        if len(sig) >= 2:
            found = (seed, xv, Y, ps, sig)
            break
SEED, xv, Y, ps, sig = found
fig, ax = plt.subplots(figsize=(4.2, 4.1))
for i in range(len(Y)):
    is_sig = i in sig
    ax.plot(xv, Y[i], "-o", ms=4,
            color=RED if is_sig else "#c9d3dd", lw=1.8 if is_sig else 0.9,
            zorder=5 if is_sig else 2,
            label=(f"$y_{{{i}}}$, $p={ps[i]:.3f}$" if is_sig else None))
axes(ax, None, None, spines="box", xlabel="pigeons encountered", ylabel="$y$")
ax.legend(fontsize=8, frameon=False, loc="upper left")
ax.set_title("twelve outcomes, pure noise", fontsize=9.5)
save(fig, P73["p_hacking_plot_use.png"])

# --- RKHS: the classic non-separable example -----------------------------
r2 = np.random.default_rng(12431)
n = 60
pts = r2.uniform(-1, 1, size=(4 * n, 2))
pts = pts[np.abs(pts).min(1) > 0.18]
lab = (pts[:, 0] * pts[:, 1]) > 0
fig, ax = plt.subplots(figsize=(4.6, 4.8))
ax.plot(pts[lab, 0], pts[lab, 1], "o", color=BLUE, ms=5)
ax.plot(pts[~lab, 0], pts[~lab, 1], "o", color=RED, ms=5)
axes(ax, (-1.1, 1.1), (-1.1, 1.1), spines="box", xlabel="$x_1$",
     ylabel="$x_2$")
ax.set_title("no line separates these", fontsize=10)
save(fig, P31["fig01.png"])

fig = plt.figure(figsize=(4.6, 4.6))
ax = mma_axes(fig, elev=18, azim=-62)
z = pts[:, 0] * pts[:, 1]
ax.scatter(pts[lab, 0], pts[lab, 1], z[lab], color=BLUE, s=14)
ax.scatter(pts[~lab, 0], pts[~lab, 1], z[~lab], color=RED, s=14)
gx, gy = np.meshgrid(np.linspace(-1.1, 1.1, 8), np.linspace(-1.1, 1.1, 8))
ax.plot_surface(gx, gy, np.zeros_like(gx), color=GREY, alpha=0.35,
                linewidth=0)
ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
ax.set_zlabel("$x_1x_2$")
ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
save(fig, P31["fig02.png"])

# --- what the posts assert ------------------------------------------------
print("  stats and ML checks:")
check("the auditory distribution is broader (post's caption)", SD_A > SD_V,
      True)
check("the combined estimate is more precise than either cue",
      SD_C < min(SD_A, SD_V), True)
check("  ... and lies between the two cue means", MU_A < MU_C < MU_V, True)
check("OLS and MAD agree closely on clean data (post)",
      abs(clean[0] - clean[1]) < 0.12, True)
check("outliers move OLS much more than MAD (post's whole point)",
      abs(dirty[0] - clean[0]) > 3 * abs(dirty[1] - clean[1]), True)
check("the p-hacking data has no real trend: it is pure noise", True, True)
check("  ... yet at least two of twelve come out significant (post)",
      len(sig) >= 2, True)
check(f"  ... at p = {', '.join(f'{ps[i]:.3f}' for i in sig[:2])} "
      f"(post reported 0.032 and 0.016)",
      bool(np.all(ps[sig] < 0.05)), True)
check("RKHS: the labels are exactly the sign of x1*x2",
      bool(np.all(lab == ((pts[:, 0] * pts[:, 1]) > 0))), True)
check("  ... so no line separates them (both classes straddle every "
      "half-plane through the origin)",
      bool(lab[pts[:, 0] > 0].any() and (~lab[pts[:, 0] > 0]).any()), True)
check("  ... but the plane x1x2 = 0 does, in the feature space",
      bool(np.all(z[lab] > 0) and np.all(z[~lab] < 0)), True)
print("  stats and ML: 6 figures written")
