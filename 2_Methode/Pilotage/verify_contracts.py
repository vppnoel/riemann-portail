#!/usr/bin/env python3
"""Verify the retained finite Bellman calculation from document 67.

Run from any directory:
  python3 -B 2_Methode/Pilotage/verify_contracts.py
  python3 -B 2_Methode/Pilotage/verify_contracts.py \
    --output 3_Preuves_et_calculs/data/v655_verification_contrats.json

Default execution only reads files and prints a JSON receipt. --output writes
that receipt; a relative output path is resolved from the corpus root.
Python and Node.js are required. --node can select another Node executable.

This checks the exact declared finite scenario model and its implementations.
It does not validate mathematical proofs, calibrate weights or costs, establish
the current status of studies, or prove any global arithmetic/RH assertion.
"""
from pathlib import Path
from itertools import product
from copy import deepcopy
from collections import deque
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORIGINAL_PAGE = ROOT / '1_Presentation/67_GRAPHE_DES_PONTS.html'
ARTICLE = ROOT / '1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.md'
COMPARE_KEYS = ('value', 'first_choices', 'choice_values', 'outcome_values', 'states')


def require(condition, message):
    """Unlike assert, verification remains active under python -O."""
    if not condition:
        raise RuntimeError(message)


def load_engine():
    spec = importlib.util.spec_from_file_location('verified_contract_engine', HERE / 'engine.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def original_payload():
    content = ORIGINAL_PAGE.read_text(encoding='utf-8')
    match = re.search(r'<script\b(?=[^>]*\bid=[\'"]bridge-data[\'"])[^>]*>(.*?)</script>',
                      content, re.S)
    require(match is not None, 'The bridge-data payload is absent from document 67')
    return json.loads(match.group(1))


def explicit_graph_solution(model, budget, mode):
    """Independent state-graph enumeration and bottom-up dynamic programming.

    This implementation uses fact/action bit masks and an explicit queue.
    It does not call the recursive engine or reuse its admissibility/utility
    helpers. Every successor has a strictly smaller budget.
    """
    fact_ids = {key: index for index, key in enumerate(model['facts'])}

    def fact_mask(facts):
        return sum(1 << fact_ids[key] for key in set(facts))

    def contracts(groups):
        return [fact_mask(group) for group in groups]

    def satisfied(mask, alternatives):
        return any(mask & required == required for required in alternatives)

    start = (fact_mask(model['initial_facts']), 0, budget)
    actions = [
        (index, action, contracts(action['requires_any']),
         fact_mask(action.get('forbids', [])),
         [(outcome['id'], fact_mask(outcome['adds'])) for outcome in action['outcomes']])
        for index, action in enumerate(model['actions'])
    ]
    capacities = [(cap['weight'], contracts(cap['requires_any']))
                  for cap in model['capabilities']]
    states = {start}
    queue = deque([start])
    transitions = {}
    while queue:
        state = queue.popleft()
        facts, done, remaining = state
        edges = []
        for index, action, requirements, forbidden, outcomes in actions:
            cost = action['duration'][1 if mode == 'lower' else 0]
            if (done & (1 << index) or cost > remaining or
                    not satisfied(facts, requirements) or facts & forbidden):
                continue
            successors = [(name, (facts | added, done | (1 << index), remaining-cost))
                          for name, added in outcomes]
            edges.append((action['id'], successors))
            for _, following in successors:
                if following not in states:
                    states.add(following)
                    queue.append(following)
        transitions[state] = edges

    values = {}
    for state in sorted(states, key=lambda item: item[2]):
        facts = state[0]
        choices = {'STOP': sum(weight for weight, requirements in capacities
                               if satisfied(facts, requirements))}
        issues = {}
        for action_id, successors in transitions[state]:
            issues[action_id] = {name: values[following]['value']
                                 for name, following in successors}
            choices[action_id] = (min if mode == 'lower' else max)(issues[action_id].values())
        best = max(choices.values())
        values[state] = dict(value=best,
                             first_choices=sorted(key for key, value in choices.items()
                                                  if value == best),
                             choice_values=choices, outcome_values=issues,
                             states=len(states))
    return values[start]


NODE_CHECK = r"""
const fs=require('fs'),vm=require('vm');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const current=require(process.cwd()+'/2_Methode/Pilotage/bellman_contracts.js');
const html=fs.readFileSync('1_Presentation/67_GRAPHE_DES_PONTS.html','utf8');
const begin=html.indexOf('function solveBridge(');
const end=html.indexOf("if(typeof module!=='undefined')module.exports={solveBridge};",begin);
if(begin<0||end<0)throw Error('Original document 67 solver not found');
const original={};vm.createContext(original);vm.runInContext(html.slice(begin,end),original);
const rows=[];
for(const factors of input.profiles){
  const model=current.applyBridgeWeightProfile(input.model,factors);
  for(const budget of input.budgets)for(const mode of ['lower','upper']){
    const actual=current.solveBridge(model,budget,mode);
    const retained=original.solveBridge(model,budget,mode);
    if(actual.value!==retained.value||
       JSON.stringify(actual.first_choices)!==JSON.stringify(retained.first_choices))
      throw Error('Mismatch with original solveBridge: '+JSON.stringify({factors,budget,mode}));
    rows.push(Object.fromEntries(input.keys.map(key=>[key,actual[key]])));
  }
}
process.stdout.write(JSON.stringify(rows));
"""


def javascript_cases(node, model, profiles, budgets):
    result = subprocess.run(
        [node, '-e', NODE_CHECK], cwd=ROOT,
        input=json.dumps(dict(model=model, profiles=profiles,
                              budgets=budgets, keys=COMPARE_KEYS)),
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode == 0, 'JavaScript verification failed: ' + result.stderr)
    return json.loads(result.stdout)


def semantic_guard_checks(engine, model):
    """Small counterexamples test state, outcomes and complementary contracts."""
    toy = dict(
        schema=engine.SCHEMA, facts={key: {} for key in ['a', 'b', 'l1', 'l2', 'l3']},
        initial_facts=[], reserved_global_claims=[], exclusive_groups=[],
        actions=[dict(id=key, label=key,
                      duration=[2, 2] if key in ['a', 'b'] else [1, 1],
                      requires_any=[[]], forbids=[], outcomes=[dict(id='ok', adds=[key])])
                 for key in ['a', 'b', 'l1', 'l2', 'l3']],
        capabilities=[dict(id='bridge', weight=12, requires_any=[['a', 'b']])] +
                     [dict(id=key, weight=2, requires_any=[[key]]) for key in ['l1', 'l2', 'l3']])
    require(engine.utility(toy, ['a']) == 0 and engine.utility(toy, ['b']) == 0 and
            engine.utility(toy, ['a', 'b']) == 12, 'AND complementarity lost')
    r = engine.solve(toy, 4)
    require(r['value'] == 12 and r['first_choices'] == ['a', 'b'],
            'Complementary constructions must beat three local values totalling 6')
    r = engine.solve(toy, 2, facts=['a'], completed=['a'])
    require(r['gain'] == 12 and r['first_choices'] == ['b'],
            'Explicit state or remaining budget handled incorrectly')
    r = engine.solve(toy, 0, facts=['a', 'b'], completed=['a', 'b'])
    require(r['gain'] == 0 and r['first_choices'] == ['STOP'],
            'Completed work credited twice or STOP lost')
    require('a' not in engine.solve(toy, 4, facts=['a'], completed=['a'])['first_choices'],
            'A completed action was repeated')
    alternative = deepcopy(toy)
    alternative['capabilities'] = [dict(id='one_capacity', weight=5,
                                       requires_any=[['a'], ['b']])]
    require(engine.utility(alternative, ['a', 'b']) == 5,
            'An OR contract credited one capacity twice')
    branch = deepcopy(toy)
    branch['actions'] = branch['actions'][:1]
    branch['actions'][0]['duration'] = [1, 1]
    branch['actions'][0]['outcomes'] = [dict(id='success', adds=['a']),
                                       dict(id='no_result', adds=[])]
    branch['capabilities'] = [dict(id='success', weight=5, requires_any=[['a']])]
    require(engine.solve(branch, 1, 'lower')['value'] == 0 and
            engine.solve(branch, 1, 'upper')['value'] == 5,
            'An inconclusive outcome acquired the favourable fact')
    require(engine.solve(branch, 1, 'lower')['first_choices'] == ['STOP', 'a'],
            'A tie with STOP was discarded')

    bad_global = deepcopy(model)
    bad_global['actions'][0]['outcomes'][0]['adds'].append('RH_proved')
    bad_exclusive = deepcopy(model)
    bad_exclusive['initial_facts'] += ['coverage_candidate', 'coverage_gap']
    bad_duration = deepcopy(model)
    bad_duration['actions'][0]['duration'][0] = 0
    invalid_models = [dict(tokens={}, criteria=[], actions=[]),
                      bad_global, bad_exclusive, bad_duration]
    for invalid in invalid_models:
        try:
            engine.validate_model(invalid)
        except ValueError:
            pass
        else:
            raise RuntimeError('A deliberately invalid model was accepted')
    return dict(AND_complementarity_12_over_6=True, OR_capability_counted_once=True,
                STOP_and_ties_preserved=True, explicit_state_and_no_repeated_work=True,
                outcomes_not_guaranteed=True, invalid_models_rejected=len(invalid_models))


def verify(node):
    engine = load_engine()
    model = engine.load_contract_model()
    original = original_payload()
    stripped = {key: value for key, value in model.items()
                if key != '_continuity_provenance'}
    require(stripped == original['model'], 'The retained model differs from document 67')
    canonical = json.dumps(stripped, ensure_ascii=False, sort_keys=True,
                           separators=(',', ':')).encode()
    canonical_sha = hashlib.sha256(canonical).hexdigest()
    require(canonical_sha == model['_continuity_provenance']['model_sha256_before_provenance'],
            'The model provenance hash does not match its content')

    reference_cases = 0
    for row in original['results']['results']:
        for mode in ('lower', 'upper'):
            actual = engine.solve(model, row['budget'], mode)
            for key in ('gain',) + COMPARE_KEYS:
                require(actual[key] == row[mode][key],
                        'Historical reference differs: ' + str((row['budget'], mode, key)))
            reference_cases += 1

    profiles = [dict(zip(('structural', 'local', 'clarity'), values))
                for values in product((1, 2, 3), repeat=3)]
    budgets = list(range(13))
    js_rows = javascript_cases(node, model, profiles, budgets)
    expected_cases = len(profiles) * len(budgets) * 2
    require(len(js_rows) == expected_cases, 'The JavaScript result set is incomplete')
    cases = []
    index = 0
    for factors in profiles:
        weighted = engine.apply_weight_profile(model, factors)
        for budget in budgets:
            for mode in ('lower', 'upper'):
                actual = engine.solve(weighted, budget, mode)
                graph = explicit_graph_solution(weighted, budget, mode)
                for key in COMPARE_KEYS:
                    detail = str((factors, budget, mode, key))
                    require(actual[key] == graph[key], 'Explicit graph mismatch: ' + detail)
                    require(actual[key] == js_rows[index][key], 'JavaScript mismatch: ' + detail)
                cases.append(dict(factors=factors, budget=budget, mode=mode,
                                  value=actual['value'], gain=actual['gain'],
                                  first_choices=actual['first_choices'], states=actual['states']))
                index += 1

    source_paths = [HERE / 'engine.py', HERE / 'bellman_contracts.js',
                    HERE / 'bellman_contrats_v643.json', Path(__file__).resolve(),
                    ORIGINAL_PAGE, ARTICLE]
    source_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in source_paths}
    return dict(
        verification='Finite contract-scenario calculation retained in document 67',
        schema='v655_contract_verification_v1',
        model_from_document67_unchanged=True, canonical_model_sha256=canonical_sha,
        profiles=len(profiles), budgets=budgets, modes=['lower', 'upper'],
        cross_engine_cases=index, independent_explicit_graph_cases=index,
        preserved_original_javascript_cases=index,
        historical_embedded_reference_cases=reference_cases,
        **semantic_guard_checks(engine, model), source_sha256=source_hashes,
        scope=('Correctness of the retained finite declared-scenario calculation only; '
               'no calibration of costs or weights, no certification of current study '
               'outcomes, no validation of mathematical proofs, no global arithmetic '
               'bound, sign law or proof of RH.'), cases=cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Optional receipt JSON, relative to the corpus root')
    parser.add_argument('--node', help='Node executable; otherwise runtime setting or PATH')
    args = parser.parse_args()
    node = args.node or os.environ.get('CODEX_PRIMARY_RUNTIME_NODE') or shutil.which('node')
    require(bool(node), 'Node.js is required; select its executable with --node')
    receipt = verify(node)
    if args.output:
        target = Path(args.output)
        if not target.is_absolute():
            target = ROOT / target
        require(target.parent.is_dir(), 'Receipt parent directory does not exist: ' + str(target.parent))
        target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {key: value for key, value in receipt.items() if key not in ('cases', 'source_sha256')}
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
