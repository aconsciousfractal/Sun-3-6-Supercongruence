"""Replay exact certificates and bounded regressions independently of frozen evidence."""
import argparse
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))

from companion.arithmetic import natural
from companion.evidence import CORE_FILES, SYMBOLIC_FILES, compare_expected, write_json
from companion import primes, invariant, eta, endpoint, hecke


def run(directory, bound=1999, symbolic=False):
    natural(bound, 'prime bound', 19)
    local_bound = min(bound, 199)
    results = [primes.regression(bound), invariant.certificates(local_bound),
               eta.certificates(), endpoint.certificates(), hecke.certificates()]
    for name, data in zip(CORE_FILES[:5], results):
        write_json(directory/name, data)
    symbolic_counts = None
    if symbolic:
        try:
            import sympy
            from companion import symbolic as algebra, structure
        except ImportError as exc:
            raise RuntimeError('Explicit --symbolic requires requirements-symbolic.txt') from exc
        if sympy.__version__ != '1.14.0':
            raise RuntimeError('Explicit --symbolic requires SymPy 1.14.0')
        symbolic_results = [algebra.certificates(), structure.certificates()]
        for name, data in zip(SYMBOLIC_FILES, symbolic_results):
            write_json(directory/name, data)
        symbolic_counts = dict(algebra_identities=symbolic_results[0]['exact_identities'],
                               structure_identities=symbolic_results[1]['symbolic_identities'])
    summary = dict(schema_version=1, status='PASS',
                   scope='exact finite certificates and bounded regressions',
                   bound_inclusive=bound, prime_count=results[0]['prime_count'],
                   original_definition_values=results[0]['original_definition_values'],
                   original_sum_checks=results[0]['original_sum_checks'],
                   endpoint_checks=results[0]['endpoint_checks'],
                   cm_matrices=len(results[0]['cm_matrices']),
                   invariant_bound_inclusive=local_bound,
                   invariant_polynomials=results[1]['invariant_polynomials'],
                   resonant_integer_equalities=results[1]['resonant_integer_equalities'],
                   local_counts=results[1]['counts'],
                   eta_series_through=results[2]['series_through'],
                   endpoint_CT_checks=len(results[3]['CT_sequence_checks']),
                   hecke_primes=results[4]['primes'],
                   integer_hecke_coefficients=results[4]['integer_coefficients'],
                   exact_CM_factors=results[4]['exact_CM_factors'],
                   symbolic_requested=symbolic, symbolic_counts=symbolic_counts)
    write_json(directory/CORE_FILES[-1], summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bound', type=int, default=1999,
                        help='inclusive prime regression bound (>=19)')
    parser.add_argument('--out', type=Path, help='write evidence to a new or empty directory')
    parser.add_argument('--expected', type=Path, help='strictly compare independent replay with frozen evidence')
    parser.add_argument('--symbolic', action='store_true', help='also run explicit SymPy 1.14.0 checks')
    args = parser.parse_args()
    natural(args.bound, 'prime bound', 19)
    if args.out is not None:
        directory = args.out.resolve()
        if args.expected is not None and directory.is_relative_to(args.expected.resolve()):
            raise ValueError('--out must be outside --expected; frozen evidence is never modified')
        if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
            raise ValueError('--out must be new or empty; existing evidence is never overwritten')
        directory.mkdir(parents=True, exist_ok=True)
        summary = run(directory, args.bound, args.symbolic)
        if args.expected is not None:
            compare_expected(directory, args.expected, args.symbolic)
    else:
        with tempfile.TemporaryDirectory(prefix='sun36-replay-') as scratch:
            directory = Path(scratch)
            summary = run(directory, args.bound, args.symbolic)
            if args.expected is not None:
                compare_expected(directory, args.expected, args.symbolic)
    import json
    print(json.dumps(summary, sort_keys=True, separators=(',', ':')))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ArithmeticError, RuntimeError) as exc:
        print('SUN36_REPLAY_FAIL: '+str(exc), file=sys.stderr)
        raise SystemExit(1)
