# Relecture de l'Archipel d'Euler (note 30, §3) : résumé pour l'auteur

**Ce que j'ai vérifié.** J'ai refait toutes les preuves du §3 :
- l'équation fonctionnelle commune ;
- la formule du défaut au premier ordre ;
- le noyau du défaut ;
- la déduction à partir de Saias–Weingartner.

J'ai aussi fait des contrôles numériques (formule exacte à 3·10⁻¹⁴ près pour les 27 points d'Euler), et j'ai vérifié les sources : Saias–Weingartner (résumé et Théorème 2), Kaczorowski–Perelli, Booker–Thorne. Pour Hamburger, seules les données bibliographiques ont été vérifiées.

**Ce qui est solide.**
- La Proposition 3.3 est juste, et la formule vaut pour tous m, n, pas seulement premiers entre eux.
- Elle se renforce en une identité exacte : pour une direction transverse b = Σ_{χ′≠χ} β_{χ′} u_{χ′} χ′ au point d'Euler λ·u_χ·L(s, χ), la moyenne du carré du défaut sur les paires de classes vaut λ²·(3·Σβ² + |Σβu|²), donc au moins 3λ²·Σβ². Les valeurs propres 2,36 à 3,27 dépendent de la troncature (M = 40) ; mieux vaut citer l'identité.
- Le corollaire 3.4 est juste. Il devient même une équivalence : pour c ≠ 0, pas de zéro dans Re s > 1 ⇔ point d'Euler.

**Ce qui est fragile.**
1. **La déduction écrite au §3.4 a un trou comblable.**
   - Les phases u_χ ont disparu des formules.
   - Le caractère χ₀ donné par Saias–Weingartner peut avoir un module quelconque, pas forcément q.
   - Les cas p(1) = 0, χ₀ trivial ou de mauvaise parité, et c = 0 ne sont pas traités.
   - Le plus simple est de citer directement leur Théorème 2 : une combinaison d'au moins deux L primitives a ≫ T zéros dans 1 < Re s < 1 + η.
2. **Ce corollaire n'est pas nouveau.** C'est un cas particulier immédiat de Saias–Weingartner (Th. 2), et aussi de Booker–Thorne. Il faut l'attribuer ainsi et retirer « démontré ici » pour cette partie.
3. **Au §3.1, la phrase « Même chose dans V₅ pair » est fausse telle quelle.** (1 + 5^(1/2−s))·ζ(s) a exactement l'équation fonctionnelle de L(s, (·/5)) et donne une déformation (avec un pôle). Elle n'est vraie que dans V_q, ou parmi les fonctions entières.
4. **La phrase en gras du §3.3 et le titre doivent dire « dans V_q ».** Les autres directions qui gardent l'équation fonctionnelle existent : en parité paire, la direction (1 + q^(1/2−s))·ζ(s).

**Le degré 2 est déjà connu pour la partie 3.4.** Booker–Thorne (2014), Th. 1.1, donnent le résultat pour S₂₄ : une forme sans zéro dans Re s > 25/2 est une forme propre de Hecke. L'analogue de 3.3 reste à écrire.

**Verdict : prêt après petites corrections.**

**Trois questions pour le relecteur externe.**
1. L'attribution « corollaire immédiat de Saias–Weingartner, Th. 2 » est-elle la bonne, ou existe-t-il une référence plus ancienne ?
2. Connaît-on une version effective de η, ou de la hauteur du premier zéro dans Re s > 1, en fonction de la distance au point d'Euler ?
3. En degré 2 (S₂₄), la rigidité au premier ordre aux formes propres, et l'analogue de la constante 3, sont-ils connus ou immédiats ?
