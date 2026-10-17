# Références externes vérifiées

Dernière vérification : 2026-10-03.

1. Clay Mathematics Institute, **Riemann Hypothesis** — statut officiel : non résolue.  
   https://www.claymath.org/millennium/Riemann-Hypothesis/

2. J.-F. Burnol, **A note on Nyman's equivalent formulation of the Riemann Hypothesis**.  
   https://arxiv.org/abs/math/9910055

3. S. Bettin, J. B. Conrey, D. W. Farmer, **An optimal choice of Dirichlet polynomials for the Nyman-Beurling criterion**.  
   https://arxiv.org/abs/1211.5191

4. W. Ehm, **On certain Gram matrices and their associated series** (2024).  
   https://arxiv.org/abs/2405.06349

5. K. Matomäki, M. Radziwiłł, X. Shao, T. Tao, J. Teräväinen,
   **Higher uniformity of arithmetic functions in short intervals II. Almost all intervals**,
   Invent. Math. 244 (2026), 967–1091.  
   https://link.springer.com/article/10.1007/s00222-026-01408-6

6. L. Guth, J. Maynard, **New large value estimates for Dirichlet polynomials**,
   Annals of Mathematics 203 (2026), 623–675. Parmi les conséquences :
   `N(sigma,T) <= T^{30(1-sigma)/13+o(1)}`.  
   https://annals.math.princeton.edu/2026/203-2/p06

7. Sur Davenport–Heilbronn et l'absence de produit d'Euler : un exemple standard de série de
   Dirichlet à équation fonctionnelle de type Riemann possédant des zéros hors de la droite
   critique, y compris dans une région d'absolue convergence, est rappelé dans :  
   https://www.sciencedirect.com/science/article/abs/pii/S0022314X22001317

8. Saffari–Vaughan type mean-square bounds for primes in short intervals under RH are
   summarized, for example, in modern literature on short-interval variances.  
   https://link.springer.com/article/10.1007/s00209-024-03601-w

## Remarque sur la nouveauté

Les références servent à situer les ingrédients connus. En particulier :

- le cadre Nyman–Beurling/Báez-Duarte est classique ;
- les covariances de dents de scie reliées aux PGCD ont une littérature ancienne
  (Franel–Landau/Vasyunin) ;
- la formule terminale `H_inf(q)` est un calcul élémentaire de série de Dirichlet.

Aucune de ces identités ne doit être présentée comme nouvelle avant un recoupement
bibliographique spécifique.

## Ajout V4.1 — analyse spectrale / localisation de sources

- J. Main, V. A. Mandelshtam, G. Wunner, H. S. Taylor, *Harmonic inversion as a general method for periodic orbit quantization*, arXiv:chao-dyn/9709009 (1997).
- E. Bombieri, *Remarks on Weil's quadratic functional in the theory of prime numbers, I* — formule explicite de Guinand–Weil avec fonctions tests.
- A. Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, arXiv:math/9811068.
- A. Connes, H. Moscovici, *The UV prolate spectrum matches the zeros of zeta*, PNAS 119 (2022), e2123174119.

Voir `docs/SOURCE_LOCALIZATION.md` et `docs/SOURCES_RH_PROGRAMME.md` pour le statut de vérification et le positionnement.


## Références V4.2 — Hamiltoniens et Schrödinger

- H. Wu, D. W. L. Sprung, *Riemann zeros and a fractal potential*, Phys. Rev. E 48 (1993), 2595–2598. DOI 10.1103/PhysRevE.48.2595. Potentiel 1D reconstruit pour reproduire numériquement les zéros.
- M. V. Berry, J. P. Keating, *H = xp and the Riemann zeros* (1997/1999). Programme semi-classique Hilbert–Pólya.
- M. V. Berry, J. P. Keating, *The Riemann Zeros and Eigenvalue Asymptotics*, SIAM Review 41 (1999), 236–266. DOI 10.1137/S0036144598347497.
- G. Sierra, J. Rodríguez-Laguna, *The H=xp model revisited and the Riemann zeros*, Phys. Rev. Lett. 106 (2011), 200201. arXiv:1102.5356.
- A. Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, Selecta Math. 5 (1999), 29–106, arXiv:math/9811068.
- C. M. Bender et al., *Hamiltonian for the Zeros of the Riemann Zeta Function*, Phys. Rev. Lett. 118 (2017), 130201. À lire avec prudence : la construction souligne elle-même que l'auto-adjointeté rigoureuse est le point décisif.


## Références V4.3 — identification dynamique et métriques positives

- P. J. Schmid, *Dynamic mode decomposition of numerical and experimental data*, Journal of Fluid Mechanics 656 (2010), 5–28. DMD identifie un opérateur linéaire approchant l'évolution à partir de snapshots.
- J. H. Tu, C. W. Rowley, D. M. Luchtenburg, S. L. Brunton, J. N. Kutz, *On Dynamic Mode Decomposition: Theory and Applications*, Journal of Computational Dynamics 1 (2014), 391–421, DOI 10.3934/jcd.2014.1.391, arXiv:1312.0041.
- A. Mostafazadeh, *Pseudo-Hermiticity versus PT symmetry: The necessary condition for the reality of the spectrum of a non-Hermitian Hamiltonian*, Journal of Mathematical Physics 43 (2002), 205–214, DOI 10.1063/1.1418246.
- A. Mostafazadeh, *Pseudo-Hermiticity versus PT-Symmetry III: Equivalence of pseudo-Hermiticity and the presence of antilinear symmetries*, Journal of Mathematical Physics 43 (2002), 3944–3951, DOI 10.1063/1.1489072, arXiv:math-ph/0203005. En dimension diagonalisable, la réalité du spectre équivaut à l'existence d'un produit scalaire positif pour lequel l'opérateur est hermitien.

Ces références positionnent uniquement le formalisme fini-dimensionnel ; elles ne fournissent pas l'opérateur arithmétique requis par Hilbert–Pólya.
