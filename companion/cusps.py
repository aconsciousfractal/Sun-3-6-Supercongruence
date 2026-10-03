"""Dedekind transformation phases determine the two real cusp signs exactly."""
from __future__ import annotations
from fractions import Fraction as F
from math import gcd,isqrt



def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ArithmeticError(msg)


def saw(x: F) -> F:
    if x.denominator == 1:
        return F(0)
    return x - (x.numerator // x.denominator) - F(1, 2)


def dedekind(a: int, c: int) -> F:
    return sum((saw(F(k, c)) * saw(F(a*k, c)) for k in range(1, c)), F(0))



def certificates():
    rows = []
    rs = {1: -5, 2: 1, 3: -1, 6: 5}
    for c, target in ((2, F(-1, 9)), (3, F(-1, 8))):
        phase = F(0)
        magnitude_squared = F(1)
        q_order = F(0)
        pieces = []
        for d, r in rs.items():
            g = gcd(c, d)
            a, cp = d//g, c//g
            e = 0 if cp == 1 else pow(a, -1, cp)
            b = (a*e-1)//cp
            require(a*e-b*cp == 1, 'unimodular cusp reduction')
            local_phase = F(a+e, 12*cp) + dedekind(-e, cp) - F(b, 12*a)
            phase += r*local_phase
            magnitude_squared *= F(g, d)**r
            q_order += F(r*g*g, 24*d)
            pieces.append(dict(d=d, exponent=r, a=a, b=b, c_reduced=cp, e=e,
                               phase_over_pi=str(local_phase)))
        require(q_order == 0, 'zero cusp order')
        require(phase == 1, 'negative real cusp phase')
        require(magnitude_squared == target*target, 'cusp absolute value')
        numerator_root=isqrt(magnitude_squared.numerator)
        denominator_root=isqrt(magnitude_squared.denominator)
        require(numerator_root**2==magnitude_squared.numerator and
                denominator_root**2==magnitude_squared.denominator,'rational cusp magnitude')
        value=-F(numerator_root,denominator_root)
        require(value==target,'exact cusp value from magnitude and phase')
        rows.append(dict(cusp=f'1/{c}', factors=pieces, phase_over_pi=str(phase),
                         squared_magnitude=str(magnitude_squared), exact_value=str(value)))
    return dict(source='DLMF 23.18.5-7',constants=2,eta_phase_terms=8,cases=rows)
