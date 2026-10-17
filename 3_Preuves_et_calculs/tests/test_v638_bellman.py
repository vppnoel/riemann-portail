"""Independent optimality, units of state, saturation and historical coverage."""
from pathlib import Path
import json
from bellman_research import solve, utility, enumerate_portfolios, validate

ROOT = Path(__file__).resolve().parents[1]


def small_model():
    return {'criteria': ['c'], 'tokens': {'x': 'c', 'y': 'c', 'z': 'c'}, 'actions': [
        {'id': 'setup', 'cost': 1, 'requires': [], 'tokens': []},
        {'id': 'finish', 'cost': 1, 'requires': ['setup'], 'tokens': ['x', 'y', 'z']},
        {'id': 'quick', 'cost': 1, 'requires': [], 'tokens': ['x']}]}


def test_delayed_deliverable_beats_myopic_choice():
    m = small_model()
    assert solve(m, 2, {'c': 1})['portfolios'] == [['finish', 'setup']]
    assert solve(m, 2, {'c': 1})['first_choices'] == ['setup']


def test_shared_token_not_rewarded_twice_and_stop_allowed():
    m = small_model()
    m['actions'][0]['tokens'] = ['x']
    assert utility(m, {'setup', 'quick'}, {'c': 1}) == 1
    result = solve(m, 0, {'c': 1}, completed=['setup'])
    assert result['value'] == 1 and result['gain'] == 0
    assert result['first_choices'] == ['STOP']


def test_all_equivalent_first_choices_preserved():
    m = small_model()
    m['actions'] = [a for a in m['actions'] if a['id'] != 'finish']
    m['actions'][0]['tokens'] = ['y']
    result = solve(m, 2, {'c': 1})
    assert set(result['first_choices']) == {'setup', 'quick'}
    assert result['portfolios'] == [['quick', 'setup']]


def test_cycles_and_nonpositive_cost_rejected():
    m = small_model()
    m['actions'][0]['requires'] = ['finish']
    try:
        validate(m)
    except ValueError:
        pass
    else:
        raise AssertionError('Cycle accepted')
    m = small_model()
    m['actions'][0]['cost'] = 0
    try:
        validate(m)
    except ValueError:
        pass
    else:
        raise AssertionError('Zero cost accepted')


def test_full_model_independent_subset_optimum():
    m = json.loads((ROOT / 'data/v638_modele_bellman.json').read_text())
    for budget in range(9):
        weights = dict.fromkeys(m['criteria'], 1)
        result = solve(m, budget, weights)
        brute = enumerate_portfolios(m, budget, weights)
        assert result['value'] == brute['value']
        assert result['portfolios'] == brute['portfolios']


def test_atlas_covers_all_original_presentation_documents():
    registry = json.loads((ROOT / 'data/v638_decisions.json').read_text(encoding='utf-8-sig'))
    assert sorted(int(x['numero']) for x in registry['documents']) == list(range(1, 62))
