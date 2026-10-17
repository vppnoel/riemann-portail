from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from dark_residual import compression_components
from dual_lock import compression_accurate, KINDS
from dual_lock_audit import generalized_decomposition, compression_components_independent

DATA=ROOT/'data'; DATA.mkdir(parents=True,exist_ok=True)
CASES=[(86.0,2.5),(113.0,2.5),(167.0,3.5),(176.0,2.5)]

def gram_from_components(comp, kind):
    return np.asarray(comp['conductor'],float)/math.log(KINDS[kind].q/math.pi)

def write_csv(path, rows):
    with path.open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)

def main(full=False):
    canonical=[]
    for T,w in CASES:
        for kind in ('DH','L_pair_chi5'):
            _,comp=compression_components(T,kind,half_width=w,dimension=7,frequency_step=0.6,arch_dt=0.02,correlation_eps=2e-8)
            G=gram_from_components(comp,kind)
            gm,_,_=generalized_decomposition(comp,G)
            _,M0=compression_accurate(T,kind,half_width=w,dimension=7,frequency_step=0.6,arch_dt=0.02,correlation_eps=2e-8)
            canonical.append({'center':T,'half_width':w,'dimension':7,'kind':kind,
                              'matrix_reconcile_maxabs':float(np.max(np.abs(M0-comp['total']))),**gm})
    write_csv(DATA/'dual_lock_audit_canonical.csv',canonical)

    dims=[]
    for T,w in CASES:
        dim_list=(3,5,7,9,11) if full else (3,5,7)
        for m in dim_list:
            for kind in ('DH','L_pair_chi5'):
                _,comp=compression_components(T,kind,half_width=w,dimension=m,frequency_step=0.6,arch_dt=0.02,correlation_eps=2e-8)
                gm,_,_=generalized_decomposition(comp,gram_from_components(comp,kind))
                dims.append({'center':T,'half_width':w,'dimension':m,'kind':kind,**gm})
    write_csv(DATA/'dual_lock_audit_dimension_runtime.csv',dims)

    quad=[]
    for dt in (0.04,0.02,0.01):
        for eps in (5e-7,1e-7,2e-8):
            for kind in ('DH','L_pair_chi5'):
                _,comp=compression_components(86.0,kind,half_width=2.5,dimension=5,frequency_step=0.6,arch_dt=dt,correlation_eps=eps)
                gm,_,_=generalized_decomposition(comp,gram_from_components(comp,kind))
                quad.append({'center':86.0,'half_width':2.5,'dimension':5,'arch_dt':dt,'correlation_eps':eps,'kind':kind,**gm})
    write_csv(DATA/'dual_lock_audit_quadrature.csv',quad)

    independent_cases=[(86.0,2.5,5),(176.0,2.5,7)]
    if full:
        independent_cases += [(86.0,2.5,7),(167.0,3.5,7)]
    ind=[]
    for T,w,m in independent_cases:
        for kind in ('DH','L_pair_chi5'):
            _,comp,G=compression_components_independent(T,kind,half_width=w,dimension=m,frequency_step=0.6,gl_order=256)
            gm,_,_=generalized_decomposition(comp,G)
            ind.append({'center':T,'half_width':w,'dimension':m,'kind':kind,'method':'composite_GL_arch+GL256_local',**gm})
    write_csv(DATA/'dual_lock_audit_independent_runtime.csv',ind)

    summary={'status':'V6.3a instrument audit','full':bool(full),'construction_uses_zeros':False,
             'canonical':canonical,'dimension_sweep':dims,'quadrature_sweep':quad,'independent':ind,
             'decision':'Use Mv=lambda Gv; high-dimension magnitudes require tolerance scaled to Gram conditioning.'}
    (DATA/'dual_lock_audit_summary_runtime.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps({'canonical':canonical,'independent':ind},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--full',action='store_true',help='run expensive high-dimension / extra independent checks')
    args=ap.parse_args()
    main(full=args.full)
