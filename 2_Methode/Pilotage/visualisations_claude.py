"""Reuse the original indicator/navigation graphic grammar with current data.

The originals are build_indicateur.py (small multiples and before/after rails)
and build_navigateur.py (position/target rails). This module changes no levels,
forecasts, contracts, ranking, weights or mathematical status. SVG is rendered
on the server and stays visible without JavaScript and on narrow screens.
"""
from pathlib import Path, PurePosixPath
import html
import json
import math
import posixpath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]


def _esc(value):
    return html.escape(str(value), quote=True)


def _document_path(path):
    if urlsplit(path).scheme:
        return None
    if path.startswith(('1_Presentation/', '2_Methode/', '3_Preuves_et_calculs/', '00_')):
        return posixpath.normpath(path)
    return posixpath.normpath('1_Presentation/' + path)


def _pdf_for(paths):
    candidates = []
    for path in paths:
        normalized = _document_path(path)
        if normalized is None or normalized.startswith('../'):
            continue
        candidate = str(PurePosixPath(normalized).with_suffix('.pdf'))
        if (ROOT / candidate).is_file():
            candidates.append(candidate)
    return next(iter(candidates), None)


def _stage_pdf(stage):
    return _pdf_for([path for _, path in stage.get('documents', [])])


def _stage_links(stage, prefix):
    pdf = _stage_pdf(stage)
    if pdf:
        return f'<a href="{_esc(prefix + pdf)}">Ouvrir le PDF de cette étape</a>'
    paths = [path for _, path in stage.get('documents', [])]
    if paths:
        path = _document_path(paths[0])
        if path:
            return f'<a href="{_esc(prefix + path)}">Ouvrir la pièce de cette étape</a>'
    return '<span>Aucune pièce liée à cette étape.</span>'


STYLE = '''<style>
.cv-instrument{--cv-line:#315a73;--cv-accent:#b56a42;--cv-muted:#657078;--cv-rule:#d9d7cf;--cv-grid:#e6e4dc;--cv-sheet:#fffefa;--cv-band:#f2f0e8;color:inherit;min-width:0;margin:8px 0 24px}
.cv-instrument h3{font-size:1rem;font-weight:650;line-height:1.35;margin:0 0 8px}.cv-instrument p{line-height:1.5}.cv-lead,.cv-question,.cv-caption{font-size:.86rem;color:var(--cv-muted)}.cv-controls{display:flex;gap:16px;flex-wrap:wrap;align-items:end;margin:16px 0}.cv-controls label{display:grid;gap:7px;font-size:.84rem;max-width:100%}.cv-controls select{max-width:100%;background:var(--cv-sheet);font-size:.85rem}.cv-legend{display:flex;gap:10px 22px;flex-wrap:wrap;font-size:.79rem;color:var(--cv-muted);margin:10px 0 18px}.cv-key{display:inline-flex;gap:8px;align-items:center}.cv-dot{width:13px;height:13px;border-radius:50%;display:inline-block;background:var(--cv-line);border:2px solid var(--cv-sheet);box-shadow:0 0 0 1px var(--cv-line)}.cv-dot.before{background:var(--cv-sheet);border:2px solid #8d8a80;box-shadow:none}.cv-dot.target{background:transparent;border:2px dashed #8d8a80;box-shadow:none}.cv-dot.up{background:var(--cv-accent);box-shadow:0 0 0 1px var(--cv-accent)}
.cv-multiples{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:22px}.cv-panel{min-width:0;padding:16px 12px 12px;background:var(--cv-sheet);border:1px solid var(--cv-rule);border-radius:5px}.cv-panel h3{display:flex;gap:8px;justify-content:space-between;align-items:baseline}.cv-panel h3 span{font-family:ui-monospace,Consolas,monospace;color:var(--cv-line);font-size:1rem;flex:none}.cv-question{margin:0 0 8px;min-height:2.8em}.cv-scroll{overflow-x:auto;max-width:100%;overscroll-behavior-x:contain;scrollbar-width:thin;-webkit-overflow-scrolling:touch}.cv-scroll:focus-visible{outline:3px solid var(--cv-accent);outline-offset:3px}.cv-timeline{display:block;height:auto;max-width:none}.cv-timeline text,.cv-rail-svg text{font-family:ui-monospace,Consolas,monospace;font-size:12px;fill:var(--cv-muted)}.cv-timeline text.cv-day{font-size:11px}.cv-timeline a circle{cursor:pointer}.cv-timeline a:hover circle,.cv-timeline a:focus circle{stroke:var(--cv-accent);stroke-width:4}.cv-timeline .cv-level-selected{stroke:var(--cv-accent);stroke-width:4}.cv-selected-step{padding:15px 18px;border-left:3px solid var(--cv-line);background:var(--cv-band);font-size:.9rem;margin:18px 0}.cv-selected-step p{margin:8px 0 0}.cv-selected-step strong{font-weight:650}.cv-rails{display:grid;gap:0}.cv-rail{display:grid;grid-template-columns:minmax(155px,210px) minmax(0,1fr);gap:16px;align-items:center;padding:14px 0;border-top:1px solid var(--cv-rule);min-width:0}.cv-rail-name{font-size:.91rem}.cv-rail-name b{display:block}.cv-rail-name small{font-size:.78rem;line-height:1.4;color:var(--cv-muted);display:block;margin-top:6px}.cv-rail-name a{font-size:.79rem;display:inline-block;margin-top:7px}.cv-rail-svg{display:block;min-width:430px;width:100%;height:auto}.cv-rail-svg .cv-tick{font-size:14px}.cv-rail-value{font-family:ui-monospace,Consolas,monospace;color:var(--cv-line);font-weight:650}.cv-rail-caption{font-size:.78rem;color:var(--cv-muted);margin:2px 0 0}.cv-caption{margin:12px 0 0}.cv-instrument a{overflow-wrap:anywhere}
.cv-rail>div{min-width:0;max-width:100%}
@media(max-width:640px){.cv-multiples{grid-template-columns:minmax(0,1fr)}.cv-panel{padding:15px 10px 12px}.cv-rail{grid-template-columns:minmax(0,1fr);gap:5px}.cv-question{min-height:0}.cv-controls{gap:12px}.cv-controls label{width:100%}.cv-controls select{width:100%}.cv-selected-step{padding:13px 14px}.cv-scroll{margin-bottom:5px}}
@media print{.cv-controls{display:none}.cv-multiples{grid-template-columns:repeat(2,minmax(0,1fr))}.cv-panel{break-inside:avoid;padding:8px}.cv-question{font-size:8pt}.cv-scroll{overflow:visible}.cv-timeline,.cv-rail-svg{min-width:0!important;width:100%!important;max-width:100%;height:auto}.cv-rail{break-inside:avoid;grid-template-columns:155px minmax(0,1fr)}.cv-selected-step{break-inside:avoid}}
</style>'''


def _rail(dim, before, current, target, pdf, prefix, *, compare):
    width, left, right, y = 560, 22, 22, 33
    xx = lambda value: left + (float(value) + .5) * (width-left-right)/10
    marks = []
    for value in range(10):
        x = xx(value)
        marks.append(f'<line x1="{x:.2f}" x2="{x:.2f}" y1="19" y2="48" stroke="var(--cv-grid)"/><text class="cv-tick" x="{x:.2f}" y="69" text-anchor="middle">{value}</text>')
    marks.append(f'<line x1="{left}" x2="{width-right}" y1="{y}" y2="{y}" stroke="var(--cv-rule)"/>')
    if target is not None:
        marks.append(f'<circle cx="{xx(target):.2f}" cy="{y}" r="10" fill="none" stroke="#8d8a80" stroke-width="2" stroke-dasharray="3 3"><title>Marche visée : {_esc(target)}</title></circle>')
    if compare:
        marks.append(f'<path class="cv-rail-arrow" d="" stroke="var(--cv-accent)" stroke-width="3" fill="none"/>')
        marks.append(f'<circle class="cv-rail-before" cx="{xx(before):.2f}" cy="{y}" r="8" fill="var(--cv-sheet)" stroke="#8d8a80" stroke-width="2"/>')
    marks.append(f'<circle class="cv-rail-now" cx="{xx(current):.2f}" cy="{y}" r="6" fill="var(--cv-line)" stroke="var(--cv-sheet)" stroke-width="1.5"/>')
    label = f'{dim["nom"]} : ' + (f'{before} vers ' if compare else '') + str(current)
    piece = f'<a href="{_esc(prefix+pdf)}">Pièce PDF liée à cette évaluation</a>' if pdf else ''
    value_text = f'{before} → {current}' if compare else str(current)
    return (f'<div class="cv-rail" data-cv-dimension="{_esc(dim["id"])}"><div class="cv-rail-name"><b>{_esc(dim["nom"])} '
            f'<span class="cv-rail-value">{_esc(value_text)}</span></b><small>{_esc(dim["question"])}</small>{piece}</div>'
            f'<div><div class="cv-scroll" tabindex="0" role="region" aria-label="Échelle de {_esc(dim["nom"])}"><svg class="cv-rail-svg" viewBox="0 0 {width} 77" role="img" aria-label="{_esc(label)}">'
            + ''.join(marks) + '</svg></div><p class="cv-rail-caption">Échelle de maturité 0 à 9'
            + (f' · marche visée : {_esc(target)}' if target is not None else '') + '</p></div></div>')


def render_navigation_chart(state, prefix='../'):
    """Original seven position/target rails, evaluated from the current state."""
    indicator = state['indicator']
    latest = indicator['etapes'][-1]
    targets = indicator.get('visees', {})
    rails = []
    for dimension in indicator['dimensions']:
        review = state.get('reviews', {}).get(dimension['id'], {})
        pdf = _pdf_for(review.get('evidence', [])) or _stage_pdf(latest)
        rails.append(_rail(dimension, None, latest['niveaux'][dimension['id']],
                           targets.get(dimension['id']), pdf, prefix, compare=False))
    return (STYLE + '<div class="cv-instrument" id="cv-navigation-chart">'
            '<p class="cv-lead">Les sept questions du navigateur gardent leur échelle initiale. Les points pleins montrent l’évaluation courante ; les anneaux pointillés indiquent les marches visées.</p>'
            '<div class="cv-legend"><span class="cv-key"><i class="cv-dot"></i>' + _esc(latest['versions']) + '</span><span class="cv-key"><i class="cv-dot target"></i>Marche visée</span></div>'
            '<div class="cv-rails">' + ''.join(rails) + '</div>'
            '<p class="cv-caption">Les niveaux sont des catégories justifiées par leurs pièces. Les écarts entre ces marques ne mesurent ni une distance à RH, ni une probabilité de preuve. Le Bellman contractuel conserve ses propres données et calculs.</p></div>')


def _timeline(dimension, stages, target, prefix):
    count = len(stages)
    width, height, left, right, top, bottom = max(720, count*18+60), 216, 32, 14, 29, 40
    span = width-left-right
    xs = lambda index: left + (index+.5)*span/count
    ys = lambda level: top+(9-float(level))*(height-top-bottom)/9
    days = []
    for index, stage in enumerate(stages):
        if not days or days[-1]['day'] != stage.get('jour', ''):
            days.append(dict(day=stage.get('jour', ''), start=index, end=index))
        else:
            days[-1]['end'] = index
    pieces = [f'<svg class="cv-timeline" style="width:{width}px" viewBox="0 0 {width} {height}" role="group" aria-label="{_esc(dimension["nom"])} : parcours complet sur {count} étapes, niveaux de maturité 0 à 9">']
    for index, day in enumerate(days):
        x0, x1 = left+day['start']*span/count, left+(day['end']+1)*span/count
        if index % 2 == 0:
            pieces.append(f'<rect x="{x0:.2f}" y="9" width="{x1-x0:.2f}" height="{height-bottom-9}" fill="var(--cv-band)"/>')
        pieces.append(f'<text class="cv-day" x="{x0+3:.2f}" y="20">{_esc(day["day"])}</text>')
    for value in range(10):
        y = ys(value)
        pieces.append(f'<line x1="{left}" x2="{width-right}" y1="{y:.2f}" y2="{y:.2f}" stroke="var(--cv-grid)" stroke-width="{1 if value%3==0 else .6}"/>')
        if value % 3 == 0:
            pieces.append(f'<text x="{left-7}" y="{y+4:.2f}" text-anchor="end">{value}</text>')
    if target is not None:
        y = ys(target)
        pieces.append(f'<line x1="{left}" x2="{width-right}" y1="{y:.2f}" y2="{y:.2f}" stroke="#8d8a80" stroke-dasharray="4 4"/><text x="{width-right-3}" y="{y-5:.2f}" text-anchor="end">visé : {_esc(target)}</text>')
    path = f'M {xs(0):.2f} {ys(stages[0]["niveaux"][dimension["id"]]):.2f}'
    for index in range(1, count):
        path += f' H {xs(index):.2f} V {ys(stages[index]["niveaux"][dimension["id"]]):.2f}'
    pieces.append(f'<path d="{path}" fill="none" stroke="var(--cv-line)" stroke-width="2" stroke-linejoin="round"/>')
    for index, stage in enumerate(stages):
        level = stage['niveaux'][dimension['id']]
        previous = stages[index-1]['niveaux'][dimension['id']] if index else level
        up = index > 0 and level > previous
        why = stage.get('pourquoi', {}).get(dimension['id'], 'Niveau conservé')
        title = f'{stage["versions"]} · {stage.get("jour", "")} · {dimension["nom"]} : {previous} → {level}. {why}'
        pdf = _stage_pdf(stage)
        circle = (f'<circle data-cv-stage="{_esc(stage["id"])}" cx="{xs(index):.2f}" cy="{ys(level):.2f}" r="{5.5 if up else 4}" '
                  f'fill="var(--cv-{ "accent" if up else "line"})" stroke="var(--cv-sheet)" stroke-width="2"><title>{_esc(title)}</title></circle>')
        if pdf:
            circle = f'<a href="{_esc(prefix+pdf)}" aria-label="{_esc(title)} · Ouvrir le PDF">{circle}</a>'
        pieces.append(circle)
        if index % max(1, math.ceil(count/11)) == 0 or index == count-1:
            pieces.append(f'<text x="{xs(index):.2f}" y="{height-10}" text-anchor="middle">{_esc(stage["court"])}</text>')
    pieces.append('</svg>')
    return ''.join(pieces)


def render_indicator_chart(state, prefix='../'):
    """Original small multiples plus dynamic before/after comparison rails."""
    indicator = state['indicator']
    stages, dimensions = indicator['etapes'], indicator['dimensions']
    require_ids = {stage['id']: stage for stage in stages}
    comparison = indicator.get('comparaison', {})
    before = require_ids.get(comparison.get('avant'), stages[0])
    current = require_ids.get(comparison.get('apres'), stages[-1])
    targets = indicator.get('visees', {})
    panels, rails = [], []
    for dimension in dimensions:
        panels.append('<article class="cv-panel"><h3>' + _esc(dimension['nom']) + '<span>' + str(stages[-1]['niveaux'][dimension['id']]) + '</span></h3><p class="cv-question">' + _esc(dimension['question']) + '</p>'
                      '<div class="cv-scroll cv-timeline-scroll" tabindex="0" role="region" aria-label="Parcours chronologique de ' + _esc(dimension['nom']) + '">' + _timeline(dimension, stages, targets.get(dimension['id']), prefix) + '</div></article>')
        pdf = _pdf_for(state.get('reviews', {}).get(dimension['id'], {}).get('evidence', [])) or _stage_pdf(current)
        rails.append(_rail(dimension, before['niveaux'][dimension['id']], current['niveaux'][dimension['id']],
                           targets.get(dimension['id']), pdf, prefix, compare=True))

    def options(selected):
        return ''.join(f'<option value="{_esc(stage["id"])}"' + (' selected' if stage['id'] == selected else '') + f'>{_esc(stage["versions"])} · {_esc(stage.get("jour", ""))}</option>' for stage in stages)

    payload = json.dumps(dict(stages=[dict(id=stage['id'], versions=stage['versions'],
                                          levels=stage['niveaux'], summary=stage['franchi'],
                                          piece_html=_stage_links(stage, prefix)) for stage in stages]), ensure_ascii=False).replace('</', '<\\/')
    script = '''<script>(function(){
const host=document.getElementById('cv-indicator-chart');if(!host)return;
const data=JSON.parse(host.querySelector('[data-cv-history]').textContent),by=new Map(data.stages.map(s=>[s.id,s]));
const step=host.querySelector('[data-cv-step]'),first=host.querySelector('[data-cv-before]'),last=host.querySelector('[data-cv-after]');
function inspect(){const s=by.get(step.value);host.querySelector('[data-cv-step-title]').textContent=s.versions;host.querySelector('[data-cv-step-summary]').textContent=s.summary;host.querySelector('[data-cv-step-piece]').innerHTML=s.piece_html;host.querySelectorAll('[data-cv-stage]').forEach(c=>{const selected=c.dataset.cvStage===s.id;c.classList.toggle('cv-level-selected',selected);if(selected){const pane=c.closest('.cv-scroll');if(pane)pane.scrollLeft=Math.max(0,Number(c.getAttribute('cx'))-pane.clientWidth/2)}})}
function compare(){const a=by.get(first.value),b=by.get(last.value),xx=v=>22+(Number(v)+.5)*516/10;host.querySelectorAll('[data-cv-dimension]').forEach(row=>{const key=row.dataset.cvDimension,x=a.levels[key],y=b.levels[key],old=xx(x),now=xx(y),direction=now>=old?1:-1;row.querySelector('.cv-rail-before').setAttribute('cx',old);row.querySelector('.cv-rail-now').setAttribute('cx',now);row.querySelector('.cv-rail-value').textContent=x+' → '+y;row.querySelector('svg').setAttribute('aria-label',key+' : '+x+' vers '+y);row.querySelector('.cv-rail-arrow').setAttribute('d',x===y?'':'M '+old+' 33 H '+now+' M '+(now-direction*7)+' 28 L '+now+' 33 L '+(now-direction*7)+' 38')})}
step.addEventListener('change',inspect);first.addEventListener('change',compare);last.addEventListener('change',compare);inspect();compare();
})();</script>'''
    return (STYLE + '<div class="cv-instrument" id="cv-indicator-chart"><h3>Les sept questions, depuis le début</h3>'
            '<p class="cv-lead">La courbe en marches, les bandes de dates, les points de hausse et les seuils visés reprennent le dessin initial. Toutes les étapes sont calculées depuis le registre courant.</p>'
            '<div class="cv-legend"><span class="cv-key"><i class="cv-dot"></i>Niveau déclaré</span><span class="cv-key"><i class="cv-dot up"></i>Hausse constatée</span><span class="cv-key"><i class="cv-dot target"></i>Marche visée</span></div>'
            '<p class="cv-caption">Sur téléphone, faites glisser les graphiques horizontalement. Les points liés ouvrent leur PDF ; la liste ci-dessous permet de choisir une étape avec une cible tactile plus grande.</p>'
            '<div class="cv-multiples">' + ''.join(panels) + '</div>'
            '<div class="cv-controls"><label>Étape à consulter<select data-cv-step>' + options(stages[-1]['id']) + '</select></label></div>'
            '<div class="cv-selected-step"><strong data-cv-step-title>' + _esc(stages[-1]['versions']) + '</strong><p data-cv-step-summary>' + _esc(stages[-1]['franchi']) + '</p><p data-cv-step-piece>' + _stage_links(stages[-1], prefix) + '</p></div>'
            '<h3>Comparer deux étapes sur l’échelle initiale</h3><div class="cv-controls"><label>Avant<select data-cv-before>' + options(before['id']) + '</select></label><label>Après<select data-cv-after>' + options(current['id']) + '</select></label></div>'
            '<div class="cv-legend"><span class="cv-key"><i class="cv-dot before"></i>Avant</span><span class="cv-key"><i class="cv-dot"></i>Après</span><span class="cv-key"><i class="cv-dot target"></i>Marche visée</span></div>'
            '<div class="cv-rails">' + ''.join(rails) + '</div>'
            '<p class="cv-caption">Une étape peut ajouter un lemme ou éliminer une méthode sans changer le niveau de la question générale. Les raisons et les limites sont conservées dans les évaluations ; ces niveaux ne s’additionnent pas en pourcentage de RH.</p>'
            '<script type="application/json" data-cv-history>' + payload + '</script>' + script + '</div>')
