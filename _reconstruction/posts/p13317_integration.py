#!/usr/bin/env python3
"""p=13317, "Integration sounds like interrogation and that scares me".

Ten lost figures, all typeset maths. The post's prose fixes the whole shape of
the argument: x=3 is the midpoint of the bounds, the first Taylor term is 1/2,
integrating it over the interval gives exactly 1, the answer is 1, and the mean
value over [2,4] is 1/2. Those together pin the interval to [2,4] and the
integrand to the classic symmetric form

    I = int_2^4  f(x) / ( f(x) + f(6-x) )  dx  =  1

since the value at the midpoint is f(3)/(f(3)+f(3)) = 1/2 and (b-a)/2 = 1.

What the text never writes is the particular f. The friend's "scary" integrand
lived only inside integral.png, so it is genuinely unrecoverable. Every display
here is therefore written for a general f, which changes none of the
mathematics; the argument the post makes is about the symmetry and not about
which f it is applied to. integral.png carries a line saying so, because that
one figure is presented as the question exactly as it was sent.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
from figstyle import display, stack, check, paths_in

P = paths_in("p=13317.html")
INTEGRAND = r"\frac{f(x)}{f(x)+f(6-x)}"

# --- integral.png: the question as it was sent --------------------------
stack([r"\int_{2}^{4}" + INTEGRAND + r"\,dx"],
      P["integral.png"],
      note="the original named a particular f(x); that image is lost")

# --- integral2.png: the Taylor polynomial about x = 3 -------------------
stack([r"g(x)=" + INTEGRAND,
       r"g(x)\approx g(3)+g'(3)(x-3)+\cdots",
       r"g(3)=\frac{f(3)}{f(3)+f(3)}=\frac{1}{2}"],
      P["integral2.png"])

# --- integral3.png: keeping only the first term -------------------------
display(r"g(x)\approx\frac{1}{2}", P["integral3.png"])

# --- integral5.png: integrating that first term -------------------------
stack([r"\int_{2}^{4}\frac{1}{2}\,dx=\left.\frac{x}{2}\right|_{2}^{4}=1"],
      P["integral5.png"])

# --- int-1.png: naming the integral -------------------------------------
display(r"\mathrm{Let}\quad I=\int_{2}^{4}" + INTEGRAND + r"\,dx",
        P["int-1.png"])

# --- int9.png: the reflection lemma, proved ------------------------------
stack([r"\mathrm{Let}\quad J=\int_{a}^{b}h(x)\,dx,\qquad u=a+b-x",
       r"du=-dx,\qquad x=a\Rightarrow u=b,\qquad x=b\Rightarrow u=a",
       r"J=-\int_{b}^{a}h(a+b-u)\,du=\int_{a}^{b}h(a+b-u)\,du",
       r"\therefore\ \int_{a}^{b}h(x)\,dx=\int_{a}^{b}h(a+b-x)\,dx"],
      P["int9.png"], align="left", fontsize=15)

# --- int6.png: the lemma applied, a=2, b=4 -------------------------------
display(r"I=\int_{2}^{4}" + INTEGRAND + r"\,dx"
        r"=\int_{2}^{4}\frac{f(6-x)}{f(6-x)+f(x)}\,dx", P["int6.png"])

# --- int7.png: adding the two forms --------------------------------------
stack([r"2I=\int_{2}^{4}\frac{f(x)+f(6-x)}{f(x)+f(6-x)}\,dx"
       r"=\int_{2}^{4}1\,dx=2"], P["int7.png"])

# --- int8.png: the answer -------------------------------------------------
stack([r"2I=2", r"\therefore\ I=1"], P["int8.png"])

# --- mean.png: the mean value over the interval --------------------------
stack([r"\bar{g}=\frac{1}{4-2}\int_{2}^{4}" + INTEGRAND + r"\,dx"
       r"=\frac{1}{2}\times 1=\frac{1}{2}"], P["mean.png"])

# --- the identity, checked for several f ---------------------------------
print("  p=13317 checks:")
check("x=3 is the midpoint of [2,4] (post's observation)", (2 + 4) / 2, 3)
check("the integrand at the midpoint is 1/2 for any f",
      1 / (1 + 1), 0.5)
check("integrating that first term over [2,4] gives 1 (post's approximation)",
      quad(lambda x: 0.5, 2, 4)[0], 1.0)
for name, f in [("exp", np.exp), ("sqrt", np.sqrt),
                ("square", lambda t: t ** 2),
                ("log", lambda t: np.log(t + 1)),
                ("sin", lambda t: np.sin(t) + 2)]:
    val = quad(lambda x: f(x) / (f(x) + f(6 - x)), 2, 4)[0]
    check(f"  I = 1 for f = {name} (the post's exact answer)", val, 1.0,
          tol=1e-9)
check("mean value over [2,4] is 1/2 (post's closing check)", 1 / (4 - 2) * 1.0,
      0.5)
print("  p=13317: 10 figures written (the particular f is unrecoverable, "
      "see docstring)")
