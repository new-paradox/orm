from functools import wraps
import json


class Routes:
    pass


class PathController:
    temp_recipient = {}


def route(method, path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(Routes, func.__name__, wrapper)
        PathController.temp_recipient[f'{method} {path}'] = func.__name__
        temp_recipient = PathController.temp_recipient
        with open('path.json', 'w') as outfile:
            json.dump(temp_recipient, outfile)
        return func

    return decorator
