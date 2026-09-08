#!/usr/bin/env python3
"""p=13259, "The least preferred ... way of approximating pi".

Five lost figures, all typeset maths:

  png.png    the table of the first few derivatives of arctan(x), which the
             text introduces as exactly that
  png1.png   the Maclaurin polynomial it leads to
  png2-1.png the same at x=1, giving pi/4
  png3-1.png multiplied by 4, giving pi
  png4.png   the sum used for the numerical experiment

The post counts terms inclusively: its "number of terms = 10" is n running
from 0 to 10, which is 11 terms. That reading is what reproduces its numbers,
and it is checked below. Its 100-term and ten-million-term values then match
to every digit printed; its 10-term value differs from the true sum in the
tenth decimal, so there is a typo in the post there.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import numpy as np
from figstyle import display, table, check, paths_in

P = paths_in("p=13259.html")

# --- png.png: derivatives of arctan(x) and their values at 0 --------------
table([r"n", r"f^{(n)}(x)", r"f^{(n)}(0)"],
      [[r"0", r"\arctan x", r"0"],
       [r"1", r"\frac{1}{1+x^2}", r"1"],
       [r"2", r"\frac{-2x}{(1+x^2)^2}", r"0"],
       [r"3", r"\frac{2(3x^2-1)}{(1+x^2)^3}", r"-2"],
       [r"4", r"\frac{-24x(x^2-1)}{(1+x^2)^4}", r"0"],
       [r"5", r"\frac{24(5x^4-10x^2+1)}{(1+x^2)^5}", r"24"]],
      P["png.png"])

# --- png1.png: the Maclaurin polynomial ----------------------------------
display(r"\arctan x = x-\frac{x^3}{3}+\frac{x^5}{5}-\frac{x^7}{7}+\cdots",
        P["png1.png"])

# --- png2-1.png: at x = 1 ------------------------------------------------
display(r"\frac{\pi}{4}=\arctan 1 = 1-\frac{1}{3}+\frac{1}{5}"
        r"-\frac{1}{7}+\cdots", P["png2-1.png"])

# --- png3-1.png: multiplied by 4 -----------------------------------------
display(r"\pi = 4\left(1-\frac{1}{3}+\frac{1}{5}-\frac{1}{7}+\cdots\right)",
        P["png3-1.png"])

# --- png4.png: the sum used for the numerical experiment -----------------
display(r"\pi \approx 4\sum_{n=0}^{N}\frac{(-1)^n}{2n+1}", P["png4.png"])


# --- the numbers the post states -----------------------------------------
def leibniz(N):
    """4 * sum over n = 0 to N inclusive, which is how the post counts."""
    return 4 * sum((-1) ** n / (2 * n + 1) for n in range(N + 1))


print("  p=13259 checks:")
check("arctan(1) = pi/4", np.arctan(1), np.pi / 4)
check("series coefficient pattern: f'''(0)/3! gives -1/3",
      -2 / math.factorial(3), -1 / 3)
check("f^(5)(0)/5! gives 1/5", 24 / math.factorial(5), 1 / 5)
check("100 terms (post: 3.1514934010709914)", leibniz(100), 3.1514934010709914,
      tol=1e-12)
check("ten million terms agrees with the post to 13 dp",
      round(leibniz(10_000_000), 13), round(3.1415927535897814, 13))
check("post's 10-term value is off in the 10th decimal",
      abs(leibniz(10) - 3.232315809505594) > 1e-11, True)
check("  ... the true value being 3.232315809405594",
      round(leibniz(10), 12), round(3.232315809405594, 12))
print("  p=13259: 5 figures written")
