"""Exact integer arithmetic for the defining Franel transform and Sun 3.6."""
from __future__ import annotations

from fractions import Fraction
from math import isqrt



def natural(value, label="integer", minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def prime(p, minimum=3):
    natural(p, "prime", minimum)
    if any(p % d == 0 for d in range(2, isqrt(p)+1)):
        raise ValueError("prime required")
    return p


def require(ok: bool, message: str) -> None:
    if not ok: raise ArithmeticError(message)


def primes(bound: int) -> list[int]:
    natural(bound, "prime bound", 3)
    return [p for p in range(3,bound+1,2)
            if all(p%d for d in range(3,isqrt(p)+1,2))]


def qseq(n: int) -> list[int]:
    natural(n, "sequence degree")
    q=[1,-6]
    for k in range(1,n):
        num=(-17*k*(k+1)-6)*q[k]-72*k*k*q[k-1]
        den=(k+1)**2
        require(num%den==0, f'integral Q recurrence at {k}')
        q.append(num//den)
    return q[:n+1]


def pascal(n: int) -> list[list[int]]:
    rows=[[1]]
    for k in range(1,n+1):
        r=rows[-1]; rows.append([1]+[r[j-1]+r[j] for j in range(1,k)]+[1])
    return rows


def original(n: int) -> tuple[list[int],list[int]]:
    natural(n, "definition degree")
    rows=pascal(n); f=[sum(x**3 for x in r) for r in rows]
    q=[sum(rows[k][j]*(-8)**(k-j)*f[j] for j in range(k+1)) for k in range(n+1)]
    return f,q


def inv_euclid(a: int,m: int) -> int:
    a%=m; r0,r1,s0,s1=m,a,0,1
    while r1:
        k=r0//r1; r0,r1=r1,r0-k*r1; s0,s1=s1,s0-k*s1
    if r0!=1: raise ValueError('nonunit')
    return s0%m


def evaluate(poly: list[int],t: int,m: int) -> int:
    out=0
    for a in reversed(poly):out=(out*t+a)%m
    return out


def pmul(a,b,mod=None):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):c[i+j]+=x*y
    return [x%mod for x in c] if mod else c


def padd(*aa):
    c=[0]*max(map(len,aa))
    for a in aa:
        for i,x in enumerate(a):c[i]+=x
    return c


def pscale(a,k):return [k*x for x in a]

def invariant(u,mod=None):
    require(bool(u) and all(type(x) is int for x in u), "nonempty exact integer polynomial required")
    th=[i*x for i,x in enumerate(u)]
    th2=[i*i*x for i,x in enumerate(u)]
    D=[1,68,1152]; td=[0,68,2304]
    core=padd(pscale(pmul(u,th2),2),pscale(pmul(th,th),-1))
    out=padd(pmul(D,core),pmul(td,pmul(u,th)),pmul([0,24,864],pmul(u,u)))
    return [x%mod for x in out] if mod else out


def validate_endpoint(p, qp, gp):
    prime(p)
    require(type(qp) is int and type(gp) is int, 'exact integer endpoint values')
    require((qp+6)%(p*p)==0 and (gp+12)%(p*p)==0, 'degree-p endpoint')


def validate_cm_row(row,p,x,y):
    """Recheck the matrix, character and exact quadratic root without numeric approximations."""
    prime(p,5)
    require(x*x+2*y*y==p,'CM representation')
    require(row['point'] in ('beta','gamma'),'CM point')
    e=2 if row['point']=='beta' and x%3==0 else 1
    require(row['e']==e and row['character']==(-1 if e==2 else 1),'Atkin-Lehner character')
    a,b,c,d=row['M']
    require(all(type(v) is int for v in row['M']) and a*d-b*c==e,'CM determinant')
    if e==1:require(c%6==0,'Gamma0(6) membership')
    tau=(Fraction(1,3),Fraction(1,6)) if row['point']=='gamma' else (Fraction(0),Fraction(1,2))
    def mult(v,w):return (v[0]*w[0]-2*v[1]*w[1],v[0]*w[1]+v[1]*w[0])
    den=(c*tau[0]+d,c*tau[1]);num=(a*tau[0]+b,a*tau[1])
    require(num==mult(((tau[0]+row['k'])/p,tau[1]/p),den),'CM image')
    root=(row['z_rational'],row['z_delta'])
    require(mult(root,mult(den,den))==(Fraction(e*p*p,row['character']),0),'exact root/character')
    require(2*root[0]==4*x*x-2*p and root[0]**2+2*root[1]**2==p*p,'CM trace/norm')


def egcd(a,b):
    if not b:return (1 if a>=0 else -1),0,abs(a)
    u,v,d=egcd(b,a%b)
    return v,u-(a//b)*v,d


def mulmat(M,N):
    a,b,c,d=M;e,f,g,h=N
    return [a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h]


def matrix_rows(p,x,y):
    prime(p, 5)
    require(type(x) is int and type(y) is int and x > 0 and y > 0 and x*x+2*y*y == p, "CM representation")
    out=[]
    a,b,d=egcd(x+2*y,6*y);require(d==1,'gamma Bezout')
    out.append(dict(point='gamma',e=1,character=1,M=[a,b,-6*y,x+2*y],
                    k=b*(x-2*y)-a*y,unit_sign=1))
    if y%3==0:
        a,b,d=egcd(x,2*y);require(d==1,'beta base Bezout')
        out.append(dict(point='beta',e=1,character=1,M=[a,b,-2*y,x],
                        k=b*x-a*y,unit_sign=1))
    else:
        require(x%3==0,'exactly one coefficient divisible by 3')
        a,b,d=egcd(2*y,x);require(d==1,'beta W2 Bezout')
        M=[2*a,b,-2*x,2*y]
        # W2^{-1} = [[-1,1/2],[-3,1]].
        base=mulmat(M,[-1,Fraction(1,2),-3,1])
        require(all(getattr(z,'denominator',1)==1 for z in base),'W2 class integral')
        require(base[2]%6==0 and base[0]*base[3]-base[1]*base[2]==1,'W2 class')
        out.append(dict(point='beta',e=2,character=-1,M=M,k=b*y-a*x,unit_sign=-1,
                        base_matrix=[int(z) for z in base]))
    # Q(delta) arithmetic; delta^2=-2. No floating point.
    def mult(a,b):return (a[0]*b[0]-2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    for row in out:
        a,b,c,d=row['M'];e=row['e'];k=row['k']
        tau=(Fraction(1,3),Fraction(1,6)) if row['point']=='gamma' else (Fraction(0),Fraction(1,2))
        num=(a*tau[0]+b,a*tau[1]); den=(c*tau[0]+d,c*tau[1])
        rhs=mult(((tau[0]+k)/p,tau[1]/p),den)
        require(num==rhs,'CM image relation')
        require(a*d-b*c==e,'CM determinant')
        if e==1:require(c%6==0,'base membership')
        v=(x,row['unit_sign']*y);z=mult(v,v)
        lhs=mult(z,mult(den,den));expected=(Fraction(e*p*p,row['character']),0)
        require(lhs==expected,'exact root formula')
        row['z_rational']=z[0];row['z_delta']=z[1]
        row['trace']=2*z[0];row['norm']=z[0]**2+2*z[1]**2
        require(row['trace']==4*x*x-2*p and row['norm']==p*p,'CM trace/norm')
        validate_cm_row(row,p,x,y)
    return out


