"""Post-results documentary planning: current model and independent exhaustive checks.

This extension is editorial. It is not a preregistered scientific prediction.
"""
from pathlib import Path
from copy import deepcopy
from itertools import product
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from bellman_research import solve,utility

def independent(model,budget,weights,completed):
    """Enumerate all remaining subsets, and derive possible first actions directly."""
    done=set(completed);remaining=[a for a in model['actions'] if a['id'] not in done]
    best=-1;ports=[];first=set()
    for mask in range(1<<len(remaining)):
        actions=[a for i,a in enumerate(remaining) if mask&(1<<i)]
        final=done|{a['id'] for a in actions}
        if sum(a['cost'] for a in actions)>budget or any(not set(a['requires'])<=final for a in actions):continue
        value=utility(model,final,weights)
        starts={a['id'] for a in actions if set(a['requires'])<=done}
        if not actions:starts.add('STOP')
        if value>best:best=value;ports=[sorted(final)];first=starts
        elif value==best:ports.append(sorted(final));first|=starts
    return dict(value=best,gain=best-utility(model,done,weights),portfolios=sorted(ports),first_choices=sorted(first))

def main():
    D=ROOT/'data'
    model=json.loads((D/'v638_modele_bellman.json').read_text(encoding='utf-8-sig'))
    model=deepcopy(model);model['version']='V6.41'
    model['extension_status']='Editorial extension after V641 results; not a scientific preregistration.'
    model['historical_model']='v638_modele_bellman.json'
    model['tokens'].update(passages_v13='discrimination',provenance_passages='reproduction',limites_passages='articulation',audit_bloc_local='certification',contrat_global='articulation',conditions_uniformes='certification')
    model['actions'] += [
      dict(id='v13_passages',label='Relier fibres, jets et paires locales',cost=3,requires=['v13_comparaison'],tokens=['passages_v13','provenance_passages','limites_passages'],source='1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.md',output='Dossier démontré et bilan contrôlé des continuations, collisions et obstacles ; achevé en V6.41.'),
      dict(id='certifier_bloc_local',label='Auditer la certification d’un bloc local',cost=3,requires=['v13_passages'],tokens=['audit_bloc_local','provenance_passages','limites_passages'],source='3_Preuves_et_calculs/preuves/V641_COLLISIONS_ET_LIMITES.md',output='Budget d’intervalles et rapport de validation ou d’obstacle explicite ; aucun certificat de zéros promis.'),
      dict(id='audit_positivite_uniforme',label='Auditer le contrat arithmétique global',cost=2,requires=['sources_conditions','v13_passages'],tokens=['contrat_global','conditions_uniformes','dossier_conditions'],source='3_Preuves_et_calculs/preuves/V641_PASSAGE_AU_GLOBAL.md',output='Domaine, signe, densité et inégalité manquante : rapport contrôlable même si le pont reste absent ; aucune positivité globale promise.'),
    ]
    completed=['v13_contraintes','v13_comparaison','v13_passages']
    profiles=[dict(zip(model['criteria'],p)) for p in product((1,2,3),repeat=5)]
    summaries=[];cases=[]
    for budget in (2,4,6,8):
        some=dict.fromkeys([a['id'] for a in model['actions']],0);all_=dict(some);first=dict(some);unique=0
        for weights in profiles:
            result=solve(model,budget,weights,completed);oracle=independent(model,budget,weights,completed)
            for field in ('value','gain','portfolios'):assert result[field]==oracle[field],(budget,weights,field)
            assert sorted(result['first_choices'])==oracle['first_choices']
            cases.append(dict(budget=budget,weights=weights,expected=result))
            union=set().union(*(set(p) for p in result['portfolios']));common=set.intersection(*(set(p) for p in result['portfolios']))
            for id in some:some[id]+=id in union;all_[id]+=id in common;first[id]+=id in result['first_choices']
            unique+=len(result['portfolios'])==1
        summaries.append(dict(budget=budget,profiles=243,unique_portfolio_profiles=unique,in_some_optimal_portfolio=some,in_all_optimal_portfolios=all_,optimal_first_choice=first,equal_weights=solve(model,budget,dict.fromkeys(model['criteria'],1),completed)))
        print('V641 Bellman budget',budget,'243 independent comparisons passed',flush=True)
    output=dict(model='finite conditional documentary planning V641',completed=completed,comparisons_passed=len(cases),results=summaries,empirical_transition_probabilities=None,guarantee='Optimality only within the declared twelve-action documentary model; no guarantee of research success.',extension_status=model['extension_status'])
    for name,value in [('v641_modele_bellman.json',model),('v641_bellman_resultats.json',output),('v641_bellman_controles.json',dict(model=model,completed=completed,cases=cases))]:
        (D/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print('972 Bellman results equal independent subset enumeration; all ties retained')

if __name__=='__main__':main()
