from pathlib import Path
import cv2
import pandas as pd
from PIL import Image
import imagehash

RAIZ = Path("data/raw/cplid")
linhas = []

for origem in ["Normal_Insulators", "Defective_Insulators"]:
    pasta = RAIZ / origem / "images"
    for caminho in pasta.glob("*.jpg"):
        img = cv2.imread(str(caminho))
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        brilho = cinza.mean()
        nitidez = cv2.Laplacian(cinza, cv2.CV_64F).var()
        tamanho_kb = caminho.stat().st_size / 1024
        hash_img = str(imagehash.phash(Image.open(caminho)))

        linhas.append({
            "origem": origem,
            "imagem": caminho.name,
            "brilho": brilho,
            "nitidez": nitidez,
            "tamanho_kb": tamanho_kb,
            "hash": hash_img,
        })

df = pd.DataFrame(linhas)
repetidos = df.groupby("hash")["imagem"].count()
print("hashes repetidos:", (repetidos > 1).sum())
print(df[df["hash"].isin(repetidos[repetidos > 1].index)].sort_values("hash").head(20))
df.to_csv("reports/fase2/estatisticas_imagem.csv", index=False)
print(df.groupby("origem")[["brilho", "nitidez", "tamanho_kb"]].describe().T)