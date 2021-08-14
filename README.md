Реализована ORM с CRUD операциями поддерживающая работу с базами данных:
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
class Article(Model):
    _table_name = "some_table"
    id: int 
    title: str 
    description: str 
    content: str
```


- В директории проекта описываются необходимые для API взаимодействия с таблицей:
```python
from models.Article import Article
from orm_core.Conditions import QFilter

def add_article(flow):
    article = Article()
    article['id'] = flow['id']
    article['title'] = flow['title']
    article['description'] = flow['description']
    article['content'] = flow['content']
    article.create()


def get_article(condition):
    article = Article()
    article.condition = condition
    return article.read()
    
def delete_article(condition):
    article = Article()
    article.condition = condition
    article.delete()

def update_article(set_update, condition):
    article = Article()
    article.set_update = set_update
    article.condition = condition
    article.update()

def read_by_one_id(model_id):
    article = Article()
    return article.read_by_one_id(model_id=model_id)
```


Пример взаимодействия с таблицей:
```python
# Create
flow = {'id': 45, 'content': 'FOO'} 
add_some_table(flow)
# Read
get_article(QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
# Update
update_article(set_update=QFilter().add_k('title').eq().add_v('AARRRGH').condition,
                   condition=QFilter().add_k('id').eq().add_v(45).condition)
# Delete
delete_article(condition=QFilter().add_k('id').eq().add_v(1).condition)

# Пример запроса по id:
read_by_one_id(45)
```
Создание запроса из терминала:
```
$ python make_query.py -Q 'SELECT * FROM name_db.some_table;'
```
