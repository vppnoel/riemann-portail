// Auteur et titulaire des droits : Vincent NOËL.
// Rend en MathML (rendu natif du navigateur, sans police ni réseau) les formules LaTeX de matrice_theories.json.
// Usage : NODE_PATH=<dossier node_modules contenant katex> node render_formules.js
const fs = require('fs'), path = require('path'), katex = require('katex');
const p = path.join(__dirname, 'matrice_theories.json');
const M = JSON.parse(fs.readFileSync(p, 'utf8')); let bad = 0;
for (const n of M.noeuds) {
  if (!n.formule) continue;
  try { n.formule_mathml = katex.renderToString(n.formule, {output: 'mathml', displayMode: true, throwOnError: true}); }
  catch (e) { bad++; console.error(n.id, e.message); }
}
fs.writeFileSync(p, JSON.stringify(M, null, 1), 'utf8');
console.log(`formules rendues : ${M.noeuds.filter(n => n.formule_mathml).length}, erreurs : ${bad}`);
