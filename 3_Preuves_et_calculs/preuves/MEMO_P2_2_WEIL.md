# Mémo P2.2 — Positivité de Weil (corps de fonctions) et ce qui lui correspond dans Q  (v3.7)

**Question.** La preuve de RH sur les corps de fonctions repose sur une positivité géométrique. Le cadre Q en
contient-il un analogue exploitable ? **Réponse : non.** Détail ci-dessous.

## 1. Les ingrédients de la preuve sur F_q (sources : Weil 1942–48 ; Bombieri–Stepanov ; Schoof, *RHcurves* ; Kedlaya, ch. 5)
| | Ingrédient | Rôle |
|---|---|---|
| (I) | **Rationalité** : Z(T)=P(T)/((1−T)(1−qT)), deg P=2g | un nombre fini de zéros = valeurs propres de Frobenius |
| (II) | **Tour d'extensions** : il suffit de prouver la borne sur N_r pour une puissance r de q (ou pour tout r) | passe d'une borne en O(q^{r/2}) à |α_i|=√q |
| (III) | **Positivité géométrique** : sur C×C, théorème de l'indice de Hodge ⇒ inégalité de Castelnuovo–Severi (D−d₂C₁−d₁C₂)² ≤ 0 ⇒ Hasse–Weil \|N_r−q^r−1\| ≤ 2g q^{r/2} | fournit la borne elle-même |

Voie alternative (Stepanov–Bombieri) : fonction auxiliaire s'annulant à haut ordre sur C×C, Riemann–Roch ; elle utilise aussi (II) et le
Frobenius comme endomorphisme d'une des deux coordonnées. Dans les deux cas **la surface C×C est essentielle**. Pour Spec Z, Spec Z × Spec Z = Spec Z
est de dimension 1 (remarque de van Frankenhuijsen, arXiv:0806.0044) : c'est l'obstruction géométrique connue à la transposition.

## 2. Dictionnaire avec le cadre Q
| Corps de fonctions | Cadre Q (ζ) | Verdict |
|---|---|---|
| (I) finitude (2g valeurs propres) | infinité de zéros ; pas d'espace de dimension finie | pas d'analogue |
| (II) tour q^r | aucune extension de corps de base ; log p n'est pas une « dimension » | pas d'analogue |
| (III) signature (1,n) de l'indice de Hodge | Gram de Nyman–Beurling **définie positive** (NB_GRAM : cond ≈ 3·10³ à N=30) | positivité **automatique**, donc sans contenu |
| formule explicite de Weil Σ_ρ f̂(ρ) = ⟨D_f,Diag⟩ | Q = ∫\|C\|²x⁻², C=Σc(n), c=Λ*Λ−Λ·log+2γΛ | Q est le **carré** de la formule explicite ; Weil évalue la formule explicite sur un carré f*f̃ |

**Point central.** Le terme dominant de Q est S=Σ_ρ A_ρ²/\|ρ\|² = Σ_ρ \|f̂(ρ)\|² avec f̂(s)=A/s : une évaluation de la fonctionnelle de Weil
sur **une seule** fonction test (non à support compact). Mais :
- Q voit \|f̂(ρ)\|² (toujours ≥ 0, pondéré par X^{2β−1}) ; le critère de Weil porte sur f̂(ρ)·conj f̂(1−ρ̄), de **signe variable** hors de la droite
  critique. Le contenu de RH est ce signe ; Q ne l'a pas.
- Le critère de Weil exige la positivité pour **toute** f ; Q n'en teste qu'une famille (dilatations de la partie fractionnaire).

## 3. Démonstration numérique (`scripts/run_function_field_analog.py`, `data/function_field_analog.csv`)
Courbes elliptiques sur F_101, P(T)=1−aT+pT² ; analogue exact de q, c, C, Q (q_n=−s_n, c_n=(s*s)_n+n s_n).
| cas | rayon max de α | Q_M / M³ à M=10, 20, 40, 60 |
|---|---|---|
| a=10 (RH vraie) | 10,05 = √p | 2,49 ; 2,46 ; 2,78 ; 2,90 (cubique) |
| a=25 (viole Hasse) | 19,93 > √p | 4,7·10⁵ ; 2,2·10¹¹ ; 8,9·10²² ; 4,7·10³⁴ (exponentiel) |
Même théorème que sur ζ : cubique ⇔ zéros sur la droite. **Mais** : sur les 10 100 courbes lisses y²=x³+Ax+B sur F_101, max\|a\|=20 ≤ 2√101=20,1 ;
a=25 n'apparaît jamais. Cette borne est produite par la **géométrie**, pas par Q : Q est un thermomètre (il enregistre la croissance après coup),
non un interdit (il ne peut pas exclure a=25).

## 4. Verdict et conséquence
- **NO-GO** pour « le cadre Q contient la positivité de Weil ». Aucun des trois ingrédients (I)–(III) n'y a d'image.
- La seule voie positive connue sur Z est le critère de Weil (positivité de la distribution explicite sur f*f̃) et ses variantes (Li, Connes) : c'est
  une reformulation de RH, déjà connue, non une preuve.
- **Règle d'arrêt P2 (test 2) : déclenchée.** À rapprocher du test 1 (Euler product localisé, couche générique) et du mémo P2.3.

## 5. Limites de ce mémo
Les attributions (Weil, Bombieri–Stepanov, van Frankenhuijsen, Schoof, Kedlaya) sont lues dans les résumés/pages consultées le 2026-10-03, pas dans les textes
complets ; l'énoncé du critère de Weil est cité de mémoire ([À VÉRIFIER] avant toute publication).
