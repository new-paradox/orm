# -*- coding: utf-8 -*-
from typing import Any


class BaseOperand:
    condition: object
    operand: str

    def __init__(self, *args):
        self.conditions = args

    def return_conditions(self):
        return self.conditions


class AND(BaseOperand):
    operand = 'AND'


class OR(BaseOperand):
    operand = 'OR'


class BaseCompare:
    compare_arg: str

    def __init__(self, key_arg: str, value_arg: Any):
        self.key_arg = key_arg
        self.value_arg = value_arg

    def prepare_condition(self) -> str:
        result_prepare = "%s %s '%s'" % (
            self.key_arg,
            self.compare_arg,
            self.value_arg
        ) if type(self.value_arg) is str else "%s %s %s" % (
            self.key_arg,
            self.compare_arg,
            self.value_arg
        )
        return result_prepare


class EQ(BaseCompare):
    def __init__(self, key_arg: str, value_arg: Any):
        super().__init__(key_arg, value_arg)
        self.compare_arg = '='


class NE(BaseCompare):
    def __init__(self, key_arg: str, value_arg: Any):
        super().__init__(key_arg, value_arg)
        self.compare_arg = '!='


class LT(BaseCompare):
    def __init__(self, key_arg: str, value_arg: Any):
        super().__init__(key_arg, value_arg)
        self.compare_arg = '<'


class GT(BaseCompare):
    def __init__(self, key_arg: str, value_arg: Any):
        super().__init__(key_arg, value_arg)
        self.compare_arg = '>'


class LE(BaseCompare):
    def __init__(self, key_arg: str, value_arg: Any):
        super().__init__(key_arg, value_arg)
        self.compare_arg = '<='


class GE(BaseCompare):
    def __init__(self, key_arg: str, value_arg: Any):
        super().__init__(key_arg, value_arg)
        self.compare_arg = '>='


class QFilter:
    def __init__(self, *args):
        self.prepare_conditions = []
        self.operands = args
        for operand_obj in self.operands:
            self.operand = operand_obj.operand
            conditions = operand_obj.return_conditions()
            for condition in conditions:
                self.prepare_conditions.append(condition.prepare_condition())

        self.and_clause_str = f' {self.operand} '.join(self.prepare_conditions)

    def __repr__(self):
        return self.and_clause_str
