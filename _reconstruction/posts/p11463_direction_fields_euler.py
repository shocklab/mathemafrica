#!/usr/bin/env python3
"""p=11463, "MAM1000 part 34, direction flows and Euler's method".

Four lost figures for dy/dx = x + y:

  dirfield1   the field "for points at integer values of x and y". The post
              prints the whole 7x7 table of gradients from -3 to 3, so the grid
              is fixed exactly.
  dirfield2   the same field on a finer grid
  dirfield3   the same with "four different solutions with different initial
              conditions", the solution being y = -1 - x + C e^x
  eulerflow   Euler's method from (0, -0.5) at "various length sections"

The post walks its coarse Euler run step by step: gradient -0.5 at the start
takes it to (1,-1), gradient 0 there takes it to (2,-1), gradient 1 there takes
it to (3,0). Those are asserted below before anything is drawn.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, ORANGE, PURPLE, GREY, save, axes, \
    check, paths_in, direction_field

P = paths_in("p=11463.html")
F = lambda x, y: x + y
XR = YR = (-3, 3)
TITLE = r"$\frac{dy}{dx}=x+y$"


def field_fig(step, size=(5.8, 5.8)):
    fig, ax = plt.subplots(figsize=size)
    direction_field(ax, F, XR, YR, step)
    axes(ax, None, None, xlabel=None, ylabel=None)
    ax.set_title(TITLE, fontsize=13)
    return fig, ax


fig, _ = field_fig(1.0)
save(fig, P["dirfield1.png"])

fig, _ = field_fig(0.4)
save(fig, P["dirfield2.png"])

# --- dirfield3: four solutions y = -1 - x + C e^x over the field --------
fig, ax = field_fig(0.4)
xs = np.linspace(-3, 3, 600)
for C, col in zip((-1.0, -0.2, 0.2, 1.0), (RED, ORANGE, GREEN, PURPLE)):
    y = -1 - xs + C * np.exp(xs)
    m = np.abs(y) <= 3.4
    ax.plot(xs[m], y[m], color=col, lw=2, zorder=6,
            label=rf"$C={C:g}$")
ax.legend(fontsize=9, frameon=False, loc="lower right")
save(fig, P["dirfield3.png"])


# --- eulerflow: Euler from (0, -0.5) at several step lengths ------------
def euler(h, x0=0.0, y0=-0.5, xend=3.0):
    xs, ys = [x0], [y0]
    while xs[-1] < xend - 1e-12:
        ys.append(ys[-1] + h * F(xs[-1], ys[-1]))
        xs.append(xs[-1] + h)
    return np.array(xs), np.array(ys)


fig, ax = plt.subplots(figsize=(7.4, 4.5))
direction_field(ax, F, (-0.4, 3.4), (-1.8, 0.4), 0.4)
for h, col in zip((1.0, 0.5, 0.1), (RED, ORANGE, GREEN)):
    xs, ys = euler(h)
    ax.plot(xs, ys, "-o" if h >= 0.5 else "-", color=col, lw=1.8, ms=4,
            zorder=6, label=rf"step ${h:g}$")
x = np.linspace(0, 3, 400)
ax.plot(x, -1 - x + 0.5 * np.exp(x), color=BLUE, lw=2, ls="--", zorder=5,
        label="exact")
ax.plot([0], [-0.5], "o", color="black", ms=6, zorder=7)
ax.annotate(r"$(0,-0.5)$", (0, -0.5), textcoords="offset points",
            xytext=(-18, -18), fontsize=9)
axes(ax, None, None, xlabel=None, ylabel=None)
ax.legend(fontsize=9, loc="lower right", framealpha=0.92,
          edgecolor="none")
ax.set_title(r"Euler's method on $\frac{dy}{dx}=x+y$ from $(0,-0.5)$",
             fontsize=11)
save(fig, P["eulerflow.png"])

# --- the post's own numbers ---------------------------------------------
print("  p=11463 checks:")
check("gradient at (3,2) (post: 5)", F(3, 2), 5)
tbl = {(x, y): x + y for x in range(-3, 4) for y in range(-3, 4)}
check("the printed table's corner (x=-3, y=-3) is -6", tbl[(-3, -3)], -6)
check("  ... and (x=3, y=3) is 6", tbl[(3, 3)], 6)
check("  ... and (x=2, y=-2) is 0", tbl[(2, -2)], 0)
xs, ys = euler(1.0)
check("Euler first step x (post's walk-through reaches x=1)", xs[1], 1.0)
check("Euler first step y (post: -1)", ys[1], -1.0)
check("Euler second step y (post: -1, gradient was 0)", ys[2], -1.0)
check("Euler third step y (post: 0, gradient was 1)", ys[3], 0.0)
check("y=-1-x+Ce^x solves the equation at x=1.3, C=0.7",
      -1 + 0.7 * np.exp(1.3), F(1.3, -1 - 1.3 + 0.7 * np.exp(1.3)))
print("  p=11463: 4 figures written")
