# src/primitive_db/engine.py

import shlex
from .core import (
    create_table, drop_table, list_tables,
    insert, select, update, delete, info
)
from .utils import load_metadata, save_metadata
from .parser import parse_set_clause, parse_where_clause

def print_help() -> None:
    print("\n***Операции с данными***")
    print("Функции:")
    print("insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись")
    print("select from <имя_таблицы> - прочитать все записи")
    print("select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию")
    print("update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение> - обновить запись")
    print("delete from <имя_таблицы> where <столбец> = <значение> - удалить запись")
    print("info <имя_таблицы> - вывести информацию о таблице")
    print("\nУправление таблицами:")
    print("create_table <имя> <столбец1:тип> ... - создать таблицу")
    print("drop_table <имя> - удалить таблицу")
    print("list_tables - показать список всех таблиц")
    print("\nОбщие команды:")
    print("exit - выход из программы")
    print("help - справочная информация\n")

def run() -> None:
    print("***База данных***")
    print_help()
    while True:
        try:
            user_input = input(">>>Введите команду: ").strip()
            if not user_input:
                continue
            args = shlex.split(user_input)
            command = args[0].lower()
            metadata = load_metadata()

            if command == "exit":
                break
            elif command == "help":
                print_help()
            elif command == "list_tables":
                list_tables(metadata)
            elif command == "create_table":
                if len(args) < 3:
                    print("Некорректное значение: недостаточно аргументов.")
                    continue
                table_name = args[1]
                columns = args[2:]
                metadata = create_table(metadata, table_name, columns)
                save_metadata(metadata)
            elif command == "drop_table":
                if len(args) != 2:
                    print("Некорректное значение: укажите имя таблицы.")
                    continue
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(metadata)
            elif command == "info":
                if len(args) != 2:
                    print("Некорректное значение: укажите имя таблицы.")
                    continue
                info(metadata, args[1])
            elif command == "insert" and len(args) >= 4 and args[1] == "into" and args[3] == "values":
                table_name = args[2]
                values_str = user_input.split("values", 1)[1].strip()
                if not (values_str.startswith('(') and values_str.endswith(')')):
                    print("Некорректный синтаксис: значения должны быть в скобках.")
                    continue
                values_str = values_str[1:-1]
                try:
                    values = [v.strip() for v in values_str.split(',')]
                except Exception:
                    print("Ошибка разбора значений.")
                    continue
                insert(metadata, table_name, values)
            elif command == "select" and len(args) >= 3 and args[1] == "from":
                table_name = args[2]
                if len(args) == 3:
                    select(table_name, metadata)
                elif len(args) == 6 and args[3] == "where":
                    where_part = f"{args[4]} = {args[5]}"
                    try:
                        where_clause = parse_where_clause(where_part)
                        select(table_name, metadata, where_clause)
                    except Exception as e:
                        print(f"Ошибка парсинга условия: {e}")
                else:
                    print("Некорректный синтаксис команды select.")
            elif command == "update" and len(args) >= 8 and args[2] == "set" and args[4] == "where":
                table_name = args[1]
                set_part = f"{args[3]} = {args[5]}"
                where_part = f"{args[6]} = {args[7]}"
                try:
                    set_clause = parse_set_clause(set_part)
                    where_clause = parse_where_clause(where_part)
                    update(metadata, table_name, set_clause, where_clause)
                except Exception as e:
                    print(f"Ошибка парсинга: {e}")
            elif command == "delete" and len(args) >= 4 and args[1] == "from" and args[3] == "where":
                table_name = args[2]
                where_part = f"{args[4]} = {args[5]}"
                try:
                    where_clause = parse_where_clause(where_part)
                    delete(table_name, where_clause)
                except Exception as e:
                    print(f"Ошибка парсинга условия: {e}")
            else:
                print(f"Функции {command} нет. Попробуйте снова.")
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
