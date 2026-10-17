"""Offline catalogue of actual corpus files, idea cards and reference records.

Links and format siblings establish documentary associations, not implications.
No index entry is a substitute for a proof or a reference verification.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import html, json, re, importlib.util

ROOT=Path(__file__).resolve().parents[2]
INDEX='3_Preuves_et_calculs/data/catalogue_fichiers_v655.json'
KINDS={'fiches':'Fiches des idées','html':'Pages HTML','pdf':'Documents PDF','tex':'Sources LaTeX',
       'md':'Notes Markdown','programmes':'Programmes Python / JS','donnees':'Données JSON / CSV / NPZ',
       'figures':'Figures et images','references':'Références bibliographiques','word':'Documents Word',
       'zip':'Paquets ZIP','autres':'Autres fichiers'}
SUFFIX={'.html':'html','.pdf':'pdf','.tex':'tex','.md':'md','.py':'programmes','.js':'programmes',
        '.cjs':'programmes','.sh':'programmes','.json':'donnees','.csv':'donnees','.npz':'donnees',
        '.npy':'donnees','.tsv':'donnees','.svg':'figures','.png':'figures','.jpg':'figures',
        '.jpeg':'figures','.gif':'figures','.webp':'figures','.docx':'word','.zip':'zip'}

def esc(s):return html.escape(str(s),quote=True)
def read_head(path):
    if path.suffix not in {'.html','.md','.py','.tex','.svg','.js','.cjs','.json'} or not path.is_file():return ''
    with path.open(encoding='utf-8-sig',errors='replace') as f:return f.read(100_000)
def title(path,text):
    if path.suffix=='.md':m=re.search(r'^#\s+(.+)',text,re.M)
    elif path.suffix=='.html':m=re.search(r'<title[^>]*>(.*?)</title>',text,re.S|re.I)
    elif path.suffix=='.py':m=re.search(r'"""([^\n]*\S[^\n]*)',text)
    elif path.suffix=='.tex':m=re.search(r'\\title\{([^}]+)\}',text)
    else:m=None
    return html.unescape(re.sub(r'<[^>]+>','',m[1].split('"""',1)[0]).strip())[:220] if m else path.stem.replace('_',' ')
def archived(rel):
    parts=Path(rel).parts
    return rel.startswith('4_Archives/') or any(x.startswith(('historique','avant_reparation','diagnostic_avant')) for x in parts)
def local_links(rel,text,paths):
    # Navigation and embedded shared state are not citations or evidence.
    text=re.sub(r'<(?:nav|script)\b[^>]*>.*?(?:</(?:nav|script)>|$)','',text,flags=re.S|re.I)
    raw=re.findall(r'(?:href|src|data)=["\']([^"\']+)["\']',text)
    raw+=re.findall(r'\]\(([^)\s]+)\)',text)
    raw+=re.findall(r'["\']([^"\'\n]+\.(?:json|csv|npz|png|svg|pdf|html|md|py|tex))["\']',text)
    found=set()
    for value in raw:
        u=urlsplit(html.unescape(value))
        if u.scheme or u.netloc or not u.path:continue
        for candidate in [ROOT/Path(rel).parent/unquote(u.path),ROOT/unquote(u.path)]:
            try:p=str(candidate.resolve().relative_to(ROOT))
            except ValueError:continue
            if p in paths:found.add(p);break
    return found

def collect(state):
    paths={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and not any(x.startswith('.') for x in p.relative_to(ROOT).parts)}
    # Travail en cours (V6.59) : dépôts et registre des fiches évoluent entre deux constructions ; ils ne font pas partie de l'état publié.
    paths-={x for x in paths if x.startswith('2_Methode/Depot/') or x in ('2_Methode/Pilotage/taches.json','2_Methode/Pilotage/journal_taches.json')}
    paths.add(INDEX)
    sources=json.loads((ROOT/'2_Methode/Sources/sources.json').read_text(encoding='utf-8-sig'))
    aliases=json.loads((ROOT/'2_Methode/Sources/references_articles.json').read_text())['aliases']
    known_refs={r['cle'] for r in sources};direct_refs={};links={};heads={}
    documents={p:d['id'] for d in state['reference_registry']['documents'] for p in d['paths']}
    for rel in paths:
        m=re.match(r'1_Presentation/(\d{2})_',rel)
        if m and 1<=int(m[1])<=79:documents.setdefault(rel,'DOC-'+f'{int(m[1]):03d}')
    by_doc={d['id']:sorted(p for p in paths if documents.get(p)==d['id']) for d in state['reference_registry']['documents']}
    siblings={}
    for rel in paths:siblings.setdefault(str(Path(rel).with_suffix('')),[]).append(rel)
    for rel in sorted(paths):
        shared_index=(rel==INDEX or rel.startswith('CHECKSUMS') or (rel.startswith('3_Preuves_et_calculs/data/') and (
            Path(rel).name in ('pilotage_courant.json','ciblage_courant.json') or Path(rel).name.startswith('v655_'))))
        head='' if shared_index else read_head(ROOT/rel);heads[rel]=head
        citation_text=re.sub(r'<(?:nav|script)\b[^>]*>.*?(?:</(?:nav|script)>|$)','',head,flags=re.S|re.I) if Path(rel).suffix=='.html' else head
        keys=set(re.findall(r'\[([A-Za-z][A-Za-z0-9]+)\]',citation_text))
        keys|={k.strip() for group in re.findall(r'\\(?:cite\w*|bibitem)(?:\[[^\]]*\])*\{([^}]+)\}',citation_text) for k in group.split(',')}
        direct_refs[rel]={k for key in keys for k in aliases.get(key,[key]) if k in known_refs}
        links[rel]=local_links(rel,head,paths)
    fig_spec=importlib.util.spec_from_file_location('catalogue_figures',ROOT/'2_Methode/Figures/build_figures.py')
    figures=importlib.util.module_from_spec(fig_spec);fig_spec.loader.exec_module(figures)
    fig_info={x['fichier']:x for x in figures.doc_figures()+figures.calc_figures()+figures.article_figures()}
    fig_ids={x['fichier']:x['id'] for x in json.loads((ROOT/'2_Methode/Figures/registre_figures.json').read_text())['figures']}
    for rel,info in fig_info.items():
        for k in ['doc','script','article_pdf','article_tex']:
            target=info.get(k)
            if target in paths:links[rel].add(target);links[target].add(rel)
    for rel in paths:
        for other in siblings[str(Path(rel).with_suffix(''))]:
            if other!=rel:links[rel].add(other)
    nodes=state['nodes'];by_key={n['id']:n for n in nodes};ideas_for={p:set() for p in paths}
    source_by_key={r['cle']:r for r in sources}
    from_documents={}
    for r in sources:
        for n in r.get('docs',[])+r.get('cite_aussi',[]):
            match=re.match(r'\d{2}',n)
            if match:from_documents.setdefault('DOC-'+f'{int(match[0]):03d}',set()).add(r['cle'])
    for n in nodes:
        seed=set(n['evidence'])|set(n.get('pdf_documents',[]))|set(n.get('related_resources',[]))
        seed|=local_links('00_Carte_des_idees.html',n.get('initial_detail_html',''),paths)
        for case in state['graph_cases']:
            if n['uid'] in case['ideas']:
                seed.add(case['view'])
                if case.get('original_source'):seed.add(case['original_source'])
        attached={p for p in seed if p in paths}
        for p in list(attached):
            attached.update(q for q in links[p] if not archived(q))
            for q in by_doc.get(documents.get(p,''),[]):attached.add(q)
        refs=set()
        for p in sorted(attached):
            if p not in paths:continue
            ideas_for[p].add(n['uid']);refs.update(direct_refs[p]);refs.update(from_documents.get(documents.get(p,''),[]))
        n['linked_resources']=[{'path':p,'kind':'figures' if p in fig_ids else SUFFIX.get(Path(p).suffix.lower(),'autres'),
                                'title':fig_info[p]['legende'] if p in fig_info else title(ROOT/p,heads[p])}
                               for p in sorted(attached) if p in paths]
        n['reference_keys']=sorted(refs)
    entries=[]
    for n in nodes:
        entries.append({'id':n['uid'],'kind':'fiches','title':n['uid']+' · '+n['title'],'href':'00_Carte_des_idees.html#node='+n['uid'],
                        'path':'','archived':False,'ideas':[n['uid']],'documents':[],
                        'references':n['reference_keys'],'related':[r['path'] for r in n['linked_resources']],
                        'search_extra':n['summary']+' '+n['family']})
    for r in sources:
        related=[p for p in sorted(paths) if r['cle'] in direct_refs[p] and not archived(p)]
        for doc in sorted(from_documents):
            if r['cle'] in from_documents[doc]:related+=by_doc.get(doc,[])
        entries.append({'id':'REF-'+r['cle'],'kind':'references','title':r['cle']+' · '+r['auteurs']+' · '+r['titre'],
                        'href':'1_Presentation/42_REGISTRE_DES_SOURCES.html#ref-'+r['cle'],'path':'','archived':False,
                        'ideas':[n['uid'] for n in nodes if r['cle'] in n['reference_keys']],'documents':[],
                        'references':[r['cle']],'related':sorted(set(related)),
                        'search_extra':r.get('publication','')+' '+r.get('usage_corpus','')+' '+r.get('statut','')})
    for rel in sorted(paths):
        doc=documents.get(rel);name=title(ROOT/rel,heads[rel])
        if rel in fig_info:name=fig_ids.get(rel,'')+' · '+fig_info[rel]['legende']
        entries.append({'id':rel,'kind':'figures' if rel in fig_ids else SUFFIX.get(Path(rel).suffix.lower(),'autres'),
                        'title':name,'href':rel,'path':rel,'archived':archived(rel),'ideas':sorted(ideas_for[rel]),
                        'documents':[doc] if doc else [],'references':sorted(direct_refs[rel]),
                        'related':sorted(links[rel]),'search_extra':Path(rel).name})
    return {'version':'V6.55','file_count':len(paths),'idea_count':len(nodes),'reference_count':len(sources),
            'association_rule':'Renvois locaux explicites, formats de même nom, identifiants documentaires conservés. Ces liens ne constituent pas une validation scientifique.',
            'entries':entries}

STYLE='''<style>
.catalogue-controls{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr) minmax(0,1fr);gap:12px}.catalogue-controls label{display:grid;gap:6px;min-width:0;font-size:.86rem}.catalogue-controls input,.catalogue-controls select{width:100%;min-width:0;font:inherit}.resource-list{display:grid;gap:0;list-style:none;padding:0;margin:0}.resource-item{padding:14px 0;border-top:1px solid var(--rule);min-width:0}.resource-item h3{font-size:.96rem;margin:0 0 6px;line-height:1.4}.resource-meta{font-size:.79rem;color:var(--muted);overflow-wrap:anywhere;display:flex;flex-wrap:wrap;gap:5px 14px}.resource-links{font-size:.8rem;margin:8px 0 0;display:flex;gap:6px 14px;flex-wrap:wrap}.resource-item details{margin-top:8px;font-size:.82rem}.resource-item details ul{padding-left:20px}.resource-list [hidden]{display:none!important}.catalogue-pager{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.catalogue-pager button{font:inherit;padding:7px 12px;color:var(--ink);background:var(--sheet);border:1px solid var(--rule);border-radius:4px}.node-publications{padding:12px 14px;background:var(--paper);border:1px solid var(--rule);border-radius:4px;font-size:.9rem}.node-resource-list{padding-left:22px}.node-resource-list li{margin:8px 0}.node-resource-kind{font-size:.8rem;color:var(--muted)}
@media(max-width:640px){.catalogue-controls{grid-template-columns:minmax(0,1fr)}.resource-item h3{font-size:.94rem}}
</style>'''
SCRIPT='''<script>(()=>{const root=document.getElementById('resource-catalogue');if(!root)return;
const data=JSON.parse(root.querySelector('[data-catalogue-data]').textContent),query=root.querySelector('[data-catalogue-query]'),kind=root.querySelector('[data-catalogue-kind]'),scope=root.querySelector('[data-catalogue-scope]'),list=root.querySelector('[data-catalogue-list]');
const norm=s=>String(s).normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLocaleLowerCase('fr'),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const by=new Map(data.entries.map(e=>[e.id,e])),link=(p,t)=>'<a href="'+esc(p)+'">'+esc(t)+'</a>',index=data.entries.map(e=>({e,search:norm([e.id,e.title,e.path,e.search_extra,...e.ideas,...e.documents,...e.references].join(' '))}));let page=0,found=[];const size=30;
function row(e){let out='<li class="resource-item" data-catalogue-entry="'+esc(e.id)+'"><h3>'+link(e.href,e.title)+'</h3><div class="resource-meta"><span>'+esc(data.kinds[e.kind])+(e.archived?' · Archive':'')+'</span><span>'+esc(e.path||e.id)+'</span>'+e.documents.map(d=>'<span>'+esc(d)+'</span>').join('')+'</div>';
if(e.ideas.length||e.references.length)out+='<p class="resource-links">'+e.ideas.map(i=>link('00_Carte_des_idees.html#node='+i,i)).concat(e.references.map(k=>link('1_Presentation/42_REGISTRE_DES_SOURCES.html#ref-'+k,'['+k+']'))).join(' ')+'</p>';
if(e.related.length)out+='<details><summary>'+e.related.length+' pièces / formats liés</summary><ul>'+e.related.map(p=>'<li>'+link(p,by.get(p)?.title+' · '+p.split('/').at(-1))+'</li>').join('')+'</ul></details>';return out+'</li>'}
function render(){const start=page*size;list.innerHTML=found.slice(start,start+size).map(row).join('')||'<li>Aucune pièce ne correspond à ces filtres.</li>';root.querySelector('[data-catalogue-count]').textContent=found.length+' résultats · '+(found.length?start+1:0)+'–'+Math.min(start+size,found.length);root.querySelector('[data-catalogue-prev]').disabled=page===0;root.querySelector('[data-catalogue-next]').disabled=start+size>=found.length}
function filter(){const words=norm(query.value).trim().split(/\\s+/).filter(Boolean);found=index.filter(({e,search})=>(!kind.value||e.kind===kind.value)&&(scope.value==='all'||(scope.value==='archives'?e.archived:!e.archived))&&words.every(w=>search.includes(w))).map(x=>x.e);page=0;render()}
const params=new URLSearchParams(location.search);query.value=params.get('recherche')||'';if(data.kinds[params.get('type')])kind.value=params.get('type');if(params.get('archives')==='oui')scope.value='all';
query.addEventListener('input',filter);kind.addEventListener('change',filter);scope.addEventListener('change',filter);root.querySelector('[data-catalogue-prev]').addEventListener('click',()=>{page--;render();list.scrollIntoView({block:'start'})});root.querySelector('[data-catalogue-next]').addEventListener('click',()=>{page++;render();list.scrollIntoView({block:'start'})});filter();window.catalogueReady=true})();</script>'''

def render(state):
    data=state['catalogue'];payload=json.dumps(dict(**data,kinds=KINDS),ensure_ascii=False).replace('</','<\\/')
    options=''.join(f'<option value="{k}">{esc(v)}</option>' for k,v in KINDS.items())
    return STYLE+f'''<div id="resource-catalogue"><p>{data['file_count']} fichiers, {data['idea_count']} fiches d’idées et {data['reference_count']} références. Recherchez un titre, un nom de fichier, un numéro DOC / IDE ou une clé bibliographique. Les versions anciennes restent accessibles avec le filtre Archives.</p>
<div class="catalogue-controls"><label>Rechercher dans tout le corpus<input data-catalogue-query type="search" placeholder="Weil, V642, IDE-047, .py, énergie…"></label><label>Type de pièce<select data-catalogue-kind><option value="">Tous les types</option>{options}</select></label><label>Périmètre<select data-catalogue-scope><option value="current">Corpus courant</option><option value="all">Courant et archives</option><option value="archives">Archives seules</option></select></label></div>
<p data-catalogue-count role="status"></p><ul class="resource-list" data-catalogue-list></ul><div class="catalogue-pager"><button type="button" data-catalogue-prev>Précédents</button><button type="button" data-catalogue-next>Suivants</button></div>
<p class="foot">Les liens documentaires servent à retrouver les pièces. Leur présence ne valide pas leur contenu. <a href="{INDEX}">Télécharger l’index complet JSON</a>.</p><noscript>Le catalogue interactif demande JavaScript ; l’index JSON ci-dessus reste accessible.</noscript><script type="application/json" data-catalogue-data>{payload}</script></div>'''+SCRIPT
