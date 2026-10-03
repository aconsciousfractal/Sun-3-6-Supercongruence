# Evidence roles and scope

The all-prime result is a written proof with explicitly attributed imports.
The companion supplies exact calculations with the distinct roles below.

| Delivered core file | Role | What it does not establish |
|---|---|---|
| prime_regression.json | Original sequence, recurrence, both sums and CM matrices in a declared finite prime window | An all-prime theorem from sampling |
| invariant_certificates.json | Finite invariant/resonance coefficients and local lifting/defect diagnostics | The generic multiplicity and lifting arguments |
| eta_certificates.json | Exact eta data, cusp constants and modular coefficient certificates | Holomorphy or modularity merely from matching a prefix |
| endpoint_certificate.json | Individual coefficient and constant-term checks | The endpoint for all primes without its source theorem or multinomial argument |
| hecke_polynomials.json | Exact reconstructions at p=5,7,11,17,19 and CM factors where applicable | The generic Hecke orbit, integral descent or degree bound |
| verification_summary.json | Counts, parameters and outcomes of the preceding calculations | A separate proof or an additional independent experiment |

The two weight-eight identities use the coefficients of q^0 through q^8.
Together with their proved membership in the relevant space of holomorphic
modular forms and the valence bound, these finite coefficient certificates
are sufficient for the identities. The proof separately justifies those
hypotheses. The weight-two identity has its own corresponding bound.

The Hecke constructors do not take the target CM roots or stored evidence as
input. Exact factors are tested only after reconstruction. Expected output
comparison is an additional operation after all calculations.

## Optional identities

Explicit `--symbolic` mode generates symbolic_identities.json and
structure_certificates.json in addition to the core output. These two files
are not members of the delivered evidence/ directory. Their generating code
is included in the computational inventory. See companion/README.md for the
identity families actually checked; no claim is made that all paper proofs
are mechanically verified.

## Identity

The SHA-256 of EVIDENCE_SHA256.txt is printed in the manuscript. That inventory
pins code, tests, configuration and the six delivered exact JSON outputs.
It excludes paper and prose that cite the digest. The full distribution is
covered separately by MANIFEST_SHA256.txt.

Reproduction compares JSON content with strict types; normal and optimised
executions must agree. A cryptographic digest establishes byte identity,
not mathematical truth, originality or independent specialist acceptance.
