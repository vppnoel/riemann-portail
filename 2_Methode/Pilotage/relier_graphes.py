"""Bind graph cases and SVG boxes to stable ideas without changing their science."""
from pathlib import Path
import json,re,html,xml.etree.ElementTree as E,base64
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
NS='http://www.w3.org/2000/svg';XL='http://www.w3.org/1999/xlink'
E.register_namespace('',NS);E.register_namespace('xlink',XL)

HELPER=r'''/* BEGIN WORKED REFERENCES */
function attachWorkedReference(n,box){
 const aside=document.createElement('aside');aside.dataset.workedReference=n.case_reference;
 aside.style.cssText='padding:12px;margin:0 0 16px;border:1px solid #8daebd;background:#eef5f8;font-size:14px';
 const title=document.createElement('strong');title.textContent='Case '+n.case_reference+' · travail et bilan actuels';aside.append(title);
 for(const [i,ref] of n.work_references.entries()){const p=document.createElement('p'),a=document.createElement('a');a.href='../00_Carte_des_idees.html#node='+ref.uid;a.textContent=(i?'Lien de travail : ':'Idée principale : ')+ref.uid+' · '+ref.title;p.append(a);aside.append(p);}
 if(n.worked_primary_source){const p=document.createElement('p'),a=document.createElement('a');a.href='../'+n.worked_primary_source;a.textContent=n.worked_primary_source_label||'Source propre de cette case';p.append(a);aside.append(p);}
 if(n.worked_reference_note){const p=document.createElement('p');p.textContent=n.worked_reference_note;aside.append(p);}
 for(const ref of n.related_work_references||[]){const p=document.createElement('p'),a=document.createElement('a');a.href='../00_Carte_des_idees.html#node='+ref.uid;a.textContent='Parenté, résultat distinct : '+ref.uid+' · '+ref.title;p.append(a);if(n.worked_relation)p.append(document.createTextNode(' — '+n.worked_relation));aside.append(p);}
 const p=document.createElement('p'),a=document.createElement('a');a.href='../'+n.worked_document;a.textContent='Ouvrir le dossier conservé (document '+n.worked_document_number+')';p.append(a);aside.append(p);
 if(n.original_source_missing){const note=document.createElement('p');note.textContent='La source séparée autrefois référencée n’est pas récupérée. Le dossier PDF conservé reste accessible ; le texte du nœud n’est pas présenté comme un nouveau rejeu.';aside.append(note);}
 box.append(aside);
}
/* END WORKED REFERENCES */
'''

def main():
 c=json.loads((HERE/'pilotage_recherche.json').read_text());nodes={n['id']:n for n in c['nodes']};cases=[]
 views={v['id']:v for v in c['graph_views']}
 for view in c['graph_views']:
  p=ROOT/view['path'];text=p.read_text(encoding='utf-8-sig')
  pattern=r'(<script\b[^>]*id="'+re.escape(view['data_id'])+r'"[^>]*>)(.*?)(</script>)'
  match=re.search(pattern,text,re.S);assert match,view['path']
  payload=json.loads(match.group(2));g=payload[view['container']] if view['container'] else payload
  assert {n['id'] for n in g['nodes']}==set(view['mapping']),view['path']
  pdf=next(p for p in (ROOT/'1_Presentation').glob(f'{view["document"]:02d}_*.pdf'))
  for n in g['nodes']:
   refs=[nodes[k] for k in view['mapping'][n['id']]]
   annotation=view.get('case_annotations',{}).get(n['id'],{})
   related=[nodes[k] for k in annotation.get('related_nodes',[])]
   if annotation.get('primary_source'):assert (ROOT/annotation['primary_source']).is_file(),annotation['primary_source']
   n['case_reference']=view['id']+'.'+n['id']
   n['work_references']=[dict(uid=x['uid'],key=x['id'],title=x['title']) for x in refs]
   n['worked_primary_source']=annotation.get('primary_source')
   n['worked_primary_source_label']=annotation.get('primary_source_label')
   n['worked_reference_note']=annotation.get('note')
   n['related_work_references']=[dict(uid=x['uid'],key=x['id'],title=x['title']) for x in related]
   n['worked_relation']=annotation.get('relation')
   n['worked_document']=str(pdf.relative_to(ROOT));n['worked_document_number']=view['document']
   n.setdefault('source_original',n.get('source'))
   n['original_source_missing']=bool(n['source_original'] and not (ROOT/n['source_original']).exists())
   if n['original_source_missing']:n['source']=n['worked_document']
   elif n['source_original']:n['source']=n['source_original']
   case=dict(id=n['case_reference'],label=n['label'],view=view['path'],local_id=n['id'],ideas=[x['uid'] for x in refs],primary_idea=refs[0]['uid'],
             original_source=n['source_original'],original_source_missing=n['original_source_missing'],document=n['worked_document'])
   if annotation:
    case.update(primary_source=annotation.get('primary_source'),primary_source_label=annotation.get('primary_source_label'),
                reference_note=annotation.get('note'),related_ideas=[x['uid'] for x in related],relation=annotation.get('relation'))
   cases.append(case)
  encoded=json.dumps(payload,ensure_ascii=False).replace('</','<\\/')
  text=text[:match.start(2)]+encoded+text[match.end(2):]
  # Existing detail functions keep their own scope and observations.
  text=re.sub(r'/\* BEGIN WORKED REFERENCES \*/.*?/\* END WORKED REFERENCES \*/\s*','',text,flags=re.S)
  if 'attachWorkedReference(n,box);' not in text:
   function='selectNode' if view['container'] else 'describe'
   pat=r'(function '+function+r'\(id\)\{.*?box\.replaceChildren\(\);)'
   text,count=re.subn(pat,lambda m:m.group(1)+'attachWorkedReference(n,box);',text,count=1,flags=re.S);assert count==1
  js_start=re.search(r'<script>(?=[^<]*(?:const g=|function solveBridge|const data=))',text)
  if js_start is None:
   starts=list(re.finditer(r'<script>(?!\s*<)',text));assert starts;js_start=starts[-1]
  text=text[:js_start.end()]+HELPER+text[js_start.end():]
  text=re.sub(r'<script id="worked-case-routing">.*?</script>','',text,flags=re.S)
  routing='''<script id="worked-case-routing">function routeWorkedCase(){if(location.hash.startsWith('#case=')){const local=decodeURIComponent(location.hash.slice(6)).split('.').slice(1).join('.');if(typeof describe==='function')describe(local);else if(typeof selectNode==='function')selectNode(local);}}addEventListener('hashchange',routeWorkedCase);routeWorkedCase();</script>'''
  text=text.replace('</body>',routing+'</body>');p.write_text(text,encoding='utf-8')

 for view in c['svg_views']:
  p=ROOT/view['path'];text=p.read_text();root=E.fromstring(text,parser=E.XMLParser(target=E.TreeBuilder(insert_comments=True)))
  if 'keys' in view:
   items=[(views[view['graph']]['mapping'][k][0],view['graph']+'.'+k) for k in view['keys']]
  else:items=list(zip(view['node_keys'],view['case_ids']))
  patches=[e for e in root.iter() if isinstance(e.tag,str) and re.fullmatch(r'patch_\d+',e.get('id',''))]
  patches=sorted(patches,key=lambda e:int(e.get('id').split('_')[-1]))[-len(items):]
  parents={child:par for par in root.iter() for child in par}
  for i,(key,case_id) in enumerate(items):
   n=nodes[key];title_group=next(e for e in root.iter() if e.get('id')==f'text_{i+1}')
   labels=[(e.text or '').strip() for e in title_group.iter() if e.tag is E.Comment]
   label=labels[0] if labels else n['title']
   assert label==view['expected_labels'][i],('SVG label changed; review case mapping',view['path'],case_id,label)
   for element in [patches[i],title_group]:
    parent=parents[element]
    if parent.tag==f'{{{NS}}}a' and parent.get('data-worked-link'):
     wrapper=parent
    else:
     wrapper=E.Element(f'{{{NS}}}a');pos=list(parent).index(element);parent.remove(element);wrapper.append(element);parent.insert(pos,wrapper)
    wrapper.set('data-worked-link',case_id);wrapper.set('href','../00_Carte_des_idees.html#node='+n['uid'])
    wrapper.set(f'{{{XL}}}href','../00_Carte_des_idees.html#node='+n['uid'])
    wrapper.set('aria-label',n['uid']+' · '+label);wrapper.set('style','cursor:pointer')
   graph_doc=int(view['graph'][1:])
   dossier=next((str(x.relative_to(ROOT)) for x in (ROOT/'1_Presentation').glob(f'{graph_doc:02d}_*.pdf')),n['evidence'][0])
   if not any(x['id']==case_id for x in cases):cases.append(dict(id=case_id,label=label,view=view['path'],local_id=case_id,ideas=[n['uid']],primary_idea=n['uid'],document=dossier))
  p.write_text(E.tostring(root,encoding='unicode'),encoding='utf-8')
  # An SVG loaded via img cannot expose its links. Embed it in the two readers.
  if view['graph'] in views:
   reader=ROOT/views[view['graph']]['path'];page=reader.read_text()
   inline=E.tostring(root,encoding='unicode');inline=re.sub(r'<svg\b', '<svg data-worked-diagram="'+view['graph']+'" style="width:100%;height:auto"',inline,count=1)
   img=r'<img\b[^>]*src="data:image/svg\+xml;base64,[^"]+"[^>]*>'
   if re.search(img,page):page=re.sub(img,lambda _:inline,page,count=1)
   elif 'data-worked-diagram' in page:
    page=re.sub(r'<svg\b[^>]*data-worked-diagram="'+view['graph']+r'".*?</svg>',lambda _:inline,page,count=1,flags=re.S)
   reader.write_text(page,encoding='utf-8')
 assert len({x['id'] for x in cases})==len(cases)
 out=dict(version='V6.55',ideas=len(nodes),cases=cases,documents_renumbered=False)
 (ROOT/'3_Preuves_et_calculs/data/references_graphes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 register=json.loads((HERE/'registre_identifiants.json').read_text());by_uid={n['uid']:n for n in c['nodes']}
 lines=['# Identifiants stables du corpus','','V6.55 est une version globale. DOC-xxx désigne un document existant ; IDE-xxx une idée ; Gxx.nom une case de graphe. Les numéros documentaires 1 à 79 sont conservés. Les identifiants d’idées ne dépendent pas de l’ordre de dessin.','','## Idées et travaux conservés','','| Identifiant | Idée | Pièces |','|---|---|---|']
 for n in c['nodes']:
  links=' ; '.join(f'[{Path(x).name}](../../{x})' for x in n['evidence'])
  lines.append(f'| {n["uid"]} | {n["title"]} | {links} |')
 lines+=['','## Cases des différentes vues','','| Case | Travail dans la vue | Idées stables | Dossier |','|---|---|---|---|']
 for case in cases:lines.append(f'| {case["id"]} | {case["label"]} | {", ".join(case["ideas"])} | [{Path(case["document"]).name}](../../{case["document"]}) |')
 lines+=['','Les sources originales retrouvées sont redevenues les liens actifs. Les éventuelles absences restent signalées dans references_graphes.json ; le dossier PDF est conservé dans tous les cas. Provenance : RECUPERATION_2026_10_15.json.','']
 (HERE/'REGISTRE_DES_IDENTIFIANTS.md').write_text('\n'.join(lines),encoding='utf-8-sig')
 print(json.dumps(dict(stable_ideas=len(nodes),linked_cases=len(cases),graph_readers=len(views),svg_maps=len(c['svg_views']),documents_renumbered=False)))

if __name__=='__main__':main()
