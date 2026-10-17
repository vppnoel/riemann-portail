# V6.2 — PRIME-LOCK : premier verrou local

**Date :** 5 octobre 2026  
**Statut :** détecteur construit, testé et intégré  
**Portée :** diagnostic de structure eulérienne ; **aucune revendication de lien nouveau avec RH**.

---

## 1. Pourquoi changer de canal

Le premier détecteur DARK-ZETA a montré une chose négative mais utile : augmenter l'ordre statistique du même signal agrégé ne suffit pas. TOMO-3, appliqué directement à \(C_F\), ne révèle pas de fermeture de phase robuste liée à la multiplicativité.

PRIME-LOCK change donc le **canal d'observation** plutôt que l'ordre statistique. On part de la dérivée logarithmique

\[
-\frac{F'}{F}(s)=\sum_{n\ge 1}\frac{\Lambda_F(n)}{n^s}.
\]

Pour un Euler-produit, le logarithme est une somme locale sur les nombres premiers. Sa dérivée logarithmique est donc supportée sur les **puissances de nombres premiers**.

Pour un facteur local de degré 1

\[
(1-\alpha_p p^{-s})^{-1},
\]

on a plus précisément

\[
\boxed{\Lambda_F(p^k)=\alpha_p^k\log p.}
\]

C'est cette rigidité locale qui devient le premier « verrou » de V6.

---

# 2. Trois canaux arithmétiques

On décompose \(\Lambda_F\) en trois canaux :

\[
\Lambda_F
=
\Lambda_F^{(p)}
+
\Lambda_F^{(p^k,k\ge2)}
+
\Lambda_F^{(\mathrm{leak})}.
\]

- **canal premiers** : \(n=p\) ;
- **canal puissances supérieures** : \(n=p^k,\ k\ge2\) ;
- **canal de fuite** : \(n\) n'est pas une puissance de premier.

Le premier observable est la fraction d'énergie coefficientielle hors puissances de premiers :

\[
\boxed{
L_F(N)=
\frac{\sum_{n\le N,\ n\ne p^k}|\Lambda_F(n)|^2}
{\sum_{2\le n\le N}|\Lambda_F(n)|^2}.
}
\]

Pour un Euler-produit exact, ce terme doit être nul, à l'erreur numérique près.

---

# 3. Verrou de tour de degré 1

Dans le sous-cadre zeta / Dirichlet \(L\) de degré 1, on définit

\[
\alpha_p=\frac{\Lambda_F(p)}{\log p}
\]

et le défaut local

\[
\delta_F(p,k)
=
\frac{\Lambda_F(p^k)}{\log p}-\alpha_p^k.
\]

La quantité normalisée utilisée est

\[
\boxed{
T_F(N)=
\frac{\sum_{p^k\le N,k\ge2}|\delta_F(p,k)|^2}
{\sum_{p^k\le N,k\ge2}
\left(
|\Lambda_F(p^k)/\log p|^2+|\alpha_p|^{2k}
\right)}.
}
\]

**Attention :** cette loi de tour est spécifique aux facteurs locaux de degré 1. Pour des fonctions \(L\) de degré supérieur, le support sur les puissances de premiers reste pertinent, mais la loi \(\alpha_p^k\) doit être remplacée par la structure locale correspondante.

---

# 4. Intervention contrôlée : « eulériser » un objet

Pour savoir si la structure locale perdue a réellement un effet sur le signal global, on construit une intervention artificielle.

On conserve les valeurs premières \(\Lambda_F(p)\), puis on impose

\[
\widehat\Lambda_F(p^k)
=
\left(\frac{\Lambda_F(p)}{\log p}\right)^k\log p,
\]

et

\[
\widehat\Lambda_F(n)=0
\qquad(n\ne p^k).
\]

C'est l'**eulérisation de degré 1** du canal logarithmique.

On reconstruit ensuite exactement le signal déjà utilisé dans le programme :

\[
c_F=\Lambda_F*\Lambda_F-\Lambda_F\log n
\]

(avec le terme archimédien déjà prévu pour \(\zeta\)), et son analogue \(\widehat c_F\).

Deux observables mesurent la propagation du défaut local :

\[
R_Q=\frac{Q(c_F-\widehat c_F)}{Q(c_F)},
\]

et la cohérence entre les deux signaux logarithmiques globaux.

---

# 5. Résultat principal à \(N=32768\)

| objet | fuite hors \(p^k\) | défaut de tour | \(Q\)-résidu après eulérisation | cohérence global/eulérisé |
|---|---:|---:|---:|---:|
| \(\zeta\) | \(1.81\times10^{-31}\) | \(3.08\times10^{-32}\) | \(8.40\times10^{-30}\) | \(1.0000\) |
| \(L(s,\chi_5)\) | \(1.18\times10^{-31}\) | \(2.68\times10^{-32}\) | \(3.38\times10^{-31}\) | \(1.0000\) |
| Davenport–Heilbronn [DH36b] [DH36a] | **0.9106** | **0.7976** | **1.3904** | **0.0751** |

Le contraste est massif.

Pour \(\zeta\) et \(L(s,\chi_5)\), PRIME-LOCK retrouve exactement la structure attendue à l'arrondi près.

Pour Davenport–Heilbronn, environ **91 % de l'énergie des coefficients de dérivée logarithmique se trouve hors du squelette des puissances de premiers** à cette troncature. En imposant artificiellement un Euler-produit de degré 1 tout en conservant les valeurs aux nombres premiers, le signal global est profondément modifié : son résidu énergétique dépasse même l'énergie du signal de départ et la cohérence tombe à environ \(0.075\).

Cela ne prouve rien sur RH. Cela montre seulement que, pour ce faux jumeau, l'absence de verrou local n'est pas une petite perturbation invisible du pipeline : elle domine sa géométrie globale.

---

# 6. Stabilité avec l'échelle pour Davenport–Heilbronn

| \(N\) | fuite hors \(p^k\) | défaut de tour | cohérence global/eulérisé |
|---:|---:|---:|---:|
| 8192 | 0.8532 | 0.8305 | 0.0278 |
| 16384 | 0.8823 | 0.8376 | 0.0070 |
| 32768 | 0.9106 | 0.7976 | 0.0751 |

La séparation n'est donc pas un accident d'une seule taille. Le défaut local reste massif sur toute la plage testée.

---

# 7. Crash-test apparié \(L_{\chi_5}\to DH\)

On reprend la trajectoire synthétique

\[
a_\theta=(1-\theta)\chi_5+\theta a_{DH},
\qquad 0\le\theta\le1.
\]

Sur les 11 valeurs de \(\theta\), le défaut multiplicatif coefficientiel, la fuite hors puissances de premiers et le défaut de tour augmentent dans exactement le même ordre :

\[
\boxed{
\rho_S(\mathcal D_F,L_F)=1,
\qquad
\rho_S(\mathcal D_F,T_F)=1.
}
\]

En revanche, la propagation vers le signal global est non linéaire :

\[
\rho_S(\mathcal D_F,R_Q)\approx0.291,
\]

et

\[
\rho_S(\mathcal D_F,\text{cohérence})\approx-0.864.
\]

Lecture : PRIME-LOCK mesure très directement la rupture multiplicative locale, mais la façon dont cette rupture se propage dans l'énergie globale \(Q\) est beaucoup moins triviale.

---

# 8. Crash-test Steinhaus : ce que PRIME-LOCK **ne** mesure pas

Huit suites complètement multiplicatives aléatoires de Steinhaus ont été utilisées comme témoins.

Elles donnent, à l'arrondi :

\[
L_F\simeq0,
\qquad
T_F\simeq0,
\qquad
R_Q\simeq0,
\qquad
\text{cohérence}\simeq1.
\]

C'est crucial.

PRIME-LOCK **ne détecte pas la fonction zeta**, ni la fonctionnelle, ni la criticité, ni RH. Il détecte essentiellement la **rigidité locale d'un Euler-produit de degré 1**.

Autrement dit :

\[
\boxed{
\text{PRIME-LOCK réussi}
\not\Rightarrow
\text{structure globale de type }L.
}
\]

Le détecteur est donc correctement calibré mais insuffisant.

---

# 9. Nouvelle carte adversariale

Les témoins produisent maintenant une séparation conceptuelle très utile :

| objet | verrou premier / Euler | symétrie fonctionnelle globale |
|---|---:|---:|
| \(\zeta\) | oui | oui |
| \(L(s,\chi_5)\) | oui | oui |
| Davenport–Heilbronn | **non** | oui |
| Steinhaus complètement multiplicatif | oui | **non / aucune complétion canonique connue dans ce protocole** |

Cela suggère que la prochaine question ne doit plus être :

> « Le produit d'Euler suffit-il ? »

La réponse expérimentale est clairement non.

La prochaine question devient :

> **Existe-t-il une contrainte de compatibilité locale–globale entre le verrou des nombres premiers et la symétrie archimédienne/fonctionnelle ?**

Nom de travail proposé :

# **DUAL-LOCK — verrouillage local/global**

Le but ne sera pas de tester séparément « Euler-produit oui/non » et « équation fonctionnelle oui/non », mais de rechercher un **terme d'interaction** entre les deux structures.

---

# 10. Verdict V6.2

PRIME-LOCK remplit son objectif : changer de canal après l'échec du bispectre brut.

Il produit un détecteur extrêmement discriminant de la structure eulérienne et montre qu'en Davenport–Heilbronn l'absence de verrou local se propage massivement au signal global.

Mais le contrôle Steinhaus ferme immédiatement toute interprétation excessive :

\[
\boxed{
\text{structure locale multiplicative}
\neq
\text{structure globale critique}.
}
\]

La piste suivante doit donc rechercher non une nouvelle statistique de multiplicativité, mais **l'accrochage entre structure locale et symétrie globale**.

---

## Fichiers reproductibles

### Code
- `3_Preuves_et_calculs/src/prime_lock.py`
- `3_Preuves_et_calculs/scripts/run_prime_lock.py`
- `3_Preuves_et_calculs/tests/test_prime_lock.py`

### Données
- `data/prime_lock_summary.csv`
- `data/prime_lock_scaling.csv`
- `data/prime_lock_chi_dh_scan.csv`
- `data/prime_lock_steinhaus_controls.csv`
- `data/prime_lock_correlations.json`
- `data/prime_lock_protocol.json`
- `data/prime_lock_chi_dh_scan.png`
- `data/prime_lock_DH_scaling.png`

## Références de cadrage

- DLMF §25.2 et §27.4 : produit d'Euler de \(\zeta\) et identité \(-\zeta'/\zeta=\sum \Lambda(n)n^{-s}\).
- DLMF §25.15 : produit d'Euler des fonctions \(L(s,\chi)\) de Dirichlet.
- Kaczorowski, Kulas, *Around the Davenport–Heilbronn function* : discussion de l'absence de produit d'Euler et des zéros dans des régions incompatibles avec une RH naïve pour ces combinaisons.

---

## Mise à jour V6.3d

Le tableau du §9 est complété par deux témoins (`24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md`, §4) : F6 (pas de produit d'Euler, zéros sur la droite) et E2 (produit d'Euler, zéros hors droite). Le verrou local mesuré par la fuite et le signe global sont indépendants ; il manque une borne de taille sur les facteurs locaux, et avec elle la question redevient l'hypothèse de Riemann généralisée.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié

<!-- references:fin -->
