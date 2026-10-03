"""Exact eta products, modular coefficient certificates and eta-based Hecke reconstruction."""
from __future__ import annotations

from fractions import Fraction as F
from math import comb,gcd



def req(ok,msg):
    if not ok:raise ArithmeticError(msg)

def add(*polys):
    n=max(map(len,polys));c=[0]*n
    for a in polys:
        for i,x in enumerate(a):c[i]+=x
    return c

def scale(a,k):return [x*k for x in a]

def mul(a,b,n):
    out=[0]*(n+1)
    for i,x in enumerate(a[:n+1]):
        if x:
            for j,y in enumerate(b[:n-i+1]):out[i+j]+=x*y
    return out

def power(a,k,n):
    out=[1]+[0]*n
    while k:
        if k%2:out=mul(out,a,n)
        a=mul(a,a,n);k//=2
    return out

def inverse(a,n):
    req(a[0] in (1,-1),'unit constant required')
    b=[a[0]]+[0]*n
    for k in range(1,n+1):b[k]=-a[0]*sum(a[j]*b[k-j] for j in range(1,min(k+1,len(a))))
    return b

def compose(a,t,n):
    req(t[0]==0,'composition at zero')
    out=[0]*(n+1)
    for v in reversed(a):out=mul(out,t,n);out[0]+=v
    return out

def eta(rs,n,engine='product'):
    from .arithmetic import natural
    natural(n, 'eta degree')
    req(bool(rs) and all(type(d) is int and d in (1,2,3,6) and type(r) is int for d,r in rs.items()), 'level-six integer eta exponents')
    if engine not in ('product','log'):raise ValueError('unknown eta engine')
    shift=F(sum(d*r for d,r in rs.items()),24)
    req(shift.denominator==1 and shift>=0,'nonnegative integral eta shift')
    shift=int(shift);N=n-shift
    if N<0:return [0]*(n+1)
    if engine=='product':
        a=[1]+[0]*N
        for k in range(1,N+1):
            e=sum(r for d,r in rs.items() if k%d==0)
            if not e:continue
            fac=[0]*(N+1)
            for j in range(N//k+1):
                fac[k*j]=((-1)**j*comb(e,j) if j<=e else 0) if e>=0 else comb(-e+j-1,j)
            a=mul(a,fac,N)
    else:
        # Logarithmic derivative recurrence: n*a_n=sum_{k=1}^n L_k*a_(n-k).
        L=[0]*(N+1)
        for k in range(1,N+1):
            e=sum(r for d,r in rs.items() if k%d==0)
            for m in range(k,N+1,k):L[m]-=k*e
        a=[1]+[0]*N
        for k in range(1,N+1):
            num=sum(L[j]*a[k-j] for j in range(1,k+1))
            req(num%k==0,'eta integral division');a[k]=num//k
    return [0]*shift+a

def theta(a):return [i*v for i,v in enumerate(a)]

def cusp(rs):
    return [F(sum(F(6*gcd(c,d)**2*r,24*gcd(c,6//c)*c*d) for d,r in rs.items())) for c in (1,2,3,6)]

def newman(rs):
    wt=F(sum(rs.values()),2);s1=sum(d*r for d,r in rs.items());s2=sum((6//d)*r for d,r in rs.items())
    primes=(2,3);square=all(sum(r*(int(d%l==0)) for d,r in rs.items())%2==0 for l in primes)
    return dict(weight=str(wt),sum_dr=s1,sum_N_over_d_r=s2,
                trivial_character=wt.denominator==1 and int(wt)%2==0 and square,
                congruences=s1%24==s2%24==0,cusp_orders=list(map(str,cusp(rs))))

H={1:-5,2:1,3:-1,6:5};Z={1:6,2:-3,3:-2,6:1}
U={d:2*r for d,r in Z.items()};V={1:2,2:-4,3:-6,6:12}
J={1:2,2:2,3:2,6:2};H2={1:-24,2:24};RU={1:-12,2:12,3:12,6:-12}

def data(n,engine='product'):
    h=eta(H,n,engine);z=eta(Z,n,engine);uu=eta(U,n,engine);vv=eta(V,n,engine);jj=eta(J,n,engine)
    Th=add(uu,scale(vv,-72));t=mul(jj,power(inverse(Th,n),2,n),n)
    return h,z,Th,jj,t

def div_exact(a,k):
    req(all(v%k==0 for v in a),f'Newton integral /{k}');return [v//k for v in a]

def polynomial_at(poly,x):
    v=F(0)
    for c in reversed(poly):v=v*x+c
    return v

def quadratic_remainder(poly,trace,p):
    a=list(map(F,poly))
    for k in range(len(a)-1,1,-1):
        u=a[k];a[k]=0;a[k-1]+=u*trace;a[k-2]-=u*p*p
    return a[:2]

def full_multiply(a,b):return mul(a,b,len(a)+len(b)-2)

def hecke(p):
    from .arithmetic import prime
    prime(p,5)
    N=p+4;S=p*N
    _,_,ths,_,_=data(S,'log')
    th=ths[:N+1];t=data(N,'log')[4]
    # Build elementary symmetric polynomials of Theta(zeta^k q^(1/p)), via integral Newton sums.
    traces=[[0]*(N+1)];zpow=[1]+[0]*S
    for j in range(1,p+1):
        zpow=mul(zpow,ths,S)
        traces.append([p*zpow[p*k] for k in range(N+1)])
    elem=[[1]+[0]*N]
    for k in range(1,p+1):
        num=[0]*(N+1)
        for j in range(1,k+1):num=add(num,scale(mul(elem[k-j],traces[j],N),(-1)**(j-1)))
        elem.append(div_exact(num,k))
    first=[th[k//p] if k%p==0 else 0 for k in range(N+1)]
    invth=inverse(th,N);polys=[]
    for k in range(p+2):
        total=[0]*(N+1)
        if k<=p:total=scale(elem[k],p**(2*(p-k)))
        if k>0:total=add(total,scale(mul(first,elem[k-1],N),p**(2*(p-k+1))))
        series=scale(mul(total,power(invth,k,N),N),(-1)**k)
        rem=series[:];poly=[];tpow=[1]+[0]*N
        for d in range(k//2+1):
            v=rem[d];poly.append(v);rem=add(rem,scale(tpow,-v));tpow=mul(tpow,t,N)
        req(not any(rem),f'Hecke degree reconstruction p={p} coefficient={k}')
        polys.append(poly)
        if k<p:req(all(c%(p*p)==0 for c in poly),'two-term modulo p2')
    req(polys[-1][0]%p==1 and all(c%p==0 for c in polys[-1][1:]),'leading modulo p')
    q=[1,-6]
    for k in range(1,p):q.append(((-17*k*(k+1)-6)*q[k]-72*k*k*q[k-1])//((k+1)**2))
    g=[comb(2*k,k)*q[k] for k in range(p)]
    cons=add(polys[p],full_multiply(polys[p+1],g))
    req(all(c%(p*p)==0 for c in cons),'finite polynomial specialization identity')
    rep=next(((x,y) for x in range(1,p) for y in range(1,p) if x*x+2*y*y==p),None)
    special=[]
    for t0 in (F(-1,32),F(1,64)):
        coeff=[polynomial_at(a,t0) for a in polys]
        row=dict(t0=str(t0),coefficients=[str(c) for c in coeff])
        if rep:
            trace=4*rep[0]**2-2*p
            rem=quadratic_remainder(coeff,trace,p)
            req(rem==[0,0],'exact CM quadratic factor')
            wrong=quadratic_remainder(coeff,-trace,p)
            req(any(wrong),'opposite-sign CM factor rejected')
            row.update(trace=trace,quadratic_factor=[p*p,-trace,1],remainder=[str(c) for c in rem],
                       wrong_sign_remainder=[str(c) for c in wrong])
        special.append(row)
    return dict(p=p,q_terms_checked=N+1,total_integer_coefficients=sum(map(len,polys)),
                coefficients_in_t=polys,specializations=special)


from .cusps import certificates as cusp_constants


def validate_period(g,t,th):
    req(len(g)==len(t)==len(th) and len(g)>=19,'nonempty period window through degree 18 required')
    req(all(type(v) is int for seq in (g,t,th) for v in seq),'exact integer period coefficients')
    req(g[0]==1 and g[1]==-12 and t[0]==0 and t[1]==1 and th[0]==1,'period normalization')
    req(compose(g,t,len(g)-1)==th,'central Q period coefficient identity')

def certificates():
    N=30
    rows={name:newman(r) for name,r in [('h',H),('U',U),('V',V),('J',J),('H2',H2),('R',RU)]}
    for v in rows.values():req(v['congruences'] and v['trivial_character'],'Newman base modularity')
    x=data(N,'product');y=data(N,'log');req(x==y,'two series engines')
    h,z,th,j,t=x;hh=mul(h,h,N);one=[1]+[0]*N
    P=mul(h,add(one,scale(h,17),scale(hh,72)),N)
    K=power(add(one,scale(hh,-72)),2,N)
    req(mul(t,K,N)==P,'rational t identity')
    # R has a pole of order 1; qR uses the same exponent product with shift removed.
    # Build qR by integrating its logarithmic derivative, independently of h.
    L=[-1]+[0]*N
    for k in range(1,N+1):
        e=sum(v for d,v in RU.items() if k%d==0)
        for m in range(k,N+1,k):L[m]-=k*e
    req(th==scale(L,-1),'Theta = -partial log R')
    # Derivative identity of h and original period.
    req(theta(h)==mul(mul(h,add(one,scale(h,17),scale(hh,72)),N),mul(z,z,N),N),'h derivative')
    H2s=eta(H2,N,'log')
    req(mul(H2s,add(one,scale(h,8)),N)==mul(h,power(add(one,scale(h,9)),3,N),N),'H2 identity')
    q=[1,-6]
    for k in range(1,N):q.append(((-17*k*(k+1)-6)*q[k]-72*k*k*q[k-1])//((k+1)**2))
    g=[comb(2*k,k)*q[k] for k in range(N+1)]
    validate_period(g,t,th)
    req(compose(q,h,N)==z,'uncentralized Q full period prefix')
    # The manuscript justifies modularity and holomorphy before applying the coefficient bound.
    logj=[1]+[0]*N
    for k in range(1,N+1):
        e=sum(v for d,v in J.items() if k%d==0)
        for m in range(k,N+1,k):logj[m]-=k*e
    W=add(mul(th,logj,N),scale(theta(th),-2))
    p1=add(mul(W,W,N),scale(power(th,4,N),-1),scale(mul(j,power(th,2,N),N),-68),scale(mul(j,j,N),-1152))
    p2=add(scale(mul(th,theta(theta(th)),N),2),scale(mul(theta(th),theta(th),N),-3),
           scale(mul(j,power(th,2,N),N),24),scale(mul(j,j,N),864))
    req(not any(p1+p2),'weight8 invariants')
    mutations=[]
    for label,bad in [('a+1',add(p1,scale(mul(j,power(th,2,N),N),4))),
                      ('b+1',add(p2,scale(mul(j,power(th,2,N),N),-4))),
                      ('c+1',add(p1,scale(mul(j,j,N),-16)))]:
        req(any(bad[:9]),'Sturm certificate catches mutation');mutations.append(dict(mutation=label,first_nonzero=next(i for i,v in enumerate(bad) if v)))
    cert=dict(bound=8,weight=8,index=12,required_coefficients=18,extra_through=N,
              p1=p1,p2=p2,mutations=mutations)
    # Explicit weight-2 certificate used to identify the Atkin--Lehner character.
    return dict(schema_version=1,status='PASS',series_through=N,
                independent_series_engines=2,eta_modularity=rows,q_series=dict(h=h,z=z,theta=th,J=j,t=t),
                weight2_certificate=dict(weight=2,index=12,required_coefficients=3,residual=add(th,L)),
                weight8_certificate=cert,cusp_constants=cusp_constants())
