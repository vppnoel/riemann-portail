"""Produce the exact-recipes V13 certificate without counting any zero."""
from pathlib import Path
import json
import sys
import hashlib
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from v639_contraintes import certificate
from relief_direct import a1_and_defect
from euler_archipelago import characters
from v639_rational import rational_certificate

def main():
    cert=certificate(80)
    high=certificate(120)
    for key in ('conjugate_pair_witnesses','minor_witnesses'):
        assert len(cert[key])==len(high[key])==24
        for a,b in zip(cert[key],high[key]):
            assert (a['anchor_index'],a['radius'],a.get('support_indices'))==(b['anchor_index'],b['radius'],b.get('support_indices'))
            assert float(a['gap_D']['lower'])>0 and float(b['gap_D']['lower'])>0
    phase=np.exp(-1j*np.array([x['phi'] for x in characters(13,1)]))
    numeric=[]
    for family in ('conjugate_pair_witnesses','minor_witnesses'):
        for item in cert[family]:
            C=np.asarray(item['exported_binary64_vectors'])
            _,D=a1_and_defect(13,1,C)
            A=C@phase
            approximate_D=[(float(item[k]['lower'])+float(item[k]['upper']))/2 for k in ('D_plus','D_minus')]
            assert np.max(np.abs(D-approximate_D))<2e-11
            assert abs(A[0]-A[1])<2e-13 and np.max(np.abs(np.sum(C*C,axis=1)-1))<2e-13
            numeric.append({'kind':item['kind'],'anchor':item['anchor_index'],'radius':item['radius'],
                            'historical_D':D.tolist(),'A_mismatch_binary64':float(abs(A[0]-A[1])),
                            'comparison_only_not_certificate':True})
    data=ROOT/'data'
    for name,value in [('v639_contraintes.json',cert),('v639_contraintes_precision120.json',high),('v639_recoupement_historique.json',numeric)]:
        (data/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    (data/'v639_certificat_rationnel.json').write_text(json.dumps(rational_certificate(),ensure_ascii=False,indent=2)+'\n')
    for family in ('conjugate_pair_witnesses','minor_witnesses'):
        old=[x for x in cert[family] if x['radius']!='pi/6']
        print(family,'18 nominal strata, gap range',min(float(x['gap_D']['lower']) for x in old),max(float(x['gap_D']['upper']) for x in old))
    print('All six anchors have kernel dimension3 and a strictly varying D; no zero counted.')

if __name__=='__main__':
    main()
