import json
from pathlib import Path


def load_config(filename: str) -> dict:
    """Carrega um arquivo de configuração JSON do diretório config."""
    path = Path(__file__).resolve().parent / filename
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração '{filename}' não encontrado.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
