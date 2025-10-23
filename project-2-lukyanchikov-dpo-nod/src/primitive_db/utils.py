# src/primitive_db/utils.py

import json
from pathlib import Path

DB_META_FILE = "db_meta.json"

def load_metadata(filepath: str = DB_META_FILE) -> dict:
    """Загружает метаданные из JSON-файла. Возвращает {} если файл не найден."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata( dict, filepath: str = DB_META_FILE) -> None:
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
