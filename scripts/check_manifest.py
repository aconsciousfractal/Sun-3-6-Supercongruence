"""Verify exact package/evidence inventories; --write explicitly refreshes them."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "MANIFEST_SHA256.txt"
EVIDENCE = "EVIDENCE_SHA256.txt"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root=ROOT, evidence=False):
    result = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if rel.parts[0] == ".git":
            continue
        if {"__pycache__", ".pytest_cache", ".venv"} & set(rel.parts):
            continue
        if rel.parts[:2] == ("paper", "build") or p.suffix in {".pyc", ".pyo"}:
            continue
        if p.is_symlink() or getattr(p.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError("Links/reparse points are not package members: " + rel.as_posix())
        if not p.is_file() or rel.as_posix() == MANIFEST:
            continue
        if evidence:
            selected = (
                rel.parts[0] in {"companion", "tests"} and p.suffix == ".py"
                or rel.parts[0] == "evidence" and p.suffix == ".json"
                or rel.as_posix() in {
                    "scripts/verify.py", "scripts/check_manifest.py", "VERSION",
                    ".gitattributes", ".github/workflows/verify.yml",
                    "requirements.txt", "requirements-symbolic.txt"
                }
            )
            if not selected:
                continue
        result[rel.as_posix()] = digest(p)
    return result


def read_manifest(path):
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        h, sep, name = line.partition("  ")
        rel = PurePosixPath(name)
        if (not sep or not re.fullmatch(r"[0-9a-f]{64}", h)
                or not name or "\\" in name or ":" in name or rel.is_absolute()
                or any(part in {"", ".", ".."} for part in name.split("/"))
                or name != rel.as_posix()):
            raise ValueError("Invalid manifest entry")
        if name in result:
            raise ValueError("Duplicate manifest member: " + name)
        result[name] = h
    if not result:
        raise ValueError("Empty manifest")
    return result


def verify(root=ROOT, evidence=False):
    expected = read_manifest(root / (EVIDENCE if evidence else MANIFEST))
    actual = inventory(root, evidence)
    if actual != expected:
        changed = sorted(n for n in expected.keys() | actual.keys()
                         if expected.get(n) != actual.get(n))
        raise ValueError("Inventory/hash mismatch: " + ", ".join(changed))
    return len(actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", action="store_true",
                        help="verify code, tests and exact evidence, excluding paper/prose")
    parser.add_argument("--write", action="store_true",
                        help="authoring operation: refresh instead of verify")
    args = parser.parse_args()
    filename = EVIDENCE if args.evidence else MANIFEST
    if args.write:
        rows = inventory(ROOT, args.evidence)
        if not rows:
            raise ValueError("Cannot write an empty manifest")
        (ROOT / filename).write_text(
            "".join(h + "  " + name + "\n" for name, h in rows.items()),
            encoding="utf-8", newline="\n")
        print(filename + " WRITTEN: " + str(len(rows)) + " files")
    else:
        print(filename + " PASS: " + str(verify(ROOT, args.evidence)) + " files")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print("MANIFEST_FAIL: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
