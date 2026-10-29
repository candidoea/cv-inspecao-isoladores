from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

RAIZ = Path("data/raw/cplid")
xmls = list(RAIZ.rglob("*.xml"))
print(len(xmls), "arquivos XML encontrados")

linhas = []
for caminho_xml in xmls:
    raiz = ET.parse(caminho_xml).getroot()
    w = int(raiz.find("size/width").text)
    h = int(raiz.find("size/height").text)
    origem = caminho_xml.relative_to(RAIZ).parts[0]      # Normal_Insulators ou Defective_Insulators
    imagem = caminho_xml.stem + ".jpg"

    for obj in raiz.findall("object"):
        bb = obj.find("bndbox")
        xmin = float(bb.find("xmin").text)
        ymin = float(bb.find("ymin").text)
        xmax = float(bb.find("xmax").text)
        ymax = float(bb.find("ymax").text)
        linhas.append({
            "origem": origem,
            "arquivo_xml": caminho_xml.name,
            "imagem": imagem,
            "classe": obj.find("name").text,
            "largura_img": w,
            "altura_img": h,
            "area_rel": (xmax - xmin) * (ymax - ymin) / (w * h),
            "xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax,
        })

df = pd.DataFrame(linhas)

saida = Path("reports/fase2")
saida.mkdir(parents=True, exist_ok=True)
df.to_csv(saida / "anotacoes.csv", index=False)

# pergunta 2: caixas por imagem
print(df.groupby(["origem", "imagem"]).size().groupby("origem").describe())

# pergunta 4: tamanho relativo das caixas
print(df.groupby(["origem", "classe"])["area_rel"].describe())

# pergunta 5: caixas inválidas
invalidas = df[(df.xmax <= df.xmin) | (df.ymax <= df.ymin) |
               (df.xmin < 0) | (df.ymin < 0) |
               (df.xmax > df.largura_img) | (df.ymax > df.altura_img)]
print("caixas inválidas:", len(invalidas))


print(df.groupby(["origem", "classe"]).size())
print("imagens distintas por origem:")
print(df.groupby("origem")["imagem"].nunique())
print(df.drop_duplicates("imagem").groupby("origem")[["largura_img", "altura_img"]].value_counts())
