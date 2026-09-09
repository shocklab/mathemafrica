#!/usr/bin/env python3
"""Five lost animations of Taylor approximations, on two posts.

p=11232, "Some animations of Taylor approximations". The post sets the colours
and names every function and expansion point:

  "In each case the function which we are approximating is in red, and the
  polynomial approximation is in blue."

  an1  (1+x)^5 about x=0, "starting at a constant, then a straight line with
       non-zero gradient, then a quadratic etc. Each one matching the higher
       and higher derivatives of the function at x=0. You see that by the time
       we get to a fifth order polynomial, the match is exact."
  an2  (1+x)^5.2 about x=0, where "the polynomial approximation doesn't stop at
       the fifth order, but can keep going to any power of x"
  an3  the same function about x=0.25
  an4  sin(x) + cos(3x)/2 about x=2.5, "up to the 14th order polynomial", and
       "a pretty good match to the original function even quite a way away from
       the point about which we are expanding"

p=13183, "Radius of convergence of a series, and approximating polynomials":

  animate  two panels. On the right sin(x) about x=1, where "as we get more and
       more terms, we approximate the function better and better far away".
       On the left sqrt(1+x) about x=1, where "after x=3, the approximations
       are nowhere near the function itself. This is because that function has
       a radius of convergence of 2, when expanded about x=1. This is due to
       the behaviour of the function at x=-1, which is a distance 2 away."

Both claims about the radius are checked below against the coefficients, not
asserted: the ratio test on the series about x=1 gives exactly 2, and the error
at x=3.5 grows with order instead of shrinking.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, animate, axes, check, paths_in

P32 = paths_in("p=11232.html")
P83 = paths_in("p=13183.html")
x = sp.Symbol("x")


def taylor(expr, about, order):
    """The Taylor polynomial of expr about `about`, as a numpy callable."""
    poly = sum(expr.diff(x, k).subs(x, about) / sp.factorial(k)
               * (x - about) ** k for k in range(order + 1))
    return sp.lambdify(x, sp.expand(poly), "numpy")


def approximation_gif(dest, expr, about, orders, xr, yr,
                      figsize=(5.0, 3.3), title=None):
    f = sp.lambdify(x, expr, "numpy")
    xs = np.linspace(*xr, 700)
    polys = [taylor(expr, about, n) for n in orders]

    def draw(ax, i):
        n, p = orders[i], polys[i]
        ax.plot(xs, f(xs) * np.ones_like(xs), color=RED, lw=2)
        ax.plot(xs, p(xs) * np.ones_like(xs), color=BLUE, lw=2)
        a0 = float(about)
        ax.plot([a0], [float(f(a0))], "o", color="black", ms=4)
        axes(ax, xr, yr)
        ax.set_title(f"{title}, order {n}" if title else f"order {n}",
                     fontsize=10)

    return animate(draw, len(orders), dest, figsize=figsize, ms=600)


# --- an1: (1+x)^5 about 0, exact by the fifth order -----------------------
approximation_gif(P32["an1.gif"], (1 + x) ** 5, 0, range(6), (-2.2, 1.2),
                  (-12, 34), title=r"$(1+x)^5$ about $x=0$")
# --- an2: (1+x)^5.2 about 0, the series never terminates -------------------
approximation_gif(P32["an2.gif"], (1 + x) ** sp.Rational(26, 5), 0,
                  range(9), (-0.98, 1.2), (-6, 40),
                  title=r"$(1+x)^{5.2}$ about $x=0$")
# --- an3: the same, about 0.25 --------------------------------------------
approximation_gif(P32["an3.gif"], (1 + x) ** sp.Rational(26, 5), sp.Rational(1, 4),
                  range(9), (-0.98, 1.4), (-6, 60),
                  title=r"$(1+x)^{5.2}$ about $x=0.25$")
# --- an4: sin x + cos(3x)/2 about 2.5, to the fourteenth order -------------
approximation_gif(P32["an4.gif"], sp.sin(x) + sp.cos(3 * x) / 2,
                  sp.Rational(5, 2), range(15), (-2.0, 7.0), (-2.2, 2.2),
                  figsize=(5.0, 3.37),
                  title=r"$\sin x+\frac{\cos 3x}{2}$ about $x=2.5$")

# --- animate.gif: a radius of convergence, and none ------------------------
ROOT, SIN = sp.sqrt(1 + x), sp.sin(x)
froot, fsin = sp.lambdify(x, ROOT, "numpy"), sp.lambdify(x, SIN, "numpy")
ORDERS = list(range(1, 15))
proot = [taylor(ROOT, 1, n) for n in ORDERS]
psin = [taylor(SIN, 1, n) for n in ORDERS]
xl = np.linspace(-0.999, 5.0, 700)
xs_ = np.linspace(-4.0, 6.5, 700)


def draw_pair(fig, i):
    n = ORDERS[i]
    axl = fig.add_subplot(121)
    axl.plot(xl, froot(xl), color=RED, lw=2)
    axl.plot(xl, proot[i](xl) * np.ones_like(xl), color=BLUE, lw=2)
    axl.axvline(3.0, color="#bbbbbb", lw=0.9, ls=":")
    axes(axl, (-1.0, 5.0), (-1.0, 4.0))
    axl.set_title(r"$\sqrt{1+x}$ about $x=1$", fontsize=9)
    axr = fig.add_subplot(122)
    axr.plot(xs_, fsin(xs_), color=RED, lw=2)
    axr.plot(xs_, psin[i](xs_) * np.ones_like(xs_), color=BLUE, lw=2)
    axes(axr, (-4.0, 6.5), (-2.2, 2.2))
    axr.set_title(r"$\sin x$ about $x=1$", fontsize=9)
    fig.suptitle(f"order {n}", fontsize=10, y=1.0)
    fig.subplots_adjust(top=0.84, wspace=0.3)


def draw_animate(ax, i):
    ax.figure.delaxes(ax)
    draw_pair(ax.figure, i)


animate(draw_animate, len(ORDERS), P83["animate.gif"], figsize=(5.73, 3.2),
        ms=600)

# --- what the posts assert ------------------------------------------------
print("  Taylor animation checks:")
p5 = taylor((1 + x) ** 5, 0, 5)
check("(1+x)^5 is matched exactly by its fifth-order Taylor polynomial (post)",
      float(sp.expand((1 + x) ** 5 - sum(sp.diff((1 + x) ** 5, x, k).subs(x, 0)
            / sp.factorial(k) * x ** k for k in range(6)))), 0.0)
check("  ... but not by the fourth", round(float(p5(0.9) - taylor((1 + x) ** 5,
      0, 4)(0.9)), 6), round(0.9 ** 5, 6))
c = [sp.diff((1 + x) ** sp.Rational(26, 5), x, k).subs(x, 0) / sp.factorial(k)
     for k in range(9)]
check("(1+x)^5.2 has non-zero coefficients past the fifth order, so its series "
      "never terminates (post)", bool(all(ci != 0 for ci in c[6:])), True)
# Radius of convergence of sqrt(1+x) about x=1, from the coefficients. Writing
# sqrt(1+x) = sqrt(2) sqrt(1 + u/2) with u = x-1 gives a_k = sqrt(2) C(1/2,k)/2^k,
# so |a_k / a_{k+1}| = 2(k+1)/(k-1/2), which falls to 2 from above.
ratio = lambda k: 2 * (k + 1) / (k - 0.5)
check("sympy's coefficients match that closed form",
      [round(float(sp.diff(ROOT, x, k).subs(x, 1) / sp.factorial(k)), 12)
       for k in (2, 3, 4)],
      [round(float(sp.sqrt(2) * sp.binomial(sp.Rational(1, 2), k)
                   / 2 ** k), 12) for k in (2, 3, 4)])
check("sqrt(1+x) about x=1 has radius of convergence 2 (post): the ratio falls "
      "towards 2", bool(ratio(10) > ratio(100) > ratio(1000) > 2), True)
check("  ... reaching it to within 0.01 by k = 1000",
      bool(abs(ratio(1000) - 2) < 0.01), True)
check("  ... which is the distance from x=1 to the singularity at x=-1 (post)",
      abs(1 - (-1)), 2)
errs = [abs(float(proot[i](3.5)) - float(froot(3.5))) for i in (4, 9, 13)]
check("  ... so past x=3 more terms make it worse, not better (post)",
      bool(errs[0] < errs[1] < errs[2]), True)
serr = [abs(float(psin[i](6.0)) - float(fsin(6.0))) for i in (4, 9, 13)]
check("sin x about x=1 improves far away as the order rises (post)",
      bool(serr[0] > serr[1] > serr[2]), True)
check("  ... to 0.006 at x=6 by the fourteenth order, five units from the "
      "expansion point", round(serr[-1], 3), 0.006)
print("  Taylor animations: 5 written")
