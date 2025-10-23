# Примитивная база данных

Проект: `project#2_lukyanchikov_<ДПО_НОД>`

Исполнитель: Лукьянчиков Валерий  
Группа: <ДПО_НОД>

## Установка и запуск

```bash
make install
make project

ВЫВОД

DB project is running!

**Пример фрагмента:**

```md
## Управление таблицами

Поддерживаемые команды:
- `create_table <имя> <столбец1:тип> ...` — создать таблицу
- `drop_table <имя>` — удалить таблицу
- `list_tables` — показать все таблицы
- `help` — справка
- `exit` — выход

### Пример

```text
>>> create_table users name:str age:int
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int

>>> list_tables
- users

**Пример фрагмента:**

```md
## CRUD-операции

### Команды
- `insert into users values ("Sergei", 28, true)`
- `select from users`
- `select from users where age = 28`
- `update users set age = 29 where name = "Sergei"`
- `delete from users where ID = 1`
- `info users`

### Пример вывода `select`:

+----+--------+-----+-----------+
| ID | name | age | is_active |
+----+--------+-----+-----------+
| 1 | Sergei | 28 | True |
+----+--------+-----+-----------+