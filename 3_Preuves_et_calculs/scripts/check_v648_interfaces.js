/* Mathematical contracts in a simulated DOM; no browser-layout claim. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const {rationalDisplay}=require(path.join(root,'2_Methode/Outils/rational_display.js'));
assert(Math.abs(rationalDisplay('1'+'0'.repeat(500)+'/'+'2'+'0'.repeat(500))-.5)<1e-15);
assert(Math.abs(rationalDisplay('-1'+'0'.repeat(500)+'/'+'4'+'0'.repeat(500))+.25)<1e-15);
assert(Number.isNaN(rationalDisplay('1/0')));
function run(file,ids,defaults){
 const h=fs.readFileSync(path.join(root,'1_Presentation',file),'utf8');
 class E{constructor(id){this.value=defaults[id]??'';this.innerHTML='';this.textContent='';this.hidden=false;this.events={};}addEventListener(t,f){this.events[t]=f;}fire(t){assert(this.events[t]);this.events[t]();}}
 const els={},document={getElementById(id){return els[id]??(els[id]=new E(id));}};
 for(const id of ids)document.getElementById(id).textContent=h.match(new RegExp('<script id="'+id+'" type="application/json">([\\s\\S]*?)</script>'))[1];
 const c={document,window:{}};vm.createContext(c);vm.runInContext(h.match(/<script>([\s\S]*?)<\/script>/)[1],c);
 return {c,el:id=>document.getElementById(id)};
}
const a=run('73_OPERATEUR_COMMUN.html',['common-data'],{parity:'0','source-form':'A',support:'0.5',metric:'R',unit:'A2'});
assert(a.el('connection').textContent.includes('valide'));
for(const p of ['0','1']){a.el('parity').value=p;a.el('parity').fire('change');assert(a.el('budgets').innerHTML.includes('Marge de Schur')&&!a.el('budgets').innerHTML.includes('NaN'));}
a.el('source-form').value='Q';a.el('source-form').fire('change');assert(a.el('source-status').textContent.includes('non calculées')&&a.el('source-status').textContent.includes('signe'));
a.el('source-form').value='A';a.el('source-form').fire('change');assert(a.el('source-status').textContent.includes('Certifié'));
a.el('support').value='0.6';a.el('connect').fire('click');assert(a.el('connection').textContent.includes('hors'));
a.el('support').value='0';a.el('connect').fire('click');assert(a.el('connection').textContent.includes('refusé'));
a.el('support').value='0.4';a.el('metric').value='H1';a.el('connect').fire('click');assert(a.el('connection').textContent.includes('incompatible'));
a.el('metric').value='R';a.el('unit').value='A';a.el('connect').fire('click');assert(a.el('connection').textContent.includes('incompatible'));
const d=run('69_LANGUE_DES_PASSAGES.html',['pedagogy-data','archive-data'],{door:'all'});
for(const id of ['cardinal_frame','interpolation_error','operator_error','minorant_sources']){
 d.c.window.pedagogicalDictionary.openLesson(id);assert(d.el('entry').innerHTML.includes('data:image/svg+xml;base64,')&&d.el('entry').innerHTML.includes('À quoi cela sert ici'));
}
d.el('door').value='Couplages';d.c.window.pedagogicalDictionary.uses();assert(d.el('tool-list').innerHTML.includes('Assembler tête, sources et queue'));
console.log('V648 : 2 parités, sources A/Q distinctes, raccords de support/norme/unités, 4 nouvelles leçons et usages vérifiés par DOM simulé.');
