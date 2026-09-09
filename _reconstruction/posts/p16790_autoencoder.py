#!/usr/bin/env python3
"""p=16790, "Basic Reverse Image Search Using an Autoencoder".

Seventeen lost figures, none of which survive to copy. The post describes its
method completely, so these are produced by running it again rather than by
drawing anything: MNIST, an autoencoder compressing 784 down to a 32-dimensional
latent space, the test set encoded, and the four nearest neighbours of a query
image by Euclidean distance in that space.

The three example sets have to satisfy what the post says about them, and the
query images are picked on exactly those stated criteria:

  6_*   a query 6 whose four nearest are all 6s
  8_*   a query 8 whose four nearest are all 8s, the post's "the images
        returned correspond to the same numbers as those in the query image"
  5_*   the failure case: "the bottom of the 5 in the query image is closed,
        similar to what we would see from an 8. This could possibly explain the
        8's showing up in the nearest images." So the query is a 5 whose
        neighbours include at least one 8, and among those candidates the one
        whose lower loop is most nearly closed.

orig.png and reconstruction.png are an 8 and its reconstruction, the post
saying "we can clearly make out the shape of the 8".

These are not the original images: a different network on a different seed
returns different digits. What is reproduced is the method and the behaviour
the post reports, including the failure.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from figstyle import UPLOADS, NOTE, check, paths_in

P = paths_in("p=16790.html")
CACHE = "/private/tmp/claude-501/-Users-jonathanshock-Cursor-folders-Mathematica/fa8467c2-86f9-4523-91a8-5388d8cc081c/scratchpad/mnist"
torch.manual_seed(16790)
np.random.seed(16790)

tf = transforms.ToTensor()
train = datasets.MNIST(CACHE, train=True, download=True, transform=tf)
test = datasets.MNIST(CACHE, train=False, download=True, transform=tf)
Xtr = train.data.float().view(-1, 784) / 255.0
Xte = test.data.float().view(-1, 784) / 255.0
yte = test.targets.numpy()


class AE(nn.Module):
    def __init__(self, latent=32):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(784, 256), nn.ReLU(),
                                 nn.Linear(256, 64), nn.ReLU(),
                                 nn.Linear(64, latent))
        self.dec = nn.Sequential(nn.Linear(latent, 64), nn.ReLU(),
                                 nn.Linear(64, 256), nn.ReLU(),
                                 nn.Linear(256, 784), nn.Sigmoid())

    def forward(self, x):
        return self.dec(self.enc(x))


model = AE()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
lossf = nn.MSELoss()
EPOCHS, BATCH = 12, 256
for ep in range(EPOCHS):
    perm = torch.randperm(len(Xtr))
    tot = 0.0
    for i in range(0, len(Xtr), BATCH):
        b = Xtr[perm[i:i + BATCH]]
        opt.zero_grad()
        l = lossf(model(b), b)
        l.backward()
        opt.step()
        tot += l.item() * len(b)
    print(f"    epoch {ep + 1}/{EPOCHS}  train MSE {tot / len(Xtr):.5f}")

model.eval()
with torch.no_grad():
    Z = model.enc(Xte).numpy()
    recon = model(Xte).numpy()


def neighbours(i, k=4):
    d = ((Z - Z[i]) ** 2).sum(1)
    d[i] = np.inf
    return np.argsort(d)[:k]


def closedness(img):
    """How closed the lower loop of a digit is: ink in the bottom-left region.

    A 5 with an open bottom leaves that corner empty; a closed one fills it.
    Only used to rank candidate 5s, as the post describes its failure case.
    """
    g = img.reshape(28, 28)
    return float(g[18:26, 4:12].sum())


def pick(digit, want_same, rng, limit=400):
    """A test image of `digit` whose neighbours meet the post's criterion.

    For the success cases the first match in a shuffled order will do. For the
    failure case every candidate is scored and the most closed-bottomed 5 wins,
    since that is the specific 5 the post shows.
    """
    idx = np.where(yte == digit)[0]
    idx = idx[rng.permutation(len(idx))[:limit]]
    best, best_nb, best_score = None, None, -np.inf
    for i in idx:
        nb = neighbours(i)
        labs = yte[nb]
        if want_same:
            if np.all(labs == digit):
                return int(i), nb
            continue
        if 8 not in labs:
            continue
        score = closedness(Xte[i].numpy())
        if score > best_score:
            best, best_nb, best_score = int(i), nb, score
    if best is None:
        raise SystemExit(f"no candidate found for digit {digit}")
    return best, best_nb


rng = np.random.default_rng(16790)
i6, nb6 = pick(6, True, rng)
i8, nb8 = pick(8, True, rng)
i5, nb5 = pick(5, False, rng)


def tile(vec, dest):
    fig = plt.figure(figsize=(2.4, 2.4), dpi=110)
    ax = fig.add_axes([0.02, 0.08, 0.96, 0.90])
    ax.imshow(vec.reshape(28, 28), cmap="gray_r", interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#cccccc")
    fig.text(0.99, 0.005, NOTE, ha="right", va="bottom", fontsize=5.0,
             color="#9a9a9a")
    out = os.path.join(UPLOADS, dest)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=110, facecolor="white")
    plt.close(fig)


# the 8 used for the original/reconstruction pair
i_orig = i8
tile(Xte[i_orig].numpy(), P["orig.png"])
tile(recon[i_orig], P["reconstruction.png"])

for stem, q, nb, names in (("6", i6, nb6, ["6_0", "6_1", "6_2", "6_4", "6_5"]),
                           ("8", i8, nb8, ["8_0", "8_1", "8_2", "8_3", "8_4"]),
                           ("5", i5, nb5, ["5_0", "5_1", "5_3", "5_4", "5_5"])):
    tile(Xte[q].numpy(), P[names[0] + ".png"])
    for name, j in zip(names[1:], nb):
        tile(Xte[j].numpy(), P[name + ".png"])

# --- what the post says must be true -------------------------------------
print("  p=16790 checks:")
check("latent dimension is 32 (post's figure)", model.enc[-1].out_features, 32)
check("input dimension is 784 (post's figure)", 28 * 28, 784)
check("four nearest neighbours returned", len(nb6), 4)
check("query 6 is a 6", int(yte[i6]), 6)
check("  ... and all four neighbours are 6s (post's success case)",
      bool(np.all(yte[nb6] == 6)), True)
check("query 8 is an 8", int(yte[i8]), 8)
check("  ... and all four neighbours are 8s", bool(np.all(yte[nb8] == 8)), True)
check("query 5 is a 5", int(yte[i5]), 5)
check("  ... and its neighbours include an 8 (post's failure case)",
      bool(8 in yte[nb5]), True)
check("reconstruction is close to the original but not identical",
      bool(0 < np.abs(recon[i_orig] - Xte[i_orig].numpy()).mean() < 0.1), True)
print(f"    neighbour labels: 6 -> {yte[nb6]}, 8 -> {yte[nb8]}, 5 -> {yte[nb5]}")
print("  p=16790: 17 figures written")
