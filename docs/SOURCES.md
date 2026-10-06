# Sources and mathematical dependencies

The bibliography is attached to the mathematical statements actually used.
Fixed preprint versions below identify the relevant source text; a preprint
version is not conflated with a later version of record. Third-party PDFs are
not redistributed by this repository.

| Source | Precise use |
|---|---|
| Zhi-Hong Sun, *Supercongruences involving Apéry-like numbers and binomial coefficients*, AIMS Mathematics **7**(2) (2022), 2729–2781, [DOI 10.3934/math.2022153](https://doi.org/10.3934/math.2022153) | Q definition and recurrence, pp.2729–2730; Theorem 3.7, p.2740, for the initial congruences modulo p; Conjecture 3.6, p.2742, is the target. Theorem 3.5 modulo p is used only for the auxiliary squarefree-factor description. |
| Guo-Shuai Mao, *Congruences involving Franel numbers and Apéry-like numbers*, ResearchGate preprint (2023), [DOI 10.13140/RG.2.2.23378.73922](https://doi.org/10.13140/RG.2.2.23378.73922) | Theorem 1.4, p.3, in the author-uploaded text dated 8 January 2025: a refinement for Q_np modulo p³, for primes p>3. Its n=1 case reduced modulo p² implies the Q_p endpoint. |
| Armin Straub, *Gessel–Lucas congruences for sporadic sequences*, [arXiv:2301.12248v1](https://arxiv.org/abs/2301.12248v1) | Equation (10) and Theorem 3.2, p.5: A_F(p^r n) ≡ A_F(p^(r−1)n) modulo p^(2r), p≥3. The sign convention is A_F(n)=(-1)^n Q_n. |
| Ofir Gorodetsky, *New representations for all sporadic Apéry-like sequences, with applications to congruences*, [arXiv:2102.11839v2](https://arxiv.org/abs/2102.11839v2) | Proposition 1.2, formula (1.8), p.4, and Proposition 3.3, row F: a five-row multinomial representation. The present manuscript also derives the required endpoint directly from this representation. |
| Frits Beukers, *Supercongruences using modular forms*, [arXiv:2403.03301v3](https://arxiv.org/abs/2403.03301v3) | Lemma 3.7, pp.17–18, supplies the Hecke-orbit mechanism; the level-six case is also proved explicitly. The proof of Theorem 6.1, p.24, supplies the degree-p coefficient-comparison mechanism, with zero-to-pole ratio 1/3 and modulus p³. Here the correction is `(binom(2p,p) Q_p + 12)t^p`, the ratio is 1/2 and the argument is established modulo p²; neither that theorem nor the general modulo-p³ theorem is invoked. |
| Jeremy Rouse and John J. Webb, *On spaces of modular forms spanned by eta-quotients*, [arXiv:1311.1460v3](https://arxiv.org/abs/1311.1460v3) | Newman modularity criterion and Ligozat cusp-order formula, p.2. |
| William Craig, *New Types of Sturm bounds via p-adic transfer methods*, [arXiv:2602.10240v1](https://arxiv.org/abs/2602.10240v1) | Only the classical bound recalled in Theorem 1.1(1), p.2; no new transfer theorem for quasimodular forms is used. |
| NIST Digital Library of Mathematical Functions, [§23.18, equations 23.18.5–7](https://dlmf.nist.gov/23.18) | Dedekind eta transformation, multiplier and principal square-root convention for the exact cusp phases. |
| Heng Huat Chan and Shaun Cooper, *Rational analogues of Ramanujan's series for 1/π*, Math. Proc. Cambridge Philos. Soc. **153**(2) (2012), 361–383, [DOI 10.1017/S0305004112000254](https://doi.org/10.1017/S0305004112000254) | Related modular-period formulas. The period in this paper is independently certified; this citation is corroborative. The recurrence parameter c has the opposite sign in their convention. |

## Boundaries of the imports

Mao's stronger congruence includes a nonzero correction term in general:
Q_np ≡ Q_n − 5 n² p² Q_(n−1) (p/3) B_(p−2)(1/3) modulo p³.
The Bernoulli polynomial value is p-integral for p>3. Set n=1 and reduce
modulo p² to obtain Q_p ≡ −6. This result does not assert Q_p ≡ −6 modulo
p³, and it does not evaluate the two sums in the main theorem. The retained
Straub/Gorodetsky argument covers the endpoint also at p=3.
The ResearchGate landing page labels the preprint December 2023; the full
text examined there is the author's January 2025 upload. These are distinct
dates, not an assertion that the present text is identical to its first version.

The printed proof of Sun's Theorem 3.7 passes through a denominator 100.
This argument is used here only for p>5. The manuscript supplies an autonomous
initial residue and computation at p=5; p=3 is handled directly as well.
The source theorem is not being used to import the conjectured modulo-p² lift.

Straub's proof for F uses Gorodetsky's representation. Citing both does not
make them two independent genealogies of the endpoint result. The imported
statements concern individual coefficients and are independent of the two
truncated sums evaluated in the main theorem.

Theorem 3.5 modulo p and Conjecture 3.5 modulo p² in Sun's article are different
statements. The latter is not a dependency of this paper.

The source checks are targeted to these dependencies. They do not constitute
an exhaustive review of antecedents or establish bibliographic priority.
