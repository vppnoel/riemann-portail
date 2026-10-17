from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

out = Path(__file__).resolve().parent
fig, ax = plt.subplots(figsize=(15, 10.8))
fig.patch.set_facecolor('#f5f7fa')
ax.set_facecolor('#f5f7fa')
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
fig.subplots_adjust(left=.025, right=.975, top=.98, bottom=.02)

def box(x, y, label, kind='known', width=.285, height=.112):
    colors = {'known': ('#eaf4ef', '#37735e'),
              'open': ('#fff1d6', '#b57721'),
              'goal': ('#eaf0f9', '#3c5c86')}
    fill, edge = colors[kind]
    patch = FancyBboxPatch((x-width/2, y-height/2), width, height,
        boxstyle='round,pad=0.008,rounding_size=0.012',
        linewidth=1.5, facecolor=fill, edgecolor=edge)
    ax.add_patch(patch)
    ax.text(x, y, label, ha='center', va='center', fontsize=12.2,
            color='#173042', linespacing=1.45)

def arrow(start, end, missing=False):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=17,
        linewidth=1.6, linestyle='--' if missing else '-',
        color='#b57721' if missing else '#496477', connectionstyle='arc3,rad=0'))

ax.text(.5, .97, 'Les parcours convergent vers une obligation globale',
        ha='center', va='top', fontsize=21, weight='bold', color='#172e45')
ax.text(.5, .925, 'Navigateur, indicateur et Bellman organisent les parcours ; les estimations décident le résultat.',
        ha='center', va='top', fontsize=12.7, color='#4a5d70')

xs = [.17, .5, .83]
for x, title in zip(xs, ['VOIE DE WEIL', 'VOIE DU SIGNAL DE SUZUKI', 'VOIE DE L’ÉNERGIE CLASSIQUE']):
    ax.text(x, .858, title, ha='center', fontsize=12, weight='bold', color='#233e58')

top = ['Tests admissibles\nP, moments, norme et parité',
       'Signal exact de Suzuki\nMesure première et source',
       'Vrais poids de Mangoldt\nIdentité des diviseurs']
mid = ['Réduction tête–queue\nSchur et certificats locaux',
       'Bilans de transport\nBrique initiale et gardes locales',
       'Énergie ancrée J(X)\nCorrélations avec coupure']
bottom = ['Pour tout support :\nsigne de la tête corrigée\net dette de couplage',
          'À toute échelle :\nadmissibilité et signe\ndu profil intérieur',
          'Pour tout X ≥ 1 :\nJ(X) ≤ C · X²\navec C indépendant de X']
for x, a, b, c in zip(xs, top, mid, bottom):
    box(x, .774, a); box(x, .584, b); box(x, .376, c, 'open', height=.137)
    arrow((x,.709), (x,.649))
    arrow((x,.519), (x,.454), missing=True)
    arrow((x,.299), (.5 + (x-.5)*.35, .222))

box(.5, .166, 'RH  ↔  positivité globale de Weil', 'goal', width=.61, height=.085)
ax.text(.5, .087, 'Les implications sont connues ; les conditions orange restent à établir.',
        ha='center', fontsize=12.4, weight='bold', color='#6e501a')
ax.text(.5, .046, 'Raccourcis fermés dans leur portée : marge H¹ uniforme • préfixes seuls • garde agrégée à rapport fixe',
        ha='center', fontsize=10.7, color='#8d4043')
ax.text(.5, .012, 'Traits pleins : identité ou implication écrite. Pointillés : estimation manquante. Aucun signe global obtenu.',
        ha='center', fontsize=10.9, color='#5b6e7f')
for ext in ['png', 'svg']:
    fig.savefig(out/f'CARTE_DES_PARCOURS.{ext}', dpi=160, facecolor=fig.get_facecolor())
