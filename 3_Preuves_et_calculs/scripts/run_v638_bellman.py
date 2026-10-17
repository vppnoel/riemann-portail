"""Solve the documented finite model and compare against independent enumeration."""
from pathlib import Path
import json
import sys
from copy import deepcopy
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from bellman_research import solve, enumerate_portfolios, sensitivity

def main():
    model = json.loads((ROOT / 'data/v638_modele_bellman.json').read_text(encoding='utf-8-sig'))
    comparisons = 0
    for budget in (2, 4, 6, 8):
        for profile in product((1, 2, 3), repeat=5):
            weights = dict(zip(model['criteria'], profile))
            dynamic = solve(model, budget, weights)
            exhaustive = enumerate_portfolios(model, budget, weights)
            assert dynamic['value'] == exhaustive['value']
            assert dynamic['portfolios'] == exhaustive['portfolios']
            comparisons += 1
    cost_scenarios = []
    for name, action_id, new_cost in [('V13 comparaison coût1', 'v13_comparaison', 1),
                                      ('DH extension coût1', 'dh_fenetres', 1),
                                      ('Contraintes V13 coût2', 'v13_contraintes', 2)]:
        changed = deepcopy(model)
        next(a for a in changed['actions'] if a['id'] == action_id)['cost'] = new_cost
        cost_scenarios.append({'name': name, 'changed_action': action_id, 'new_cost': new_cost,
                               'results': [dict(budget=b, **solve(changed, b, dict.fromkeys(changed['criteria'], 1)))
                                           for b in (2, 4, 6, 8)]})
    output = {'model': 'finite conditional documentary planning', 'comparisons_passed': comparisons,
              'results': sensitivity(model), 'empirical_transition_probabilities': None,
              'cost_scenarios': cost_scenarios,
              'cost_scenario_status': 'Exploratory sensitivity added after the base run; not a scientific preregistration.',
              'guarantee': 'Optimality within the stated model, not optimality of real research.'}
    (ROOT / 'data/v638_bellman_resultats.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(f'{comparisons} comparisons with independent subset enumeration passed')
    for item in output['results']:
        print('Budget', item['budget'], 'equal-weight value', item['equal_weights']['value'],
              'portfolios', len(item['equal_weights']['portfolios']))

if __name__ == '__main__':
    main()
