#!/usr/bin/env python3
"""Exploratory common compensation for all active prime powers.

No interval certificate: phase thresholds, quadratures and eigenvalues are
floating point. Same moment Gram projects every frequency and source column.
Unitary Fourier; projected parity concentration factor is 1/pi.
"""
import json,time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import digamma

C0=np.log(8*np.pi)+np.euler_gamma+np.pi/2
SUPPORTS=[('11/20',.55),('3/5',.6),('7/10',.7)]
CONFIGURATIONS=[(9.,300.,[(160,30000),(256,60000)]),
                (9.5,400.,[(224,40000),(320,80000)]),
                (10.,700.,[(384,50000),(512,100000)])]

def active_powers(S):
    return [(p,m,v) for p,m,v in [(2,1,2),(3,1,3),(2,2,4)]
            if np.log(v)<2*S]

def run(S,U,T,N,n,split=False):
    begin=time.monotonic();powers=active_powers(S);count=len(powers)
    roots,weights=leggauss(N);x=roots[N//2:]*S;wx=weights[N//2:]*S;sw=np.sqrt(2*wx)
    t=(np.arange(n)+.5)*T/n;a=np.real(digamma(.25+1j*t/2))-digamma(.25)
    oscillations=[2*np.log(p)/np.sqrt(v)*(1-np.cos(t*np.log(v))) for p,m,v in powers]
    b=a+sum(oscillations);phi=np.maximum(0,U-b)
    C=C0+2*sum(np.log(p)/np.sqrt(v) for p,m,v in powers)
    records=[]
    for parity in [0,1]:
        q=sw*(np.cosh(x/2) if parity==0 else np.sinh(x/2));Gram=float(q@q)
        B=np.zeros((N//2,N//2));parts=[np.zeros_like(B) for _ in powers] if split else []
        for start in range(0,n,2048):
            tt=t[start:start+2048]
            columns=sw[:,None]*(np.cos(x[:,None]*tt) if parity==0 else np.sin(x[:,None]*tt))
            columns-=q[:,None]*(q@columns)[None,:]/Gram
            common=columns*np.sqrt(phi[start:start+2048]*T/n/np.pi)
            B+=common@common.T
            if split:
                for j,osc in enumerate(oscillations):
                    phij=np.maximum(0,(U-a[start:start+2048])/count-osc[start:start+2048])
                    part=columns*np.sqrt(phij*T/n/np.pi);parts[j]+=part@part.T
        eigen=np.linalg.eigvalsh(B);assert eigen[0]>-1e-10
        record=dict(parity='even' if parity==0 else 'odd',norm=float(eigen[-1]),
                    second_eigenvalue=float(eigen[-2]),trace=float(np.trace(B)),
                    schatten2=float(np.linalg.norm(B)),
                    margin=U-C-float(eigen[-1]),moment_gram=Gram)
        if split:
            total=sum(parts);norms=[float(np.linalg.eigvalsh(M)[-1]) for M in parts]
            summed_norm=float(np.linalg.eigvalsh(total)[-1])
            assert np.linalg.eigvalsh(total-B)[0]>-1e-9
            record['split_comparison']=dict(energy_shares='equal a/count and cap U/count',
                compensation_norms=norms,sum_of_norms=sum(norms),
                norm_of_sum=summed_norm,
                norm_of_sum_margin=U-C-summed_norm,
                sum_of_norms_margin=U-C-sum(norms),
                explanation='sum of positive parts dominates positive part of sum; shared head also avoids separate maximizers')
        records.append(record)
    return dict(U=U,Tmax=T,spatial_nodes=N,frequency_nodes=n,
                duration_seconds=time.monotonic()-begin,C_constant=C,
                point_a_Tmax=float(np.real(digamma(.25+1j*T/2))-digamma(.25)),
                parity=records,margin=min(r['margin'] for r in records))

def main():
    supports=[]
    for label,S in SUPPORTS:
        cases=[]
        for U,T,configs in CONFIGURATIONS:
            records=[run(S,U,T,N,n,split=(U==9 and j==1)) for j,(N,n) in enumerate(configs)]
            cases.append(dict(U=U,resolutions=records,
                refinement_margin_difference=records[1]['margin']-records[0]['margin']))
            print(label,'U',U,'margins',[r['margin'] for r in records[-1]['parity']],
                  'stability only',cases[-1]['refinement_margin_difference'])
        powers=[dict(p=p,m=m,n=v,phase=np.log(v),weight=np.log(p)/np.sqrt(v),
                     distance_from_threshold=2*S-np.log(v)) for p,m,v in active_powers(S)]
        supports.append(dict(S=label,active_prime_powers=powers,cases=cases))
    result=dict(version='V6.49',scope='exploratory multi-prime common compensation diagnostic',
        certified=False,new_positive_certificate=False,global_RH_claim=False,
        zero_data_used=False,chosen_after_exploration=True,
        exact_identity='b_S=a+2 sum_(p,m) (log(p)/sqrt(p^m))(1-cos(m log(p)t)); C_S=C0+2 sum weights; Q=integral(b_S-C_S)|fhat|^2',
        normalization='unitary Fourier; same moment projection and 1/pi in both parities',
        invariants=['phase of p^m is m log p','weight is log p / p^(m/2), not log(p^m)/p^(m/2)',
                    'moment Gram diag(S+sinh S,sinh S-S) is shared by all powers',
                    'changing the truncation cap does not change the original form'],
        limitations=['no outward intervals','no proven spatial or frequency quadrature error',
                    'point tail check is not an interval proof','Nystrom eigenvalues are not infinite operator upper bounds',
                    'refinement agreement describes stability only','support thresholds were classified in floating point'],
        supports=supports)
    target=Path(__file__).resolve().parents[1]/'data/v649_multi_prime_diagnostic.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert not any(result[k] for k in ['certified','new_positive_certificate','global_RH_claim'])
    print('discrete PSD/split-Loewner checks and exploratory guards passed;',target.name)

if __name__=='__main__':main()
