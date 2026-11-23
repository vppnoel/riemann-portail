# TAC-006 — Pli sur une fibre à coefficient A fixé

*Producteur : ia:claude (Claude Opus 5.5) · 18 octobre 2026 · branche `tac-006` · Programme Riemann V6.59. Auteur et titulaire des droits : Vincent NOËL.*

**En une phrase.** Sur la fibre exacte à A = cos(π/6)·z₁ (ancre χ₁, rayon π/6) de la famille V13, un grand cercle de la fibre porte un pli transversal certifié près de la hauteur 5 :
- d'un côté, deux zéros critiques ;
- au pli, un zéro exactement double ;
- de l'autre côté, une paire hors de la droite.

C'est le passage local que le document 66 n'avait obtenu qu'en faisant varier le rayon, donc avec A variable.

**Révision du 18 octobre** (revue de ChatGPT, PR #19, fil #13). Les quatre corrections demandées sont faites. Aucun objet, chemin, boîte ni critère n'a changé ; le lanceur a été rejoué en entier.
- **C1. Comparaison de Rouché.** Elle utilisait la borne basse de `magnitude()`, qui majore le module sur un rectangle ; ce n'est pas en général un minorant. Elle est remplacée par un vrai minorant, lower(√(Re α² + Im α²))·R². Les bornes sont exportées en fractions exactes, et la relecture vérifie par carrés rationnels que comparaison² ≤ |α|²R⁴. Le résultat est inchangé à la 12ᵉ décimale.
- **C2. Portée de P2.** Le calcul couvre maintenant tout λ ∈ [boîte de λ* ± 10⁻⁴] et **tout** centre du cercle dans la boîte certifiée de t*, et non plus seulement λ_c ± 10⁻⁴ autour d'un centre arrondi. L'énoncé vaut donc pour le pli exact, comme le disait la prévision.
- **C3. Décimales.** Les tableaux sont refaits depuis les bornes binaires exactes, avec arrondi vers l'extérieur. La marge s'écrit « ≥ 0,025537 », et non plus « ≥ 0,025538 », qui n'était pas établi.
- **C4. Encodage.** La marque UTF-8 a été ajoutée au rapport.

## Prévision

Elle a été enregistrée avant toute évaluation de fonction L, le **18 octobre 2026 à 00:11:24 UTC** (`taches.py prevoir`, commit `9e2ece7` sur `main`). Les calculs ont commencé ensuite : premier essai vers 00:13 UTC, troisième essai de 00:18 à 00:19 UTC.

**Objet.** Il est fixé par la prévision :
- V13 impaire modulo 13, ancre k = 1, r = π/6 ;
- A = cos(π/6)·z₁, centre de l'ellipse (η = 0) ;
- premier des quatre candidats de jets V6.41 : hauteur 5, premier vecteur de `v641_geometrie.json`.

La règle de sélection est la plus petite hauteur, premier membre. Les recours n'ont pas servi.

**Chemin.** Un grand cercle exact de la fibre :

c(λ) = cos r·e₁ + sin r·(cos λ·p + sin λ·q)

Ici p est voisin du candidat, et q est la direction de plus forte pente de Z(5) dans ker M₁ ∩ p^⊥.

| Prévision | Énoncé enregistré | Verdict |
|---|---|---|
| P1 | Un zéro double unique (λ*, t*) est certifié aux plans 50 et 80 décimales, avec \|λ*\| < 10⁻⁶, \|t* − 5\| < 10⁻⁶, et Z_λ, Z_tt séparés de zéro. | **Juste** |
| P2 | Rouché uniforme sur \|w − w*\| = 1/5 pour λ ∈ [λ* − 10⁻⁴, λ* + 10⁻⁴]. | **Juste**, au premier essai : 256 arcs, rayon 1/5. Depuis la révision, cela couvre toute la boîte du pli (λ*, t*). |
| P3 | En λ_c ± 10⁻⁴ : deux zéros critiques d'un côté, une paire hors droite de l'autre, du côté donné par le signe de κ = −2Z_λ/Z_tt. | **Juste** |
| P4 | Témoin négatif : le long de la direction tangente orthogonale à q, le même certificat, avec les mêmes largeurs de boîtes, est refusé. | **Juste** : refusé |

## Méthode

On a repris le moteur certifié du document 66 (`3_Preuves_et_calculs/src/v642_intervalles.py`), que le dépôt importe en lecture seule. On l'a étendu des deux composantes de la famille radiale aux six composantes B_j(s) = z_j·L(s, χ_j), pour k = 1, 3, …, 11.

**Pièces mathématiques réemployées (document 66).**
- **Lemme I1.** Euler–Maclaurin, avec reste borné analytiquement par la série de Fourier des Bernoulli, puis estimation de Cauchy pour les dérivées d'ordre ≤ 2. Ici le reste est ajouté bloc de Hurwitz par bloc, ce qui donne un majorant plus large que nécessaire, mais valide.
- **Lemme I2.** La projection réelle fixe H = Re[ωF] = h(t)·Z préserve le pli dès que la projection d'une composante (l'ancre) est séparée de zéro. Ici ω = 1, le premier choix ; le recours ω = i n'a pas servi.
- **Théorème I3.** Inclusion stricte et contraction donnent existence et unicité :
  - pour le système (H, H_t) en (λ, t), qui fournit le pli ;
  - pour F en s, qui fournit les racines.
- **Lemme I4.** Rouché sur 256 arcs, avec reste de Taylor d'ordre 2. Il est uniforme pour tout λ de l'intervalle.
- **Lemme I5.** Symétrie s ↦ 1 − s̄ et unicité : une boîte centrée sur Re s = 1/2 donne un zéro critique ; une boîte qui exclut la droite donne un zéro hors droite.

**Ce qui est nouveau : rester exactement sur la fibre.**
- On fixe une fois pour toutes des coefficients **rationnels** (`a_libre`, `b_libre`, `n_libre` dans `resultats_tac006.json`). On les combine à des vecteurs **exacts** de ker M₁, obtenus par élimination sur un mineur pivot 2×2 dont l'encadrement est −0,99925… et exclut donc 0.
- Gram–Schmidt exact donne alors p, q et n.
- Pour tout λ, ancre, rayon, norme et A sont conservés **exactement**, et pas seulement aux erreurs d'arrondi près. Les encadrements des résidus Σ p_j z_j et Σ q_j z_j sont de l'ordre de 5·10⁻⁴⁸ : ce sont des enclosures de zéro, pas des approximations.
- Le pli certifié est donc un pli **à A constant**.

**Contrôles préalables, non certifiants.**
- Les six B_j(1/2 + 5i) ont la même phase : Im(B_j·conj B₁) est d'environ 10⁻³². C'est cohérent avec Z_c réelle sur la droite critique, que le corpus démontre au document 66, lemme I2, et dans `LEMME_CONTRAINTES_V13_V639.md`.
- Les jets d'ordre 0 à 2 de χ₁ et χ₃ recoupent la formule de Hurwitz de mpmath (`zeta(s, a, derivative=m)`) à moins de 1,5·10⁻³¹, contre une largeur certifiée d'environ 3·10⁻²⁸.

**Plans.**
- Pli : 50 décimales (N = 32, M = 12) et 80 décimales (N = 48, M = 12), comme au document 66.
- Rouché et racines : plan 50.
- Demi-largeurs fixées dans le code avant le premier essai et inchangées : 10⁻¹² pour le pli, 10⁻⁹ pour les racines.

**Relecture.** `verifier_tac006.py` reconstruit en fractions les bornes binaires exportées et recontrôle sans opération d'intervalles :
- les inclusions et les séparations ;
- la symétrie ou l'exclusion de la droite ;
- la disjonction des boîtes et leur appartenance au disque de Rouché.

Résultat : **41 contrôles sur 41**. La révision ajoute le minorant de Rouché par carrés rationnels, les décimales extérieures et la couverture de la boîte du pli. Comme au document 66, cette relecture ne réévalue pas les primitives transcendantes.

**Écarts de déroulement, tous conservés dans `journaux/`.**
- **Essai 1.** Arrêt au plan 80 : Newton arrondissait à 10⁻⁴⁵ pour une tolérance de 10⁻⁶⁰.
- **Essai 2.** Arrêt aux racines : `iv.mpc(mpc)` échoue en mpmath 1.3.0, le défaut de constructeur de copie déjà signalé au document 66.

Ces deux corrections touchent le code seulement. Ni l'objet, ni le chemin, ni les boîtes, ni les critères n'ont changé. Les lignes de pli et de Rouché des essais 1 et 2 sont identiques octet pour octet à celles de l'essai 3. Seule exception : dans l'essai 1, la contraction était affichée comme une fraction tronquée, défaut d'affichage corrigé en même temps.

**Environnement.**
- Python 3.13.16.
- mpmath **1.3.0**, installé depuis le dépôt GitHub `mpmath/mpmath` au tag 1.3.0, commit `b5c04506ef0c` : PyPI était inaccessible dans cette session.
- NumPy n'est pas utilisé par le certificat.
- Aucun zéro de fonction L n'est injecté. Les seules entrées sont :
  - les phases exactes de Gauss ;
  - le vecteur candidat V6.41, qui sert de point de départ ;
  - la hauteur 5, prescrite par la section de jets V6.41.

## Résultat

Tous les chiffres sont dans `resultats_tac006.json`. Les encadrements sont certifiés au sens du théorème I3. Les décimales affichées sont arrondies vers l'extérieur depuis les bornes binaires exactes ; les valeurs précédées de « ≈ » sont seulement indicatives.

**Le pli à A constant.** Au plan 50 :

| Grandeur | Encadrement certifié |
|---|---|
| λ* | [−1,7823491352·10⁻¹⁵ ; −1,7823463531·10⁻¹⁵] |
| t* | [5,000000000160760864543 ; 5,000000000160760864555] |
| H_λ sur la boîte | [1,0541015542 ; 1,0541015546] : transversalité sur la fibre |
| H_tt sur la boîte | [−1,5073855828 ; −1,5073855689] : zéro **exactement** double |
| κ = −2H_λ/H_tt | [1,39858250 ; 1,39858253] |
| Projection d'ancre Re B₁ | ≈ 0,39338, séparée de zéro (lemme I2) |
| Contraction | q ≤ 5,72·10⁻⁹ |

Au plan 80, la même boîte est acceptée avec q ≤ 8,85·10⁻⁹ et des encadrements compatibles.

Le pli se trouve à λ* ≈ −1,8·10⁻¹⁵ du point p construit depuis le candidat. Le candidat V6.41, calculé avec des jets par différences finies sans borne d'erreur, était donc correct à cette échelle. La hauteur certifiée diffère de la hauteur prescrite de 1,6·10⁻¹⁰.

**Le compte : Rouché.**
- Cercle |w − w₀| = 1/5, sur 256 arcs. Il est uniforme pour **tout** centre w₀ dans la boîte certifiée de t* (demi-largeur 10⁻¹²), donc en particulier pour w₀ = t*.
- Il est aussi uniforme pour tout λ ∈ [λ_c − 10⁻¹² − 10⁻⁴ ; λ_c + 10⁻¹² + 10⁻⁴], intervalle qui contient [λ* − 10⁻⁴ ; λ* + 10⁻⁴]. Les valeurs, en fractions exactes dans le JSON et en décimales extérieures ici :
  - comparaison ≥ 0,036442232171 ;
  - défaut ≤ 0,010904606249 ;
  - **marge ≥ 0,025537625922**.
- F_{c(λ)} a donc exactement deux zéros dans le disque, avec multiplicité, pour tout λ de l'intervalle.
- La vérification indépendante de ChatGPT (PR #19) obtient de son côté une marge supérieure à 0,02553739, par un calcul séparé.

**Les quatre racines.**

| Paramètre | Re(s) | Im(s) | Nature |
|---|---|---|---|
| λ_c − 10⁻⁴ | [0,5118260099034 ; 0,5118260099041] | ≈ 4,9999937229 | hors droite |
| λ_c − 10⁻⁴ | [0,4881739900958 ; 0,4881739900966] | ≈ 4,9999937229 | hors droite, partenaire symétrique |
| λ_c + 10⁻⁴ | 1/2 exactement (symétrie et unicité) | [5,011832603188 ; 5,011832603189] | critique |
| λ_c + 10⁻⁴ | 1/2 exactement | [4,988179950717 ; 4,988179950719] | critique |

Les contractions valent toutes moins de 4·10⁻⁴. Les boîtes sont disjointes et contenues dans le disque. Avec le compte de Rouché égal à 2, elles identifient **toute** la paire locale.

Le côté critique est celui où κ·(λ − λ*) > 0, comme annoncé. L'écart observé, 0,01183, est celui du modèle quadratique, √(κ·10⁻⁴) ≈ 0,01183.

**Le témoin négatif (P4).** On reprend le même système le long de la direction tangente n, orthogonale à q dans la fibre :
- au pli, H_λ le long de n vaut 4,3·10⁻¹¹, contre 1,054 le long de q ;
- Newton ne converge pas ;
- le certificat, avec la même demi-largeur, est **refusé** : contraction ≈ 33,7, inclusion refusée, et H_λ ∈ [−1,0·10⁻¹⁰ ; 1,9·10⁻¹⁰] non séparé de zéro.

La méthode détecte donc, au bon endroit, la direction où la dérivée paramétrique s'annule. C'est le témoin « dérivée paramétrique nulle » de la fiche.

## Portée

**Établi.** Sous les hypothèses déclarées (backend iv de mpmath 1.3.0, primitives transcendantes non revalidées indépendamment) :
- dans la famille V13 impaire modulo 13, sur la fibre {ancre χ₁, r = π/6, A = cos(π/6)·z₁}, le grand cercle défini par (p, q) porte un pli transversal ;
- en λ* ≈ −1,8·10⁻¹⁵, la fonction F_{c(λ*)} a un zéro critique exactement double à t* ≈ 5,00000000016 ;
- pour λ un peu plus grand, deux zéros critiques ; pour λ un peu plus petit, une paire hors de la droite ;
- ces configurations sont certifiées aux paramètres λ_c ± 10⁻⁴, avec un compte exact dans le disque pour tout λ ∈ [λ* − 10⁻⁴ ; λ* + 10⁻⁴] et tout centre du cercle dans la boîte de t*.

Le document 66 notait que *« le déploiement sur une fibre à A constant reste une expérience distincte »*. C'est cette expérience-là, réalisée et certifiée.

**Non établi.**
- Rien sur les autres candidats, les autres fibres, les autres hauteurs ou le premier zéro global.
- Rien sur l'exhaustivité des plis.
- Rien sur la loi globale de Weil, ni sur Q(X).
- La fiche l'annonçait : *cette branche ne garantit pas la loi globale de Weil*.

**Contrôles anti-circularité.**
- **Davenport–Heilbronn.** L'argument n'utilise que l'équation fonctionnelle commune des six caractères, l'analyticité et des bornes explicites. Il s'applique **mot pour mot** à toute combinaison de type DH. Le résultat le montre lui-même : pour λ < λ*, F_{c(λ)} a des zéros hors de la droite. **Ce certificat ne peut donc pas servir pour RH**, et il ne le prétend pas. Il localise un mécanisme : le passage par un zéro double est exactement la porte par laquelle des zéros quittent la droite dans une famille sans produit d'Euler.
- **Corps de fonctions.** Pas d'analogue pertinent : une famille linéaire de fonctions L, à coefficients non multiplicatifs, n'a pas de RH à comparer. On ne revendique aucune positivité.
- **Aucune donnée injectée.** Le candidat V6.41 fournit un point de départ, pas la réponse. Le pli est relocalisé et certifié indépendamment ; sa distance au départ est mesurée, pas présupposée.
- **Témoin négatif.** P4, refusé comme prévu.
- **Équivalence à RH.** Aucune.
- **Constantes.** Toutes sont données avec leur encadrement ou leur marge.

**Ce que cela change, à proposer à l'auteur.**
- **Graphe du document 66.** La flèche « jets nuls → zéro double exact » et la flèche « zéro double → pli d'une paire », pour une cible complexe fixée, peuvent passer de *candidat* à *certifié pour un cas*, celui-ci.
- **Fiches suivantes possibles.**
  1. Le second membre et les deux candidats à la hauteur 15 (ancre χ₃), avec le même code. Coût faible : environ une minute de calcul par cas.
  2. Une cible **hors du centre** de l'ellipse (η > 0), que V6.41 n'avait pas encore trouvée faisable. C'est elle qui montrerait que la géométrie des fibres étend réellement le domaine des collisions.

## Critère de rejet

Critère de la fiche, écrit avant : *un jet nul non certifié ne donne pas un zéro double ; préserver les pertes et les indéterminations.*

Il est respecté :
- le zéro double n'est pas déduit d'un jet nul : il est certifié par existence et unicité, avec H_tt ≠ 0 ;
- la direction indéterminée (n) est conservée comme témoin, et elle est refusée ;
- les deux essais interrompus sont conservés.

Témoins de la fiche :
- *fibre vide* : la fibre est intérieure, η = 0, avec un rayon de sphère égal à 1 ;
- *rang perdu* : le mineur pivot est séparé de zéro ;
- *dérivée paramétrique nulle* : présente le long de n, et détectée.

Ce qui aurait conduit à rejeter le résultat :
- H_λ ou H_tt non séparés ;
- inclusion ou contraction refusées aux deux plans ;
- Rouché refusé aux deux rayons ;
- témoin P4 accepté.

Aucun de ces cas ne s'est produit.

## Statut proposé

**demontre**, pour l'énoncé local de la section Portée : démonstration assistée par ordinateur, avec le backend iv de mpmath 1.3.0, que sa documentation qualifie d'expérimental. Ce n'est **pas** un énoncé équivalent à RH, et il n'apporte rien au signe global.

### Pièces

| Fichier | Rôle |
|---|---|
| `tac006_pli_fibre.py` | Moteur : jets validés des six composantes, chemin exact sur la fibre, pli, Rouché, racines |
| `run_tac006.py` | Lanceur, dans l'ordre de la prévision ; refuse d'écraser `resultats_tac006.json` |
| `resultats_tac006.json` | Toutes les sorties, avec les bornes binaires exactes |
| `verifier_tac006.py` | Relecture rationnelle, 41 contrôles |
| `journaux/essai1_arret_newton80.txt`, `journaux/essai2.txt` | Essais interrompus, conservés |
| `journaux/essai3.txt` | Essai complet |
| `journaux/verification_rationnelle.txt` | Sortie de la relecture |
| `journaux/essai4_revision.txt` | Rejeu complet après la révision du 18 octobre |

### Rejouer

Depuis la racine du dépôt, avec mpmath 1.3.0 dans le chemin Python :

```bash
cd 2_Methode/Depot/TAC-006
mv resultats_tac006.json /tmp/ref.json   # le lanceur refuse d'écraser
python -I run_tac006.py /chemin/vers/mpmath-1.3.0   # environ une minute
python -I verifier_tac006.py
```

Fil de discussion : https://github.com/vppnoel/Riemann/issues/13
