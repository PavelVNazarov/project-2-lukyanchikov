# src/primitive_db/core.py

SUPPORTED_TYPES = {'int', 'str', 'bool'}

def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict:
    """Создаёт новую таблицу в метаданных."""
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

    # Автоматически добавляем ID:int
    full_columns = ["ID:int"] + parsed_columns
    metadata[table_name] = full_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(full_columns)}')
    return metadata

def drop_table(metadata, table_name: str) -> dict:
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata) -> None:
    """Выводит список всех таблиц."""
    if not metadata:
        print("Нет таблиц.")
    else:
        for name in metadata:
            print(f"- {name}")