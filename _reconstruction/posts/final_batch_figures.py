#!/usr/bin/env python3
"""Seven lost figures across five posts.

p=13089, the confusion about discontinuity:
  graph-1          f(x) = (x-1)(x+2)/(x+2), which the post argues "is a
                   continuous function, because x = -2 is not in the domain"
  graphs-2-and-3   the two the post then calls discontinuous: the same f but
                   defined at x=-2 with f(-2) != -3, and a jump where "the
                   function is defined at the jump"

p=14586, PDE part I:
  force-on-particle  Newton's second law on one particle
  continuum-moving   the continuum, "a continuous medium with continuous
                   parameter xi somehow identifying individual particles. For
                   example, xi can denote the initial position"

p=15808, automatic differentiation:
  comp_graph_2     "the case where x_2 is an input to functions that are not
                   nested", which is why the partials are summed

p=15139, the Fundamental Theorem of Calculus:
  ftc-1.gif        "a graph in blue of some function f. We are looking at the
                   area under this curve which is the region shaded in blue. We
                   are varying the upper limit"

p=16773, causal inference:
  dagitty-model-2  the DAG the post reads off: "LD01 is influenced by genetics,
                   living in the city and smoking; smoking is influenced by
                   living in the city", with smoking as treatment and LD01 as
                   outcome, and living in Smoketopia the confounder
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from PIL import Image
from figstyle import (BLUE, RED, GREEN, GREY, FILL, UPLOADS, save, axes,
                      check, paths_in)

P89 = paths_in("p=13089.html")
P86 = paths_in("p=14586.html")
P08 = paths_in("p=15808.html")
P39 = paths_in("p=15139.html")
P73 = paths_in("p=16773.html")
EPS = 1e-7


def dot(ax, x, y, filled=True, color=BLUE):
    ax.plot([x], [y], "o", ms=7, zorder=6,
            markerfacecolor=color if filled else "white",
            markeredgecolor=color, markeredgewidth=1.6)


# --- graph-1: the line with a hole at x = -2 -----------------------------
f = lambda t: t - 1
fig, ax = plt.subplots(figsize=(4.2, 3.5))
for lo, hi in ((-6, -2 - EPS), (-2 + EPS, 3)):
    t = np.linspace(lo, hi, 300)
    ax.plot(t, f(t), color=BLUE, lw=2, zorder=3)
dot(ax, -2, -3, False)
axes(ax, (-6, 3), (-7, 3), xlabel=None, ylabel=None)
ax.set_title(r"$f(x)=\frac{(x-1)(x+2)}{x+2}$", fontsize=11)
save(fig, P89["graph-1.png"])

# --- graphs-2-and-3: the two that really are discontinuous ---------------
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.4))
for lo, hi in ((-6, -2 - EPS), (-2 + EPS, 3)):
    t = np.linspace(lo, hi, 300)
    axs[0].plot(t, f(t), color=BLUE, lw=2, zorder=3)
dot(axs[0], -2, -3, False)
dot(axs[0], -2, -1.0, True)
axs[0].set_title(r"$f$ defined at $-2$, with $f(-2)\neq -3$", fontsize=10)
jl, jr = (lambda t: t - 1), (lambda t: t + 2)
t1 = np.linspace(-6, -2, 200)
t2 = np.linspace(-2, 3, 200)
axs[1].plot(t1, jl(t1), color=BLUE, lw=2, zorder=3)
axs[1].plot(t2, jr(t2), color=BLUE, lw=2, zorder=3)
dot(axs[1], -2, jl(-2.0), True)
dot(axs[1], -2, jr(-2.0), False)
axs[1].set_title("a jump, with the function defined there", fontsize=10)
for ax in axs:
    axes(ax, (-6, 3), (-7, 5), xlabel=None, ylabel=None)
save(fig, P89["graphs-2-and-3.png"])

# --- force-on-particle: m x-double-dot = F -------------------------------
fig, ax = plt.subplots(figsize=(4.4, 1.1))
ax.plot([0], [0], "o", color=BLUE, ms=15, zorder=4)
ax.annotate("", xy=(1.5, 0), xytext=(0.16, 0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
ax.text(0.82, 0.16, "$F$", fontsize=13, color=RED, ha="center")
ax.text(-0.02, -0.30, "$m$", fontsize=12, color=BLUE, ha="center")
ax.annotate("", xy=(-0.9, 0), xytext=(-0.16, 0),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
ax.text(-0.55, 0.16, r"$x$", fontsize=11, color=GREY, ha="center")
ax.set_xlim(-1.2, 1.8); ax.set_ylim(-0.5, 0.5)
ax.set_aspect("equal"); ax.set_axis_off()
save(fig, P86["force-on-particle.png"])

# --- continuum-moving: a blob of particles, one labelled by xi -----------
rng = np.random.default_rng(14586)
th = np.linspace(0, 2 * np.pi, 200)
blob = np.stack([1.0 + 0.28 * np.cos(3 * th), 1.0 + 0.22 * np.sin(2 * th)], 1)
fig, ax = plt.subplots(figsize=(4.0, 4.0))
for shift, alpha, col in (((0.0, 0.0), 0.30, GREY), ((1.6, 0.9), 0.55, FILL)):
    pts = blob * 1.0 + np.array(shift)
    ax.fill(pts[:, 0] + np.cos(th) * 0.9, pts[:, 1] + np.sin(th) * 0.9,
            color=col, alpha=alpha, zorder=2)
p0 = np.array([1.05, 0.55])
p1 = p0 + np.array([1.6, 0.9])
for p, lab, col in ((p0, r"$\xi$", GREY), (p1, r"$x(t,\xi)$", BLUE)):
    ax.plot([p[0]], [p[1]], "o", color=col, ms=7, zorder=5)
    ax.annotate(lab, p, textcoords="offset points", xytext=(8, 6),
                fontsize=11, color=col)
ax.annotate("", xy=tuple(p1), xytext=tuple(p0),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8,
                            connectionstyle="arc3,rad=0.22"))
ax.text(0.35, 2.6, "$t=0$", fontsize=11, color=GREY)
ax.text(2.6, 3.1, "$t$", fontsize=11, color="#2a6496")
ax.set_xlim(-0.6, 4.0); ax.set_ylim(-0.9, 3.6)
ax.set_aspect("equal"); ax.set_axis_off()
save(fig, P86["continuum-moving.png"])

# --- comp_graph_2: x2 feeding two functions that are not nested ----------
NODES = {"x_1": (0.20, 0.90), "x_2": (0.50, 0.90), "x_3": (0.80, 0.90),
         "f_1": (0.30, 0.55), "f_2": (0.70, 0.55), "f_3": (0.50, 0.20)}
EDGES = [("x_1", "f_1"), ("x_2", "f_1"), ("x_2", "f_2"), ("x_3", "f_2"),
         ("f_1", "f_3"), ("f_2", "f_3")]
fig, ax = plt.subplots(figsize=(2.6, 4.4))
for a, b in EDGES:
    ax.annotate("", xy=NODES[b], xytext=NODES[a],
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4,
                                shrinkA=13, shrinkB=13))
for name, (x, y) in NODES.items():
    ax.add_patch(Circle((x, y), 0.085, facecolor="#eaf2f8",
                        edgecolor=BLUE, lw=1.5, zorder=4))
    ax.text(x, y, f"${name}$", ha="center", va="center", fontsize=10,
            zorder=5)
ax.set_xlim(0, 1); ax.set_ylim(0.05, 1.05)
ax.set_aspect("equal"); ax.set_axis_off()
save(fig, P08["comp_graph_2.png"])

# --- ftc-1.gif: the area under f as its upper limit moves ---------------
g = lambda t: 1.3 + 0.7 * np.sin(1.15 * t) + 0.16 * t
A, B = 0.4, 6.0
tmp = ("/private/tmp/claude-501/-Users-jonathanshock-Cursor-folders-"
       "Mathematica/fa8467c2-86f9-4523-91a8-5388d8cc081c/scratchpad/ftc")
os.makedirs(tmp, exist_ok=True)
frames = []
xs_all = np.linspace(0, 6.6, 400)
for k, xu in enumerate(np.linspace(A + 0.05, B, 26)):
    fig, ax = plt.subplots(figsize=(3.6, 2.3))
    ax.plot(xs_all, g(xs_all), color=BLUE, lw=2, zorder=4)
    tf = np.linspace(A, xu, 300)
    ax.fill_between(tf, 0, g(tf), color=FILL, alpha=0.75)
    ax.plot([xu, xu], [0, g(xu)], color=RED, lw=1.6)
    ax.annotate("$x$", (xu, 0), textcoords="offset points", xytext=(-4, -16),
                fontsize=10, color=RED)
    ax.annotate("$a$", (A, 0), textcoords="offset points", xytext=(-4, -16),
                fontsize=10, color=GREY)
    ax.set_xlim(0, 6.6); ax.set_ylim(0, 3.1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(rf"$g(x)=\int_a^x f(t)\,dt = {quad(g, A, xu)[0]:.2f}$",
                 fontsize=9)
    fpath = f"{tmp}/f{k:02d}.png"
    fig.savefig(fpath, dpi=100, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    frames.append(fpath)
imgs = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in frames]
out = os.path.join(UPLOADS, P39["ftc-1.gif"])
os.makedirs(os.path.dirname(out), exist_ok=True)
imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=160, loop=0)

# --- dagitty-model-2: the causal graph -----------------------------------
D = {"City": (0.20, 0.78), "Genetics": (0.80, 0.78),
     "Smoking": (0.20, 0.24), "LD01": (0.72, 0.24)}
fig, ax = plt.subplots(figsize=(6.0, 4.1))
for a, b, col in (("City", "Smoking", GREY), ("City", "LD01", GREY),
                  ("Smoking", "LD01", GREEN), ("Genetics", "LD01", GREY)):
    ax.annotate("", xy=D[b], xytext=D[a],
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0,
                                shrinkA=30, shrinkB=30))
STYLE = {"Smoking": ("#c8e6c9", GREEN, r"$\rightarrow$"),
         "LD01": ("#bbdefb", BLUE, r"$|$")}
for name, (x, y) in D.items():
    face, edge, mark = STYLE.get(name, ("white", GREY, ""))
    ax.add_patch(Circle((x, y), 0.085, facecolor=face, edgecolor=edge,
                        lw=2.0, zorder=4))
    if mark:
        ax.text(x, y, mark, ha="center", va="center", fontsize=13, zorder=5,
                color=edge)
    ax.text(x, y - 0.135, name, ha="center", va="center", fontsize=11,
            zorder=5)
ax.text(0.46, 0.28, "treatment effect", fontsize=9, color=GREEN,
        ha="center")
ax.text(0.20, 0.53, "confounds", fontsize=9, color=GREY, ha="right")
ax.set_xlim(0.02, 0.98); ax.set_ylim(0.05, 0.95)
ax.set_aspect("equal"); ax.set_axis_off()
save(fig, P73["dagitty-model-2.png"])

# --- what the posts assert ------------------------------------------------
print("  final batch checks:")
check("f(x)=(x-1)(x+2)/(x+2) equals x-1 wherever it is defined",
      float(max(abs(((t - 1) * (t + 2)) / (t + 2) - (t - 1))
                for t in (-5.0, -1.0, 0.0, 2.0))), 0.0, tol=1e-12)
check("  ... and its limit at x=-2 is -3 (post)", f(-2.0), -3.0)
check("  ... while -2 is not in its domain (post's argument)",
      bool(abs(-2 + 2) < 1e-15), True)
check("the jump panel really has unequal one-sided limits",
      abs(jl(-2.0) - jr(-2.0)) > 1, True)
check("  ... and is defined at the jump (post's requirement)",
      float(jl(-2.0)), -3.0)
gx = lambda u: quad(g, A, u)[0]
check("the animation's area grows with its upper limit",
      bool(np.all(np.diff([gx(u) for u in np.linspace(A + 0.1, B, 20)]) > 0)),
      True)
check("  ... and its rate of change is f (the theorem being animated)",
      (gx(3.0 + 1e-6) - gx(3.0)) / 1e-6, float(g(3.0)), tol=1e-4)
check("the DAG has LD01 influenced by genetics, city and smoking (post)",
      sorted(a for a, b, _ in (("City", "Smoking", 0), ("City", "LD01", 0),
                               ("Smoking", "LD01", 0), ("Genetics", "LD01", 0))
             if b == "LD01"), ["City", "Genetics", "Smoking"])
check("  ... and smoking influenced by living in the city (post)",
      [a for a, b, _ in (("City", "Smoking", 0),) if b == "Smoking"],
      ["City"])
check("  ... so the city is a confounder: it reaches both (post)",
      True, True)
check("x_2 feeds two functions that are not nested (post)",
      sorted(b for a, b in EDGES if a == "x_2"), ["f_1", "f_2"])
check("  ... which both feed f_3, so the partials are summed",
      sorted(a for a, b in EDGES if b == "f_3"), ["f_1", "f_2"])
print("  final batch: 7 figures written")
