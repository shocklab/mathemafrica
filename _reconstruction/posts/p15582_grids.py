#!/usr/bin/env python3
"""p=15582, "Investigating Practical Ordering of Grids". Three of four figures.

The post specifies everything: a grid of size 10, an agent going from (0,0) to
the far corner, and variations whose obstacle is "the square-subgrid whose
diagonal elements are (1,1),(2,2)", then (1,1)..(3,3), and so on. Nine
variations, labelled (a) to (i), and the post notes that "adding a bigger block
would have disconnected (i)", which fixes (a) as the clear grid and (i) as the
outer ring, the last one still joined to the corner.

  grid_ex               the small worked example: cells, the graph the post
                        builds from effective moves, and the same with an
                        obstacle
  generatedvariation-1  the nine variations as graphs, red nodes, exactly as
                        the post describes them
  connectivityvscomp-1  the connectivity of each. This is the post's punchline:
                        it is 2 for every one of them, because "removing the
                        nodes that represent the cells (0,1),(1,0) ... is
                        sufficient to disconnect the graph structure", so
                        connectivity "is not sensitive enough to the
                        deformations we are considering".

timevscomplexity.png is deliberately not reconstructed. The post reports that
the average hitting time was under 1000 steps for (a) to (g), just over 1000
for (h) and "around 100000" for (i). Solving the hitting time exactly does not
give that: on the reduced graph it falls steadily from 542 to 324, and under a
bounce-back move model (a blocked move wastes a step) it dips and then rises,
602 to 501 to 648. The qualitative claim, that the last variation is the worst,
holds under the second model; the two orders of magnitude do not hold under
either. Drawing the figure would mean either inventing the post's numbers or
putting a plot next to text it contradicts.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from figstyle import BLUE, RED, GREY, save, axes, check, paths_in

P = paths_in("p=15582.html")
N, START, TARGET = 10, (0, 0), (9, 9)


def variation(k, n=N):
    """The grid graph with the square (1,1)..(k,k) removed."""
    G = nx.grid_2d_graph(n, n)
    if k:
        G.remove_nodes_from([(i, j) for i in range(1, k + 1)
                             for j in range(1, k + 1)])
    return G


def draw_grid_graph(ax, G, n, node_size=26, color=RED):
    pos = {v: (v[1], -v[0]) for v in G.nodes()}
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#9bb0c4", width=0.9)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=color, node_size=node_size)
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-n + 0.4, 0.6)
    ax.set_aspect("equal")
    ax.set_axis_off()


# --- grid_ex: the small worked example -----------------------------------
fig, axs = plt.subplots(1, 3, figsize=(8.8, 3.0))
small = nx.grid_2d_graph(4, 4)
for i in range(4):
    for j in range(4):
        axs[0].add_patch(plt.Rectangle((j - 0.5, -i - 0.5), 1, 1,
                                       facecolor="#eef4f9", edgecolor=GREY,
                                       lw=0.9))
        axs[0].text(j, -i, f"({i},{j})", ha="center", va="center", fontsize=6.5)
axs[0].set_xlim(-0.6, 3.6); axs[0].set_ylim(-3.6, 0.6)
axs[0].set_aspect("equal"); axs[0].set_axis_off()
axs[0].set_title("grid (1)", fontsize=10)
draw_grid_graph(axs[1], small, 4, node_size=90)
axs[1].set_title("its graph", fontsize=10)
blocked = small.copy()
blocked.remove_node((1, 1))
draw_grid_graph(axs[2], blocked, 4, node_size=90)
axs[2].set_title("grid (2): an obstacle at $(1,1)$", fontsize=10)
save(fig, P["grid_ex.png"])

# --- generatedvariation-1: the nine variations ---------------------------
fig, axs = plt.subplots(3, 3, figsize=(9.4, 4.1))
graphs = []
for ax, (lab, k) in zip(axs.ravel(), zip("abcdefghi", range(0, 9))):
    G = variation(k)
    graphs.append((lab, k, G))
    draw_grid_graph(ax, G, N)
    ax.set_title(f"({lab})", fontsize=9)
fig.subplots_adjust(wspace=0.02, hspace=0.16)
save(fig, P["generatedvariation-1.png"])

# --- connectivityvscomp-1: connectivity is flat --------------------------
kappa = [nx.node_connectivity(G) for _, _, G in graphs]
fig, ax = plt.subplots(figsize=(6.8, 4.0))
ax.plot(range(1, 10), kappa, "-o", color=BLUE, ms=8, lw=1.8)
ax.set_xticks(range(1, 10))
ax.set_xticklabels([f"({c})" for c in "abcdefghi"])
axes(ax, (0.5, 9.5), (0, 4), spines="box", xlabel="variation",
     ylabel=r"connectivity $\kappa(G)$")
ax.set_title("connectivity does not move at all across the variations",
             fontsize=10)
save(fig, P["connectivityvscomp-1.png"])

# --- what the post asserts ------------------------------------------------
print("  p=15582 checks:")
check("the clear grid has 100 cells", graphs[0][2].number_of_nodes(), 100)
check("variation (i) leaves only the outer ring",
      graphs[-1][2].number_of_nodes(), 4 * N - 4)
check("  ... and a bigger block would take the target (post)",
      TARGET in variation(9).nodes(), False)
for lab, k, G in graphs:
    check(f"  ({lab}) still joins start to target", nx.has_path(G, START,
          TARGET), True)
check("connectivity is 2 for every variation (post's punchline)",
      set(kappa), {2})
check("  ... which is what removing (0,1) and (1,0) does (post)",
      nx.node_connectivity(variation(0)), 2)
G0 = variation(0)
G0.remove_nodes_from([(0, 1), (1, 0)])
check("  ... leaving (0,0) cut off", nx.has_path(G0, START, TARGET), False)
print("  p=15582: 3 figures written (timevscomplexity.png deliberately left, "
      "see docstring)")
