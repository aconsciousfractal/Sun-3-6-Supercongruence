# Sun's supercongruence for two Apéry-like binomial sums

This repository accompanies the proof of Zhi-Hong Sun's Conjecture 3.6 in
*Supercongruences involving Apéry-like numbers and binomial coefficients*,
AIMS Mathematics **7** (2022), 2729–2781,
[DOI 10.3934/math.2022153](https://doi.org/10.3934/math.2022153).

For the Franel numbers and their binomial transform

$$
f_n=\sum_{j=0}^{n}\binom nj^3,\qquad
Q_n=\sum_{k=0}^{n}\binom nk(-8)^{n-k}f_k,
$$

the manuscript proves, for every odd prime $p$,

$$
\sum_{n=0}^{p-1}\binom{2n}{n}\frac{Q_n}{(-32)^n}
\equiv
\sum_{n=0}^{p-1}\binom{2n}{n}\frac{Q_n}{64^n}
\equiv
\begin{cases}
4x^2-2p,&p=x^2+2y^2\equiv1,3\pmod8,\\
0,&p\equiv5,7\pmod8,
\end{cases}\pmod{p^2}.
$$

The proof treats the two sums separately. A finite differential invariant
gives the inert-prime branch, including a lifting formula at simple singular
points. Modular identities, a degree bound for a Hecke polynomial and an
independent coefficient congruence give the split-prime branch. The primes
3 and 5, the coefficient of degree p and the two complex-multiplication
matrix cases are treated explicitly.

## Read and reproduce

- [Manuscript PDF](paper/Sun_3_6_Supercongruence.pdf) and
  [standalone LaTeX source](paper/Sun_3_6_Supercongruence.tex).
- [Reader's guide](docs/READING_GUIDE.md), [claim and evidence map](docs/CLAIM_MAP.md)
  and [source notes](docs/SOURCES.md).
- [Reproduction instructions](REPRODUCE.md), [companion](companion/README.md)
  and [evidence guide](docs/EVIDENCE.md).

From the repository root, with Python 3.10 or later:

```text
python -B scripts/verify.py --expected evidence
python -B -m unittest discover -s tests -v
python -B scripts/check_manifest.py
```

Core verification uses only the standard library and no network. Optional
symbolic identities and PDF rebuilding are documented in REPRODUCE.

## Scope and identity

Finite prime checks supplement the written proof. The modular coefficient
certificates become sufficient only together with the proved holomorphy and
valence bound. Neither a successful replay nor a file digest proves the
all-prime statement. The congruence is modulo p²; the analogous equality
modulo p³ already fails at p=7.

The work has not undergone independent specialist human review. No claim of
bibliographic priority is made. See [AI assistance](AI_USE.md).

Version: **0.1.0**. EVIDENCE_SHA256.txt identifies the computational core;
its digest is also printed in the manuscript. MANIFEST_SHA256.txt identifies
the complete distribution. These inventories are not signed authenticity
claims. A package version does not denote a journal version of record.

Companion repository:
[aconsciousfractal/Sun-3-6-Supercongruence](https://github.com/aconsciousfractal/Sun-3-6-Supercongruence).

Code, certificate data and documentation use [MIT](LICENSE); the manuscript
uses [CC BY 4.0](LICENSE_MANUSCRIPT.md). See [licence scope](LICENSE_SCOPE.md)
and [citation metadata](CITATION.cff).
