# Test Davenport–Heilbronn — protocole et premiers résultats (v3.2)

## Définition exécutable
f(s) = ½(1−iκ)L(s,χ) + ½(1+iκ)L(s,χ̄), χ mod 5 avec χ(2)=i (impair), 
κ = (√(10−2√5) − 2)/(√5 − 1) ≈ 0,28408. Équation fonctionnelle vérifiée numériquement :
\|Λ(s) − Λ(1−s)\|/\|Λ(s)\| < 10⁻¹⁶ en trois points (test `test_dh_functional_equation`).

## Pipeline générique (src/rejection.py)
Λ_f défini par f·Λ_f = a·log (donc −f'/f = ΣΛ_f n^{-s}), c_f = Λ_f*Λ_f − Λ_f log
(+ 2γΛ_f pour ζ seulement, à cause du pôle). Contrôle : pour ζ, le pipeline retrouve
Λ et c à 10⁻¹³ près.

## Résultats (N = 3·10⁵, `data/rejection_growth.csv`)
| Objet | Euler | pente log Q/log X (dernière décade) | densité du support de c | max \|c\| |
|---|---|---|---|---|
| ζ | oui | 0,326 | 0,40 | 144 |
| L(s,χ₅) | oui | 0,338 | 0,37 | 159 |
| DH | **non** | **0,563** | 0,71 | 23 249 |

Zéros de DH trouvés par Newton (`data/dh_zeros.csv`, t ≤ 200 : **125 trouvés pour ≈ 129,5 attendus** par la formule asymptotique,
écart ≈ 4,5 compatible avec son terme d'erreur O(log T) ; deux balayages plus fins n'ont presque rien ajouté) : hors droite critique, 0,8085+85,699i ; 0,6508+114,163i ;
0,4256 et 0,5744 + 166,479i (paire symétrique) ; 0,7243+176,703i. Le plus à droite est
σ = 0,8085, soit une pente prédite 2σ−1 ≈ 0,617 pour Q, comparable à la pente mesurée 0,563.
**Aucun zéro avec σ > 1 n'a été trouvé jusqu'à t = 200** (je m'attendais à en voir ; ce
n'est pas exclu au-delà ou parmi les zéros manquants).

**Correction V6.3d (2026-10-07).** La liste ci-dessus était incomplète de six zéros : les quatre partenaires 1 − σ des zéros hors droite (V6.3b) et deux zéros bas, t = 5,0942 et t = 8,9399 (la recherche partait de t = 10). L'écart 125/129,5 n'était donc pas dû au terme d'erreur. Comptage exact par le principe de l'argument : 130 zéros pour 0 < t ≤ 200,5 ; 494 pour 0 < t ≤ 600, dont 15 paires hors droite, partie réelle maximale 0,8695, aucune au-delà de 1 (`data/dh_zeros_600.csv`, `data/zeros_600_count_audit.csv`).

## Lecture
- **Couche générique confirmée** : Q détecte les zéros hors droite, y compris dans DH
  (pente 0,56 contre ≈ 0,33 pour les deux fonctions d'Euler). Ceci ne prouve rien sur RH.
- **Ce qui distingue ζ/L de DH dans l'observable** : la parcimonie de c (≤ 2 premiers distincts)
  n'est qu'à moitié visible ici (densité 0,40 et 0,37 contre 0,71) car la densité du support
  décroît lentement avec N ; la distinction nette reste un fait structurel (L3), pas numérique.
- **Test de rejet** : toute future inégalité doit citer l'étape qui utilise Λ, μ, la parcimonie
  de c ou les canaux H_∞ de façon irréversible ; si elle fonctionne mot pour mot pour DH, elle est rejetée.

## Statut
Protocole exécutable ; aucune inégalité candidate n'a encore été soumise au test (GAP-4 reste ouvert).
