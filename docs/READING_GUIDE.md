# Reading the proof and companion

Start with the main theorem and definitions in the manuscript. There are two
sums, both truncated at p−1, with denominators −32 and 64. The target is
modulo p² for every odd prime; the residue is a quadratic-form trace in the
split classes and zero in the inert classes.

## A short first pass

1. Read the main theorem, proof outline and stated source dependencies.
2. Read the local lifting result and the independent endpoint congruence.
3. Read the finite polynomial specialisation and the final CM calculations.
4. Consult [CLAIM_MAP](CLAIM_MAP.md) for the distinction between proof,
   source import, sufficient finite certificate and bounded regression.

The key structural point is that the two sums are evaluated separately.
Their equality is not assumed to transfer a known value from one to the other.

## Points to inspect closely

| Point | What the argument must retain |
|---|---|
| Finite invariant | Separate treatment of the coefficients at degrees p and 2p |
| Singular roots | The half-degree bound modulo p and the derivative-unit hypothesis |
| Full truncation | All coefficients through p−1 remain present modulo p² |
| Modular certificates | Holomorphy at every cusp before using the valence bound |
| Hecke coefficients | Integral descent and a geometric degree bound for arbitrary p |
| Degree p | The endpoint g_p ≡ g_1; a prefix only through p−1 is insufficient |
| CM matrices | Both 3\|x and 3\|y, including determinant 2 and character −1 |
| Embeddings | Separate unit embeddings when the two exhibited roots are conjugate |
| Exceptional primes | Autonomous calculations at 3 and 5 |

## Computational pass

Run `python -B scripts/verify.py --expected evidence` and the unit tests in
[REPRODUCE](../REPRODUCE.md). Read eta_certificates.json for the finite
modular certificates and hecke_polynomials.json for the exact small-prime
reconstructions. The latter check normalisations; the general degree argument
is in the paper. Optional symbolic checks test explicitly listed identities,
not the complete theorem or every algebraic sentence in the manuscript.

The companion can reveal arithmetic or transcription errors. A successful
run cannot replace reading the proof, establish novelty or confer peer review.
