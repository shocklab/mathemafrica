# Mathemafrica archive

A static reconstruction of [mathemafrica.org](http://mathemafrica.org), the maths
blog that ran from 2014 to 2018 and was lost when its server stopped being paid
for. Live at **https://shocklab.github.io/mathemafrica/**.

## Provenance

The recovery from the Wayback Machine was done by
[sanxofon](https://github.com/sanxofon/mathemafrica); this repository is a fork
of that work with the fixes listed below. The cleaning scripts sanxofon used are
preserved in `_clean_tools/`.

The original site was WordPress with query permalinks, so pages were addressed as
`mathemafrica.org/?p=1234`. The recovery flattens those into files named
`p=1234.html`, all of them in the repository root.

## What is here

| | |
|---|---|
| posts | 426, plus 96 files that are query-string variants of the same posts (a further 33 posts are linked from the archives but were never crawled) |
| static pages | 4 (about, blog index, contact, home) |
| monthly archives | 99 |
| tag / category / author pages | 81 / 42 / 40 |
| RSS feeds | 147, under `_xml/` |
| theme and plugin assets | complete |

## Known gaps

- **Some images were never captured.** A recovery pass against the Wayback
  Machine restored the 127 that had been archived under the Jetpack CDN the
  site served images through. Of the rest, the mathematical figures have been
  redrawn from the text of their posts (below). Photographs, posters and
  material from other sources cannot be redrawn; each is listed with its
  reason in `_reconstruction/not-reconstructed.md`.
- The recovered photographs arrived as camera originals of 5184x3456, several
  megabytes each, which the pages display a few hundred pixels wide. The 70
  JPEGs over 1.5 MB were resized to a 1600 px longest side at quality 85,
  taking 260 MB down to 14 MB. Plots, screenshots and the animated GIFs were
  left untouched, and the originals remain in the git history.
- Comment forms, search and the login box post to WordPress endpoints that no
  longer exist. They are inert.
- Traffic-stats and rating widgets show frozen 2018 numbers.

## Changes made to sanxofon's recovery

- All 170,689 root-absolute `/mathemafrica/...` links and asset paths were made
  relative. Since every page sits in the repository root this resolves
  identically whether the site is served from a subpath or a domain root, so
  attaching a domain needs no further rewriting.
- Feed links were repointed at `_xml/`, where the feeds actually live.
- `.nojekyll` added. Without it GitHub Pages runs Jekyll, which hides any
  directory beginning with an underscore, and every feed 404s.
- A hidden SEO spam link (`garcinia-cambogia.fr`, `display:none`) injected into
  793 pages by a backdoored `traffic-stats-widget` plugin was removed.
- `index.html` maps legacy query permalinks onto the flattened filenames, so an
  old link to `/?p=1234` still lands on the right post.
- A `404.html` explains that the archive is partial, and falls back from
  addresses like `p=1234&share=twitter.html` to `p=1234.html`.
- Equations, which WordPress served as images from its hosted LaTeX service,
  are now LaTeX in the page, typeset by MathJax 3.2.2 from the copy in
  `mathjax/`. An equation that made up a whole paragraph is set as displayed
  maths. `_reconstruction/latex_to_mathjax.py` does the conversion.
- Lost figures are redrawn from the text of their posts, one script per post
  in `_reconstruction/posts/`, each checking the post's own numbers before it
  draws. `_reconstruction/rebuild_all.py` regenerates them all. Every redrawn
  image carries the note "figure reconstructed from the post text, 2026" in
  its file metadata.
- The `og:url`, `og:image` and canonical tags are absolute, so link previews
  and search engines resolve them.

## Putting mathemafrica.org back in front of it

At the DNS host for the domain:

    @      A      185.199.108.153
    @      A      185.199.109.153
    @      A      185.199.110.153
    @      A      185.199.111.153
    @      AAAA   2606:50c0:8000::153
    @      AAAA   2606:50c0:8001::153
    @      AAAA   2606:50c0:8002::153
    @      AAAA   2606:50c0:8003::153
    www    CNAME  shocklab.github.io.

and in this repository, add a `CNAME` file containing `mathemafrica.org`, then
enable HTTPS in the repository's Pages settings once the certificate is issued.
Finally point the sharing tags at the domain:

    python3 _reconstruction/absolute_urls.py https://mathemafrica.org/

## Licence

The posts belong to their authors. This repository exists to keep them readable.
