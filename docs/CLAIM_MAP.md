# Claims, proof obligations and finite checks

The manuscript is the mathematical argument. This map identifies its inputs
and the precise role of the companion; a finite replay is not a proof for
all primes. Section titles and TeX labels remain stable across pagination.

| Claim | Written argument | Computational support and its limit |
|---|---|---|
| Both sums satisfy Sun's Conjecture 3.6 modulo p² for every odd prime | Theorem `thm:main`; separate inert and split proofs, with p=3 and p=5 explicit | `prime_regression.json`: 302 odd primes from 3 to 1999. Recurrence coefficients are compared with the original binomial definition through degree 198; 88 sum values are recomputed directly from that definition. |
| Full finite invariant modulo p² | Proposition `prop:finite-invariant`, exact residual and the two resonant coefficients at p and 2p; no removal of the upper half of the sum | `invariant_certificates.json`: 44 complete invariant polynomials and 88 resonant integer equalities for primes 5–199. The generic product-rule identity is an optional symbolic check. |
| Ordinary zeros lift for every representative; singular zeros have a precise defect | Lemma `lem:multiplicities`, Theorems `thm:ordinary-lift`, `thm:exact-singular-lift`, `thm:defect`, and Corollary `cor:root-discs` | The same JSON tests 39,608 ordinary lifts and 4,634 singular lifts/defects. The generic multiplicity and lifting proofs are in the text. |
| Inert branch, including p=5 | Section `sec:inert`; Sun's Theorem 3.7 is used only for p>5, followed by the lifting results. The p=5 residue and modulo-25 argument are autonomous | Original coefficients, exceptional-prime terms and shifted-singularity counterexample. No claimed lifting beyond the proved hypotheses. |
| The coefficient of degree p is paid independently | Lemma `lem:endpoint`: Mao's Theorem 1.4 implies the Q_p congruence for p>3; Straub's Theorem 3.2 covers all odd primes; also the explicit all-pure/non-pure row argument from Gorodetsky's representation | `endpoint_certificate.json`: 26 Laurent constant-term values and 18 pure-row configurations. `prime_regression.json`: 604 coefficient congruences. Neither finite range proves the generic endpoint. |
| Eta data and exact cusp phases | Section `sec:period` and Appendix `app:cusps`; modularity criterion, divisor calculation and Dedekind transformation law | `eta_certificates.json`: exact exponents, cusp orders, all eight rational multiplier phases and both signed cusp values. |
| The period G(t(q)) equals Θ(q) | Lemmas `lem:eta-identities`, `lem:weight8` and the period argument in `sec:period`: covariance and holomorphy precede the valence bound, then the differential equation determines every coefficient | The eta certificate checks the three weight-2 coefficients and both weight-8 residuals through q⁸, plus longer consistency windows. The finite coefficients are sufficient only with the written modularity, holomorphy and bound. Optional symbolic identities check the rational substitutions into the invariant. |
| Character, projective quotient, divisors and CM values | Section `sec:geometry`: explicit transformations of h, character of Θ, degree-four rational coordinate, eta inversion and the W₂ fixed point | Eta data plus optional rational identities and bounded normalizer permutations. The projective group and divisor arguments are not established by bounded checks. |
| Integral Hecke polynomial and degree bound for every p>3 | Section `sec:Hecke`: explicit generic orbit reduction, cusp holomorphy, pole bound, cyclotomic integrality and triangular expansion in t | `hecke_polynomials.json`: five independently reconstructed polynomials at p=5,7,11,17,19, with 311 integer coefficients. These examples do not prove the generic statement. |
| Finite polynomial identity before specialization | Section `sec:finite`: the two-term modulo-p² kernel, leading coefficient modulo p, degree bound and `binom(2p,p) Q_p ≡ -12` | Coefficient-wise checks for the five delivered Hecke polynomials. The manuscript explains why the degree-p term vanishes and why infinite-series evaluation is unnecessary. |
| Exact CM roots and rational trace | Section `sec:split`: all three Bézout constructions, character sign and separate p-adic embeddings when 3 divides x | 288 exact matrices through p=1999 and six exact quadratic factors at the split Hecke examples. Wrong signs and corrupted matrices are rejected by tests. |
| Auxiliary squarefree-factor description | The separately identified auxiliary argument uses Sun's Theorem 3.5 modulo p, not Conjecture 3.5 modulo p² | Optional `structure_certificates.json` checks primes 5–199. This auxiliary result is not needed for the main theorem. |

The optional symbolic run produces `symbolic_identities.json` (24 identities)
and `structure_certificates.json` (15 identities, plus bounded permutations
and squarefree decompositions). They are generated on request and are not
part of the six supplied core JSON files. Their count is a count of selected
algebraic identities, not of all steps in the proof.

The counterexample to a stronger precision is also retained: at p=7 the sums
are 294 and 49 modulo 343. The theorem asserts their equality modulo 49.

The package does not certify novelty, priority, formal verification or
independent human specialist acceptance. The complete distribution and
computational subset have separate inventories; see [evidence](EVIDENCE.md),
[sources](SOURCES.md) and [reproduction](../REPRODUCE.md).
