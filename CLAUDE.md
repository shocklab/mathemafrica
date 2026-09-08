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

## State as of 2026-09-08

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

Not done: the domain, and the figure reconstruction below.

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

**The equations are LaTeX hiding in image URLs.** Maths renders through
`s0.wp.com/latex.php?latex=...`, which still works, and the query parameter holds
the original LaTeX source. That is how the figure inventory recovered the
mathematical context around each lost image. 8,660 equations depend on that
service, so converting them to MathJax would cut the last outside dependency.

**A hidden spam link was injected into the archive.** A backdoored
`traffic-stats-widget` plugin put a `display:none` link to garcinia-cambogia.fr
into 793 pages. Removed. Check for its like before republishing anything else.

**Do not trust the test browser on image failures.** It caches 404s from earlier
in a session and will report images broken long after they are being served.
Verify with `curl` against the live URL, checking status, content-type and
length, before concluding anything is wrong.

## The domain

Not lost. Still registered at GoDaddy, expiring **2026-11-06**, still delegated
to `ns5/ns6.kasserver.com` (All-Inkl), but the zone is empty so nothing resolves.
The hosting lapsed, not the registration, which means it cannot simply be bought;
it needs access to the registrar or the DNS account. If nobody renews by the
expiry it will drop, and a domain with this much inbound linkage is likely to be
caught by a drop-catcher rather than sit waiting.

Once there is DNS control, the records and the `CNAME` step are in `README.md`.
While doing that, consider making `og:url` and `og:image` absolute again; they
are currently relative, which is no worse than the broken state they were in, but
is wrong for social sharing.

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

### Pilot

Six figures for `p=13193.html`, "Checking direction fields", complete and
verified, in `_reconstruction/pilot-direction-fields/` with the script that made
them. **They have not been placed into `wp-content/uploads/`**, pending the two
decisions below.

One editorial point to raise with Jonathan: his text says "Along the y-axis we
have vertical lines", but the reason he then gives is that tan(y) = 0 when y = 0,
which is the x-axis. The reconstruction boxes y = 0, following the explanation
rather than the wording.

### Open decisions, both Jonathan's, both applying to all 222

1. **Should a reconstructed figure be visibly marked as one?** The pilot carries
   a small grey "figure reconstructed from the post text, 2026" in the corner.
   The alternatives are a clean image with the list recorded in `README.md`, or a
   clean image with the note in the PNG metadata. This matters for whether a
   reader can tell an original from a reconstruction.
2. **What should the figures look like?** The pilot uses a neutral matplotlib
   style making no claim to match the originals. Jonathan may remember what he
   drew them in; if it was Mathematica the styling should probably follow.

He was asked both and shut the session down before answering, so ask again
before generating at scale.

## Conventions

- Scripts that did real work live in `_reconstruction/`. Keep new ones there.
- `_clean_tools/` is sanxofon's original cleaning kit; leave it as provenance.
- The repo is ~420 MB with history. Pages allows 1 GB, so there is room, but
  don't add camera originals back without downscaling.
