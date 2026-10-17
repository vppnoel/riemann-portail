"""Compare preserved minimal diagnostics with the nonminimal initial raccord."""
import csv
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps=60
OUT=Path(__file__).resolve().parent
CUTS=(10,100,1000)


def read_json(name):
    return json.loads((OUT/name).read_text())


def read_rows(name):
    return list(csv.DictReader((OUT/name).open()))


def number(value):
    return mp.mpf(value)


def serial(value):
    if isinstance(value,mp.mpf):
        return mp.nstr(value,60)
    if isinstance(value,dict):
        return {key:serial(val) for key,val in value.items()}
    if isinstance(value,(list,tuple)):
        return [serial(val) for val in value]
    return value


comparison=[]
nonminimal_kernels={}
for X in CUTS:
    old=read_json(f'shadow_high_precision_x{X}_summary.json')
    new=read_json(f'nonminimal_x{X}_summary.json')
    rows=read_rows(f'nonminimal_x{X}_rows.csv')
    oldrows=read_rows(f'shadow_high_precision_x{X}_rows.csv')
    kernels=read_json(f'nonminimal_x{X}_kernels.json')
    nonminimal_kernels[X]=kernels
    m=number(new['m'])
    residual=new['residual_after_raccord_and_prime_powers_before_boundary']
    head_mass=number(residual['source_mass_intervals'][0][1])-m
    all_intervals=sorted((number(a),number(b)) for line in kernels
                         for a,b in line['source_mass_intervals'])
    gaps=[abs(all_intervals[0][0]),abs(all_intervals[-1][1]-number(new['source_mass']))]
    gaps += [abs(b-c) for (a,b),(c,d) in zip(all_intervals,all_intervals[1:])]
    after_initial_atom_0=sum(max(0,min(number(b),m)-number(a))
                             for line in kernels[1:]
                             for a,b in line['source_mass_intervals'])
    old_cost=number(old['true_lines_total_quadratic_cost'])+number(old['boundary_quadratic_cost'])
    new_cost=number(new['nonboundary_lines_total_quadratic_cost'])+number(new['boundary_quadratic_cost'])
    comparison.append(dict(
        cutoff=X,prime_power_lines_q_greater_2=new['prime_power_lines_q_greater_2'],
        initial_raccord_lines=1,artificial_boundary_lines=1,
        original_atom_0_before_boundary=number(old['residual_after_true_lines_before_boundary']['atom_0_mass']),
        nonminimal_atom_0_before_boundary=number(residual['atom_0_mass']),
        atom_0_mass_used_after_initial_raccord=after_initial_atom_0,
        nonminimal_compact_head_mass_above_T=head_mass,
        original_max_width=number(old['max_kernel_width']),
        nonminimal_max_width=number(new['max_kernel_width']),
        original_max_transport_distance=max(
            max(number(r['x'])-number(r['source_low']),number(r['source_high'])-number(r['x']))
            for r in oldrows[:-1]),
        nonminimal_max_transport_distance=number(new['max_transport_distance']),
        original_nonboundary_cost=number(old['true_lines_total_quadratic_cost']),
        nonminimal_nonboundary_cost=number(new['nonboundary_lines_total_quadratic_cost']),
        original_boundary_cost=number(old['boundary_quadratic_cost']),
        nonminimal_boundary_cost=number(new['boundary_quadratic_cost']),
        original_total_cost=old_cost,nonminimal_total_cost=new_cost,
        total_cost_difference=new_cost-old_cost,
        max_prime_power_availability_slack_difference=max(
            abs(number(r['availability_slack'])-number(o['availability_slack']))
            for r,o in zip(rows[1:-1],oldrows[1:-1])),
        max_mass_error=number(new['max_atom_mass_error']),
        max_moment_error=number(new['max_atom_moment_error']),
        max_partition_gap_or_overlap=max(gaps),
        residual_source_after_boundary=number(new['residual_source_mass']),
        source_mass=number(new['source_mass']),
        source_first_moment=number(new['source_first_moment']),
        artificial_boundary_mass=number(new['boundary_mass'])))

stability=[]
for small,large in ((10,100),(10,1000),(100,1000)):
    a=nonminimal_kernels[small][:-1]
    b=nonminimal_kernels[large][:-1][:len(a)]
    errors=[]
    for left,right in zip(a,b):
        assert left['atom']==right['atom'] and left['kind']==right['kind']
        assert len(left['source_mass_intervals'])==len(right['source_mass_intervals'])
        for p,q in zip(left['source_mass_intervals'],right['source_mass_intervals']):
            errors.extend(abs(number(x)-number(y)) for x,y in zip(p,q))
    stability.append(dict(small_cutoff=small,large_cutoff=large,
                          matching_nonboundary_lines=len(a),
                          labels_and_piece_counts_match=True,
                          max_source_mass_endpoint_difference=max(errors)))

result=dict(numeric_diagnostic_digits=60,certified_by_intervals=False,
            cutoffs=comparison,prefix_stability=stability,
            fixed_initial_raccord=read_json('nonminimal_x1000_summary.json')['fixed_initial_raccord'])
(OUT/'nonminimal_comparison.json').write_text(json.dumps(serial(result),indent=2))
print(json.dumps(serial(result),indent=2))
