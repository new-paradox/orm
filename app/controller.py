from http.cookies import BaseCookie, SimpleCookie
from http import cookies
from sws import route, render
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
    # return '<form action="/add_user" method="post" enctype="multipart/form-data"><p><input type="text" name="text" value="Как звать-та?"><button type="submit">Submit</button></form>'
    return render('index.html')
    # return render('/home/avail/PycharmProjects/some_framework/app/templates/index.html')


@route(path='/get_auth', method='GET')
def get_auth(request):
    print('я в get_auth:')
    # name = request.get_content['text'][0]
    # return f'<form action="/auth" method="post" enctype="multipart/form-data"><p><input type="text" name="text" value="Как звать-та?"><button type="submit">Submit</button></form>'
    return render('login.html')


@route(path='/auth', method='POST')
def auth(request):
    print('я в auth и ниже запрос:')
    # name = request.get_content['text'][0]
    # coockie = request.headers['Cookie']

    print(request.headers['Cookie'])
    # TODO: 1. научиться смотреть кукисы
    # TODO: 2. научиться класть кукисы в директорю браузеров chrome и firefox
    #  тут типа авторизовались, генерится ключ, ключ кладется в бд к соответсвии с пользаком
    #  и кладется в кукисы в ответ


    """
    Cookies
    6. Проверяю наличие этих параметров в куках
    Если их там нет, модифицирую булевый флаг
    обновляю атрибут request.rcookies 
    """
    print(f'obj in route {request.rcookies}')
    request.rcookies.set_cookies = False
    if 'some_key=123355' not in request.rcookies.cookies:
        request.rcookies.set_cookies = True
        # request.cookies_modyficate = True
        print(f'in route {request.rcookies.cookies}')
        request.rcookies.cookies = [('Set-cookie', 'some_key=123355')]











    # TODO: 3. реализовать алгоритм ниже

    # TODO: Чекаем кукис на предмет ключа
    # TODO: если ключ есть:
    # TODO:     пускаем на страничку которую декоратор обернул
    # TODO: иначе:
    # TODO:     пусть идет на страницу аутентификации
    # TODO:     вариативность возврата страниц вошел/нет
    # TODO:     проверка если вошел ->
    # TODO:         запиши клиенту кукис с токеном/ключом
    # TODO:         верни страничку под декоратором (пока не декоратор - только одну)
    # TODO:     иначе:
    # TODO:         верни страничку с ошибкой аутентификации и заставь попробовать еще раз
    return render('create.html')
    # return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><h1>Его звали {get_user(QFilter().add_k("name").eq().add_v(name).condition)} и он устал :( </h1></body></html>'
