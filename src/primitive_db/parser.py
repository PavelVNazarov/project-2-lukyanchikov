# src/primitive_db/parser.py

def parse_condition(condition_str: str) -> dict:
    """
    Парсит условие вида 'age = 28' или 'name = "Sergei"'.
    Поддерживает int, bool, str (в кавычках).
    """
    if '=' not in condition_str:
        raise ValueError("Условие должно содержать '='")
    key, value_str = condition_str.split('=', 1)
    key = key.strip()
    value_str = value_str.strip()

    # Строки в кавычках
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return {key: value_str[1:-1]}

    # Булевы значения
    if value_str.lower() == 'true':
        return {key: True}
    if value_str.lower() == 'false':
        return {key: False}

    # Целые числа
    try:
        return {key: int(value_str)}
    except ValueError:
        pass

    raise ValueError(f"Некорректное значение: {value_str}")

def parse_set_clause(set_str: str) -> dict:
    return parse_condition(set_str)

def parse_where_clause(where_str: str) -> dict:
    return parse_condition(where_str)

