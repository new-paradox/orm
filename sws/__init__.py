from functools import wraps
import json
from jinja2 import Environment, FileSystemLoader
from config import TEMPLATES
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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


def render(html_file):
    logger.debug(f"try render {html_file} from {TEMPLATES}")
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template(html_file)
    output_from_parsed_template = template.render()
    return output_from_parsed_template
