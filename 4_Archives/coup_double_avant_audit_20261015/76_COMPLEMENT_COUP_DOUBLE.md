---
title: "Signe et couverture : le coup double précisément situé"
subtitle: "Complément au document 76 — Programme Riemann V6.55"
author: "Vincent P. P. NOËL — dossier de recherche, rédaction assistée"
date: "15 octobre 2026"
lang: fr
---

# 1. Ce qui change dans la direction de recherche

**Le transfert de couverture existe déjà dans le corpus. Le mécanisme arithmétique qui fournirait le signe global reste ouvert.** Le document 67, pont B3, construit un cœur dense en norme $H^1$ à support fixé et justifie le transfert d'une positivité établie sur toute la famille. Le document 76 donne des grammaires couvrantes : paquets traduits et deux filtres. Il serait inexact de remettre ces résultats à zéro.

La proposition « trouver $Q(f)=\|Tf\|^2$ » reçoit ici un opérateur candidat concret. Le résultat de cette passe est un contrat de travail vérifiable : établir une identité de Gram sur un cœur dense, puis employer une continuité obtenue indépendamment de cette identité. L'identité de Gram n'est pas prouvée ici.

Ce complément conserve les numéros des documents, les identifiants des idées et les outils de pilotage. Il prolonge les fiches IDE-044 (domaines), IDE-047 (Schur), IDE-050 (couverture), IDE-051 (signe) et IDE-052 (Weil). Les preuves ci-dessous sont des résultats auxiliaires, sans revendication de nouveauté et sans validation extérieure.

# 2. L'opérateur de la littérature et sa garde de continuité

[SuzH23] construit sans RH les fonctions $\mathfrak S_t\in L^2(\mathbb R)$ et l'opérateur
\[
T f=\pi^{-1/2}\widehat{\mathcal P_{Df}},\qquad Df=if'.
\]
Les propositions 1.2–1.3 définissent ce candidat ; le théorème 1.4 rend l'identité $\|Tf\|_2^2=\langle f,f\rangle_W$ sur tous les tests lisses compacts équivalente à RH. Le §3.2 établit aussi une borne uniforme de $\|\mathfrak S_t\|_2$ sur chaque compact de $t$. Nous utilisons ces résultats publiés comme entrées, sans redémontrer leur analyse complexe.

**Convention.** Nous notons $q(f,g)$ la forme de Weil de cette référence, rendue antilinéaire en première variable. Sa valeur diagonale reste celle de la source. Le $Q_W$ arithmétique du document 76 emploie sa propre convention Fourier et des moments polaires nuls. Avant tout calcul comparatif, il faut dériver leur concordance exacte à partir de la formule explicite, facteur de normalisation compris. Ce raccord n'est pas certifié numériquement dans cette passe.

**Lemme A — Continuité indépendante de l'identité.** Pour $S>0$, poser
\[
M_S=\sup_{|t|\le S}\|\mathfrak S_t\|_2<\infty,
\qquad C_S=\sqrt{2S/\pi}\,M_S.
\]
Alors, pour $f\in C_c^\infty(-S,S)$,
\[
\boxed{\|Tf\|_2\le C_S\|f'\|_2.}
\]
**Preuve.** La formule intégrale de $\widehat{\mathcal P}$ donne
\[
\|Tf\|_2\le\pi^{-1/2}\int_{-S}^{S}
 \|\mathfrak S_t^\sharp\|_2|f'(t)|\,dt
\le\pi^{-1/2}M_S\|f'\|_1
\le C_S\|f'\|_2.
\]
Sur l'axe réel, la conjugaison $\sharp$ préserve la norme. Minkowski puis Cauchy–Schwarz donnent les deux inégalités. L'opérateur s'étend donc par continuité à $H_0^1(-S,S)$. Les extensions pour supports emboîtés coïncident sur leur domaine commun, par densité et unicité. Aucune constante uniforme en $S$ n'est nécessaire. Aucune positivité de Weil n'a été utilisée.

**Portée.** Ce lemme raccorde le candidat publié à la topologie de couverture du corpus. La constante est finie ; aucune valeur numérique certifiée de $M_S$ n'est fournie ici.

# 3. Le défaut qui porte l'obligation globale

Dans un espace $E_S$ où $q$ est continu en norme $H^1$, définir
\[
\mathfrak D(f,g)=q(f,g)-\langle Tf,Tg\rangle_2,
\qquad d(f)=\mathfrak D(f,f).
\]
On peut choisir le sous-espace à moments polaires nuls du document 67, après raccord des normalisations. Pour le critère publié sur tous les tests compacts, choisir le domaine de forme correspondant et sa continuité. Il faut déclarer lequel est employé ; ces choix ne se substituent pas silencieusement.

**Lemme B — Identité sur un cœur, signe sur le domaine.** Soient $f_j$ tels que l'union de $V_n=\operatorname{span}_{\mathbb C}(f_1,\ldots,f_n)$ soit dense dans $E_S$. Si
\[
\mathfrak D(f_i,f_j)=0\quad\text{pour tous }i,j,
\]
alors $q(f,f)=\|Tf\|_2^2\ge0$ pour tout $f\in E_S$.

**Preuve.** La sesquilinéarité donne la nullité sur chaque $V_n\times V_n$. Pour $f_n\to f$ dans $H^1$, la continuité de $q$ donne $q(f_n,f_n)\to q(f,f)$ et le lemme A donne $Tf_n\to Tf$ dans $L^2$. Passer à la limite dans l'identité prouve le résultat. Traiter chaque support entier $S\ge1$ couvre tout test compact. Cette implication n'exige aucune minoration strictement positive uniforme.

**Variante moins exigeante.** Une factorisation exacte est suffisante, mais elle n'est pas nécessaire pour établir le signe. Si, pour tous $n$,
\[
q(v,v)\ge-\varepsilon_{S,n}\|v\|_{H^1}^2
\quad(v\in V_n),\qquad\varepsilon_{S,n}\longrightarrow0,
\]
le signe suit également. En effet, un $v\in V_m$ appartient à tous les $V_n$ ultérieurs ; sa norme reste fixe, puis la densité achève la preuve. Ce transfert était déjà présent dans le document 67. Il reste à produire l'estimation arithmétique pour tous les rangs.

# 4. Pourquoi il faut tester les mélanges

Avec notre convention antilinéaire en première variable,
\[
\operatorname{Re}\mathfrak D(f,g)
=\frac{d(f+g)-d(f-g)}4,
\]
\[
\operatorname{Im}\mathfrak D(f,g)
=-\frac{d(f+ig)-d(f-ig)}4.
\]
Ces identités suivent en développant les quatre formes quadratiques. Elles déterminent exactement les couplages et leurs phases.

**Contre-exemple réel.** Pour $T=I$ sur $\mathbb C^2$ et
\[
Q=\begin{pmatrix}1&2\\2&1\end{pmatrix},
\]
les deux vecteurs de base ont la bonne énergie, mais $q(1,-1)=-2$. Une vérification brique par brique échoue.

**Contre-exemple complexe.** Pour
\[
Q=\begin{pmatrix}1&2i\\-2i&1\end{pmatrix},
\]
$q(x)=\|x\|^2$ pour tout vecteur réel $x$, tandis que $q(1,i)=-2$. Même tous les tests réels ne valident pas une forme hermitienne arbitraire. Une symétrie particulière peut réduire les tests seulement après démonstration de cette symétrie.

Ces deux matrices sont des contre-modèles abstraits de protocoles insuffisants ; elles ne sont pas des matrices de Weil. Pour l'opérateur exact de Suzuki, un défaut non nul démontré rigoureusement aurait une portée sur RH. Une différence flottante sans contrôle des intégrales, singularités apparentes et queues ne suffit pas.

# 5. La brique d'assemblage : Schur sans perdre les noyaux

Soit $M\succeq0$ une matrice hermitienne, $b$ une colonne et $a$ un réel. Poser
\[
\widetilde M=\begin{pmatrix}M&b\\b^*&a\end{pmatrix}.
\]
**Lemme C.** Avec $M^\dagger$ la pseudo-inverse de Moore–Penrose,
\[
\widetilde M\succeq0
\iff b\in\operatorname{Ran}M\ \text{et}\
\delta=a-b^*M^\dagger b\ge0.
\]
**Preuve.** Si $z\in\ker M$, la restriction à $(tz,1)$ impose $z^*b=0$, sinon le terme linéaire prend des valeurs négatives arbitraires. Ainsi $b\perp\ker M$, donc $b\in\operatorname{Ran}M$. Sous cette condition, compléter le carré sur l'image donne
\[
x^*Mx+2\operatorname{Re}(x^*by)+a|y|^2
=(x+M^\dagger by)^*M(x+M^\dagger by)+\delta|y|^2.
\]
La nécessité et la suffisance suivent.

Si $M=V^*V$, on garde les anciennes colonnes et on ajoute
\[
w=VM^\dagger b+\sqrt\delta\,e,
\]
où $e$ est un vecteur unitaire orthogonal à toutes les anciennes colonnes. On obtient $V^*w=b$ et $\|w\|^2=a$ : la réalisation Gram est compatible avec l'étape précédente.

**Usage et limite.** Une règle arithmétique qui impose l'appartenance à l'image et $\delta\ge0$ à tous les rangs ferait le coup double sur une famille couvrante. Le lemme ne fournit pas cette règle. Factoriser des matrices dont on connaît déjà le signe ne constitue pas une preuve supplémentaire de ce signe. La garde d'image reste indispensable lorsqu'un pivot s'annule.

# 6. Deux fausses couvertures écartées

**Mauvaise norme.** Sur $C_c^\infty(-1,1)$, poser $r(f)=\|f\|_2^2-|f(0)|^2$. Les fonctions nulles au voisinage de zéro sont denses dans $L^2$ et y ont $r\ge0$. Pourtant, pour une bosse $\phi(0)=1$, $f_\eta(x)=\phi(x/\eta)$ donne $r(f_\eta)=\eta\|\phi\|_2^2-1<0$ pour $\eta$ petit. L'évaluation ponctuelle n'est pas continue en norme $L^2$ ; elle l'est en $H^1$ en dimension un.

**Norme qui s'échappe.** $r(f)=-\|f\|^2$, $R_n(f)=e^{2n}\|f\|^2$ et $\varepsilon_n=e^{-n}$ satisfont $r(f)\ge-\varepsilon_nR_n(f)$ pour $n\ge0$, avec $\varepsilon_n\to0$. Pourtant le signe reste négatif. Ce qui doit tendre vers zéro est le produit d'erreur pour chaque test fixé.

# 7. Protocole actif, critères de décision et portée

| Étape | Produit exigé | État de cette passe |
|---|---|---|
| Domaines et transfert | Continuité indépendante de l'identité, cœur et exhaustion | Lemme A établi à partir de la borne publiée ; transfert rappelé et prouvé |
| Normalisations | Égalité exacte entre forme publiée et forme arithmétique du corpus sur le domaine choisi | À dériver avant comparaison numérique |
| Couplages | Formule de $\mathfrak D(f_i,f_j)$ à partir des vrais coefficients, avec phases complexes | Obligation ouverte |
| Assemblage | Garde d'image et dette de Schur pour toute la grammaire | Lemme C prouvé ; règle arithmétique ouverte |
| Calculs | Contre-modèles, polarisation complexe, pivots singuliers | Contrôles exacts exécutés par le programme joint |
| Conclusion RH | Quantificateurs sur tous les rangs et supports, gardes satisfaites | Non obtenue |

Le programme joint ne calcule pas l'opérateur de Suzuki sur les premiers : il vérifie exactement les identités algébriques et les pièges qui décideront de la validité d'un tel calcul. Il ne fournit aucun certificat numérique de RH.

**Décision de recherche.** Conserver l'identité de Gram comme cible structurée et l'inégalité à erreur évanescente comme alternative. Le prochain calcul utile doit exposer le défaut mixte avec ses conventions et ses bornes d'erreur. Une simple extension de plafond ou une série de normes positives n'apporterait pas ce renseignement.

Le Bellman documentaire conserve ses coûts et ses scores : aucune probabilité de réussite n'est inventée. Ses investigations « couverture constructive », « dette duale » et « test de paquets » reçoivent les nouvelles pièces et les obligations précises. Les niveaux de progression restent inchangés : un raccord fonctionnel ne ferme pas le signe global.

# Références et pièces reliées

- [SuzH23] M. Suzuki, *On the Hilbert space derived from the Weil distribution*, arXiv:2301.00421, version consultée v3 ; propositions 1.2–1.3, théorème 1.4, §3.2. [Texte](https://arxiv.org/html/2301.00421v3) ; [publication](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/on-the-hilbert-space-derived-from-the-weil-distribution/FD33EBD117A6B448053450DD8D62ADB6). Vérification ciblée le 15 octobre 2026.
- Document 67, *Construire des ponts avec Bellman*, ponts B2, B3, B5 : domaines, cœur et Schur.
- Document 76, *Weil : retrouver la piste du signe global*, §2.3–2.4 : grammaires couvrantes et rôle de l'arithmétique.
- Documents 78–79 : transport cohérent, compensations et obstructions aux résumés trop grossiers.
- Programme : `3_Preuves_et_calculs/coup_double_20261015/verifier_coup_double.py` ; résultats : `resultats.json` ; confrontation : `CONFRONTATION.md`.
