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

| p=12655, "Computational Complexity: Article 3" | `turing.png` | "I have included a picture from Wikipedia", captioned "Turing Machine Illustration, Wikipedia, (Drawing after Minsky, 1967)". |
| p=16174 and p=16331, "Systems of Reasoning" | `logic-things-1.png`, `logic-thing-2.png`, `logic-thing-3.png` | "The image comes from the textbook mentioned above". Scans of a logic textbook's pages. `capeholly.jpg` on the same post is a photograph of trees. |
| p=14586, "PDE Part I" | `wing-flow.jpg` | Captioned "Source: CFDIinside blog". |
| p=16521, "Inverse Reinforcement Learning" | `RL-vs-IRL.png`, `tennis.jpg`, `bernie.jpg` | The diagram is captioned "Image source: Inverse Reinforcement Learning"; the other two are stock photographs the post links out for. |
| p=16997, "CRL Task 1" | `ZB-2017-1.jpg`, `B-kl-UCB.png`, `UC-DTR.png` | Algorithm boxes and a figure reproduced from Zhang and Bareinboim, which the post cites as [16], [17] and [18] and tells the reader to "refer to the source material". |
| p=17025, "CRL Task 2" | `ZB-2019-Fig1.png`, `ZB-2019-Fig4.png` | Figures 1 and 4 of the same authors' 2019 paper, as the filenames say. |
| p=16082, "The Res-Net-NODE Narrative" | `Screenshot-120.png` | The residual-network against neural-ODE vector-field comparison, which is Figure 1 of Chen et al.'s Neural ODE paper. |
| p=15845, "Captain Raymond Holt vs Claude Shannon" | `images-2.jpeg`, `Screenshot-2019-09-10-at-01.20.38.png` | A still from the television episode, and a working shown as "taken from (2)". |
| p=15609, "Review: Calculus Reordered" | `9780691181318.png` | A book cover, named by its ISBN. |
| p=11877, p=11950, p=11952, p=11956, p=11998, p=12002, p=12026, the Elephant Delta 2015 live-blog | `wordcloud.png`, `Pachinkogram.png`, `rubiks.png`, `proj1.png`, `proj2.png`, `projective.png`, `table-quinn.png`, `room.png`, `room-2.png`, `room-3.png`, `abstract.png`, and `talk5.png` on the November 2015 index | Notes taken live during other people's conference talks, each post headed by the speaker's name. The images are their slides, a wordcloud the room generated in the session, an abstract, and three photographs of Sheffield Hallam's learning space credited in the post to a journal issue. |
| p=15105, June Barrow-Green's talk in Oxford | `Screenshot-2019-06-17-18.27.48.png` | The same: live notes on someone else's talk, and this is a screenshot of the speaker's material on Eva Bayer-Fluckiger's 1992 'Dear Sir' postcards. The post says outright that "nothing should be used to quote the speaker from this article". |
| p=12372, two posts open at UCT | `Science-SCI_16041_L_MAM_teaching-md1.png` | A screenshot of the advertisement PDF for the teaching post. Its sibling `SCI_16040_L_SL_MAM.png` survives, so the pair is half there; inventing a department's job advert is not a reconstruction. |
| p=16931, "Causal Reinforcement Learning: A Primer" | `ModelBasedDiagram.png` | Dropped into the text with no caption and nothing describing it, on a post whose references carry a header-image credit and whose siblings reproduce figures from Zhang and Bareinboim. There is nothing to reconstruct it from. |
| p=13509, "Counting to Infinity" | `20170728_101802.png` | A phone photograph of a hand-drawn sketch. |
| p=11143 | `twothirds.png` | A histogram of the class's actual guesses in the two-thirds-of-the-average game. The post reports only the winning guess of 20 and one of 20.333; the rest of the data is gone, and a histogram invented around two known values would be fabricated data about real people. |

## Where the post's own numbers cannot be reproduced

| post | figure | why |
|---|---|---|
| p=15582, "Investigating Practical Ordering of Grids" | `timevscomplexity.png` | The post reports the average hitting time as under 1000 steps for variations (a) to (g), just over 1000 for (h) and "around 100000" for (i). Solving the hitting time exactly does not give that. On the reduced graph it falls steadily, 542 down to 324. Under a bounce-back move model, where a blocked move wastes a step, it dips and then rises, 602 to 501 to 648, which reproduces the post's qualitative claim that the last variation is the worst but not its two orders of magnitude. Drawing the figure would mean either inventing the post's numbers or setting a plot beside text it contradicts. The post's other three figures are reconstructed, including the connectivity one, whose flat line at 2 is its actual punchline. |

## Data that is not in the archive

| post | figures | why |
|---|---|---|
| p=12064 | `curvloc.png`, `smalllarge1.png`, `finallines.png`, `Dougieweight.png` | Every one of these plots data the post extracted, pixel by pixel, from a figure in that Nature paper. The paper's figure is not in the archive, so the density profiles behind all four are unavailable. Profiles fitted backwards to the post's stated answers (a 30 kg Dougie weighing about 71 kg at the outer limb and about 190 kg on the solid surface) would be invented data attributed to a published measurement. |

| p=10484, "Cooking with Mathematics" | `foodgroups3.png`, `foodgroups5.png` | The flavour-pairing data was scraped from an external site and is gone. The post quotes enough of it (five ingredients' lists, twelve seven-cliques, several named pairs) to rebuild a genuine subgraph, which is what the other two figures use, but not the whole graph. `foodgroups5` shows the path from eggplant to white chocolate with four ingredients between them, and the post never names those four; inventing them would be a fabricated claim about which flavours pair. |
| p=10615, "Cooking with Mathematics II" | `randomsample1.png` | `Graph[RandomSample[graphedges2,100],...]`: one random hundred of the graph's roughly 800 edges, drawn with every vertex labelled. The archive quotes the first few dozen pairs of that edge list and no more. |
| p=10749, "Cooking with Mathematics III" | `chain.png` | The shortest path from white chocolate to olives, which the post says is six ingredients long. It names the two ends and never the four between them, the same gap that leaves `foodgroups5.png` undrawn. |
| p=13826, "Graph Theory, Numberphile and Mathematica" | `Screenshot-2018-01-15-12.27.45.png`, `Screenshot-2018-01-15-13.52.13.png` | They show code that the post then quotes in full in its prose, so a reader loses nothing. A fabricated notebook screenshot would assert a formatting nobody can know. |

## Link previews and slides

WordPress inlined a screenshot of the page an author linked to. The link itself
is still in the text, so the reader loses a thumbnail and nothing else.

| post | figure | what it showed |
|---|---|---|
| p=11165, the binomial theorem | `aesthetic.png` | The article on three proofs of the binomial theorem, linked in the sentence before it. |
| p=11249, Taylor series in class | `Untitled.png` | The review paper on Ramanujan's series for pi, linked as "There is a nice review paper here". |
| p=11718, Fibonacci and the golden ratio | `Untitled.png` | The golden-spiral page linked in the sentence after it. |
| p=15139, "The Fundamental Theorem of Calculus, part 1 (part i)" | `Screen-Shot-2019-07-09-at-16.06.58.png`, `Screen-Shot-2019-07-09-at-16.07.27.png` | Two slides showing how the course fits together, "this is what we have looked at so far" and "This will be the new picture". A concept map whose nodes and arrows the text never lists. |

## Featured images

The picture at the head of a post, above the title. None of them is a figure,
and none is described anywhere in the text.

| post | image | what it was |
|---|---|---|
| p=10192, the AIMS newsletter | `2014-12-12-04.44.50-pm.png`, and the crops WordPress served in the sidebar, `2014-12-12-04.44.50-pm-52x50.png` and `2014-12-12-04.44.50-pm-180x138.png` | A screenshot of the newsletter's cover, dated by its own filename. |
| p=12398, the Next Einstein Forum | `nef-einstein1.png` | A photograph or poster from the forum; the post's other image, `setup-NEF.jpg`, is a photograph too. |
| p=13875, e-day | `eday.png` | The post's header artwork. |
| p=15897, the Cauchy distribution | `zGTLU.png` | Named by an image-host id rather than by anything, which is what a picture lifted from elsewhere looks like. |

## Animations

A still cannot stand in for these, and the posts use them as animations.

- p=13659, "Guidelines for visualising ... volumes of revolution": `movie1-1.gif`, `movie.gif`
- p=11169, Pascal and Sierpinski: the surviving `ezgif.com-optimize.gif` is intact, so nothing is needed there

## Photographs

Roughly 110 of the lost images are photographs of people, events and workshops.
Nothing can reconstruct a photograph, and nothing should try. They are counted
in the archive's gap and left alone.

## The JPEG and GIF tail

The first sweep looked for PNGs, which is a file format rather than an
editorial category, and it missed a tier of the blog's own diagrams stored as
JPEGs and animated GIFs. Those have since been drawn. What follows is
everything else in those two formats, so that the manifest covers the whole
archive and not one corner of it. Most of it is photographs, and a photograph
cannot be reconstructed by anybody.

| post | figures | why |
|---|---|---|
| p=13469, "Siyaphumelela conference" | `Carnegie-1.jpg`, `WhatsApp-Image-2017-06-27-at-18.37.16.jpeg`, `WhatsApp-Image-2017-06-27-at-18.37.41.jpeg`, `WhatsApp-Image-2017-06-27-at-18.38.22.jpeg`, `WhatsApp-Image-2017-06-27-at-18.57.16-1.jpeg`, `WhatsApp-Image-2017-06-27-at-18.57.16.jpeg`, `WhatsApp-Image-2017-06-27-at-18.59.54.jpeg`, `WhatsApp-Image-2017-06-27-at-19.00.15-1.jpeg`, `WhatsApp-Image-2017-06-27-at-19.00.15.jpeg`, `WhatsApp-Image-2017-06-27-at-19.00.23.jpeg`, `WhatsApp-Image-2017-06-27-at-19.00.43.jpeg` | Photographs taken at the conference, straight off a phone, plus the Carnegie logo. |
| p=13481, "Siyaphumelela, part 2" | `SIyaphumelela.jpg` | The conference's own logo. |
| p=12456, "Mathemafrica and the NEF #2" | `DSC00597.jpg`, `DSC00605.jpg`, `DSC00610.jpg`, `DSC00617.jpg`, `DSC00621.jpg` | Camera photographs from the forum. |
| p=1, "Mathematics Communication in Africa" | `1557358_733040443437209_1967139371182466938_o.jpg`, `1655694_733040073437246_2711029163490327134_o-52x50.jpg`, `1655694_733040073437246_2711029163490327134_o.jpg`, `AFC001-e1383652009860-52x50.jpg` | Photographs from the AIMS-IMAGINARY workshop. |
| p=10306, "AIMS-IMAGINARY Workshop 2014" | `1655694_733040073437246_2711029163490327134_o-180x138.jpg`, `AFC001-e1383652009860-180x138.jpg`, `leadimage-300x200.jpeg` | The same photographs, and WordPress's crops of the African-fractals artwork. |
| p=10178, "The fractals at the heart of African design" | `AFC001-e1383652009860.jpg` | The artwork the post is about, photographed. |
| p=16947, "Preliminaries for CRL" | `BCII-2020-FIg2.jpg`, `CausalProbabilityModels.jpg`, `GraphBuildingBlocks.jpg`, `RL_Diagram.jpg`, `SCM-Graphical_Models.jpg`, `d-separation_example.jpg` | Figures from the papers the post surveys, named after their authors and years. |
| p=17042, "CRL Task 3" | `CausalTS.jpg`, `FB-2019-Fig1.jpg`, `FB-2019-Fig2.jpg`, `FPB-2017-Fig3.jpg`, `FPB-2017-Fig4.jpg`, `ZB-2016-Fig1.jpg` | The same: figures from Zhang and Bareinboim, and from Forney and Bareinboim. |
| p=13762, "Brazil Delta keynote, Marcelo Borba" | `Borba-book.jpg`, `Joni-small.jpg`, `Marcelo.jpg`, `Modeling.jpg` | A photograph of the speaker, his book's cover, and slides from his talk. |
| p=13806, "Brazil Delta, Chris Rasmussen" | `Chris.jpg`, `book-insights.jpg`, `graph-active-l.jpg`, `saber-tooth.jpg` | A photograph of the speaker, a book cover, a cartoon, and the active-learning graph from Freeman et al. as it appeared on his slide. |
| p=13785, "Brazil Delta, David Easdown" | `David.jpg`, `SOLO.jpg` | A photograph of the speaker and the SOLO taxonomy diagram from his slide. |
| p=13818, "Brazil Delta, R. Nazim Khan" | `nazim.jpg` | A photograph of the speaker. |
| p=12019, "Elephant Delta, Joao Frederico Meyer" | `joni.jpg` | A photograph of the speaker. |
| p=11345, "complex numbers part iv" | `NPIFkhS6_400x400.jpg` | A 400x400 avatar, the size Twitter serves. |
| p=11415, "Mathematics or dreams (Sepedi)" | `MoMA-asymptote-of-dreams-01-2wp7d55jp0s8tswt4y8xz4.jpg` | A photograph of the MoMA piece the post discusses. |
| p=11500, "Galileoscope in action" | `Mathematics_architecture.jpg` | A photograph. |
| p=11559, "AIMS applications are open" | `AIMS-South-Africa-Masters-poster-NEW.jpg` | The recruitment poster. |
| p=11869, "The Tenth Southern Hemisphere Conference" | `poster.jpg` | The conference poster. |
| p=13170, "Mathematical Modelling for Infectious Diseases" | `Advertisement_2016-e1471425207735.jpg` | The course advertisement. |
| p=12563, "UCT maths is hiring" | `MAMhiring.jpg` | The advertisement. |
| p=14615, "Kovalevskaia research grants" | `KovaleskaiaAward2018.jpg` | The award's own artwork. |
| p=14684, "Shuttleworth Postgraduate Scholarship" | `ShuttleworthPostGradScholarship_UCT.jpg` | The scholarship advertisement. |
| p=14705, "USAf Teaching and Learning of Mathematics" | `R-Govender.jpg` | A photograph of the speaker. |
| p=14707, "Diagnostic Mathematics Information" | `robert-prince.jpg` | A photograph of the speaker. |
| p=13684, "The Seduction of Curves, a review" | `greenflash2.jpg` | A photograph. |
| p=12194, "Why radians?" | `GpuBOLO.jpg` | Captioned "Source: Imgur". |
| p=13931, "1. Sets" | `giphy.gif` | An animation from Giphy. |
| p=14224, "3. power sets" | `interesting.gif` | A reaction GIF. |
| p=14248, "2. Subsets" | `06d85daad5e49420eee5ccefd597782ca7ad37c03a306458f5ee865e6d22a5b6.jpg` | Named by a content hash, which is what a downloaded image looks like. |
| p=15108, "Omar Khayyam's geometrical solution" | `Kent.jpg`, `euc-115.gif` | A photograph of the speaker, and a page of Oliver Byrne's 1847 coloured Euclid, which the post links to: "Page taken from here". |
| p=16931, "Causal Reinforcement Learning: A Primer" | `CausalGraph.jpg` | Header artwork, credited in the references and described nowhere. |
| p=12797, "Proof by induction winner" | `inductionFor12_trdgia001.jpg`, `inductionFor12_trdgia002.jpg` | The winning entry itself, drawn and written by the student whose number names the files. |
| p=10700, "Cooking with Mathematics, part 2" | `cliquenumbers.jpg` | The number of cliques of each size, on a log scale, computed from the flavour-pairing graph that is not in the archive. |
| p=13680, "2017 2/3rds numbers game" | `gametheory.jpg`, `numbersgame2017.jpg` | Histograms of what four years of first-year classes actually guessed. The post gives this year's mean, 24.4, and the two closest guesses, and nothing else; the rest is real data about real people. |
| p=15105, "June Barrow-Green's talk" | `JGB.jpg` | The photograph of the speaker the post takes from Wikipedia. |
| p=10693, "Paying it Forward" | `RHS-28.jpg` | A photograph from the school the project ran in. |
| p=13190, "Cellular Automaton" | `try.gif` | A post with no text at all: a title, an animation, and nothing to say what the animation shows. |
| p=11261, "Could these have been the first computer games?" | `fig10.jpg`, `fig2.gif`, `fig4.gif`, `fig8.jpg`, `fig9.gif` | fig2 is credited to ehess.modelisationsavoirs.fr, fig4 to the book African Fractals, fig8 to Bouchet's manuscript and fig10 to Broline and Loeb's proof. fig9's determined position is named but not specified: the post says South has one pebble in pit B and North takes two pebbles in pit B, which cannot both be read off one board. |
| the listing pages | `Amanda_Weltman005.jpg`, `Morphett.jpg`, `greg-o.jpg`, `jonathan.jpg` | Author portraits, which appear beside a post's excerpt and nowhere else. |

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
| p=10311 | `multiplier1-e1426450380957.png` | The post fixes the shape of the Keynesian cross and every relation on it, but no numbers. b(1-t) = 0.6 and an autonomous rise of 10 are used, which makes the multiplier 2.5 and puts enough space between the steps of the staircase to label them. |
| Vectors part ii (2015/09) | `vec1.png` | The post's own page is not in the archive. Its excerpt on the September 2015 index carries the sentence the figure illustrates, which fixes the content; five copies of one arrow is a choice of five. |
| "Circular base, semi-circular top, triangular cross-section" (2015/08) | `triangcirc2.png` | That page is not archived either. The title fixes the solid: only an isosceles right cross-section gives a semicircular top, since equilateral slices give an elliptical one. Which slice to draw is free, and the one at y = 0.35r is drawn. |
| p=14148, Cartesian products | `download.jpg`, `thumbnail_Screen-Shot-2018-04-05-at-10.26.55-PM.png` | Both originals were found images rather than the author's, one named `download.jpg` and the other a screenshot. They illustrate "the set of all integers in 2D space" and the same in 3D, which is all that is drawn: the lattice points in a small window. |
| p=13535 | `pl1.jpg`-`pl6.jpg` | "We'll start with an arbitrary function f(x)", says the post, and never names one. The text does force it to increase across [0.5, 1.5], since left endpoints have to underestimate and right endpoints overestimate; the function drawn does, and the checks confirm the sums bracket the area and close in. |
| p=12734 | `graph-big-O.jpg`, `Omega.gif`, `graph-Theta.jpg` | The definitions are quoted in full and fix the shape. The constants and n_0 drawn are a choice, made to bound the post's own T(n) = 3n^3 + 5n^2 + 2n + 5 from n_0 = 2, which is checked rather than assumed. |
| p=13883 | `1_map-1.jpg`, `same_graph-1.jpg` | The roadmap's shape is free; its roads are drawn as curves whose own arc lengths become the weights on the abstracted map, so the two figures agree. Figure 3's graph is complete, as the text says, and is drawn on four vertices to match the four already on stage. |
| p=11261 | `mboard.jpg`, `fig3-.gif`, `fig5.gif`, `fig6.gif`, `fig7.gif` | The rules and Bouchet's table of periods fix which arrangement each figure holds, and the simulation reproduces every entry in that table. How a Mancala board is drawn, and whether the automaton is shown as a strip or as one row per move, are choices. |
| p=11592, p=11387, p=13671, p=11232, p=13183 | the animations | The functions, points, vectors and stages are all named in the posts. Frame counts, timings and camera angles are not, and are chosen. In `try.gif` the two vectors lie along one line, so the shorter is drawn solid and the longer dashed over it rather than either being moved off the line. |
