# V4.3 — Générateur arithmétique, métrique positive et conservation

**Statut : [HEUR/NUM/GAP].** Ce document formalise l'étape suivante de la branche Schrödinger/flux. Il ne modifie pas les Théorèmes A/B/C et ne constitue pas une preuve de RH.

## 1. But précis

La V4.2 associait formellement à un zéro

\[
\rho=\beta+i\gamma
\]

le mode en temps logarithmique

\[
\psi_\rho(t)=e^{(\beta-1/2)t}e^{i\gamma t}
\]

et l'énergie effective

\[
E_\rho=-\gamma+i(\beta-1/2)
\]

(en unités \(\hbar=1\)). La V4.3 demande si cette dynamique peut être **identifiée à partir du signal arithmétique**, plutôt que construite en injectant les zéros.

La chaîne proposée est

\[
\boxed{
\text{primes}\to\text{signaux multicanaux}\to A\to H_{\rm eff}\to M\to H_{\rm eff}^*M-MH_{\rm eff}.
}
\]

Le point de preuve potentiel n'est pas l'ajustement numérique d'un spectre fini. Il serait de dériver analytiquement les objets \((H,M)\) depuis l'arithmétique et de démontrer une conservation uniforme.

## 2. Construction d'un état observable

Partir d'un signal de nombres premiers filtré, par exemple

\[
y_j(t)=K_j*\left(\sum_{n\ge2}\frac{\Lambda(n)}{\sqrt n}\,\delta_{\log n}\right)(t)-d_j(t),
\]

où \(d_j\) contient les termes déterministes connus de la formule explicite. Les canaux \(K_j\) peuvent être des gaussiennes, dérivées de gaussiennes, ondelettes, filtres de Slepian, etc.

Former un vecteur d'état par empilement des canaux et de retards :

\[
z(t)=\big(y_1(t),\ldots,y_m(t),y_1(t-\tau),\ldots\big)^T.
\]

On cherche ensuite un propagateur fini-dimensionnel

\[
z(t+\Delta t)\approx A z(t).
\]

C'est la même classe de méthodes que Prony, matrix pencil, ESPRIT, DMD/Koopman et l'identification de systèmes linéaires.

## 3. Du propagateur au Hamiltonien effectif

Si

\[
A\approx e^{-iH_{\rm eff}\Delta t},
\]

alors, sur une branche cohérente du logarithme matriciel,

\[
\boxed{
H_{\rm eff}=\frac{i}{\Delta t}\log A.
}
\]

Un mode \(e^{(\beta-1/2+i\gamma)t}\) donne

\[
\lambda(A)=e^{(\beta-1/2+i\gamma)\Delta t},
\]

d'où

\[
\lambda(H_{\rm eff})=-\gamma+i(\beta-1/2).
\]

Ainsi :

- \(\beta=1/2\) : énergie réelle, amplitude neutre ;
- \(\beta>1/2\) : partie imaginaire positive, gain ;
- \(\beta<1/2\) : partie imaginaire négative, perte.

## 4. La métrique n'a aucune raison d'être euclidienne

Dans un problème inverse, la métrique naturelle peut être donnée par un Gram, une covariance ou une énergie du milieu. On cherche donc une matrice hermitienne positive

\[
M>0
\]

telle que

\[
\boxed{H^*M=MH.}
\]

Ceci signifie que \(H\) est auto-adjoint pour

\[
\langle u,v\rangle_M=u^*Mv.
\]

En temps discret, la conservation correspondante est

\[
\boxed{A^*MA=M.}
\]

et l'énergie quadratique

\[
\mathcal E_M(t)=z(t)^*Mz(t)
\]

est conservée.

### Fait fini-dimensionnel important

Si \(H\) est diagonalisable, alors :

- s'il existe \(M>0\) tel que \(H^*M=MH\), le spectre de \(H\) est réel ;
- réciproquement, si \(H=VDV^{-1}\) avec \(D\) réel, alors
  \[
  M=(V^{-1})^*V^{-1}>0
  \]
  satisfait \(H^*M=MH\).

Cette équivalence est utilisée dans le module numérique V4.3 comme **diagnostic**, pas comme preuve de RH.

## 5. Relation avec Gram, covariance et « GPS analytique »

La V4.3 réunit plusieurs branches antérieures :

1. **Nyman–Beurling / Gram** : fournit naturellement des métriques positives ;
2. **GPS/Kalman** : fournit des matrices de covariance et des compléments de Schur ;
3. **source localization** : fournit les états et les paramètres \((\beta,\gamma)\) ;
4. **Schrödinger/flux** : fournit le critère de conservation.

Le défaut

\[
\boxed{\mathcal D_M(H)=H^*M-MH}
\]

est alors interprété comme un défaut de conservation interne. En discret :

\[
\mathcal U_M(A)=A^*MA-M.
\]

## 6. Formulation du verrou RH dans cette branche

Une voie de preuve demanderait bien plus qu'un bon fit numérique. Il faudrait construire, depuis les données arithmétiques seules :

- un espace d'état \(\mathcal H_{\rm arith}\) ;
- un générateur exact \(H\) ;
- une métrique positive \(M\) ;
- un opérateur d'observation reliant cet état à la formule explicite ;

puis démontrer

\[
H^*M=MH
\]

et que chaque zéro \(\rho\) fournit effectivement une valeur spectrale

\[
E_\rho=-\gamma+i(\beta-1/2).
\]

Alors la réalité du spectre imposerait \(\beta=1/2\).

Le **GAP-SCHR-GEN** est précisément l'absence actuelle d'une telle dérivation exacte.

## 7. Test Davenport–Heilbronn

La fonction de Davenport–Heilbronn possède des zéros hors de la droite critique. Le pipeline est donc falsifiable :

- construire le même type de signaux à partir de ses coefficients ;
- identifier \(A\) et \(H_{\rm eff}\) ;
- vérifier que le défaut métrique ne peut pas être supprimé par une métrique positive stable, ou que des valeurs propres complexes persistent.

Un pipeline qui rendrait Davenport–Heilbronn artificiellement « hermitien » serait rejeté.

## 8. Ce que les expériences finies peuvent et ne peuvent pas montrer

Elles peuvent tester :

- stabilité de l'identification \(A\) ;
- sensibilité au lissage et aux retards ;
- conditionnement de la métrique \(M\) ;
- séparation d'un mode hors ligne synthétique ;
- comparaison zêta / Davenport–Heilbronn.

Elles ne peuvent pas montrer :

- auto-adjointeté de l'opérateur arithmétique infini ;
- absence de zéros hors ligne à des hauteurs non observées ;
- unicité du générateur identifié ;
- convergence du modèle fini vers un opérateur exact.

## 9. Critère de succès analytique

La branche ne devient mathématiquement décisive que si l'on peut démontrer une propriété de type

\[
\exists M>0:\quad H^*M=MH
\]

avec contrôle uniforme de la coercivité

\[
c\|u\|^2\le u^*Mu\le C\|u\|^2
\]

lorsque la dimension et la hauteur augmentent, et un lien spectral exact avec les zéros de \(\zeta\).

Sans ces trois éléments — **positivité, uniformité, exactitude spectrale** — la branche reste une méthode de traitement de signal / diagnostic.


## 10. Audit v4.4 (voir `AUDIT_V4_3.md`)

- Les tests de §§3–7 sont circulaires (modes injectés) ; le certificat M>0 est équivalent à « spectre réel ».
- Sur le vrai signal ψ : Re λ biaisé de −0,002 à −0,09 pour des zéros critiques, fantômes à haute fréquence ; sur DH : zéro hors ligne détecté (Re = +0,23 pour +0,3085) **et** mode fantôme à +0,345 (Im ≈ 73,8).
- Le signal d'ordre 2 (G) est défectif (bloc de Jordan) : exclu ; seul le signal d'ordre 1 avec zéros simples est admissible.
- `spectral_metric(..., metric_cond_max=...)` permet de rejeter les métriques dégénérées (cond(M) ≈ cond(V)²).
