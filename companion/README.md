# Exact companion

The core uses Python 3.10 or newer and the standard library. It constructs
integer coefficients from definitions and recurrence relations, and uses exact
rational arithmetic for cusp phases and CM matrices. Frozen evidence is read
only after those calculations finish.

From the repository root:

```console
python -B scripts/verify.py --expected evidence
python -B -O scripts/verify.py --expected evidence
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
```

Without `--out`, the replay uses a temporary directory which is removed on exit.
`--out DIR` retains a replay in a new or empty directory and refuses to overwrite
existing files. `--bound N` changes the inclusive prime bound (minimum 19);
comparison against the supplied evidence requires the default bound 1999.
Expected evidence must contain precisely the six core files below. Duplicate
keys, nonfinite JSON values, missing or extra files, changed members, and changed
types or values fail. Differences in JSON whitespace are allowed.

| Module | Calculation | Core output |
|---|---|---|
| `arithmetic`, `primes` | Original Franel transform through degree 198; recurrence through degree 1999; both sums, endpoint congruences, exceptional primes and exact CM matrices | `prime_regression.json` |
| `invariant` | Full invariant and both resonant coefficients; all ordinary and singular lifts for primes 5–199; singular defect formula; autonomous p=5 and negative p³ control | `invariant_certificates.json` |
| `eta`, `cusps` | Independent product/logarithmic derivative engines; period coefficients; Newman and cusp data; exact Dedekind phases; weight 2 and weight 8 coefficient certificates | `eta_certificates.json` |
| `endpoint` | Laurent constant terms through degree 25 and the 18 pure-row configurations with signed sum 6 | `endpoint_certificate.json` |
| `hecke`, `eta` | Independent Fourier and eta reconstructions for p=5,7,11,17,19; integral coefficients, degree bounds, finite polynomial relation and six exact CM factors | `hecke_polynomials.json` |
| `scripts/verify.py` | Explicit bounds and aggregate counts | `verification_summary.json` |

Each core output has `schema_version: 1` and `status: "PASS"`. The nested
coefficient arrays, matrix entries, root data and regression rows are retained
to make the checks inspectable. In a Hecke polynomial the array with index m
contains the ascending coefficients in t of C_m(t), the coefficient of X^m.
The fixed polynomial array length is p+2, and the coefficient-array length is
floor(m/2)+1, including trailing zeros.

Optional symbolic checks require the pinned package in
`requirements-symbolic.txt`. They are explicitly requested:

```console
python -B scripts/verify.py --symbolic --out symbolic-replay
```

The symbolic run adds `symbolic_identities.json` (24 exact identities) and
`structure_certificates.json` (15 structural identities, plus normalizer
permutations and squarefree decompositions for primes 5–199). It fails if
SymPy 1.14.0 is unavailable. To compare two symbolic runs, use a separately
generated expected directory containing all eight files; the supplied core
`evidence` directory is intended for the standard-library replay.

The universal arguments are in the manuscript. Finite prime checks do not prove
the theorem, and bounded Hecke reconstructions do not prove generic degree or
integrality statements. The coefficient certificates use the modularity,
holomorphy and coefficient bounds established in the manuscript. The checks
also retain the precision boundary: at p=7 the two sums have residues 294 and
49 modulo 343, so their equality modulo p² does not extend to p³.
