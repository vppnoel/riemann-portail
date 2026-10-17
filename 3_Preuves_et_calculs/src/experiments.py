"""Numerical experiments used in the consolidated RH programme."""
from __future__ import annotations

import math
import numpy as np
import pandas as pd

from rh_core import (
    EULER_GAMMA, KAPPA, arithmetic_a, arithmetic_c_via_a,
    arithmetic_c_via_lambda, C_partial, Q_truncated, H_eta_truncated,
    diagonal_proxy, kappa_reference_Q, mobius_sieve, sawtooth_covariance_exact,
    scalar_projection_step,
)


def verify_c_identity(N: int = 20000) -> pd.DataFrame:
    c1 = arithmetic_c_via_lambda(N)
    c2 = arithmetic_c_via_a(N)
    err = np.abs(c1-c2)
    return pd.DataFrame([{
        "N": N,
        "max_abs_error": float(err.max()),
        "l2_error": float(np.linalg.norm(err)),
    }])


def apollo_trajectory(maxN: int = 200000) -> pd.DataFrame:
    c = arithmetic_c_via_lambda(maxN)
    C = C_partial(c)
    Xs = [100, 300, 1000, 3000, 10000, 30000, 100000, 200000]
    Xs = [x for x in Xs if x <= maxN]
    rows = []
    prev = None
    for X in Xs:
        q = Q_truncated(C, X)
        ref = kappa_reference_Q(X)
        row = {
            "X": X,
            "Q_measured": q,
            "Q_reference_log3": ref,
            "ratio": q/ref,
            "logQ_over_logX": math.log(q)/math.log(X),
        }
        if prev is not None:
            x0,q0 = prev
            row["local_slope"] = (math.log(q)-math.log(q0))/(math.log(X)-math.log(x0))
            row["reference_slope_mid"] = 3.0/math.log(math.sqrt(x0*X))
        rows.append(row)
        prev=(X,q)
    return pd.DataFrame(rows)


def weighted_energy_vs_diagonal(maxN: int = 200000) -> pd.DataFrame:
    c = arithmetic_c_via_lambda(maxN)
    C = C_partial(c)
    rows=[]
    for X in [1000, 3000, 10000, 30000, 100000, 200000]:
        if X>maxN: continue
        for eta in [0.05,0.10,0.20,0.30,0.50]:
            H=H_eta_truncated(C,eta,X)
            D=diagonal_proxy(c,eta,X)
            rows.append({"X":X,"eta":eta,"H_X":H,"diag_proxy":D,
                         "H_over_diag":H/D,"eta3_H":eta**3*H})
    return pd.DataFrame(rows)


def local_fourier_energy(Ns=(256,512,1024,2048,4096,8192), oversample: int=16) -> pd.DataFrame:
    rows=[]
    for N in Ns:
        mu=mobius_sieve(2*N).astype(float)
        a=mu[N+1:2*N+1]
        M=oversample*N
        z=np.zeros(M)
        z[:N]=a
        F=np.fft.fft(z)
        power=np.abs(F)**2
        total=np.sum(a*a)
        w=oversample # frequency width 1/N
        p2=np.r_[power,power[:w-1]]
        roll=np.convolve(p2,np.ones(w),mode='valid')[:M]/M
        expected=total/N
        ratio=roll/expected
        rows.append({"N":N,"squarefree_energy":total,
                     "expected_width_1_over_N":expected,
                     "mean_ratio":float(np.mean(ratio)),
                     "p95_ratio":float(np.quantile(ratio,.95)),
                     "p99_ratio":float(np.quantile(ratio,.99)),
                     "max_ratio":float(np.max(ratio))})
    return pd.DataFrame(rows)


def saw_band_values(xs: np.ndarray, lo: int, hi: int, a: np.ndarray) -> np.ndarray:
    out=np.zeros_like(xs,dtype=float)
    for d in range(lo+1,hi+1):
        if a[d]!=0:
            u=xs/d
            out += a[d]*(u-np.floor(u)-0.5)
    return out


def gcd_covariance_validation(X: int=200000) -> pd.DataFrame:
    bands=[(20,40),(40,80),(80,160),(160,320)]
    a=arithmetic_a(max(b[1] for b in bands))
    xs=np.arange(X,2*X,dtype=float)+0.37
    vals=[saw_band_values(xs,*b,a) for b in bands]
    rows=[]
    for i,b1 in enumerate(bands):
        for j,b2 in enumerate(bands):
            if j<i: continue
            measured=float(np.mean(vals[i]*vals[j]))
            pred=0.0
            for d in range(b1[0]+1,b1[1]+1):
                if a[d]==0: continue
                for e in range(b2[0]+1,b2[1]+1):
                    if a[e]==0: continue
                    pred += a[d]*a[e]*sawtooth_covariance_exact(d,e)
            rows.append({"band_i":str(b1),"band_j":str(b2),"measured":measured,
                         "gcd_prediction":pred,
                         "relative_error":(measured-pred)/(abs(pred)+1e-30)})
    return pd.DataFrame(rows)


def predictor_G(X: int, D: int, a: np.ndarray) -> np.ndarray:
    """Finite low-divisor predictor used in the multiscale diagnostic."""
    N=2*X
    b=np.zeros(N+1)
    for d in range(1,D+1):
        ad=a[d]
        if ad!=0:
            b[d::d]+=ad
    floor_sum=np.cumsum(b)
    s1=np.sum(a[1:D+1]/np.arange(1,D+1))
    AD=np.sum(a[1:D+1])
    xs=np.arange(X,2*X+1,dtype=float)
    fs=floor_sum[X:2*X+1]
    return -xs*s1+fs+AD*(xs/D-np.floor(xs/D))


def kalman_information(Xs=(5000,10000,20000,50000), ratio=1.2, dmax_exp=.95) -> pd.DataFrame:
    rows=[]
    for X in Xs:
        c=arithmetic_c_via_lambda(2*X)
        C=C_partial(c)
        a=arithmetic_a(2*X)
        xs=np.arange(X,2*X+1,dtype=float)
        target=C[X:2*X+1]
        weights=1/xs**2
        D0=max(2,int(round(X**.5)))
        Dmax=min(X,int(round(X**dmax_exp)))
        Ds=[D0]
        while Ds[-1]<Dmax:
            nd=max(Ds[-1]+1,int(round(Ds[-1]*ratio)))
            if nd>Dmax: nd=Dmax
            Ds.append(nd)
            if nd==Dmax: break
        Gs=[predictor_G(X,D,a) for D in Ds]
        residual=target-Gs[0]
        var0=float(np.sum(weights*residual**2))
        info=0.0
        for j in range(len(Ds)-1):
            innovation=Gs[j+1]-Gs[j]
            residual, step=scalar_projection_step(residual,innovation,weights)
            rho2=min(step.rho*step.rho,1-1e-15)
            info += -math.log(1-rho2)
        varf=float(np.sum(weights*residual**2))
        rows.append({"X":X,"logX":math.log(X),"n_updates":len(Ds)-1,
                     "information":info,"info_per_logX":info/math.log(X),
                     "initial_variance":var0,"final_variance":varf,
                     "variance_ratio":varf/var0})
    return pd.DataFrame(rows)
