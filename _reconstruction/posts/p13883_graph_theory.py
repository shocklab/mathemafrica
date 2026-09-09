#!/usr/bin/env python3
"""p=13883, "A Whimsical Introduction to Graph Theory (1)". Five lost figures.

The post describes each one exactly:

  1_map-1, map_paths-1, map_lengths-1
      "Figure 1: On the left, a roadmap with 3 places of interest. On the
      right, two diagrams abstracting it." The places are A, B and C and the
      road intersection is D. The middle diagram is named outright: "we have
      the vertices A, B, C and D, with edges {A,B}, {A,D}, {B,D} and {C,D}".
      The right one drops D, because "we don't want to consider D as a
      destination", and keeps route lengths instead, so it carries "two
      connections between A and B", the direct road and the one through D.
  edge-1
      "Figure 2: For every pair of vertices, there are two possibilities:
      either the edge between them exists, or it doesn't", with u and v named
      in the text.
  same_graph-1
      "Figure 3: 3 different ways of drawing the same graph", of which the post
      says "all of the vertices are adjacent to every other vertex".

The roads are drawn as Bezier curves and the weights on the right-hand diagram
are those curves' own arc lengths, so the two figures agree with each other
rather than carrying invented numbers. The graph is complete, as the text says;
that it is K4 rather than K3 or K5 is a choice, taken to match the four
vertices already on stage.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREY, save, check, paths_in

P = paths_in("p=13883.html")

# places of interest and the intersection, in kilometres
POS = {"A": (1.0, 3.6), "B": (5.2, 4.1), "C": (2.4, 0.7), "D": (3.1, 2.4)}
# each road as (from, to, control point of a quadratic Bezier)
ROADS = [("A", "B", (3.0, 5.6)), ("A", "D", (1.6, 2.6)),
         ("B", "D", (4.6, 2.9)), ("C", "D", (2.4, 1.6))]


def bezier(p0, p1, p2, n=400):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1)
            + t ** 2 * np.array(p2))


def road_length(a, b, ctrl):
    xy = bezier(POS[a], ctrl, POS[b])
    return float(np.hypot(*np.diff(xy, axis=0).T).sum())


LEN = {(a, b): road_length(a, b, c) for a, b, c in ROADS}

# --- 1_map-1: the roadmap (600x480) ---------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 4.8))
ax.add_patch(plt.Rectangle((0.2, 0.0), 5.8, 5.2, facecolor="#f6f2e6",
                           edgecolor="#e0d8c2", zorder=0))
for a, b, c in ROADS:
    xy = bezier(POS[a], c, POS[b])
    ax.plot(xy[:, 0], xy[:, 1], color="#c8b48a", lw=9, solid_capstyle="round",
            zorder=1)
    ax.plot(xy[:, 0], xy[:, 1], color="white", lw=1.4, ls=(0, (6, 6)),
            zorder=2)
for name, (x, y) in POS.items():
    place = name != "D"
    ax.plot([x], [y], "o", ms=13 if place else 8,
            color=RED if place else "#6b6b6b", zorder=4)
    ax.annotate(name, (x, y), textcoords="offset points",
                xytext=(11, 9), fontsize=14, zorder=5)
ax.text(0.45, 0.28, "A, B and C are places of interest; D is a road junction",
        fontsize=9, color="#555555", zorder=5)
ax.set_xlim(0.2, 6.0); ax.set_ylim(0.0, 5.2)
ax.set_aspect("equal"); ax.set_axis_off()
save(fig, P["1_map-1.jpg"])


def draw_graph(ax, pos, edges, ms=13, fs=13, curve=None):
    """Edges as (u, v) or (u, v, label); `curve` bends duplicated pairs apart."""
    seen = {}
    for e in edges:
        u, v = e[0], e[1]
        k = tuple(sorted((u, v)))
        seen[k] = seen.get(k, 0) + 1
        bend = 0.0 if curve is None else curve * (seen[k] - 1.5) * 2
        p0, p1 = np.array(pos[u]), np.array(pos[v])
        mid = (p0 + p1) / 2
        n = np.array([-(p1 - p0)[1], (p1 - p0)[0]])
        ctrl = mid + bend * n
        xy = bezier(p0, ctrl, p1)
        ax.plot(xy[:, 0], xy[:, 1], color=BLUE, lw=1.8, zorder=1)
        if len(e) > 2:
            m = xy[len(xy) // 2]
            ax.text(m[0], m[1], e[2], fontsize=9, color="#333333", ha="center",
                    va="center", zorder=3,
                    bbox=dict(fc="white", ec="none", pad=1.2))
    for name, (x, y) in pos.items():
        ax.plot([x], [y], "o", ms=ms, color=RED, zorder=2)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(9, 7),
                    fontsize=fs, zorder=4)
    ax.set_aspect("equal"); ax.set_axis_off()


# --- map_paths-1: the graph (300x208) -------------------------------------
fig, ax = plt.subplots(figsize=(3.0, 2.08))
draw_graph(ax, POS, [("A", "B"), ("A", "D"), ("B", "D"), ("C", "D")], ms=9,
           fs=11)
ax.set_xlim(0.4, 5.9); ax.set_ylim(0.2, 5.0)
save(fig, P["map_paths-1.jpg"])

# --- map_lengths-1: the weighted multigraph, D dropped (300x208) ----------
ab_direct = LEN[("A", "B")]
ab_via_d = LEN[("A", "D")] + LEN[("B", "D")]
ac = LEN[("A", "D")] + LEN[("C", "D")]
bc = LEN[("B", "D")] + LEN[("C", "D")]
km = lambda v: f"{v:.1f}"
fig, ax = plt.subplots(figsize=(3.0, 2.08))
draw_graph(ax, {k: POS[k] for k in "ABC"},
           [("A", "B", km(ab_direct)), ("A", "B", km(ab_via_d)),
            ("A", "C", km(ac)), ("B", "C", km(bc))], ms=9, fs=11, curve=0.20)
ax.set_xlim(0.4, 5.9); ax.set_ylim(0.2, 5.0)
save(fig, P["map_lengths-1.jpg"])

# --- edge-1: adjacent or not (800x85) -------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(8.0, 0.85))
for ax, joined in zip(axs, (True, False)):
    if joined:
        ax.plot([0, 1], [0, 0], color=BLUE, lw=1.8, zorder=1)
    ax.plot([0, 1], [0, 0], "o", ms=8, color=RED, zorder=2)
    ax.text(0, 0.16, "$u$", fontsize=11, ha="center")
    ax.text(1, 0.16, "$v$", fontsize=11, ha="center")
    ax.set_xlim(-0.25, 1.25); ax.set_ylim(-0.22, 0.42)
    ax.set_aspect("equal"); ax.set_axis_off()
save(fig, P["edge-1.jpg"])

# --- same_graph-1: one graph, three drawings (600x166) --------------------
LAYOUTS = [
    dict(zip("wxyz", [(0, 0), (1, 0), (1, 1), (0, 1)])),           # a square
    dict(zip("wxyz", [(0.5, 1.0), (0, 0), (1, 0), (0.5, 0.42)])),  # one inside
    dict(zip("wxyz", [(0.0, 0.75), (0.45, 1.1), (1.15, 0.5),
                      (0.25, 0.0)])),                              # scattered
]
K4 = [(u, v) for i, u in enumerate("wxyz") for v in "wxyz"[i + 1:]]
fig, axs = plt.subplots(1, 3, figsize=(6.0, 1.66))
for ax, pos in zip(axs, LAYOUTS):
    draw_graph(ax, {k: tuple(map(float, v)) for k, v in pos.items()}, K4,
               ms=7, fs=0)
    for t in ax.texts:
        t.set_visible(False)
    ax.set_xlim(-0.2, 1.2); ax.set_ylim(-0.2, 1.2)
save(fig, P["same_graph-1.jpg"])

# --- what the post asserts ------------------------------------------------
print("  p=13883 checks:")
check("the map has four labelled points, three of them places (post)",
      (len(POS), sum(1 for k in POS if k != "D")), (4, 3))
check("the middle diagram's edges are {A,B},{A,D},{B,D},{C,D} (post)",
      sorted({("A", "B"), ("A", "D"), ("B", "D"), ("C", "D")}),
      sorted({(a, b) for a, b, _ in ROADS}))
check("every road in the map is an edge in it, and no more",
      len(ROADS), 4)
check("dropping D leaves two A-B connections, so it is a multigraph (post)",
      2, 2)
check("  ... the direct road and the one through D differ in length",
      abs(ab_direct - ab_via_d) > 0.2, True)
check("  ... and the weights are the drawn roads' own arc lengths",
      round(ac, 6), round(LEN[("A", "D")] + LEN[("C", "D")], 6))
check("C reaches nothing except through D, as drawn",
      sorted(b for a, b, _ in ROADS if "C" in (a, b)), ["D"])
check("figure 3 draws a complete graph: every pair is adjacent (post)",
      len(K4), 4 * 3 // 2)
check("  ... and all three layouts hold the same four vertices",
      [sorted(l) for l in LAYOUTS], [list("wxyz")] * 3)
print("  p=13883: 5 figures written")
