#!/usr/bin/env python3
"""Rebuild the four living V6.55 tools and their short navigation.

python -B 2_Methode/Outils/integrate_v655.py --rebuild

The four main views are generated from reviewed data, rather than patched with
successive research banners. Other pieces retain their stated scientific scope.
"""
from pathlib import Path
import argparse,importlib.util,json,re,subprocess,sys,html
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'3_Preuves_et_calculs/data'

def load_module(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def synchronise_pages():
    bi=load_module('indicateur_v655','2_Methode/Indicateur/build_indicateur.py')
    active=json.loads((DATA/'v655_pages_actives.json').read_text())['pages']
    snippets=[str(p.relative_to(ROOT)) for p in (ROOT/'1_Presentation').glob('*_nav.html')]
    active=list(dict.fromkeys(active+snippets))
    config=json.loads((ROOT/'2_Methode/Pilotage/pilotage_recherche.json').read_text())
    primary={p['path'] for p in config['primary_pages']}
    for rel in active:
        if rel in primary:continue
        p=ROOT/rel; text=p.read_text(encoding='utf-8-sig');prefix='../'*(len(Path(rel).parts)-1)
        text=re.sub(r'<aside\b(?=[^>]*data-current=[\'\"]v65[45][\'\"])[^>]*>.*?</aside>','',text,flags=re.S)
        text=re.sub(r'<section\b(?=[^>]*id=[\'\"]v655-research-panel[\'\"])[^>]*>.*?</section>','',text,flags=re.S)
        def recovered_link(m):
            attrs=m[1];target=re.search(r'data-missing-target="([^"]+)"',attrs)
            if not target:return m[0]
            rel=html.unescape(target[1])
            if not (p.parent/rel).is_file():return m[0]
            attrs=re.sub(r'href="[^"]*"',lambda _: 'href="'+html.escape(rel,quote=True)+'"',attrs,count=1)
            attrs=re.sub(r'\s+data-missing-target="[^"]*"','',attrs)
            attrs=re.sub(r'\s+title="Fichier non récupéré[^"]*"','',attrs)
            return '<a'+attrs+'>'
        text=re.sub(r'<a\b([^>]*)>',recovered_link,text)
        nav=bi.topnav('',prefix)
        pattern=r'<nav\b(?=[^>]*class=[\'\"][^\'\"]*\btopnav\b)[^>]*>.*?</nav>'
        if re.search(pattern,text,flags=re.S):text=re.sub(pattern,lambda _:nav,text,count=1,flags=re.S)
        else:text=re.sub(r'(<body\b[^>]*>)',lambda m:m.group(1)+nav,text,count=1)
        p.write_text(text,encoding='utf-8')
    return active

def rebuild():
    for rel in ['3_Preuves_et_calculs/amplification_20261014/generer_html.py',
                '2_Methode/Matrice/build_matrice.py','2_Methode/Figures/build_figures.py',
                '2_Methode/Sources/build_sources.py']:
        args=['--registry-only'] if rel.endswith('build_sources.py') else []
        subprocess.run([sys.executable,'-B',str(ROOT/rel),*args],cwd=ROOT,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--rebuild',action='store_true');args=parser.parse_args()
    if args.rebuild:rebuild()
    linker=load_module('liens_graphes_v655','2_Methode/Pilotage/relier_graphes.py');linker.main()
    steering=load_module('pilotage_v655','2_Methode/Pilotage/build_pilotage.py')
    state=steering.build_all();active=synchronise_pages()
    print(json.dumps(dict(version='6.55',revision=state['revision'],primary_views=4,linked_pages=len(active),historical_calculations_rerun=False),ensure_ascii=False))

if __name__=='__main__':main()
