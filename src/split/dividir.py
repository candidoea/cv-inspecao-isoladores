from pathlib import Path
import shutil

import numpy as np
import pandas as pd

ORIGEM_DADOS = Path("data/interim")
DESTINO = Path("data/processed")
GRUPOS = Path("reports/fase3/grupos.csv")
PROPORCAO = {"test": 0.15, "val": 0.15}
SEMENTE = 42

tabela = pd.read_csv(GRUPOS, dtype={"imagem": str})
tabela["conjunto"] = "train"
rng = np.random.default_rng(SEMENTE)

for origem, parte in tabela.groupby("origem"):
    tamanhos = parte.groupby("grupo").size()
    pequenos = tamanhos[tamanhos <= 5].index.to_numpy().copy()
    rng.shuffle(pequenos)                       # ordem aleatória, mas reproduzível

    total = len(parte)
    alvo = {nome: round(total * p) for nome, p in PROPORCAO.items()}
    contagem = {nome: 0 for nome in PROPORCAO}

    for g in pequenos:
        for nome in ("test", "val"):            # enche o teste primeiro, depois a validação
            if contagem[nome] + tamanhos[g] <= alvo[nome]:
                tabela.loc[(tabela.origem == origem) & (tabela.grupo == g), "conjunto"] = nome
                contagem[nome] += tamanhos[g]
                break                           # o grupo foi alocado; vai para o próximo

# teste de vazamento: nenhum grupo pode aparecer em dois conjuntos
conjuntos_por_grupo = tabela.groupby("grupo")["conjunto"].nunique()
assert (conjuntos_por_grupo == 1).all(), "VAZAMENTO: há grupo dividido entre conjuntos"
assert not tabela.imagem.duplicated().any(), "imagem repetida na tabela"

# resumo da divisão
resumo = pd.crosstab(tabela.conjunto, tabela.origem, margins=True, margins_name="total")
resumo["% com defeito"] = (100 * resumo["defeito"] / resumo["total"]).round(1)
print(resumo)

# cópia dos arquivos para a estrutura que o YOLO espera
for _, linha in tabela.iterrows():
    stem = Path(linha.imagem).stem
    for tipo, ext in (("images", ".jpg"), ("labels", ".txt")):
        pasta = DESTINO / linha.conjunto / tipo
        pasta.mkdir(parents=True, exist_ok=True)
        shutil.copy(ORIGEM_DADOS / tipo / (stem + ext), pasta / (stem + ext))

# arquivo de dataset para a Ultralytics, com caminho absoluto desta máquina (fica fora do Git)
(DESTINO / "cplid.yaml").write_text(
    f"path: {DESTINO.resolve().as_posix()}\n"
    "train: train/images\nval: val/images\ntest: test/images\n"
    "names:\n  0: isolador\n  1: defeito\n",
    encoding="utf-8",
)

tabela.to_csv("configs/split.csv", index=False)
print("\nDivisão salva em configs/split.csv e arquivos copiados para", DESTINO)