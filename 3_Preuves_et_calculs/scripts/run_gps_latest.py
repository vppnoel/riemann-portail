#!/usr/bin/env python3
from pathlib import Path
import sys, math
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from rh_core import arithmetic_a
from gps_channels import terminal_channel_table

OUT=ROOT/'data'; OUT.mkdir(exist_ok=True)

# Terminal channel comparison
rows=terminal_channel_table(D=100000,Q=1000)
df=pd.DataFrame(rows,columns=['q','H_partial_D','H_terminal','tail_residual','mu_q','phi_q'])
df.to_csv(OUT/'channel_terminal_D100000_Q1000.csv',index=False)

# Aggregated diagnostics by Q using Jordan J2 computed directly.
def J2(q):
    x=q; r=q*q; p=2
    n=x
    pp=2
    f=[]
    d=2
    while d*d<=n:
        if n%d==0:
            f.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:f.append(n)
    for p in f: r*=1-1/(p*p)
    return r

agg=[]
for Q in [10,30,100,300,1000]:
    sub=df.iloc[:Q]
    js=np.array([J2(int(q)) for q in sub.q],dtype=float)
    term=np.sum(js*sub.H_terminal.to_numpy()**2)
    res=np.sum(js*sub.tail_residual.to_numpy()**2)
    part=np.sum(js*sub.H_partial_D.to_numpy()**2)
    agg.append({'D':100000,'Q':Q,'weighted_terminal_energy':term,
                'weighted_tail_residual_energy':res,
                'residual_over_terminal':res/term if term else math.nan,
                'weighted_partial_energy':part})
pd.DataFrame(agg).to_csv(OUT/'channel_terminal_summary.csv',index=False)
print('Wrote channel_terminal_D100000_Q1000.csv and channel_terminal_summary.csv')
