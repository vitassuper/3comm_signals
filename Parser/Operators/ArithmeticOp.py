from typing import Dict, Union

from Parser.Operators.ArithmeticOpType import ArithmeticOpType
from Parser.Operators.BinaryOp import BinaryOp


class ArithmeticOp(BinaryOp):
    def evaluate(self, context: Dict[str, Union[int, float]]) -> float:
        left_value = self.left.evaluate(context)
        right_value = self.right.evaluate(context)

        if self.op == ArithmeticOpType.PLUS:
            return left_value + right_value
        if self.op == ArithmeticOpType.MINUS:
            return left_value - right_value
        if self.op == ArithmeticOpType.DIV:
            return left_value / right_value
        if self.op == ArithmeticOpType.MUL:
            return left_value * right_value

        raise ValueError(f'Unknown operator: {self.op}')
