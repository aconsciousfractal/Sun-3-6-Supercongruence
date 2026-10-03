"""Definition-based ordinary and singular lift checks, including the full defect identity."""
from __future__ import annotations

from fractions import Fraction
from math import comb,isqrt

from .arithmetic import require, natural, original, invariant

def primes(n: int) -> list[int]:
    return [p for p in range(5,n+1) if all(p%d for d in range(2,isqrt(p)+1))]

def evaluate(a: list[int], x: int, mod: int) -> int:
    v=0
    for c in reversed(a): v=(v*x+c)%mod
    return v

def fracmod(x: Fraction, mod: int) -> int:
    return x.numerator*pow(x.denominator,-1,mod)%mod


def validate_invariant(g,p):
    from .arithmetic import prime, qseq
    prime(p,5)
    require(len(g)==p and all(type(x) is int for x in g), 'full exact invariant window required')
    require(g[0]==1 and g[1]==-12, 'invariant normalization')
    q=qseq(p); gp=comb(2*p,p)*q[p]
    result=invariant(g)
    require(all(v%(p*p)==0 for v in result),'complete invariant')
    require(result[p]==-2*p*p*gp,'exact resonant p coefficient')
    require(result[2*p]==4*72*(2*p-1)*(2*p+1)*g[p-1]**2,'exact resonant 2p coefficient')
    return result

def certificates(bound=199):
    natural(bound,'local bound',19)
    if bound>499:raise ValueError('local bound must be <=499')
    ps=primes(bound); require(bool(ps),'empty prime range')
    _,q=original(bound-1)
    for n in range(1,len(q)-1):
        require((n+1)**2*q[n+1]+(17*n*(n+1)+6)*q[n]+72*n*n*q[n-1]==0,f'recurrence n={n}')
    counts=dict(primes=len(ps),definition_values=len(q),ordinary_roots=0,singular_roots=0,
                ordinary_lifts=0,singular_lifts=0,defect_equalities=0,branch_evaluations=0)
    data=[]; specials=[]; resonances=[]
    for p in ps:
        m=p*p; exact=[comb(2*n,n)*q[n] for n in range(p)]
        coeff=[value%m for value in exact]
        validate_invariant(exact,p)
        resonances.append(dict(p=p,coefficient_count=len(invariant(exact)),
                              degree_mod_p=max(i for i,c in enumerate(coeff) if c%p)))
        dcoeff=[n*coeff[n] for n in range(1,p)]
        d2coeff=[n*(n-1)*coeff[n] for n in range(2,p)]
        require(all(c%p==0 for c in coeff[(p+1)//2:]),f'half degree p={p}')
        roots=[]
        for r in range(1,p):
            if evaluate(coeff,r,p): continue
            Dr=(1+68*r+1152*r*r)%p
            slope=evaluate(dcoeff,r,p)
            if Dr:
                require(slope==0 and evaluate(d2coeff,r,p)!=0,f'ordinary multiplicity p={p},r={r}')
                counts['ordinary_roots']+=1; lifted=[]
                for s in range(p):
                    x=r+p*s; v=evaluate(coeff,x,m)
                    require(v==0,f'ordinary disc p={p},x={x}')
                    counts['ordinary_lifts']+=1; lifted.append(x)
                roots.append(dict(residue=r,kind='ordinary_double',lift_count=len(lifted)))
            else:
                require(slope!=0,f'singular simplicity p={p},r={r}')
                counts['singular_roots']+=1; lifted=[]
                for s in range(p):
                    x=r+p*s; D=1+68*x+1152*x*x; D1=68+2304*x
                    v=evaluate(coeff,x,m); vp=evaluate(dcoeff,x,m)
                    require(D1%p!=0,'simple discriminant root')
                    rhs=D*vp*pow(D1,-1,m)%m
                    require(v==rhs,f'local defect p={p},x={x}: {v} != {rhs}')
                    require((v==0)==(D%m==0),f'iff p={p},x={x}')
                    counts['singular_lifts']+=1;counts['defect_equalities']+=1
                    if v==0: lifted.append(x)
                require(len(lifted)==1,f'unique singular lift p={p},r={r}')
                roots.append(dict(residue=r,kind='singular_simple',lift_count=1,lift=lifted[0],slope_mod_p=slope))
        # Original branch values from the exact definitions, never used above as an oracle for roots.
        rep=None
        if p%8 in (1,3):
            for y in range(1,isqrt(p//2)+1):
                x=isqrt(p-2*y*y)
                if x*x+2*y*y==p: rep=(x,y);break
            require(rep is not None,'missing split representation')
        expected=(4*rep[0]**2-2*p)%m if rep else 0
        vals=[]
        for t in [Fraction(-1,32),Fraction(1,64)]:
            v=evaluate(coeff,fracmod(t,m),m);require(v==expected,f'target regression {p}')
            vals.append(v);counts['branch_evaluations']+=1
        data.append(dict(p=p,roots=roots,original_values=vals))
        if p in (5,7,11,19):
            for t in [Fraction(-1,32),Fraction(-1,36),Fraction(1,64)]:
                x=fracmod(t,m)
                specials.append(dict(p=p,t=str(t),t_residue=x,U=evaluate(coeff,x,m),
                    D=fracmod(1+68*t+1152*t*t,m),Uprime_mod_p=evaluate(dcoeff,x,p),
                    shifted_value=evaluate(coeff,(x+p)%m,m)))
    # No scalar multiple of a recurrence solution can be silently replaced by the all-zero polynomial.
    require(q[0]==1 and q[1]==-6,'nonvacuity')
    # Exact rational exceptional-prime bridge: 1/64 is already the correct 5-adic singular lift.
    require(Fraction(1,64)+Fraction(1,36)==Fraction(25,576),'p5 exact rational difference')
    require(Fraction(75,32).numerator%25==0,'p5 D divisibility')
    # A bounded counterexample excludes an unjustified promotion from p^2 to p^3.
    p3=7; mm=p3**3
    high=[sum(comb(2*n,n)*q[n]*pow(den,-n,mm) for n in range(p3))%mm for den in (-32,64)]
    require(high==[294,49], 'p7 modulo p3 witness')
    return dict(schema_version=1,status='PASS',bound_inclusive=bound,counts=counts,
                invariant_polynomials=len(resonances),resonant_integer_equalities=2*len(resonances),
                resonances=resonances,rows=data,specials=specials,
                exceptional_p5=dict(polynomial_mod5=[c%5 for c in [comb(2*n,n)*q[n] for n in range(5)]],
                    rational_difference='25/576',discriminant_at_plus64='75/32'),
                negative_mod_p3=dict(p=7,modulus=343,values=high,difference=(high[0]-high[1])%343))
