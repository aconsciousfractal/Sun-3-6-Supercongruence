"""Optional exact SymPy identities; no symbolic dependency in the core replay."""


import sympy as s


def certificates():
    results=[]
    def zero(name,expr):
        r=s.factor(expr)
        if r!=0:raise ArithmeticError(f'{name}: {r}')
        results.append(dict(identity=name,residual='0'))
    t,a,b,c,h,j,ss=s.symbols('t a b c h j ss')
    Y=s.Function('Y')(t);th=lambda z:s.expand(t*s.diff(z,t))
    D=1-4*a*t+16*c*t*t
    I=D*(2*Y*th(th(Y))-th(Y)**2)+th(D)*Y*th(Y)+4*t*(-b+3*c*t)*Y**2
    LY=th(th(th(Y)))-2*t*(2*th(a*th(th(Y))+a*th(Y)+b*Y)+a*th(th(Y))+a*th(Y)+b*Y)
    LY+=4*c*t*t*(4*th(th(th(Y)))+12*th(th(Y))+11*th(Y)+3*Y)
    zero('theta I = 2 Y L Y',th(I)-2*Y*LY)
    coeff3=s.expand(LY).coeff(s.diff(Y,t,3));coeff2=s.expand(LY).coeff(s.diff(Y,t,2))
    zero('ordinary leading coefficient',coeff3-t**3*D)
    zero('ordinary second-derivative coefficient',coeff2-3*t*t*D-s.Rational(3,2)*t**3*s.diff(D,t))
    m=s.symbols('m')
    zero('simple-singular indicial factor',m*(m-1)*(m-2)+s.Rational(3,2)*m*(m-1)-m*(m-1)*(m-s.Rational(1,2)))
    # Highest resonance coefficient, with n=p-1.
    n,p=s.symbols('n p')
    zero('highest invariant coefficient',16*c*(p-1)**2+32*c*(p-1)+12*c-4*c*(2*p-1)*(2*p+1))
    # Covariance of the weight-8 certificate and W.
    u,du,ddu,l=s.symbols('u du ddu l')
    utr=j*j*u;dutr=j**4*du+2*ss*j**3*u;ddutr=j**6*ddu+6*ss*j**5*du+6*ss**2*j**4*u
    ltr=j*j*l+4*ss*j
    zero('weight4 W covariance',utr*ltr-2*dutr-j**4*(u*l-2*du))
    zero('weight8 bilinear covariance',2*utr*ddutr-3*dutr**2-j**8*(2*u*ddu-3*du**2))
    mutated=s.factor(2*utr*ddutr-2*dutr**2-j**8*(2*u*ddu-2*du**2))
    if mutated==0:raise ArithmeticError('coefficient mutation not rejected')
    # Pullback of the bilinear certificate to the invariant.
    y,y1,y2=s.symbols('y y1 y2');td=t*s.diff(D,t)
    d2=D*y*y*y2+(td*y*y/2+D*y*y1)*y1
    pr=2*y*d2-3*D*y*y*y1*y1+4*t*(-b+3*c*t)*y**4
    zero('bilinear pullback to invariant',pr-y*y*(D*(2*y*y2-y1*y1)+td*y*y1+4*t*(-b+3*c*t)*y*y))
    P=h*(1+8*h)*(1+9*h);K=(1-72*h*h)**2;tt=P/K;R=(1+8*h)*(1+9*h)/h
    phi2=-(1+8*h)/(8*(1+9*h));phi6=1/(72*h)
    zero('phi2 involution',phi2.subs(h,phi2)-h)
    zero('phi6 involution',phi6.subs(h,phi6)-h)
    zero('phi2 phi6 commute',phi2.subs(h,phi6)-phi6.subs(h,phi2))
    for label,f in [('2',phi2),('6',phi6)]:
        zero('t invariant W'+label,tt.subs(h,f)-tt)
        zero('R character W'+label,R.subs(h,f)-(1/R if label=='2' else R))
    zero('CM beta polynomial factor',64*h*(1+9*h)**3-(1+8*h)-(72*h*h+16*h+1)*(648*h*h+72*h-1))
    zero('CM beta rational target',64*P-K+(8*h*h-8*h-1)*(648*h*h+72*h-1))
    zero('CM gamma rational target',32*P+K-(72*h*h+16*h+1)**2)
    zero('gamma fixed point equation',6*((2+s.sqrt(-2))/6)**2-4*((2+s.sqrt(-2))/6)+1)
    # Determinantal invariance of the CM coset is checked for every split prime by the other verifier.
    x,y,aa,bb=s.symbols('x y aa bb')
    W2=s.Matrix([[2,-1],[6,-2]])
    M=s.Matrix([[2*aa,bb],[-2*x,2*y]])
    prod=M*W2.inv()
    difference=prod-s.Matrix([[-2*aa-3*bb,aa+bb],[2*x-6*y,-x+2*y]])
    for entry in difference:
        if s.factor(entry)!=0:raise ArithmeticError('beta W2 matrix entry')
    results.append(dict(identity='beta W2 class formula, every entry',residual='0'))
    zero('Q discriminant factors',(1+68*t+1152*t*t)-(1+32*t)*(1+36*t))
    zero('ordinary point discriminant',(1+68*t+1152*t*t).subs(t,s.Rational(1,64))-s.Rational(75,32))
    zero('singular point exact discriminant',(1+68*t+1152*t*t).subs(t,-s.Rational(1,32)))
    zero('singular theta D',th(1+68*t+1152*t*t).subs(t,-s.Rational(1,32))-s.Rational(1,8))
    data=dict(ok=True,sympy_version=s.__version__,exact_identities=len(results),identities=results,
              rejected_covariance_mutation=str(mutated),beta_W2_base_matrix=str(prod),
              singular_indicial='t0^3 Dprime(t0) m(m-1)(m-1/2)')
    data.update(schema_version=1,status="PASS")
    return data
