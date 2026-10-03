"""Build the standalone manuscript using an existing pdflatex, without installation."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
JOB = "Sun_3_6_Supercongruence"
EPOCH = "1790985600"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=PAPER / "build")
    parser.add_argument("--update", action="store_true",
                        help="explicitly replace the delivered PDF with this build")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out == PAPER.resolve() or out == ROOT.resolve():
        raise ValueError("Use a separate build directory")
    engine = os.environ.get("PDFLATEX") or shutil.which("pdflatex")
    if not engine:
        raise ValueError("An existing pdflatex is required; set PDFLATEX or PATH.")
    print("Build directory: " + str(out), flush=True)
    out.mkdir(parents=True, exist_ok=True)
    (out / "build_info.json").unlink(missing_ok=True)
    version = subprocess.run([engine, "--version"], capture_output=True,
                             text=True, check=True).stdout
    flags = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
             "-no-shell-escape", "-output-directory=" + str(out)]
    if "MiKTeX" in version:
        flags.insert(0, "--disable-installer")
    env = dict(os.environ, SOURCE_DATE_EPOCH=EPOCH, FORCE_SOURCE_DATE="1", TZ="UTC")
    for suffix in (".aux", ".log", ".out", ".toc", ".pdf"):
        (out / (JOB + suffix)).unlink(missing_ok=True)
    for _ in range(3):
        run = subprocess.run([engine, *flags, JOB + ".tex"], cwd=PAPER, env=env,
                             capture_output=True, text=True, errors="replace", timeout=180)
        if run.returncode:
            print(run.stdout[-9000:] + run.stderr[-3000:], file=sys.stderr)
            return run.returncode
    pdf = out / (JOB + ".pdf")
    log = (out / (JOB + ".log")).read_text(encoding="utf-8", errors="replace")
    warnings = [line for line in log.splitlines()
                if "Warning:" in line or "Overfull" in line or "Underfull" in line]
    if warnings:
        print("\n".join(warnings), file=sys.stderr)
        raise ValueError("Build has unresolved warnings; PDF not accepted.")
    info = {"engine": version.splitlines()[0], "source_date_epoch": int(EPOCH),
            "source_sha256": hashlib.sha256((PAPER / (JOB + ".tex")).read_bytes()).hexdigest(),
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "passes": 3, "warnings": warnings}
    (out / "build_info.json").write_text(json.dumps(info, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    if args.update:
        shutil.copyfile(pdf, PAPER / (JOB + ".pdf"))
    print("PDF_BUILD_PASS " + info["pdf_sha256"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print("BUILD_FAIL: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
