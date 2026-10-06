# Reproduction

Run commands from the repository root. Core verification requires Python
3.10 or later and the standard library, with no network access. The paper PDF
is included; compiling it is separate from running the companion.

## Exact companion

```text
python -B scripts/verify.py --expected evidence
python -B -O scripts/verify.py --expected evidence
python -B -m unittest discover -s tests -v
python -B -O -m unittest discover -s tests -v
python -B scripts/check_manifest.py
python -B scripts/check_manifest.py --evidence
```

The default prime window is every odd prime from 3 through 1999. Local
polynomial and lifting checks use the smaller bound declared in their output;
modular certificates and exact Hecke polynomials use their own stated
precisions. These finite scopes are not proofs for arbitrary primes.

The six core JSON files are recomputed, then compared with evidence/.
Expected data never supplies a coefficient to a constructor. Missing, extra,
changed or malformed expected records fail the comparison. A different
`--bound` changes the regression output and should not be compared with the
default delivered evidence.

The verifier uses temporary output unless `--out PATH` is supplied. Explicit
output must be new or empty. It does not update the delivered evidence or
inventories; with `--expected`, output must also lie outside that directory.
See [companion documentation](companion/README.md) and the
[evidence guide](docs/EVIDENCE.md).

## Optional symbolic identities

With the optional dependency installed in the environment you intend to use:

```text
python -m pip install -r requirements-symbolic.txt
python -B scripts/verify.py --symbolic
python -B -O scripts/verify.py --symbolic
```

These commands explicitly request the SymPy checks and fail if SymPy is
unavailable. A core PASS does not assert that symbolic checks were run.
Symbolic mode produces two additional JSON files alongside the six core
outputs. The delivered evidence/ contains only the six core files, so do not
combine `--symbolic` with `--expected evidence`.

## Paper

Use an existing pdflatex installation with the packages declared in the TeX
preamble. The build script does not install TeX or packages. It disables
shell escape and automatic MiKTeX package installation.

```text
python -B scripts/build_pdf.py
```

This writes the rebuilt PDF and build_info.json into ignored paper/build/;
it leaves the delivered PDF unchanged. The explicit authoring option
`--update` replaces the delivered PDF after a successful build. A deliberate
paper update also requires refreshing the full distribution inventory.

The source suppresses volatile PDF dates and IDs; the builder fixes
SOURCE_DATE_EPOCH and performs three passes. Identical bytes are expected
with the recorded engine, package versions and fonts, not across all TeX
installations. See [manuscript build](paper/BUILD.md).

## Inventories and source archive

EVIDENCE_SHA256.txt covers the exact computational evidence, companion and
verification code, tests and declared verification configuration. Its digest
is printed in the paper. Paper and explanatory prose are excluded from that
identity to avoid a circular hash reference. MANIFEST_SHA256.txt covers the
complete distribution except itself. Neither inventory is a signature.

Normal verification never rewrites inventories. After deliberate edits,
`python -B scripts/check_manifest.py --write --evidence` and
`python -B scripts/check_manifest.py --write` are explicit authoring commands;
update the paper's evidence digest before rebuilding when the core changes.

```text
python -B scripts/make_archive.py --output <existing-output-directory>/Sun-3-6-Supercongruence-0.1.1.zip
```

Replace the placeholder with an existing writable directory outside the
repository and quote the whole path if it contains spaces. The destination
must not already exist. The archive contains only verified inventory members
with deterministic entry metadata and excludes Git state, caches and builds.
An extracted copy supports the same verification commands without Git.

Hosted CI is configured for the core checks. Its presence does not establish
that a hosted run has occurred.
