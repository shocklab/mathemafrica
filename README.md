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
| post pages | 522 (33 more are linked but were never crawled) |
| static pages | 4 (about, blog index, contact, home) |
| monthly archives | 99 |
| tag / category / author pages | 81 / 42 / 40 |
| RSS feeds | 147, under `_xml/` |
| theme and plugin assets | complete |

## Known gaps

- **558 images were never captured.** 275 of the 522 post pages have at least
  one broken image. The files are only referenced, not present. Most should be
  recoverable from the Wayback Machine directly.
- Equations are rendered by WordPress's hosted LaTeX service
  (`s0.wp.com/latex.php`), which still works. Roughly 8,000 equations depend on
  it. If it ever goes away the maths will vanish, so converting to MathJax is
  worth doing eventually.
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

## Putting mathemafrica.org back in front of it

The domain is still registered (GoDaddy, expiring 2026-11-06) and still delegated
to `ns5/ns6.kasserver.com`, but the zone is empty, so nothing resolves. Restoring
it needs access to either the registrar account or the All-Inkl DNS account.

Once there is DNS control, at the DNS host:

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

## Licence

The posts belong to their authors. This repository exists to keep them readable.
