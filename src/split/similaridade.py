from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torchvision import models

PASTA = Path("data/interim/images")
SAIDA = Path("reports/fase3")
SAIDA.mkdir(parents=True, exist_ok=True)

# 1. a rede pré-treinada, sem a última camada (a que classifica as 1000 classes do ImageNet)
pesos = models.ResNet18_Weights.IMAGENET1K_V1
rede = models.resnet18(weights=pesos)
rede.fc = torch.nn.Identity()
rede.eval()
preparar = pesos.transforms()          # redimensiona e normaliza como no treino da rede

# 2. um embedding de 512 números por imagem
imagens = sorted(PASTA.glob("*.jpg"))
embeddings = []
with torch.no_grad():                  # só inferência: não guarda gradientes
    for i, caminho in enumerate(imagens):
        x = preparar(Image.open(caminho).convert("RGB")).unsqueeze(0)
        embeddings.append(rede(x).squeeze(0).numpy())
        if i % 100 == 0:
            print(f"{i}/{len(imagens)}")

E = np.array(embeddings)
E = E / np.linalg.norm(E, axis=1, keepdims=True)   # normalizar: o produto vira cosseno
sim = E @ E.T                                       # matriz 845 x 845 de similaridades
np.fill_diagonal(sim, 0)                            # ignora cada imagem com ela mesma

# 3. os pares mais parecidos
nomes = [c.name for c in imagens]
origem = ["defeito" if len(Path(n).stem) == 3 else "normal" for n in nomes]
i, j = np.triu_indices(len(nomes), k=1)
pares = pd.DataFrame({
    "img_a": np.array(nomes)[i], "origem_a": np.array(origem)[i],
    "img_b": np.array(nomes)[j], "origem_b": np.array(origem)[j],
    "similaridade": sim[i, j],
}).sort_values("similaridade", ascending=False)

pares.head(200).to_csv(SAIDA / "pares_similares.csv", index=False)
np.save(SAIDA / "embeddings.npy", E)

print(pares.head(15).to_string(index=False))
print("\nPares com similaridade >= 0,90 por combinação de origens:")
print(pares[pares.similaridade >= 0.90].groupby(["origem_a", "origem_b"]).size())