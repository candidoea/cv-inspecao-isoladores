from pathlib import Path
import shutil
import pandas as pd

RAIZ = Path("data/raw/cplid")
DESTINO = Path("data/interim")
CLASSES = {"insulator": 0, "defect": 1}
DUPLICATAS = {"2984.jpg", "1876.jpg", "1938.jpg"}      # achado 7: cópia removida

df = pd.read_csv("reports/fase2/anotacoes.csv", dtype={"imagem": str})
df = df[~df.imagem.isin(DUPLICATAS)]

(DESTINO / "images").mkdir(parents=True, exist_ok=True)
(DESTINO / "labels").mkdir(parents=True, exist_ok=True)

for (origem, imagem), caixas in df.groupby(["origem", "imagem"]):
    shutil.copy(RAIZ / origem / "images" / imagem, DESTINO / "images" / imagem)

    linhas_txt = []
    for _, c in caixas.iterrows():
        cx = (c.xmin + c.xmax) / 2 / c.largura_img
        cy = (c.ymin + c.ymax) / 2 / c.altura_img
        bw = (c.xmax - c.xmin) / c.largura_img
        bh = (c.ymax - c.ymin) / c.altura_img
        linhas_txt.append(f"{CLASSES[c.classe]} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

    nome_txt = Path(imagem).stem + ".txt"
    (DESTINO / "labels" / nome_txt).write_text("\n".join(linhas_txt))

print(len(list((DESTINO / "images").glob("*.jpg"))), "imagens convertidas")