"""V6.60, document de travail RECOLLER_LES_MORCEAUX_V6_60.md : niveau 0 de l'échelle (Tchebychev, C(2n, n)).
Prévision : data/prevision_v660_echelle.md. Résultat : data/resultat_v660_niveau0.txt."""
import math, sys
N=200_000; M=2*N
sieve=bytearray([1])*(M+1); sieve[0]=sieve[1]=0
for i in range(2,int(M**.5)+1):
    if sieve[i]: sieve[i*i::i]=bytearray(len(range(i*i,M+1,i)))
theta=[0.0]*(M+1); s=0.0
for k in range(M+1):
    if sieve[k]: s+=math.log(k)
    theta[k]=s
lg=lambda n: math.lgamma(2*n+1)-2*math.lgamma(n+1)
viol=sum(1 for n in range(1,N+1) if theta[2*n]-theta[n] > lg(n)+1e-9)
print("P1 exceptions:", viol, "; max (log C)/(2n log2) =", max(lg(n)/(2*n*math.log(2)) for n in range(1,N+1)))
print("P2 max theta(x)/x for x in [100, 400000]:", round(max(theta[x]/x for x in range(100,M+1)),4), "; bound 2log2 =", round(2*math.log(2),4))
for n in (10_000, 50_000, 100_000, 200_000):
    g=lg(n)-(theta[2*n]-theta[n]); print(f"P3 n={n}: gaspillage/n = {g/n:.4f} ; gaspillage/sqrt(n) = {g/math.sqrt(n):.1f}")
