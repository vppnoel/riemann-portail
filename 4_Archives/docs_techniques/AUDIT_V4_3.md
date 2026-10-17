# Audit de la V4.3 (branches localisation de sources, Schrödinger/flux, générateur arithmétique) — v4.4

**Verdict.** La base A/B/C est inchangée et saine. Les trois branches V4.1–V4.3 sont de la **reformulation et du traitement de signal** ; elles ne contiennent aucun mécanisme
qui force β = ½. Sur le vrai signal arithmétique, la chaîne primes → A → H_eff **biaise** la partie réelle (jusqu'à −0,09 sur des zéros critiques) et, sur le témoin
Davenport–Heilbronn, **produit un mode fantôme** plus « hors ligne » que le vrai zéro hors ligne. Les 30 tests de la V4.3 passent, mais plusieurs sont circulaires.

## F1. Les tests V4.3 sont circulaires
`test_arithmetic_generator_*` fabriquent des exponentielles exactes e^{((β−½)+iγ)t} avec (β,γ) **injectés**, puis les « retrouvent » : l'écart 10⁻¹³ mesure l'arithmétique flottante, pas
l'arithmétique des nombres premiers. De plus le document le dit lui-même (§4) : pour H diagonalisable, ∃M>0 avec H*M=MH **⇔ spectre réel**. Le certificat « métrique positive » n'apporte donc
aucune information au-delà de Im λ = 0, c'est-à-dire au-delà de β = ½ lu sur les valeurs propres. Test ajouté : `test_metric_certificate_is_equivalent_to_real_spectrum`.

## F2. Sur le vrai signal de ζ, Re λ est biaisé (`scripts/run_generator_real_signal.py`, `data/generator_real_signal.csv`)
Signal y(t) = e^{−t/2}(ψ(eᵗ) − eᵗ + log 2π) pour X ≤ 4·10⁶, estimateur ESPRIT/Hankel (version la plus favorable de A → H_eff : troncature SVD).

| γ (zéro) | Im estimé | Re λ estimé (vrai : 0) |
|---|---|---|
| 14,135 | 14,1342 | −0,0024 |
| 21,022 | 21,0205 | −0,0233 |
| 25,011 | 24,983 | −0,0297 |
| 32,935 | 32,9348 | −0,0101 |
| 47,93 | 47,93 | −0,0900 |
| 60,6 | 60,61 | −0,0931 |
| 67,3 (ordre 28) | 67,27 | **−5,79** (fantôme) |

La fréquence est retrouvée à 10⁻³ pour les premiers zéros, mais Re λ est **systématiquement négatif** (perte apparente) et du même ordre que ce qu'on voudrait détecter (|β−½| ≲ 0,1).
Le pipeline classerait des zéros critiques comme « avec perte ». Comme RH est vérifiée jusqu'à une hauteur ≈ 3·10¹² (valeur citée de mémoire), un zéro hors ligne éventuel est loin hors de portée.

## F3. Témoin Davenport–Heilbronn : détecte, mais avec un faux positif
Même pipeline sur y(t) = e^{−t/2}Σ_{n≤eᵗ}Λ_f(n) (X ≤ 3·10⁵). Le zéro hors ligne connu 0,8085 + 85,699i (β−½ = +0,3085) apparaît à Im = 85,67 avec Re = +0,23–0,24 (sous-estimé de 25 %).
**Mais** le mode de plus grande partie réelle est à Im ≈ 73,80, Re = **+0,345** (stable pour r = 12 à 40), alors que la fonction DH n'a là qu'un zéro **sur** la droite (74,325) : balayage de |f| sur une grille
et Newton ne trouvent aucun zéro près de 0,84 + 73,8i. C'est un artefact de fuite spectrale du mode dominant. Un pipeline qui désigne le mauvais mode comme « le plus hors ligne » ne passe pas le test de rejet
de la section 7 du document V4.3 (il passerait un test naïf « une valeur propre complexe persiste »). Test d'archive : `test_generator_dh_ghost_mode_in_data`.

## F4. Blocs de Jordan : le signal d'ordre 2 est exclu, et le garde-fou est trop faible
Le signal de G (double pôle) est Σ(A t + u)e^{iγt} : le propagateur est **défectif** (bloc de Jordan par zéro). Aucune métrique M>0 ne rend un bloc de Jordan auto-adjoint, **même sous RH** ; la branche n'a donc de sens que pour le
signal d'ordre 1 (type ψ) et des zéros **simples** (un zéro multiple est aussi un bloc de Jordan). Numériquement, le garde-fou `cond(V) ≤ 10¹²` accepte un bloc de Jordan (cond V = 1,7·10⁶) et construit une métrique
de conditionnement 2,8·10¹² : la coercivité uniforme exigée au §9 du document échoue sans que le code le dise. Correctif v4.4 : paramètre `metric_cond_max` dans `spectral_metric` (défaut inchangé pour compatibilité). Test : `test_second_order_signal_is_jordan_block`.

## F5. Dictionnaire de Schrödinger : reparamétrisation, pas mécanisme
E_ρ = −γ + i(β−½) est une réécriture de λ = (β−½) + iγ. « RH ⇔ Im E = 0 » est la phrase « β = ½ » dans une autre variable. L'équation de continuité avec potentiel complexe (d‖ψ‖²/dt = (2/ħ)∫Im V|ψ|²)
est correcte et standard, mais le potentiel n'est pas dérivé de l'arithmétique : **GAP-SCHR et GAP-SCHR-GEN sont exactement le problème de Hilbert–Pólya** (opérateur canonique, auto-adjoint, de spectre {γ}), dont la
difficulté n'est pas changée par la métrique M. Les trois exigences du §9 (positivité, uniformité, exactitude spectrale) sont celles de ce programme depuis son origine.

## F6. Hygiène éditoriale
- Les « simulations de referee » A/B/C sont internes : elles ne remplacent pas une relecture indépendante des théorèmes A et B (le résumé le dit déjà).
- Les entrées de changelog V4.1–V4.3 existent (vérifié) ; l'ancienne entrée « canaux terminaux » du changelog cite encore la forme longue de H_∞ (équivalente à la forme courte).
- La liste « [LU EN ENTIER] » des sources ne couvre que Bettin–Conrey–Farmer ; les autres références sont lues sur page/abstract.

## Décision
La règle d'arrêt P2 de la v3.7 s'applique aux branches V4.1–V4.3 : elles sont conservées comme **diagnostics** (avec les réserves F1–F5), non comme voies d'attaque. Priorités : (1) relecture externe de A et B ;
(2) recherche de priorité ; (3) rédaction d'une note courte A/B/C + résultats négatifs, en y ajoutant la section « limites d'identification de modes sur le signal des premiers » (F2–F3).
