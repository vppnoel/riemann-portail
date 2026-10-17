> **Statut v3 : diagnostic historique.** Cette note est conservée pour reproductibilité. Le schéma GPS/Kalman n'est plus une priorité de preuve ; voir `docs/PRIORITES.md`.

# Dernière évolution — « GPS analytique » par canaux de diviseurs

## 1. Ce qui est analogue au GPS/Kalman

La partie purement Kalman est simplement une projection quadratique séquentielle:

\[
R_{j+1}=R_j-K_jU_j,
\quad
K_j=\frac{\langle R_j,U_j\rangle}{\|U_j\|^2},
\quad
P_{j+1}=P_j(1-\rho_j^2).
\]

C'est utile pour suivre les variances/covariances, mais cela ne crée aucun théorème arithmétique nouveau.

Le vrai analogue d'un modèle de navigation apparaît lorsqu'on dispose d'un **état terminal analytique** pour les canaux de covariance.

## 2. Canaux de diviseurs

Pour un bloc `I`, la covariance des dents de scie se factorise via

\[
H_I(q)=\sum_{\substack{d\in I\\q\mid d}}\frac{a(d)}d,
\qquad
\Sigma(I,J)=\frac1{12}\sum_qJ_2(q)H_I(q)H_J(q).
\]

Pour la somme complète

\[
H_\infty(q)=\sum_{q\mid d}\frac{a(d)}d,
\]

on peut calculer une valeur terminale fermée.

## 3. Formule terminale exacte [RIG]

Si `q` n'est pas sans carré, `H_infty(q)=0`. Pour `q` sans carré,

\[
\boxed{
H_\infty(q)=
-\frac{2\mu(q)}{\varphi(q)}
\left(
\log q+\sum_{p\mid q}\frac{\log p}{p-1}
\right).
}
\]

Et `H_infty(1)=0`.

### Dérivation

Pour `d=qm` et `(m,q)=1`, introduisons

\[
F_q(s)=\sum_{(m,q)=1}\frac{\mu(m)}{m^s}
=\frac1{\zeta(s)}\prod_{p\mid q}(1-p^{-s})^{-1}.
\]

Comme `1/zeta(1)=0`, `(1/zeta)'(1)=1`, `(1/zeta)''(1)=-2 gamma`, les moments logarithmiques de `F_q` donnent la formule ci-dessus après dérivation du produit fini.

## 4. Interprétation

Pour chaque canal `q`, on possède donc:

- une **mesure partielle** `H_D(q)` calculable;
- une **position terminale attendue** `H_infty(q)` exacte;
- un résidu de queue `H_infty(q)-H_D(q)`;
- une pondération de covariance `J_2(q)`.

C'est un analogue nettement plus fidèle d'un filtre de navigation: on compare un état partiel observé à une destination analytique connue, puis on doit borner l'incertitude de la queue.

## 5. Diagnostic numérique

Le fichier `data/channel_terminal_summary.csv` mesure

\[
\sum_{q\le Q}J_2(q)|H_\infty(q)-H_D(q)|^2
\]

pour `D=100000`.

Le résidu est très petit pour les tout petits canaux, puis augmente lorsque `Q` approche l'échelle de troncature. Cela soutient une stratégie hybride:

1. traiter exactement/finement les petits `q`;
2. utiliser des estimations moyennes pour la longue queue de grands `q`;
3. optimiser le seuil `Q` par balance biais/variance.

## 6. Verrou inchangé

La formule terminale n'est pas RH. Le point difficile devient une borne suffisamment forte sur la somme pondérée des **résidus de queue des canaux**. Il faut exploiter leur corrélation et la structure Möbius; la majoration absolue ne suffit pas.

