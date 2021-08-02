from sws import route


@route(path='/', method='GET')
def foo():
    print('hello world!')


@route(path='/bar', method='GET')
def bar():
    print(f'Message:')
