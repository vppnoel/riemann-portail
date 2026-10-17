"""Finite scenario planning on mathematical contracts, not on document counts.

No empirical probabilities. Lower = adverse declared outcome and high duration;
upper = favorable declared outcome and low duration. Both allow adaptive plans.
"""
from functools import lru_cache


def satisfies(facts, alternatives):
    return any(set(package) <= facts for package in alternatives)


def validate(model):
    facts = set(model['facts'])
    ids = [a['id'] for a in model['actions']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate action')
    for cap in model['capabilities']:
        if not cap['requires_any'] or any(not set(p) <= facts for p in cap['requires_any']):
            raise ValueError('Invalid capability contract')
        if type(cap['weight']) is not int or cap['weight'] < 0:
            raise ValueError('Invalid capability weight')
    if len({c['id'] for c in model['capabilities']}) != len(model['capabilities']):
        raise ValueError('Duplicate capability')
    for a in model['actions']:
        lo, hi = a['duration']
        if type(lo) is not int or type(hi) is not int or not 0 < lo <= hi:
            raise ValueError('Invalid duration')
        if not a['requires_any'] or any(not set(p) <= facts for p in a['requires_any']):
            raise ValueError('Invalid prerequisites')
        if not set(a.get('forbids', [])) <= facts or not a['outcomes']:
            raise ValueError('Invalid outcomes/guards')
        if len({o['id'] for o in a['outcomes']}) != len(a['outcomes']):
            raise ValueError('Duplicate outcome')
        for o in a['outcomes']:
            if not set(o['adds']) <= facts:
                raise ValueError('Unknown result fact')
            if set(o['adds']) & set(model.get('reserved_global_claims', [])):
                raise ValueError('Global theorem cannot be granted by this finite model')
    for group in model.get('exclusive_groups', []):
        if not set(group) <= facts:
            raise ValueError('Unknown exclusive fact')


def check_state(model, facts, done):
    if not facts <= set(model['facts']) or not done <= {a['id'] for a in model['actions']}:
        raise ValueError('Unknown state')
    if any(len(facts & set(g)) > 1 for g in model.get('exclusive_groups', [])):
        raise ValueError('Contradictory result state')


def utility(model, facts):
    return sum(c['weight'] for c in model['capabilities']
               if satisfies(facts, c['requires_any']))


def solve(model, budget, mode='lower', initial=None, done=()):
    validate(model)
    if type(budget) is not int or budget < 0 or mode not in ('lower', 'upper'):
        raise ValueError('Invalid budget/mode')
    initial = frozenset(model['initial_facts'] if initial is None else initial)
    done = frozenset(done)
    check_state(model, initial, done)
    reduce_outcomes = min if mode == 'lower' else max
    duration_index = 1 if mode == 'lower' else 0

    @lru_cache(None)
    def visit(facts, executed, remaining):
        stop = utility(model, facts)
        values = {'STOP': stop}
        issues = {}
        for a in model['actions']:
            cost = a['duration'][duration_index]
            if a['id'] in executed or cost > remaining:
                continue
            if not satisfies(facts, a['requires_any']) or facts & set(a.get('forbids', [])):
                continue
            outcomes = {}
            for o in a['outcomes']:
                nxt = facts | frozenset(o['adds'])
                check_state(model, nxt, executed | {a['id']})
                outcomes[o['id']] = visit(nxt, executed | {a['id']}, remaining-cost)[0]
            values[a['id']] = reduce_outcomes(outcomes.values())
            issues[a['id']] = outcomes
        best = max(values.values())
        choices = tuple(sorted(k for k, v in values.items() if v == best))
        return best, choices, values, issues

    value, choices, values, issues = visit(initial, done, budget)
    return dict(value=value, gain=value-utility(model, initial), first_choices=list(choices),
                choice_values=values, outcome_values=issues, states=visit.cache_info().currsize,
                mode=mode, scope='Declared finite scenarios only; no RH probability')


def bottom_up(model, budget, mode='lower', initial=None, done=()):
    """Independent explicit state graph and backward table, without recursion/cache."""
    validate(model)
    if type(budget) is not int or budget < 0 or mode not in ('lower', 'upper'):
        raise ValueError('Invalid budget/mode')
    initial = frozenset(model['initial_facts'] if initial is None else initial)
    done = frozenset(done); check_state(model, initial, done)
    root = (initial, done, budget); frontier=[root]; graph={}
    index = 1 if mode == 'lower' else 0
    while frontier:
        node = frontier.pop()
        if node in graph: continue
        f, d, b = node; edges={}
        for a in model['actions']:
            if a['id'] in d or a['duration'][index] > b: continue
            if all(not set(p) <= f for p in a['requires_any']): continue
            if any(k in f for k in a.get('forbids', [])): continue
            edges[a['id']]=[]
            for o in a['outcomes']:
                nxt=(frozenset(set(f).union(o['adds'])), d|{a['id']}, b-a['duration'][index])
                check_state(model,nxt[0],nxt[1]);edges[a['id']].append(nxt);frontier.append(nxt)
        graph[node]=edges
    table={}
    for node in sorted(graph,key=lambda n:n[2]):
        score=sum(c['weight'] for c in model['capabilities']
                  if any(set(p)<=node[0] for p in c['requires_any']))
        vals={'STOP':score}
        for a, children in graph[node].items():
            v=[table[ch][0] for ch in children]
            vals[a]=min(v) if mode=='lower' else max(v)
        best=max(vals.values());table[node]=(best,sorted(k for k,v in vals.items() if v==best))
    return dict(value=table[root][0],first_choices=table[root][1])
