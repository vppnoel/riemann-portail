"""V6.35 : comptages exacts sur des tours finies et spectres normalisés."""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT/"3_Preuves_et_calculs/data/v635_tour.json").read_text())
colors = {3: "#007c91", 5: "#ae4b3e", 7: "#7355a0", 11: "#62812d"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), layout="constrained")
ax = axes[0]
for p, color in colors.items():
    rows = [r for r in data["comptages"] if r["p"] == p]
    ax.plot([r["n"] for r in rows], [r["ecart_normalise"] for r in rows],
            marker="o", label=f"p = {p}", color=color)
ax.axhline(2, color="#222222", linestyle="--", linewidth=1.2)
ax.text(3.96, 2.05, "Borne déduite : 2", ha="right", fontsize=9)
ax.set(xlabel="Étage n de la tour", ylabel=r"$|N_n-p^n-1|\,/\,p^{n/2}$",
       title="Comptages directs", xticks=[1, 2, 3, 4], ylim=(-.06, 2.3))
ax.grid(alpha=.17)
ax.legend(ncol=2, frameon=False, loc="lower left")
ax = axes[1]
theta = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(theta), np.sin(theta), color="#222222", linewidth=1)
for s in data["spectres_controles"]:
    p, t = s["p"], s["trace"]
    x = t/(2*math.sqrt(p))
    y = math.sqrt(4*p-t*t)/(2*math.sqrt(p))
    ax.scatter([x, x], [y, -y], color=colors[p], s=42, label=f"p = {p}", zorder=4)
ax.axhline(0, color="#888888", linewidth=.6)
ax.axvline(0, color="#888888", linewidth=.6)
ax.set(xlabel="Partie réelle", ylabel="Partie imaginaire",
       title=r"Racines $\alpha/\sqrt{p},\ \beta/\sqrt{p}$",
       xlim=(-1.2, 1.2), ylim=(-1.15, 1.15), aspect="equal")
ax.grid(alpha=.17)
fig.savefig(ROOT/"1_Presentation/59_Tour_et_spectre.png", dpi=220, facecolor="white")
