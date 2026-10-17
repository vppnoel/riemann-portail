"""Execute the frozen prime-centered protocol and separate validated/exploratory output."""
from pathlib import Path
import sys,json,hashlib
import mpmath as mp
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data';sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import prime_centered_bridge as b
import symbolic_weil_family as w
def main():
    p=D/'v645_protocole_arithmetique.json';protocol=json.loads(p.read_text());b.setup(protocol['interval_binary_precision'])
    old=json.loads((D/'v644_family_resultats.json').read_text());oldtails=json.loads((D/'v644_contrats_queue_entiers.json').read_text())['contracts']
    result=dict(version='V6.45',protocol_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),zero_data_used=False,
        validated_scope='rational seed energy, prime/residual entries with binary outward intervals, geometric/row/multiplier/tail bounds, negative base rational witnesses',
        exploratory_scope='archimedean matrices and generalized spectra reused from V644; no full Schur sign certificate',supports=[])
    for row,oldtail in zip(old['supports'],oldtails):
        S=F(row['S']);powers=[tuple(v) for v in row['prime_powers']];cut=row['cutoff_certificate']['cutoff'];n=8
        print('intervals S='+str(S),flush=True);B=b.norm_budgets(S,powers,cut);entries=[];P0=mp.matrix(n);Res=mp.matrix(n);maxwidth=F(0)
        for i in range(n):
          for j in range(i,n):
            v=b.prime_residual_intervals(S,i,j,powers);P0[i,j]=P0[j,i]=w.mpq(v['seed']);Res[i,j]=Res[j,i]=b.midpoint(v['residual'])
            maxwidth=max(maxwidth,b.hi(v['residual'])-b.lo(v['residual']),b.hi(v['ibp'])-b.lo(v['ibp']))
            entries.append(dict(i=i,j=j,seed_energy_exact=str(v['seed']),**{key:b.pack(v[key]) for key in ['prime','residual','ibp','continuum']}))
        archived=row['precisions'][-1];A=mp.matrix([[mp.mpf(x) for x in line] for line in archived['arch']]);metric=mp.matrix([[mp.mpf(x) for x in line] for line in archived['B']]);G=mp.matrix([[mp.mpf(x) for x in line] for line in archived['G']]);base=A+P0
        diff=max(abs((base-Res-G)[i,j]) for i in range(n) for j in range(n));assert diff<mp.mpf('1e-50')
        prefixes=[]
        for m in protocol['dimensions']:
            e=w.normalized_spectrum(base[:m,:m],metric[:m,:m]);prefixes.append(dict(n=m,base_lambda_min_exploratory=mp.nstr(e[0],25),full_lambda_min_v644=archived['prefixes'][protocol['dimensions'].index(m)]['lambda_min']))
        tail=b.improved_tail(S,B['chosen_upper'],protocol['kernel_series_split'],protocol['tail_dyadic_J_range'])
        tail['old_q_digits']=oldtail['q_decimal_digits'];tail['old_J']=oldtail['J']
        r=dict(S=str(S),prime_power_count=len(powers),cutoff=cut,entries=entries,interval_max_width=mp.nstr(w.mpq(maxwidth),10),
            budgets={k:b.pack(B[k]) for k in ['c0','raw','geometric','row','prime_norm_lower']},chosen_L_upper=str(B['chosen_upper']),
            chain_lengths=B['chain_lengths'],tail=tail,prefixes=prefixes,reconstruction_difference_exploratory=mp.nstr(diff,12))
        result['supports'].append(r);(D/'v645_arithmetique_resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    result['wide_base_rational_certificates']=[b.negative_base_bound(F(s)) for s in protocol['wide_seed_supports']]
    result['uniform_negative_base_certificate']=b.uniform_negative_base_certificate()
    result['complete']=True;(D/'v645_arithmetique_resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('prime/residual interval checks, tail gates and rational base witnesses complete',flush=True)
if __name__=='__main__':main()
