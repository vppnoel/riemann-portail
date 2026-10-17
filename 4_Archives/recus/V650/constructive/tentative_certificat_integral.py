#!/usr/bin/env python3
"""New bounded-support certificate attempt; checkpoints before every stage.

No pre-existing corpus file is modified. Full operator positivity is asserted
only when all outward budgets below are positive and successfully checked.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import sys,json,time,hashlib
import numpy as np
from numpy.polynomial.legendre import leggauss
import mpmath as mp
import reconstruction as r
sys.set_int_max_str_digits(0)

ROOT=Path(__file__).resolve().parent
source_candidates=[ROOT.parent/'v650'/'programme-riemann'/'3_Preuves_et_calculs'/'src']
for ancestor in ROOT.parents:
    source_candidates.extend([ancestor/'3_Preuves_et_calculs'/'src',ancestor/'src'])
SOURCE=next((p for p in source_candidates if (p/'common_operator_certificate.py').is_file()),None)
if SOURCE is None:raise FileNotFoundError('place this directory inside the Programme Riemann corpus')
sys.path.insert(0,str(SOURCE))
import common_operator_certificate as old
import prime_centered_bridge as bridge

S=F(11,20);T=F(700);U=F(10);N=640;H=F(1,200);h=F(1,1000)

def checkpoint(j):
    (ROOT/'checkpoint_integral.json').write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
    print(j['stage'],flush=True)

def certify_gauss(n=640,bisections=40,brackets=None):
    guess,_=leggauss(n)
    coefficients=old.legendre_integer_coefficients(n)
    deriv=old.legendre_integer_coefficients(n,1)
    rows=[];last=F(0)
    def sign(q):
        a=old.exact_polynomial_value(coefficients,q)
        if not a: raise ValueError('nonzero bracket endpoint required')
        return 1 if a>0 else -1
    for i,g in enumerate(guess[n//2:]):
        if brackets is None:
            center=F.from_float(float(g));lo=center-F(1,2**42);hi=center+F(1,2**42)
        else:
            lo=F(brackets[i]['root_lo']);hi=F(brackets[i]['root_hi'])
        if not last<lo<hi<1: raise ValueError('ordered disjoint root brackets required')
        sl=sign(lo)
        if sl!=-sign(hi): raise ValueError('exact sign change missing')
        for _ in range(bisections):
            mid=(lo+hi)/2
            if sign(mid)==sl:lo=mid
            else:hi=mid
        xx=mp.iv.mpf([bridge.midpoint(bridge.I(lo)),bridge.midpoint(bridge.I(hi))])
        dc=bridge.I(old.exact_polynomial_value(deriv,(lo+hi)/2,2**n))
        eps=F(n**4)*(hi-lo)/2
        dp=dc+mp.iv.mpf([-bridge.midpoint(bridge.I(eps)),bridge.midpoint(bridge.I(eps))])
        weight=2/((1-xx*xx)*dp*dp)
        if bridge.lo(weight)<=0:raise ValueError('positive weight interval required')
        rows.append(dict(root_lo=str(lo),root_hi=str(hi),weight=bridge.pack(weight)))
        last=hi
    return rows

def trig(z):
    if np.any(np.asarray(z[0])<-386) or np.any(np.asarray(z[1])>386):raise ValueError('phase guard failed')
    v=r.times(z,r.qiv(F(1,512)));v2=r.times(v,v)
    c=r.horner([F((-1)**k,factorial(2*k)) for k in range(11)],v2)
    s=r.times(v,r.horner([F((-1)**k,factorial(2*k+1)) for k in range(11)],v2))
    ec=r.qiv(F(1,factorial(22)))[1];es=r.qiv(F(1,factorial(23)))[1]
    c=r.plus(c,(-ec,ec));s=r.plus(s,(-es,es))
    for _ in range(9):
        c,s=r.minus(r.times(c,c),r.times(s,s)),r.times(r.qiv(2),r.times(c,s))
    return c,s

def exp_iv(z):
    if np.any(np.abs(z[0])>.276) or np.any(np.abs(z[1])>.276):raise ValueError('exponential guard failed')
    out=r.horner([F(1,factorial(k)) for k in range(25)],z)
    rem=F(4,3)*F(3,10)**25/factorial(25)
    e=r.qiv(rem)[1]
    return r.plus(out,(-e,e))

def positive_integral(g0,g1):
    """Outward evaluation of monotone integral for exact dyadic endpoints."""
    pos=(g0>0)&(g1>0)
    left=(g0>0)&(g1<=0);right=(g0<=0)&(g1>0)
    lo=np.zeros_like(g0);hi=np.zeros_like(g0)
    for mask,mode in ((pos,'both'),(left,'left'),(right,'right')):
        if not np.any(mask):continue
        a=(g0[mask],g0[mask]);b=(g1[mask],g1[mask])
        if mode=='both':val=r.times(r.qiv(h/2),r.plus(a,b))
        elif mode=='left':val=r.times(r.qiv(h/2),r.over(r.times(a,a),r.minus(a,b)))
        else:val=r.times(r.qiv(h/2),r.over(r.times(b,b),r.minus(b,a)))
        lo[mask]=val[0];hi[mask]=val[1]
    return lo,hi

def weights_iv(table):
    nf=int(T/h);ratio=int(H/h);idx=np.arange(nf,dtype=np.int64)
    macro=idx//ratio;k=idx%ratio
    a=(table[macro],table[macro]);b=(table[macro+1],table[macro+1])
    def at(k):
        sums=r.plus(r.times((ratio-k,ratio-k),a),r.times((k,k),b))
        return r.minus(r.qiv(U),r.over(sums,r.qiv(ratio)))
    g0=at(k);g1=at(k+1)
    lower=positive_integral(g0[0],g1[0])[0]
    upper=positive_integral(g0[1],g1[1])[1]
    return r.over((lower,upper),r.iv_to_float(mp.iv.pi))

def gamma_enclosure(n=1024):
    Hn=sum((F(1,k) for k in range(1,n+1)),F(0))
    base=bridge.I(Hn)-mp.iv.log(bridge.I(n))-bridge.I(F(1,2*n))+bridge.I(F(1,12*n*n))
    lower=bridge.lo(bridge.I(bridge.lo(base)-F(1,120*n**4)))
    upper=bridge.hi(bridge.I(bridge.hi(base)))
    return mp.iv.mpf([bridge.midpoint(bridge.I(lower)),bridge.midpoint(bridge.I(upper))])

def run():
    begin=time.monotonic()
    old_checkpoint=ROOT/'checkpoint_integral.json'
    cached_gauss=None
    if old_checkpoint.exists():
        cached=json.loads(old_checkpoint.read_text())
        if cached.get('gauss_nodes')==N and len(cached.get('positive_gauss',[]))==N//2:
            cached_gauss=cached['positive_gauss']
    j=dict(stage='started',version='V6.50 NEW reconstruction',continuous_positive_certificate=False,global_RH_claim=False)
    checkpoint(j)
    if np.finfo(np.float64).eps!=2**-52 or np.finfo(np.float64).nmant!=52:raise ValueError('IEEE binary64 required')
    table,radius,table_detail=r.build_table()
    j.update(stage='table_certified',table=table_detail)
    checkpoint(j)
    gauss=certify_gauss(N,0,cached_gauss) if cached_gauss is not None else certify_gauss()
    j.update(stage='gauss_nodes_weights_certified',gauss_nodes=N,positive_gauss=gauss)
    checkpoint(j)
    x=(np.array([r.qiv(F(row['root_lo']))[0] for row in gauss])[:,None],
       np.array([r.qiv(F(row['root_hi']))[1] for row in gauss])[:,None])
    weights=[mp.iv.mpf([bridge.midpoint(bridge.I(bridge.endpoint_q(row['weight']['binary'][0]))),
                      bridge.midpoint(bridge.I(bridge.endpoint_q(row['weight']['binary'][1])))]) for row in gauss]
    swi=[r.iv_to_float(mp.iv.sqrt(2*bridge.I(S)*w)) for w in weights]
    sw=(np.array([a for a,b in swi])[:,None],np.array([b for a,b in swi])[:,None])
    x=r.times(x,r.qiv(S))
    ep=exp_iv(r.times(x,r.qiv(F(1,2))));em=exp_iv(r.times(x,r.qiv(F(-1,2))))
    cw=r.times(r.plus(ep,em),r.qiv(F(1,2)));ssw=r.times(r.minus(ep,em),r.qiv(F(1,2)))
    si=bridge.I(S)
    sh=(mp.iv.exp(si/2)-mp.iv.exp(-si/2))/2
    ch=(mp.iv.exp(si/2)+mp.iv.exp(-si/2))/2
    gp=si+(mp.iv.exp(si)-mp.iv.exp(-si))/2
    gm=(mp.iv.exp(si)-mp.iv.exp(-si))/2-si
    if bridge.lo(gm)<=2*S/F(49):raise ValueError('moment Gram floor failed')
    if bridge.hi(mp.iv.exp(si/2))>=F(4,3):raise ValueError('exponential interpolation factor failed')
    wi=weights_iv(table);nf=len(table)*int(H/h)-int(H/h)
    # nf equals exactly T/h; local weight errors are separate from table error.
    if nf!=int(T/h):raise ValueError('grid count mismatch')
    wm=wi[0]/2+wi[1]/2
    we=r.up(np.maximum(np.abs(wm-wi[0]),np.abs(wi[1]-wm)))
    max_weight_error=F.from_float(float(np.max(we)))
    if np.min(wm)<0 or np.max(wm)>float(U*h)/float(mp.pi)*1.001:raise ValueError('weight guards failed')
    matrices=[np.zeros((N//2,N//2)),np.zeros((N//2,N//2))]
    row_errors=[np.zeros(N//2),np.zeros(N//2)]
    norm_sample=[0.,0.]
    for first in range(0,nf,2048):
        idx=np.arange(first,min(nf,first+2048),dtype=np.float64)
        selected=wm[first:first+2048]>0
        if not np.any(selected):
            continue
        idx=idx[selected]
        ti=r.times((idx+.5,idx+.5),r.qiv(h));ti=(ti[0][None,:],ti[1][None,:])
        co,sn=trig(r.times(ti,r.qiv(S)))
        cx,sx=trig(r.times(x,ti))
        denom=r.plus(r.times(ti,ti),r.qiv(F(1,4)))
        bc=r.over(r.plus(r.times(r.iv_to_float(sh),co),r.times(r.times(r.qiv(2),ti),r.times(r.iv_to_float(ch),sn))),denom)
        bs=r.over(r.minus(r.times(r.iv_to_float(ch),sn),r.times(r.times(r.qiv(2),ti),r.times(r.iv_to_float(sh),co))),denom)
        even=r.times(sw,r.minus(cx,r.times(r.over(bc,r.iv_to_float(gp)),cw)))
        odd=r.times(sw,r.minus(sx,r.times(r.over(bs,r.iv_to_float(gm)),ssw)))
        for p,v in enumerate((even,odd)):
            center=v[0]/2+v[1]/2
            ve=r.up(np.maximum(np.abs(center-v[0]),np.abs(v[1]-center)))
            row_errors[p]=np.maximum(row_errors[p],np.max(ve,axis=1))
            norm_sample[p]=max(norm_sample[p],float(np.max(np.sum(center*center,axis=0))))
            matrices[p]+=(center*wm[first:first+2048][selected])@center.T
        if first%102400==0:
            j.update(stage='assembly_'+str(first)+'_of_'+str(nf),max_sample_norm2=norm_sample)
            checkpoint(j)
    j.update(stage='matrix_assembly_completed')
    checkpoint(j)
    # All remaining error algebra is exact rational or directed mp interval.
    pi_low=bridge.lo(mp.iv.pi);R0=F(21,20)
    leading=F(factorial(2*N),2**N*factorial(N)**2)
    epsN=R0*((T*S)**N+F(28,3)*(S/2)**N)/(factorial(N)*leading)
    spatial=U*T/pi_low*(2*R0*epsN+epsN*epsN)
    epsV=[bridge.hi(mp.iv.sqrt(bridge.I(sum((F.from_float(float(e))**2 for e in errs),F(0))))) for errs in row_errors]
    if max(epsV)>=F(1,1000000):raise ValueError('sample vector interval budget too large')
    sample=[U*T/pi_low*(2*(R0+epsN)*e+e*e) for e in epsV]
    if max(R0+epsN+e for e in epsV)>=2:raise ValueError('analytic sample-column norm guard failed')
    # 16 safely dominates squared vector norms. Discarded cells wm=0 are
    # also paid here: their true weight is <=max_weight_error and ideal
    # squared vector norm<4, without sampling any vector for those cells.
    weight_error=16*nf*max_weight_error
    unit=F(1,2**53);gamma=(2*nf+128)*unit/(1-(2*nf+128)*unit)
    # Declared gamma_n dot-product arithmetic model; safe absolute column budget.
    assembly_error=32*gamma*U*T/pi_low
    analytic_budget=r.budgets(radius)
    table_error=F.from_float(radius)+F(35)*H*H/8
    L=F(8)+2*F.from_float(radius)/H
    K1=4*S*S*F(578,1000);K2=4*S**3*(F(448,1000)+F(1,3))
    quadrature=T*h*h/pi_low*(L*K1/12+U*K2/24)
    C0=mp.iv.log(8*mp.iv.pi)+gamma_enclosure()+mp.iv.pi/2
    C=C0+2*sum((mp.iv.log(bridge.I(p))/mp.iv.sqrt(bridge.I(p)) for p in (2,3)),bridge.I(0))
    C_upper=bridge.hi(C)
    records=[]
    final_matrices={}
    for p,M in enumerate(matrices):
        symmetric=(M+M.T)/2
        final_matrices['matrix_even' if p==0 else 'matrix_odd']=symmetric
        sym_error=max(abs(F.from_float(float(symmetric[i,k]))-F.from_float(float(M[i,k]))) for i in range(len(M)) for k in range(len(M)))*len(M)
        cert=r.matrix_congruence_certificate(symmetric,ROOT/('congruence_integrale_even.npy' if p==0 else 'congruence_integrale_odd.npy'))
        total=table_error+quadrature+spatial+sample[p]+weight_error+assembly_error+sym_error
        ceiling=F(cert['tau_fraction'])
        margin=U-C_upper-ceiling-total
        records.append(dict(parity='even' if p==0 else 'odd',matrix_certificate=cert,
            sample_vector_epsilon=str(epsV[p]),sample_operator_error=str(sample[p]),
            sample_operator_error_float=float(sample[p]),symmetrization_error=str(sym_error),
            total_operator_error=str(total),total_operator_error_float=float(total),
            mass_floor_lower=str(margin),mass_floor_lower_float=float(margin)))
    matrix_path=ROOT/'matrices_certificat_integral.npz'
    np.savez_compressed(matrix_path,**final_matrices)
    matrix_hash=hashlib.sha256(matrix_path.read_bytes()).hexdigest()
    floor=min(F(rec['mass_floor_lower']) for rec in records)
    j.update(stage='complete',continuous_positive_certificate=bool(floor>0),
        status='certified_local_all_tests_declared_arithmetic_model' if floor>0 else 'inconclusive',
        support='11/20',N=N,T=str(T),U=str(U),frequency_cells=nf,
        frequency_cells_positive=int(np.sum(wm>0)),
        table_error=str(table_error),table_error_float=float(table_error),
        weighted_quadrature_error=str(quadrature),weighted_quadrature_error_float=float(quadrature),
        spatial_error=str(spatial),spatial_error_float=float(spatial),
        integrated_weight_error=str(weight_error),integrated_weight_error_float=float(weight_error),
        assembly_error=str(assembly_error),assembly_error_float=float(assembly_error),
        C_upper=str(C_upper),C_upper_float=float(C_upper),parities=records,
        final_matrix_file=matrix_path.name,final_matrix_sha256=matrix_hash,
        mass_floor_lower=str(floor),mass_floor_lower_float=float(floor),
        arithmetic_model='outward IEEE binary64 primitives; mpmath intervals; exact integer polynomial signs; declared gamma_n BLAS dot-product enclosure',
        zero_data_used=False,global_RH_claim=False,
        novelty_claim=False,original_post_v649_work_recovered=False,
        duration_seconds=time.monotonic()-begin)
    checkpoint(j)
    (ROOT/'resultats_certificat_integral.json').write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in j.items() if k!='positive_gauss'},indent=2,ensure_ascii=False),flush=True)

if __name__=='__main__':
    try:run()
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc),flush=True)
        raise
