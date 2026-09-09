#!/usr/bin/env python3
"""p=11688, "How Pringles are made (or alternatively hyperbolic paraboloids)".

Four lost images for f(x,y) = x^2 - y^2, all specified by the text:

  p0    the z=0 slice, x^2-y^2=0, "two lines of gradient +1 and -1 which pass
        through the origin", drawn in three dimensions because the post frames
        it that way: "if we slice through our surface at z=0 we should find
        these two lines"
  p1    z=1, giving y = +-sqrt(x^2-1) on |x|>1
  p2    z=-1, giving y = +-sqrt(x^2+1)
  try.gif  the animation, which the post describes frame by frame: "the first
        line you see is that at z=-5, then z=-3 then -1, then 0 then the same
        but positive values, going up. Finally we see the shape forming, as we
        put the slices at the appropriate height, and we overlay the actual
        function on top of this"

The animation is rebuilt rather than skipped because, unlike the other lost
animations in the archive, the post says exactly what each stage shows.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from figstyle import BLUE, RED, MMA, UPLOADS, NOTE, save, check, paths_in, \
    mma_axes

P = paths_in("p=11688.html")
LIM, ZLIM = 3.0, 9.0


def surface(ax, alpha=0.28):
    g = np.linspace(-LIM, LIM, 60)
    X, Y = np.meshgrid(g, g)
    ax.plot_surface(X, Y, X ** 2 - Y ** 2, color=MMA[0], alpha=alpha,
                    linewidth=0.25, edgecolor="#5a5a5a", shade=False)


def slice_curves(z, n=400):
    """The two branches of x^2 - y^2 = z, as (x, y) arrays."""
    if abs(z) < 1e-12:
        x = np.linspace(-LIM, LIM, n)
        return [(x, x), (x, -x)]
    if z > 0:                     # y = +- sqrt(x^2 - z), needs |x| >= sqrt(z)
        out = []
        for sx in (1, -1):
            x = sx * np.linspace(np.sqrt(z), LIM, n)
            y = np.sqrt(np.maximum(x ** 2 - z, 0))
            out += [(x, y), (x, -y)]
        return out
    x = np.linspace(-LIM, LIM, n)  # y = +- sqrt(x^2 + |z|)
    y = np.sqrt(x ** 2 - z)
    return [(x, y), (x, -y)]


def frame3d(z_values, with_surface, dest=None, title=""):
    fig = plt.figure(figsize=(5.2, 3.4))
    ax = mma_axes(fig, elev=20, azim=-58)
    if with_surface:
        surface(ax)
    for z in z_values:
        for x, y in slice_curves(z):
            m = np.abs(y) <= LIM
            ax.plot(x[m], y[m], zs=z, color=RED, lw=2.0, zorder=6)
    ax.set_xlim(-LIM, LIM); ax.set_ylim(-LIM, LIM); ax.set_zlim(-ZLIM, ZLIM)
    ax.set_box_aspect((1, 1, 1.1))
    if title:
        ax.set_title(title, fontsize=10)
    if dest:
        save(fig, dest)
        return None
    return fig


frame3d([0.0], True, P["p0.png"], r"$z=0$:  $y=\pm x$")
frame3d([1.0], True, P["p1.png"], r"$z=1$:  $y=\pm\sqrt{x^2-1}$")
frame3d([-1.0], True, P["p2.png"], r"$z=-1$:  $y=\pm\sqrt{x^2+1}$")

# --- try.gif: slices accumulating, then the surface laid over them -------
ORDER = [-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0]
frames = []
tmp = "/private/tmp/claude-501/-Users-jonathanshock-Cursor-folders-Mathematica/fa8467c2-86f9-4523-91a8-5388d8cc081c/scratchpad/pringle"
os.makedirs(tmp, exist_ok=True)
for k in range(1, len(ORDER) + 1):
    fig = frame3d(ORDER[:k], False, title=f"slices up to $z={ORDER[k-1]:g}$")
    f = f"{tmp}/f{k:02d}.png"
    fig.savefig(f, dpi=90, facecolor="white")
    plt.close(fig)
    frames.append(f)
for i, a in enumerate((0.10, 0.20, 0.30, 0.40)):
    fig = frame3d(ORDER, False, title=r"$f(x,y)=x^2-y^2$")
    ax = fig.axes[0]
    surface(ax, alpha=a)
    f = f"{tmp}/g{i:02d}.png"
    fig.savefig(f, dpi=90, facecolor="white")
    plt.close(fig)
    frames.append(f)

imgs = [Image.open(f).convert("P", palette=Image.ADAPTIVE) for f in frames]
out = os.path.join(UPLOADS, P["try.gif"])
os.makedirs(os.path.dirname(out), exist_ok=True)
imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=700,
             loop=0)
print(f"  wrote animation with {len(imgs)} frames")

# --- the algebra the post does -------------------------------------------
print("  p=11688 checks:")
check("z=0 gives y=+-x (post)", 2.0 ** 2 - 2.0 ** 2, 0.0)
check("z=1 needs |x|>=1 (post: domain |x|>1)",
      bool(np.isnan(np.sqrt(0.5 ** 2 - 1))), True)
for z in (-1.0, 0.0, 1.0, 3.0):
    for x, y in slice_curves(z):
        r = x ** 2 - y ** 2
        check(f"every point of the z={z:g} slice satisfies x^2-y^2=z",
              float(np.nanmax(np.abs(r - z))), 0.0, tol=1e-9)
check("the surface is a saddle: rising along x, falling along y",
      float((2.0 ** 2 - 0.0) > 0 and (0.0 - 2.0 ** 2) < 0), 1.0)
print("  p=11688: 4 images written")
