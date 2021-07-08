# -*- coding: utf-8 -*-
from typing import Any


class QFilter:
    def __init__(self, *args):
        self.prepare_conditions = []
        self.and_clause_str: str
        self.condition = args
        for elem in self.condition:
            if type(elem) is EQ:
                self.prepare_conditions.append(elem.prepare_condition())
        self.and_clause_str = ' AND '.join(self.prepare_conditions)

    def __repr__(self):
        return self.and_clause_str


class EQ:
    def __init__(self, key_arg: str, value_arg: Any):
        self.key_arg = key_arg
        self.value_arg = value_arg

    def prepare_condition(self):
        if type(self.value_arg) is str:
            return "%s = '%s'" % (self.key_arg, self.value_arg)
        else:
            return "%s = %s" % (self.key_arg, self.value_arg)
