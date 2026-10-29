import argparse
import json
import subprocess
from pathlib import Path

import torch
import ultralytics
import yaml
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument("config", help="arquivo YAML do experimento")
parser.add_argument("--epochs", type=int, help="sobrescreve as épocas (ex.: 1 para teste rápido)")
parser.add_argument("--nome", help="sobrescreve o nome do experimento")
args = parser.parse_args()

cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
if args.epochs:
    cfg["epochs"] = args.epochs
if args.nome:
    cfg["nome"] = args.nome

modelo = YOLO(cfg["modelo"])
modelo.train(
    data=cfg["dados"],
    epochs=cfg["epochs"],
    imgsz=cfg["imgsz"],
    batch=cfg["batch"],
    patience=cfg["patience"],
    seed=cfg["seed"],
    cache=cfg.get("cache", False),
    project=str(Path("runs").resolve()),   # caminho absoluto: sem pasta extra
    name=cfg["nome"],
    exist_ok=False,
)

pasta = Path(modelo.trainer.save_dir)      # onde a biblioteca de fato salvou
commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
registro = {
    "config": cfg,
    "arquivo_config": args.config,
    "commit": commit,
    "ultralytics": ultralytics.__version__,
    "torch": torch.__version__,
    "dispositivo": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    "pasta": str(pasta),
}
(pasta / "registro.json").write_text(json.dumps(registro, indent=2, ensure_ascii=False), encoding="utf-8")
print("\nRegistro salvo em", pasta / "registro.json")