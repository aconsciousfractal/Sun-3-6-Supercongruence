"""Recompute both sums and endpoint congruences; branch values are regression targets only."""
from collections import Counter
from math import comb, isqrt
from .arithmetic import (natural,primes,qseq,original,pascal,evaluate,inv_euclid,
                         require,matrix_rows,validate_endpoint)

def regression(bound=1999):
    natural(bound, 'prime bound', 19)
    ps=primes(bound);qs=qseq(bound)
    # Exact central coefficients; no conjectural reduction used to construct them.
    gs=[comb(2*n,n)*q for n,q in enumerate(qs)]
    ncheck=min(198,bound);_,orig=original(ncheck)
    require(orig==qs[:ncheck+1],'original binomial Q vs recurrence')
    sums=[];matrices=[]
    exceptions=[]
    for p in ps:
        m=p*p;tminus=-pow(32,-1,m)%m;tplus=pow(64,-1,m)
        u=[g%m for g in gs[:p]]
        sm=evaluate(u,tminus,m);sp=evaluate(u,tplus,m)
        rep=next(((x,isqrt((p-x*x)//2)) for x in range(1,isqrt(p)+1)
                 if (p-x*x)%2==0 and 2*isqrt((p-x*x)//2)**2==p-x*x),None)
        split=p%8 in (1,3)
        require(bool(rep)==split,'quadratic representation classification')
        target=(4*rep[0]**2-2*p)%m if rep else 0
        require(sm==target and sp==target,f'target at p={p}')
        validate_endpoint(p,qs[p],gs[p])
        if p<=ncheck:
            # Pascal original values, separate Euclidean inverse and forward summation.
            rows=pascal(2*(p-1));origgs=[rows[2*n][n]*orig[n] for n in range(p)]
            for den,value in [(-32,sm),(64,sp)]:
                power=1;v=0;iv=inv_euclid(den,m)
                for g in origgs:v=(v+g*power)%m;power=power*iv%m
                require(v==value,'independent original sum')
        sums.append(dict(p=p,residue8=p%8,x=rep[0] if rep else '',y=rep[1] if rep else '',
                         minus32=sm,plus64=sp,target=target,Qp=qs[p]%m,gp=gs[p]%m))
        if split and p>3:matrices += [dict(p=p,x=rep[0],y=rep[1],**r) for r in matrix_rows(p,*rep)]
        if p in (3,5):
            exceptions.append(dict(p=p,minus_terms=[g*pow(tminus,n,m)%m for n,g in enumerate(gs[:p])],
                                   plus_terms=[g*pow(tplus,n,m)%m for n,g in enumerate(gs[:p])],value=sm))
    counts=Counter(r['residue8'] for r in sums)
    require(any(r['target'] for r in sums),'nonzero split regression required')
    return dict(schema_version=1,status='PASS',scope='bounded exact regression',
                bound_inclusive=bound,prime_count=len(ps),residue_counts=dict(counts),
                original_definition_values=ncheck+1,original_sum_checks=2*len([p for p in ps if p<=ncheck]),
                endpoint_checks=2*len(ps),rows=sums,cm_matrices=matrices,exceptional_primes=exceptions)
