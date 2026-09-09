#!/usr/bin/env python3
"""Three lost figures, one each on three posts.

p=12930, "The Newton-Raphson Method":
  plot2  the zoom on the first guess. The post fixes everything about it: the
         function is y(x) = x^2 - 3, the guess is x = 2 where y(2) = 1, and
         "The yellow line in the above is the tangent line", whose equation the
         post then works out as y = 4x - 7. Its sibling plot1-1.jpg survives on
         the same post and is drawn in the xkcd style, which the post says
         outright ("we've implemented the xkcd Mathematica style using the code
         here"), so this one is drawn that way too.

p=10779, "integration by substitution":
  xtou   "Looking of the graphs written in both the x variable and the u
         variable they look very different. The point is that the area is still
         the same." The two integrals are the post's own worked example:
         1/(x (ln x)^3) from e to e^2, and 1/u^3 from 1 to 2, both equal to 3/8.

p=14624, "The Recaman sequence":
  Recaman  the post gives the Mathematica that drew it, in full, and this is a
         port of that code rather than a fresh idea of what it should look
         like: 66 terms from the loop `For[i = 1, i < 66, i++, ...]`, then a
         semicircle on each consecutive pair, centred at their midpoint with
         radius half their difference, alternating above and below the axis
         through the arc range {i Pi, (i+1) Pi}, over a base line drawn from
         x = 0 to x = 91.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, FILL, GREY, save, axes, check, paths_in

P30 = paths_in("p=12930.html")
P79 = paths_in("p=10779.html")
P24 = paths_in("p=14624.html")

# --- plot2: the tangent at the first guess, in the post's xkcd style ------
y = lambda x: x ** 2 - 3
tangent = lambda x: 4 * x - 7
with plt.xkcd(scale=0.9, length=110, randomness=2):
    fig, ax = plt.subplots(figsize=(3.93, 2.13))
    xs = np.linspace(1.62, 2.12, 300)
    # the tangent is drawn thick and the curve over it, so the two are both
    # visible where they touch and separate visibly on either side
    ax.plot(xs, tangent(xs), color="#e8b800", lw=3.4)
    ax.plot(xs, y(xs), color="#6b7fd7", lw=1.8)
    ax.plot([2], [1], "o", color="black", ms=5)
    ax.plot([7 / 4], [0], "o", color="black", ms=5)
    ax.annotate("(2, 1)", (2, 1), textcoords="offset points", xytext=(-34, 4),
                fontsize=9)
    ax.annotate("$x=7/4$", (7 / 4, 0), textcoords="offset points",
                xytext=(-18, -30), fontsize=9,
                arrowprops=dict(arrowstyle="-", color="black", lw=1.2))
    ax.plot(xs, 0 * xs, color="black", lw=2)
    ax.set_xlim(1.62, 2.12); ax.set_ylim(-0.65, 1.35)
    ax.set_xticks([1.75, 2.0]); ax.set_yticks([0, 1])
    for sp in ("top", "right", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_position(("data", 1.62))
    ax.set_xlabel("x"); ax.set_ylabel("y(x)")
    ax.set_title("the tangent at the first guess", fontsize=10)
    save(fig, P30["plot2.jpg"])

# --- xtou: the same area, in x and in u ----------------------------------
fx = lambda x: 1 / (x * np.log(x) ** 3)
fu = lambda u: 1 / u ** 3
fig, axs = plt.subplots(1, 2, figsize=(6.69, 2.21))
xs = np.linspace(np.e * 0.92, np.e ** 2 * 1.05, 400)
axs[0].plot(xs, fx(xs), color=BLUE, lw=2)
sh = np.linspace(np.e, np.e ** 2, 300)
axs[0].fill_between(sh, 0, fx(sh), color=FILL, alpha=0.6)
axes(axs[0], (xs[0], xs[-1]), (0, 0.55), spines="box", xlabel="$x$",
     ylabel=None)
axs[0].set_xticks([np.e, np.e ** 2]); axs[0].set_xticklabels(["$e$", "$e^2$"])
axs[0].set_title(r"$\int_e^{e^2}\frac{dx}{x(\ln x)^3}$", fontsize=10)
us = np.linspace(0.9, 2.15, 400)
axs[1].plot(us, fu(us), color=RED, lw=2)
sh = np.linspace(1, 2, 300)
axs[1].fill_between(sh, 0, fu(sh), color=FILL, alpha=0.6)
axes(axs[1], (0.9, 2.15), (0, 1.35), spines="box", xlabel="$u$", ylabel=None)
axs[1].set_xticks([1, 2])
axs[1].set_title(r"$\int_1^2\frac{du}{u^3}=\frac{3}{8}$", fontsize=10)
save(fig, P79["xtou.jpg"])

# --- Recaman: a port of the post's own Mathematica -----------------------
nums = [0]
for i in range(1, 66):
    back = nums[-1] - i
    nums.append(back if back > 0 and back not in nums else nums[-1] + i)

fig, ax = plt.subplots(figsize=(11.0, 6.4))
for i in range(len(nums) - 1):
    a, b = nums[i], nums[i + 1]
    c, r = (a + b) / 2, abs(b - a) / 2
    th = np.linspace(i * np.pi, (i + 1) * np.pi, 200)
    ax.plot(c + r * np.cos(th), r * np.sin(th), color=BLUE, lw=1.0)
# Plot[0, {x, 0, 91}] draws the base line over 0 to 91 only; Show expands the
# view to hold the graphics, and the widest arc reaches x = 114.
ax.plot([0, 91], [0, 0], color="black", lw=1.0)
ax.set_xlim(-3, 117); ax.set_ylim(-34, 34)
ax.set_aspect("equal")
ax.set_yticks([])
ax.spines["left"].set_visible(False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_position("zero")
ax.set_xticks([0, 20, 40, 60, 80])
ax.set_title("the first 66 terms of the Recamán sequence", fontsize=12)
save(fig, P24["Recaman.jpg"])

# --- what the posts assert ------------------------------------------------
print("  three singletons checks:")
check("y(2) = 2^2 - 3 = 1 (post)", y(2), 1)
check("the gradient there is y'(2) = 4 (post)", 2 * 2, 4)
check("so the tangent is y = 4x - 7 (post)",
      [tangent(2), tangent(0)], [1, -7])
check("  ... and it cuts the axis at 7/4", 7 / 4, -(-7) / 4)
check("  ... which is nearer sqrt(3) than the guess of 2 was",
      abs(7 / 4 - np.sqrt(3)) < abs(2 - np.sqrt(3)), True)
check("the x-integral is 3/8 (post)", round(quad(fx, np.e, np.e ** 2)[0], 12),
      0.375)
check("  ... and so is the u-integral, which is the point (post)",
      round(quad(fu, 1, 2)[0], 12), 0.375)
check("  ... u = ln x sends the limits e and e^2 to 1 and 2 (post)",
      [float(np.log(np.e)), float(np.log(np.e ** 2))], [1.0, 2.0])
check("the Recaman loop gives 66 terms (post's For[i = 1, i < 66, i++])",
      len(nums), 66)
check("  ... starting 0, 1, 3, 6, 2, 7, 13, 20, 12, 21", nums[:10],
      [0, 1, 3, 6, 2, 7, 13, 20, 12, 21])
check("  ... and reaching 91, which is where the post's base line stops",
      nums[-1], 91)
check("  ... though the arcs run out to x = 114, past the end of that line",
      max((a + b) / 2 + abs(b - a) / 2 for a, b in zip(nums, nums[1:])), 114.0)
check("  ... with consecutive terms differing by exactly i",
      [abs(nums[i + 1] - nums[i]) for i in range(1, 6)], [2, 3, 4, 5, 6])
check("  ... so each arc's radius is i/2, as the code's Abs[Differences]/2 says",
      [abs(nums[i + 1] - nums[i]) / 2 for i in (10, 20)], [5.5, 10.5])
# The Position test blocks a backward step onto a value already seen, but says
# nothing about forward steps, and four of these 66 terms do repeat.
back_ok = all(nums[i] != nums[i - 1] - i or nums[i] not in nums[:i]
              for i in range(1, len(nums)))
check("  ... every backward step lands somewhere new, which is what the code's "
      "Position test enforces", back_ok, True)
check("  ... while forward steps may revisit, so 66 terms take 62 values",
      len(set(nums)), 62)
print("  three singletons: 3 figures written")
