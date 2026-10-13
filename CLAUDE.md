# Mathemafrica archive: working notes

Read this before touching anything here. It records where the project got to,
what is already known, and the decisions still open.

## What this is

A static reconstruction of mathemafrica.org, the maths blog Jonathan ran from
2014 to 2021, lost when its server stopped being paid for. Recovered from the
Wayback Machine by [sanxofon](https://github.com/sanxofon/mathemafrica); this
repository is that work plus the fixes below.

- Local clone: `/Users/jonathanshock/Cursor folders/Mathemafrica`
- Remote: `shocklab/mathemafrica` (public; a free org plan will not serve Pages
  from a private repo). Push with `git -C <path> push shocklab main`.
- Live: <https://shocklab.github.io/mathemafrica/>
- Jonathan wrote most of the maths posts himself and is the author of most of
  the lost figures, so he can adjudicate any reconstruction.

## State as of 2026-10-13

Done and pushed:

- All 170,689 root-absolute `/mathemafrica/...` paths made relative, so the site
  renders identically at a subpath or a domain root. Verified by serving at both.
- Feed links repointed at `_xml/`; `.nojekyll` added.
- Hidden SEO spam link removed from 793 pages (see gotchas).
- Legacy `/?p=1234` permalinks mapped onto the flattened filenames by a shim in
  `index.html`; `404.html` explains the archive is partial and falls back from
  `p=123&share=twitter.html` to `p=123.html`.
- 127 images refetched from the Wayback Machine.
- The 70 recovered camera JPEGs downscaled to a 1600 px longest side (260 MB to
  14 MB).
- Lost figures redrawn (below); the reconstruction note sits in each image's
  metadata, not on the image (Jonathan, 2026-10-13).
- Equations converted from latex.php images to MathJax 3.2.2, vendored in
  `mathjax/` (see gotchas).
- `og:url`, `og:image` and canonical made absolute under the github.io address
  by `_reconstruction/absolute_urls.py`.
- Seven slips in Jonathan's own posts corrected at his request (see below).

Not done: the domain (below).

## Gotchas, so you don't rediscover them

**The images are archived under the CDN, not the site.** The Wayback Machine
holds only 17 files under `mathemafrica.org/wp-content/uploads/`. The blog served
images through Jetpack's Photon CDN, so the crawler stored them under
`i0/i1/i2.wp.com/www.mathemafrica.org/...`. Searching those hosts is what found
the 127. A domain-wide image sweep adds nothing beyond theme assets. 431 images
have no capture under any host; individual CDX queries confirm it, so treat that
number as final rather than re-running the search.

**`.nojekyll` is load-bearing.** Without it Pages runs Jekyll, which hides any
directory whose name begins with `_`, and all 147 feeds under `_xml/` 404. They
still 404 on sanxofon's copy for exactly this reason.

**Paths must stay relative.** Every HTML file sits in the repository root, which
is the only reason plain relative links work from any mount point. Do not
reintroduce a root-absolute prefix; it would pin the site to one URL again.

**The equations are MathJax now.** WordPress served every equation as an image
from `s0.wp.com/latex.php?latex=...`, the LaTeX in the query string.
`_reconstruction/latex_to_mathjax.py` put that LaTeX back into the pages
(14,532 equations in 400 pages; a paragraph holding only an equation becomes
display maths) and the pages load `mathjax/tex-chtml-full.js`. MathJax rejects
three things WordPress's real LaTeX accepted (`minipage`, `\hfill`,
`\Big\slash`); the converter rewrites them. Mathematica's `\[Pi]` in quoted code
reads as a display delimiter, so those paragraphs carry `tex2jax_ignore`. The
earlier figure inventory was built from the latex.php URLs; the git history
before commit eda440e still has them.

**A hidden spam link was injected into the archive.** A backdoored
`traffic-stats-widget` plugin put a `display:none` link to garcinia-cambogia.fr
into 793 pages. Removed. Check for its like before republishing anything else.

**Do not trust the test browser on image failures.** It caches 404s from earlier
in a session and will report images broken long after they are being served.
Verify with `curl` against the live URL, checking status, content-type and
length, before concluding anything is wrong.

## The domain

Held by IMAGINARY gGmbH (Andreas Matt) at GoDaddy, on auto-renewal, which
IMAGINARY pays for; Jonathan is happy for it to stay in their name (thread
"Good news: Mathematica resurrected!", 8 September 2026). Still delegated to
`ns5/ns6.kasserver.com` (All-Inkl) with an empty zone, so nothing resolves.
Andreas has to make the DNS change; the records are in `README.md`. Once the
domain resolves here: add the `CNAME` file, enable HTTPS in the Pages settings,
and run `_reconstruction/absolute_urls.py https://mathemafrica.org/`.

## Figure reconstruction (in progress)

431 images are gone for good. They are disproportionately the mathematical
figures rather than the photographs: 67% of the lost are PNG against 27% of the
survivors, and 35% sit in teaching posts against 19%. The heaviest losses are in
the MAM1000 lecture notes and the calculus explainers, where the figure carries
the argument.

`_reconstruction/lost-figures-inventory.json` holds, for every lost image, its
host post, alt text, caption, display width, and the surrounding prose with the
equations decoded back into LaTeX. Buckets:

| bucket | n |
|---|---|
| figure, maths context and plot language | 110 |
| figure, maths context only | 62 |
| figure, plot language only | 29 |
| screenshot of typeset maths (regenerable as LaTeX) | 21 |
| photo / animation / external source | 138 |
| unclear | 53 |

222 are plausible candidates. Concentration by post: absolute values 11,
polynomial division 10, MAM1000 parts 9 and 10 seventeen between them, Pascal's
triangle 6, Mandelbrot 6.

### Method that worked

Work a whole post at a time, not a figure at a time; figures in a series share
their setup and the later text often constrains the earlier figure. Dump the post
with `[[[FIGURE: name.png]]]` markers in place of the images and the LaTeX
decoded inline, then read it as prose and let the text dictate every parameter.

Then verify numerically against the post's own claims rather than by eye. In the
pilot the text asserted gradient 2 at (1,1), 0 at (1,−1), slope 0 along x = −2,
infinite at y = 0, near-flat at y = ±1.6, and each was checked in code.

Two parameters came out of the text rather than taste, and both are the kind of
thing to look for again: the sample spacing had to be 0.4 rather than 0.5,
because the post describes near-flat lines at y = ±1.6 and a 0.5 grid lands on
1.5; and the lattice had to be aligned on zero, or the row of vertical lines at
y = 0 that one figure boxes would not exist. Original aspect ratios are also
recoverable from the `?resize=WxH` parameters still in the HTML, which is how the
two-panel layout of one figure was identified before drawing it.

Leave a gap rather than invent a figure. A wrong figure in a teaching post is
worse than a missing one.

### Progress

As of 2026-09-09: 56 scripts, 277 images written, and every missing image in
the archive, of any format, is either drawn or recorded in
`_reconstruction/not-reconstructed.md` with its reason. Measured the same way at
both ends (`git ls-tree` at sanxofon's last commit against the working tree),
the archive went from 561 missing image files to 157, and from 226 posts intact
of 427 to 334.

The first sweep triaged on file format, looking only at PNGs, and so missed a
whole tier of the blog's own diagrams stored as JPEGs and animated GIFs. Do not
repeat that: sweep by what a figure is, not by what it is called. What remains
missing is photographs, posters, screenshots of other people's slides, figures
from the papers a post surveys, and a handful of cases where the data behind a
plot is gone.

One script per post under `_reconstruction/posts/`, each writing straight into
`wp-content/uploads/` and asserting the post's own arithmetic before it draws.
`rebuild_all.py` runs the lot and doubles as the regression test for changes to
`figstyle`. `dump_post.py <post.html>` prints a post as prose with figure slots
and the equations as $...$ source; that is the way in to a new
post. Never guess an upload path: `figstyle.paths_in(post)` reads the YYYY/MM
directory out of the HTML.

One editorial point to raise with Jonathan: his text says "Along the y-axis we
have vertical lines", but the reason he then gives is that tan(y) = 0 when y = 0,
which is the x-axis. The reconstruction boxes y = 0, following the explanation
rather than the wording.

### The originals were Mathematica

Three figures recovered from the archive settle this. `approxfunc.png` and
`plboth.png` are Mathematica `Plot` output: axes crossing at the origin, no
frame, no grid, tick labels sitting on the axes themselves, and in `plboth` a
`GraphicsRow` pair. `p3dlineb.png` is a `Plot3D` with the default surface
colours and a dark mesh. Reconstructions sit beside these on the same pages, so
`figstyle.axes()` draws crossed unlabelled axes by default, falling back to a
frame only where the origin lies outside the plotted range, and
`figstyle.mma_axes`/`plane` match the 3D look.

If a post you are working on still has a surviving figure, look at it before
drawing its siblings. It is the best guide available.

### Marking reconstructed figures

Jonathan decided on 2026-10-13: clean images, with the note in the file
metadata. `figstyle.stamp` writes `figstyle.NOTE` into the PNG, JPEG or GIF
without re-encoding it, and `rebuild_all.py` stamps every image a run writes.
`figstyle.VISIBLE_MARK = True` would print it under the figure again.

Slips in Jonathan's own posts are corrected in the HTML at his request
(2026-10-13): p=11480, p=13193, p=11387, p=12480, p=15794, p=13259 and p=16848.
Each script's docstring records what the post said before.

### Repeatable output

`rebuild_all.py` run twice gives byte-identical images; check that after any
change to `figstyle`. Two things broke it before. Pillow's JPEG encoder (10.0.1
in this environment) gives different bytes for the same pixels between runs,
sometimes with a smudge along the last row, so `figstyle.save` writes JPEGs
through macOS `sips`. And `G.subgraph()` in networkx orders nodes by string
hash, which moves a seeded spring layout between runs; build graphs in a fixed
order.

## Conventions

- Scripts that did real work live in `_reconstruction/`. Keep new ones there.
- `_clean_tools/` is sanxofon's original cleaning kit; leave it as provenance.
- The repo is ~420 MB with history. Pages allows 1 GB, so there is room, but
  don't add camera originals back without downscaling.
