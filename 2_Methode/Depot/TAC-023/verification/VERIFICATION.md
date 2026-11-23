# TAC-023 — Vérification du second dépôt, note anglaise v4

23 novembre 2026 · ia:chatgpt-sol-6.1-max · **conforme** pour l'exposition conditionnelle. Ce jugement concerne le dépôt enregistré dans `942c0e99` après [la correction nº 71](https://github.com/vppnoel/Riemann/pull/71). L'avis précédent est reproduit plus bas pour conserver la chronologie.

Les deux empreintes d'entrée et les deux empreintes du dépôt concordent. Le diff du producteur porte exclusivement sur la note et son rapport. Les passages modifiés ont été relus face au code Lean figé à `51d9b1a28026d458aef9c9af3df8b083276e3d2d`.

1. Au §5, `HostExW` choisit la famille S avant de quantifier sur les échelles s. La version anglaise donne séparément ε, le seuil sur x, l'égalité s.J = S.J et l'appartenance de s.x à S.Win. Cela restitue les lignes 102–105 de `ThinScalesIffHostBound.lean` et la ligne 23 de `Scales.lean`. Deux échelles de même ε et même x peuvent différer par J ; le texte rend désormais cette restriction explicite.
2. Au §2, les deux renvois à `landau_pole_asym` aboutissent à sa déclaration en ligne 23. La borne abstraite de `landau_pole_re_le` est correctement donnée comme Re ρ ≤ 2. La borne ≤ 1 est attribuée aux fonctions L de Dirichlet. La dichotomie couvre ses deux branches en présence d'un zéro initial réel.
3. Rejeu du contrôleur de liens avec le contenu des fichiers lu au commit Lean figé. Sur 93 occurrences et 40 fichiers, il signale deux libellés de fichier : `Main.lean` pointe à la déclaration du théorème et `TopPlug` à l'appel avec λ = 3/2. Les deux passages indiqués sont pertinents. Aucun écart résiduel parmi les quatre corrections demandées.
4. La démonstration conditionnelle et le témoin ζ du dépôt précédent restent applicables. L'estimation (⋆) reste admise ; fournir les entrées arithmétiques qui la produisent dépasse la portée de cette note. Vérification sur sources, sans recompilation Lean.

**Intérêt pour un lecteur.** La note est prête à être proposée à un analyste qui souhaite suivre le passage de (⋆) à GRH et localiser les hypothèses importées. Un test de sa valeur pédagogique serait de demander à un lecteur extérieur d'identifier, à partir du texte seul, l'étape qui fournit la borne sur fenêtres et les échelles auxquelles elle s'applique. Cette appréciation éditoriale interne ne vaut ni validation humaine ni déclaration de nouveauté.

---

# TAC-023 — Vérification de la note anglaise, version 3

Vérificateur : ia:chatgpt-sol-6.1-max. 23 novembre 2026. Verdict : **non_conforme**. L'implication conditionnelle est justifiée. La définition de l'un des termes que la fiche demandait explicitement de traduire reste à corriger avant diffusion.

## Contrôle de l'argument

Les deux entrées et les deux pièces du dépôt correspondent aux empreintes enregistrées. Lecture de la note, comparaison avec TAC-017 et le code Lean au commit `51d9b1a28026d458aef9c9af3df8b083276e3d2d`. La relecture a porté sur les 92 occurrences de liens dans 40 fichiers, sur la teneur des énoncés et sur les passages ajoutés. Il n'y a pas eu de recompilation Lean ni d'audit des preuves arithmétiques admises au §5.

- Le §2 donne l'inégalité (K) à partir des moments et de la partie positive. La coupure des queues et le choix du petit paramètre permettent la contradiction dans les deux cas géométriques. Le caractère trivial redonne le témoin TAC-017.
- Les §§3 à 5 distinguent l'existence des hôtes, la production de familles, la moyenne `core_gm` et le critère analytique `formB`. L'application utilise λ = 3/2. La preuve du résultat arithmétique qui fournit (⋆) reste hors du périmètre. Le moteur analytique appliqué à un analogue de Davenport–Heilbronn ne produirait pas cette estimation.
- Le §6(c) traite séparément s = 0 par ζ(0) = −1/2. Avec les hypothèses du texte, la déduction (⋆) ⇒ GRH ⇒ RH tient. La note anglaise est une exposition conditionnelle.

## Écart qui impose une reprise

Le §5 définit `HostExW` en promettant un hôte à chaque échelle de paramètre ε dont le point x est assez grand et appartient à Win. Or [HostExW, ligne 102](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/ThinScalesIffHostBound.lean#L102) exige `S.Mem s`. La [définition de Mem, ligne 23](https://github.com/leanprover-community/riemann-hypothesis/blob/51d9b1a28026d458aef9c9af3df8b083276e3d2d/src/Development/AutomorphicArithmetic/PrimeDiscriminants/Scales.lean#L23) est `s.J = S.J ∧ s.x ∈ S.Win`. On peut conserver x et ε en changeant J. La phrase attribue alors à Lean une existence supplémentaire.

Correction anglaise proposée pour le passage : “For each admissible ε there are constants and a family of scales S with a fixed parameter S.J. Its set S.Win contains arbitrarily late windows. Every scale s satisfying s.eps = ε, s.J = S.J, and s.x ∈ S.Win, with s.x sufficiently large, admits a host satisfying the stated conditions.”

## Autres retouches pour la version destinée aux lecteurs

- Les deux liens étiquetés `landau_pole_asym` doivent pointer à la ligne 23. À la ligne 14 commence `landau_pole_asym_deriv`. La présence du nom comme préfixe ne distingue pas ces deux déclarations.
- Pour `landau_pole_re_le`, la borne abstraite est Re ρ ≤ 2. Elle suffit pour σ > 2. Attribuer séparément aux fonctions L considérées la borne plus forte Re ρ ≤ 1.
- Dans le passage sur un zéro de Siegel, un zéro initial réel ne force pas à lui seul le cas B de la dichotomie. La preuve couvre les deux branches.

**Portée éditoriale.** Une fois la définition et les renvois corrigés puis revérifiés, la note est candidate à une diffusion comme guide de lecture conditionnel. Son utilisation comme référence d'étalonnage (unité E2) doit conserver la version et le verdict correspondants.
