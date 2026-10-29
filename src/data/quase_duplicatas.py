import pandas as pd
import imagehash
from itertools import combinations
import numpy as np

df = pd.read_csv("reports/fase2/estatisticas_imagem.csv", dtype={"hash": str})
hashes = [imagehash.hex_to_hash(h) for h in df["hash"]]

pares = []
for i, j in combinations(range(len(df)), 2):
    d = hashes[i] - hashes[j]          # distância de Hamming
    if d <= 8:
        pares.append({
            "img_a": df.imagem[i], "origem_a": df.origem[i],
            "img_b": df.imagem[j], "origem_b": df.origem[j],
            "distancia": d,
        })

pares = pd.DataFrame(pares)

pares.to_csv("reports/fase2/quase_duplicatas.csv", index=False)
print(len(pares), "pares com distância <= 8")
print(pares.groupby(["origem_a", "origem_b"]).size())
print(pares.sort_values("distancia").head(15))

normais = df[df.origem == "Normal_Insulators"].copy()
normais["num"] = normais.imagem.str.replace(".jpg", "").astype(int)
normais = normais.sort_values("num").reset_index(drop=True)
h = [imagehash.hex_to_hash(x) for x in normais.hash]

vizinhos = [h[i] - h[i + 1] for i in range(len(h) - 1)]
rng = np.random.default_rng(42)
aleatorios = [h[i] - h[j] for i, j in rng.integers(0, len(h), size=(2000, 2)) if i != j]

print("distância mediana entre vizinhos:", np.median(vizinhos))
print("distância mediana entre pares aleatórios:", np.median(aleatorios))
print("vizinhos com distância <= 16:", sum(d <= 16 for d in vizinhos), "de", len(vizinhos))