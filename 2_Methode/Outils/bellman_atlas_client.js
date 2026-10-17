// Finite documentary model. STOP, all ties and unique actions are preserved.
function solveAtlas(model, budget, weights, completed=[]) {
  const actions = model.actions, memo = new Map();
  function utility(mask) {
    const tokens = new Set();
    actions.forEach((a, i) => { if (mask & (1 << i)) a.tokens.forEach(t => tokens.add(t)); });
    return [...tokens].reduce((s, t) => s + weights[model.tokens[t]], 0);
  }
  function visit(mask, remaining) {
    const key = mask + ':' + remaining;
    if (memo.has(key)) return memo.get(key);
    let value = utility(mask), first = ['STOP'], endpoints = new Set([mask]);
    actions.forEach((a, i) => {
      const bit = 1 << i;
      if ((mask & bit) || a.cost > remaining || !a.requires.every(k => mask & (1 << actions.findIndex(x => x.id === k)))) return;
      const next = visit(mask | bit, remaining - a.cost);
      if (next.value > value) { value = next.value; first = [a.id]; endpoints = new Set(next.endpoints); }
      else if (next.value === value) { first.push(a.id); next.endpoints.forEach(e => endpoints.add(e)); }
    });
    const result = {value, first_choices: first, endpoints}; memo.set(key, result); return result;
  }
  const start=completed.reduce((mask,k)=>mask|(1<<actions.findIndex(a=>a.id===k)),0);
  const result = visit(start, budget);
  return {value: result.value, gain: result.value-utility(start), first_choices: result.first_choices,
          portfolios: [...result.endpoints].map(mask => actions.filter((a, i) => mask & (1 << i)).map(a => a.id).sort()).sort((a,b) => JSON.stringify(a).localeCompare(JSON.stringify(b)))};
}
if (typeof module !== 'undefined') module.exports = {solveAtlas};
