"""Restore the contract-scenario Bellman from document 67, sections 1 and 7.

State is (facts K, studies executed D, budget b). Capabilities have AND/OR
contracts; finishing a study does not imply its favourable scientific outcome.
The lower envelope uses the upper duration and the worst declared outcome;
the upper envelope uses the lower duration and the best declared outcome.
These are declared finite scenarios, not confidence bounds or an RH-distance.

The union-of-deliverable-tokens model is deliberately not accepted here.
"""
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import json
import math

MODEL_PATH = Path(__file__).with_name('bellman_contrats_v643.json')
SCHEMA = 'bridge_contract_scenarios_v1'
SCOPE = 'Declared finite scenarios only; no RH probability'
STRUCTURAL_CAPABILITIES = frozenset({
    'contrat_structurel', 'noyau_resolu', 'pont_conditionnel',
    'transfert_controle',
})


def load_contract_model(path=None):
    """Load the exact declared model retained in 67_GRAPHE_DES_PONTS.html."""
    model = json.loads(Path(path or MODEL_PATH).read_text(encoding='utf-8'))
    validate_model(model)
    return model


def _finite_nonnegative(value):
    return (type(value) in (int, float) and math.isfinite(value) and value >= 0)


def _has(facts, alternatives):
    return any(set(required) <= facts for required in alternatives)


def _check_alternatives(alternatives, known, label):
    if not isinstance(alternatives, list) or not alternatives:
        raise ValueError(label + ': requires_any must contain declared AND contracts')
    for required in alternatives:
        if not isinstance(required, list) or not all(isinstance(k, str) for k in required):
            raise ValueError(label + ': a contract must be a list of fact IDs')
        if not set(required) <= known:
            raise ValueError(label + ': unknown prerequisite fact')


def _check_state(model, facts):
    if not facts <= set(model['facts']):
        raise ValueError('Unknown fact in state')
    if facts & set(model.get('reserved_global_claims', ())):
        raise ValueError('A research simulation cannot establish a reserved global claim')
    for group in model.get('exclusive_groups', ()):
        if len(facts & set(group)) > 1:
            raise ValueError('Mutually exclusive outcomes in state')


def validate_model(model):
    """Check model structure and protected claims, not mathematical proofs."""
    if model.get('schema') != SCHEMA or 'tokens' in model:
        raise ValueError('Use the document 67 contract-scenario model, not union of tokens')
    known = set(model['facts'])
    if not known or not all(isinstance(k, str) and k for k in known):
        raise ValueError('Facts need distinct nonempty string IDs')
    protected = set(model.get('reserved_global_claims', ()))
    if not protected <= known:
        raise ValueError('Unknown reserved global claim')
    for group in model.get('exclusive_groups', ()):
        if not set(group) <= known:
            raise ValueError('Unknown fact in exclusive group')
    _check_state(model, set(model['initial_facts']))
    actions = model['actions']
    ids = [a['id'] for a in actions]
    if len(set(ids)) != len(ids) or 'STOP' in ids:
        raise ValueError('Duplicate or reserved action ID')
    for action in actions:
        label = 'Action ' + action['id']
        duration = action['duration']
        if (not isinstance(duration, list) or len(duration) != 2 or
                any(type(v) is not int or v <= 0 for v in duration) or
                duration[0] > duration[1]):
            raise ValueError(label + ': durations must be positive integer bounds')
        _check_alternatives(action['requires_any'], known, label)
        if not set(action.get('forbids', ())) <= known:
            raise ValueError(label + ': unknown forbidden fact')
        outcomes = action['outcomes']
        if not outcomes or len({o['id'] for o in outcomes}) != len(outcomes):
            raise ValueError(label + ': nonempty distinct outcomes required')
        for outcome in outcomes:
            additions = set(outcome['adds'])
            if not additions <= known:
                raise ValueError(label + ': unknown outcome fact')
            if additions & protected:
                raise ValueError(label + ': outcome cannot credit a reserved global proof')
            _check_state(model, additions)
    capabilities = model['capabilities']
    if len({c['id'] for c in capabilities}) != len(capabilities):
        raise ValueError('Duplicate capability ID')
    for capability in capabilities:
        if not _finite_nonnegative(capability['weight']):
            raise ValueError('Capability weights must be finite and nonnegative')
        _check_alternatives(capability['requires_any'], known,
                            'Capability ' + capability['id'])


def apply_weight_profile(model, factors=None):
    """Same three editable multipliers as renderPlan in document 67."""
    factors = factors or dict(structural=1, local=1, clarity=1)
    if set(factors) != {'structural', 'local', 'clarity'} or not all(
            _finite_nonnegative(v) for v in factors.values()):
        raise ValueError('Expected nonnegative structural/local/clarity factors')
    result = deepcopy(model)
    for capability in result['capabilities']:
        key = ('structural' if capability['id'] in STRUCTURAL_CAPABILITIES
               else 'local' if capability['id'] == 'local' else 'clarity')
        capability['weight'] *= factors[key]
    validate_model(result)
    return result


def utility(model, facts):
    """Credit a capacity once, only when one complete AND contract holds."""
    facts = frozenset(facts)
    return sum(c['weight'] for c in model['capabilities']
               if _has(facts, c['requires_any']))


def solve(model, budget, mode='lower', facts=None, completed=()):
    """Exact adaptive finite scenario envelope; preserve STOP and all ties.

    ``facts`` is an explicit current state, defaulting to initial_facts.
    ``completed`` only prevents repeating studies; it never adds their outcomes.
    choice_values and outcome_values describe the first decision and its issues.
    Flat terminal portfolios are not returned, because later decisions can depend
    on which outcome was obtained.
    """
    validate_model(model)
    if type(budget) is not int or budget < 0:
        raise ValueError('Budget must be a nonnegative integer')
    if mode not in {'lower', 'upper'}:
        raise ValueError('Mode must be lower or upper')
    initial = frozenset(model['initial_facts'] if facts is None else facts)
    done = frozenset(completed)
    _check_state(model, initial)
    if not done <= {a['id'] for a in model['actions']}:
        raise ValueError('Unknown completed study')
    duration_index = 1 if mode == 'lower' else 0

    @lru_cache(None)
    def visit(current, executed, remaining):
        choices = {'STOP': utility(model, current)}
        issues = {}
        for action in model['actions']:
            cost = action['duration'][duration_index]
            if (action['id'] in executed or cost > remaining or
                    not _has(current, action['requires_any']) or
                    current & set(action.get('forbids', ()))):
                continue
            values = {}
            for outcome in action['outcomes']:
                following = current | frozenset(outcome['adds'])
                _check_state(model, following)
                values[outcome['id']] = visit(
                    following, executed | {action['id']}, remaining-cost)['value']
            issues[action['id']] = values
            choices[action['id']] = (min if mode == 'lower' else max)(values.values())
        best = max(choices.values())
        return dict(value=best,
                    first_choices=sorted(k for k, v in choices.items() if v == best),
                    choice_values=choices, outcome_values=issues)

    result = dict(visit(initial, done, budget))
    result.update(gain=result['value']-utility(model, initial),
                  states=visit.cache_info().currsize, mode=mode, scope=SCOPE,
                  budget=budget, facts=sorted(initial), completed=sorted(done))
    return result


def solve_envelopes(model, budget, facts=None, completed=()):
    """Both declared scenario envelopes, with no transition probabilities."""
    return {mode: solve(model, budget, mode, facts=facts, completed=completed)
            for mode in ('lower', 'upper')}
