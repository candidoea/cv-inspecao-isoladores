from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

PASTA = Path("data/interim/images")
SAIDA = Path("reports/fase3")

E = np.load(SAIDA / "embeddings.npy")
nomes = [c.name for c in sorted(PASTA.glob("*.jpg"))]
defeito = np.array([len(Path(n).stem) == 3 for n in nomes])
sim = E @ E.T
i, j = np.triu_indices(len(nomes), k=1)
s = sim[i, j]

# 1. calibração: como é a similaridade entre pares quaisquer
print("Similaridade entre todos os pares:")
for p in [5, 25, 50, 75, 95, 99]:
    print(f"  percentil {p:>2}: {np.percentile(s, p):.3f}")

# 2. os pares a olhar
cruzados = np.where((defeito[i] != defeito[j]) & (s >= 0.90))[0]
def perto(alvo, mesmo_defeito):
    m = np.where(defeito[i] == defeito[j])[0] if mesmo_defeito is None else \
        np.where((defeito[i] == mesmo_defeito) & (defeito[j] == mesmo_defeito))[0]
    return m[np.argmin(np.abs(s[m] - alvo))]

escolhidos = list(cruzados[np.argsort(-s[cruzados])])
for alvo in (0.97, 0.94, 0.90):
    escolhidos.append(perto(alvo, True))     # defeito x defeito
    escolhidos.append(perto(alvo, False))    # normal x normal

# 3. uma linha por par: imagem a | imagem b
fig, axes = plt.subplots(len(escolhidos), 2, figsize=(9, 3.2 * len(escolhidos)))
for linha, k in enumerate(escolhidos):
    for col, idx in enumerate((i[k], j[k])):
        axes[linha, col].imshow(Image.open(PASTA / nomes[idx]))
        axes[linha, col].set_title(f"{nomes[idx]}  (sim {s[k]:.3f})", fontsize=9)
        axes[linha, col].axis("off")
plt.tight_layout()
plt.savefig(SAIDA / "pares_para_inspecao.png", dpi=80)
print("\nFigura salva em", SAIDA / "pares_para_inspecao.png")