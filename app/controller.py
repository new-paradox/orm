from sws import route
from models.users import Users
from orm_core.Conditions import QFilter
import logging
from jinja2 import Template, Environment, FileSystemLoader
from config import TEMPLATES

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


def render(html_file):
    print('работат')
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template(html_file)
    output_from_parsed_template = template.render()
    print(output_from_parsed_template)
    return output_from_parsed_template


@route(path='/index', method='GET')
@route(path='/', method='GET')
def index(request):
    print('я в индексе и ниже запрос:')
    # return '<form action="/add_user" method="post" enctype="multipart/form-data"><p><input type="text" name="text" value="Как звать-та?"><button type="submit">Submit</button></form>'
    return render('index.html')
    # return render('/home/avail/PycharmProjects/some_framework/app/templates/index.html')


@route(path='/get_auth', method='GET')
def get_auth(request):
    print('я в add_user и ниже запрос:')
    # name = request.get_content['text'][0]
    # return f'<form action="/auth" method="post" enctype="multipart/form-data"><p><input type="text" name="text" value="Как звать-та?"><button type="submit">Submit</button></form>'
    return render('about.html')


@route(path='/auth', method='GET')
def auth(request):
    print('я в add_user и ниже запрос:')
    # name = request.get_content['text'][0]
    return render('create.html')
    # return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><h1>Его звали {get_user(QFilter().add_k("name").eq().add_v(name).condition)} и он устал :( </h1></body></html>'
