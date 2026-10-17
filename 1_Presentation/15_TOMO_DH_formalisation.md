# V6 — TOMO-DH : tomographie multiplicative inter-échelles

**Statut :** branche exploratoire falsifiable  
**Version :** 6.0 — 5 octobre 2026  
**But :** transformer l'intuition « perte d'information par passage à une norme » en un programme testable qui sépare corrélation d'ordre 2, information de phase d'ordre 3 et défaut multiplicatif.

## 1. Correction conceptuelle de départ

La fonction classique de Davenport–Heilbronn [DH36b] [DH36a] est un excellent témoin négatif parce qu'elle satisfait une équation fonctionnelle de type Riemann mais **ne possède pas de produit d'Euler**. Le séparateur recherché n'est donc pas la symétrie fonctionnelle seule, mais la rigidité multiplicative absente chez Davenport–Heilbronn.

Schéma de travail :

\[
\text{symétrie analytique} \neq \text{rigidité multiplicative}.
\]

Cette distinction devient le principe adversarial de la branche TOMO-DH.

## 2. TOMO-2 — cohérence inter-échelles d'ordre 2

On part d'un signal arithmétique \(C_F(t)\). Dans le cas de \(\zeta\), le candidat naturel est le signal déjà utilisé dans le programme.

On passe en coordonnées logarithmiques :

\[
u=\log t,\qquad g_F(u)=e^{-u/2}C_F(e^u).
\]

Alors

\[
\int_0^\infty |C_F(t)|^2\,\frac{dt}{t^2}
=\int_{-\infty}^{\infty}|g_F(u)|^2\,du.
\]

Une dilatation de \(t\) devient une translation de \(u\). Pour \(\tau_j=j\delta\), définir

\[
(T_\tau g)(u)=g(u-\tau)
\]

et la matrice de Gram

\[
\boxed{K^{(2)}_{ij}(F)=\langle T_{\tau_i}g_F,T_{\tau_j}g_F\rangle.}
\]

Elle est hermitienne positive et, hors effets de bord, de type Toeplitz :

\[
K^{(2)}_{ij}=R_F(\tau_i-\tau_j).
\]

### Limite fondamentale

Par Plancherel [Tit37],

\[
K^{(2)}_{ij}
=\frac1{2\pi}\int |\widehat g_F(\omega)|^2e^{i\omega(\tau_i-\tau_j)}\,d\omega.
\]

Donc \(K^{(2)}\) ne dépend que du **spectre de puissance** \(|\widehat g_F|^2\). La phase spectrale a disparu.

Conséquence : TOMO-2 ne doit pas être appelée « tomographie de phase ». Son nom correct est :

> **tomographie de cohérence inter-échelles d'ordre 2**.

Deux signaux ayant le même module de transformée de Fourier et des phases différentes doivent donner la même matrice \(K^{(2)}\), à effets de bord près.

## 3. Observable TOMO-2

Si

\[
K^{(2)}v_k=\lambda_kv_k,
\qquad
p_k=\frac{\lambda_k}{\operatorname{tr}K^{(2)}},
\]

on définit l'entropie spectrale normalisée

\[
\boxed{
\mathcal H_2(F)=-\frac1{\log m}\sum_{k=1}^m p_k\log p_k.
}
\]

Elle mesure la concentration de la covariance inter-échelles, **pas** un alignement de phase.

La première question expérimentale est seulement :

\[
\mathcal H_2(\zeta)\stackrel{?}{\neq}\mathcal H_2(DH)
\]

après normalisations et témoins adéquats.

## 4. Étalon algébrique : défaut multiplicatif

Pour une série de Dirichlet normalisée

\[
F(s)=\sum_{n\ge1}\frac{a_F(n)}{n^s},\qquad a_F(1)=1,
\]

définir

\[
\boxed{\Delta_F(m,n)=a_F(mn)-a_F(m)a_F(n),\qquad (m,n)=1.}
\]

Pour un objet multiplicatif, \(\Delta_F(m,n)=0\).

On introduit un indicateur de calibration

\[
\boxed{
\mathcal D_F(P)=\sum_{\substack{m,n\le P\\(m,n)=1}}
w_{m,n}|\Delta_F(m,n)|^2.
}
\]

Ainsi, pour \(\zeta\), \(\mathcal D_\zeta(P)=0\) exactement. Pour Davenport–Heilbronn, le défaut multiplicatif est non nul.

**Rôle de \(\mathcal D_F\) :** étalonner ce que signifie « voir la multiplicativité ». Il ne constitue pas une avancée sur RH.

## 5. Question V6 reformulée

La question n'est plus :

> « \(K^{(2)}\) distingue-t-elle \(\zeta\) de Davenport–Heilbronn ? »

mais :

> **Un invariant de TOMO-2 détecte-t-il indirectement la même rigidité que le défaut multiplicatif \(\Delta_F\), sans que cette rigidité ait été injectée explicitement dans sa définition ?**

Si non, la branche TOMO-2 est diagnostique seulement.

## 6. TOMO-3 — phase et fermeture ternaire

Pour conserver une information de phase, passer à l'ordre 3.

Définir une tricorrélation logarithmique

\[
R_F^{(3)}(\tau_1,\tau_2)
=\int g_F(u)g_F(u+\tau_1)\overline{g_F(u+\tau_2)}\,du.
\]

Le bispectre associé est

\[
\boxed{
B_F(\omega_1,\omega_2)
=\widehat g_F(\omega_1)
\widehat g_F(\omega_2)
\overline{\widehat g_F(\omega_1+\omega_2)}.
}
\]

Si \(\widehat g_F(\omega)=A_F(\omega)e^{i\phi_F(\omega)}\), alors

\[
\arg B_F
=\phi_F(\omega_1)+\phi_F(\omega_2)-\phi_F(\omega_1+\omega_2).
\]

Cette quantité conserve un couplage de phase que TOMO-2 élimine.

## 7. Principe de fermeture multiplicative

La multiplicativité arithmétique obéit à

\[
a(mn)=a(m)a(n),
\]

et, en coordonnées logarithmiques,

\[
\log(mn)=\log m+\log n.
\]

Le bispectre couple précisément des fréquences vérifiant

\[
\omega_3=\omega_1+\omega_2.
\]

D'où le programme exploratoire :

\[
\boxed{
\text{multiplication arithmétique}
\xrightarrow{\log}
\text{addition d'échelles}
\xrightarrow{\text{ordre 3}}
\text{fermeture de phase}.
}
\]

**Principe de fermeture multiplicative (hypothèse de travail).**  
Un objet possédant une structure multiplicative cohérente peut produire, après représentation logarithmique adaptée, une signature ternaire plus rigide qu'une superposition non multiplicative.

Ce principe n'est pas démontré ; il est conçu pour être falsifié.

## 8. Crash-tests obligatoires

| Témoin | Produit d'Euler / multiplicativité | Équation fonctionnelle | Rôle |
|---|---:|---:|---|
| \(\zeta\) | oui | oui | cible |
| \(L(s,\chi)\) appropriée | oui | oui | contrôle multiplicatif proche de DH |
| Davenport–Heilbronn | non | oui | témoin adversarial principal |
| signal \(\zeta\) à phases Fourier randomisées | détruite au niveau du signal | n/a | contrôle TOMO-2 vs TOMO-3 |
| suite complètement multiplicative aléatoire | oui au niveau coefficientiel | non | séparer multiplicativité et structure analytique |

### Test interne essentiel

Construire \(\widetilde g\) tel que

\[
|\widehat{\widetilde g}(\omega)|=|\widehat g_\zeta(\omega)|
\]

avec phases randomisées. Alors, à conventions et bords identiques,

\[
K^{(2)}(\widetilde g)=K^{(2)}(g_\zeta).
\]

Si le code obtient autre chose, il y a un bug, une normalisation cachée ou un effet de bord non contrôlé.

TOMO-3, elle, doit généralement changer.

## 9. Règle d'arrêt

La branche TOMO est rétrogradée si, après contrôle du spectre de puissance, des effets de bord et du défaut multiplicatif :

1. TOMO-3 ne sépare pas les témoins au-delà de ce que prédit déjà \(\mathcal D_F\) ; ou
2. toute séparation disparaît sous normalisation ; ou
3. la signature observée est entièrement expliquée par un invariant classique déjà connu et n'ajoute aucune structure exploitable.

## 10. Prochaine cible minimale

La question suivante est volontairement petite :

\[
\boxed{
\text{Existe-t-il une relation mesurable entre }
B_F(\omega_1,\omega_2)
\text{ et }
\Delta_F(m,n)
\text{ après passage en coordonnées logarithmiques ?}
}
\]

Trois issues sont acceptables :

- **relation structurelle non triviale** : ouvrir une sous-branche ;
- **relation purement tautologique** : classer comme reformulation ;
- **absence de relation robuste** : fermer TOMO-DH.

## 11. Collision bibliographique minimale

- Les bispectres/polyspectres sont des statistiques d'ordre supérieur conçues pour détecter des dépendances inter-fréquences et des couplages de phase absents des statistiques d'ordre 2.
- Les matrices de Gram et structures de dilatation apparaissent déjà dans des généralisations du cadre Nyman–Beurling [Nym50] [Beu55] ; la nouveauté éventuelle ne peut donc pas être « utiliser une matrice de Gram », mais seulement le couplage précis entre multiplicativité arithmétique, échelle logarithmique et statistique d'ordre 3.
- Davenport–Heilbronn reste un témoin indispensable car l'équation fonctionnelle seule n'implique pas un produit d'Euler ni RH.

## 12. Statut V6

**TOMO-2 :** défini, rôle corrigé, testable.  
**TOMO-3 :** défini, conserve l'information de fermeture de phase.  
**Pont multiplicativité ↔ bispectre :** hypothèse ouverte, prochaine cible.  
**Revendiquer un lien avec RH :** interdit à ce stade.


## 13. Position dans DARK-ZETA

TOMO-DH devient le **premier détecteur** du cadre transversal DARK-ZETA (« secteur sombre arithmétique »).

L'analogie est uniquement méthodologique : une information peut être invisible à un observable d'ordre faible tout en laissant des effets sur plusieurs observables d'ordre supérieur. TOMO fournit un cas-test exact de cette idée :

\[
K^{(2)} \text{ élimine la phase},
\qquad
B_F \text{ conserve une fermeture de phase ternaire}.
\]

La campagne DARK-ZETA impose donc que tout signal TOMO survivant soit triangulé avec au moins un second canal indépendant — défaut multiplicatif, inertie/forme de Weil [Wei52], criticité ou statistique de Möbius — avant toute interprétation structurelle.

**Interdiction :** une séparation TOMO entre \(\zeta\) et Davenport–Heilbronn ne suffit pas à elle seule. Elle doit être reliée analytiquement à une propriété arithmétique et survivre aux contrôles de randomisation et de normalisation.


# 13. Mise à jour après construction du premier détecteur

Le protocole a été implémenté dans `3_Preuves_et_calculs/src/dark_zeta.py` et exécuté à plusieurs échelles. Le verdict initial est **négatif pour TOMO-3 dans sa forme brute** : la bicoherence du signal agrégé `C_F` ne suit pas de manière stable le défaut multiplicatif et reste proche de son nul obtenu par phases randomisées.

TOMO-2 montre en revanche une corrélation forte avec le défaut multiplicatif sur la trajectoire appariée `chi_5 -> DH`, mais les contrôles Steinhaus prouvent que cette entropie n'est **pas** un invariant universel de multiplicativité.

Statut révisé :

- **TOMO-2 : SURVIT COMME DIAGNOSTIC** ;
- **TOMO-3 brut : RÉTROGRADÉ** ;
- **pont multiplicativité ↔ bispectre brut : NON OBSERVÉ** ;
- **prochaine étape : changer de canal avant d'augmenter l'ordre statistique**.

Voir `17_DARK_ZETA_premier_detecteur_resultats.md`.

# 14. Mise à jour V6.3d

La question du §10 est tranchée (`24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md`, §7) : dans le canal u, le bispectre de C_F teste les relations additives entre zéros, pas la multiplicativité ; dans le canal t, la fermeture ternaire redonne exactement Δ_F (relation tautologique, classée comme reformulation). Le signal de TOMO-2 est reconstruit à partir des zéros seuls (§5). Règle d'arrêt n° 3 appliquée : **TOMO-3 brut clos.**

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [Beu55] A. Beurling. *A closure problem related to the Riemann zeta-function*. Proc. Natl. Acad. Sci. USA 41 (1955), 312–314. <https://www.pnas.org/doi/pdf/10.1073/pnas.41.5.312> — vérifié en ligne
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [Nym50] B. Nyman. *On the one-dimensional translation group and semi-group in certain function spaces*. Thèse, Université d'Uppsala, 1950. — partiellement vérifié
- [Tit37] E. C. Titchmarsh. *Introduction to the Theory of Fourier Integrals*. Oxford, Clarendon Press, 1937. — non vérifié
- [Wei52] A. Weil. *Sur les « formules explicites » de la théorie des nombres premiers*. Comm. Sém. Math. Univ. Lund, vol. suppl. dédié à M. Riesz (1952), 252–265. <https://en.wikipedia.org/wiki/Weil%27s_criterion> — partiellement vérifié

<!-- references:fin -->
