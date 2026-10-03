"""Create a deterministic source ZIP from a verified delivered manifest."""
from pathlib import Path
import argparse
import hashlib
import re
import zipfile

from check_manifest import ROOT, MANIFEST, read_manifest, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="destination ZIP outside the repository")
    args = parser.parse_args()
    out = args.output.resolve()
    if out.is_relative_to(ROOT):
        raise ValueError("Archive output must be outside the repository")
    if out.exists():
        raise ValueError("Output exists; choose a new path")
    verify()
    frozen_manifest = (ROOT / MANIFEST).read_bytes()
    expected = read_manifest(ROOT / MANIFEST)
    payloads = {}
    for name, expected_digest in expected.items():
        data = (ROOT / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected_digest:
            raise ValueError("Source changed during archiving: " + name)
        payloads[name] = data
    if (ROOT / MANIFEST).read_bytes() != frozen_manifest:
        raise ValueError("Manifest changed during archiving")
    # The parser read and frozen raw manifest must describe exactly the same bytes.
    canonical_manifest = "".join(h + "  " + name + "\n" for name, h in expected.items()).encode("utf-8")
    if frozen_manifest != canonical_manifest:
        raise ValueError("Manifest is not canonical; deliberately regenerate it before archiving")
    payloads[MANIFEST] = frozen_manifest
    version = payloads["VERSION"].decode("utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("VERSION must have three decimal components for a safe archive prefix")
    prefix = "Sun-3-6-Supercongruence-" + version
    print("Archive directory: " + str(out.parent))
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "x", compression=zipfile.ZIP_STORED) as z:
        for name in sorted(payloads):
            info = zipfile.ZipInfo(prefix + "/" + name, date_time=(2026, 10, 3, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, payloads[name])
    print("ARCHIVE_PASS " + hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
