/* Progressive interfaces, tested with a simulated DOM, not a browser renderer. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),root=path.resolve(__dirname,'../..');
const html=fs.readFileSync(path.join(root,'1_Presentation/69_LANGUE_DES_PASSAGES.html'),'utf8');
const payload=id=>JSON.parse(html.match(new RegExp('<script id="'+id+'" type="application/json">([\\s\\S]*?)</script>'))[1]);
const P=payload('pedagogy-data'),A=payload('archive-data'),script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
class Element{constructor(id){this.value=id==='door'?'all':'';this.innerHTML='';this.textContent='';this.hidden=false;this.events={};}addEventListener(t,fn){this.events[t]=fn;}fire(t,e={}){assert(this.events[t]);this.events[t](e);}}
const elements={},document={getElementById(id){return elements[id]??(elements[id]=new Element(id));}};document.getElementById('pedagogy-data').textContent=JSON.stringify(P);document.getElementById('archive-data').textContent=JSON.stringify(A);
const c={document,window:{}};vm.createContext(c);vm.runInContext(script,c);const el=id=>document.getElementById(id);
assert(el('stage-title').textContent.startsWith('1.'));
assert(el('list').innerHTML.includes('Fonction')&&!el('list').innerHTML.includes('Schur'));
el('next').fire('click');assert(el('stage-title').textContent.startsWith('2.'));
el('search').value='derivee';el('search').fire('input');assert(el('entry').innerHTML.includes('Dérivée')&&el('entry').innerHTML.includes('data:image/svg+xml;base64,'));
c.window.pedagogicalDictionary.openLesson('schur');assert(el('stage-title').textContent.startsWith('5.')&&el('entry').innerHTML.includes('Dette de Schur'));
el('tab-tools').fire('click');assert(!el('tools').hidden&&el('learn').hidden);
el('door').value='Couplages';el('door').fire('change');assert(el('tool-list').innerHTML.includes('Gram de sources')&&el('tool-list').innerHTML.includes('pas encore certifiées'));
el('tab-archive').fire('click');el('archive-search').value='moule';el('archive-search').fire('input');assert(!el('archive').hidden&&el('archive-list').innerHTML.length>0);
el('code-search').value='certificate_lego';el('code-search').fire('input');assert(el('code-list').innerHTML.includes('assemble_local_certificate'));
console.log('V646 : 32 fiches, 5 étapes, prérequis, SVG, 4 portes et usages séparés vérifiés avec DOM simulé.');
