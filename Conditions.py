# -*- coding: utf-8 -*-
from typing import Any, List


class QFilter:
    prepare_condition: List

    def __init__(self, *args):
        self.condition = args

    def __str__(self):
        return f'WHERE {self.condition if len(self.condition) > 1 else self.condition[0]}'


class EQ:
    def __init__(self, first_arg: str, second_arg: Any):
        self.first_arg = first_arg
        self.second_arg = second_arg

    def __str__(self):
        return f"{self.first_arg} = {self.second_arg}"
