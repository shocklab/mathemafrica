#!/usr/bin/env python3
"""p=15734, "R-squared values for linear regression".

Three lost scatter plots, each with its R^2 quoted in the text, so the noise
level is tuned here until the fitted R^2 rounds to the value the post gives:

  Good_fit_low_noise      a genuinely linear relationship, R^2 = 0.99
  Bad_fit_low_noise       a linear fit to a quadratic relationship, low noise,
                          R^2 = 0.97, and "the regression fit is first below
                          the data, then above the data, then below the data
                          again", which is what a straight line does against an
                          upward parabola
  Good_fit_high_noise-1   a linear relationship with much more noise,
                          R^2 = 0.56

The post also fixes the drawing: "the red line (our predictions) is much closer
to the data than to the mean (the blue line)", so red is the fit and blue is
the mean of y.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, save, axes, check, paths_in

P = paths_in("p=15734.html")
N = 60
X = np.linspace(0, 10, N)


def fit(x, y):
    b1, b0 = np.polyfit(x, y, 1)
    yhat = b0 + b1 * x
    ssreg = float(((yhat - y.mean()) ** 2).sum())
    ctss = float(((y - y.mean()) ** 2).sum())
    return yhat, ssreg / ctss


def tune(shape, target, seed):
    """Pick the noise level whose fitted R^2 rounds to the post's value."""
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 1, N)
    lo, hi = 1e-4, 60.0
    for _ in range(80):
        mid = (lo + hi) / 2
        y = shape(X) + mid * base
        _, r2 = fit(X, y)
        if round(r2, 2) == target:
            return y, r2
        if r2 > target:
            lo = mid
        else:
            hi = mid
    y = shape(X) + ((lo + hi) / 2) * base
    return y, fit(X, y)[1]


def plot(x, y, dest, title):
    yhat, r2 = fit(x, y)
    fig, ax = plt.subplots(figsize=(4.2, 2.9))
    ax.plot(x, y, "o", color="#5a5a5a", ms=3.6, alpha=0.85)
    ax.axhline(y.mean(), color=BLUE, lw=1.8)
    ax.plot(x, yhat, color=RED, lw=2)
    axes(ax, None, None, spines="box", xlabel="$x$", ylabel="$y$")
    ax.set_title(f"{title}:  $R^2={r2:.2f}$", fontsize=9.5)
    save(fig, dest)
    return r2


LIN = lambda x: 3.0 + 1.6 * x
# A quadratic with a real linear trend. A symmetric parabola over this range
# fits to a flat line and gives R^2 near zero, which cannot reach the 0.97 the
# post reports; this curvature leaves R^2 = 0.983 noiseless, so a little noise
# brings it to 0.97 while the residuals stay clearly curved.
QUAD = lambda x: 3.0 + 1.6 * x + 0.08 * (x - 5) ** 2

y_good, _ = tune(LIN, 0.99, 15734)
y_bad, _ = tune(QUAD, 0.97, 15735)
y_noisy, _ = tune(LIN, 0.56, 15736)

r_good = plot(X, y_good, P["Good_fit_low_noise.png"], "linear, little noise")
r_bad = plot(X, y_bad, P["Bad_fit_low_noise.png"],
             "a straight line through a quadratic")
r_noisy = plot(X, y_noisy, P["Good_fit_high_noise-1.png"],
               "linear, plenty of noise")

# --- the values and the behaviour the post states ------------------------
print("  p=15734 checks:")
check("good fit R^2 (post: 0.99)", round(r_good, 2), 0.99)
check("bad fit R^2 (post: 0.97)", round(r_bad, 2), 0.97)
check("noisy fit R^2 (post: 0.56)", round(r_noisy, 2), 0.56)
check("a high R^2 can come from a bad model (post's whole point)",
      r_bad > r_noisy, True)

res = y_bad - fit(X, y_bad)[0]
third = N // 3
check("the quadratic's residuals are positive at the left (fit below data)",
      float(res[:third].mean()) > 0, True)
check("  ... negative in the middle (fit above data)",
      float(res[third:2 * third].mean()) < 0, True)
check("  ... and positive again at the right",
      float(res[2 * third:].mean()) > 0, True)
check("perfect predictions would give R^2 = 1 (post)",
      fit(X, LIN(X))[1], 1.0, tol=1e-9)
check("predicting the mean everywhere gives R^2 = 0 (post)",
      float(((np.full(N, y_good.mean()) - y_good.mean()) ** 2).sum()), 0.0)
print("  p=15734: 3 figures written")
