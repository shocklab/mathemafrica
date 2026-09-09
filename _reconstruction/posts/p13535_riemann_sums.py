#!/usr/bin/env python3
"""p=13535, "MAM1000W 2017 semester 2, lecture 1 (part i)". Six lost figures.

The post builds the Riemann sum a step at a time over the interval it names,
"the area under the curve between x=0.5 and x=1.5", and each figure is the next
step:

  pl1  "It's the area shaded under the curve here"
  pl2  one rectangle each side, where "the red rectangle on the left
       underestimates the area, whereas the red rectangle on the right
       overestimates" it, with areas (1.5-0.5)f(0.5) and (1.5-0.5)f(1.5)
  pl3  "how about we try and approximate it with two rectangles"
  pl4  "The left plot is made up of five rectangles, each with width (b-a)/5"
  pl6  the same five, with the left-hand points named: "The first one is going
       to be called x_0 and is actually the point x=a ... The point x=b is
       called x_5"
  pl5  "let's try with 15 rectangles instead of 5"

The post never names f: it says "We'll start with an arbitrary function f(x)
and move on to concrete examples later", and the concrete example at the end of
the post (e^x on [0,1], area e-1) belongs to no figure. So f is chosen here.
The text does constrain it: left endpoints must underestimate and right
endpoints overestimate, which forces f to be increasing across the interval.
The function used is increasing, and the checks below verify that, that the
sums bracket the true area, and that they close in as n grows.

Sizes come from the archive's resize parameters: pl2 to pl5 are 1200x393, a
wide strip holding the two plots side by side, pl1 is 800x544 and pl6 600x420,
single plots.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, FILL, GREY, save, axes, check, paths_in

P = paths_in("p=13535.html")
A, B = 0.5, 1.5
f = lambda x: 1.0 + 0.9 * x + 0.25 * np.sin(3 * x - 1)
XR, YR = (0.15, 1.85), (0.0, 3.2)
EXACT = quad(f, A, B)[0]


def curve(ax):
    x = np.linspace(*XR, 600)
    ax.plot(x, f(x), color=BLUE, lw=2, zorder=4)
    axes(ax, XR, YR, spines="box", xlabel="$x$", ylabel="$y$")
    ax.set_xticks([A, B]); ax.set_xticklabels(["$a$", "$b$"])
    ax.set_yticks([])


def rectangles(ax, n, side):
    """n rectangles on [a, b], height taken at the left or the right point."""
    edges = np.linspace(A, B, n + 1)
    dx = (B - A) / n
    for lo in edges[:-1]:
        h = f(lo if side == "left" else lo + dx)
        ax.add_patch(plt.Rectangle((lo, 0), dx, h, facecolor=FILL, alpha=0.5,
                                   edgecolor=RED, lw=1.3, zorder=2))
    return float(sum(f(edges[:-1] if side == "left" else edges[1:])) * dx)


def pair(dest, n, title_l, title_r):
    fig, axs = plt.subplots(1, 2, figsize=(12.0, 3.93))
    out = []
    for ax, side in zip(axs, ("left", "right")):
        curve(ax)
        out.append(rectangles(ax, n, side))
    axs[0].set_title(title_l, fontsize=11)
    axs[1].set_title(title_r, fontsize=11)
    save(fig, dest)
    return out


# --- pl1: the area we are after ------------------------------------------
fig, ax = plt.subplots(figsize=(8.0, 5.44))
xs = np.linspace(A, B, 400)
ax.fill_between(xs, 0, f(xs), color=FILL, alpha=0.6, zorder=2)
curve(ax)
ax.set_title("the area under $y=f(x)$ between $x=a=0.5$ and $x=b=1.5$",
             fontsize=11)
save(fig, P["pl1.jpg"])

# --- pl2, pl3, pl4, pl5: one, two, five and fifteen rectangles ------------
L1, R1 = pair(P["pl2.jpg"], 1, "one rectangle, height $f(a)$: too small",
              "one rectangle, height $f(b)$: too big")
L2, R2 = pair(P["pl3.jpg"], 2, "$L_2$", "$R_2$")
L5, R5 = pair(P["pl4.jpg"], 5, "$L_5$", "$R_5$")
L15, R15 = pair(P["pl5.jpg"], 15, "$L_{15}$", "$R_{15}$")

# --- pl6: the five left-hand points named --------------------------------
fig, ax = plt.subplots(figsize=(6.0, 4.2))
curve(ax)
rectangles(ax, 5, "left")
edges = np.linspace(A, B, 6)
ax.set_xticks(edges)
ax.set_xticklabels([f"$x_{i}$" for i in range(6)])
ax.set_title(r"$x_0=a$, $x_5=b$, and $\Delta x=(b-a)/5$ between them",
             fontsize=11)
save(fig, P["pl6.jpg"])

# --- what the post asserts ------------------------------------------------
print("  p=13535 checks:")
check("f is increasing across [a,b], which is what makes the left sum an "
      "underestimate and the right sum an overestimate (post)",
      bool(np.all(np.diff(f(np.linspace(A, B, 4001))) > 0)), True)
check("one rectangle on the left is (b-a)f(a) (post)", L1, (B - A) * f(A))
check("one rectangle on the right is (b-a)f(b) (post)", R1, (B - A) * f(B))
check("  ... and the left underestimates while the right overestimates (post)",
      bool(L1 < EXACT < R1), True)
check("two rectangles: L = (1-0.5)f(0.5) + (1.5-1)f(1) (post)",
      L2, 0.5 * f(0.5) + 0.5 * f(1.0))
check("  ... R = (1-0.5)f(1) + (1.5-1)f(1.5) (post)",
      R2, 0.5 * f(1.0) + 0.5 * f(1.5))
dx5 = (B - A) / 5
check("five rectangles each have width (b-a)/5 (post)", dx5, 0.2)
check("  ... and L_5 is the sum of dx f(a + i dx), i = 0..4 (post)",
      L5, float(sum(dx5 * f(A + i * dx5) for i in range(5))))
check("  ... which is the same as sum_{i=1}^{5} dx f(x_{i-1}) (post)",
      L5, float(sum(dx5 * f(A + (i - 1) * dx5) for i in range(1, 6))))
check("x_0 = a and x_5 = b (post)", (edges[0], edges[-1]), (A, B))
check("the sums close in as n grows (post)",
      bool((R15 - L15) < (R5 - L5) < (R2 - L2) < (R1 - L1)), True)
check("  ... and they still bracket the area at n=15",
      bool(L15 < EXACT < R15), True)
check("R_n - L_n is exactly (f(b) - f(a))(b-a)/n, so it goes to zero (post)",
      R15 - L15, (f(B) - f(A)) * (B - A) / 15)
print("  p=13535: 6 figures written")
