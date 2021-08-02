from functools import wraps
import json


class Routes:
    pass


def read_rout2json():
    with open('path.json', 'r') as outfile:
        return json.load(outfile)


def write_rout2json(temp_recipient, method, path, func):
    with open('path.json', 'w') as outfile:
        temp_recipient[f'{method} {path}'] = func.__name__
        json.dump(temp_recipient, outfile)


def route(path, method):
    temp_recipient = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(Routes, func.__name__, wrapper)
        temp_recipient = read_rout2json()
        write_rout2json(temp_recipient=temp_recipient, method=method, path=path, func=func)

        return func

    return decorator
