"""Build declared bridge scenarios and exact audit examples."""
from pathlib import Path
from itertools import product
from copy import deepcopy
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from bridge_planning import solve,bottom_up
from schur_bridge import append_contract


def build_model():
    initial=['nb_transport','weil_continuity','admissible_core','regularization_bound','schur_identity','ladder_contract']
    extra=['regularization_assessed','coverage_candidate','coverage_gap','debt_assessed','invariant_candidate',
           'candidate_refuted','open_debt','kernel_assessed','kernel_checked','kernel_obstruction',
           'transfer_assessed','fixed_transfer_verified','transfer_insufficient','family_dossier',
           'local_assessed','fixed_A_certificate','local_obstruction','local_inconclusive',
           'weil_reading_assessed','weil_full_read','weil_access_gap','RH_proved','global_sign_proved']
    def action(id,label,duration,req,outs,forbids=()):
        return dict(id=id,label=label,duration=duration,requires_any=req,forbids=list(forbids),
                    outcomes=[dict(id=k,adds=v) for k,v in outs],
                    scope='Proposed bounded study; an assessed candidate is not a uniform sign theorem')
    actions=[
      action('regime_commun','Construire une famille régularisée et son défaut',[2,3],[['regularization_bound','admissible_core']],
             [('couverture_candidate',['regularization_assessed','coverage_candidate']),('couverture_manquante',['regularization_assessed','coverage_gap'])]),
      action('dette_schur','Chercher un invariant pour la dette de Schur',[2,4],[['schur_identity','weil_continuity']],
             [('candidat',['debt_assessed','invariant_candidate']),('refutation',['debt_assessed','candidate_refuted']),('sans_borne',['debt_assessed','open_debt'])]),
      action('noyaux','Auditer noyaux et couplages du candidat',[1,2],[['invariant_candidate'],['open_debt']],
             [('compatible',['kernel_assessed','kernel_checked']),('obstacle',['kernel_assessed','kernel_obstruction'])],['candidate_refuted']),
      action('transfert','Contrôler un transfert d’erreur sur la famille choisie',[2,3],[['coverage_candidate','invariant_candidate']],
             [('controle_fixe',['transfer_assessed','fixed_transfer_verified']),('borne_insuffisante',['transfer_assessed','transfer_insufficient'])],['candidate_refuted']),
      action('synthese_famille','Assembler le contrat et ses limites',[1,2],[['regularization_assessed','debt_assessed','kernel_assessed'],['regularization_assessed','candidate_refuted']],
             [('contrat',['family_dossier'])]),
      action('fibre_A','Certifier un autre passage local à A fixé',[2,4],[[]],
             [('certificat',['local_assessed','fixed_A_certificate']),('obstacle',['local_assessed','local_obstruction']),('inconclusif',['local_assessed','local_inconclusive'])]),
      action('relire_weil','Terminer l’audit du mémoire de Weil',[2,3],[[]],
             [('lecture_integrale',['weil_reading_assessed','weil_full_read']),('acces_partiel',['weil_reading_assessed','weil_access_gap'])])]
    caps=[
      dict(id='contrat_structurel',label='Domaine et dette définis ensemble',weight=8,requires_any=[['regularization_assessed','debt_assessed']]),
      dict(id='noyau_resolu',label='Couplage du candidat audité',weight=3,requires_any=[['kernel_assessed']]),
      dict(id='transfert_controle',label='Transfert fixe contrôlé',weight=4,requires_any=[['fixed_transfer_verified']]),
      dict(id='candidat_rejete',label='Candidat précisément réfuté',weight=3,requires_any=[['candidate_refuted']]),
      dict(id='pont_conditionnel',label='Contrat assemblé, quantificateurs ouverts',weight=5,requires_any=[['family_dossier']]),
      dict(id='lecture',label='Audit de lecture circonscrit',weight=2,requires_any=[['weil_reading_assessed']]),
      dict(id='local',label='Étude locale circonscrite',weight=2,requires_any=[['local_assessed']])]
    return dict(version='V6.43',schema='bridge_contract_scenarios_v1',initial_facts=initial,
                facts={f:dict(status='proved_internal' if f in initial else 'hypothetical_outcome',scope='Domaine et hypothèses du lemme dans le dossier' if f in initial else 'Issue d’étude bornée ; aucun quantificateur global acquis',
                              evidence='preuves/V643_PONTS_MATHEMATIQUES.md' if f in initial else None) for f in initial+extra},
                actions=actions,capabilities=caps,reserved_global_claims=['RH_proved','global_sign_proved'],
                exclusive_groups=[['coverage_candidate','coverage_gap'],['invariant_candidate','candidate_refuted','open_debt'],
                                  ['kernel_checked','kernel_obstruction'],['fixed_transfer_verified','transfer_insufficient']],
                units=dict(budget='H: unité conventionnelle de travail, pas heure',value='U: préférence déclarée de capacité'),
                assumptions=['No calibrated transition probabilities','No RH-distance or proof probability',
                             'Durations are declared intervals, not measured effort',
                             'Study completion is conditional; scientific outcomes branch',
                             'Lower/upper are declared scenario envelopes, not empirical confidence intervals',
                             'Costs and weights are editorial choices dated after the lemmas',
                             'Capabilities count mathematical contracts once, regardless of document subdivision'],
                next_contract='Specify a candidate invariant and its arithmetic Schur debt for the complete form, with kernel and family quantifiers')


def toy():
    facts={f:{} for f in ['a','b','l1','l2','l3']}
    actions=[dict(id=k,label=k,duration=[c,c],requires_any=[[]],outcomes=[dict(id='ok',adds=[f])])
             for k,f,c in [('construction_a','a',2),('construction_b','b',2),('local1','l1',1),('local2','l2',1),('local3','l3',1)]]
    caps=[dict(id='pont',weight=12,requires_any=[['a','b']])]+[dict(id=f,weight=2,requires_any=[[f]]) for f in ['l1','l2','l3']]
    return dict(facts=facts,initial_facts=[],actions=actions,capabilities=caps)


def main():
    D=ROOT/'data';model=build_model();rows=[];checks=0;client_cases=[]
    for weights in product((1,2,3),repeat=3):
        m=deepcopy(model)
        for c in m['capabilities']:
            factor=weights[0] if c['id'] in ('contrat_structurel','noyau_resolu','pont_conditionnel','transfert_controle') else weights[1] if c['id']=='local' else weights[2]
            c['weight']*=factor
        for b in (2,4,6,8,10):
            for mode in ('lower','upper'):
                s=solve(m,b,mode);ref=bottom_up(m,b,mode)
                assert s['value']==ref['value'] and s['first_choices']==ref['first_choices'];checks+=1
                client_cases.append(dict(profile=weights,budget=b,mode=mode,expected=dict(value=s['value'],first_choices=s['first_choices'])))
            if weights==(1,1,1):rows.append(dict(budget=b,lower=solve(m,b,'lower'),upper=solve(m,b,'upper')))
    t=toy();t_sol=solve(t,4)
    assert t_sol['value']==12 and set(t_sol['first_choices'])=={'construction_a','construction_b'}
    results=dict(version='V6.43',comparisons_passed=checks,weight_profiles=27,budgets=[2,4,6,8,10],results=rows,
                 toy=dict(budget=4,bridge_value=12,three_local_value=6,optimal=t_sol),
                 schur_examples=[dict(label='pivot positif',**append_contract([[2]],[1],1)),
                                 dict(label='couplage dans le noyau',**append_contract([[0]],[1],1)),
                                 dict(label='dette négative',**append_contract([[2]],[2],1))])
    def encode(o):
        from fractions import Fraction
        if isinstance(o,Fraction):return str(o)
        raise TypeError(type(o))
    for n,v in [('v643_modele_ponts.json',model),('v643_bellman_ponts.json',results)]:
        (D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=encode)+'\n')
    (D/'v643_clients_controls.json').write_text(json.dumps(dict(model=model,cases=client_cases),ensure_ascii=False,indent=2)+'\n')
    print(f'{checks} comparaisons Bellman / graphe explicite ; complémentarité 12 contre 6 ; trois contrats Schur')
    for row in rows:print(row['budget'],row['lower']['value'],row['lower']['first_choices'],row['upper']['value'])
if __name__=='__main__':main()
