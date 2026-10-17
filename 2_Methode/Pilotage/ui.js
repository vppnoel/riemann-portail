if(typeof document!=='undefined'){
(() => {
  'use strict';
  const S=JSON.parse(document.getElementById('steering-data').textContent),by=new Map(S.nodes.map(n=>[n.id,n]));
  S.nodes.forEach(n=>by.set(n.uid,n));
  const el=id=>document.getElementById(id),escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const link=(p,t)=>'<a href="'+escape(S.prefix+p)+'">'+escape(t)+'</a>';
  const nodeButton=(k,t)=>'<button class="textlink" data-node="'+escape(k)+'">'+escape(t||by.get(k).title)+'</button>';
  const dlg=el('node-dialog');let last=null;
  document.querySelectorAll('table').forEach(t=>{
    const labels=[...t.querySelectorAll('thead th')].map(x=>x.textContent);
    t.querySelectorAll('tbody tr').forEach(r=>[...r.children].forEach((cell,i)=>{if(cell.tagName==='TD')cell.dataset.label=labels[i]||''}));
  });
  function openNode(k,trigger){
    const n=by.get(k);if(!n)return;last=trigger||last;
    k=n.id;el('node-status').textContent=S.status_labels[n.status];el('node-title').textContent=n.uid+' · '+n.title;
    const incoming=S.edges.filter(e=>e.target===k),outgoing=S.edges.filter(e=>e.source===k);
    const rel=(e,d)=>'<div class="relation">'+nodeButton(d==='in'?e.source:e.target)+' <span class="badge">'+escape(e.kind)+'</span><p>'+escape(e.label)+(e.requires?' · Tous requis : '+e.requires.map(x=>escape(by.get(x).title)).join(' ET '):'')+'</p></div>';
    const tasks=S.investigations.filter(a=>a.nodes.includes(k));
    let body=(n.pdf_documents.length?'<div class="node-publications"><strong>Publications PDF</strong> : '+n.pdf_documents.map(p=>link(p,'PDF · '+p.split('/').pop().replace(/_/g,' '))).join(' · ')+'</div>':'')+'<p>'+escape(n.summary)+'</p><h3>Évaluation actuelle</h3><p>'+escape(n.review)+'</p><p class="foot">Réévaluation documentaire : '+escape(n.reviewed_on)+'.</p><h3>Pièces et preuves</h3><ul>'+n.evidence.map(p=>'<li>'+link(p,p.split('/').pop())+'</li>').join('')+'</ul>';
    const cases=S.graph_cases.filter(c=>c.ideas.includes(n.uid));
    if(cases.length)body+='<h3>Cases des différentes cartes</h3><ul>'+cases.map(c=>'<li>'+link(c.view+(c.view.endsWith('.html')?'#case='+c.id:''),c.id+' · '+c.label)+'</li>').join('')+'</ul>';
    body+='<h3>Tous les formats et ressources liés</h3><p>'+link('00_PORTAIL.html?recherche='+encodeURIComponent(n.uid)+'#documents','Retrouver cette idée et ses fichiers dans le catalogue')+'</p>';
    const grouped=new Map();for(const r of n.linked_resources||[]){if(!grouped.has(r.kind))grouped.set(r.kind,[]);grouped.get(r.kind).push(r)}
    for(const [kind,items] of grouped)body+='<details class="node-resources"><summary>'+escape(S.catalogue_kinds[kind]||kind)+' · '+items.length+'</summary><ul class="node-resource-list">'+items.map(r=>'<li>'+link(r.path,r.title)+'<br><span class="node-resource-kind">'+escape(r.path)+'</span></li>').join('')+'</ul></details>';
    if(n.reference_keys?.length)body+='<h3>Références reliées à ces pièces</h3><p>'+n.reference_keys.map(key=>link('1_Presentation/42_REGISTRE_DES_SOURCES.html#ref-'+key,'['+key+']')).join(' · ')+'</p>';
    body+='<h3>Ce qui conduit à ce nœud</h3>'+(incoming.map(e=>rel(e,'in')).join('')||'<p>Aucune dépendance entrante déclarée. Cette idée est une racine ou un outil de méthode.</p>');
    body+='<h3>Ce qu’il permet ou laisse ouvert</h3>'+(outgoing.map(e=>rel(e,'out')).join('')||'<p>But terminal ou relation distale non construite : aucune implication n’est inventée.</p>');
    if(tasks.length)body+='<h3>Usage dans les investigations actuelles</h3><ul>'+tasks.map(a=>'<li>'+link('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#action-'+a.id,a.label)+'</li>').join('')+'</ul>';
    if(n.initial_detail_html)body+='<details class="original-detail"><summary>Détail d’origine et contexte de départ</summary>'+n.initial_detail_html+'</details>';
    el('node-body').innerHTML=body;
    // Original details are root-relative corpus fragments, including on nested views.
    el('node-body').querySelectorAll('.original-detail a[href],.original-detail img[src]').forEach(item=>{
      const attr=item.tagName==='IMG'?'src':'href',p=item.getAttribute(attr);
      if(p&&!/^(?:[a-z][a-z0-9+.-]*:|\/|#)/i.test(p))item.setAttribute(attr,S.prefix+p);
    });
    if(!dlg.open){if(dlg.showModal)dlg.showModal();else dlg.setAttribute('open','')}
    dlg.scrollTop=0;history.replaceState(null,'','#node='+encodeURIComponent(n.uid));
  }
  document.addEventListener('click',e=>{const b=e.target.closest('[data-node]');if(b){if(b.tagName.toLowerCase()==='a')e.preventDefault();openNode(b.dataset.node,b)}});
  document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('.mapnode')){e.preventDefault();openNode(e.target.dataset.node,e.target)}});
  el('close-dialog').addEventListener('click',()=>dlg.close?dlg.close():dlg.removeAttribute('open'));
  dlg.addEventListener('click',e=>{if(e.target===dlg){const r=dlg.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dlg.close()}});
  dlg.addEventListener('close',()=>{if(last&&last.isConnected&&(document.activeElement===document.body||dlg.contains(document.activeElement)))last.focus();if(location.hash.startsWith('#node='))history.replaceState(null,'',location.pathname+location.search)});
  document.querySelectorAll('[data-search]').forEach(input=>input.addEventListener('input',()=>{
    const q=input.value.toLocaleLowerCase('fr');document.getElementById(input.dataset.search).querySelectorAll('[data-search-row]').forEach(row=>row.hidden=!row.textContent.toLocaleLowerCase('fr').includes(q));
  }));
  if(el('comparison')){
    const I=S.indicator,E=I.etapes,D=I.dimensions;
    function compare(){
      const a=E[Number(el('compare-before').value)],b=E[Number(el('compare-after').value)];
      el('comparison').innerHTML='<p><b>'+escape(a.court)+' → '+escape(b.court)+'</b> : les changements ci-dessous concernent ces deux étapes.</p><div class="comparison">'+D.map(d=>'<div><span>'+escape(d.nom)+'</span><b>'+a.niveaux[d.id]+' → '+b.niveaux[d.id]+'</b></div>').join('')+'</div>';
    }
    el('compare-before').addEventListener('change',compare);el('compare-after').addEventListener('change',compare);compare();
    el('sparklines').innerHTML=D.map(d=>{
      let path='M 12 '+(84-8*E[0].niveaux[d.id]);E.forEach((e,i)=>{if(i)path+=' H '+(12+356*i/(E.length-1))+' V '+(84-8*e.niveaux[d.id])});
      return '<article class="spark"><h3>'+escape(d.nom)+'<span>'+E[E.length-1].niveaux[d.id]+'/9</span></h3><svg viewBox="0 0 380 96" role="img" aria-label="'+escape(d.nom)+', parcours complet de '+E.length+' étapes"><path class="axis" d="M12 4 V84 H368"/><path class="trace" d="'+path+'"/>'+E.map((e,i)=>'<circle cx="'+(12+356*i/(E.length-1))+'" cy="'+(84-8*e.niveaux[d.id])+'" r="2" fill="#15557a"><title>'+escape(e.court+' : '+e.niveaux[d.id]+' ; '+(e.pourquoi[d.id]||'niveau conservé'))+'</title></circle>').join('')+'</svg><div class="foot">'+escape(E[0].court)+' → '+escape(E[E.length-1].court)+'</div></article>'
    }).join('');
  }
  if(el('bellman-result')){
    const base=JSON.parse(JSON.stringify(S.bellman)),labels=Object.fromEntries(base.actions.map(a=>[a.id,a.label]));
    const names={structural:'Contrats et couplages',local:'Étude locale',clarity:'Lecture et réfutation'};
    function calculate(){
      const budget=Math.round(Math.max(0,Math.min(12,Number(el('budget').value)||0)));el('budget').value=budget;
      const weights=Object.fromEntries(Object.keys(names).map(k=>[k,Math.max(0,Math.min(5,Number(el('w-'+k).value)||0))]));
      const model=applyBridgeWeightProfile(base,weights);
      for(const a of model.actions){
        const lo=Math.round(Math.max(1,Math.min(12,Number(el('c-'+a.id+'-lo').value)||1)));
        const hi=Math.round(Math.max(lo,Math.min(12,Number(el('c-'+a.id+'-hi').value)||lo)));
        a.duration=[lo,hi];el('c-'+a.id+'-lo').value=lo;el('c-'+a.id+'-hi').value=hi;
      }
      const r=solveBridgeEnvelopes(model,budget,S.bellman_state.facts,S.bellman_state.completed);
      const choices=d=>d.first_choices.map(k=>k==='STOP'?'STOP':link('1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#contrat-'+k,labels[k])).join(' · ');
      let text='<h3>Gains de capacité dans les scénarios : '+r.lower.gain+' à '+r.upper.gain+' U · budget '+budget+' H</h3>';
      text+='<p><b>Enveloppe pessimiste :</b> '+choices(r.lower)+'.</p><p><b>Enveloppe optimiste :</b> '+choices(r.upper)+'.</p>';
      text+='<details><summary>Valeur des premiers choix et de leurs issues</summary><ul>'+Object.entries(r.lower.choice_values).map(([k,v])=>'<li>'+escape(labels[k]||k)+' : '+v+' U (bas)'+(r.upper.choice_values[k]!==undefined?' ; '+r.upper.choice_values[k]+' U (haut)':'')+'</li>').join('')+'</ul></details>';
      text+='<p class="foot">Les gains concernent les capacités déclarées de ce modèle fini. Les futurs choix dépendent des issues. Le signe global, la couverture signée et RH restent ouverts.</p>';
      if(el('ciblage-bellman-live'))el('ciblage-bellman-live').innerHTML='<p><strong>Étude du modèle Bellman, budget '+budget+' H :</strong> '+choices(r.lower)+'. Les réglages sont ceux affichés ci-dessous ; aucun programme n’est lancé.</p>';
      el('bellman-result').innerHTML=text;el('bellman-result').dataset.value=r.lower.value;el('bellman-result').dataset.first=JSON.stringify(r.lower.first_choices);el('bellman-result').dataset.upper=JSON.stringify(r.upper.first_choices);
    }
    el('weights').innerHTML=Object.keys(names).map(k=>'<label>'+names[k]+'<input id="w-'+k+'" type="number" min="0" max="5" value="1"></label>').join('');
    el('costs').innerHTML=base.actions.map(a=>'<label>'+escape(a.label)+'<span><input aria-label="Durée basse" id="c-'+a.id+'-lo" type="number" min="1" max="12" value="'+a.duration[0]+'">–<input aria-label="Durée haute" id="c-'+a.id+'-hi" type="number" min="1" max="12" value="'+a.duration[1]+'"> H</span></label>').join('');
    el('budget').addEventListener('input',calculate);
    [...el('weights').querySelectorAll('input'),...el('costs').querySelectorAll('input')].forEach(x=>x.addEventListener('input',calculate));calculate();
  }
  if(el('graph-family')){
    function filter(){const f=el('graph-family').value,t=el('graph-status').value,q=el('graph-search').value.toLocaleLowerCase('fr');let shown=0;
      document.querySelectorAll('[data-idea-card]').forEach(n=>{const yes=(!f||n.dataset.family===f)&&(!t||n.dataset.status===t)&&n.textContent.toLocaleLowerCase('fr').includes(q);n.hidden=!yes;if(yes)shown++});el('graph-count').textContent=shown+' nœud(s) visible(s) sur '+S.nodes.length;}
    ['graph-family','graph-status','graph-search'].forEach(k=>el(k).addEventListener(k==='graph-search'?'input':'change',filter));filter();
  }
  if(location.hash.startsWith('#node=')){const k=decodeURIComponent(location.hash.slice(6));openNode(k,null)}
  window.steeringReady=true;
})();
}
