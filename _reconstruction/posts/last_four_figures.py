#!/usr/bin/env python3
"""The last four recoverable figures.

p=15219, SA Mathematics Olympiad problem 2:
  problem2_sketch  triangle ABC with AB=AC, D on BC, E on AC, F on AB, DE=DC,
                   DF=DB, DC/BD=2 and AF/AE=5. The post says its sketch is
                   "more accurate than it needs to be because when I was
                   creating it, I already knew what all of the lengths in the
                   problem work out to be", so this one is drawn to the exact
                   solution: AB/BC = sqrt(3)/2, which gives AF/AE = 5 exactly.

p=15343, problem 4:
  problem4_sketch  triangle ABC, its altitudes meeting at H, an arbitrary P,
                   and D, E, F the feet of the perpendiculars from P onto the
                   three altitudes, "with the circle that passes through P, E,
                   D, H, and F" drawn in as the post says it drew it. Both the
                   concyclicity and the area identity are checked here.

p=11480, MAM1000 part 36:
  flow             the flow for the post's worked example, y' - y/2 = 4 sin(3t),
                   whose general solution it gives as
                   -(8/37)(6 cos 3t - sin 3t) + c e^{t/2}. That sign is wrong:
                   substituting it gives 140 sin(3t)/37 + 48 cos(3t)/37 rather
                   than 4 sin(3t). The correct particular solution has a plus
                   on the sine, and that is what is drawn.

p=16082, the Res-Net-NODE narrative:
  Screenshot-119   "an example of this kind of structure ... a single residual
                   unit", for x_{k+1} = x_k + p(W_k x_k + b_k)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from figstyle import (BLUE, RED, GREEN, GREY, SERIES, save, axes, check,
                      paths_in, direction_field)

P19 = paths_in("p=15219.html")
P43 = paths_in("p=15343.html")
P80 = paths_in("p=11480.html")
P82 = paths_in("p=16082.html")


def label(ax, p, text, off=(8, 8), color="black", size=11):
    ax.plot([p[0]], [p[1]], "o", color=color, ms=5, zorder=6)
    ax.annotate(text, p, textcoords="offset points", xytext=off,
                fontsize=size, color=color)


# --- problem2_sketch ------------------------------------------------------
a = 2.0
b = np.sqrt(3) / 2 * a                       # the answer: AB/BC = sqrt(3)/2
B2 = np.array([0.0, 0.0])
C2 = np.array([a, 0.0])
A2 = np.array([a / 2, np.sqrt(b ** 2 - (a / 2) ** 2)])
D2 = B2 + (C2 - B2) * (1 / 3)                # BD : DC = 1 : 2
cosB = (a / 2) / b
F2 = B2 + (A2 - B2) / b * (2 * (a / 3) * cosB)      # BF = 2 BD cos B
E2 = C2 + (A2 - C2) / b * (2 * (2 * a / 3) * cosB)  # CE = 2 DC cos C
fig, ax = plt.subplots(figsize=(5.4, 4.4))
ax.plot(*zip(A2, B2, C2, A2), color=BLUE, lw=2, zorder=3)
for p, q, col in ((D2, E2, RED), (D2, F2, RED)):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=1.8, zorder=4)
for p, t, off in ((A2, "$A$", (-4, 8)), (B2, "$B$", (-16, -6)),
                  (C2, "$C$", (6, -6)), (D2, "$D$", (-4, -18)),
                  (E2, "$E$", (8, 0)), (F2, "$F$", (-18, 2))):
    label(ax, p, t, off)
ax.set_xlim(-0.35, 2.35); ax.set_ylim(-0.45, 1.85)
ax.set_aspect("equal"); ax.set_axis_off()
ax.set_title(r"$DE=DC$, $DF=DB$, $\frac{DC}{BD}=2$, $\frac{AF}{AE}=5$",
             fontsize=10)
save(fig, P19["problem2_sketch.png"])


# --- problem4_sketch ------------------------------------------------------
def circumcentre(p, q, r):
    (ax_, ay), (bx, by), (cx, cy) = p, q, r
    d = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax_ ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay)
          + (cx ** 2 + cy ** 2) * (ay - by)) / d
    uy = ((ax_ ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax_ - cx)
          + (cx ** 2 + cy ** 2) * (bx - ax_)) / d
    return np.array([ux, uy])


def foot(P, A, d):
    d = d / np.linalg.norm(d)
    return A + np.dot(P - A, d) * d


A4 = np.array([0.3, 2.6]); B4 = np.array([-1.8, -0.7]); C4 = np.array([2.4, -0.5])
O4 = circumcentre(A4, B4, C4)
R4 = float(np.linalg.norm(A4 - O4))
H4 = A4 + B4 + C4 - 2 * O4
P4 = np.array([1.2, 1.1])
D4, E4, F4 = (foot(P4, A4, H4 - A4), foot(P4, B4, H4 - B4),
              foot(P4, C4, H4 - C4))
ctr = circumcentre(P4, D4, E4)
rad = float(np.linalg.norm(P4 - ctr))
fig, ax = plt.subplots(figsize=(5.8, 5.4))
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(ctr[0] + rad * np.cos(th), ctr[1] + rad * np.sin(th), color=GREY,
        lw=1.2, ls="--", zorder=2)
ax.plot(*zip(A4, B4, C4, A4), color=BLUE, lw=2, zorder=3)
for V, col in ((A4, SERIES[0]), (B4, SERIES[1]), (C4, SERIES[2])):
    d = H4 - V
    ax.plot([V[0] - 0.6 * d[0], V[0] + 1.9 * d[0]],
            [V[1] - 0.6 * d[1], V[1] + 1.9 * d[1]], color=col, lw=1.1,
            ls=":", zorder=3)
ax.plot(*zip(D4, E4, F4, D4), color=RED, lw=1.8, zorder=5)
for p, t, off in ((A4, "$A$", (-4, 8)), (B4, "$B$", (-18, -6)),
                  (C4, "$C$", (8, -6)), (H4, "$H$", (6, -14)),
                  (P4, "$P$", (8, 4)), (D4, "$D$", (6, 6)),
                  (E4, "$E$", (6, 6)), (F4, "$F$", (-18, 4))):
    label(ax, p, t, off)
ax.set_aspect("equal"); ax.set_axis_off()
ax.set_title(r"area$(DEF)=\frac{PH^2}{4R^2}\,$area$(ABC)$", fontsize=11)
save(fig, P43["problem4_sketch.png"])

# --- flow: the worked first-order linear example -------------------------
# The post writes the particular solution as -(8/37)(6 cos 3t - sin 3t), but
# that does not satisfy its own equation: substituting gives
# 140 sin(3t)/37 + 48 cos(3t)/37, not 4 sin(3t). The sine term's sign is wrong.
# sympy's dsolve gives C exp(t/2) - 8 sin(3t)/37 - 48 cos(3t)/37, which is
# -(8/37)(6 cos 3t + sin 3t) + c exp(t/2). That is what is drawn.
sol = lambda t, c: -(8 / 37) * (6 * np.cos(3 * t) + np.sin(3 * t)) \
    + c * np.exp(t / 2)
fig, ax = plt.subplots(figsize=(4.6, 7.4))
direction_field(ax, lambda t, y: y / 2 + 4 * np.sin(3 * t), (-3, 3), (-6, 6),
                0.5)
tt = np.linspace(-3, 3, 700)
for c, col in zip((-1.2, -0.4, 0.0, 0.4, 1.2), SERIES):
    y = sol(tt, c)
    m = np.abs(y) <= 6.4
    ax.plot(tt[m], y[m], color=col, lw=2, zorder=6)
axes(ax, None, None, xlabel=None, ylabel=None)
ax.set_title(r"$y'-\frac{y}{2}=4\sin(3t)$", fontsize=12)
save(fig, P80["flow.png"])

# --- Screenshot-119: one residual unit ------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 4.2))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_axis_off()
BOXES = [(0.30, 0.42, r"$W_k\cdot x_k+b_k$"), (0.52, 0.42, r"$p(\cdot)$")]
for x, w, txt in BOXES:
    ax.add_patch(FancyBboxPatch((x - w / 2 * 0.34, 0.42), 0.16, 0.16,
                                boxstyle="round,pad=0.012",
                                facecolor="#eaf2f8", edgecolor=BLUE, lw=1.6))
    ax.text(x - w / 2 * 0.34 + 0.08, 0.50, txt, ha="center", va="center",
            fontsize=12)
ax.add_patch(Circle((0.76, 0.50), 0.035, facecolor="white", edgecolor=GREEN,
                    lw=1.8, zorder=4))
ax.text(0.76, 0.50, "$+$", ha="center", va="center", fontsize=14,
        color=GREEN, zorder=5)
for a_, b_ in ((0.14, 0.23), (0.39, 0.44), (0.60, 0.723), (0.797, 0.88)):
    ax.annotate("", xy=(b_, 0.50), xytext=(a_, 0.50),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.annotate("", xy=(0.76, 0.535), xytext=(0.16, 0.80),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6,
                            connectionstyle="arc3,rad=-0.18"))
ax.text(0.44, 0.85, "identity (the skip connection)", fontsize=11,
        color=GREEN, ha="center")
ax.text(0.11, 0.50, "$x_k$", fontsize=14, ha="center", va="center")
ax.text(0.92, 0.50, "$x_{k+1}$", fontsize=14, ha="center", va="center")
ax.text(0.50, 0.24, r"$x_{k+1}=x_k+p(W_k\cdot x_k+b_k)$", fontsize=13,
        ha="center")
save(fig, P82["Screenshot-119.png"])

# --- what the posts assert ------------------------------------------------
def area(p, q, r):
    return abs(float(np.cross(np.append(q - p, 0), np.append(r - p, 0))[2])) / 2


print("  last four checks:")
check("P2: AB = AC as the problem requires",
      float(np.linalg.norm(A2 - B2)), float(np.linalg.norm(A2 - C2)))
check("P2: DC/BD = 2 (given)", float(np.linalg.norm(D2 - C2)
      / np.linalg.norm(B2 - D2)), 2.0)
check("P2: DF = DB (given)", float(np.linalg.norm(D2 - F2)),
      float(np.linalg.norm(D2 - B2)))
check("P2: DE = DC (given)", float(np.linalg.norm(D2 - E2)),
      float(np.linalg.norm(D2 - C2)))
check("P2: AF/AE = 5 (given)", float(np.linalg.norm(A2 - F2)
      / np.linalg.norm(A2 - E2)), 5.0, tol=1e-9)
check("P2: so AB/BC = sqrt(3)/2 (the answer)",
      float(np.linalg.norm(A2 - B2) / np.linalg.norm(B2 - C2)),
      np.sqrt(3) / 2)
for V, name in ((A4, "A"), (B4, "B"), (C4, "C")):
    other = [X for X in (A4, B4, C4) if X is not V]
    check(f"P4: the altitude through {name} is perpendicular to the "
          f"opposite side", float(np.dot(H4 - V, other[0] - other[1])), 0.0,
          tol=1e-9)
for X, nm in ((D4, "D"), (E4, "E"), (F4, "F"), (H4, "H")):
    check(f"P4: {nm} lies on the drawn circle",
          float(np.linalg.norm(X - ctr)), rad, tol=1e-9)
check("P4: area(DEF) = PH^2/(4R^2) area(ABC) (the thing to prove)",
      area(D4, E4, F4),
      float(np.linalg.norm(P4 - H4) ** 2 / (4 * R4 ** 2)) * area(A4, B4, C4),
      tol=1e-9)
d = 1e-6
check("flow: the drawn solution satisfies y' - y/2 = 4 sin 3t "
      "(the post's own sign on the sine term does not)",
      float((sol(1.0 + d, 0.4) - sol(1.0 - d, 0.4)) / (2 * d)
            - sol(1.0, 0.4) / 2), float(4 * np.sin(3.0)), tol=1e-6)
check("  ... for any c", float((sol(-2.0 + d, -1.2) - sol(-2.0 - d, -1.2))
      / (2 * d) - sol(-2.0, -1.2) / 2), float(4 * np.sin(-6.0)), tol=1e-6)
print("  last four: 4 figures written")
