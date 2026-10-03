"""Exact Laurent constant terms and the pure-row endpoint normalization."""
import itertools



def req(ok,msg):
    if not ok:raise ArithmeticError(msg)

def mul(a,b):
    o={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():o[i+k,j+l]=o.get((i+k,j+l),0)+v*w
    return {k:v for k,v in o.items() if v}


def certificates():
    factors=[{(1,0):-1,(0,1):1,(0,0):1},{(1,0):1,(0,1):-1,(0,0):1},
             {(1,0):1,(0,1):1,(0,0):-1},{(1,0):1,(0,1):1,(0,0):1},
             {(2,0):1,(0,2):1,(0,0):1}]
    lam={(0,0):1}
    for f in factors:lam=mul(lam,f)
    lam={(i-2,j-2):v for (i,j),v in lam.items()}
    q=[1,-6]
    for n in range(1,25):
        num=(-17*n*(n+1)-6)*q[n]-72*n*n*q[n-1]
        req(num%(n+1)**2==0,'integral recurrence');q.append(num//(n+1)**2)
    pol={(0,0):1};rows=[]
    for n in range(26):
        val=pol.get((0,0),0)
        req(val==(-1)**n*q[n],'positive F sign normalization')
        rows.append(dict(n=n,F_constant_term=val,Qn=q[n]));pol=mul(pol,lam)
    pure=[]
    for rowsel in itertools.product(range(3),repeat=5):
        total=[sum(int(rowsel[k]==i) for k in range(4))+2*int(rowsel[4]==i) for i in range(3)]
        if total!=[2,2,2]:continue
        sign=(-1)**(int(rowsel[0]==0)+int(rowsel[1]==1)+int(rowsel[2]==2))
        pure.append(dict(rows=rowsel,sign=sign))
    req(sum(v['sign'] for v in pure)==6,'F1 exact pure-row sum')
    return dict(schema_version=1,status='PASS',
             source='Gorodetsky Proposition 1.2 equation (1.8)',
             exact_CT_terms=[dict(i=i,j=j,value=v) for (i,j),v in sorted(lam.items())],
             CT_sequence_checks=rows,pure_base_rows=pure,pure_base_sum=6)
