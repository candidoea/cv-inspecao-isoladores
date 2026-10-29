from pathlib import Path
import fiftyone as fo

PASTA = Path("data/interim")
NOMES = {0: "isolador", 1: "defeito"}

amostras = []
for img in sorted((PASTA / "images").glob("*.jpg")):
    rotulo = PASTA / "labels" / (img.stem + ".txt")
    deteccoes = []
    for linha in rotulo.read_text().splitlines():
        classe, cx, cy, w, h = linha.split()
        cx, cy, w, h = float(cx), float(cy), float(w), float(h)
        deteccoes.append(fo.Detection(
            label=NOMES[int(classe)],
            bounding_box=[cx - w / 2, cy - h / 2, w, h],   # FiftyOne usa canto superior esquerdo
        ))
    amostra = fo.Sample(filepath=str(img.resolve()))
    amostra["ground_truth"] = fo.Detections(detections=deteccoes)
    amostra["origem"] = "defeito" if len(img.stem) == 3 else "normal"
    amostras.append(amostra)

ds = fo.Dataset("cplid_interim", overwrite=True)
ds.add_samples(amostras)
print(ds)
sessao = fo.launch_app(ds)
sessao.wait()