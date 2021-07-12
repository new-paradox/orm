# -*- coding: utf-8 -*-


def chained(fn):
    def new(*args, **kwargs):
        fn(*args, **kwargs)
        return args[0]

    return new


class QFilter:
    def __init__(self):
        self.condition = ''

    @chained
    def add_k(self, condition):
        self.condition += condition

    @chained
    def add_v(self, condition):
        if isinstance(condition, str):
            self.condition += f"'{condition}'"
        else:
            self.condition += f"{condition}"

    @chained
    def open_sh(self):
        self.condition += '('

    @chained
    def close_sh(self):
        self.condition += ')'

    @chained
    def eq(self):
        self.condition += ' = '

    @chained
    def ne(self):
        self.condition += ' != '

    @chained
    def lt(self):
        self.condition += ' < '

    @chained
    def gt(self):
        self.condition += ' > '

    @chained
    def le(self):
        self.condition += ' <= '

    @chained
    def ge(self):
        self.condition += ' >= '

    @chained
    def q_and(self):
        self.condition += ' AND '

    @chained
    def q_or(self):
        self.condition += ' OR '
