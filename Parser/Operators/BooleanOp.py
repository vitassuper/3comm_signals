from typing import Dict, Union

from Parser.Operators.BinaryOp import BinaryOp
from Parser.Operators.LogicalOpType import LogicalOpType


class BooleanOp(BinaryOp):
    def evaluate(self, context: Dict[str, Union[int, float]]) -> bool:
        left_value = self.left.evaluate(context)
        right_value = self.right.evaluate(context)
        if self.op == LogicalOpType.AND:
            return left_value and right_value
        if self.op == LogicalOpType.OR:
            return left_value or right_value

        raise ValueError(f'Unknown operator: {self.op}')
