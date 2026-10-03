"""Deterministic evidence I/O and strict semantic equality after independent calculation."""
import json
from pathlib import Path
from .arithmetic import require

CORE_FILES = ('prime_regression.json', 'invariant_certificates.json',
              'eta_certificates.json', 'endpoint_certificate.json',
              'hecke_polynomials.json', 'verification_summary.json')
SYMBOLIC_FILES = ('symbolic_identities.json', 'structure_certificates.json')


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'nonfinite JSON constant: {value}')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=reject_duplicates, parse_constant=reject_constant)


def write_json(path, data):
    with Path(path).open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(data, sort_keys=True, indent=2, allow_nan=False)+'\n')


def compare_expected(actual_directory, expected_directory, symbolic=False):
    """Check a fixed inventory and every JSON member, type and value.

    Expected data never enter a mathematical calculation. Canonical JSON
    equality distinguishes integers, floats and booleans, including schema_version.
    """
    actual_directory, expected_directory = Path(actual_directory), Path(expected_directory)
    require(actual_directory.resolve() != expected_directory.resolve(),
            'generated and expected evidence must be distinct')
    require(expected_directory.is_dir(), 'expected evidence directory is missing')
    names = set(CORE_FILES) | (set(SYMBOLIC_FILES) if symbolic else set())
    require({p.name for p in actual_directory.iterdir()} == names,
            'generated evidence inventory differs from fixed schema')
    require({p.name for p in expected_directory.iterdir()} == names,
            'expected evidence inventory differs from fixed schema')
    for name in sorted(names):
        require((actual_directory/name).is_file() and (expected_directory/name).is_file(),
                f'evidence member is not a file: {name}')
        actual, expected = read_json(actual_directory/name), read_json(expected_directory/name)
        for data in (actual, expected):
            require(type(data) is dict and type(data.get('schema_version')) is int and
                    data['schema_version'] == 1 and data.get('status') == 'PASS',
                    f'invalid evidence root: {name}')
        require(json.dumps(actual, sort_keys=True, allow_nan=False) ==
                json.dumps(expected, sort_keys=True, allow_nan=False),
                f'evidence mismatch: {name}')
