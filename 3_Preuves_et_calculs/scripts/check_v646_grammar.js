const fs=require('fs'),path=require('path'),assert=require('assert'),root=path.resolve(__dirname,'../..');
const {infer}=require(path.join(root,'2_Methode/Outils/domain_grammar_client.js'));
const cases=JSON.parse(fs.readFileSync(path.join(root,'3_Preuves_et_calculs/data/v644_clients_grammaire.json'),'utf8'));
for(const c of cases){const out=infer(c.op,c.input,c.parameter);for(const k of ['S','r','q','u'])assert(Math.abs(out[k]-c.expected[k])<1e-12);}
console.log(cases.length+' contrats historiques JavaScript/Python vérifiés ; le parcours pédagogique reste séparé.');
