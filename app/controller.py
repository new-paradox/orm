from random import randint
from http.cookies import SimpleCookie

from sws import route, render
from models.users import Users
from models.auth_key import AuthKey
from orm_core.Conditions import QFilter
import logging
from functools import wraps

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def add_users(flow):
    row = Users()
    row['username'] = flow['username']
    row['password'] = flow['password']
    row.create()


def add_auth_key(flow):
    row = AuthKey()
    row['cookie'] = flow['cookie']
    row['username'] = flow['username']
    row.create()


class Authentication:
    pass


def auth(fu):
    # TODO: обернуть ф-ю маршрутизатора
    #  если что-то - возвращать функцию
    #  иначе - шаблонный ответ в виде страницы авторизации
    # def decorator(func):
    #     @wraps(func)
    #     def wrapper(*args, **kwargs):
    #         return func(*args, **kwargs)
    #     return fu

    return fu


def get_user(condition):
    """

    :param condition: (QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    """

    row = Users()
    row.condition = condition
    return row.read()


def get_auth_key(k):
    print('может я в get_auth_key')
    print(f'это ключ его распарсить {k}')
    row = AuthKey()
    row.condition = QFilter().add_k('cookie').eq().add_v(f'{k}').condition
    res = row.read()
    print(f' query db: {res} and type: {type(res)}')
    return res


def get_cookie(rawdata):
    cookie = SimpleCookie()
    cookie.load(rawdata)
    cookies = {}
    if len(cookie) > 0:
        for key, morsel in cookie.items():
            cookies[key] = morsel.value
        if cookies.get('auth_key'):
            return cookies['auth_key']


def login(request) -> bool:
    cook_keys = get_cookie(request.headers['Cookie'])
    # запрашиваем ключ из бд
    if cook_keys and get_auth_key(cook_keys)[0][1] == cook_keys:
        return True
    else:
        return False


@auth
@route(path='/index', method='GET')
@route(path='/', method='GET')
def index(request):
    print('я в индексе и ниже запрос:')
    # return '<form action="/add_user" method="post" enctype="multipart/form-data"><p><input type="text" name="text" value="Как звать-та?"><button type="submit">Submit</button></form>'
    return render('index.html')
    # return render('/home/avail/PycharmProjects/some_framework/app/templates/index.html')


@auth
@route(path='/get_auth', method='GET')
def get_auth(request):
    print('я в get_auth:')
    return render('login.html')

# @route(path='/auth', method='POST')
# def auth(request):
#     print('я в auth и ниже запрос:')
#     # name = request.get_content['text'][0]
#     # coockie = request.headers['Cookie']
#
#     print(request.headers['Cookie'])
#     # TODO: 1. научиться смотреть кукисы
#     # TODO: 2. научиться класть кукисы в директорю браузеров chrome и firefox
#     #  тут типа авторизовались, генерится ключ, ключ кладется в бд к соответсвии с пользаком
#     #  и кладется в кукисы в ответ
#
#
#     """
#     Cookies
#     6. Проверяю наличие этих параметров в куках
#     Если их там нет, модифицирую булевый флаг
#     обновляю атрибут request.rcookies
#     """
#     print(f'obj in route {request.rcookies}')
#     request.rcookies.set_cookies = False
#     if 'some_key=123355' not in request.rcookies.cookies:
#         request.rcookies.set_cookies = True
#         # request.cookies_modyficate = True
#         print(f'in route {request.rcookies.cookies}')
#         request.rcookies.cookies = [('Set-cookie', 'some_key=123355')]
#     return index(request)

#
# @route(path='/reg', method='POST')
# def register(request):
#
#     return render('index.html')


# @route(path='/auth', method='POST')
# def auth(request):
#     print('я в auth и ниже запрос:')
#     # name = request.get_content['text'][0]
#     # coockie = request.headers['Cookie']
#
#     print(request.headers['Cookie'])
#     request.rcookies.set_cookies = False
#     if 'auth_key=sdfsf43' not in request.rcookies.cookies:
#         request.rcookies.set_cookies = True
#         request.rcookies.cookies = [('Set-cookie', 'auth_key=sdfsf43')]
#
#     return render('index.html')


# @route(path='/new_row', method='GET')
# def create_row(request):
#     if login(request):
#         print('я в индексе и ниже запрос:')
#         return render('create.html')
#     else:
#         get_auth(request)
