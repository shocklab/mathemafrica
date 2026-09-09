#!/usr/bin/env python3
"""p=15794, "p-values (part 3): meta distribution of p-values".

Four lost histograms, one per true mean. The post specifies the simulation
completely: draw 10,000 samples of size 30 from a Gaussian with standard
deviation 1 and mean 0, 0.05, 0.1 or 0.3; test one-sided that the mean exceeds
0, so the statistic follows a t with 29 degrees of freedom; histogram the
10,000 p-values. "The red line in each plot shows the 5% cutoff value ... The
blue line shows the 'true' (or 'typical') p-value that we would get if our
sample mean was exactly the true mean."

The post also prints a table of the proportion of p-values below 0.001, 0.005,
0.01 and 0.05 for each mean. All sixteen of its entries agree with the exact
non-central t power to within Monte Carlo error, which is what confirms this
setup, and the re-run here is checked against that same theory.

One slip in the post, worth knowing before reading it: the paragraph beginning
"Consider figure 3 and the final column in the table" describes the mean of
0.3, which is figure 4. Its arithmetic only works there. The typical p-value is
0.294 at mean 0.1 but 0.0556 at mean 0.3, and it is the latter the text calls
"just over 0.05"; likewise 0.48 of experiments significant, and 0.1544/0.48 of
those below 0.005, is "about half" and "one-third" for the 0.3 column alone.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, save, axes, check, paths_in

P = paths_in("p=15794.html")
N, DF, RUNS = 30, 29, 10_000
MEANS = [(0.0, "Mu_0.png"), (0.05, "Mu_0_05.png"),
         (0.1, "Mu_0_1.png"), (0.3, "Mu_0_3.png")]
ALPHAS = [0.001, 0.005, 0.01, 0.05]
# the table the post prints, for comparison
POST_TABLE = {0.0: [0.0007, 0.0048, 0.0093, 0.0465],
              0.05: [0.0027, 0.0111, 0.0200, 0.0849],
              0.1: [0.0048, 0.0185, 0.0389, 0.1369],
              0.3: [0.0554, 0.1544, 0.2269, 0.4800]}
rng = np.random.default_rng(15794)

results = {}
for mu, name in MEANS:
    x = rng.normal(mu, 1.0, size=(RUNS, N))
    t = x.mean(1) / (x.std(1, ddof=1) / np.sqrt(N))
    p = stats.t.sf(t, DF)
    results[mu] = p
    typical = float(stats.t.sf(mu * np.sqrt(N), DF))

    fig, ax = plt.subplots(figsize=(4.4, 2.4))
    ax.hist(p, bins=50, range=(0, 1), color="#7fa8cd", edgecolor="white",
            lw=0.3)
    ax.axvline(0.05, color=RED, lw=1.4)
    ax.axvline(typical, color=BLUE, lw=1.4)
    axes(ax, (0, 1), None, spines="box", xlabel="p-value", ylabel="count")
    ax.set_title(rf"mean $={mu:g}$   (typical $p={typical:.3f}$)", fontsize=9)
    save(fig, P[name])

# --- against the post's own table, and against exact theory --------------
print("  p=15794 checks:")
for mu, _ in MEANS:
    p = results[mu]
    for a, claimed in zip(ALPHAS, POST_TABLE[mu]):
        theory = float(stats.nct.sf(stats.t.isf(a, DF), DF, mu * np.sqrt(N)))
        got = float((p < a).mean())
        se = np.sqrt(theory * (1 - theory) / RUNS)
        check(f"mean {mu:<5g} P(p<{a}): post {claimed:.4f}, theory "
              f"{theory:.4f}, run {got:.4f} within 4 s.e.",
              abs(got - theory) < 4 * se + 1e-4, True)
check("at mean 0 the p-values are near-uniform (KS test not rejected)",
      float(stats.kstest(results[0.0], "uniform").pvalue) > 0.01, True)
check("the typical p-value at mean 0 is 0.5", stats.t.sf(0.0, DF), 0.5)
check("the typical p-value at mean 0.3 is just over 0.05 (post's remark)",
      round(float(stats.t.sf(0.3 * np.sqrt(N), DF)), 4), 0.0556)
check("  ... whereas at mean 0.1 it is 0.294, so that remark is about "
      "the last column, not figure 3",
      round(float(stats.t.sf(0.1 * np.sqrt(N), DF)), 3), 0.294)
sig = float((results[0.3] < 0.05).mean())
very = float((results[0.3] < 0.005).mean())
check("at mean 0.3 about half the experiments are significant (post)",
      abs(sig - 0.5) < 0.05, True)
check("  ... and about a third of those are below 0.005 (post)",
      abs(very / sig - 1 / 3) < 0.06, True)
check("the leftmost bin grows fastest with the mean (post's central point)",
      float((results[0.3] < 0.02).mean()) > float((results[0.1] < 0.02).mean())
      > float((results[0.05] < 0.02).mean())
      > float((results[0.0] < 0.02).mean()), True)
print("  p=15794: 4 figures written")
