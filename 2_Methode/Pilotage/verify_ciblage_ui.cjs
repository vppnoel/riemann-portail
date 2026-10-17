/* Exercise actual ui.js input handlers with a minimal DOM harness.
   This checks JavaScript integration, not browser layout or accessibility. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const html=fs.readFileSync(path.join(root,'1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html'),'utf8');
const payload=html.match(/<script type="application\/json" id="steering-data">([\s\S]*?)<\/script>/)[1];
const nodes=new Map();
class Element {
 constructor(id,value=''){this.id=id;this.value=value;this.dataset={};this.listeners={};this.inputs=[];nodes.set(id,this)}
 addEventListener(name,fn){this.listeners[name]=fn}
 querySelectorAll(selector){return selector==='input'?this.inputs:[]}
 set innerHTML(text){this.markup=text;this.inputs=[];
  for(const tag of text.matchAll(/<input\b[^>]*>/g)){
   const id=tag[0].match(/id="([^"]+)"/),v=tag[0].match(/value="([^"]*)"/);
   if(id)this.inputs.push(new Element(id[1],v?v[1]:''));
  }
 }
 get innerHTML(){return this.markup||''}
}
for(const id of ['node-dialog','close-dialog','bellman-result','weights','costs','ciblage-bellman-live'])new Element(id);
new Element('budget','6');new Element('steering-data').textContent=payload;
const document={getElementById:id=>nodes.get(id)||null,querySelectorAll:()=>[],addEventListener:()=>{}};
const context=vm.createContext({document,window:{},location:{hash:''},console});
vm.runInContext(fs.readFileSync(path.join(__dirname,'bellman_contracts.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(__dirname,'ui.js'),'utf8'),context);
const el=id=>nodes.get(id);const checks=[];
const ck=(name,ok)=>{assert(ok,name);checks.push({name,passed:true})};
ck('initial budget 6 : noyaux',el('bellman-result').dataset.first==='["noyaux"]'&&el('ciblage-bellman-live').innerHTML.includes('noyaux'));
el('budget').value='0';el('budget').listeners.input();
ck('budget 0 : STOP synchronisé',el('bellman-result').dataset.first==='["STOP"]'&&el('ciblage-bellman-live').innerHTML.includes('STOP')&&el('ciblage-bellman-live').innerHTML.includes('budget 0'));
el('budget').value='6';el('budget').listeners.input();
ck('retour budget 6 : choix restauré',el('bellman-result').dataset.first==='["noyaux"]');
const before=el('ciblage-bellman-live').innerHTML;
el('w-structural').value='0';el('w-structural').listeners.input();
const after=el('ciblage-bellman-live').innerHTML;
const choices=JSON.parse(el('bellman-result').dataset.first);
ck('poids : résumé aligné sur moteur',choices.every(k=>after.includes(k==='STOP'?'STOP':JSON.parse(payload).bellman.actions.find(a=>a.id===k).label)));
ck('actualisation sans mutation du modèle source',el('steering-data').textContent===payload&&context.window.steeringReady===true);
console.log(JSON.stringify({checks,passed:checks.length,scope:'DOM harness, actual JavaScript handlers; no browser layout test',browser_visual_QA:false},null,2));
