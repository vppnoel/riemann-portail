# Mémo P2.3 — Peut-on tirer une densité de zéros de Q ? (go/no-go)  (v3.7)

**Réponse : NO-GO pour améliorer les densités connues** ; GO seulement pour un usage de calibration.

## 1. Cible
Borner N(σ,T)=#{ρ : β≥σ, \|γ\|≤T} par T^{c(1−σ)}. État de l'art : Ingham 3/(2−σ), Huxley 12/5 (σ≥3/4), **Guth–Maynard 30/13** (*Ann. of Math.* 203, 2026)
près de σ=3/4 ; hypothèse de densité : 2. Un résultat du cadre Q devrait battre 30/13 quelque part, ou au moins retrouver 12/5.

## 2. Trois routes depuis Q, et pourquoi chacune échoue
**Route A — Plancherel sur des droites intérieures.** Q_η=(1/2π)∫\|G(σ'+it)\|²/\|s\|²dt est une identité **seulement pour σ'>Θ**
(sinon l'intégrale de Mellin de C diverge). Pour une densité il faut des droites σ'<Θ : circulaire.

**Route B — énergie de fenêtre et zéros isolés.** Borne inférieure de l'énergie d'une fenêtre par la contribution d'un sous-ensemble de zéros (β≥σ) :
impossible, car les fréquences γ,γ' à distance <1/L ne sont pas orthogonales et les zéros restants (β<σ) peuvent s'annuler avec eux (pas de positivité
séparante — c'est P2.2). Les méthodes de densité évitent cela en **évaluant aux zéros** (valeurs ponctuelles), ce qui transforme un problème L² en
problème de **grandes valeurs** (inégalité de Halász–Montgomery, théorèmes de Huxley, Guth–Maynard).

**Route C — polynômes de Dirichlet de Q.** Les coefficients a(n)=μ(n)(log²n−2γ log n) vérifient \|a(n)\|≪log²n : même classe que les mollificateurs
classiques. Les sommes partielles de G sont, aux effets de domaine près (pq≤X), le **carré** (Σ_{m≤X}Λ(m)m^{-s})² d'un polynôme premier. Toute densité
obtenue serait donc une instance de « grandes valeurs de polynômes de Dirichlet à coefficients bornés » : aucune structure de c (≤2 premiers distincts)
n'apporte plus que la décomposition bilinéaire de Vaughan/Heath-Brown, déjà exploitée.

## 3. Mesure du détecteur d'énergie (`scripts/run_localisation.py`, ce mémo)
- Énergie totale d'un signal B de longueur L : ∫B²dt = U(L) (identité de Plancherel) — petite (≈150 à L=12,6).
- **Plancher de bruit** des sauts de C (sommes de c(n)n^{-s}) : Σ_{n≤3·10⁵}c(n)²/n = 6 691 (≈ 0,02 log⁵X).
- **Rapport signal/bruit des raies de zéros** (fenêtre de Hann, L=12,6, 21 zéros 8<γ<80) :

| plage γ | SNR médian | SNR min | n |
|---|---|---|---|
| 8–25 | 55 | 39 | 2 |
| 25–45 | 11,5 | 7,2 | 6 |
| 45–80 | 3,3 | 2,4 | 13 |

SNR·γ² ≈ 1,2–1,6·10⁴ sur les trois plages : **SNR ∝ 1/γ²** (cohérent avec \|A_γ\|²=4/\|ρ\|²). À L=12,6 les raies passent sous le plancher vers γ≈110.
La dépendance en L n'a pas été mesurée. Dans le régime des densités (X=T^A, L=A log T) il faudrait un SNR qui croît plus vite que T² : rien ne l'indique.

## 4. Verdict
| Question | Réponse |
|---|---|
| Q fournit-il une inégalité de densité nouvelle ? | Non attendu : se réduit à des grandes valeurs (Route B/C) |
| Retrouve-t-il Ingham/Huxley ? | Non démontré ; non tenté (aucune route claire) |
| Utile en calibration ? | Oui : localisation des zéros jusqu'à γ≈100 (18/20 pics) et SNR ∝ 1/γ² |

**Règle d'arrêt P2 (test 3) : déclenchée.** Avec le test 2 (P2.2) et le test 1 (couche générique), le cadre ne fournit ni positivité ni gain de densité.

## 5. Limites
Le jugement des routes A–C est un raisonnement, non un théorème ; les SNR sont mesurés sur un seul L et une seule fenêtre (21 zéros).
L'énoncé de Halász–Montgomery est invoqué sans en recopier la forme ([À VÉRIFIER] avant publication).
