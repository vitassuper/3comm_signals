from Parser.Nodes.AstNode import ASTNode
from Parser.Operators.ArithmeticOp import ArithmeticOp
from Parser.Operators.ArithmeticOpType import ArithmeticOpType
from Parser.Operators.BooleanOp import BooleanOp
from Parser.Operators.ComparisonOp import ComparisonOp
from Parser.Operators.ComparisonOpType import ComparisonOpType
from Parser.Operators.LogicalOpType import LogicalOpType


class BinaryOperatorFactory:
    @staticmethod
    def create(
        left: ASTNode, op: str, right: ASTNode
    ) -> ArithmeticOp | ComparisonOp | BooleanOp:
        if op in ArithmeticOpType:
            return ArithmeticOp(left, op, right)
        if op in ComparisonOpType:
            return ComparisonOp(left, op, right)
        if op in LogicalOpType:
            return BooleanOp(left, op, right)

        raise ValueError(f'Unexpected operator {op}')
