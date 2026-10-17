# Relecture du Théorème B : résumé pour l'auteur

**Vérifié.** J'ai refait toute la preuve : Plancherel sur Re s = ½+η, borne ponctuelle de G, queue uniforme en η, calcul local du pôle double (constante A²/(4|ρ|²)), termes croisés entre zéros, ordre des limites, étape de Karamata et valeur S = 4κ. J'ai aussi relu REFEREE_A/B/C, cherché l'antériorité (une dizaine de requêtes) et refait les calculs numériques avec mon propre code.

**Solide.** La preuve est correcte et je n'y ai trouvé aucune erreur. Q_η est exactement la transformée de Laplace–Stieltjes de U(L) = Q(e^L), qui est croissante, en λ = 2η : Karamata s'applique donc tel quel. Les paires de zéros proches (H3) ne touchent pas le terme dominant, parce que η → 0 est pris à hauteur Y fixée, avant Y → ∞ ; c'est aussi pourquoi il n'y a pas de vitesse. κ est vérifié à 8·10⁻⁶ près (relatif) avec 1070 zéros et une correction de queue.

**Petites retouches avant envoi.** (1) Restreindre η à (0, ¼] à l'étape 4, sinon la droite sort du rectangle [½, ¾]. (2) Remplacer O_Y(η^½) par O_Y(η). (3) Rédiger en entier la borne |G| ≪ (log t)W + log²t, « point majeur » de REFEREE_B ; c'est fait dans la note anglaise. (4) Donner des références exactes pour F1–F4 (Titchmarsh 9.2 et 9.6(A), Davenport ch. 12, Widder ou Korevaar pour Karamata) ; je les cite de mémoire.

**Hors du Théorème B.** α ≈ −0,264 est une somme partielle sur 300 zéros sans correction de queue. La valeur corrigée est α ≈ −0,307, stable de 100 à 1070 zéros, car Re b_ρ = −2θ′(γ) − 2γ_E exactement. β vaut environ 0,64, valeur incertaine. Avec ces valeurs, Q(X) est reproduit à 1–5 % près jusqu'à 10⁸. Le rapport à (4κ/3)L³ (de 0,44 à 0,755) progresse lentement à cause du terme moyen en L², ce qui est attendu.

**Antériorité.** Je n'ai trouvé nulle part l'énoncé B lui-même. L'analogue pour ψ, ∫(ψ−x)²x⁻²dx ∼ (Σ m/|ρ|²) log X, est cité par Brent–Platt–Trudgian (J. Number Theory 238, 2022) d'après Montgomery–Vaughan. B en est la transposition au pôle double : il ne faut pas présenter la méthode comme nouvelle. Nouveau corollaire, à faire vérifier : sous RH, S ≥ 4κ, avec égalité si et seulement si tous les zéros sont simples.

**Verdict.** Prêt à envoyer après ces petites retouches ; rien à changer sur le fond.

**Questions au relecteur externe :**
1. B, ou un théorème de type Cramér pour des pôles d'ordre k sur Re s = ½, figure-t-il déjà dans la littérature (Montgomery–Vaughan ch. 13, cadre B² d'Akbary–Ng–Shahabi) ?
2. Acceptez-vous que la preuve n'utilise aucune information sur les écarts entre zéros (queue uniforme en η, termes croisés à Y fixé) ?
3. Peut-on obtenir un reste O((log X)^{3−δ}) sous RH seule, ou toute vitesse exige-t-elle une hypothèse sur les paires proches ou sur ζ′(ρ) ?

Note complète : `RELECTURE_THEOREME_B_EN.md`, dans ce même dossier.
