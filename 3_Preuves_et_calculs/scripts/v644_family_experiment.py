"""Execute the prospectively frozen arithmetic-family experiment (no zero data)."""
from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import symbolic_weil_family as w
D=ROOT/'3_Preuves_et_calculs/data'
def strings(M):return [[mp.nstr(M[i,j],mp.mp.dps) for j in range(M.cols)] for i in range(M.rows)]
def maxdiff(A,B):return max(abs(A[i,j]-B[i,j]) for i in range(A.rows) for j in range(A.cols))
def symbolic_checks(S,n):
    for k in range(n):
        for d in range(4):
            assert w.evalq(w.derivative(w.seed(k),d),1)==w.evalq(w.derivative(w.seed(k),d),-1)==0
        for d in range(2):
            assert w.evalq(w.derivative(w.test(S,k),d),1)==w.evalq(w.derivative(w.test(S,k),d),-1)==0
    for i in range(n):
      for j in range(n):
        assert w.metric(S,i,j)==w.seed_metric(S,i,j)
        h=w.symmetric_correlation(S,i,j)
        assert h[0]==w.mass(S,i,j)
        assert len(h)==1 or h[1]==0
        if (i+j)%2:assert h==[F(0)]
        if len(h)>2:
            dg=w.integral_even(w.mul(w.derivative(w.test(S,i)),w.derivative(w.test(S,j))))/S
            assert -2*h[2]/S**2==dg
    assert w.correlation(S,0,1)!=[F(0)] # raw cross parity is not a zero correlation
    return dict(endpoint_jets=True,moments_by_exact_integration_by_parts=True,
                metric_identity=True,parity_symmetrized=True,raw_cross_parity_nonzero=True,
                second_translation_jet=True)
def numerical_checks(S,M):
    sm=w.mpq(S);errs=[]
    for i,j in [(0,0),(0,2),(1,3),(0,1)]:
      for z in [F(0),F(1,3),F(1),F(3,2),F(2)]:
        zm=w.mpq(z);t=sm*zm
        direct=mp.quad(lambda x:w.evalmp(w.test(S,i),x/sm)*w.evalmp(w.test(S,j),(x-t)/sm),[t-sm,sm]) if z<2 else mp.mpf(0)
        expected=w.evalmp(w.correlation(S,i,j),zm)
        errs.append(abs(direct-expected)/(1+abs(expected)))
    ae=max(abs(w.arch(S,i,j,True)-M['arch'][i,j])/(1+abs(M['arch'][i,j])) for i,j in [(0,0),(0,2),(1,3),(7,7)])
    C=mp.eye(8)
    for k in range(7):C[k,k+1]=mp.mpf(1)/3
    e=w.normalized_spectrum(M['G'],M['B']);ec=w.normalized_spectrum(C.T*M['G']*C,C.T*M['B']*C)
    ce=max(abs(e[k]-ec[k]) for k in range(8))
    dg=w.debt(M['G']);db=w.debt(M['B'])
    # New vector 2*v+old, old basis mixed invertibly. Same flag, ratio unchanged.
    C[7,7]=2;C[0,7]=mp.mpf(2)/7
    se=abs(dg/db-w.debt(C.T*M['G']*C)/w.debt(C.T*M['B']*C))
    return dict(correlation_direct_relative_error=mp.nstr(max(errs)),arch_two_forms_relative_error=mp.nstr(ae),
                congruence_spectrum_error=mp.nstr(ce),fixed_flag_schur_ratio_error=mp.nstr(se),
                phase_and_common_translation='exact algebra: autocorrelation unchanged; window grows under translation')
def main():
    p=D/'v644_protocole_traductions.json';protocol=json.loads(p.read_text())
    result=dict(version='V6.44',protocol_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        status='numerical_exploration_not_interval_certificate',zero_data_used=False,
        exact_scope='rational polynomials, H1 metric, parity, jets and integer prime-power cutoff',
        numerical_scope='transcendental archimedean quadrature, prime weights and eigenvalues',supports=[])
    maxn=max(protocol['dimensions'])
    for support in protocol['supports']:
        S=F(support);row=dict(S=support,symbolic=symbolic_checks(S,maxn),precisions=[])
        saved=[]
        for digits in protocol['precisions']:
          print('calcul S='+support+' dps='+str(digits),flush=True)
          with mp.workdps(digits):
            M=w.matrices(S,maxn,digits);saved.append(M)
            checks=numerical_checks(S,M);prefix=[]
            for n in protocol['dimensions']:
                G=M['G'][:n,:n];B=M['B'][:n,:n];e=w.normalized_spectrum(G,B)
                ds=w.debt(G)/w.debt(B)
                prefix.append(dict(n=n,eigenvalues=[mp.nstr(x,digits) for x in e],
                    lambda_min=mp.nstr(e[0],digits),lambda_max=mp.nstr(e[-1],digits),
                    normalized_last_schur_debt=mp.nstr(ds,digits)))
            row['precisions'].append(dict(digits=digits,G=strings(M['G']),B=strings(M['B']),
                arch=strings(M['arch']),primes=strings(M['primes']),checks=checks,prefixes=prefix))
            row.update(prime_power_count=len(M['powers']),prime_powers=M['powers'],cutoff_certificate=M['cutoff'])
        with mp.workdps(max(protocol['precisions'])):
            err=maxdiff(saved[0]['G'],saved[1]['G'])/(1+max(abs(x) for x in saved[1]['G']))
            row['precision_relative_matrix_difference']=mp.nstr(err,30)
            assert err<mp.mpf('1e-25'), 'precision instability'
            for x in row['precisions']:
                for name,val in x['checks'].items():
                    if name.endswith('error'):assert mp.mpf(val)<mp.mpf('1e-25'),name
        result['supports'].append(row)
        (D/'v644_family_resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    result['complete']=True
    (D/'v644_family_resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('4 supports; 16 prefixes; 2 precisions; exact guards and numerical cross-checks passed',flush=True)
if __name__=='__main__':main()
