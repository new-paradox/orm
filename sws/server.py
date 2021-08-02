import json
from app import routes


class Server:
    def __init__(self):
        pass

    def response(self, path, method):
        with open('path.json', 'r') as outfile:
            rout = json.load(outfile)
        if f'{path} {method}' in rout:
            f = getattr(routes, rout[f'{path} {method}'])
            return f()


if __name__ == "__main__":
    server = Server()
    server.response('GET', '/bar')
    pass
