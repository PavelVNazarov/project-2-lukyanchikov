# src/primitive_db/utils.py

import json
from pathlib import Path

DB_META_FILE = "db_meta.json"
DATA_DIR = "data"

Path(DATA_DIR).mkdir(exist_ok=True)

def load_metadata(filepath: str = DB_META_FILE) -> dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except FileNotFoundError:
        return {}

def save_metadata(metadata: dict, filepath: str = DB_META_FILE) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def load_table_data(table_name: str) -> list:
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []

def save_table_data(table_name: str, data: list) -> None:
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

