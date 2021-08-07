# TODO: весь import, кроме route, перетянуть на темную сторону фреймворка
from sws import route
from models.users import Users
from orm_core.Conditions import QFilter
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def add_users(flow):
    row = Users()
    row['name'] = flow['name']
    row['age'] = flow['age']
    row['city'] = flow['city']
    row.create()


def get_user(condition):
    """

    :param condition: (QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    """

    row = Users()
    row.condition = condition
    return row.read()


@route(path='/index', method='GET')
@route(path='/', method='GET')
def index(request):
    print('я в индексе и ниже запрос:')
    return '<form action="/add_user" method="post" enctype="multipart/form-data"><p><input type="text" name="text" value="Как звать-та?"><button type="submit">Submit</button></form>'


@route(path='/add_user', method='POST')
def auth(request):
    print('я в add_user и ниже запрос:')
    name = request.content['text'][0]
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><h1>Его звали {get_user(QFilter().add_k("name").eq().add_v(name).condition)} и он устал :( </h1></body></html>'
