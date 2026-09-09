#!/usr/bin/env python3
"""Shared styling for reconstructed Mathemafrica figures.

Every reconstruction imports from here so the whole set looks like one hand,
and so the provenance marker is defined in exactly one place. Nothing in a
figure should be invented: the post text dictates the maths, this module only
decides how it is drawn.
"""
import os
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = "/Users/jonathanshock/Cursor folders/Mathemafrica"
UPLOADS = os.path.join(REPO, "wp-content", "uploads")

NOTE = "figure reconstructed from the post text, 2026"

BLUE   = "#1f4e79"
RED    = "#d02020"
GREEN  = "#2e7d32"
ORANGE = "#e07b39"
PURPLE = "#7b4397"
GREY   = "#8a8a8a"
FILL   = "#9ecae1"
SERIES = [BLUE, RED, GREEN, ORANGE, PURPLE]

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "mathtext.fontset": "cm",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def axes(ax, xr=None, yr=None, grid=None, equal=False,
         xlabel="x", ylabel="y", spines=None):
    """Common axis furniture, in the house style of the surviving originals.

    Three figures recovered from the archive (approxfunc.png, plboth.png and
    the Plot3D in p3dlineb.png) are plainly Mathematica: axes crossing at the
    origin, no frame, no grid, tick labels sitting on the axes themselves.
    Reconstructions sit beside those on the same pages, so that is the default
    here rather than matplotlib's boxed-and-gridded look.

    Where the origin falls outside the plotted range, crossed axes would be
    off-screen, so the fall-back is a plain frame. Pass spines="box" or
    grid=True to force the older look.
    """
    if xr: ax.set_xlim(*xr)
    if yr: ax.set_ylim(*yr)
    if equal: ax.set_aspect("equal")

    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    inside = (x0 <= 0 <= x1) and (y0 <= 0 <= y1)
    if spines is None:
        spines = "cross" if inside else "box"
    if grid is None:
        grid = spines == "box"

    # matplotlib re-enables the grid if line properties arrive alongside False
    if grid:
        ax.grid(True, color="#dddddd", lw=0.6)
    else:
        ax.grid(False)
    if spines == "cross":
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_position("zero")
            ax.spines[s].set_color("#555555")
            ax.spines[s].set_linewidth(0.9)
        ax.tick_params(direction="out", length=3, width=0.8,
                       colors="#333333", labelsize=8)
        # Mathematica omits the tick at the origin, where the labels collide
        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _: "" if abs(v) < 1e-12 else f"{v:g}"))
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda v, _: "" if abs(v) < 1e-12 else f"{v:g}"))
        # Mathematica's Plot carries no axis labels by default and neither do
        # the surviving originals, and placed at the axis ends they collide
        # with the title, so crossed axes go unlabelled.
    else:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=8)
        if xlabel: ax.set_xlabel(xlabel, fontsize=10)
        if ylabel: ax.set_ylabel(ylabel, fontsize=10)
    return ax


def direction_field(ax, f, xr, yr, step, seg=0.38, color=BLUE, lw=1.1):
    """Short constant-length segments of slope f(x, y) on a lattice through 0.

    The lattice is snapped to multiples of `step` so that x=0 and y=0 are
    always sampled; posts routinely make claims about the behaviour there.
    Axis limits are padded so edge segments are not sliced in half.
    """
    def lattice(lo, hi):
        k0 = int(np.ceil(lo / step - 1e-9))
        k1 = int(np.floor(hi / step + 1e-9))
        return np.arange(k0, k1 + 1) * step

    L = seg * step * 2
    for x in lattice(*xr):
        for y in lattice(*yr):
            with np.errstate(divide="ignore", invalid="ignore"):
                m = f(x, y)
            if m is None or not np.isfinite(m):
                dx, dy = 0.0, L / 2
            else:
                th = np.arctan(m)
                dx, dy = (L / 2) * np.cos(th), (L / 2) * np.sin(th)
            ax.plot([x - dx, x + dx], [y - dy, y + dy],
                    color=color, lw=lw, solid_capstyle="round")
    pad = 0.7 * step
    ax.set_xlim(xr[0] - pad, xr[1] + pad)
    ax.set_ylim(yr[0] - pad, yr[1] + pad)
    ax.set_aspect("equal")


def save(fig, dest, dpi=110, mark=True):
    """Write a figure to its path under wp-content/uploads, with the marker.

    `dest` is the uploads-relative path the archived HTML asks for, e.g.
    '2015/09/pl1.png'.
    """
    if mark:
        # below the axes rather than inside them: with bbox_inches="tight" the
        # crop grows to include it, so it never lands on an axis label
        fig.text(1.0, -0.11, NOTE, ha="right", va="top",
                 fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if out.lower().endswith(".gif"):
        # matplotlib has no GIF writer; a few archived stills are named .gif
        import io
        from PIL import Image
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, facecolor="white",
                    bbox_inches="tight", pad_inches=0.18)
        buf.seek(0)
        Image.open(buf).convert("RGB").convert(
            "P", palette=Image.ADAPTIVE).save(out)
    else:
        fig.savefig(out, dpi=dpi, facecolor="white",
                    bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return out


def animate(draw, frames, dest, dpi=90, mark=True, ms=90, figsize=(5.0, 4.0),
            three_d=False, **axkw):
    """Write an animated GIF, one frame per call to `draw(ax, i)`.

    Several archived figures are animations, and a still cannot stand in for
    them: the post says "watch what happens as ...". Each frame is rendered
    through the same `save` styling so an animation matches the static figures
    beside it, then Pillow writes the loop.
    """
    import io
    from PIL import Image
    ims = []
    for i in range(frames):
        fig = plt.figure(figsize=figsize)
        if three_d:
            ax = mma_axes(fig, **axkw)
        else:
            ax = fig.add_subplot(111)
        draw(ax, i)
        if mark:
            # the frame is written without a tight bbox, so the marker has to
            # sit inside the canvas or it is simply cropped away
            fig.text(0.99, 0.015, NOTE, ha="right", va="bottom", fontsize=6.0,
                     color="#9a9a9a", transform=fig.transFigure)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, facecolor="white",
                    bbox_inches=None, pad_inches=0.18)
        plt.close(fig)
        buf.seek(0)
        ims.append(Image.open(buf).convert("RGB"))
    size = ims[0].size
    ims = [im if im.size == size else im.resize(size) for im in ims]
    pal = [im.convert("P", palette=Image.ADAPTIVE, colors=128) for im in ims]
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pal[0].save(out, save_all=True, append_images=pal[1:], duration=ms, loop=0,
                optimize=True)
    return out


def check(label, got, want, tol=1e-9):
    """Assert a claim the post itself makes. Prints so the run is auditable."""
    if isinstance(want, (bool, np.bool_)) or isinstance(got, (bool, np.bool_)):
        ok = bool(got) == bool(want)
    elif isinstance(want, (str, list, tuple, dict, set)):
        ok = got == want
    elif want in (np.inf, -np.inf):
        ok = got == want
    else:
        ok = abs(got - want) <= tol
    print(f"    {'ok  ' if ok else 'FAIL'} {label}: got {got}, post says {want}")
    if not ok:
        raise AssertionError(f"{label}: {got} != {want}")


# ---------------------------------------------------------------------------
# Typeset displays
#
# Several posts show a piecewise definition as a screenshot of typeset maths.
# There is no LaTeX on this machine and matplotlib's mathtext has no `cases`
# environment, so the brace and the two columns are laid out by hand, with the
# column positions measured from the rendered text rather than guessed.
# ---------------------------------------------------------------------------

# The archive's LaTeX (recovered from the latex.php URLs) uses short forms that
# mathtext does not know. Normalise rather than editing every call site. The
# match is on a whole control word, so \left and \leq survive untouched.
_ALIASES = {
    "ge": "geq", "le": "leq", "ne": "neq",
    "implies": "Rightarrow", "text": "mathrm", "to": "rightarrow",
    "textrm": "mathrm", "rm": "mathrm",
    # mathtext has no \bmod or \pmod; \mathrm{mod} renders the same
    "bmod": "mathrm{mod}", "dfrac": "frac", "tfrac": "frac",
}
_CTRL = re.compile(r"\\([A-Za-z]+)")


def mt(s):
    """Make a fragment of archive LaTeX safe for matplotlib's mathtext."""
    if s is None:
        return None
    return _CTRL.sub(lambda m: "\\" + _ALIASES.get(m.group(1), m.group(1)), s)


def _measure_wh(strings, fontsize, dpi):
    """Rendered pixel (width, height) of each mathtext fragment."""
    scratch = plt.figure(figsize=(24, 8), dpi=dpi)
    r = scratch.canvas.get_renderer()
    out = []
    for s in strings:
        t = scratch.text(0.01, 0.5, f"${s}$", fontsize=fontsize)
        bb = t.get_window_extent(r)
        out.append((bb.width, bb.height))
        t.remove()
    plt.close(scratch)
    return out


def _measure(strings, fontsize, dpi):
    """Rendered pixel widths of a list of mathtext fragments."""
    return [w for w, _ in _measure_wh(strings, fontsize, dpi)]


def cases(lhs, rows, dest, fontsize=17, dpi=130, gap=18, row_pt=40,
          mark=True, cond_word="if", pad=16):
    """Render  lhs = { expr   if cond ; ... }  as a display.

    rows is a list of (expr, cond) mathtext strings, without dollar signs; a
    cond of None omits the condition for that row. The canvas is sized to the
    measured content, so the marker sits against the display rather than
    stretching the image to a fixed width.
    """
    lhs = mt(lhs) + r"\,="
    rows = [(mt(e), mt(c)) for e, c in rows]
    n = len(rows)
    word = r"\mathrm{" + cond_word + "}" if cond_word else None

    widths = _measure([lhs] + [e for e, _ in rows]
                      + [c for _, c in rows if c]
                      + ([word] if word else []), fontsize, dpi)
    lhs_w = widths[0]
    expr_w = widths[1:1 + n]
    rest = widths[1 + n:]
    cond_w = rest[:sum(1 for _, c in rows if c)]
    word_w = rest[-1] if word else 0

    block_h = row_pt * n
    brace_w = 0.36 * block_h          # the glyph is far narrower than it is tall

    x_lhs = pad
    x_brace = x_lhs + lhs_w + gap
    x_expr = x_brace + brace_w + gap
    x_word = x_expr + (max(expr_w) if expr_w else 0) + gap
    x_cond = x_word + word_w + (gap if word else 0)
    total_w = x_cond + (max(cond_w) if cond_w else 0) + pad
    total_h = block_h + 2 * pad + (14 if mark else 0)

    fig = plt.figure(figsize=(total_w / dpi, total_h / dpi), dpi=dpi)
    r = fig.canvas.get_renderer()
    y_top = total_h - pad
    ys = [y_top - row_pt * (i + 0.5) for i in range(n)]
    y_mid = (ys[0] + ys[-1]) / 2

    def put(xpx, ypx, s, size=fontsize):
        return fig.text(xpx / total_w, ypx / total_h, f"${s}$",
                        fontsize=size, ha="left", va="center")

    put(x_lhs, y_mid, lhs)
    br = fig.text(x_brace / total_w, y_mid / total_h, "{", fontsize=fontsize,
                  ha="left", va="center")
    bh = br.get_window_extent(r).height
    br.set_fontsize(fontsize * block_h / max(bh, 1))

    for y, (e, c) in zip(ys, rows):
        put(x_expr, y, e)
        if c:
            if word:
                put(x_word, y, word)
            put(x_cond, y, c)

    if mark:
        fig.text(1 - pad / total_w / 2, 3 / total_h, NOTE, ha="right",
                 va="bottom", fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)
    return out


def paths_in(post):
    """Map each image basename in an archived post to its uploads-relative path.

    Guessing the YYYY/MM directory from a filename is a good way to write a
    figure nobody will ever see; read it out of the HTML instead.

        P = paths_in("p=12378.html");  save(fig, P["step0.png"])
    """
    h = open(os.path.join(REPO, post), encoding="utf-8", errors="replace").read()
    out = {}
    for m in re.finditer(r'wp-content/uploads/([^"?\s]+)', h):
        rel = m.group(1)
        out[os.path.basename(rel)] = rel
    return out


# ---------------------------------------------------------------------------
# Solids
#
# Several of the MAM1000 volume posts show solids of revolution, stacks of
# approximating disks and cylinders. These build the meshes; the calling script
# supplies the radius function the post actually names.
# ---------------------------------------------------------------------------

def solid3d(fig, pos=111, elev=18, azim=-58, box=(1, 1, 0.85)):
    args = pos if isinstance(pos, tuple) else (pos,)
    ax = fig.add_subplot(*args, projection="3d")
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect(box)
    ax.grid(False)
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.pane.set_alpha(0.0)
        pane.pane.set_edgecolor("none")
    return ax


def revolve(ax, t, radius, axis="x", n=80, color=FILL, alpha=0.55,
            edge="none", lw=0):
    """Surface swept by rotating `radius(t)` about the named axis."""
    th = np.linspace(0, 2 * np.pi, n)
    T, TH = np.meshgrid(t, th)
    Rr = radius(T)
    if axis == "x":
        X, Y, Z = T, Rr * np.cos(TH), Rr * np.sin(TH)
    else:
        X, Y, Z = Rr * np.cos(TH), Rr * np.sin(TH), T
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=lw,
                    edgecolor=edge, shade=True, antialiased=True)
    return X, Y, Z


def disk_stack(ax, edges, radius, axis="x", n=60, color=FILL, alpha=0.5,
               edgecolor="#5a9bd4"):
    """Approximate a solid by cylinders spanning consecutive `edges`.

    `radius` is evaluated at each cylinder's midpoint, which is how the posts
    describe the approximation.
    """
    th = np.linspace(0, 2 * np.pi, n)
    for lo, hi in zip(edges[:-1], edges[1:]):
        rad = radius(0.5 * (lo + hi))
        if rad <= 0:
            continue
        T, TH = np.meshgrid(np.array([lo, hi]), th)
        Rr = np.full_like(T, rad)
        if axis == "x":
            X, Y, Z = T, Rr * np.cos(TH), Rr * np.sin(TH)
        else:
            X, Y, Z = Rr * np.cos(TH), Rr * np.sin(TH), T
        ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0.3,
                        edgecolor=edgecolor, shade=True)
        for end in (lo, hi):
            rr = np.linspace(0, rad, 6)
            RR, TH2 = np.meshgrid(rr, th)
            EE = np.full_like(RR, end)
            if axis == "x":
                ax.plot_surface(EE, RR * np.cos(TH2), RR * np.sin(TH2),
                                color=color, alpha=alpha, linewidth=0, shade=True)
            else:
                ax.plot_surface(RR * np.cos(TH2), RR * np.sin(TH2), EE,
                                color=color, alpha=alpha, linewidth=0, shade=True)


def display(expr, dest, fontsize=19, dpi=130, pad=16, mark=True):
    """One centred mathtext expression on a canvas sized to fit it.

    For the posts that show a single equation as a screenshot.
    """
    expr = mt(expr)
    w = _measure([expr], fontsize, dpi)[0]
    h = _measure(["X^{2}_{2}"], fontsize, dpi)[0]  # rough line height proxy
    scratch = plt.figure(figsize=(20, 6), dpi=dpi)
    t = scratch.text(0.01, 0.5, f"${expr}$", fontsize=fontsize)
    bb = t.get_window_extent(scratch.canvas.get_renderer())
    w, h = bb.width, bb.height
    plt.close(scratch)

    W, H = w + 2 * pad, h + 2 * pad + (14 if mark else 0)
    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    fig.text(0.5, (h / 2 + pad + (14 if mark else 0)) / H, f"${expr}$",
             fontsize=fontsize, ha="center", va="center")
    if mark:
        fig.text(1 - pad / W / 2, 3 / H, NOTE, ha="right", va="bottom",
                 fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)
    return out


def table(headers, rows, dest, fontsize=15, dpi=130, pad=16, col_gap=26,
          row_gap=14, mark=True, rule=True):
    """A small mathtext table, for the posts that show one as a screenshot.

    Row heights are measured, not assumed: a cell holding a fraction is much
    taller than one holding an integer, and a fixed row pitch overlaps them.
    """
    headers = [mt(c) for c in headers]
    rows = [[mt(c) for c in r] for r in rows]
    ncol = len(headers)

    dims = {}
    for j in range(ncol):
        col = [headers[j]] + [r[j] for r in rows]
        for cell, wh in zip(col, _measure_wh(col, fontsize, dpi)):
            dims[(j, cell)] = wh
    widths = [max(dims[(j, c)][0]
                  for c in [headers[j]] + [r[j] for r in rows])
              for j in range(ncol)]
    heights = [max(dims[(j, headers[j])][1] for j in range(ncol))] + \
              [max(dims[(j, r[j])][1] for j in range(ncol)) for r in rows]

    xs, x = [], pad
    for w in widths:
        xs.append(x)
        x += w + col_gap
    W = x - col_gap + 2 * pad
    H = sum(heights) + row_gap * len(heights) + 2 * pad + (14 if mark else 0)

    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)

    def put(xpx, ypx, s):
        fig.text(xpx / W, ypx / H, f"${s}$", fontsize=fontsize,
                 ha="left", va="center")

    y = H - pad
    for i, line in enumerate([headers] + rows):
        y -= heights[i] / 2 + row_gap / 2
        for j, cell in enumerate(line):
            put(xs[j], y, cell)
        y -= heights[i] / 2 + row_gap / 2
        if i == 0 and rule:
            fig.add_artist(plt.Line2D([pad / W, (W - pad) / W],
                                      [y / H, y / H], color="black", lw=1.0))

    if mark:
        fig.text(1 - pad / W / 2, 3 / H, NOTE, ha="right", va="bottom",
                 fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Mathematica-style plane plots
#
# p3dlineb.png survives on p=11646 and is plainly a Mathematica Plot3D: default
# surface colours, a dark mesh over each surface, a thin bounding box with
# ticks. Its lost siblings are drawn to match it rather than to this project's
# usual matplotlib look, since a reader sees them side by side.
# ---------------------------------------------------------------------------

MMA = ["#5E81B5", "#E19C24", "#8FB031", "#EB6235", "#8778B3"]


def mma_axes(fig, pos=111, elev=16, azim=-64):
    ax = fig.add_subplot(*(pos if isinstance(pos, tuple) else (pos,)),
                         projection="3d")
    ax.view_init(elev=elev, azim=azim)
    ax.grid(False)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor("white")
        a.pane.set_alpha(1.0)
        a.pane.set_edgecolor("#b0b0b0")
        a.line.set_color("#909090")
    ax.tick_params(labelsize=8, colors="#333333")
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("y", fontsize=11)
    ax.set_zlabel("z", fontsize=11)
    return ax


def plane(ax, coeffs, xr, yr, zr, color, n=14, alpha=0.92, mesh="#3a3a3a"):
    """Draw the plane a*x + b*y + c*z = d inside the given box.

    Solves for whichever variable has the largest coefficient, so vertical
    planes such as y = 1 come out as well as graphs of z.
    """
    a, b, c, d = coeffs
    j = int(np.argmax(np.abs([a, b, c])))
    if j == 2:
        U, V = np.meshgrid(np.linspace(*xr, n), np.linspace(*yr, n))
        X, Y, Z = U, V, (d - a * U - b * V) / c
    elif j == 1:
        U, V = np.meshgrid(np.linspace(*xr, n), np.linspace(*zr, n))
        X, Y, Z = U, (d - a * U - c * V) / b, V
    else:
        U, V = np.meshgrid(np.linspace(*yr, n), np.linspace(*zr, n))
        X, Y, Z = (d - b * U - c * V) / a, U, V
    Z = np.where((Z >= zr[0]) & (Z <= zr[1]), Z, np.nan)
    X = np.where((X >= xr[0]) & (X <= xr[1]), X, np.nan)
    Y = np.where((Y >= yr[0]) & (Y <= yr[1]), Y, np.nan)
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0.4,
                    edgecolor=mesh, shade=False, antialiased=True)


def stack(lines, dest, fontsize=17, dpi=130, pad=16, gap=14, mark=True,
          align="center", note=None):
    """Several mathtext lines stacked, for multi-step displays.

    `note` adds a small grey line underneath, for the rare figure that needs to
    say something about itself.
    """
    lines = [mt(s) for s in lines]
    wh = _measure_wh(lines, fontsize, dpi)
    widths = [w for w, _ in wh]
    heights = [h for _, h in wh]
    note_h = 0
    if note:
        note_h = _measure_wh([note], 9, dpi)[0][1] + gap
    W = max(widths) + 2 * pad
    H = sum(heights) + gap * (len(lines) - 1) + 2 * pad + note_h + \
        (14 if mark else 0)

    fig = plt.figure(figsize=(W / dpi, H / dpi), dpi=dpi)
    y = H - pad
    for s, h in zip(lines, heights):
        y -= h / 2
        x = 0.5 if align == "center" else pad / W
        fig.text(x, y / H, f"${s}$", fontsize=fontsize,
                 ha="center" if align == "center" else "left", va="center")
        y -= h / 2 + gap
    if note:
        fig.text(0.5, (y - note_h / 2 + gap) / H, note, fontsize=9,
                 ha="center", va="center", color="#777777")
    if mark:
        fig.text(1 - pad / W / 2, 3 / H, NOTE, ha="right", va="bottom",
                 fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)
    return out
