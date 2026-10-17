"""Document 58 : synthèse reproductible depuis les résultats V6.34."""
from pathlib import Path
import json,pandas as pd
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';P=ROOT.parent/'1_Presentation'
def fr(x,d=3):return f'{x:.{d}f}'.replace('.',',')

def main():
    v7=json.loads((D/'v634_relief_v7.json').read_text())
    v11=json.loads((D/'v634_independant_v11.json').read_text())
    roots=json.loads((D/'v634_racines_recoupees.json').read_text())
    jets=json.loads((D/'v634_jets_certificats.json').read_text())
    rows=pd.read_csv(D/'v634_relief_v7.csv')
    tab7='\n'.join(f"| {r.id} | {'>300 (censuré)' if r.T_proxy>300 else str(int(r.T_proxy))} | {'>300 (censuré)' if r.censure else str(int(r.premiere_detection))} |" for _,r in rows[~rows.euler].iterrows())
    tabroot='\n'.join(f"| {r['id']} | {fr(float(r['beta_mp']),9)} | {fr(float(r['gamma_mp']),9)} |" for r in roots)
    tabjet='\n'.join(f"| {r['p']} | {r['J']}, {r['K']}, {r['M']} | {r['dimension']} | {r['rang_majore']} | {r['borne_S']} | {r['S']} |" for r in jets)
    ci=v11['bootstrap_a1_IC95'];cid=v11['bootstrap_D_IC95']
    text=r"""# V6.34 - Validation directe du relief et lemme des jets

**Document 58. Auteur : Vincent P. P. NOËL. Date : 12 octobre 2026.**

**Ce qui est acquis.** Les articles sont corrigés, le relief est contrôlé par un comptage direct, l'ancrage par le premier coefficient est testé sur une autre famille, et le mécanisme des jets donne une borne démontrée dans le modèle fini. Prévisions et résultats sont conservés séparément. L'indicateur garde ses niveaux : ces travaux n'ont pas encore de relecture externe.

![Validation directe et borne des jets](58_Validation_directe_et_jets.png)

## 1. Deux articles plus précis

L'article 1 contient désormais le **critère conjoint** obtenu en combinant A et B′ :

$$\lim_{X\to\infty}\frac{Q(X)}{(\log X)^3}=\frac{4\kappa}{3}
\quad\Longleftrightarrow\quad
\text{RH et simplicité de tous les zéros non triviaux},$$

où $\kappa=2+\gamma_E-\log(4\pi)$. Le sens direct n'a pas besoin de supposer RH : la limite finie impose une croissance polylogarithmique ; A donne alors $\Theta=1/2$, puis B′ donne la simplicité. Le sens réciproque vient de B. C'est une conséquence des résultats déjà présents. Le signe ≥ de la remarque sur Cramér est corrigé.

Dans l'article 2, le côté arithmétique de $-F'/F$ contient des indices qui ne sont pas des puissances de premiers pour Davenport-Heilbronn : son coefficient en 6 vaut $(1+\xi^2)\log6\ne0$. La conjugaison de la preuve d'inertie est rectifiée. La positivité exacte exige toutes les ordonnées réelles, ou un contrôle de la queue en norme. Une paire hors droite apporte une direction négative lorsque ses deux vecteurs restent indépendants ; une compression ou un fond positif peut la masquer. L'audit des traces à $10^{-6}$ ne certifie pas les signes au seuil $10^{-11}$.

Trois formulations historiques sont corrigées dans leurs textes et PDF :

- **47 :** la dualité classe par classe implique l'équation fonctionnelle agrégée ; celle-ci ne reconstitue pas les espaces de sections.
- **51 :** les automorphismes sur les valeurs et les points du site arithmétique sont distingués des endomorphismes sur les faisceaux du carré. L'échec du modèle d'échelle étudié ne ferme pas tous les mécanismes possibles.
- **56 :** RH impose un point d'Euler dans la famille ; sa réciproque serait une instance de GRH, qui reste ouverte. Le seuil historique T* mesure un déficit persistant relatif à un témoin.

Le fichier `articles/LISEZMOI_ARTICLES.md` donne les questions précises de relecture : transition taubérienne de B, nouveauté, références, conventions complexes et erreurs spectrales. Les lettres restent des brouillons.

## 2. Le relief V₇, compté directement

Le protocole écrit avant les nouveaux calculs sélectionne huit points connus de la carte V₇, plus les trois témoins d'Euler. Il s'agit d'une **validation de l'instrument** : la carte historique était déjà connue.

Pour $F_c(s)=\sum c_\chi e^{-i\phi_\chi}L(s,\chi)$, $c$ réel et caractères primitifs impairs, on compte les zéros de la fonction complétée entière

$$\Lambda_c(s)=(q/\pi)^{(s+1)/2}\Gamma((s+1)/2)F_c(s).$$

Sa réflexion donne $\Lambda_c(s)=\overline{\Lambda_c(1-\bar s)}$. Le contour symétrique est $[1-\sigma_R,\sigma_R]\times[-T,T]$. Un facteur réel positif est retiré pour éviter le sous-dépassement de Gamma ; cela conserve les arguments. Le bord droit est garanti sans zéro par

$$\frac{|a(1)|}{\|c\|_2}>\sqrt d\,(\zeta(\sigma_R)-1),$$

car $|a(n)|\le\sqrt d\|c\|_2$. Ici $\sigma_R=3$ pour V₇ et 4 pour V₁₁. La différence entre le comptage total et les changements de signe sur la droite donne le nombre de zéros hors droite détectés, sans comparaison à une autre fonction.

**Contrôles.** Pas vertical 0,02, puis 0,01 sur la droite et sur le bord droit ; raffinement horizontal jusqu'à un saut de phase inférieur à 0,8 radian. Aucune ligne de contour ne reste ambiguë selon ce critère, aucun comptage ne change aux raffinements et les différences sont paires et non négatives. Les résidus d'enroulement entier sont inférieurs à $3\cdot10^{-11}$. Des tangences sans changement de signe ou des oscillations plus fines que le maillage demanderaient une certification supplémentaire : le calcul reste numérique.

| Point sélectionné | T* historique | Première détection directe |
|---|---:|---:|
@@TAB7@@

Les trois témoins d'Euler ne présentent aucun zéro hors droite détecté jusqu'à 300. Aux deux points du col, le seuil 145 retarde fortement la sortie réelle. Les quatre points intermédiaires ou bas concordent à ±2. Les deux observations censurées restent sans sortie détectée à 300 ; la valeur historique stockée $10^6$ était un marqueur, pas une mesure.

**P3 n'est pas validée :** quatre concordances sont établies sur huit, deux points sont en désaccord et deux sont censurés. La prévision de six concordances ne peut pas être déclarée tenue. Les deux désaccords réfutent déjà l'identification générale du seuil historique à une première sortie.

### Racines recoupées par un second évaluateur

Les caractères, sommes de Gauss et phases sont reconstruits à 50 chiffres. `mpmath.dirichlet` retrouve les racines d'Euler-Maclaurin ; l'écart maximal est inférieur à $2\cdot10^{-13}$. Les chiffres supplémentaires servent au contrôle et ne valent pas certificat d'intervalles. Chaque racine a son partenaire $1-\bar\rho$ par réflexion ; le signe de la hauteur est conservé ci-dessous.

| Point | Re ρ | Im ρ |
|---|---:|---:|
@@TABROOT@@

## 3. L'ancrage sur une famille indépendante V₁₁

Le nouvel échantillon contient **96 directions réelles uniformes sur la sphère de dimension 4**, graine 6341101, et cinq témoins d'Euler. Il n'est pas sélectionné depuis le relief V₇. Le plafond est 150 ; trois directions non Euler sont censurées. Les cinq témoins restent sans sortie détectée. Toutes les premières détections sont stables aux raffinements.

La distance au point d'Euler est projective : $\arccos\max_\chi|c_\chi|$ pour $\|c\|_2=1$. Les corrélations sont des corrélations de rang après régression sur les rangs des contrôles. Les censures reçoivent un rang ex æquo au-dessus de 150 ; ce n'est pas une estimation des hauteurs non observées.

| Mesure | Résultat |
|---|---:|
| Corrélation T–\|a(1)\|, distance contrôlée | **@@CORR@@** |
| Intervalle bootstrap à 95 %, 1 000 rééchantillonnages de directions | [@@CILO@@ ; @@CIHI@@] |
| Même corrélation, 93 observations non censurées | @@UNC@@ |
| Corrélation T–D, distance et \|a(1)\| contrôlés | **@@D@@** |
| Intervalle bootstrap à 95 % pour cette dernière | [@@DLO@@ ; @@DHI@@] |

La prévision P4 demandait une corrélation positive au moins égale à 0,3 : elle est **tenue**. P5 demandait une corrélation résiduelle négative avec le défaut de multiplicativité : le signe observé est positif, la prévision est **fausse selon le critère fixé**. Cette mesure ne démontre pas de causalité. D contient déjà une contribution de $|a(1)|^2$, suivant l'identité du document 57 ; il ne fournit pas une seconde force indépendante établie.

## 4. Le lemme des jets produit une borne

Le document 48 mesurait la perte de rang due au Frobenius. Voici sa formulation pour une cubique $f$ sur $\mathbb F_p$. Posons $g=f^{(p-1)/2}$ et $S=\{a:f(a)\ne0,\ g(a)=1\}$. L'espace de polynômes

$$W=\operatorname{span}\{x^{jp+a},x^{jp+a}g:0\le j<J,\ 0\le a<K\}$$

a dimension $2JK$ si $K\le(p-3)/2$ : tous les degrés dominants sont distincts. Pour $M<p$, l'application des jets de Hasse aux points de S vérifie

$$\operatorname{rang}\mathcal J_M\le
\sum_{k=0}^{M-1}\min\{|S|,K+J-1+2k\}
\le M(K+J-1)+M(M-1).$$

**La preuve.** $D(x^{jp})=0$. La récurrence $P_0=1$, $P_{k+1}=fP'_k+(e-k)f'P_k$, $e=(p-1)/2$, donne $f^kD^kg=gP_k$ et $\deg P_k\le2k$. Après multiplication des lignes de jets par $f(a)^k$, le bloc d'ordre k se factorise par des polynômes de degré au plus $K+J-2+2k$. C'est la borne de rang. Les dérivées ordinaires et de Hasse sont équivalentes ici car $k!$ est inversible.

Si $2JK$ dépasse cette borne, un **polynôme non nul** s'annule à l'ordre M en tous les points de S. Son degré est au plus $(J-1)p+K-1+3(p-1)/2$, d'où

$$|S|\le U:=\left\lfloor
\frac{(J-1)p+K-1+3(p-1)/2}{M}\right\rfloor.$$

Les paramètres sont choisis sans connaître les points ; le minimum présenté est celui de la fenêtre déclarée $J,M\le256$.

| p | J, K, M | Dimension | Rang majoré | Borne U | \|S\| exact |
|---:|---|---:|---:|---:|---:|
@@TABJET@@

Pour 29, 61 et 101, les coefficients d'un témoin sont conservés ; ses multiplicités sont vérifiées par division synthétique, indépendamment des jets. Pour 1009 et 10007, l'existence découle du lemme ; aucune grande matrice n'est construite.

### Une famille de paramètres explicite

Pour $r=\lfloor\sqrt{(p-5)/6}\rfloor\ge1$, choisir

$$J=r+1,\quad K=3r^2-r+1,\quad M=2r.$$

Alors dimension moins rang majoré vaut **2** pour toute cubique. On obtient

$$U=\left\lfloor\frac p2+\frac{3(p-1)}{4r}+\frac{3r-1}{2}\right\rfloor
=\frac p2+O(\sqrt p).$$

La même borne s'applique au tordu par un non-résidu quadratique. Si z est le nombre de racines de f, $N=2|S|+z+1$ vérifie

$$|N-(p+1)|\le2U-p+z=O(\sqrt p),\qquad z\le3.$$

C'est une borne démontrée, plus faible que Hasse : la constante asymptotique de cette famille est $2\sqrt6$, contre 2 pour la borne de Hasse sur une cubique lisse. La méthode de Stepanov est classique. La preuve complète est dans `preuves/LEMME_RANG_JETS_V634.md` ; aucune nouveauté mathématique n'est revendiquée pour cette réalisation.

## 5. Prochaines étapes justifiées par ces résultats

1. **Relecture externe des articles.** A, B et le critère conjoint sont des résultats concrets à faire contrôler ; le dossier explicite les passages et références à vérifier.
2. **Ancrage, test apparié V₁₃.** Fixer à l'avance des couples de directions à distances d'Euler comparables et dissocier premier coefficient et défaut. Le résultat V₁₁ justifie ce test ; il ne suffit pas à appeler l'ancrage une force causale.
3. **Signatures et erreurs en norme.** Recertifier les signes du cas DH à 25 directions avec une marge supérieure à l'erreur complète. Les concordances de traces ne suffisent pas à cette décision.
4. **Transfert du lemme d'existence.** Fournir un espace indépendant, un opérateur de jets et un contrôle des multiplicités pour les entiers. Les unités fictives du document 50 accompagnent correctement les bilans, mais ce transfert exige ces objets et leurs propriétés.

Le gain de cette version est précis : le relief est mieux défini, l'ancrage résiste à une réplication indépendante et le modèle fini possède une preuve de borne. La construction qui imposerait l'analogue à ζ reste le problème structurel ouvert.

## Reproduction et provenance

Depuis `3_Preuves_et_calculs/`, exécuter :

```bash
python scripts/run_v634_relief_direct.py --part all
python scripts/run_v634_root_crosscheck.py
python scripts/run_v634_jet_bound.py
python scripts/figure_v634.py
python scripts/build_v634_document.py
python tests/run_all_tests.py
```

Le protocole antérieur aux nouveaux comptages est `data/prevision_v634_relief.md`. Sélections, comptages bruts, diagnostics, statistiques, racines et certificats sont conservés sous le préfixe `v634_`. Les calculs de contours sont numériques ; les calculs sur $\mathbb F_p$ sont exacts. Les modules nouveaux sont `src/relief_direct.py` et `src/jet_bound.py`.

Sources de contexte : Stepanov (1969), <https://mathnet.ru/eng/im2197> ; Bombieri (1973), <https://www.numdam.org/item/SB_1972-1973__15__234_0/> ; Connes–Consani, *The Arithmetic Site* (2014), introduction, §2.3 et §3, <https://arxiv.org/html/1405.4527v1>. Les articles du corpus, les documents 47, 48, 50, 51, 56 et 57 constituent les sources internes.

Les calculs, preuves élémentaires et révisions V6.34 ont été préparés avec l'aide de ChatGPT (OpenAI), à la suite du travail initial du corpus avec Claude (Anthropic). Responsabilité finale : l'auteur.
"""
    substitutions=dict(TAB7=tab7,TABROOT=tabroot,TABJET=tabjet,
        CORR=fr(v11['corr_T_a1_sachant_distance']),CILO=fr(ci[0]),CIHI=fr(ci[1]),
        UNC=fr(v11['corr_T_a1_non_censures']),D=fr(v11['corr_T_D_sachant_distance_a1']),DLO=fr(cid[0]),DHI=fr(cid[1]))
    for k,v in substitutions.items():text=text.replace('@@'+k+'@@',v)
    (P/'58_VALIDATION_DIRECTE_DU_RELIEF_ET_LEMME_DES_JETS.md').write_text(text,encoding='utf-8-sig')
if __name__=='__main__':main()
