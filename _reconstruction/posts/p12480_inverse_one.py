#!/usr/bin/env python3
"""p=12480, "Can we find the inverse of a function which is not one-to-one?
(part one)".

Four lost figures. The text fixes the colours: the three panels of domains.png
are blue, green and red, "the graph of the function on the left doesn't have an
inverse, but the middle and right functions do", so blue is x^2 unrestricted
and green and red are the two halves. domains2-1.png then shows "the graphs
above (dashed blue, green and red)" with their reflections in y=x solid and the
line itself dashed black.

The post has a small slip after the second figure, "the green and blue solid
lines do", where it means green and red; nothing here depends on it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREEN, GREY, save, axes, check, paths_in

P = paths_in("p=12480.html")
DOMAINS = [("all of $\\mathbb{R}$", (-2.2, 2.2), BLUE),
           (r"restricted to $[0,\infty)$", (0, 2.2), GREEN),
           (r"restricted to $(-\infty,0]$", (-2.2, 0), RED)]


def frame(ax):
    axes(ax, None, None, xlabel=None, ylabel=None)
    ax.tick_params(labelsize=7)


# --- domains.png (669x140): the three restrictions of x^2 -----------------
fig, axs = plt.subplots(1, 3, figsize=(9.0, 1.95))
for ax, (lab, (lo, hi), col) in zip(axs, DOMAINS):
    x = np.linspace(lo, hi, 300)
    ax.plot(x, x ** 2, color=col, lw=2)
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-0.4, 5.0)
    frame(ax)
    ax.set_title(lab, fontsize=8.5)
save(fig, P["domains.png"])

# --- domains2-1.png (669x229): each with its reflection in y=x -----------
fig, axs = plt.subplots(1, 3, figsize=(9.0, 3.15))
for ax, (lab, (lo, hi), col) in zip(axs, DOMAINS):
    x = np.linspace(lo, hi, 400)
    ax.plot(x, x ** 2, color=col, lw=1.6, ls="--")
    ax.plot(x ** 2, x, color=col, lw=2.2)          # reflected in y = x
    ax.plot([-2.4, 5.0], [-2.4, 5.0], color="black", lw=1.0, ls="--")
    ax.set_xlim(-2.4, 5.0); ax.set_ylim(-2.4, 5.0)
    ax.set_aspect("equal")
    frame(ax)
    ax.set_title(lab, fontsize=8.5)
save(fig, P["domains2-1.png"])

# --- sinarcsin.png (742x743): sin reflected in y=x is not a function -----
fig, ax = plt.subplots(figsize=(6.4, 6.4))
t = np.linspace(-3 * np.pi, 3 * np.pi, 2000)
ax.plot(t, np.sin(t), color=BLUE, lw=1.5, ls="--", label=r"$y=\sin x$")
ax.plot(np.sin(t), t, color=BLUE, lw=2.0,
        label=r"$y=\sin x$ reflected in $y=x$")
ax.plot([-9.6, 9.6], [-9.6, 9.6], color="black", lw=1.0, ls="--",
        label="$y=x$")
ax.set_xlim(-9.6, 9.6); ax.set_ylim(-9.6, 9.6)
ax.set_aspect("equal")
frame(ax)
ax.legend(fontsize=9, frameon=False, loc="upper left")
save(fig, P["sinarcsin.png"])

# --- invsin.png (467x467): sin on [-pi/2, pi/2] and its inverse ---------
fig, ax = plt.subplots(figsize=(4.6, 4.6))
t = np.linspace(-np.pi / 2, np.pi / 2, 500)
ax.plot(t, np.sin(t), color=BLUE, lw=2, label=r"$y=\sin x$")
ax.plot(np.sin(t), t, color=GREEN, lw=2, label=r"$y=\arcsin x$")
ax.plot([-1.8, 1.8], [-1.8, 1.8], color="black", lw=1.0, ls="--",
        label="$y=x$")
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
ax.set_aspect("equal")
frame(ax)
ax.legend(fontsize=9, frameon=False, loc="upper left")
save(fig, P["invsin.png"])

# --- the claims the post makes -------------------------------------------
print("  p=12480 checks:")
check("f(x)=x+3 has inverse x-3", (5 + 3) - 3, 5)
check("x^2 is two-to-one: 3 and -3 both give 9", 3 ** 2, (-3) ** 2)
check("sqrt undoes x^2 only on [0,inf): sqrt((-3)^2) is 3, not -3",
      np.sqrt((-3) ** 2), 3)
check("sin is one-to-one on [-pi/2, pi/2]",
      bool(np.all(np.diff(np.sin(np.linspace(-np.pi / 2, np.pi / 2, 500))) > 0)),
      True)
check("arcsin(sin(x)) = x there", np.arcsin(np.sin(1.2)), 1.2)
check("the fundamental domain [0, 2pi) is still not one-to-one: "
      "sin(pi/6) = sin(5pi/6)", np.sin(np.pi / 6), np.sin(5 * np.pi / 6))
print("  p=12480: 4 figures written")
