# some_framework
Реализован MVC фреймоврк.
Возможен рендер шаблонов.
Имеется возможность класть куки и оперировать с ними.
Организовна обработка заполнения и передачи данных по форме.
Возникла потребность в создании объекта Session, чтобы этот объект жил, пока клиент на сервисе.
Не реализована адекватная система аутентификации -> нужно рефакторить код, чтобы сделать хорошо.
Текущие методы для организации авторизации и прихранивания куки на стороне клиента костыльные.


Реализована ORM с CRUD операциями поддерживающая работу с:
  - MySQL
  - PostgreSQL
  - sqlite3

Необходимо создать и заполнить config.py по примеру config.py.default.py;

В директории models создается структура таблицы:

class SomeTable(Model):
_table_name = "some_table"
id: int title: str description: str content: str

В необходимом для проекта месте описываются необходимые для API взаимодействия с таблицей:

def add_some_table(flow):
row = SomeTable()
row['id'] = flow['id']
row['title'] = flow['title']
row['description'] = flow['description']
row['content'] = flow['content']
row.create()

def delete_some_table(condition)
...

Пример взаимодействия с таблицей:

flow = {'id': 45, 'content': 'FOO'} add_some_table(flow)

Создание запроса из терминала:

$ python make_query.py -Q 'SELECT * FROM name_db.some_table;'

