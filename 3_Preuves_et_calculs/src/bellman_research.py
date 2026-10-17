"""Finite documentary planning. No learned probabilities or RH-distance.

V(D,b) includes the utility of D. STOP is allowed and actions are unique.
Tokens represent proposed deliverables, even when the scientific result is negative.
"""
from functools import lru_cache
from itertools import product


def validate(model):
    actions = model['actions']
    ids = [a['id'] for a in actions]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate action')
    tokens = model['tokens']
    criteria = model['criteria']
    if any(c not in criteria for c in tokens.values()):
        raise ValueError('Unknown criterion')
    for action in actions:
        if type(action['cost']) is not int or action['cost'] <= 0:
            raise ValueError('Costs must be positive integers')
        if not set(action['requires']).issubset(ids):
            raise ValueError('Unknown prerequisite')
        if not set(action['tokens']).issubset(tokens):
            raise ValueError('Unknown token')
    done = set()
    while True:
        new = {a['id'] for a in actions if set(a['requires']).issubset(done)}
        if new.issubset(done):
            break
        done |= new
    if done != set(ids):
        raise ValueError('Cyclic prerequisites')


def utility(model, completed, weights):
    tokens = set().union(*(set(a['tokens']) for a in model['actions']
                           if a['id'] in completed))
    return sum(weights[model['tokens'][token]] for token in tokens)


def solve(model, budget, weights, completed=()):
    """Exact Bellman values, all optimal first choices and all terminal portfolios."""
    validate(model)
    if type(budget) is not int or budget < 0:
        raise ValueError('Budget must be a nonnegative integer')
    if set(weights) != set(model['criteria']) or any(type(v) is not int or v < 0 for v in weights.values()):
        raise ValueError('Weights must be nonnegative integers on all criteria')
    actions = model['actions']
    index = {a['id']: i for i, a in enumerate(actions)}
    completed = set(completed)
    if not completed.issubset(index):
        raise ValueError('Unknown completed action')
    if any(not set(actions[index[k]]['requires']).issubset(completed) for k in completed):
        raise ValueError('Completed actions must include prerequisites')
    start = sum(1 << index[k] for k in completed)

    def names(mask):
        return {a['id'] for i, a in enumerate(actions) if mask & (1 << i)}

    @lru_cache(None)
    def visit(mask, remaining):
        done = names(mask)
        value = utility(model, done, weights)
        choices = ['STOP']
        finals = {mask}
        for i, action in enumerate(actions):
            bit = 1 << i
            if mask & bit or action['cost'] > remaining or not set(action['requires']).issubset(done):
                continue
            candidate, _, endpoints = visit(mask | bit, remaining - action['cost'])
            if candidate > value:
                value, choices, finals = candidate, [action['id']], set(endpoints)
            elif candidate == value:
                choices.append(action['id'])
                finals.update(endpoints)
        return value, tuple(choices), frozenset(finals)

    value, choices, endpoints = visit(start, budget)
    return {'value': value, 'gain': value - utility(model, completed, weights),
            'first_choices': list(choices),
            'portfolios': sorted([sorted(names(mask)) for mask in endpoints]),
            'states_visited': visit.cache_info().currsize}


def enumerate_portfolios(model, budget, weights):
    """Independent subset enumeration, not a recursive Bellman implementation."""
    validate(model)
    actions = model['actions']
    best, portfolios = -1, []
    for mask in range(1 << len(actions)):
        selected = [a for i, a in enumerate(actions) if mask & (1 << i)]
        done = {a['id'] for a in selected}
        if sum(a['cost'] for a in selected) > budget:
            continue
        if any(not set(a['requires']).issubset(done) for a in selected):
            continue
        value = utility(model, done, weights)
        if value > best:
            best, portfolios = value, [sorted(done)]
        elif value == best:
            portfolios.append(sorted(done))
    return {'value': best, 'portfolios': sorted(portfolios)}


def sensitivity(model, budgets=(2, 4, 6, 8)):
    """243 explicit weight profiles on five criteria; frequencies are not probabilities."""
    validate(model)
    profiles = [dict(zip(model['criteria'], p)) for p in product((1, 2, 3), repeat=len(model['criteria']))]
    result = []
    for budget in budgets:
        counts = {a['id']: 0 for a in model['actions']}
        mandatory = dict(counts)
        first = dict(counts)
        unique = 0
        for weights in profiles:
            solution = solve(model, budget, weights)
            if len(solution['portfolios']) == 1:
                unique += 1
            union = set().union(*(set(p) for p in solution['portfolios']))
            common = set.intersection(*(set(p) for p in solution['portfolios']))
            for k in counts:
                counts[k] += k in union
                mandatory[k] += k in common
                first[k] += k in solution['first_choices']
        result.append({'budget': budget, 'profiles': len(profiles), 'unique_portfolio_profiles': unique,
                       'in_some_optimal_portfolio': counts, 'in_all_optimal_portfolios': mandatory,
                       'optimal_first_choice': first,
                       'equal_weights': solve(model, budget, dict.fromkeys(model['criteria'], 1))})
    return result
