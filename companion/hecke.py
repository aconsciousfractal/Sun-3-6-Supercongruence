"""Independent divisor-sum Fourier reconstruction of five exact Hecke polynomials."""
from __future__ import annotations

from fractions import Fraction as F
from math import comb,isqrt


def req(ok,msg):
    if not ok:raise ArithmeticError(msg)

def times(a,b,K):
    out=[0]*(K+1)
    for k in range(K+1):
        out[k]=sum(a[j]*b[k-j] for j in range(max(0,k+1-len(b)),min(k,len(a)-1)+1))
    return out

def plus(a,b,K):return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(K+1)]
def scalar(a,s):return [s*v for v in a]
def derivative(a):return [i*v for i,v in enumerate(a)]
def inverse(a,K):
    req(a[0]==1,'unit-normalized inverse')
    b=[1]
    for i in range(1,K+1): b.append(-sum(a[j]*b[i-j] for j in range(1,min(i+1,len(a)))))
    return b

def sigma6(K):
    # Remove only 2 and 3 from n, then sum all divisors of the residual.
    sig=[0]*(K+1)
    for d in range(1,K+1):
        for n in range(d,K+1,d):sig[n]+=d
    out=[1]
    for n in range(1,K+1):
        k=n
        for l in (2,3):
            while k%l==0:k//=l
        out.append(-12*sig[k])
    return out

def eta_product(exps,K):
    shift=F(sum(d*r for d,r in exps.items()),24)
    req(shift.denominator==1 and 0<=shift<=K,'eta shift')
    shift=int(shift); N=K-shift; out=[1]+[0]*N
    # Apply a single (1-q^k) or its reciprocal at a time; no binomial-factor routine.
    for d,r in exps.items():
        for k in range(d,N+1,d):
            for repeat in range(abs(r)):
                if r>0:
                    for n in range(N,k-1,-1):out[n]-=out[n-k]
                else:
                    for n in range(k,N+1):out[n]+=out[n-k]
    return [0]*shift+out

def eval_poly(c,x):
    s=F(0)
    for a in reversed(c):s=s*x+a
    return s

def remainder_quadratic(c,T,p):
    a=list(map(F,c))
    for n in range(len(a)-1,1,-1):
        v=a[n];a[n]=0;a[n-1]+=T*v;a[n-2]-=p*p*v
    return a[:2]

def build(p):
    from .arithmetic import prime
    prime(p,5)
    K=p+6;S=p*K
    th_all=sigma6(S); th=th_all[:K+1]
    J=eta_product({1:2,2:2,3:2,6:2},K)
    inv=inverse(th,K);t=times(J,times(inv,inv,K),K)
    # Trace identity at each q^n: p*c_(n/p)+c_(pn)=(p+1)c_n.
    for n in range(K+1):
        req(p*(th[n//p] if n%p==0 else 0)+th_all[p*n]==(p+1)*th[n],f'Fourier trace p={p},n={n}')
    traces=[None];current=[1]+[0]*S
    for r in range(1,p+1):
        current=times(current,th_all,S)
        traces.append([p*current[p*n] for n in range(K+1)])
    elems=[[1]+[0]*K]
    for r in range(1,p+1):
        num=[0]*(K+1)
        for j in range(1,r+1): num=plus(num,scalar(times(elems[r-j],traces[j],K),(-1)**(j-1)),K)
        req(all(v%r==0 for v in num),'exact Newton division')
        elems.append([v//r for v in num])
    thp=[th[n//p] if n%p==0 else 0 for n in range(K+1)]
    invpower=[1]+[0]*K;polys=[];validation=[]
    for r in range(p+2):
        raw=[0]*(K+1)
        if r<=p:raw=scalar(elems[r],p**(2*(p-r)))
        if r:raw=plus(raw,scalar(times(thp,elems[r-1],K),p**(2*(p-r+1))),K)
        raw=scalar(times(raw,invpower,K),(-1)**r)
        rem=raw[:];tpower=[1]+[0]*K;poly=[]
        for j in range(r//2+1):
            coeff=rem[j];poly.append(coeff)
            rem=plus(rem,scalar(tpower,-coeff),K);tpower=times(tpower,t,K)
        req(not any(rem),f'bounded extra coefficient check p={p},r={r}')
        polys.append(poly); validation.append(K-r//2)
        invpower=times(invpower,inv,K)
    req(polys[1]==[-p**(2*p-1)*(p+1)],'exact Eisenstein C1')
    req(polys[0]==[p**(2*p)],'constant X coefficient')
    req(all(c%(p*p)==0 for a in polys[:p] for c in a),'two-term p2 core')
    req(polys[-1][0]%p==1 and all(c%p==0 for c in polys[-1][1:]),'leading p core')
    # Only AFTER construction: finite specialization check using integer Q coefficients.
    q=[1,-6]
    for n in range(1,p-1):
        v=(-17*n*(n+1)-6)*q[n]-72*n*n*q[n-1]
        req(v%((n+1)**2)==0,'Q integrality');q.append(v//((n+1)**2))
    g=[comb(2*n,n)*q[n] for n in range(p)]
    Z=plus(polys[p],times(polys[p+1],g,len(polys[p+1])+len(g)-2),len(polys[p+1])+len(g)-2)
    req(all(v%(p*p)==0 for v in Z),'finite specialization coefficient identity')
    rep=None
    for y in range(1,isqrt(p//2)+1):
        x=isqrt(p-2*y*y)
        if x*x+2*y*y==p:rep=(x,y);break
    special=[]
    for t0 in [F(-1,32),F(1,64)]:
        vals=[eval_poly(c,t0) for c in polys]
        obj=dict(t0=str(t0),coefficients=list(map(str,vals)))
        if rep:
            trace=4*rep[0]**2-2*p
            rem=remainder_quadratic(vals,trace,p)
            req(rem==[0,0],'CM quadratic factor after construction')
            bad=remainder_quadratic(vals,-trace,p)
            req(any(bad),'wrong-sign mutation must be detected')
            obj.update(representation=rep,trace=trace,remainder=list(map(str,rem)),wrong_sign_remainder=list(map(str,bad)))
        special.append(obj)
    return dict(p=p,coefficients_in_t=polys,integer_coefficients=sum(map(len,polys)),
                extra_q_coefficients=sum(validation),trace_coefficient=polys[1][0],specializations=special)


from .eta import hecke as eta_hecke

def validate_polynomial(polys,p):
    from .arithmetic import prime,qseq
    prime(p,5)
    req(len(polys)==p+2 and all(len(a)==k//2+1 and all(type(c) is int for c in a) for k,a in enumerate(polys)), 'Hecke coefficient schema/degree')
    req(polys[0]==[p**(2*p)] and polys[1]==[-p**(2*p-1)*(p+1)], 'exact constant and trace coefficients')
    req(all(c%(p*p)==0 for a in polys[:p] for c in a),'two-term p2 core')
    req(polys[-1][0]%p==1 and all(c%p==0 for c in polys[-1][1:]),'leading p core')
    q=qseq(p-1);g=[comb(2*n,n)*q[n] for n in range(p)]
    width=len(polys[p+1])+len(g)-2
    relation=plus(polys[p],times(polys[p+1],g,width),width)
    req(all(v%(p*p)==0 for v in relation),'finite identity at every polynomial coefficient')
    for y in range(1,isqrt(p//2)+1):
        x=isqrt(p-2*y*y)
        if x*x+2*y*y==p:
            trace=4*x*x-2*p
            for t0 in (F(-1,32),F(1,64)):
                vals=[eval_poly(c,t0) for c in polys]
                req(remainder_quadratic(vals,trace,p)==[0,0],'exact CM factor')
            break

def certificates():
    ps=[5,7,11,17,19]
    K=80;th=sigma6(K)
    U=eta_product({1:12,2:-6,3:-4,6:2},K);V=eta_product({1:2,2:-4,3:-6,6:12},K)
    req(th==plus(U,scalar(V,-72),K),'Eisenstein versus direct eta coefficients')
    # Required weight-8 certificates reconstructed from a separate Fourier data source.
    J=eta_product({1:2,2:2,3:2,6:2},K)
    logs=[1]+[0]*K
    for d in (1,2,3,6):
        for n in range(d,K+1,d):
            for k in range(n,K+1,n):logs[k]-=2*n
    W=plus(times(th,logs,K),scalar(derivative(th),-2),K)
    th2=times(th,th,K);J2=times(J,J,K)
    res1=plus(plus(times(W,W,K),scalar(times(th2,th2,K),-1),K),
              plus(scalar(times(J,th2,K),-68),scalar(J2,-1152),K),K)
    res2=plus(plus(scalar(times(th,derivative(derivative(th)),K),2),scalar(times(derivative(th),derivative(th),K),-3),K),
              plus(scalar(times(J,th2,K),24),scalar(J2,864),K),K)
    req(not any(res1+res2),'weight8 certificate')
    hp=[build(p) for p in ps]
    eta_polynomials=[eta_hecke(p) for p in ps]
    for direct,eta in zip(hp,eta_polynomials):
        req(direct['coefficients_in_t']==eta['coefficients_in_t'],'two independent Hecke reconstructions')
        validate_polynomial(direct['coefficients_in_t'],direct['p'])
    return dict(schema_version=1,status='PASS',source_of_theta='1-12*sum sigma_1(n stripped of 2,3)*q^n',
                primes=ps,polynomials=hp,eta_q_terms=[dict(p=r['p'],q_terms_checked=r['q_terms_checked']) for r in eta_polynomials],
                eta_comparison_coefficients=K+1,weight8_required_coefficients=18,
                weight8_checked_coefficients=2*(K+1),weight8_residuals=[res1,res2],theta_prefix=th,
                integer_coefficients=sum(r['integer_coefficients'] for r in hp),
                exact_CM_factors=sum(2 for r in hp if 'representation' in r['specializations'][0]))
