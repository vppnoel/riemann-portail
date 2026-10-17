"""Linked 2D views of existing idea contracts; layout is not a research metric."""
from pathlib import Path
import html,heapq,json
ROOT=Path(__file__).resolve().parents[2]
W,H=240,110
MAPS={
 'weil':{'title':'Weil : signe ET couverture','size':(1030,1390),'positions':{
  'prime_norm':(45,75),'domaines':(370,75),'identity':(695,75),
  'compact':(45,290),'fluctuation':(695,290),'schur':(45,510),'local':(370,510),'transport':(695,510),
  'global_sign':(370,740),'coverage':(695,740),'weil_all':(370,1010),'RH':(370,1230)},
  'gate':{'id':'@weil','at':(565,920),'requires':['global_sign','coverage'],'target':'weil_all','label':'Signe ET couverture'}},
 'energie':{'title':'Énergie et amplification V6.55','size':(1030,1610),'positions':{
  'identity':(45,75),'anchoring':(695,75),'J':(370,295),'copies':(45,510),'generic_sieve':(695,510),
  'head':(45,735),'large_q':(370,735),'threequarters':(370,1010),'thA':(45,1010),
  'Q_bound':(45,1230),'J_bound':(695,1230),'RH':(370,1450)},
  'gate':{'id':'@amplification','at':(458,920),'requires':['copies','head','large_q'],'target':'threequarters','label':'Restitution ET tête ET grande queue'}},
 'ponts':{'title':'Ponts, témoins et voies limitées','size':(1030,1180),'positions':{
  'surface':(45,75),'rencontre_n':(695,75),'stepanov':(45,295),'jets':(370,295),
  'prime_norm':(45,510),'v13':(370,510),'dh_cert':(695,510),
  'domaines':(45,735),'schur':(695,735),'global_sign':(370,1010)}}}
TITLES={'domaines':'P, moments et domaines','compact':'Métrique et queue effective','fluctuation':'Fluctuation arithmétique','schur':'Dette des couplages','local':'Certificat local S ≤ 11/20',
 'transport':'Transport et réserve','coverage':'Couverture et limite','global_sign':'Loi de signe globale','weil_all':'Weil sur tous les tests','RH':'Hypothèse de Riemann',
 'identity':'Identité des poids premiers','anchoring':'Corrélations ancrées','J':'Énergie positive J','J_bound':'Borne J(X) = O(X²)','Q_bound':'Borne globale de Q',
 'copies':'Restitution et dilatations','head':'Petits conducteurs : tête','large_q':'Grands conducteurs signés','threequarters':'Conséquence visée : Re(s)>3/4',
 'generic_sieve':'Limite du crible générique','prime_norm':'Norme première divergente','surface':'Surface et Frobenius virtuels','stepanov':'Transplantation de Stepanov',
 'jets':'Jets : lemme et relief','v13':'Fibres, jets et pli choisi','dh_cert':'Témoin négatif de DH','rencontre_n':'Interactions : Rencontre à n','thA':'Théorème A : critère pour Q'}
STATUS={'demontre':'Démontré dans le dossier','classique':'Critère / résultat classique','partiel':'Acquis partiel','ouvert':'Obligation ouverte','conditionnel':'Conséquence conditionnelle',
 'obstacle':'Obstruction circonscrite','diagnostic':'Diagnostic','outil':'Outil','mesure':'Mesuré dans le cadre déclaré'}
def esc(x):return html.escape(str(x),quote=True)
def wrap(text,limit=21):
 lines=['']
 for word in text.split():
  if len(lines[-1]+' '+word)>limit and lines[-1]:lines.append(word)
  else:lines[-1]+=(' ' if lines[-1] else '')+word
 return lines

def geometry(spec):
 d={k:(x,y,W,H) for k,(x,y) in spec['positions'].items()}
 if spec.get('gate'):
  x,y=spec['gate']['at'];d[spec['gate']['id']]=(x,y,64,38)
 return d

def route(geo,source,target,usage):
 a,b=geo[source],geo[target];ax,ay,aw,ah=a;bx,by,bw,bh=b
 if by>ay+ah:
  start=(ax+aw/2,ay+ah+15);end=(bx+bw/2,by-15);sp=(start[0],ay+ah);ep=(end[0],by)
 elif by+bh<ay:
  side=-1 if ax<=bx else 1;start=(ax-15 if side<0 else ax+aw+15,ay+ah/2);end=(bx-15 if side<0 else bx+bw+15,by+bh/2)
  sp=(ax if side<0 else ax+aw,start[1]);ep=(bx if side<0 else bx+bw,end[1])
 elif bx>ax:
  start=(ax+aw+15,ay+ah/2);end=(bx-15,by+bh/2);sp=(ax+aw,start[1]);ep=(bx,end[1])
 else:
  start=(ax-15,ay+ah/2);end=(bx+bw+15,by+bh/2);sp=(ax,start[1]);ep=(bx+bw,end[1])
 xs={15.,1015.,start[0],end[0]};ys={25.,start[1],end[1]}
 for x,y,w,h in geo.values():xs.update([x-15,x+w/2,x+w+15]);ys.update([y-15,y+h/2,y+h+15])
 xs=sorted(xs);ys=sorted(ys)
 def valid(x,y):return not any(rx-7<x<rx+rw+7 and ry-7<y<ry+rh+7 for rx,ry,rw,rh in geo.values())
 def segment(p,q):
  if p[0]==q[0]:return not any(rx-7<p[0]<rx+rw+7 and max(min(p[1],q[1]),ry-7)<min(max(p[1],q[1]),ry+rh+7) for rx,ry,rw,rh in geo.values())
  return not any(ry-7<p[1]<ry+rh+7 and max(min(p[0],q[0]),rx-7)<min(max(p[0],q[0]),rx+rw+7) for rx,ry,rw,rh in geo.values())
 begin=(xs.index(start[0]),ys.index(start[1]),0);queue=[(0,begin)];dist={begin:0};parent={};goal=None
 while queue:
  cost,state=heapq.heappop(queue)
  if cost!=dist[state]:continue
  i,j,direction=state;p=(xs[i],ys[j])
  if p==end:goal=state;break
  for ii,jj,newdir in [(i-1,j,1),(i+1,j,1),(i,j-1,2),(i,j+1,2)]:
   if not (0<=ii<len(xs) and 0<=jj<len(ys)):continue
   q=(xs[ii],ys[jj])
   if not valid(*q) or not segment(p,q):continue
   key=tuple(sorted([p,q]));extra=abs(q[0]-p[0])+abs(q[1]-p[1])+(18 if direction and direction!=newdir else 0)+usage.get(key,0)*6
   nxt=(ii,jj,newdir);value=cost+extra
   if value<dist.get(nxt,float('inf')):dist[nxt]=value;parent[nxt]=state;heapq.heappush(queue,(value,nxt))
 if goal is None:raise ValueError('No diagram route '+source+'→'+target)
 points=[];s=goal
 while True:
  points.append((xs[s[0]],ys[s[1]]))
  if s==begin:break
  s=parent[s]
 points.reverse()
 for p,q in zip(points,points[1:]):key=tuple(sorted([p,q]));usage[key]=usage.get(key,0)+1
 points=[sp]+points+[ep];simple=[]
 for p in points:
  if len(simple)>1 and (simple[-2][0]==simple[-1][0]==p[0] or simple[-2][1]==simple[-1][1]==p[1]):simple[-1]=p
  else:simple.append(p)
 return 'M'+' L'.join(f'{x:g},{y:g}' for x,y in simple)

def edges_for(s,spec):
 keys=set(spec['positions']);gate=spec.get('gate');out=[]
 for e in s['edges']:
  if e['source'] not in keys or e['target'] not in keys:continue
  if gate and e['target']==gate['target'] and e['source'] in gate['requires']:
   if set(e.get('requires',[]))!=set(gate['requires']):raise ValueError('AND gate disagrees with source contract')
   continue
  out.append(e)
 if gate:
  for key in gate['requires']:out.append({'source':key,'target':gate['id'],'kind':'conditionnel','label':gate['label'],'requires':gate['requires']})
  out.append({'source':gate['id'],'target':gate['target'],'kind':'conditionnel','label':gate['label'],'requires':gate['requires']})
 return out

def svg(s,key,prefix=''):
 spec=MAPS[key];geo=geometry(spec);by={n['id']:n for n in s['nodes']};usage={};w,h=spec['size'];out=[f'<svg xmlns="http://www.w3.org/2000/svg" class="advanced-svg" data-map-svg="{key}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(spec["title"])}">',f'<defs><marker id="advanced-arrow-{key}" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="context-stroke"/></marker></defs>']
 out.append(STYLE)
 out.append(f'<text x="45" y="35" class="map-heading">{esc(spec["title"])}</text>')
 for e in edges_for(s,spec):
  kind=e['kind'];cl='limited' if kind in ['insuffisant','obstruction'] else 'open' if kind in ['obligation','conditionnel'] else 'known'
  guard=' ; ET : '+', '.join(e.get('requires',[])) if e.get('requires') else ''
  out.append(f'<path class="advanced-edge {cl}" data-edge-kind="{esc(kind)}" data-source="{esc(e["source"])}" data-target="{esc(e["target"])}" d="{route(geo,e["source"],e["target"],usage)}" marker-end="url(#advanced-arrow-{key})"><title>{esc(e["label"]+guard)}</title></path>')
 for node,(x,y) in spec['positions'].items():
  n=by[node];uid=n['uid'];out.append(f'<g class="advanced-node {n["status"]}" id="map-{key}-{uid}" data-map-node="{node}"><a data-node="{node}" href="{esc(prefix+"00_Carte_des_idees.html#node="+uid)}" aria-label="{esc(uid+" · "+n["title"])}"><rect class="node-bg" x="{x}" y="{y}" width="{W}" height="{H}" rx="6"/><text class="map-uid" x="{x+14}" y="{y+21}">{uid}</text>')
  for i,line in enumerate(wrap(TITLES.get(node,n['title']))):out.append(f'<text class="map-node-title" x="{x+14}" y="{y+46+i*19}">{esc(line)}</text>')
  out.append(f'<text class="map-node-status" x="{x+14}" y="{y+96}">{esc(STATUS[n["status"]])}</text><title>{esc(n["summary"])}</title></a>')
  pdf=n.get('pdf_documents',[])
  if pdf:out.append(f'<a class="map-pdf" data-pdf="{node}" href="{esc(prefix+pdf[0])}" aria-label="PDF : {esc(n["title"])}"><rect x="{x+W-49}" y="{y+8}" width="38" height="21" rx="3"/><text x="{x+W-30}" y="{y+23}" text-anchor="middle">PDF</text><title>{esc(pdf[0])}</title></a>')
  out.append('</g>')
 if spec.get('gate'):
  g=spec['gate'];x,y=g['at'];out.append(f'<g class="and-gate" data-and-guard="{esc(" ".join(g["requires"]))}"><rect x="{x}" y="{y}" width="64" height="38" rx="19"/><text x="{x+32}" y="{y+25}" text-anchor="middle">ET</text><title>{esc(g["label"])}</title></g>')
 out.append('</svg>');return ''.join(out)

STYLE='''<style>
.advanced-atlas{--map-ink:var(--ink,#1b2430);--map-rule:var(--rule,#d5dae1);--map-sheet:var(--sheet,#fff);min-width:0}.advanced-tabs,.advanced-tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:12px 0}.advanced-tabs button,.advanced-tools button{border:1px solid var(--map-rule);border-radius:4px;padding:7px 10px;background:var(--map-sheet);color:var(--map-ink);font:inherit;font-size:.86rem}.advanced-tabs button[aria-selected=true]{border-bottom:3px solid var(--ink);font-weight:650}.advanced-tools label{display:flex;gap:8px;align-items:center;font-size:.8rem}.advanced-tools input{width:100px}.advanced-legend{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:.78rem;margin:8px 0;color:var(--ink2,var(--muted))}.advanced-legend span{display:inline-flex;gap:8px;align-items:center}.advanced-legend i{display:inline-block;width:24px;border-top:2px solid var(--ink2,#4c5868)}.advanced-legend i.open{border-top:2px dashed var(--cond,#b26a00)}.advanced-legend i.limited{border-top:2px dotted var(--neg,#a6392e)}.advanced-viewport{overflow:auto;max-width:100%;max-height:73vh;border:1px dashed var(--map-rule);border-radius:7px;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;background:var(--paper,#f6f7f9);touch-action:pan-x pan-y}.advanced-svg{display:block!important;max-width:none!important;height:auto;width:1030px}.advanced-svg text{fill:var(--map-ink)}.advanced-svg .map-heading{font:600 20px var(--serif,Georgia,serif)}.advanced-node .node-bg{fill:var(--sheet,#fff);stroke:var(--ink2,#4c5868);stroke-width:1.4}.advanced-node.demontre .node-bg{fill:var(--core-bg,#e6f2ec);stroke:var(--core,#1f6f54)}.advanced-node.classique .node-bg{fill:var(--lit-bg,#e9ecf8);stroke:var(--lit,#3b4a9b)}.advanced-node.ouvert .node-bg,.advanced-node.conditionnel .node-bg,.advanced-node.partiel .node-bg{fill:var(--cond-bg,#fff3de);stroke:var(--cond,#b26a00)}.advanced-node.obstacle .node-bg{fill:var(--neg-bg,#f8e9e6);stroke:var(--neg,#a6392e)}.advanced-svg .map-uid{font:11px ui-monospace,monospace;fill:var(--ink2,#4c5868)}.advanced-svg .map-node-title{font:600 16px var(--serif,Georgia,serif)}.advanced-svg .map-node-status{font:11px var(--sans,system-ui,sans-serif);fill:var(--ink2,#4c5868)}.advanced-node>a:first-child{cursor:pointer}.advanced-node>a:first-child:hover .node-bg{stroke-width:2.8}.map-pdf rect{fill:var(--map-sheet);stroke:var(--map-rule)}.advanced-svg .map-pdf text{font:600 11px system-ui;fill:var(--lit,#3b4a9b)}.advanced-edge{fill:none;stroke-width:1.65;stroke-linejoin:round;stroke-linecap:round;stroke:var(--ink2,#4c5868)}.advanced-edge.open{stroke:var(--cond,#b26a00);stroke-dasharray:7 5}.advanced-edge.limited{stroke:var(--neg,#a6392e);stroke-dasharray:2 5}.and-gate rect{fill:var(--map-sheet);stroke:var(--cond,#b26a00);stroke-width:1.8}.and-gate text{font:700 15px system-ui}.advanced-foot{font-size:.8rem;color:var(--ink2,var(--muted))}.advanced-panel[hidden]{display:none!important}@media(max-width:640px){.advanced-viewport{max-height:68vh}.advanced-tools{gap:8px}.advanced-tabs button{font-size:.78rem;padding:7px}.advanced-tabs{gap:6px}}@media print{.advanced-tools,.advanced-tabs{display:none}.advanced-panel[hidden]{display:block!important}.advanced-viewport{max-height:none;overflow:visible}.advanced-svg{width:100%!important;max-width:100%!important}.advanced-panel{break-inside:avoid}}
</style>'''
STYLE=STYLE.replace('.advanced-svg{display:', '.advanced-svg{--map-ink:var(--ink,#1b2430);--map-rule:var(--rule,#d5dae1);--map-sheet:var(--sheet,#fff);display:')
EXPORTS={'weil':'CIBLES_WEIL_V655.svg','energie':'CIBLES_ENERGIE_V655.svg','ponts':'CIBLES_PONTS_V655.svg'}

def export_svgs(state):
 """Keep linked, self-styled copies in the global figure register."""
 for key,name in EXPORTS.items():
  (ROOT/'1_Presentation'/name).write_text(svg(state,key,'../'),encoding='utf-8')

SCRIPT='''<script>(()=>{const root=document.getElementById('advanced-atlas');if(!root)return;let selected='weil';const scale=root.querySelector('[data-map-scale]');
function panel(){return root.querySelector('[data-map-panel="'+selected+'"]')}
function zoom(){const svg=panel().querySelector('svg');svg.style.width=(1030*Number(scale.value)/100)+'px';root.querySelector('[data-map-percent]').textContent=scale.value+' %'}
root.querySelectorAll('[data-map-tab]').forEach(b=>b.addEventListener('click',()=>{selected=b.dataset.mapTab;root.querySelectorAll('[data-map-panel]').forEach(p=>p.hidden=p.dataset.mapPanel!==selected);root.querySelectorAll('[data-map-tab]').forEach(x=>x.setAttribute('aria-selected',String(x===b)));zoom()}));
scale.addEventListener('input',zoom);root.querySelector('[data-map-fit]').addEventListener('click',()=>{scale.value=Math.max(30,Math.min(140,Math.floor(panel().querySelector('.advanced-viewport').clientWidth/1030*100)));zoom()});
root.querySelector('[data-map-read]').addEventListener('click',()=>{scale.value=100;zoom()});root.querySelector('[data-map-goal]').addEventListener('click',()=>{const p=panel(),node=p.querySelector('[data-map-node="RH"]')||p.querySelector('[data-map-node="global_sign"]'),v=p.querySelector('.advanced-viewport'),r=node.getBoundingClientRect(),vr=v.getBoundingClientRect();v.scrollBy({left:r.left-vr.left-(vr.width-r.width)/2,top:r.top-vr.top-(vr.height-r.height)/2,behavior:'smooth'})});if(innerWidth>=768)scale.value=Math.min(100,Math.floor(panel().querySelector('.advanced-viewport').clientWidth/1030*100));zoom();})();</script>'''

def render(s,prefix=''):
 out=[STYLE,'<div class="advanced-atlas" id="advanced-atlas"><p>Chaque case ouvre sa fiche ; le bouton PDF ouvre la publication associée. Les positions organisent les dépendances et ne mesurent aucune distance à RH.</p><div class="advanced-tabs" role="tablist" aria-label="Cartes des cibles">']
 for key,spec in MAPS.items():out.append(f'<button type="button" role="tab" data-map-tab="{key}" aria-selected="{str(key=="weil").lower()}">{esc(spec["title"])}</button>')
 out.append('</div><div class="advanced-tools"><button type="button" data-map-goal>Aller à la cible</button><button type="button" data-map-read>Lecture 100 %</button><button type="button" data-map-fit>Vue d’ensemble</button><label>Zoom <input data-map-scale type="range" min="30" max="140" value="100"><output data-map-percent>100 %</output></label></div><div class="advanced-legend"><span><i></i>Construction ou critère sous son contrat</span><span><i class="open"></i>Obligation / condition</span><span><i class="limited"></i>Insuffisance ou obstruction ciblée</span></div>')
 for key,spec in MAPS.items():out.append(f'<div class="advanced-panel" data-map-panel="{key}"'+(' hidden' if key!='weil' else '')+'><div class="advanced-viewport" tabindex="0" aria-label="Carte 2D défilante : '+esc(spec['title'])+'">'+svg(s,key,prefix)+'</div><p class="advanced-foot"><a href="'+esc(prefix+'1_Presentation/'+EXPORTS[key])+'">Ouvrir cette carte en SVG lié</a></p></div>')
 out.append('<p class="advanced-foot">Sur téléphone : déplacez la carte dans les deux directions. ET exige tous les contrats indiqués. L’étape 3/4 ne suffit pas pour RH. Les autres relations et tous les documents restent dans les fiches et le registre.</p></div>');out.append(SCRIPT)
 return ''.join(out)
