from sws import route



@route(path='/index', method='GET')
@route(path='/', method='GET')
def index():
    print('я в индексе')
    # return render_template('index.html')
    return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body><h1>Hello!</h1></body></html>'
    # return 'Hello Word!'


@route(path='/auth', method='GET')
def bar():
    return f'Message:'
