/* Executed workshop contracts in a simulated DOM; no browser-layout claim. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
function run(file,ids,defaults){
 const h=fs.readFileSync(path.join(root,'1_Presentation',file),'utf8');
 class E{constructor(id){this.value=defaults[id]??'';this.innerHTML='';this.textContent='';this.hidden=false;this.events={};}addEventListener(t,f){this.events[t]=f;}fire(t){assert(this.events[t]);this.events[t]();}}
 const els={},document={getElementById(id){return els[id]??(els[id]=new E(id));}};
 for(const id of ids)document.getElementById(id).textContent=h.match(new RegExp('<script id="'+id+'" type="application/json">([\\s\\S]*?)</script>'))[1];
 const c={document,window:{}};vm.createContext(c);vm.runInContext(h.match(/<script>([\s\S]*?)<\/script>/)[1],c);
 return {c,el:id=>document.getElementById(id)};
}
const a=run('74_COMPENSATION_MULTI_PREMIERS.html',['payment-data','diagnostic-data'],{support:'1',cap:'10'});
assert(a.el('payment').innerHTML.includes('Réserve d’énergie positive')&&a.el('payment').innerHTML.includes('Le signe de Q reste'));
for(const s of ['1/2','11/20','3/5','7/10','4/5','1','2']){
 a.el('support').value=s;a.el('support').fire('change');assert(!/NaN|Infinity/.test(a.el('payment').innerHTML));
 if(s==='2')assert(a.el('payment').innerHTML.includes('aucune conclusion'));
}
a.el('support').value='11/20';a.el('support').fire('change');assert(a.el('diagnostic').innerHTML.includes('0.000583')&&a.el('diagnostic').innerHTML.includes('Aucune extension'));
a.el('support').value='5';a.el('support').fire('change');assert(a.el('payment').textContent.includes('Aucun certificat'));
const d=run('69_LANGUE_DES_PASSAGES.html',['pedagogy-data','archive-data'],{door:'all'});
for(const id of ['prime_phase','edge_multiplicity','joint_payment']){
 d.c.window.pedagogicalDictionary.openLesson(id);assert(d.el('entry').innerHTML.includes('data:image/svg+xml;base64,')&&d.el('entry').innerHTML.includes('À quoi cela sert ici'));
}
d.el('door').value='Arithmétique';d.c.window.pedagogicalDictionary.uses();assert(d.el('tool-list').innerHTML.includes('Paiement des bandes conjointes'));
console.log('V649 : sept supports enregistrés ; paiement/signification distincts ; diagnostic non certifié ; trois leçons et usages contrôlés par DOM simulé.');
