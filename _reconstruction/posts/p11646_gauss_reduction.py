#!/usr/bin/env python3
"""p=11646, "UCT MAM1000 lecture notes part 50, linear algebra part iii".

Five lost figures. Four of them are the three planes of Example 1 redrawn after
each stage of the Gauss reduction, and the matrices at every stage are printed
in the post, so they are fully determined:

  p111   x+3y-z=-1,  2x+y+4z=-1,  -x+y+z=5      the original system
  p112   after R2-2R1 and R3+R1
  p113   after the swap, R1-3R2 and R3+5R2
  p114   reduced row echelon form: x=-3, y=1, z=1

The fifth, p3dline, is the illustration of "three planes intersecting at a
line, even though they are not parallel planes". The post says explicitly that
it "is not from this example", so it only has to be a valid instance; the one
drawn here is x-y=0, y-z=0, x-z=0, whose normals are coplanar and which share
the line x=y=z.

Style follows p3dlineb.png, which survives on this post: it is a Mathematica
Plot3D with its default surface colours and a dark mesh, and these sit beside
it on the page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from figstyle import MMA, mma_axes, plane, save, check, paths_in

P = paths_in("p=11646.html")

SYSTEM = np.array([[1., 3., -1.], [2., 1., 4.], [-1., 1., 1.]])
RHS = np.array([-1., -1., 5.])
SOL = np.linalg.solve(SYSTEM, RHS)

# the four stages exactly as the post prints them
STAGES = {
    "p111.png": [(1, 3, -1, -1), (2, 1, 4, -1), (-1, 1, 1, 5)],
    "p112.png": [(1, 3, -1, -1), (0, -5, 6, 1), (0, 4, 0, 4)],
    "p113.png": [(1, 0, -1, -4), (0, 1, 0, 1), (0, 0, 6, 6)],
    "p114.png": [(1, 0, 0, -3), (0, 1, 0, 1), (0, 0, 1, 1)],
}

BOX = ((-5.5, -0.5), (-1.0, 3.0), (-1.5, 3.5))   # centred on the solution

for name, planes in STAGES.items():
    fig = plt.figure(figsize=(7.0, 4.4))
    ax = mma_axes(fig)
    for coeffs, col in zip(planes, MMA):
        plane(ax, coeffs, *BOX, color=col)
    ax.plot([SOL[0]], [SOL[1]], [SOL[2]], "o", color="black", ms=5, zorder=10)
    ax.set_xlim(*BOX[0]); ax.set_ylim(*BOX[1]); ax.set_zlim(*BOX[2])
    fig.subplots_adjust(left=-0.02, right=1.02, bottom=-0.06, top=1.06)
    save(fig, P[name])

# --- p3dline.png: three non-parallel planes sharing a line ---------------
fig = plt.figure(figsize=(6.6, 7.4))
ax = mma_axes(fig, elev=14, azim=-62)
B2 = ((-2.0, 2.0), (-2.0, 2.0), (-2.0, 2.0))
for coeffs, col in zip([(1, -1, 0, 0), (0, 1, -1, 0), (1, 0, -1, 0)], MMA):
    plane(ax, coeffs, *B2, color=col, alpha=0.85)
t = np.linspace(-2, 2, 2)
ax.plot(t, t, t, color="black", lw=2.4, zorder=10)
ax.set_xlim(*B2[0]); ax.set_ylim(*B2[1]); ax.set_zlim(*B2[2])
fig.subplots_adjust(left=-0.02, right=1.02, bottom=-0.04, top=1.04)
save(fig, P["p3dline.png"])

# --- the arithmetic the post prints --------------------------------------
print("  p=11646 checks:")
check("solution x (post: -3)", SOL[0], -3)
check("solution y (post: 1)", SOL[1], 1)
check("solution z (post: 1)", SOL[2], 1)
for i, (row, r) in enumerate(zip(SYSTEM, RHS), start=1):
    check(f"  original equation {i} holds at the solution", row @ SOL, r)
for name, planes in STAGES.items():
    for k, (a, b, c, d) in enumerate(planes, start=1):
        check(f"{name} plane {k} passes through the solution",
              a * SOL[0] + b * SOL[1] + c * SOL[2], d, tol=1e-9)
n1, n2, n3 = np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([1, 0, -1])
check("p3dline normals are coplanar (their triple product is 0)",
      float(np.dot(n1, np.cross(n2, n3))), 0.0)
check("  ... and no two are parallel",
      bool(np.linalg.norm(np.cross(n1, n2)) > 1e-9
           and np.linalg.norm(np.cross(n1, n3)) > 1e-9
           and np.linalg.norm(np.cross(n2, n3)) > 1e-9), True)
print("  p=11646: 5 figures written")
