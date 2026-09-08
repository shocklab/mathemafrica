#!/usr/bin/env python3
"""Reconstruct the six lost figures of 'Checking direction fields' (p=13193).

Every equation, sample spacing and highlighted region is stated in the post
text; nothing here is invented beyond plot ranges and styling.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = "/private/tmp/claude-501/-Users-jonathanshock-Cursor-folders-Mathematica/fa8467c2-86f9-4523-91a8-5388d8cc081c/scratchpad/pilot/"
NOTE = "figure reconstructed from the post text, 2026"
SEG  = 0.38          # segment length as a fraction of the sample spacing unit
LINE = dict(color="#1f4e79", lw=1.1, solid_capstyle="round")

def field(ax, f, xr, yr, step, seg_scale=SEG):
    # snap the lattice to multiples of `step` so that x=0 and y=0 are sampled;
    # the post's claims about y=0 and y=+-1.6 depend on those points existing
    def lattice(lo, hi):
        k0, k1 = int(np.ceil(lo / step - 1e-9)), int(np.floor(hi / step + 1e-9))
        return np.arange(k0, k1 + 1) * step
    xs, ys = lattice(*xr), lattice(*yr)
    L = seg_scale * step * 2
    for x in xs:
        for y in ys:
            with np.errstate(divide="ignore", invalid="ignore"):
                m = f(x, y)
            if m is None or not np.isfinite(m):
                dx, dy = 0.0, L / 2          # singular: vertical
            else:
                th = np.arctan(m)
                dx, dy = (L / 2) * np.cos(th), (L / 2) * np.sin(th)
            ax.plot([x - dx, x + dx], [y - dy, y + dy], **LINE)
    # pad beyond the sampled range so edge segments are not clipped in half
    pad = 0.7 * step
    ax.set_xlim(xr[0] - pad, xr[1] + pad)
    ax.set_ylim(yr[0] - pad, yr[1] + pad)
    ax.set_aspect("equal")
    ax.grid(True, color="#dddddd", lw=0.6)
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axvline(0, color="#999999", lw=0.8)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.tick_params(labelsize=8)

def finish(fig, name):
    fig.text(0.995, 0.006, NOTE, ha="right", va="bottom",
             fontsize=6.5, color="#9a9a9a")
    fig.savefig(OUT + name, dpi=110, facecolor="white",
                bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print("wrote", name)

# 1. dy/dx = x + y, half-integer sampling (left) and quarter-integer (right)
f1 = lambda x, y: x + y
fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.75))
for ax, step, lab in zip(axes, (0.5, 0.25),
                         ("sample spacing 0.5", "sample spacing 0.25")):
    field(ax, f1, (-3, 3), (-3, 3), step)
    ax.set_title(lab, fontsize=10)
fig.suptitle(r"$\frac{dy}{dx} = x + y$", fontsize=14, y=0.99)
finish(fig, "xplusy.png")

# 2. dy/dx = x / y
def f2(x, y):
    return np.inf if y == 0 else x / y
fig, ax = plt.subplots(figsize=(6.4, 6.5))
field(ax, f2, (-3, 3), (-3, 3), 0.5)
ax.set_title(r"$\frac{dy}{dx} = \frac{x}{y}$", fontsize=13)
finish(fig, "xovery.png")

# 3-6. dy/dx = sqrt(x+2) / tan(y), plain and with the boxes the post describes
def f3(x, y):
    t = np.tan(y)
    if abs(t) < 1e-9: return np.inf
    return np.sqrt(max(x + 2.0, 0.0)) / t

def tanfig(boxes, name, title):
    fig, ax = plt.subplots(figsize=(6.4, 6.5))
    field(ax, f3, (-2, 4), (-3, 3), 0.4)
    for (x0, y0, w, h) in boxes:
        ax.add_patch(Rectangle((x0, y0), w, h, fill=False,
                               edgecolor="#d02020", lw=1.8, zorder=5))
    ax.set_title(title, fontsize=13)
    finish(fig, name)

T = r"$\frac{dy}{dx} = \frac{\sqrt{x+2}}{\tan(y)}$"
tanfig([], "tan.png", T)
tanfig([(-2.20, -3.28, 0.40, 6.56)], "tanr1.png", T)          # x = -2, flat
tanfig([(-2.28, -0.20, 6.56, 0.40)], "tanr2.png", T)          # y = 0, vertical
tanfig([(-2.28, 1.42, 6.56, 0.36),
        (-2.28, -1.78, 6.56, 0.36)], "tanr3.png", T)          # y = +-1.6, flat
