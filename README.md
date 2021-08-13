Реализована ORM с CRUD операциями поддерживающая работу с:
  1. MySQL
  2. PostgreSQL
  3. sqlite3



- Необходимо создать и заполнить:
```python
config.py 
```
- по примеру:
```python
config.py.default.py
```
- В поле DB_DRIVER указать на выбор: psql, mysql или sqlite
- каталог orm пометить как sources

В директории models создается структура таблицы:
```python
class SomeTable(Model):
    _table_name = "some_table"
    id: int 
    title: str 
    description: str 
    content: str
```


- В директории проекта описываются необходимые для API взаимодействия с таблицей:
```python
from models.Article import SomeTable
from orm_core.Conditions import QFilter

def add_some_table(flow):
    row = SomeTable()
    row['id'] = flow['id']
    row['title'] = flow['title']
    row['description'] = flow['description']
    row['content'] = flow['content']
    row.create()


def get_article(condition):
    row = SomeTable()
    row.condition = condition
    return row.read()
    

def delete_article(condition):
    row = SomeTable()
    row.condition = condition
    row.delete()

def update_article(set_update, condition):
    row = SomeTable()
    row.set_update = set_update
    row.condition = condition
    row.update()

def read_by_one_id(model_id):
    row = SomeTable()
    return row.read_by_one_id(model_id=model_id)
```


Пример взаимодействия с таблицей:
```python
# SELECT
get_article(QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
# INSERT
flow = {'id': 45, 'content': 'FOO'} 
add_some_table(flow)
# UPDATE
update_article(set_update=QFilter().add_k('title').eq().add_v('AARRRGH').condition,
                   condition=QFilter().add_k('id').eq().add_v(45).condition)
# DELETE
delete_article(condition=QFilter().add_k('id').eq().add_v(1).condition)

# Пример SELECT запроса с запросом id строки:
read_by_one_id(45)
```
Создание запроса из терминала:
```
$ python make_query.py -Q 'SELECT * FROM name_db.some_table;'
```
