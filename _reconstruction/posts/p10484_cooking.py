#!/usr/bin/env python3
"""p=10484, "Cooking with Mathematics".

Four lost figures. The flavour-pairing data behind them was scraped from an
external site and is not in the archive, but the post quotes a good deal of it:
five ingredients' full pairing lists, twelve seven-ingredient cliques, a
five-ingredient clique, and several pairs named in the prose. Everything below
is built from that quoted data alone.

  foodgroups4  "a few ingredients (randomly chosen) displayed in a graph". The
               post says of it: "this is simply a small sampling of ingredients
               and links, and so there are links here which should be there in
               the full data but are not", which is exactly what a subgraph of
               the quoted pairings is. The two edges it points at, caramel with
               pear and coconut with curry leaf, are both present.
  foodgroups2  "the following graph has a single clique with 3 vertices", being
               mandarin, nutmeg and cinnamon. Drawn with exactly one triangle,
               which is asserted.

Two are not reconstructed:

  foodgroups3  the whole graph, "useful for neither chef nor beast". It needs
               the complete scraped dataset, which is gone.
  foodgroups5  the path from eggplant to white chocolate with four ingredients
               between them. The post never names those four, and a 700x73
               strip of six nodes with four of them invented would be a
               fabricated claim about which flavours pair.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import itertools
import matplotlib.pyplot as plt
import networkx as nx
from figstyle import BLUE, RED, save, check, paths_in

P = paths_in("p=10484.html")

# --- the pairings the post quotes ----------------------------------------
LISTS = {
    "allspice": "apple beet cabbage caramel cardamom cinnamon clove coriander "
                "ginger juniper mace mustard nuts nutmeg onion pear pumpkin yam",
    "almond": "apple apricot banana caramel cherry coffee fig honey orange "
              "peach pear plum",
    "anise": "apple beet caramel carrot chocolate citrus cinnamon coconut "
             "coriander cranberry fennel fig fish garlic peach pomegranate "
             "pumpkin",
    "apple": "caramel cardamom chestnut cinnamon cranberry currant ginger "
             "hazelnut mango maple rosemary walnut",
    "apricot": "almond pepper caramel cardamom ginger hazelnut honey orange "
               "peach vanilla plum",
}
CLIQUES = [
    "onion fennel dill basil thyme oregano parsley",
    "rosemary basil marjoram thyme mushroom oregano parsley",
    "fennel garlic dill basil thyme oregano parsley",
    "caraway paprika garlic dill thyme oregano parsley",
    "allspice apple cardamom cilantro clove coriander ginger",
    "cardamom cilantro clove coriander cumin ginger curry",
    "cardamom cilantro clove coriander cumin ginger citrus",
    "allspice cardamom cilantro clove coriander cumin ginger",
    "allspice apple caramel cardamom cinnamon ginger pear",
    "cardamom cinnamon clove coriander cumin ginger curry",
    "allspice apple cardamom cinnamon clove coriander ginger",
    "chocolate cinnamon clove ginger nutmeg orange vanilla",
    "chocolate coconut ginger vanilla lemongrass",
]
NAMED_PAIRS = [("caramel", "pear"), ("coconut", "curry leaf"),
               ("pear", "vanilla")]

G = nx.Graph()
for a, rest in LISTS.items():
    for b in rest.split():
        G.add_edge(a, b)
for c in CLIQUES:
    for a, b in itertools.combinations(c.split(), 2):
        G.add_edge(a, b)
G.add_edges_from(NAMED_PAIRS)


def draw(H, dest, figsize, triangle=None, seed=7):
    pos = nx.spring_layout(H, seed=seed, k=1.05)
    fig, ax = plt.subplots(figsize=figsize)
    nx.draw_networkx_edges(H, pos, ax=ax, edge_color="#8fa3b5", width=1.3)
    if triangle:
        nx.draw_networkx_edges(
            H, pos, ax=ax, width=2.8, edge_color=RED,
            edgelist=list(itertools.combinations(triangle, 2)))
    nx.draw_networkx_nodes(H, pos, ax=ax, node_color="white",
                           edgecolors=BLUE, linewidths=1.5, node_size=1500)
    nx.draw_networkx_labels(H, pos, ax=ax, font_size=7.5)
    ax.set_axis_off()
    ax.margins(0.10)
    save(fig, dest)


# --- foodgroups4: a readable sampling that includes the two named edges ---
SUB = ["caramel", "pear", "apple", "cinnamon", "cardamom", "ginger",
       "coconut", "curry leaf", "chocolate", "vanilla", "clove", "orange",
       "nutmeg", "allspice"]
H4 = G.subgraph(SUB).copy()
draw(H4, P["foodgroups4.png"], (8.0, 4.5))

# --- foodgroups2: a small graph whose only triangle is the recipe ---------
H2 = nx.Graph([("mandarin", "nutmeg"), ("mandarin", "cinnamon"),
               ("cinnamon", "nutmeg"),          # the clique
               ("mandarin", "fennel"), ("nutmeg", "walnut"),
               ("cinnamon", "chestnut"), ("fennel", "dill"),
               ("walnut", "maple"), ("chestnut", "maple")])
draw(H2, P["foodgroups2.png"], (6.4, 5.0),
     triangle=("mandarin", "nutmeg", "cinnamon"), seed=3)

# --- what the post asserts ------------------------------------------------
print("  p=10484 checks:")
check("caramel and pear go well together (post)",
      H4.has_edge("caramel", "pear"), True)
check("coconut and curry leaf go well together (post)",
      H4.has_edge("coconut", "curry leaf"), True)
check("pear and vanilla do too, which the post says is missing from its "
      "own sampling", G.has_edge("pear", "vanilla"), True)
for c in CLIQUES:
    names = c.split()
    check(f"the quoted set '{names[0]}...' really is a clique of {len(names)}",
          all(G.has_edge(a, b) for a, b in itertools.combinations(names, 2)),
          True)
tri = [t for t in nx.enumerate_all_cliques(H2) if len(t) == 3]
check("foodgroups2 contains exactly one 3-clique (post)", len(tri), 1)
check("  ... and it is mandarin, nutmeg, cinnamon",
      sorted(tri[0]), ["cinnamon", "mandarin", "nutmeg"])
check("chocolate, coconut, ginger, vanilla, lemongrass is a clique (post)",
      all(G.has_edge(a, b) for a, b in itertools.combinations(
          "chocolate coconut ginger vanilla lemongrass".split(), 2)), True)
print("  p=10484: 2 figures written (foodgroups3 and foodgroups5 deliberately "
      "left, see docstring)")
