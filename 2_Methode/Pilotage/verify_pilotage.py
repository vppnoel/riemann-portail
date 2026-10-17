"""Check documentary continuity and the four rendered views; no scientific replay.

Run after integrate_v655.py --rebuild. Contract calculation has its independent
verifier verify_contracts.py. Browser interactions have a separate QA receipt.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import importlib.util,json,re,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
builder=module('builder_check',HERE/'build_pilotage.py')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.nav=0;self.navlinks=0;self.primary=[];self.resources=[];self.tools=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='nav' and 'topnav' in a.get('class','').split():self.nav+=1
  if tag=='a' and self.nav:
   self.navlinks+=1
   if 'data-primary' in a:self.primary.append(a['data-primary'])
   if 'data-resource' in a:self.resources.append(a['data-resource'])
   if 'data-tool-link' in a:self.tools.append(a['data-tool-link'])
  if tag in ['a','img','object']:
   value=a.get({'a':'href','img':'src','object':'data'}[tag]);
   if value:self.links.append(value)
 def handle_endtag(self,tag):
  if tag=='nav' and self.nav:self.nav-=1

def main():
 s=builder.load_state();nodes={n['id']:n for n in s['nodes']}
 assert len(nodes)==len(s['nodes'])==69
 assert len({n['uid'] for n in s['nodes']})==69
 assert all(nodes[k]['status']=='ouvert' for k in ['RH','global_sign','J_bound','large_q','Q_bound'])
 for source in ['global_sign','coverage']:
  e=next(e for e in s['edges'] if e['source']==source and e['target']=='weil_all');assert set(e['requires'])=={'global_sign','coverage'}
 for source in ['copies','head','large_q']:
  e=next(e for e in s['edges'] if e['source']==source and e['target']=='threequarters');assert set(e['requires'])=={'copies','head','large_q'}
 assert set(nodes)=={k for e in s['edges'] for k in [e['source'],e['target']]}
 nav=json.loads((ROOT/'2_Methode/Navigateur/carte_navigation.json').read_text(encoding='utf-8-sig'))
 assert len(s['reviews'])==7 and len(s['actions'])==len(nav['coups'])>=99 and len({c['id'] for c in s['actions']})==len(s['actions'])
 rec=json.loads((ROOT/'RECUPERATION_2026_10_14.json').read_text())
 assert s['missing_historical_sources']==[p for p in rec['missing_source_paths_from_v649_index'] if not (ROOT/p).exists()]
 assert s['historical_recovery_complete']==(not s['missing_historical_sources'] and not s['missing_separate_notes'] and not s['missing_later_sources'])
 reg=s['reference_registry'];numbers={d['number'] for d in reg['documents']};assert numbers==set(range(1,max(numbers)+1)) and max(numbers)>=79
 for d in reg['documents']:
  for p in d['paths']:assert (ROOT/p).is_file(),p
 issues=[];nlinks=0
 for v in s['primary_pages']:
  path=ROOT/v['path'];text=path.read_text();parser=Links();parser.feed(text)
  assert parser.navlinks==12,(v['id'],parser.navlinks)
  assert parser.primary==[p['id'] for p in s['primary_pages']]
  assert parser.resources==['atlas','matrice','references-pdf','references','figures','articles','dossiers']
  assert parser.tools==['bellman']
  assert f'content="{s["fingerprint"]}"' in text
  assert len(parser.ids)==len(set(parser.ids)),('duplicate HTML ID',v['id'])
  for link in parser.links:
   u=urlsplit(link)
   if u.scheme or u.netloc:continue
   target=path.parent/unquote(u.path) if u.path else path
   if not target.exists():issues.append((v['path'],link));continue
   nlinks+=1
   if u.fragment and target.suffix=='.html':
    if u.fragment.startswith('node='):
     assert u.fragment[5:] in {n['uid'] for n in s['nodes']}|set(nodes)
    elif u.fragment.startswith('case='):
     assert u.fragment[5:] in {c['id'] for c in s['graph_cases']}
    elif not re.search(r'\bid=[\"\']'+re.escape(u.fragment)+r'[\"\']',target.read_text(encoding='utf-8-sig')):
     issues.append((v['path'],link))
 assert not issues,issues
 cases=s['graph_cases'];assert len(cases)==72 and len({c['id'] for c in cases})==72
 assert next(c for c in cases if c['id']=='G68.case07')['ideas'][0]=='IDE-047'
 assert next(c for c in cases if c['id']=='G65.jet')['ideas'][0]=='IDE-043'
 fig=json.loads((ROOT/'2_Methode/Figures/registre_figures.json').read_text())['figures']
 assert len(fig)==len({f['id'] for f in fig})
 assert all((ROOT/f['fichier']).is_file() for f in fig)
 assert len(re.findall('data-node=',builder.retained_graph(s)))==42
 mapped={k for spec in builder.advanced.MAPS.values() for k in spec['positions']}
 assert set(nodes)-{n['id'] for n in s['nodes'][:42]}<=mapped
 for key,name in builder.advanced.EXPORTS.items():
  assert (ROOT/'1_Presentation'/name).is_file()
  assert 'class="advanced-svg"' in (ROOT/'1_Presentation'/name).read_text()
 catalogue=s['catalogue'];entries=catalogue['entries'];files={e['path'] for e in entries if e['path']}
 assert len(files)==catalogue['file_count']
 assert {e['id'] for e in entries if e['kind']=='fiches'}=={n['uid'] for n in s['nodes']}
 nsources=len(json.loads((ROOT/'2_Methode/Sources/sources.json').read_text(encoding='utf-8-sig')))
 assert len([e for e in entries if e['kind']=='references'])==nsources>=176
 assert len({e['id'] for e in entries})==len(entries)
 for e in entries:
  if e['path']:assert (ROOT/e['path']).is_file(),e['path']
  assert set(e['related'])<=files,(e['id'],set(e['related'])-files)
  assert set(e['ideas'])<={n['uid'] for n in s['nodes']}
 for n in s['nodes']:
  assert all(r['path'] in files for r in n['linked_resources'])
  assert set(n['reference_keys'])<={r['cle'] for r in json.loads((ROOT/'2_Methode/Sources/sources.json').read_text())}
 print(json.dumps(dict(primary_views=4,internal_links_checked=nlinks,actions_preserved=len(s['actions']),targeted_action_corrections=13,
  dimensions_documentarily_reassessed=7,stable_ideas=69,stable_documents=max(numbers),linked_graph_cases=72,
  figures_with_stable_ids=len(fig),advanced_2d_maps=3,advanced_mapped_ideas=len(mapped),menu_resources=7,direct_bellman=True,catalogued_files=len(files),catalogued_idea_cards=69,catalogued_reference_cards=nsources,AND_guards=True,missing_v649_scripts_modules=len(s['missing_historical_sources']),
  missing_separate_notes=len(s['missing_separate_notes']),missing_later_sources=len(s['missing_later_sources']),scientific_replay=False),ensure_ascii=False))
if __name__=='__main__':main()
