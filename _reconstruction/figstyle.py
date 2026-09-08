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


def axes(ax, xr=None, yr=None, grid=True, equal=False,
         xlabel="x", ylabel="y", spines="box"):
    """Common axis furniture. spines='cross' puts the axes through the origin."""
    if xr: ax.set_xlim(*xr)
    if yr: ax.set_ylim(*yr)
    if equal: ax.set_aspect("equal")
    if grid: ax.grid(True, color="#dddddd", lw=0.6)
    if spines == "cross":
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["left"].set_color("#666666")
        ax.spines["bottom"].set_color("#666666")
    else:
        ax.axhline(0, color="#999999", lw=0.8, zorder=1)
        ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
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
        fig.text(0.995, 0.006, NOTE, ha="right", va="bottom",
                 fontsize=6.5, color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=dpi, facecolor="white",
                bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return out


def check(label, got, want, tol=1e-9):
    """Assert a claim the post itself makes. Prints so the run is auditable."""
    ok = (got == want) if want in (np.inf, -np.inf) else abs(got - want) <= tol
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
}
_CTRL = re.compile(r"\\([A-Za-z]+)")


def mt(s):
    """Make a fragment of archive LaTeX safe for matplotlib's mathtext."""
    if s is None:
        return None
    return _CTRL.sub(lambda m: "\\" + _ALIASES.get(m.group(1), m.group(1)), s)


def _measure(strings, fontsize, dpi):
    """Rendered pixel widths of a list of mathtext fragments."""
    scratch = plt.figure(figsize=(20, 4), dpi=dpi)
    r = scratch.canvas.get_renderer()
    out = []
    for s in strings:
        t = scratch.text(0.01, 0.5, f"${s}$", fontsize=fontsize)
        out.append(t.get_window_extent(r).width)
        t.remove()
    plt.close(scratch)
    return out


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
