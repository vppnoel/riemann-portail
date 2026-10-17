/* Recorded certificates and learning UI; simulated DOM, no browser rendering. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
function run(file,ids,defaults){
 const html=fs.readFileSync(path.join(root,'1_Presentation',file),'utf8');
 class E{constructor(id){this.value=defaults[id]??'';this.innerHTML='';this.textContent='';this.hidden=false;this.events={};}addEventListener(t,f){this.events[t]=f;}fire(t){assert(this.events[t]);this.events[t]();}}
 const els={},document={getElementById(id){return els[id]??(els[id]=new E(id));}};
 for(const id of ids)document.getElementById(id).textContent=html.match(new RegExp('<script id="'+id+'" type="application/json">([\\s\\S]*?)</script>'))[1];
 const c={document,window:{}};vm.createContext(c);vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],c);
 return {c,el:id=>document.getElementById(id)};
}
const {c,el}=run('72_CONCENTRATION_PROJETEE.html',['concentration-data','operator-data'],{level:'6.8',support:'0.375',metric:'R',unit:'A2'});
assert(el('connection').textContent.includes('valide'));
for(const u of ['0.02','5','7.2']){el('level').value=u;el('level').fire('input');assert(el('layer').innerHTML.includes('Concentration retenue')&&!el('layer').innerHTML.includes('NaN'));}
el('support').value='0.5';el('connect').fire('click');assert(el('connection').textContent.includes('hors'));
for(const s of ['0','-1','NaN']){el('support').value=s;el('connect').fire('click');assert(el('connection').textContent.includes('refusé'));}
el('support').value='0.3';el('metric').value='H1';el('connect').fire('click');assert(el('connection').textContent.includes('incompatible'));
el('metric').value='R';el('unit').value='A';el('connect').fire('click');assert(el('connection').textContent.includes('incompatible'));
assert(el('diagnostic').innerHTML.includes('Nyström'));
const p=run('69_LANGUE_DES_PASSAGES.html',['pedagogy-data','archive-data'],{door:'all'});
for(const id of ['joint_cost','sublevel','schatten2','common_operator']){
 p.c.window.pedagogicalDictionary.openLesson(id);assert(p.el('entry').innerHTML.includes('data:image/svg+xml;base64,')&&p.el('entry').innerHTML.includes('À quoi cela sert ici'));
}
p.c.window.pedagogicalDictionary.tab('tools');assert(!p.el('tools').hidden);
p.el('door').value='Couplages';p.c.window.pedagogicalDictionary.uses();assert(p.el('tool-list').innerHTML.includes('Opérateur commun'));
console.log('V647 : certificat, couches, gardes de support/métrique/unités ; 4 nouvelles leçons, SVG, usages et prérequis vérifiés par DOM simulé.');
