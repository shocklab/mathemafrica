#!/usr/bin/env python3
"""p=13826, "Graph Theory, Numberphile and Mathematica".

Four lost graph figures, all of them exactly computable from the rule the post
gives: nodes are the integers 1..n, and two are joined when their sum is a
square.

  graph12  n=12, "note that there are three disconnected pieces of it"
  graph14  n=14, connected but with no Hamiltonian path
  graph15  n=15, the first n that has one, "the red line here is a Hamiltonian
           path"
  graph18  n=18, which does not

Every one of those claims is checked before drawing, along with the post's
further remarks that 16 and 17 have paths, 18 does not, then 23 does, 24 does
not and 25 does.

Self-loops appear whenever 2i is a square, and the post notes them in passing:
"the self-connected vertices are not important in any of this". They are drawn,
small, because the originals evidently showed them.

The two Mathematica screenshots on this post are not reconstructed. They show
the code, and the post then quotes every piece of that code in its prose, so a
reader loses nothing; a fabricated notebook screenshot would only assert a
formatting that cannot be known.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from figstyle import BLUE, RED, GREY, save, check, paths_in

P = paths_in("p=13826.html")


def is_square(k):
    r = math.isqrt(k)
    return r * r == k


def build(n):
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            if is_square(i + j):
                G.add_edge(i, j)
    return G


def hamiltonian_path(G):
    """A Hamiltonian path if one exists, else None. Exact, over small n."""
    nodes = list(G.nodes())
    n = len(nodes)
    idx = {v: i for i, v in enumerate(nodes)}
    adj = [0] * n
    for u, v in G.edges():
        if u != v:
            adj[idx[u]] |= 1 << idx[v]
            adj[idx[v]] |= 1 << idx[u]
    seen = set()

    def go(mask, last, path):
        if mask == (1 << n) - 1:
            return path
        if (mask, last) in seen:
            return None
        seen.add((mask, last))
        m = adj[last] & ~mask
        while m:
            b = m & -m
            j = b.bit_length() - 1
            m ^= b
            r = go(mask | b, j, path + [nodes[j]])
            if r:
                return r
        return None

    for s in range(n):
        seen.clear()
        r = go(1 << s, s, [nodes[s]])
        if r:
            return r
    return None


def draw(n, dest, figsize, highlight):
    G = build(n)
    simple = nx.Graph((u, v) for u, v in G.edges() if u != v)
    simple.add_nodes_from(G.nodes())
    pos = nx.kamada_kawai_layout(simple)
    xs = np.array([p[0] for p in pos.values()])
    ys = np.array([p[1] for p in pos.values()])
    # stretch to the frame the original used, which for the path-like graphs
    # is much wider than it is tall
    sx = figsize[0] / max(np.ptp(xs), 1e-6)
    sy = figsize[1] / max(np.ptp(ys), 1e-6)
    pos = {k: (v[0] * sx, v[1] * sy) for k, v in pos.items()}

    fig, ax = plt.subplots(figsize=figsize)
    nx.draw_networkx_edges(simple, pos, ax=ax, edge_color="#7f8c9b", width=1.4)
    if highlight:
        path = hamiltonian_path(simple)
        if path:
            nx.draw_networkx_edges(
                simple, pos, ax=ax, width=2.6, edge_color=RED,
                edgelist=list(zip(path[:-1], path[1:])))
    for v in G.nodes():
        if G.has_edge(v, v):
            x, y = pos[v]
            ax.add_patch(plt.Circle((x, y + 0.10 * figsize[1] / 4),
                                    0.09 * figsize[1] / 4, fill=False,
                                    edgecolor="#7f8c9b", lw=1.2, zorder=2))
    nx.draw_networkx_nodes(simple, pos, ax=ax, node_color="white",
                           edgecolors=BLUE, linewidths=1.6, node_size=430)
    nx.draw_networkx_labels(simple, pos, ax=ax, font_size=9)
    ax.set_axis_off()
    ax.margins(0.07)
    save(fig, dest)
    return G


G12 = draw(12, P["graph12.jpg"], (4.6, 3.8), False)
G14 = draw(14, P["graph14.jpg"], (7.4, 2.0), False)
G15 = draw(15, P["graph15.jpg"], (7.4, 1.8), True)
G18 = draw(18, P["graph18.jpg"], (7.4, 1.7), False)

# --- every claim the post makes ------------------------------------------
print("  p=13826 checks:")
check("12 joins 4 because 12+4=16 (post)", is_square(12 + 4), True)
check("4 joins 5 because 4+5=9 (post)", is_square(4 + 5), True)
check("2 joins 7 because sqrt(2+7)=3 (post's worked position)",
      is_square(2 + 7), True)
check("n=12 has three disconnected pieces (post)",
      nx.number_connected_components(nx.Graph(
          (u, v) for u, v in G12.edges() if u != v)), 3)


def simple_of(n):
    G = build(n)
    S = nx.Graph((u, v) for u, v in G.edges() if u != v)
    S.add_nodes_from(G.nodes())
    return S


check("n=14 is connected (post)",
      nx.number_connected_components(simple_of(14)), 1)
for n, want in ((12, False), (14, False), (15, True), (16, True), (17, True),
                (18, False), (23, True), (24, False), (25, True)):
    check(f"n={n} has a Hamiltonian path: post says {want}",
          hamiltonian_path(simple_of(n)) is not None, want)
path15 = hamiltonian_path(simple_of(15))
check("the n=15 path visits all 15 nodes", len(set(path15)), 15)
check("  ... and every step of it sums to a square",
      all(is_square(a + b) for a, b in zip(path15[:-1], path15[1:])), True)
print("  p=13826: 4 figures written (the two Mathematica screenshots are "
      "deliberately left, see docstring)")
