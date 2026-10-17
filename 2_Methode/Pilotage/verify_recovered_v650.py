#!/usr/bin/env python3
"""Recheck original sources recovered from the V6.50 archive, without rewriting them.

Run from any directory with mpmath 1.3.0 and NumPy installed:
  python3 -B 2_Methode/Pilotage/verify_recovered_v650.py
  python3 -B 2_Methode/Pilotage/verify_recovered_v650.py \
    --output 3_Preuves_et_calculs/data/v655_verification_sources_retrouvees.json

Execution is read-only by default, including disabled bytecode. --output writes
only the requested receipt. Relative output paths start at the corpus root.
The original tests are zero-argument functions without pytest fixtures; their
assertions are executed directly, unmodified. Python -O is therefore refused.

The checks cover recovered bytes, syntax, saved finite certificates, exact
algebra and the declared Bellman calculation. They do not replay every original
experiment or validate all analytic proofs. No global sign law, bound or RH
proof is inferred from recovery or from a passing finite check.
"""
from pathlib import Path
from itertools import product
import argparse
import ast
import hashlib
import importlib.util
import inspect
import json
import sys
import time
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROOF = ROOT / '3_Preuves_et_calculs'

# Byte references from the user-supplied original V6.50 archive. These reference
# hashes do not depend on that ZIP still being present when this program runs.
ORIGINAL_ARCHIVE = 'programme-riemann_github_v6_50(1).zip'
ORIGINAL_ARCHIVE_SHA256 = 'b5d996824beb3fc29279ea388b958abfb008fa0800ffc0a487ca09451de965c1'
EXPECTED_SOURCE_SHA256 = {
    "3_Preuves_et_calculs/scripts/check_v642_certificate.py": "642b915e9bb1cd08f06000426bfe030773e627811e21c9f5f42ca1a24ae28224",
    "3_Preuves_et_calculs/scripts/check_v647_links.py": "45f9dc5c3a5bbae7396f294962aa0f11b209dc2e6fbae4a59b9c49d1cbb56368",
    "3_Preuves_et_calculs/scripts/check_v648_links.py": "979b03c57ff64485d0908a8d50ad00978f8b8862b7fe6e14dad44772375a4f92",
    "3_Preuves_et_calculs/scripts/check_v649_links.py": "d4ef48078f357b2d64b85e7532970cc6ac27c9c04146e7402499ca60e4c0d9e4",
    "3_Preuves_et_calculs/scripts/run_v642_bellman.py": "ee3d9a59fde7c9572df6ef8fffb7a289399be0349e806c5ac78d8a69b6460a47",
    "3_Preuves_et_calculs/scripts/run_v642_certification.py": "529a0c2717c3dcbf5f4649f9e30829e631eed513a5ac969e02c1dad62d196b34",
    "3_Preuves_et_calculs/scripts/run_v643_bridges.py": "0a8f4f7256a1569c94dd2a07f038398f3b5aa9f1c78f1cbb18ffdb31def36469",
    "3_Preuves_et_calculs/scripts/v644_family_experiment.py": "203286ca86905935afc18cb0dd43b922b3de160ca47e451d5bc181b3d3089182",
    "3_Preuves_et_calculs/scripts/v644_integer_tail.py": "c973e07e9e8a42462c8fffa238982c29cac63afce51aea9a16a7371825854fae",
    "3_Preuves_et_calculs/scripts/v645_arithmetic_experiment.py": "1dbd8f2d4bcffa2b668a37e5c293ac2fc5d8b312a8b1aee16ea3b463fa7cc4bf",
    "3_Preuves_et_calculs/scripts/v645_compensation_directions.py": "af668fa7b5af774bddc8736a4e7efd6d23515b4ea7082731498df3c3aea77c1f",
    "3_Preuves_et_calculs/scripts/v646_fourier_joint_diagnostic.py": "bc888229cd1266066e220f193770ab40ec76add0c3a60b9ba04f56886fc8560c",
    "3_Preuves_et_calculs/scripts/v646_lego_experiment.py": "b8731bc5a7665dc1ea9a24aa3de67d43804a5edaabd309b9c55eb0b14b4e80ff",
    "3_Preuves_et_calculs/scripts/v647_concentration_experiment.py": "8c49a1afe9082407eb32e7b5ede38c4b44b53e24ecfef9d5f5cb0c953b4cd13e",
    "3_Preuves_et_calculs/scripts/v647_operator_diagnostic.py": "daf845ebf33de757e5834b9d3da49ca0b57f156c252d75c3c87130db8de48ac1",
    "3_Preuves_et_calculs/scripts/v648_common_certificate_experiment.py": "3404ef06b707ad9af5f9ea01c38c5035bd328e96e8f26f9732e47bbc90287259",
    "3_Preuves_et_calculs/scripts/v648_common_operator_diagnostic.py": "30be1e1bce61128511549813c5d74458cf809c42e2d23be72083952b23e01c75",
    "3_Preuves_et_calculs/scripts/v649_joint_payment_experiment.py": "5498bb1f58974c153ca0353620f5f72c0121c31504cc1b2238c2440d5a4a67d3",
    "3_Preuves_et_calculs/scripts/v649_multi_prime_diagnostic.py": "bd3dad29da93271298c936a4b45e55b6449685b0afab4fe9c9d9b46d968c78bc",
    "3_Preuves_et_calculs/src/bridge_planning.py": "05d29a79c819fd98ceed68f126b12a2f6c87a88320bf27bbd8deaa6c1eb9de2d",
    "3_Preuves_et_calculs/src/certificate_lego.py": "2208a6b0eec784db12ce9bc7b47990af207be0663facd48d94985e98164b1198",
    "3_Preuves_et_calculs/src/common_operator_certificate.py": "80eb332e7aa818e032b3cf286efebc65dffffb6a49eec831d6c814f6005d4dfc",
    "3_Preuves_et_calculs/src/domain_grammar.py": "6e191500c80ab409edecdcacf80d04f036fc3cac80bd11ae0b2e93c60d71c84f",
    "3_Preuves_et_calculs/src/multi_prime_compensation.py": "5ee6e0b2830014093796695e943e63795e6c24ab36e2d67aac7f3d18a5781bca",
    "3_Preuves_et_calculs/src/projected_concentration.py": "883ca28fd3874bc9e69f763a8a61fb26482d4e1affeaedfb4c7978354c6ab4e5",
    "3_Preuves_et_calculs/src/schur_bridge.py": "75b62ccb9e8f8fb7f9cb00d554964bba53bf406f8e56f4e92f47dfb722194aa0",
    "3_Preuves_et_calculs/src/v642_intervalles.py": "a6169a58d2e089ef962c264e3cf4e792316ece54b99c7e028f58bdf350913d94",
    "3_Preuves_et_calculs/preuves/V642_CERTIFICATION_LOCALE.md": "50f1b7077be9d0756f7ae6d6efcd73ecc6a64309c5368163de74cbe7779d638d",
    "3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md": "f7eb07778900653147cbc3de40cbd8586afba58e6e5c00c77fcbdf46ced957a6",
    "3_Preuves_et_calculs/preuves/V643_PONTS_MATHEMATIQUES.md": "9aab283244c86a9d0ff51c5bb2ee5f543f06aa6c0ccb44b9a05020d4e22a92bf"
}
MODEL_SHA256 = '7829fe9cd93269aef6350ead4aabbb1819c956c755b60b6c96d36c4263d9448d'
TEST_FILES = (
    'test_v642_certification.py', 'test_v643_bridges.py',
    'test_v644_domain_language.py', 'test_v645_prime_centered_bridge.py',
    'test_v646_certificate_lego.py', 'test_v647_projected_concentration.py',
    'test_v648_common_operator_certificate.py', 'test_v649_multi_prime_compensation.py',
)
EXCLUDED_CURRENT_TESTS = frozenset({
    'test_v644_domain_language.py::test_current_registry_covers_69_documents_and_matches_sources',
    'test_v645_prime_centered_bridge.py::test_current_dictionary_supplements_history_and_index_parses_all_code',
    'test_v645_prime_centered_bridge.py::test_current_registry_and_global_progress_match_research_scope',
    'test_v646_certificate_lego.py::test_current_registry_index_and_four_doors_are_consistent',
    'test_v647_projected_concentration.py::test_current_lessons_have_progressive_prerequisites_and_concrete_uses',
    'test_v648_common_operator_certificate.py::test_current_dictionary_prerequisites_and_source_scope_are_explicit',
    'test_v648_common_operator_certificate.py::test_current_support_and_global_obligations_are_not_confused',
    'test_v649_multi_prime_compensation.py::test_current_course_and_tools_have_ordered_prerequisites_and_scope',
    'test_v649_multi_prime_compensation.py::test_current_state_retains_prior_support_certificate_and_does_not_promote_diagnostic',
})
COMPARE_KEYS = ('value', 'gain', 'first_choices', 'choice_values', 'outcome_values', 'states')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def check_recovered_bytes():
    observed = {}
    parsed = []
    for relative, expected in EXPECTED_SOURCE_SHA256.items():
        path = ROOT / relative
        require(path.is_file(), 'Recovered original is missing: ' + relative)
        actual = sha256(path)
        require(actual == expected, 'Recovered bytes differ from the original ZIP: ' + relative)
        observed[relative] = actual
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8-sig'), filename=relative)
            parsed.append(relative)
    require(len(parsed) == 27 and len(observed) == 30, 'The targeted recovery inventory changed')
    return observed, parsed


def compare_bridge_models_and_engines(engine, recovered):
    stored_path = PROOF / 'data/v643_modele_ponts.json'
    original = json.loads(stored_path.read_text(encoding='utf-8-sig'))
    require(canonical_hash(original) == MODEL_SHA256,
            'Stored V643 model differs from the model recovered in the original ZIP')
    retained = engine.load_contract_model()
    require({key: value for key, value in retained.items()
             if key != '_continuity_provenance'} == original,
            'Restored contract model differs from the original V643 model')
    comparisons = []
    for factors in product((1, 2, 3), repeat=3):
        profile = dict(zip(('structural', 'local', 'clarity'), factors))
        weighted = engine.apply_weight_profile(original, profile)
        for budget in range(13):
            for mode in ('lower', 'upper'):
                old = recovered.solve(weighted, budget, mode)
                new = engine.solve(weighted, budget, mode)
                graph = recovered.bottom_up(weighted, budget, mode)
                label = str((profile, budget, mode))
                for key in COMPARE_KEYS:
                    require(old[key] == new[key], 'Recovered/restored engine mismatch: ' + label + ' ' + key)
                require(old['value'] == graph['value'] and old['first_choices'] == graph['first_choices'],
                        'Recovered explicit graph mismatch: ' + label)
                comparisons.append(dict(profile=profile, budget=budget, mode=mode,
                                        value=new['value'], gain=new['gain'],
                                        first_choices=new['first_choices'], states=new['states']))

    # These four facts and two bounded studies are the explicitly reviewed
    # continuity scenario, not an automatic consequence of completing a task.
    facts = original['initial_facts'] + [
        'regularization_assessed', 'coverage_candidate', 'debt_assessed', 'open_debt']
    completed = ['regime_commun', 'dette_schur']
    current = []
    for budget in range(13):
        for mode in ('lower', 'upper'):
            old = recovered.solve(original, budget, mode, initial=facts, done=completed)
            new = engine.solve(original, budget, mode, facts=facts, completed=completed)
            graph = recovered.bottom_up(original, budget, mode, initial=facts, done=completed)
            for key in COMPARE_KEYS:
                require(old[key] == new[key], 'Reconciled state mismatch: ' + str((budget, mode, key)))
            require(new['value'] == graph['value'] and new['first_choices'] == graph['first_choices'],
                    'Reconciled explicit graph mismatch: ' + str((budget, mode)))
            current.append(dict(budget=budget, mode=mode, value=new['value'], gain=new['gain'],
                                first_choices=new['first_choices'], states=new['states']))
    return dict(
        exact_model_matches_original=True, canonical_model_sha256=MODEL_SHA256,
        original_state_cases=len(comparisons), reconciled_state_cases=len(current),
        original_bottom_up_cases=len(comparisons), reconciled_bottom_up_cases=len(current),
        compared_fields=list(COMPARE_KEYS), profiles=27, budgets=list(range(13)),
        reconciled_scenario=dict(
            facts=facts, completed=completed,
            sources=[
                '1_Presentation/68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.md',
                '1_Presentation/70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.md',
                '1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.md',
                '1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.md'],
            scope=('Bounded family/debt studies examined; qualitative coverage and open '
                   'arithmetic debt. Global obligations remain partial/open. No favourable '
                   'outcome on the A-fixed fibre is credited. This verifier checks numerical '
                   'agreement for that declared state, not its scientific attestation.')),
        cases=comparisons, reconciled_cases=current)


def run_original_test_functions():
    loaded = []
    # Match collection-before-execution semantics. All selected tests are plain
    # functions; no fixture, parametrization or framework hook is substituted.
    for name in TEST_FILES:
        loaded.append((name, module('recovered_readonly_' + name[:-3], PROOF / 'tests' / name)))
    results = []
    excluded = []
    by_module = []
    for name, loaded_module in loaded:
        before = len(results)
        for key, function in loaded_module.__dict__.items():
            if not (key.startswith('test_') and inspect.isfunction(function) and
                    function.__module__ == loaded_module.__name__):
                continue
            test_id = name + '::' + key
            if test_id in EXCLUDED_CURRENT_TESTS:
                excluded.append(test_id)
                continue
            require(not inspect.signature(function).parameters,
                    'Fixture-dependent test requires a real framework: ' + test_id)
            start = time.monotonic()
            try:
                function()
                result = dict(test=test_id, status='passed')
            except Exception as error:
                result = dict(test=test_id, status='failed',
                              error=type(error).__name__ + ': ' + str(error),
                              traceback=traceback.format_exc())
            result['seconds'] = round(time.monotonic() - start, 4)
            results.append(result)
        group = results[before:]
        by_module.append(dict(module=name, passed=sum(item['status'] == 'passed' for item in group),
                              failed=sum(item['status'] == 'failed' for item in group)))
    require(set(excluded) == EXCLUDED_CURRENT_TESTS, 'The nine editorial exclusions changed')
    require(len(results) == 85, 'The original functional test inventory changed')
    return dict(
        runner='Direct execution of original zero-argument test functions, with their assertions',
        selected=len(results), passed=sum(item['status'] == 'passed' for item in results),
        failed=sum(item['status'] == 'failed' for item in results),
        excluded_current_editorial_tests=excluded,
        exclusion_scope=('These nine tests compare frozen older current pages/indexes or '
                         'version markers. They are excluded here, not reported as passing. '
                         'Current interface consistency needs the V655 continuity checks.'),
        modules=by_module, cases=results)


def verify():
    require(__debug__, 'Run without -O: the original test assertions must remain active')
    sys.path[:0] = [str(PROOF / 'src'), str(PROOF / 'scripts')]
    try:
        import mpmath
        import numpy
        import bridge_planning
    except ImportError as error:
        raise RuntimeError('Install the declared mpmath/NumPy dependencies and restore the original sources') from error
    require(Path(bridge_planning.__file__).resolve() == (PROOF / 'src/bridge_planning.py').resolve(),
            'A different bridge_planning module was imported')
    started = time.monotonic()
    before, syntax_checked = check_recovered_bytes()
    engine = module('restored_contract_engine_for_recovery', HERE / 'engine.py')
    bellman = compare_bridge_models_and_engines(engine, bridge_planning)
    tests = run_original_test_functions()
    after, _ = check_recovered_bytes()
    require(before == after, 'An original targeted source changed during verification')
    receipt = dict(
        schema='v655_recovered_source_verification_v1',
        reference_archive=dict(name=ORIGINAL_ARCHIVE, sha256=ORIGINAL_ARCHIVE_SHA256),
        targeted_originals=30, python_sources_syntax_checked=len(syntax_checked),
        expected_original_sha256=EXPECTED_SOURCE_SHA256,
        protected_targets_unchanged=True,
        dependencies=dict(python=sys.version.split()[0], mpmath=mpmath.__version__, numpy=numpy.__version__),
        bellman=bellman, tests=tests, seconds=round(time.monotonic()-started, 4),
        calculation_and_tests_passed=(tests['failed'] == 0),
        scope=('Original byte recovery and finite regression checks only. No experiments '
               'are silently regenerated; the complete historical experiment suite and '
               'all analytic premises are not revalidated. Passing checks do not establish '
               'a global arithmetic bound, global Weil positivity, a sign law, or RH. '
               'Matching an archive hash identifies that supplied archive; it is not an '
               'independent validation of every original scientific claim.'))
    source_paths = [Path(__file__).resolve(), HERE / 'engine.py', HERE / 'bellman_contrats_v643.json',
                    PROOF / 'data/v643_modele_ponts.json'] + [PROOF / 'tests' / name for name in TEST_FILES]
    receipt['verification_source_sha256'] = {
        str(path.relative_to(ROOT)): sha256(path) for path in source_paths}
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Optional JSON receipt; relative to corpus root')
    args = parser.parse_args()
    receipt = verify()
    if args.output:
        target = Path(args.output)
        if not target.is_absolute():
            target = ROOT / target
        require(target.parent.is_dir(), 'Receipt parent directory does not exist')
        target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(
        targeted_originals=receipt['targeted_originals'],
        python_sources_syntax_checked=receipt['python_sources_syntax_checked'],
        protected_targets_unchanged=receipt['protected_targets_unchanged'],
        bellman_original_cases=receipt['bellman']['original_state_cases'],
        bellman_reconciled_cases=receipt['bellman']['reconciled_state_cases'],
        original_bottom_up_cases=receipt['bellman']['original_bottom_up_cases'],
        reconciled_bottom_up_cases=receipt['bellman']['reconciled_bottom_up_cases'],
        functional_tests_passed=receipt['tests']['passed'],
        functional_tests_failed=receipt['tests']['failed'],
        editorial_tests_excluded=len(receipt['tests']['excluded_current_editorial_tests']),
        dependencies=receipt['dependencies'], seconds=receipt['seconds'], scope=receipt['scope']),
        ensure_ascii=False))
    if not receipt['calculation_and_tests_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
