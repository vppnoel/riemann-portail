/* Exercise client grammar and DOM event handlers without a browser renderer. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const html=fs.readFileSync(path.join(root,'1_Presentation/69_LANGUE_DES_PASSAGES.html'),'utf8');
if(html.includes('id="pedagogy-data"')){require('./check_v646_pedagogy.js');require('./check_v646_grammar.js');}
else {
const data=JSON.parse(html.match(/<script id="language-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const defaults={search:'',level:'all',kind:'all',S:'1',r:'1',q:'0',u:'1',op:'add',parameter:'1','code-search':''};
class Element{
 constructor(id){this.id=id;this.value=defaults[id]??'';this.innerHTML='';this.textContent='';this.hidden=true;this.events={};}
 addEventListener(type,fn){this.events[type]=fn;}
 fire(type,event={}){assert(this.events[type],type+' missing');this.events[type](event);}
}
const elements={};const document={getElementById(id){return elements[id]??(elements[id]=new Element(id));}};
document.getElementById('language-data').textContent=JSON.stringify(data);
const context={document,window:{},console};vm.createContext(context);vm.runInContext(script,context);
const cases=JSON.parse(fs.readFileSync(path.join(root,'3_Preuves_et_calculs/data/v644_clients_grammaire.json'),'utf8'));
for(const c of cases){const out=context.window.languageGrammar.infer(c.op,c.input,c.parameter);for(const k of ['S','r','q','u'])assert(Math.abs(out[k]-c.expected[k])<1e-12,JSON.stringify({c,out,k}));}
const el=id=>document.getElementById(id);
el('search').value='derivee';el('search').fire('input');assert(el('list').innerHTML.includes('Dérivée'));
el('search').value='';el('kind').value='metaphor';el('kind').fire('input');assert(el('count').textContent.startsWith('95 fiches'));
el('list').fire('click',{target:{closest(){return {dataset:{entry:'math:convolution_algebra'}};}}});assert(el('entry').innerHTML.includes('Algèbre de convolution'));
el('op').value='multiply';el('play').fire('click');assert(el('result').textContent.includes('non garantis'));
el('op').value='P';el('play').fire('click');assert(el('result').textContent.includes('r=2'));
el('r').value='-1';el('play').fire('click');assert(el('result').textContent.includes('refusée'));
el('global').fire('click');assert(!el('global-result').hidden&&el('global-result').textContent.includes('tous les supports'));
el('code-search').value='domain_grammar.py';el('code-search').fire('input');assert(el('code-list').innerHTML.includes('translate'));
console.log(cases.length+' contrats JavaScript/Python concordants ; recherche sans accents, filtres, sélection, jeu et garde globale vérifiés avec DOM simulé.');

}
