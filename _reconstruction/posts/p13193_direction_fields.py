#!/usr/bin/env python3
"""p=13193, "Checking direction fields".

Six lost figures. The post names each differential equation and every feature
it then boxes in red, so all six are fully determined.

Two parameters come from the text rather than from taste. The sample spacing
for the tan field is 0.4, not 0.5, because the post describes the near-flat
lines as sitting at y = +-1.6 and a 0.5 grid lands on 1.5. And the lattice is
aligned on zero, or the row of vertical lines at y = 0 that tanr2 boxes would
not exist at all.

One editorial call: the post says "Along the y-axis we have vertical lines",
but the reason it gives is that tan(y) = 0 when y = 0, which is the x-axis.
tanr2 boxes y = 0, following the explanation rather than the wording.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figstyle import RED, save, axes, check, paths_in, direction_field

P = paths_in("p=13193.html")


def furniture(ax, title):
    ax.grid(True, color="#dddddd", lw=0.6)
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axvline(0, color="#999999", lw=0.8)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.tick_params(labelsize=8)
    ax.set_title(title, fontsize=13)


# --- xplusy.png (shown 1024x535, a two-panel strip) ------------------------
f1 = lambda x, y: x + y
fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.75))
for ax, step in zip(axs, (0.5, 0.25)):
    direction_field(ax, f1, (-3, 3), (-3, 3), step)
    furniture(ax, "")
    ax.set_title(f"sample spacing {step}", fontsize=10)
fig.suptitle(r"$\frac{dy}{dx} = x + y$", fontsize=14, y=0.99)
save(fig, P["xplusy.png"])

# --- xovery.png (660x669) --------------------------------------------------
def f2(x, y):
    return np.inf if y == 0 else x / y


fig, ax = plt.subplots(figsize=(6.4, 6.5))
direction_field(ax, f2, (-3, 3), (-3, 3), 0.5)
furniture(ax, r"$\frac{dy}{dx} = \frac{x}{y}$")
save(fig, P["xovery.png"])


# --- tan.png and the three boxed versions ---------------------------------
def f3(x, y):
    t = np.tan(y)
    return np.inf if abs(t) < 1e-9 else np.sqrt(max(x + 2.0, 0.0)) / t


T = r"$\frac{dy}{dx} = \frac{\sqrt{x+2}}{\tan(y)}$"


def tanfig(boxes, name):
    fig, ax = plt.subplots(figsize=(6.4, 6.5))
    direction_field(ax, f3, (-2, 4), (-3, 3), 0.4)
    for (x0, y0, w, h) in boxes:
        ax.add_patch(Rectangle((x0, y0), w, h, fill=False,
                               edgecolor=RED, lw=1.8, zorder=5))
    furniture(ax, T)
    save(fig, P[name])


tanfig([], "tan.png")
tanfig([(-2.20, -3.28, 0.40, 6.56)], "tanr1.png")          # x = -2, flat
tanfig([(-2.28, -0.20, 6.56, 0.40)], "tanr2.png")          # y = 0, vertical
tanfig([(-2.28, 1.42, 6.56, 0.36),
        (-2.28, -1.78, 6.56, 0.36)], "tanr3.png")          # y = +-1.6, flat

# --- the claims the post makes about these fields -------------------------
print("  p=13193 checks:")
check("dy/dx=x+y at (1,1), post says 2", f1(1, 1), 2)
check("dy/dx=x+y at (1,-1), post says 0", f1(1, -1), 0)
check("dy/dx=x/y along y=x, post says 1", f2(2, 2), 1)
check("dy/dx=x/y along y=-x, post says -1", f2(2, -2), -1)
check("tan field at x=-2 is flat", f3(-2, 1.2), 0.0)
check("tan field at y=0 is vertical", f3(2, 0), np.inf)
check("tan field near y=1.6 is near-flat", abs(f3(2, 1.6)) < 0.1, True)
check("1.6 is just past pi/2", 1.6 > np.pi / 2, True)
print("  p=13193: 6 figures written")
