# Figures deliberately left missing

Not everything lost should be redrawn. These are the ones passed over on
purpose, with the reason, so nobody re-derives the decision later. Figures not
listed here are simply not done yet.

## Other people's work

| post | figures | why |
|---|---|---|
| p=11427, the Mandelbrot set | `Mandelset_hires.png` | The text says it is "an image taken from wikipedia". Not Jonathan's figure to reconstruct. |
| p=12064, "How much does a Dougie weigh on Jupiter?" | `Jupiter.png` | A screenshot of the abstract of a Nature paper (nature14278). Reproducing it would be reproducing the paper. |
| p=16040, "Scaled Reinforcement Learning" | all four: `RL_agent_env_int.png`, `cliff.png`, `DQN_graphicsx.png`, `dqn_algos.png` | Every figure on this post is credited in the text to someone else: two to Francois-Lavet et al. 2018, the cliff-walking gridworld to Sutton and Barto, and the algorithm box to Mnih et al. 2015. The agent-environment diagram is generic enough to redraw, but the post points at a particular rendition of it, so redrawing would put words in that citation's mouth. |
| p=11480, "MAM1000 part 36" | `steak_100km.png` | WordPress's cropped thumbnail of this one survives and shows it is an xkcd What If? figure, the falling-steak terminal-velocity plot. Randall Munroe's, not Jonathan's. |
| p=15060, "Introduction to Wolfram Mathematica programming" | `wcFolderIcon.png`, `upload-button.png`, `WCfileexplorer.png`, `downloadButton.png` | Screenshots of the Wolfram Cloud interface. Drawing imitations of another product's UI would be inventing evidence of what that product looks like. |

## Data that is not in the archive

| post | figures | why |
|---|---|---|
| p=12064 | `curvloc.png`, `smalllarge1.png`, `finallines.png`, `Dougieweight.png` | Every one of these plots data the post extracted, pixel by pixel, from a figure in that Nature paper. The paper's figure is not in the archive, so the density profiles behind all four are unavailable. Profiles fitted backwards to the post's stated answers (a 30 kg Dougie weighing about 71 kg at the outer limb and about 190 kg on the solid surface) would be invented data attributed to a published measurement. |

| p=10484, "Cooking with Mathematics" | `foodgroups3.png`, `foodgroups5.png` | The flavour-pairing data was scraped from an external site and is gone. The post quotes enough of it (five ingredients' lists, twelve seven-cliques, several named pairs) to rebuild a genuine subgraph, which is what the other two figures use, but not the whole graph. `foodgroups5` shows the path from eggplant to white chocolate with four ingredients between them, and the post never names those four; inventing them would be a fabricated claim about which flavours pair. |
| p=13826, "Graph Theory, Numberphile and Mathematica" | the two Mathematica screenshots | They show code that the post then quotes in full in its prose, so a reader loses nothing. A fabricated notebook screenshot would assert a formatting nobody can know. |

## Animations

A still cannot stand in for these, and the posts use them as animations.

- p=13659, "Guidelines for visualising ... volumes of revolution": `movie1-1.gif`, `movie.gif`
- p=11169, Pascal and Sierpinski: the surviving `ezgif.com-optimize.gif` is intact, so nothing is needed there

## Photographs

Roughly 110 of the lost images are photographs of people, events and workshops.
Nothing can reconstruct a photograph, and nothing should try. They are counted
in the archive's gap and left alone.

## Where a reconstruction goes past the text

These were drawn, but the text does not fix every detail, and the scripts say
so in their docstrings:

| post | figure | what was chosen |
|---|---|---|
| p=10954 | `RS.png`, `betweencurves.png` | The post fixes the rectangles as left-point with dx=0.02 from x=0 but never names f and g. A generic pair is used, and reused across both so the two agree. |
| p=13659 | `pl1`–`pl4-1` | "The equations don't matter for the visualisation" is the post's own wording. y=x^2 and y=4-x^2 are used, both above the line of rotation so the slices are annuli as described. |
| p=15781 | `K_means_elbow.png` | The original plotted a Kaggle FIFA19 dataset that is not in the archive. This is a real K-means run over stand-in data whose elbow falls at K=3 as the post's does, and the figure title says so. |
| p=13317 | all ten | The particular integrand lived only inside `integral.png`. Every display is written for a general f, which changes no mathematics; `integral.png` carries a line saying its original named a specific one. |
| p=16790 | all seventeen | Produced by running the post's method again. The digits are not the original ones; the behaviour reported, including the failure case, is reproduced. |
| p=11322 | `mult.png` | The post never names a z. 1+2i is used because it keeps z-bar-z on screen at the square shape the original had. |
| p=11646 | `p3dline.png` | The post says explicitly that this figure "is not from this example", so it only has to be a valid instance of three non-parallel planes sharing a line. |
