"""Current documentary model after the interval and arithmetic-contract audits."""
from pathlib import Path
from copy import deepcopy
from itertools import product
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from bellman_research import solve
from run_v641_bellman import independent

def main():
    D=ROOT/'data';model=deepcopy(json.loads((D/'v641_modele_bellman.json').read_text()))
    model['version']='V6.42';model['extension_status']='Editorial state and prerequisite correction after V642 results; not a scientific preregistration.'
    action=next(a for a in model['actions'] if a['id']=='audit_positivite_uniforme')
    action['requires']=['v13_passages'];action['output']='Primary-source normalization, exact arithmetic inequality and obstruction to a uniform prime-part norm; global sign still open.'
    model['prerequisite_correction']='The Weil-source checks are included in the global-contract audit. The broader sources_conditions action for other dossier sources remains uncompleted; no full-source audit is claimed.'
    completed=['v13_contraintes','v13_comparaison','v13_passages','certifier_bloc_local','audit_positivite_uniforme'];cases=[];summaries=[]
    for budget in (2,4,6,8):
        counts={a['id']:0 for a in model['actions']};mandatory=dict(counts);unique=0
        for profile in product((1,2,3),repeat=5):
            weights=dict(zip(model['criteria'],profile));a=solve(model,budget,weights,completed);b=independent(model,budget,weights,completed)
            assert all(a[k]==b[k] for k in ('value','gain','portfolios'));assert sorted(a['first_choices'])==b['first_choices']
            cases.append(dict(budget=budget,weights=weights,expected=a));union=set().union(*(set(p) for p in a['portfolios']));common=set.intersection(*(set(p) for p in a['portfolios']))
            for id in counts:counts[id]+=id in union;mandatory[id]+=id in common
            unique+=len(a['portfolios'])==1
        summaries.append(dict(budget=budget,profiles=243,unique_portfolio_profiles=unique,in_some_optimal_portfolio=counts,in_all_optimal_portfolios=mandatory,equal_weights=solve(model,budget,dict.fromkeys(model['criteria'],1),completed)))
    output=dict(model='finite conditional documentary planning V642',completed=completed,comparisons_passed=972,results=summaries,empirical_transition_probabilities=None,guarantee='Only documentary optimization; neither a global positivity proof nor its probability.',extension_status=model['extension_status'])
    for name,value in [('v642_modele_bellman.json',model),('v642_bellman_resultats.json',output),('v642_bellman_controles.json',dict(model=model,completed=completed,cases=cases))]:(D/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print('V642 Bellman: 972 exhaustive comparisons; twelve actions, five completed, all ties retained')
if __name__=='__main__':main()
