import shlex
from core import create_table, drop_table, list_tables
from utils import load_metadata, save_metadata

def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("***База данных***")
    print_help()
    while True:
        try:
            user_input = input(">>>Введите команду: ").strip()
            if not user_input:
                continue
            args = shlex.split(user_input)
            command = args[0]
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
            else:
                print(f"Функции {command} нет. Попробуйте снова.")
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы.")
            break
        except ValueError as e:
            print(f"Некорректный ввод: {e}")

