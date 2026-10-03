"""Optional exact structural identities and bounded normalizer/squarefree certificates."""
from __future__ import annotations

from math import comb,gcd,isqrt

import sympy as S

def req(ok,msg):
    if not ok:raise ArithmeticError(msg)

def matlist(M):return [[int(M[i,j]) for j in range(2)] for i in range(2)]
def egcd(a,b):
    r0,r1=a,b;s0,s1=1,0;t0,t1=0,1
    while r1:
        q=r0//r1;r0,r1=r1,r0-q*r1;s0,s1=s1,s0-q*s1;t0,t1=t1,t0-q*t1
    if r0<0:return -r0,-s0,-t0
    return r0,s0,t0

def reduce_left(M,p):
    a,b,c,d=map(int,[M[0,0],M[0,1],M[1,0],M[1,1]])
    req(a*d-b*c==p and c%6==0,'valid Hecke matrix')
    r,u,v=egcd(a,c);req(r in (1,p),'first-column gcd')
    L=S.Matrix([[u,v],[-c//r,a//r]])
    req(L.det()==1 and L[1,0]%6==0,'left reducer in Gamma0(6)')
    H=L*M;req(H[0,0]==r and H[1,0]==0 and H[1,1]==p//r,'Hermite form')
    modulus=p//r;k=int(H[0,1])%modulus
    shift=(int(H[0,1])-k)//modulus
    T=S.Matrix([[1,-shift],[0,1]])
    H=T*H;L=T*L
    req(L*M==H,'left equality')
    return ('inf' if r==p else str(k)), L


def certificates():
    t,a,b,c=S.symbols('t a b c');y=S.Function('y')(t);theta=lambda f:t*S.diff(f,t)
    D=1-4*a*t+16*c*t*t
    I=D*(2*y*theta(theta(y))-theta(y)**2)+theta(D)*y*theta(y)+4*t*(-b+3*c*t)*y*y
    L=theta(theta(theta(y)))-2*t*(2*theta(a*theta(theta(y))+a*theta(y)+b*y)+(a*theta(theta(y))+a*theta(y)+b*y))
    L+=4*c*t*t*(4*theta(theta(theta(y)))+12*theta(theta(y))+11*theta(y)+3*y)
    ident=S.expand(theta(I)-2*y*L);req(ident==0,'Leibniz invariant identity')
    A3=S.expand(L).coeff(S.diff(y,t,3));A2=S.expand(L).coeff(S.diff(y,t,2))
    req(S.expand(A3-t**3*D)==0,'third derivative coefficient')
    req(S.expand(A2-3*t*t*D-S.Rational(3,2)*t**3*S.diff(D,t))==0,'second derivative coefficient')
    m=S.symbols('m');req(S.expand(m*(m-1)*(m-2)+S.Rational(3,2)*m*(m-1)-m*(m-1)*(m-S.Rational(1,2)))==0,'singular indicial factor')
    # Linearization of the invariant at U=p*u, D=p*d, keeping first order in p.
    P,u,dd,z,w,e,k=S.symbols('P u dd z w e k')
    Ip=P*dd*(2*P*u*w-z*z)+e*P*u*z+k*P**2*u*u
    req(S.expand(S.expand(Ip).coeff(P,1)-z*(e*u-dd*z))==0,'defect linearization')
    W2=S.Matrix([[2,-1],[6,-2]]);W6=S.Matrix([[0,-1],[6,0]])
    aa,bb,cc,dd0=S.symbols('aa bb cc dd',integer=True);M=S.Matrix([[aa,bb],[6*cc,dd0]])
    c2=W2.inv()*M*W2;c6=W6.inv()*M*W6
    req(all(S.Poly(x,aa,bb,cc,dd0).domain.is_ZZ for x in c2),'integer W2 conjugation')
    req(all(S.Poly(x,aa,bb,cc,dd0).domain.is_ZZ for x in c6),'integer W6 conjugation')
    req(all(S.Poly(W[1,0]/6,aa,bb,cc,dd0).domain.is_ZZ for W in [c2,c6]),'conjugated lower entry divisible by 6')
    req(W2**2==-2*S.eye(2) and W6**2==-6*S.eye(2),'squares projectively trivial')
    comm=W2*W6*(W6*W2).inv();req(comm==S.Matrix([[5,2],[12,5]]),'commutator')
    h=S.symbols('h');R=1/h+17+72*h;phi2=-(1+8*h)/(8*(1+9*h));phi6=1/(72*h)
    tp=h*(1+8*h)*(1+9*h)/(1-72*h*h)**2
    identities={
      'R_phi2':S.factor(R.subs(h,phi2)-1/R),'R_phi6':S.factor(R.subs(h,phi6)-R),
      't_phi2':S.factor(tp.subs(h,phi2)-tp),'t_phi6':S.factor(tp.subs(h,phi6)-tp),
      'simple_group_commute':S.factor(phi2.subs(h,phi6)-phi6.subs(h,phi2))}
    req(not any(identities.values()),'rational character invariants')
    ps=[p for p in range(5,200) if all(p%d for d in range(2,isqrt(p)+1))]
    permutations=[];matrix_checks=0
    for p in ps:
        labels=['inf']+[str(k) for k in range(p)]
        representatives=[S.Matrix([[p,0],[0,1]])]+[S.Matrix([[1,k],[0,p]]) for k in range(p)]
        for name,W in [('W2',W2),('W6',W6),('T',S.Matrix([[1,1],[0,1]])),('V',S.Matrix([[1,0],[6,1]]))]:
            image=[]
            for rep in representatives:
                C=W.inv()*rep*W
                req(all(v.is_Integer for v in C),'integral conjugate for representatives')
                label,aux=reduce_left(C,p);image.append(label);matrix_checks+=1
            req(set(image)==set(labels) and len(image)==len(set(image)),'orbit permutation')
            permutations.append(dict(p=p,generator=name,image=image))
    # Completely separate direct Q formula for squarefree-part certificates.
    f=[sum(comb(n,k)**3 for k in range(n+1)) for n in range(199)]
    q=[sum(comb(n,k)*(-8)**(n-k)*f[k] for k in range(n+1)) for n in range(199)]
    sq=[]
    for p in ps:
        U=S.Poly.from_list([comb(2*n,n)*q[n]%p for n in range(p-1,-1,-1)],t,modulus=p)
        g=S.gcd(U,U.diff());g0=int(g.eval(0))%p;req(g0!=0,'normalizable gcd')
        V=g.mul_ground(pow(g0,-1,p));SF=U.exquo(V*V)
        Disc=S.Poly(1+68*t+1152*t*t,t,modulus=p)
        req(Disc.rem(SF).is_zero,'squarefree part divides discriminant')
        req(S.gcd(SF,SF.diff()).degree()==0 and S.gcd(SF,V).degree()==0,'only multiplicities one/two')
        leg=lambda n:1 if pow(n%p,(p-1)//2,p)==1 else -1
        e2=(1-leg(-2))//2;e3=(1-leg(-3))//2
        predicted=S.Poly((1+32*t)**e2*(1+36*t)**e3,t,modulus=p)
        req(SF==predicted,'character squarefree-part regression')
        sq.append(dict(p=p,U_degree=U.degree(),V_degree=V.degree(),e_minus2=e2,e_minus3=e3,
                 squarefree_coefficients=[int(x)%p for x in reversed(SF.all_coeffs())]))
    obj=dict(schema_version=1,status="PASS",symbolic_identities=15,normalizer_matrix_checks=matrix_checks,
             conjugation_W2=str(c2),conjugation_W6=str(c6),commutator=matlist(comm),
             permutations=permutations,squarefree_decompositions=sq,
             note='15 identities: Leibniz, A3,A2, indicial, defect, two conjugation integrality formulas, two squares, commutator, five rational identities. Finite permutations/squarefree checks do not establish their uniform statements.')
    return obj
