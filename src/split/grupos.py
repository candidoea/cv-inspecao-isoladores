from pathlib import Path

import numpy as np
import pandas as pd

PASTA = Path("data/interim/images")
SAIDA = Path("reports/fase3")

E = np.load(SAIDA / "embeddings.npy")
nomes = [c.name for c in sorted(PASTA.glob("*.jpg"))]
origem = ["defeito" if len(Path(n).stem) == 3 else "normal" for n in nomes]
sim = E @ E.T


def formar_grupos(limiar):
    """Cada imagem começa sozinha; imagens com similaridade >= limiar entram no mesmo grupo."""
    grupo = list(range(len(nomes)))           # cada imagem aponta para o "chefe" do seu grupo

    def chefe(a):
        while grupo[a] != a:
            a = grupo[a]
        return a

    i, j = np.where(np.triu(sim, k=1) >= limiar)
    for a, b in zip(i, j):
        grupo[chefe(a)] = chefe(b)            # une os dois grupos
    return [chefe(a) for a in range(len(nomes))]


for limiar in (0.90, 0.92, 0.94):
    g = pd.Series(formar_grupos(limiar))
    tamanhos = g.value_counts()
    print(f"limiar {limiar:.2f}: {len(tamanhos)} grupos | "
          f"sozinhas {(tamanhos == 1).sum()} | maior grupo {tamanhos.max()} imagens | "
          f"grupos com mais de 5: {(tamanhos > 5).sum()}")

LIMIAR = 0.92
tabela = pd.DataFrame({"imagem": nomes, "origem": origem, "grupo": formar_grupos(LIMIAR)})
mistos = tabela.groupby("grupo")["origem"].nunique()
print(f"\nCom limiar {LIMIAR}: {(mistos > 1).sum()} grupos misturam as duas origens")
print(tabela.groupby("grupo").size().sort_values(ascending=False).head(10))
tabela.to_csv(SAIDA / "grupos.csv", index=False)