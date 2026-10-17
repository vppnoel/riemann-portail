#!/usr/bin/env python3
"""NEW reconstruction after V6.49, not recovery of a missing original.

Proved analytic budgets, outward binary64 table and optional exploratory
matrix with a validated bound on that EXACT dyadic matrix only.
This program does not certify the original continuous operator.
"""
import argparse
from fractions import Fraction as F
from math import factorial, ceil
from pathlib import Path
import json
import hashlib
import time
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import cholesky, solve_triangular
import mpmath as mp

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 100
mp.iv.prec = 300


def down(x):
    return np.nextafter(x, -np.inf)


def up(x):
    return np.nextafter(x, np.inf)


def qiv(x):
    x = F(x)
    z = float(x)
    zq = F.from_float(z)
    return (down(z) if zq > x else z, up(z) if zq < x else z)


def ivq(x):
    x = F(x)
    return mp.iv.mpf(x.numerator) / x.denominator


def endq(x):
    sign, man, exp, bc = x
    if bc < 0:
        raise ValueError("finite endpoint required")
    return F((-1 if sign else 1) * man) * F(2)**exp


def mp_bounds(x):
    return endq(x._mpi_[0]), endq(x._mpi_[1])


def iv_to_float(x):
    a, b = mp_bounds(x)
    return qiv(a)[0], qiv(b)[1]


def plus(x, y):
    return down(x[0] + y[0]), up(x[1] + y[1])


def minus(x, y):
    return plus(x, (-y[1], -y[0]))


def times(x, y):
    vals = (x[0]*y[0], x[0]*y[1], x[1]*y[0], x[1]*y[1])
    return down(np.minimum.reduce(vals)), up(np.maximum.reduce(vals))


def over(x, y):
    if np.any(np.asarray(y[0]) <= 0):
        raise ValueError("strictly positive denominator required")
    return times(x, (down(1/y[1]), up(1/y[0])))


def horner(coefs, z):
    r = qiv(coefs[-1])
    for c in coefs[-2::-1]:
        r = plus(times(r, z), qiv(c))
    return r


def cos_iv(z):
    """|z|<=800; degree20 Taylor after /2048; 11 angle doublings."""
    if np.any(np.asarray(z[0]) < -800) or np.any(np.asarray(z[1]) > 800):
        raise ValueError("phase domain exceeded")
    v = times(z, qiv(F(1, 2048)))
    c = horner([F((-1)**k, factorial(2*k)) for k in range(11)], times(v, v))
    # |v|<1, so remainder <=1/22!; it remains inside every doubling.
    e = qiv(F(1, factorial(22)))[1]
    c = plus(c, (-e, e))
    for _ in range(11):
        c = minus(times(qiv(2), times(c, c)), qiv(1))
    return c


def log_positive_iv(z, count=80):
    """0<=log(z), 1<=z<=3; atanh series and positive remainder."""
    if np.any(np.asarray(z[0]) < 1-1e-14) or np.any(np.asarray(z[1]) > 3):
        raise ValueError("log domain exceeded")
    # Outward roundoff may make a zero numerator slightly negative; include
    # it normally in the polynomial, and bound remainder by |y| below.
    y = over(minus(z, qiv(1)), plus(z, qiv(1)))
    yy = times(y, y)
    term = y
    s = qiv(0)
    for k in range(count):
        s = plus(s, times(term, qiv(F(2, 2*k+1))))
        term = times(term, yy)
    abs_y = up(np.maximum(np.abs(y[0]), np.abs(y[1])))
    if np.any(abs_y>F(1,2)):
        raise ValueError("atanh series remainder domain exceeded")
    rem = qiv(F(8,3)*F(1,2)**(2*count+1)/F(2*count+1))[1]
    return plus(s, (-rem, rem))


def arch_table_iv(t, K=256):
    """Analytic coth tail bracket, evaluated outward on exact-rational t."""
    tt = times(t, t)
    total = qiv(0)
    for n in range(K):
        bn = F(4*n+1, 2)
        total = plus(total, over(times(qiv(2), tt), times(qiv(bn), plus(qiv(bn*bn), tt))))
    B = F(4*K+1, 2)
    integral = times(qiv(F(1, 2)), log_positive_iv(plus(qiv(1), over(tt, qiv(B*B)))))
    f = over(times(qiv(2), tt), times(qiv(B), plus(qiv(B*B), tt)))
    # -f'(B)/6 = t²(3B²+t²) / [3B²(B²+t²)²].
    df = over(times(tt, plus(qiv(3*B*B), tt)),
              times(qiv(3*B*B), times(plus(qiv(B*B), tt), plus(qiv(B*B), tt))))
    upper_tail = plus(plus(integral, times(qiv(F(1, 2)), f)), df)
    correction = qiv(F(4, 15)/B**4)[1]
    return plus(total, (down(upper_tail[0]-correction), upper_tail[1]))


def build_table(S=F(11,20), T=F(700), H=F(1,200), K=256):
    if T/H != int(T/H):
        raise ValueError("exact divisible grid required")
    j = np.arange(int(T/H)+1, dtype=np.float64)
    t = times((j,j), qiv(H))
    a = arch_table_iv(t,K)
    b = a
    for p in (2,3):
        d = mp.iv.log(ivq(p))
        c = d/mp.iv.sqrt(ivq(p))
        phase = cos_iv(times(t, iv_to_float(d)))
        b = plus(b, times(iv_to_float(2*c), minus(qiv(1),phase)))
    mid = np.maximum(0,b[0]/2+b[1]/2)
    radius = up(np.maximum(np.abs(mid-b[0]),np.abs(b[1]-mid)))
    return mid, float(np.max(radius)), {
        "table_points":len(mid), "K":K,
        "max_outward_radius":float(np.max(radius)),
        "tail_width_analytic":str(F(4,15)/F(4*K+1,2)**4),
        "binary64_arithmetic_model":"outward nextafter primitives; elementary interval Taylor/log series",
        "a_T_interval": [float(a[0][-1]),float(a[1][-1])],
        "a_T_above_U_certified":bool(a[0][-1]>10)
    }


def integrated_positive_weights(table, U=10., T=700., H=.005, h=.001):
    """Exact formula; floating evaluation here remains exploratory."""
    n = round(T/h)
    i = np.arange(n)
    ratio = round(H/h)
    k = i//ratio
    frac = (i % ratio)/ratio
    g0 = U-((1-frac)*table[k]+frac*table[k+1])
    f1 = frac+1/ratio
    g1 = U-((1-f1)*table[k]+f1*table[k+1])
    positive = (g0>0) & (g1>0)
    w = np.zeros(n)
    w[positive] = .5*h*(g0[positive]+g1[positive])
    left = (g0>0) & (g1<=0)
    right = (g0<=0) & (g1>0)
    w[left] = .5*h*g0[left]**2/(g0[left]-g1[left])
    w[right] = .5*h*g1[right]**2/(g1[right]-g0[right])
    if np.any(w<0) or np.any(w>h*U*(1+1e-12)):
        raise ValueError("positive weight bound failed")
    return w, dict(kink_cells=int(np.sum(left|right)),
                  weight_sum=float(w.sum()),
                  classification="floating evaluation of exact positive-linear-cell integral")


def matrix_congruence_certificate(M,save_congruence=None):
    """Certifies ceiling for EXACT binary64 M, not its continuous parent."""
    n = len(M)
    if np.any(M!=M.T):
        raise ValueError("exactly symmetric binary64 input matrix required")
    eig = float(np.linalg.eigvalsh(M)[-1])
    tau = F(ceil((eig+F(1,100000))*2**24),2**24)
    A = float(tau)*np.eye(n)-M
    L = cholesky(A,lower=True)
    C = solve_triangular(L,np.eye(n),lower=True)
    if not np.all(np.isfinite(C)) or np.any(np.diag(C)==0) or np.any(np.triu(C,1)!=0):
        raise ValueError("exact dyadic congruence matrix must be triangular/invertible")
    alo,ahi = down(A),up(A)
    # Explicit interval dot products. No BLAS rounding bound enters the proof.
    def left_product_exact_float(C,X):
        lo=np.zeros((n,n));hi=np.zeros((n,n))
        for k in range(n):
            c=C[:,k,None]
            p0=c*X[0][k,None,:];p1=c*X[1][k,None,:]
            lo=down(lo+down(np.minimum(p0,p1)))
            hi=up(hi+up(np.maximum(p0,p1)))
        return lo,hi
    X=left_product_exact_float(C,(alo,ahi))
    # (C A C^T)^T = C (C A)^T, and enclosure handles symmetry safely.
    R=left_product_exact_float(C,(X[0].T,X[1].T))
    diag_lower=np.diag(R[0]).copy()
    off_abs=up(np.maximum(np.abs(R[0]),np.abs(R[1])))
    np.fill_diagonal(off_abs,0)
    rows=np.zeros(n)
    for k in range(n):
        rows=up(rows+off_abs[:,k])
    floors=down(diag_lower-rows)
    if np.min(floors)<=0:
        raise ValueError("congruence Gershgorin positivity not established")
    result=dict(tau_fraction=str(tau),tau_float=float(tau),
        floating_eigenvalue=eig,congruence_dimension=n,
        congruence_gershgorin_floor=float(np.min(floors)),
        classification="validated ceiling for exact dyadic finite matrix under declared IEEE model",
        continuous_operator_certified=False,
        proof="C exact dyadic lower triangular, nonzero diagonal. Outward C(tau I-M)C^T strictly diagonally dominant with positive diagonal => tau I-M positive definite.")
    if save_congruence is not None:
        path=Path(save_congruence)
        np.save(path,C)
        result['congruence_matrix_file']=path.name
        result['congruence_matrix_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def interpolation_budget(N, S=F(11,20), T=F(700)):
    leading = F(factorial(2*N),2**N*factorial(N)**2)
    main = (T*S)**N/(factorial(N)*leading)
    gmin = mp.sinh(mp.mpf(S.numerator)/S.denominator)-mp.mpf(S.numerator)/S.denominator
    coefficient = mp.sqrt(2*mp.mpf(S.numerator)/S.denominator/gmin)
    exp_factor = coefficient*mp.exp(mp.mpf(S.numerator)/(2*S.denominator))
    extra = mp.mpf(str((S/2)**N/(factorial(N)*leading).numerator))/mp.mpf(str((S/2)**N/(factorial(N)*leading).denominator))*exp_factor
    mainmp=mp.mpf(main.numerator)/main.denominator
    eps=mp.sqrt(2*mp.mpf(S.numerator)/S.denominator)*(mainmp+extra)
    # Exact rational sufficient bound at S=11/20: sqrt(2S)<21/20,
    # sqrt(2S/(sinhS-S))<7 and exp(S/2)<4/3.
    if S==F(11,20):
        exact_eps=F(21,20)*((T*S)**N+F(28,3)*(S/2)**N)/(factorial(N)*leading)
    else:
        exact_eps=None
    return dict(N=N,lagrange_pointwise_main=str(float(main)),
        moment_projection_coefficient=str(coefficient),
        L2_epsilon=str(eps),L2_epsilon_exact_rational_upper=str(exact_eps),
        classification="exact rational wave term; high precision displayed moment-factor estimate")


def budgets(table_radius=0., S=F(11,20),T=F(700),U=F(10),H=F(1,200),h=F(1,1000)):
    # Rational bounds 1/sqrt(3)<.578 and 1/sqrt(5)<.448.
    assert F(578,1000)**2*3>1 and F(448,1000)**2*5>1
    K1 = 4*S*S*F(578,1000)
    K2 = 4*S**3*(F(448,1000)+F(1,3))
    L=F(8)+2*F.from_float(table_radius)/H
    B2=F(35); pi_lower=F(3141592653589793,10**15)
    assert pi_lower<mp_bounds(mp.iv.pi)[0]
    tailwidth=F(4,15)/F(1025,2)**4
    table=F.from_float(table_radius)+B2*H*H/8
    weighted=T*h*h/pi_lower*(L*K1/12+U*K2/24)
    total=table+weighted
    return dict(S=str(S),U=str(U),T=str(T),H=str(H),h=str(h),
        b_prime_upper=str(L),b_second_upper=str(B2),K_prime_norm_upper=str(K1),K_second_norm_upper=str(K2),
        table_interpolation_error_fraction=str(B2*H*H/8),
        weighted_midpoint_error_fraction=str(weighted),
        table_interpolation_error=float(table),weighted_midpoint_error=float(weighted),
        combined_analytic_and_table_budget=float(total),
        exploratory_margin_649=0.0005830255155219177,
        budget_below_exploratory_margin=bool(float(total)<0.0005830255155219177),
        remaining_budget_vs_old_exploratory_margin=0.0005830255155219177-float(total),
        missing_certificate_components=["exact Gauss nodes/weights and sample vector intervals at N640",
            "correct projected moment Gram and numerical evaluation bounds",
            "outward integrated cell weights and matrix assembly errors",
            "combined outward finite-matrix + continuous-operator final inequality"],
        continuous_operator_certified=False)


def diagnostic(table):
    S=.55;T=700.;h=.001;N=640
    w,weight_details=integrated_positive_weights(table)
    roots,gweights=leggauss(N)
    x=S*roots[N//2:]
    sw=np.sqrt(2*S*gweights[N//2:])
    t=(np.arange(len(w))+.5)*h
    C0=np.log(8*np.pi)+np.euler_gamma+np.pi/2
    C=C0+2*(np.log(2)/np.sqrt(2)+np.log(3)/np.sqrt(3))
    records=[]
    arrays={}
    for parity in (0,1):
        q=sw*(np.cosh(x/2) if parity==0 else np.sinh(x/2))
        Gram=float(q@q)
        matrix=np.zeros((N//2,N//2))
        for first in range(0,len(w),4096):
            if not np.any(w[first:first+4096]):
                continue
            ts=t[first:first+4096]
            columns=sw[:,None]*(np.cos(x[:,None]*ts) if parity==0 else np.sin(x[:,None]*ts))
            columns-=q[:,None]*(q@columns)[None,:]/Gram
            scaled=columns*np.sqrt(w[first:first+4096]/np.pi)
            matrix+=scaled@scaled.T
        matrix=(matrix+matrix.T)/2
        cert=matrix_congruence_certificate(matrix)
        arrays['matrix_even' if parity==0 else 'matrix_odd']=matrix
        records.append(dict(parity='even' if parity==0 else 'odd',
            floating_point_margin=10-C-cert['floating_eigenvalue'],
            exact_dyadic_matrix_ceiling=cert, moment_gram_float=Gram))
    np.savez_compressed(ROOT/'matrices_exploratoires.npz',**arrays)
    return dict(N=N,frequency_cells=len(w),weights=weight_details,
        C_float=C,parities=records,
        classification="new floating reconstruction; finite dyadic matrices have validated ceilings; full continuous operator remains uncertified")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--diagnostic',action='store_true')
    parser.add_argument('--skip-table',action='store_true')
    args=parser.parse_args()
    begin=time.monotonic()
    table=None
    if not args.skip_table:
        table,radius,details=build_table()
    else:
        radius=0.;details={"not_evaluated":True}
    j=dict(version="V6.50 new reconstruction",original_post_v649_work_recovered=False,
        recovered_source="V6.49 corpus",continuous_positive_certificate=False,global_RH_claim=False,
        interpolation=[interpolation_budget(N) for N in (512,640)],
        table=details,budgets=budgets(radius))
    if args.diagnostic:
        if table is None:
            raise ValueError("diagnostic requires table")
        j['diagnostic']=diagnostic(table)
    j['duration_seconds']=time.monotonic()-begin
    out=ROOT/'resultats_reconstruction.json'
    out.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(j,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
