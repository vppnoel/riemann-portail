const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'../..');
const {solveAtlas}=require(path.join(root,'2_Methode/Outils/bellman_atlas_client.js'));
const f=JSON.parse(fs.readFileSync(path.join(root,'3_Preuves_et_calculs/data/v642_bellman_controles.json'),'utf8'));
const canonical=p=>JSON.stringify(p.map(x=>[...x].sort()).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b))));
for(const r of f.cases){const a=solveAtlas(f.model,r.budget,r.weights,f.completed),b=r.expected;if(a.value!==b.value||a.gain!==b.gain||canonical(a.portfolios)!==canonical(b.portfolios)||JSON.stringify([...a.first_choices].sort())!==JSON.stringify([...b.first_choices].sort()))throw Error('V642 Bellman client mismatch');}
console.log(JSON.stringify({cases:f.cases.length,all_results_match:true,all_ties_retained:true}));
