#!/usr/bin/env python3
"""p=11261, Tapiwa Chadenga's "Could these have been the first computer games?"

Ten images are lost. Five are reconstructed here; the other five are credited
in the post to outside sources and are recorded in not-reconstructed.md.

  mboard   "Fig.1. Typical Mancala board configuration: Player A has played pit
           A3." The post gives the rules that fix the position exactly: six
           field pits a side, "field pits begin with the same number of
           pebbles, typically 4, and home pits start off empty", sowing
           counter-clockwise one pebble at a time, dropping one in your own
           home pit and skipping the opponent's. Playing A3 therefore leaves
           A with 4,4,0,5,5,5 and one pebble home, and B untouched.
  fig3-    "Fig. 3. Marching Group 2 1": Bennett's group of "2 neighbouring
           pits with 2 and 1 pebbles respectively ... The player can move the
           group to the right preserving the 2 - 1 arrangement, to finally
           capture two pebbles in pit b."
  fig5     "Fig. 5. Owari board as an automaton", where "a marching group is
           replicated with a right-shift, thus a pattern with a period of 1"
  fig6     "Fig. 6. Two state board configuration", "a pattern with period 2
           which flips between two states, 2 pebbles in one pit, or one pebble
           in two neighbouring pits"
  fig7     "Fig. 7. Shows 4 pebbles with period of 3"

The post prints Bouchet's table of periods against pebbles:

    Pebbles  1  2  3  4  5  6  7  8
    Periods  1  2  1  3  3  1  4  4, 2

That table is what fixes which arrangement each figure holds. Sowing from the
rearmost occupied pit is simulated below and every entry in the table is
reproduced from it, so the patterns drawn are found rather than assumed: three
pebbles as 2-1 with period 1, two pebbles with period 2, four pebbles as 2-2
with period 3. The kalah sequence the post works through by hand, from
0,0,4,2,2,0 down to an empty side, is replayed against the same rules too.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from figstyle import BLUE, RED, GREY, MMA, save, animate, check, paths_in

P = paths_in("p=11261.html")
WOOD, PIT, SEED = "#c8a165", "#f2e3c8", "#5a3b1e"


def pebbles_in(ax, cx, cy, n, r=0.30, rad=0.058):
    """n pebbles scattered inside a pit, deterministically."""
    if n <= 0:
        return
    rng = np.random.default_rng(1000 + n)
    for k in range(n):
        a = 2 * np.pi * k / n + 0.4 * rng.random()
        d = 0.0 if n == 1 else r * (0.45 + 0.35 * rng.random())
        ax.add_patch(Circle((cx + d * np.cos(a), cy + d * np.sin(a)), rad,
                            facecolor=SEED, edgecolor="#2e1d0d", lw=0.4,
                            zorder=4))


def board(ax, top, bottom, home_l=0, home_r=0, labels=True, title=None,
          mark=None):
    """A kalah board: `bottom` is the near player's row, left to right."""
    n = len(bottom)
    ax.add_patch(FancyBboxPatch((-0.7, -0.85), n + 2.1, 2.5,
                                boxstyle="round,pad=0.12", facecolor=WOOD,
                                edgecolor="#8a6c3f", lw=1.2, zorder=0))
    for i in range(n):
        for row, y in ((top, 0.95), (bottom, -0.15)):
            ax.add_patch(Circle((i + 0.35, y), 0.36, facecolor=PIT,
                                edgecolor="#8a6c3f", lw=0.8, zorder=1))
            pebbles_in(ax, i + 0.35, y, row[i])
    for x, v, lab in ((-0.35, home_l, "B"), (n + 0.75, home_r, "A")):
        ax.add_patch(FancyBboxPatch((x - 0.3, -0.42), 0.6, 1.65,
                                    boxstyle="round,pad=0.06", facecolor=PIT,
                                    edgecolor="#8a6c3f", lw=0.8, zorder=1))
        pebbles_in(ax, x, 0.4, v, r=0.34)
        if labels:
            ax.text(x, -0.72, f"{lab} home", fontsize=6.5, ha="center")
    if labels:
        for i in range(n):
            ax.text(i + 0.35, -0.72, f"A{i + 1}", fontsize=6.5, ha="center")
            ax.text(i + 0.35, 1.44, f"B{n - i}", fontsize=6.5, ha="center")
    if mark is not None:
        ax.add_patch(Circle((mark + 0.35, -0.15), 0.44, facecolor="none",
                            edgecolor=RED, lw=1.6, zorder=5))
    ax.set_xlim(-0.85, n + 1.3); ax.set_ylim(-1.05, 1.8)
    ax.set_aspect("equal"); ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=8)


# --- mboard: the position after A plays A3 --------------------------------
def sow_kalah(row, home, other, i, pits=6):
    """Sow from pit i of `row`, counter-clockwise, into the player's home."""
    row, other = list(row), list(other)
    hand, pos = row[i], i
    row[i] = 0
    while hand:
        pos += 1
        if pos < pits:
            row[pos] += 1
        elif pos == pits:
            home += 1
        else:
            other[(pos - pits - 1) % pits] += 1
            if pos - pits - 1 >= pits - 1:
                pos = -1
        hand -= 1
    return row, home, other


START = [4] * 6
A_row, A_home, B_row = sow_kalah(START, 0, START, 2)

fig, ax = plt.subplots(figsize=(3.0, 1.31))
board(ax, B_row[::-1], A_row, home_l=0, home_r=A_home, mark=2,
      title="Fig. 1: player A has played pit A3")
save(fig, P["mboard.jpg"])


# --- the owari automaton --------------------------------------------------
def step(state):
    """Empty the rearmost occupied pit into the pits ahead of it."""
    s = list(state) + [0] * (max(state) + 2)
    i = next(k for k, v in enumerate(s) if v)
    hand, s[i] = s[i], 0
    for k in range(1, hand + 1):
        s[i + k] += 1
    while s and s[-1] == 0:
        s.pop()
    return s


def trimmed(state):
    """The pattern with leading and trailing empty pits removed."""
    s = list(state)
    while s and s[0] == 0:
        s.pop(0)
    while s and s[-1] == 0:
        s.pop()
    return tuple(s)


def period(state, limit=60):
    """Steps until the pattern repeats itself, shifted."""
    seen, s = trimmed(state), list(state)
    for k in range(1, limit + 1):
        s = step(s)
        if trimmed(s) == seen:
            return k
    return None


def strip_gif(dest, start, frames, note, width=9):
    states = [list(start)]
    for _ in range(frames - 1):
        states.append(step(states[-1]))

    def draw(ax, i):
        s = states[i] + [0] * width
        for k in range(width):
            ax.add_patch(Circle((k, 0), 0.40, facecolor=PIT,
                                edgecolor="#8a6c3f", lw=0.9, zorder=1))
            pebbles_in(ax, k, 0, s[k], r=0.30, rad=0.075)
        ax.add_patch(FancyBboxPatch((-0.75, -0.72), width - 0.5, 1.44,
                                    boxstyle="round,pad=0.1", facecolor=WOOD,
                                    edgecolor="#8a6c3f", lw=1.2, zorder=0))
        ax.set_xlim(-0.95, width - 0.4); ax.set_ylim(-1.0, 1.0)
        ax.set_aspect("equal"); ax.set_axis_off()
        ax.set_title(f"{note}, move {i}", fontsize=8)

    animate(draw, frames, dest, figsize=(3.0, 1.5), ms=650)


def spacetime(dest, start, rows, note, width=9):
    """Successive states stacked downwards, the way an automaton is drawn."""
    states = [list(start)]
    for _ in range(rows - 1):
        states.append(step(states[-1]))
    fig, ax = plt.subplots(figsize=(3.0, 2.01))
    for r, st in enumerate(states):
        y = -1.15 * r
        s_ = st + [0] * width
        ax.add_patch(FancyBboxPatch((-0.72, y - 0.5), width - 0.55, 1.0,
                                    boxstyle="round,pad=0.06", facecolor=WOOD,
                                    edgecolor="#8a6c3f", lw=0.8, zorder=0))
        for k in range(width):
            ax.add_patch(Circle((k, y), 0.33, facecolor=PIT,
                                edgecolor="#8a6c3f", lw=0.6, zorder=1))
            pebbles_in(ax, k, y, s_[k], r=0.24, rad=0.062)
    ax.set_xlim(-0.95, width - 0.4)
    ax.set_ylim(-1.15 * (rows - 1) - 0.75, 0.75)
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_title(note, fontsize=8)
    save(fig, dest)


strip_gif(P["fig3-.gif"], [2, 1], 5, "the 2-1 marching group")
spacetime(P["fig5.gif"], [2, 1], 5,
          "the board as an automaton: one move per row,\nthe group shifting "
          "right unchanged")
strip_gif(P["fig6.gif"], [2], 5, "period 2: one pit of 2, then two pits of 1")
strip_gif(P["fig7.gif"], [2, 2], 7, "period 3, on four pebbles")

# --- what the post asserts ------------------------------------------------
print("  p=11261 checks:")
check("the board starts with 4 pebbles in each of 12 field pits (post)",
      sum(START) * 2, 48)
check("playing A3 leaves A with 4,4,0,5,5,5 (post's counter-clockwise sowing)",
      A_row, [4, 4, 0, 5, 5, 5])
check("  ... one pebble in A's home, since the fourth lands there (post)",
      A_home, 1)
check("  ... and B untouched, the pebbles having run out first",
      B_row, [4] * 6)
check("  ... with no pebble lost", sum(A_row) + A_home + sum(B_row), 48)
# Bouchet's table, printed in the post
TABLE = {1: [1], 2: [2], 3: [1], 4: [3], 5: [3], 6: [1], 7: [4], 8: [4, 2]}
# every arrangement of m pebbles over up to m pits, with no leading or
# trailing gap, run until it repeats itself shifted
def arrangements(m):
    for length in range(1, m + 1):
        def walk(rest, acc):
            if len(acc) == length:
                if rest == 0 and acc[0] and acc[-1]:
                    yield tuple(acc)
                return
            for v in range(rest + 1):
                yield from walk(rest - v, acc + [v])
        yield from walk(m, [])


found = {}
for m in range(1, 9):
    seen = set()
    for pat in arrangements(m):
        p = period(list(pat))
        if p:
            seen.add(p)
    found[m] = sorted(seen)
check("Bouchet's table of periods is reproduced by sowing from the rearmost "
      "pit: 3 pebbles give period 1 (post)", 1 in found[3], True)
check("  ... 2 pebbles give period 2 (post)", found[2], [2])
check("  ... 4 pebbles give period 3 (post)", 3 in found[4], True)
check("  ... 8 pebbles give both 4 and 2, as the post's table alone does",
      set(TABLE[8]).issubset(found[8]), True)
check("  ... and every period the post lists is one the simulation finds",
      all(set(TABLE[m]).issubset(found[m]) for m in TABLE), True)
check("the 2-1 group marches right unaltered (post)",
      trimmed(step([2, 1])), (2, 1))
check("  ... which is what period 1 means", period([2, 1]), 1)
check("two pebbles flip between one pit of 2 and two pits of 1 (post)",
      [trimmed(step([2])), trimmed(step(step([2])))], [(1, 1), (2,)])
check("four pebbles as 2-2 return to themselves after three moves (post)",
      period([2, 2]), 3)
# the kalah sequence the post works through by hand
seq = [[0, 0, 4, 2, 2, 0], [0, 0, 4, 2, 0, 1], [0, 0, 4, 2, 0, 0],
       [0, 0, 0, 3, 1, 1], [0, 0, 0, 3, 1, 0], [0, 0, 0, 0, 2, 1],
       [0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]
# At every step the post plays a pit whose pebbles run out exactly in the home
# pit, which is what earns the extra turn and lets the whole side be emptied in
# one go. Where two such pits exist it takes the rightmost, as it says at the
# start: "sow from the rightmost pit with 2".
home, row, ok = 0, list(seq[0]), True
for nxt in seq[1:]:
    i = max(k for k, v in enumerate(row) if v and v == 6 - k)
    row, home, _ = sow_kalah(row, home, [0] * 6, i)
    ok = ok and row == nxt
check("the post's worked kalah sequence replays under its own rules, from "
      "0,0,4,2,2,0 to an empty side", ok, True)
check("  ... capturing all eight pebbles in one turn (post)", home, 8)
print("  p=11261: 5 figures written (fig2, fig4, fig8, fig9 and fig10 are "
      "credited elsewhere or undescribed, see not-reconstructed.md)")
