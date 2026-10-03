"""Adverse checks of scientific boundaries, exact arithmetic and frozen evidence I/O."""
import copy
import hashlib
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from companion.arithmetic import (original,qseq,invariant,matrix_rows,validate_cm_row,
                                  validate_endpoint,natural)
from companion import eta, hecke
from companion.invariant import certificates,validate_invariant
from companion.primes import regression
from companion.evidence import CORE_FILES,compare_expected,write_json


class ScientificBoundaryTests(unittest.TestCase):
    def test_original_definition_and_exceptional_primes(self):
        _,q=original(25)
        self.assertEqual(q,qseq(25))
        result=regression(19)
        self.assertEqual([(r['p'],r['value']) for r in result['exceptional_primes']],[(3,7),(5,0)])
        self.assertEqual({r['p']:r['target'] for r in result['rows']}[11],14)
        local=certificates(19)
        self.assertEqual(local['exceptional_p5']['polynomial_mod5'],[1,3,2,0,0])
        self.assertEqual(local['negative_mod_p3']['values'],[294,49])
        singular=[r for r in local['specials'] if r['p']==7 and r['t']=='-1/32'][0]
        self.assertEqual(singular['U'],0)
        self.assertNotEqual(singular['shifted_value'],0)
        ordinary=[r for r in local['specials'] if r['p']==7 and r['t']=='1/64'][0]
        self.assertEqual(ordinary['shifted_value'],0)

    def test_degree_p_endpoint_cannot_be_dropped(self):
        p=11;q=qseq(p);g=comb(2*p,p)*q[p]
        validate_endpoint(p,q[p],g)
        for qp,gp in ((q[p]+p,g),(q[p],g+p),(True,g),(q[p],float(g))):
            with self.subTest(qp=qp),self.assertRaises(ArithmeticError):validate_endpoint(p,qp,gp)
        coeff=[comb(2*n,n)*q[n] for n in range(p)]
        validate_invariant(coeff,p)
        for index in (1,5,10):
            bad=coeff[:];bad[index]+=1
            with self.subTest(index=index),self.assertRaises(ArithmeticError):validate_invariant(bad,p)
        for bad in ([],coeff[:-1],[0]*p):
            with self.assertRaises(ArithmeticError):validate_invariant(bad,p)

    def test_both_CM_classes_reject_wrong_character_and_matrix(self):
        for p,x,y in ((11,3,1),(19,1,3)):
            for row in matrix_rows(p,x,y):
                validate_cm_row(row,p,x,y)
                wrong=copy.deepcopy(row);wrong['character']*=-1
                with self.subTest(p=p,point=row['point']),self.assertRaises(ArithmeticError):
                    validate_cm_row(wrong,p,x,y)
                wrong=copy.deepcopy(row);wrong['M'][0]+=1
                with self.assertRaises(ArithmeticError):validate_cm_row(wrong,p,x,y)
                wrong=copy.deepcopy(row);wrong['z_rational']*=-1
                with self.assertRaises(ArithmeticError):validate_cm_row(wrong,p,x,y)
        with self.assertRaises(ArithmeticError):matrix_rows(11,1,1)
        with self.assertRaises(ValueError):matrix_rows(15,1,1)

    def test_period_corruption_and_empty_window_fail(self):
        cert=eta.certificates();series=cert['q_series'];N=cert['series_through']
        g=[comb(2*n,n)*v for n,v in enumerate(qseq(N))]
        eta.validate_period(g,series['t'],series['theta'])
        for index in (1,18,30):
            bad=g[:];bad[index]+=1
            with self.subTest(index=index),self.assertRaises(ArithmeticError):
                eta.validate_period(bad,series['t'],series['theta'])
        for length in (0,8,18):
            with self.assertRaises(ArithmeticError):
                eta.validate_period(g[:length],series['t'][:length],series['theta'][:length])
        for exps in ({},{1:1},{1:-24},{1:1.0},{0:24}):
            with self.subTest(exps=exps),self.assertRaises(ArithmeticError):eta.eta(exps,10)
        with self.assertRaises(ValueError):eta.eta({1:24},10,'unknown')

    def test_exact_Hecke_factor_rejects_corruption_invisible_mod_p2(self):
        p=11;polys=hecke.build(p)['coefficients_in_t']
        hecke.validate_polynomial(polys,p)
        changes=[(0,0,1),(1,0,p*p),(p,0,p*p),(p+1,0,p*p)]
        for k,j,delta in changes:
            bad=copy.deepcopy(polys);bad[k][j]+=delta
            with self.subTest(k=k),self.assertRaises(ArithmeticError):hecke.validate_polynomial(bad,p)
        for bad in ([],polys[:-1]):
            with self.assertRaises(ArithmeticError):hecke.validate_polynomial(bad,p)
        with self.assertRaises(ValueError):hecke.build(9)

    def test_integer_and_nonempty_bounds(self):
        for value in (True,19.0,-1,0,18):
            with self.subTest(value=value),self.assertRaises(ValueError):regression(value)
        for value in (True,3.0,-1):
            with self.assertRaises(ValueError):qseq(value)
        with self.assertRaises(ArithmeticError):invariant([])
        with self.assertRaises(ArithmeticError):invariant([1.0,-12.0])


class FrozenEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='sun36-tests-')
        base=Path(self.temp.name);self.actual=base/'actual';self.expected=base/'expected'
        self.actual.mkdir();self.expected.mkdir()
        self.data=dict(schema_version=1,status='PASS',nested={'value':1},rows=[1,False])
        for name in CORE_FILES:
            for directory in (self.actual,self.expected):write_json(directory/name,self.data)

    def tearDown(self):self.temp.cleanup()

    def test_whitespace_allowed_every_member_type_and_value_checked(self):
        path=self.expected/CORE_FILES[0]
        path.write_text(json.dumps(self.data,separators=(',',':')),encoding='utf-8')
        compare_expected(self.actual,self.expected)
        for changed in (dict(self.data,schema_version=True),dict(self.data,schema_version=1.0),
                        dict(self.data,extra=1),dict(self.data,nested={'value':True}),
                        dict(self.data,nested={'value':1.0}),dict(self.data,rows=[1,0]),
                        dict(self.data,rows=[1,False,2])):
            write_json(path,changed)
            with self.subTest(changed=changed),self.assertRaises(ArithmeticError):
                compare_expected(self.actual,self.expected)

    def test_inventory_missing_extra_directory_and_empty_fail(self):
        with self.assertRaises(ArithmeticError):compare_expected(self.actual,self.actual)
        path=self.expected/CORE_FILES[0];path.unlink()
        with self.assertRaises(ArithmeticError):compare_expected(self.actual,self.expected)
        path.mkdir()
        with self.assertRaises(ArithmeticError):compare_expected(self.actual,self.expected)
        path.rmdir();write_json(path,self.data)
        write_json(self.expected/'extra.json',self.data)
        with self.assertRaises(ArithmeticError):compare_expected(self.actual,self.expected)
        empty=self.expected.parent/'empty';empty.mkdir()
        with self.assertRaises(ArithmeticError):compare_expected(self.actual,empty)

    def test_invalid_JSON_and_duplicate_keys_fail(self):
        for text in ('{}','{"status":"PASS","status":"FAIL"}',
                     '{"value":NaN}','{"value":Infinity}','[]'):
            (self.expected/CORE_FILES[0]).write_text(text,encoding='utf-8')
            with self.subTest(text=text),self.assertRaises((ValueError,ArithmeticError)):
                compare_expected(self.actual,self.expected)

    def test_comparison_preserves_frozen_input_on_failure(self):
        path=self.expected/CORE_FILES[0];write_json(path,dict(self.data,nested={'value':7}))
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.expected.iterdir()}
        with self.assertRaises(ArithmeticError):compare_expected(self.actual,self.expected)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.expected.iterdir()}
        self.assertEqual(before,after)

    def test_CLI_refuses_overwrite_and_symbolic_missing_dependency(self):
        empty_child=self.expected/'empty';empty_child.mkdir()
        commands=[['-B','scripts/verify.py','--bound','19','--out',str(self.expected)],
                  ['-B','scripts/verify.py','--bound','19','--out',str(self.expected/'new'),
                   '--expected',str(self.expected)],
                  ['-B','scripts/verify.py','--bound','19','--out',str(empty_child),
                   '--expected',str(self.expected)],
                  ['-B','scripts/verify.py','--bound','18'],
                  ['-S','-B','scripts/verify.py','--bound','19','--symbolic']]
        snapshot=lambda: {p.relative_to(self.expected).as_posix():
                          p.read_bytes() if p.is_file() else None
                          for p in self.expected.rglob('*')}
        before=snapshot()
        for command in commands:
            result=subprocess.run([sys.executable,*command],cwd=ROOT,capture_output=True,text=True)
            with self.subTest(command=command):
                self.assertNotEqual(result.returncode,0)
                self.assertIn('SUN36_REPLAY_FAIL:',result.stderr)
        self.assertIn('requires requirements-symbolic.txt',result.stderr)
        self.assertEqual(before,snapshot())


if __name__=='__main__':unittest.main()
