"""Distribution corruption checks, independent of scientific regression output."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "check_manifest.py"
SPEC = importlib.util.spec_from_file_location("manifest_under_test", SOURCE)
manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manifest)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sun36-manifest-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "README.md").write_text("Reader package\n", encoding="utf-8")
        (self.root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
        self.freeze()

    def freeze(self, evidence=False):
        name = manifest.EVIDENCE if evidence else manifest.MANIFEST
        data = manifest.inventory(self.root, evidence)
        (self.root / name).write_text(
            "".join(h + "  " + n + "\n" for n, h in data.items()), encoding="utf-8")

    def test_full_inventory_rejects_changed_missing_and_extra_members(self):
        self.assertEqual(manifest.verify(self.root), 2)
        path = self.root / "README.md"
        original = path.read_bytes()
        path.write_bytes(original + b"modified")
        with self.assertRaises(ValueError):
            manifest.verify(self.root)
        path.unlink()
        with self.assertRaises(ValueError):
            manifest.verify(self.root)
        path.write_bytes(original)
        (self.root / "unexpected.txt").write_text("extra", encoding="utf-8")
        with self.assertRaises(ValueError):
            manifest.verify(self.root)

    def test_evidence_identity_has_declared_scope(self):
        self.freeze(evidence=True)
        self.assertEqual(manifest.verify(self.root, evidence=True), 1)
        (self.root / "README.md").write_text("Editorial change", encoding="utf-8")
        self.assertEqual(manifest.verify(self.root, evidence=True), 1)
        (self.root / "VERSION").write_text("0.1.1", encoding="utf-8")
        with self.assertRaises(ValueError):
            manifest.verify(self.root, evidence=True)

    def test_reader_rejects_malformed_duplicate_and_unsafe_names(self):
        path = self.root / manifest.MANIFEST
        sha = "a" * 64
        invalid = ["", sha + "  README.md\n" + sha + "  README.md\n",
                   "not-a-digest  README.md\n"]
        invalid += [sha + "  " + name + "\n" for name in
                    ["../x", "/x", "C:/x", "a\\x", "a//x", "./x", "a/../x", ""]]
        for data in invalid:
            with self.subTest(data=data):
                path.write_text(data, encoding="utf-8")
                with self.assertRaises(ValueError):
                    manifest.read_manifest(path)


if __name__ == "__main__":
    unittest.main()
