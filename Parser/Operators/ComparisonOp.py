from typing import Dict, Union

from Parser.Operators.BinaryOp import BinaryOp
from Parser.Operators.ComparisonOpType import ComparisonOpType


class ComparisonOp(BinaryOp):
    def evaluate(self, context: Dict[str, Union[int, float]]) -> bool:
        left_value = self.left.evaluate(context)
        right_value = self.right.evaluate(context)
        if self.op == ComparisonOpType.LESS_THAN:
            return left_value < right_value
        elif self.op == ComparisonOpType.GREATER_THAN:
            return left_value > right_value
        elif self.op == ComparisonOpType.LESS_THAN_OR_EQUAL:
            return left_value <= right_value
        elif self.op == ComparisonOpType.GREATER_THAN_OR_EQUAL:
            return left_value >= right_value
        else:
            raise ValueError(f'Unknown operator: {self.op}')
