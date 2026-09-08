#!/usr/bin/env python3
"""p=10954, "UCT MAM1000 Lecture notes part 9" (areas between curves).

Nine lost figures. Eight are fully determined by the text: it names both
curves, the region, the intersection points and the answer in every case, and
each of those numbers is checked below before anything is drawn.

The exception is RS.png, where the post says only that the rectangles are
left-point with dx = 0.02 starting at x_1 = 0, and never names f and g. The
curves there are drawn generically and reused for betweencurves.png, so the two
illustrative figures at the top of the post agree with each other. That is the
one place in this post where the drawing goes beyond what the text fixes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, FILL, save, axes, check, paths_in

P = paths_in("p=10954.html")

# generic pair used only for the two illustrative figures at the top
gf = lambda x: 3.0 + 0.8 * np.sin(2.6 * x) - 0.5 * x
gg = lambda x: 0.7 + 0.9 * x ** 2


def curve_pair(ax, f, g, lo, hi, n=600, fill=True, flab=None, glab=None):
    x = np.linspace(lo, hi, n)
    ax.plot(x, f(x), color=BLUE, lw=2, label=flab, zorder=3)
    ax.plot(x, g(x), color=RED, lw=2, label=glab, zorder=3)
    if fill:
        ax.fill_between(x, g(x), f(x), color=FILL, alpha=0.55, zorder=2)


# --- betweencurves.png (669x184, a 3.6:1 strip): area under f, minus area
#     under g, equals the area between them ----------------------------------
fig, axs = plt.subplots(1, 3, figsize=(8.4, 1.85))
xs = np.linspace(0, 1, 400)
for ax, mode in zip(axs, ("f", "g", "both")):
    if mode in ("f", "both"):
        ax.plot(xs, gf(xs), color=BLUE, lw=1.8)
    if mode in ("g", "both"):
        ax.plot(xs, gg(xs), color=RED, lw=1.8)
    lo = gg(xs) if mode == "both" else np.zeros_like(xs)
    hi = gf(xs) if mode in ("f", "both") else gg(xs)
    ax.fill_between(xs, lo, hi, color=FILL, alpha=0.55)
    ax.set_xlim(0, 1); ax.set_ylim(0, 4.2)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axs[0].set_title(r"$\int f$", fontsize=11)
axs[1].set_title(r"$\int g$", fontsize=11)
axs[2].set_title(r"$\int (f-g)$", fontsize=11)
for x in (0.345, 0.678):
    fig.text(x, 0.52, "$-$" if x < 0.5 else "$=$", fontsize=15, ha="center")
save(fig, P["betweencurves.png"])

# --- RS.png (833x518): left-point rectangles, dx = 0.02, x_1 = 0 ------------
dx = 0.02
fig, ax = plt.subplots(figsize=(7.2, 4.5))
left = np.arange(0, 1, dx)
for xi in left:
    ax.add_patch(plt.Rectangle((xi, gg(xi)), dx, gf(xi) - gg(xi),
                               facecolor=FILL, edgecolor="#5a9bd4",
                               lw=0.5, alpha=0.9, zorder=2))
curve_pair(ax, gf, gg, 0, 1, fill=False, flab="$f(x)$", glab="$g(x)$")
axes(ax, (-0.02, 1.02), (0, 4.2))
ax.legend(loc="upper right", fontsize=10, frameon=False)
ax.set_title(r"left-point rectangles, $\Delta x=0.02$, "
             r"heights $f(x_i)-g(x_i)$", fontsize=11)
save(fig, P["RS.png"])

# --- updown.png (833x525): -x^2+6 and x^2+3, meeting at +-sqrt(3/2) --------
r = np.sqrt(1.5)
f1, g1 = (lambda x: -x ** 2 + 6), (lambda x: x ** 2 + 3)
fig, ax = plt.subplots(figsize=(7.2, 4.6))
curve_pair(ax, f1, g1, -3, 3, flab=r"$f(x)=-x^2+6$", glab=r"$g(x)=x^2+3$")
x = np.linspace(-r, r, 200)
ax.fill_between(x, g1(x), f1(x), color=FILL, alpha=0.85, zorder=2)
for s in (-r, r):
    ax.plot([s], [f1(s)], "o", color=GREEN, ms=6, zorder=4)
ax.annotate(r"$x=\pm\sqrt{\frac{3}{2}}$", (r, f1(r)), textcoords="offset points",
            xytext=(10, -4), fontsize=11, color=GREEN)
axes(ax, (-3, 3), (0, 13))
ax.legend(loc="upper center", fontsize=10, frameon=False)
save(fig, P["updown.png"])

# --- nonint.png (833x520): x and -x^2-3 between x=-4 and x=3 ---------------
f2, g2 = (lambda x: x), (lambda x: -x ** 2 - 3)
fig, ax = plt.subplots(figsize=(7.2, 4.5))
curve_pair(ax, f2, g2, -4.6, 3.6, fill=False,
           flab=r"$f(x)=x$", glab=r"$g(x)=-x^2-3$")
x = np.linspace(-4, 3, 300)
ax.fill_between(x, g2(x), f2(x), color=FILL, alpha=0.7, zorder=2)
for v in (-4, 3):
    ax.plot([v, v], [g2(v), f2(v)], color=GREEN, lw=1.6, ls="--", zorder=3)
    ax.text(v, f2(v) + 1.2, f"$x={v}$", ha="center", fontsize=10, color=GREEN)
axes(ax, (-4.8, 3.8), (-22, 6))
ax.legend(loc="lower left", fontsize=10, frameon=False)
save(fig, P["nonint.png"])

# --- sinsquare.png (833x524): sin x and x^2-2 -------------------------------
p = lambda x: np.sin(x) - x ** 2 + 2
lo_i, hi_i = brentq(p, -2, 0), brentq(p, 0, 2)
f3, g3 = np.sin, (lambda x: x ** 2 - 2)
fig, ax = plt.subplots(figsize=(7.2, 4.5))
curve_pair(ax, f3, g3, -2.6, 2.6, fill=False,
           flab=r"$f(x)=\sin x$", glab=r"$g(x)=x^2-2$")
x = np.linspace(lo_i, hi_i, 400)
ax.fill_between(x, g3(x), f3(x), color=FILL, alpha=0.7, zorder=2)
for s in (lo_i, hi_i):
    ax.plot([s], [np.sin(s)], "o", color=GREEN, ms=6, zorder=4)
ax.annotate(f"$x\\approx{lo_i:.2f}$", (lo_i, np.sin(lo_i)),
            textcoords="offset points", xytext=(-58, -16), fontsize=10, color=GREEN)
ax.annotate(f"$x\\approx{hi_i:.2f}$", (hi_i, np.sin(hi_i)),
            textcoords="offset points", xytext=(8, 6), fontsize=10, color=GREEN)
axes(ax, (-2.6, 2.6), (-2.6, 5))
ax.legend(loc="upper left", fontsize=10, frameon=False)
save(fig, P["sinsquare.png"])

# --- px.png (833x561): p(x) = sin x - x^2 + 2, showing its two zeros --------
fig, ax = plt.subplots(figsize=(7.2, 4.9))
x = np.linspace(-3, 3, 700)
ax.plot(x, p(x), color=BLUE, lw=2, zorder=3)
for s, off in ((lo_i, (-46, 14)), (hi_i, (10, 14))):
    ax.plot([s], [0], "o", color=RED, ms=7, zorder=4)
    ax.annotate(f"${s:.2f}$", (s, 0), textcoords="offset points",
                xytext=off, fontsize=10, color=RED)
axes(ax, (-3, 3), (-6.5, 3.2))
ax.set_title(r"$p(x)=\sin x-x^2+2$", fontsize=12)
save(fig, P["px.png"])

# --- pxNewt.png (833x547): three Newton iterations from x=1 ----------------
dp = lambda x: np.cos(x) - 2 * x
xs_n = [1.0]
for _ in range(3):
    xs_n.append(xs_n[-1] - p(xs_n[-1]) / dp(xs_n[-1]))
fig, ax = plt.subplots(figsize=(7.2, 4.7))
x = np.linspace(-0.5, 3.0, 700)
ax.plot(x, p(x), color=BLUE, lw=2, zorder=3)
for i in range(3):
    x0, x1 = xs_n[i], xs_n[i + 1]
    ax.plot([x0, x0], [0, p(x0)], color=GREY, lw=0.9, ls=":", zorder=3)
    ax.plot([x0, x1], [p(x0), 0], color=RED, lw=1.4, zorder=4)
    ax.plot([x0], [p(x0)], "o", color=RED, ms=4, zorder=5)
    ax.annotate(f"$x_{i}={x0:.3f}$", (x0, 0), textcoords="offset points",
                xytext=(3, 8 + 12 * (i % 2)), fontsize=9, color=RED)
ax.plot([hi_i], [0], "o", color=GREEN, ms=7, zorder=6)
axes(ax, (-0.5, 3.0), (-6.0, 3.0))
ax.set_title(r"three Newton steps on $p(x)=\sin x-x^2+2$ from $x=1$",
             fontsize=11)
save(fig, P["pxNewt.png"])

# --- yfunc.png (833x847): y = x-1 and x = (y^2-6)/2, drawn in y ------------
fig, ax = plt.subplots(figsize=(6.4, 6.5))
y = np.linspace(-3.4, 5.0, 500)
ax.plot(y + 1, y, color=BLUE, lw=2, label=r"$y=x-1$", zorder=3)
ax.plot((y ** 2 - 6) / 2, y, color=RED, lw=2,
        label=r"$x=\frac{y^2-6}{2}$", zorder=3)
yy = np.linspace(-2, 4, 300)
ax.fill_betweenx(yy, (yy ** 2 - 6) / 2, yy + 1, color=FILL, alpha=0.65, zorder=2)
for yv in (-2, 4):
    ax.plot([yv + 1], [yv], "o", color=GREEN, ms=6, zorder=4)
    ax.annotate(f"$y={yv}$", (yv + 1, yv), textcoords="offset points",
                xytext=(8, -4), fontsize=10, color=GREEN)
axes(ax, (-4, 7), (-3.4, 5.0))
ax.legend(loc="upper left", fontsize=11, frameon=False)
save(fig, P["yfunc.png"])

# --- sincos.png (833x486): sin 2x and cos x on [0, pi/2], two regions ------
fig, ax = plt.subplots(figsize=(7.2, 4.2))
x = np.linspace(0, np.pi / 2, 500)
ax.plot(x, np.sin(2 * x), color=BLUE, lw=2, label=r"$y=\sin 2x$", zorder=3)
ax.plot(x, np.cos(x), color=RED, lw=2, label=r"$y=\cos x$", zorder=3)
xa = np.linspace(0, np.pi / 6, 200)
xb = np.linspace(np.pi / 6, np.pi / 2, 300)
ax.fill_between(xa, np.sin(2 * xa), np.cos(xa), color=FILL, alpha=0.75, zorder=2)
ax.fill_between(xb, np.cos(xb), np.sin(2 * xb), color="#f4b6b6", alpha=0.85, zorder=2)
ax.plot([np.pi / 6], [np.cos(np.pi / 6)], "o", color=GREEN, ms=6, zorder=4)
ax.annotate(r"$x=\frac{\pi}{6}$", (np.pi / 6, np.cos(np.pi / 6)),
            textcoords="offset points", xytext=(-16, 12), fontsize=11, color=GREEN)
axes(ax, (0, np.pi / 2), (-0.05, 1.15))
ax.set_xticks([0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2])
ax.set_xticklabels(["$0$", r"$\frac{\pi}{6}$", r"$\frac{\pi}{4}$",
                    r"$\frac{\pi}{3}$", r"$\frac{\pi}{2}$"])
ax.legend(loc="lower left", fontsize=10, frameon=False)
save(fig, P["sincos.png"])

# --- every number the post states -----------------------------------------
print("  p=10954 checks:")
check("updown intersections at sqrt(3/2)", r, np.sqrt(1.5))
check("updown area (post: 2sqrt6)", 2 * (-2 * r ** 3 / 3 + 3 * r), 2 * np.sqrt(6))
F = lambda x: x ** 2 / 2 + x ** 3 / 3 + 3 * x
check("nonint area (post: 287/6)", F(3) - F(-4), 287 / 6)
check("sin/x^2 left intersection (post: -1.06)", round(lo_i, 2), -1.06)
check("sin/x^2 right intersection (post: 1.73)", round(hi_i, 2), 1.73)
check("sin/x^2 area (post: 4.10)",
      round(quad(lambda t: np.sin(t) - (t ** 2 - 2), lo_i, hi_i)[0], 2), 4.10)
check("third Newton iterate reaches 1.73", round(xs_n[3], 2), 1.73)
check("yfunc lower y limit (post: -2)", float(min(np.roots([1, -2, -8]))), -2.0)
check("yfunc upper y limit (post: 4)", float(max(np.roots([1, -2, -8]))), 4.0)
check("sin2x = cos x crossing (post: the left one)",
      np.sin(2 * np.pi / 6), np.cos(np.pi / 6), tol=1e-12)
print("  p=10954: 9 figures written (RS.png and betweencurves.png generic, "
      "see docstring)")
