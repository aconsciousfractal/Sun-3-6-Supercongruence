# Manuscript build

The delivered manuscript has 18 A4 pages, 10 main sections and 3 appendices.
Its source is a standalone LaTeX file; no additional project files, external
figures or bibliography processor are required.

From the repository root, use an existing pdfLaTeX installation:

```console
python -B scripts/build_pdf.py
```

The script uses three passes, disables shell escape and MiKTeX automatic
installation, and fails on unresolved compilation, reference, overfull or
underfull warnings. A successful run writes `paper/build/build_info.json`.
The delivered PDF changes only with the explicit `--update` option.
The build directory is excluded from the package inventory.

The supplied PDF was built with **MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)**,
pdfTeX 1.40.28. All three passes completed; the final log contains zero
warnings. `SOURCE_DATE_EPOCH=1790985600`, `FORCE_SOURCE_DATE=1` and `TZ=UTC`
are fixed by the build script. The source suppresses PDF date fields and
the trailer identifier.

| Artifact | SHA-256 |
|---|---|
| `Sun_3_6_Supercongruence.tex` | `479cc6c0164ee13b4422d2256e6f44d7ace0e1c0c5bf93f9069a08383c9117d8` |
| `Sun_3_6_Supercongruence.pdf` | `1ff111e26cefb5053f66ef5195f28a91ec9e9ecc824754287c469b1219327b5a` |
| `../EVIDENCE_SHA256.txt` | `47f214dfbf8133220e57c1a67ade26d09c0343fe17df719e38ad98c26a86f1c8` |

The manuscript uses plain page numbers: no table of contents, running title,
running author name, or author identifier beneath the name. Fonts are embedded.

Identical PDF bytes require the same engine, fonts and package versions;
another TeX distribution can produce an equivalent document with different
bytes. The full package inventory binds the supplied source and PDF, while
the evidence inventory binds the computational subset quoted by the paper.
Neither digest is an authenticity signature or a proof certificate by itself.
