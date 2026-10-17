"""V6.36 : marges numériques et sous-espace négatif validé de DH."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
rep=json.loads((ROOT/"3_Preuves_et_calculs/data/v636_norme.json").read_text())
e=np.array(rep["valeurs_propres_40_premieres"])
fig,ax=plt.subplots(figsize=(8.3,3.7),layout="constrained")
ax.axvspan(.5,25.5,color="#ba3d45",alpha=.09)
ax.axhline(0,color="#555555",lw=.8)
ax.scatter(np.arange(1,26),e[:25],color="#ba3d45",s=26,label="25 vecteurs proposés : compression validée négative")
ax.scatter(np.arange(26,41),e[25:],color="#73828a",s=22,label="Autres valeurs calculées : pas de certificat complémentaire")
ax.set_yscale("symlog",linthresh=1e-12)
ax.set(xlabel="Indice dans le spectre numérique ordonné",ylabel="Valeur propre calculée",
       title="DH : fenêtre a = 0,02 ; h = 0,005 ; L = 1115",xlim=(.5,40.5))
ax.grid(alpha=.2)
ax.legend(fontsize=8,loc="lower right",frameon=False)
fig.savefig(ROOT/"1_Presentation/60_Marges_du_certificat.png",dpi=220,facecolor="white")
