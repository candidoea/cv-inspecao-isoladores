import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

PASTA = Path("data/interim/images")
SAIDA = Path("reports/fase3")
tabela = pd.read_csv(SAIDA / "grupos.csv", dtype={"imagem": str})

tamanhos = tabela.groupby("grupo").size().sort_values(ascending=False)
posicao = int(sys.argv[1]) if len(sys.argv) > 1 else 0     # 0 = maior grupo, 1 = segundo maior...
grupo = tamanhos.index[posicao]
membros = tabela[tabela.grupo == grupo]
print(f"Grupo {grupo}: {len(membros)} imagens, origem: {membros.origem.unique()}")
print(", ".join(membros.imagem))

amostra = membros.head(16)
fig, axes = plt.subplots(4, 4, figsize=(12, 9))
for ax, nome in zip(axes.flat, amostra.imagem):
    ax.imshow(Image.open(PASTA / nome))
    ax.set_title(nome, fontsize=8)
    ax.axis("off")
for ax in axes.flat[len(amostra):]:
    ax.axis("off")
plt.tight_layout()
plt.savefig(SAIDA / f"grupo_{posicao}.png", dpi=70)
print("Figura salva em", SAIDA / f"grupo_{posicao}.png")