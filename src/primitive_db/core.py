# src/primitive_db/core.py

import ast
import os
from typing import Any, Optional, List
from prettytable import PrettyTable
from .utils import load_table_data, save_table_data

SUPPORTED_TYPES = {'int', 'str', 'bool'}

def _cast_value(value: Any, target_type: str) -> Any:
    if target_type == 'int':
        return int(value)
    elif target_type == 'bool':
        return bool(value)
    elif target_type == 'str':
        return str(value)
    else:
        raise ValueError(f"Неизвестный тип: {target_type}")

def _validate_and_cast_values(schema: List[str], raw_values: List[str]) -> dict:
    """Валидация и приведение типов значений для вставки."""
    expected_cols = schema[1:]  # пропускаем ID:int
    if len(raw_values) != len(expected_cols):
        raise ValueError(f"Ожидалось {len(expected_cols)} значений, получено {len(raw_values)}")

    record = {"ID": None}
    for col_def, val in zip(expected_cols, raw_values):
        name, typ = col_def.split(':', 1)
        try:
            parsed_val = ast.literal_eval(val)
        except (ValueError, SyntaxError):
            parsed_val = val
        casted = _cast_value(parsed_val, typ)
        record[name] = casted
    return record

def create_table(metadata, table_name: str, columns: list[str]) -> dict:
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = []
    for col in columns:
        if ':' not in col:
            print(f'Некорректное значение: {col}. Попробуйте снова.')
            return metadata
        name, typ = col.split(':', 1)
        if typ not in SUPPORTED_TYPES:
            print(f'Некорректное значение: {col}. Поддерживаемые типы: int, str, bool.')
            return metadata
        parsed_columns.append(f"{name}:{typ}")

    full_columns = ["ID:int"] + parsed_columns
    metadata[table_name] = full_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(full_columns)}')
    return metadata

def drop_table(metadata, table_name: str) -> dict:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    del metadata[table_name]
    data_file = f"data/{table_name}.json"
    if os.path.exists(data_file):
        os.remove(data_file)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata: dict) -> None:
    if not metadata:
        print("Нет таблиц.")
    else:
        for name in metadata:
            print(f"- {name}")

# === CRUD ===

def insert(metadata, table_name: str, raw_values: List[str]) -> None:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    schema = metadata[table_name]
    try:
        record = _validate_and_cast_values(schema, raw_values)
    except Exception as e:
        print(f"Ошибка валидации: {e}")
        return

    table_data = load_table_data(table_name)
    new_id = max((r["ID"] for r in table_data), default=0) + 1
    record["ID"] = new_id
    table_data.append(record)
    save_table_data(table_name, table_data)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

def select(table_name: str, metadata, where_clause: Optional[dict] = None) -> None:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = load_table_data(table_name)
    schema = metadata[table_name]
    col_names = [col.split(':')[0] for col in schema]

    if where_clause:
        key, value = next(iter(where_clause.items()))
        table_data = [r for r in table_data if r.get(key) == value]

    if not table_data:
        print("Нет записей.")
        return

    pt = PrettyTable()
    pt.field_names = col_names
    for row in table_data:
        pt.add_row([row.get(col, "") for col in col_names])
    print(pt)

def update(metadata: dict, table_name: str, set_clause: dict, where_clause: dict) -> None:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    table_data = load_table_data(table_name)
    schema_dict = {col.split(':')[0]: col.split(':')[1] for col in metadata[table_name]}

    set_key, set_value = next(iter(set_clause.items()))
    if set_key not in schema_dict:
        print(f'Ошибка: Столбец "{set_key}" не существует в таблице "{table_name}".')
        return
    try:
        set_value = _cast_value(set_value, schema_dict[set_key])
    except Exception as e:
        print(f"Ошибка приведения типа: {e}")
        return

    where_key, where_value = next(iter(where_clause.items()))
    updated = False
    for record in table_data:
        if record.get(where_key) == where_value:
            record[set_key] = set_value
            updated = True
            print(f'Запись с ID={record["ID"]} в таблице "{table_name}" успешно обновлена.')
    if not updated:
        print("Не найдено записей для обновления.")
    if updated:
        save_table_data(table_name, table_data)

def delete(table_name: str, where_clause: dict) -> None:
    table_data = load_table_data(table_name)
    where_key, where_value = next(iter(where_clause.items()))
    before_len = len(table_data)
    table_data = [r for r in table_data if r.get(where_key) != where_value]
    after_len = len(table_data)
    if before_len == after_len:
        print("Не найдено записей для удаления.")
    else:
        deleted_count = before_len - after_len
        save_table_data(table_name, table_data)
        print(f"Удалено {deleted_count} записей из таблицы \"{table_name}\".")

def info(metadata: dict, table_name: str) -> None:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    schema = metadata[table_name]
    table_data = load_table_data(table_name)
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(schema)}")
    print(f"Количество записей: {len(table_data)}")
