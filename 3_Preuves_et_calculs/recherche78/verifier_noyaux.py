"""Relecture numérique indépendante des noyaux exportés, pas certificat global.

Reconstruit les moments depuis A et A' fermés, sans importer le balayage.
Les positions sont des décimales approchées : les contrôles utilisent une
tolérance explicitement déclarée et ne certifient pas ces lignes par intervalles.
"""
from pathlib import Path
import argparse
import json
import mpmath as mp


def verify(path, summary_path):
    mp.mp.dps=75
    kernels=json.loads(Path(path).read_text())
    summary=json.loads(Path(summary_path).read_text())
    T=mp.log(2)
    C0=mp.log(8*mp.pi)+mp.euler+mp.pi/2
    total=mp.pi**2/4+2*mp.catalan
    def A(t):
        z=mp.exp(-2*t)
        value=mp.mpf(0)
        for n in reversed(range(180)):
            value=value*z+1/(2*n+mp.mpf(".5"))**2
        return 4*(mp.exp(t/2)+mp.exp(-t/2)-2)-C0*t/2+total-mp.exp(-t/2)*value
    def Ap(t):
        z=mp.exp(-t/2)
        return 2*(mp.exp(t/2)-mp.exp(-t/2))-C0/2+mp.atanh(z)+mp.atan(z)
    def beta(t):
        return mp.exp(t/2)-mp.exp(-mp.mpf("2.5")*t)/(1-mp.exp(-2*t))
    m=A(T)/T
    a=Ap(T)-T/mp.sqrt(2)
    U=mp.mpf(summary["U"])
    bound=m+Ap(U)-Ap(T)
    cache={}
    tolerance=mp.mpf("1e-38")
    def J(s):
        if s<=m+mp.mpf("1e-56"):
            return mp.mpf(0)
        key=str(s)
        if key not in cache:
            guess=max(T,2*mp.log(s/2+mp.sqrt(2)))
            u=mp.findroot(lambda v:m+Ap(v)-Ap(T)-s,guess,
                          df=beta,tol=mp.mpf("1e-65"),maxsteps=80)
            cache[key]=u*Ap(u)-A(u)-T*Ap(T)+A(T)
        return cache[key]
    max_mass=max_moment=mp.mpf(0)
    pieces=[]
    cutoff=int(summary["cutoff"])
    labels=[]
    for row in kernels:
        c=mp.mpf(row["c"]);x=mp.mpf(row["x"])
        intervals=[(mp.mpf(l),mp.mpf(r)) for l,r in row["source_mass_intervals"]]
        assert intervals and all(-tolerance<=l<r<=bound+tolerance for l,r in intervals)
        actual_mass=sum(r-l for l,r in intervals)
        actual_moment=sum(J(r)-J(l) for l,r in intervals)
        max_mass=max(max_mass,abs(actual_mass-c))
        max_moment=max(max_moment,abs(actual_moment-c*x))
        label=row["atom"];labels.append(label)
        if label in ("T","raccord_T"):
            assert abs(c-(m-a))<tolerance and abs(x-T)<tolerance
        elif label=="boundary":
            assert abs(x-mp.log(cutoff))<tolerance
        else:
            q=int(label)
            assert q>2 and q<=cutoff and abs(x-mp.log(q))<tolerance
            p=next(p for p in range(2,q+1) if q%p==0)
            remainder=q
            while remainder%p==0:
                remainder//=p
            assert remainder==1
            assert abs(c-mp.log(p)/mp.sqrt(q))<tolerance
        pieces.extend(intervals)
    pieces.sort()
    max_partition=max(abs(pieces[0][0]),abs(pieces[-1][1]-bound))
    for (_,right),(left,_) in zip(pieces,pieces[1:]):
        max_partition=max(max_partition,abs(left-right))
    assert max_mass<tolerance and max_moment<tolerance and max_partition<tolerance
    assert labels.count("boundary")==1
    return dict(all_checks_passed=True,kernel_file=Path(path).name,cutoff=cutoff,
                row_count=len(kernels),checked_initial_raccord=True,
                checked_arithmetic_weights=True,checked_positive_source_pieces=True,
                max_mass_error=str(max_mass),max_moment_error=str(max_moment),
                max_partition_gap_or_overlap=str(max_partition),
                independent_formulas="closed A_prime; Horner A with 180 terms; quantile inversion from original measure",
                working_digits=75,declared_tolerance=str(tolerance),
                interval_certificate=False,global_RH_claim=False)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--kernels",type=Path,required=True)
    ap.add_argument("--summary",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    result=verify(args.kernels,args.summary)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
