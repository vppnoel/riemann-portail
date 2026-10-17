# V6 — DARK-ZETA : premier détecteur construit et testé

**Date :** 5 octobre 2026  
**Statut :** expérience reproductible intégrée — résultat négatif partiel, diagnostic utile  
**Aucune revendication de lien nouveau avec RH.**

---

## 1. Question testée

Le cadre DARK-ZETA pose une question d'observabilité : à quel niveau une information arithmétique distinctive, perdue par une énergie scalaire, réapparaît-elle ?

Le premier détecteur a été construit autour du signal déjà présent dans le programme,

\[
C_F(t)=\sum_{n\le t}c_F(n),
\qquad
 g_F(u)=e^{-u/2}C_F(e^u),\quad u=\log t,
\]

où \(c_F\) est obtenu par le pipeline logarithmique générique de `src/rejection.py`.

On compare quatre niveaux :

1. **défaut multiplicatif coefficientiel** \(\Delta_F(m,n)\) — étalon explicite ;
2. **TOMO-2** — matrice de Gram des translations logarithmiques, donc spectre de puissance ;
3. **TOMO-3** — bicoherence segmentée, donc fermeture de phase quadratique ;
4. témoins adversariaux : \(\zeta\), \(L(s,\chi_5)\), Davenport–Heilbronn [DH36b] [DH36a], phases randomisées et suites complètement multiplicatives aléatoires.

La fonction de Davenport–Heilbronn est utilisée parce qu'elle possède une équation fonctionnelle de type Riemann mais pas de produit d'Euler, tandis que les coefficients des Dirichlet \(L\)-fonctions sont multiplicatifs. Le produit d'Euler de \(\zeta\) est l'expression analytique classique de cette multiplicativité.

---

# 2. Construction exacte

## 2.1 Étalon : défaut multiplicatif

Pour

\[
F(s)=\sum_{n\ge1}a_F(n)n^{-s},\qquad a_F(1)=1,
\]

on définit

\[
\Delta_F(m,n)=a_F(mn)-a_F(m)a_F(n),\qquad (m,n)=1.
\]

L'indicateur numérique utilisé est

\[
\mathcal D_F(P)=
\frac{\sum_{m,n\le P,(m,n)=1}|\Delta_F(m,n)|^2}
{\sum_{m,n\le P,(m,n)=1}
\left(|a_F(mn)|^2+|a_F(m)a_F(n)|^2\right)}.
\]

Il vaut zéro, à l'arrondi près, pour \(\zeta\), \(L(s,\chi_5)\) et les témoins synthétiques complètement multiplicatifs ; il est non nul pour Davenport–Heilbronn.

## 2.2 TOMO-2

Sur le signal centré et normalisé \(g_F\), on forme une matrice de Gram de translations circulaires :

\[
K^{(2)}_{ij}=\langle T_{\tau_i}g_F,T_{\tau_j}g_F\rangle.
\]

Le choix circulaire sert de contrôle interne : \(K^{(2)}\) dépend exactement du spectre de puissance discret et doit donc être invariant sous randomisation de la phase de Fourier.

Observable principal : entropie spectrale normalisée des valeurs propres de \(K^{(2)}\).

## 2.3 TOMO-3

Le signal est découpé en segments chevauchants. Pour chaque segment, on calcule la transformée de Fourier \(X_r(k)\), puis la bicoherence quadratique

\[
b^2(k,l)=
\frac{\left|\mathbb E_r[X_r(k)X_r(l)\overline{X_r(k+l)}]\right|^2}
{\mathbb E_r|X_r(k)X_r(l)|^2\;\mathbb E_r|X_r(k+l)|^2}.
\]

La bicoherence est précisément conçue pour détecter une relation de phase entre \(f_1\), \(f_2\) et \(f_1+f_2\). Elle constitue donc le premier test du « principe de fermeture multiplicative » proposé dans TOMO-DH.

---

# 3. Paramètres du premier run

- troncature arithmétique : \(N=32768\) ;
- grille logarithmique : 4096 points ;
- défaut multiplicatif : \(P=48\) ;
- TOMO-2 : 32 translations, pas 8 ;
- TOMO-3 : segments 512, recouvrement 50 %, 24 premiers bins positifs ;
- 32 surrogats à phases randomisées pour chaque objet principal ;
- 4 témoins Steinhaus complètement multiplicatifs ;
- trajectoire synthétique \(\chi_5\to DH\) en 11 valeurs de \(\theta\).

Tous ces paramètres sont enregistrés dans `data/dark_zeta_protocol.json`.

---

# 4. Résultats principaux

## 4.1 Le contrôle TOMO-2 passe exactement

Après randomisation des phases de Fourier tout en conservant leur module,

\[
\max_{ij}|K^{(2)}_{ij}(g)-K^{(2)}_{ij}(g_{\rm rand})|
<10^{-15}
\]

pour \(\zeta\), \(L(s,\chi_5)\) et Davenport–Heilbronn.

**Interprétation :** le code confirme la prédiction analytique. TOMO-2 ne voit aucune phase cachée ; il mesure uniquement une structure de puissance/covariance.

## 4.2 TOMO-2 voit quelque chose sur la trajectoire appariée \(\chi_5\to DH\)

Sur la famille synthétique

\[
a_\theta=(1-\theta)\chi_5+\theta a_{DH},\qquad 0\le\theta\le1,
\]

l'entropie TOMO-2 croît fortement avec le défaut multiplicatif.

À \(N=32768\) :

\[
\rho_{\rm Spearman}=0.9636,
\qquad p\approx2\times10^{-6}.
\]

Le phénomène reste visible aux trois échelles testées :

| \(N\) | Spearman \(\mathcal D\) vs entropie TOMO-2 |
|---:|---:|
| 8192 | 0.8818 |
| 16384 | 0.9636 |
| 32768 | 0.9636 |

**Mais ce n'est pas un détecteur universel de multiplicativité.** Les témoins Steinhaus ont un défaut multiplicatif nul à l'arrondi, tout en ayant des entropies TOMO-2 très différentes de \(\zeta\) ou \(L(s,\chi_5)\). Le lien observé est donc **conditionnel à cette famille appariée**, pas une loi générale.

## 4.3 TOMO-3 ne confirme pas le pont multiplicativité ↔ fermeture de phase

À \(N=32768\), la corrélation entre défaut multiplicatif et bicoherence moyenne sur la trajectoire \(\chi_5\to DH\) est

\[
\rho_{\rm Spearman}=0,
\qquad p=1.
\]

Pour le quantile 90 %, on obtient seulement

\[
\rho_{\rm Spearman}\simeq0.109,
\qquad p\simeq0.75.
\]

Plus important : la corrélation TOMO-3 est **instable avec l'échelle** :

| \(N\) | Spearman \(\mathcal D\) vs bicoherence moyenne |
|---:|---:|
| 8192 | -0.400 |
| 16384 | +0.709 |
| 32768 | 0.000 |

Cette inversion de comportement interdit d'interpréter le run intermédiaire positif comme une loi.

## 4.4 Calibration par phases randomisées

La bicoherence au nombre fini de segments possède un plancher statistique non nul. On a donc comparé chaque observation à 32 surrogats conservant **exactement** le spectre de puissance mais randomisant la phase.

Pour la bicoherence moyenne :

| Objet | observé | moyenne surrogats | z-score |
|---|---:|---:|---:|
| \(\zeta\) | 0.0533 | 0.0626 | -1.65 |
| \(L(s,\chi_5)\) | 0.0745 | 0.0743 | +0.01 |
| DH | 0.0796 | 0.0701 | +1.59 |

Aucun de ces écarts n'est suffisamment net pour soutenir une signature TOMO-3. Les autres résumés (médiane, q90, maximum) conduisent au même diagnostic global : **pas de séparation robuste à ce stade**.

---

# 5. Verdict scientifique

Le premier détecteur DARK-ZETA produit un résultat mixte mais utile.

### Ce qui survit

- la séparation conceptuelle TOMO-2 / TOMO-3 est correcte et validée numériquement ;
- TOMO-2 contient davantage d'information que le scalaire \(Q\) et distingue nettement la trajectoire appariée \(L_\chi\to DH\) ;
- l'idée de « cartographier une information perdue » reste opérationnelle.

### Ce qui est falsifié dans sa forme naïve

Le pont proposé

\[
\text{multiplicativité}
\Longrightarrow
\text{fermeture de phase bispectrale de }C_F
\]

**n'est pas soutenu par le premier protocole.**

TOMO-3, appliquée directement au signal \(C_F\), se comporte essentiellement comme une statistique au voisinage de son nul de phase randomisée et ne suit pas de façon stable le défaut multiplicatif.

### Conséquence méthodologique

Il ne faut pas monter automatiquement à TOMO-4 ou TOMO-5. Ce serait reproduire l'ancien réflexe « ajouter de la complexité jusqu'à voir quelque chose ».

La bonne question devient plus précise :

> **Quelle représentation du signal rend la loi multiplicative visible avant la réduction spectrale ?**

Autrement dit, le problème peut être moins « ordre statistique insuffisant » que **mauvais canal d'observation**.

---

# 6. Statut des sous-branches

| Sous-branche | Statut après premier détecteur |
|---|---|
| Défaut multiplicatif \(\mathcal D_F\) | **CALIBRATION EXACTE** — tautologique mais indispensable |
| TOMO-2 Gram / spectre de puissance | **SURVIT COMME DIAGNOSTIC** |
| TOMO-2 = détecteur universel de multiplicativité | **RÉFUTÉ** par témoins Steinhaus |
| TOMO-3 bispectre de \(C_F\) | **RÉTROGRADÉ** |
| « fermeture multiplicative » dans le bispectre brut | **NON OBSERVÉE** |
| DARK-ZETA multi-observable | **OUVERT** — le premier capteur n'a pas trouvé l'information recherchée |

---

# 7. Prochaine cible recommandée

Ne pas chercher immédiatement un polyspectre d'ordre supérieur.

La prochaine expérience doit modifier le **canal**, pas seulement l'ordre : construire des canaux explicitement résolus par structure arithmétique (premiers, puissances de premiers, défaut local de convolution, canaux de log-dérivée), puis tester des **cross-bispectres** entre ces canaux et \(C_F\).

Nom de travail proposé :

> **PRIME-LOCK — verrouillage inter-canaux premiers / signal global**.

Une telle expérience aurait une chance de tester une interaction réelle entre multiplicativité locale et observable global sans réduire immédiatement l'information à un seul signal agrégé.

---

# 8. Fichiers reproductibles

### Code
- `src/dark_zeta.py`
- `scripts/run_dark_zeta.py`
- `tests/test_dark_zeta.py`

### Données
- `data/dark_zeta_detector_summary.csv`
- `data/dark_zeta_phase_random_controls.csv`
- `data/dark_zeta_tomo3_surrogate_calibration.csv`
- `data/dark_zeta_chi_dh_scan.csv`
- `data/dark_zeta_scaling_scan.csv`
- `data/dark_zeta_scaling_correlations.csv`
- `data/dark_zeta_steinhaus_controls.csv`
- `data/dark_zeta_tomo3_triads_zeta.csv`
- `data/dark_zeta_tomo3_triads_L_chi5.csv`
- `data/dark_zeta_tomo3_triads_DH.csv`
- `data/dark_zeta_protocol.json`

### Figures
- `data/dark_zeta_tomo2_defect_scan.png`
- `data/dark_zeta_tomo3_defect_scan.png`
- `data/dark_zeta_tomo3_surrogate_calibration.png`

---

# 9. Références de cadrage

- NIST DLMF, §27.4, *Euler Products and Dirichlet Series* : multiplicativité et produits d'Euler ; produit d'Euler de \(\zeta\). https://dlmf.nist [OLBC10].gov/27.4
- NIST DLMF, §25.2(iv), produit d'Euler de la fonction zêta. https://dlmf.nist.gov/25.2
- Description classique de la fonction de Davenport–Heilbronn comme combinaison de deux fonctions \(L\) modulo 5, avec équation fonctionnelle de type Riemann mais sans structure d'Euler correspondante : voir le document de synthèse Kyoto cité dans la bibliographie interne et `DAVENPORT_HEILBRONN_TEST.md`.
- La bicoherence mesure le couplage de phase quadratique entre \(f_1\), \(f_2\) et \(f_1+f_2\) ; voir par exemple les revues en accès libre indexées dans PMC (notamment PMC6751382 et PMC3287025).

---

## Conclusion

Le premier détecteur ne trouve pas encore le « secteur sombre » recherché. C'est précisément son intérêt.

Il montre que :

\[
\boxed{
\text{plus de structure spectrale} \neq
\text{automatiquement plus d'information arithmétique}
}
\]

et que la fermeture de phase d'ordre 3 du signal agrégé \(C_F\) n'est pas, dans ce protocole, le bon capteur de la multiplicativité.

La V6 obtient donc son premier résultat conforme à sa nouvelle méthode : **une hypothèse précise a été construite, instrumentée, testée, puis partiellement rejetée sans déplacer les poteaux.**

---

## Mise à jour V6.3d

Le résultat nul de TOMO-3 et la séparation L / DH de TOMO-2 sont expliqués dans `24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md` : le signal est une somme de tons aux ordonnées des zéros ; l'excès d'entropie de DH est porté par ses zéros hors droite ; une statistique d'ordre 2 sur les zéros (différences de zéros sondées aux zéros de ζ) répond à la question du §7.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [OLBC10] F. W. J. Olver, D. W. Lozier, R. F. Boisvert, C. W. Clark (éd.). *NIST Digital Library of Mathematical Functions, ch. 25 (Zeta and related functions)*. NIST, version en ligne (2010). <https://dlmf.nist.gov/25> — vérifié en ligne

<!-- references:fin -->
