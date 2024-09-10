from typing import List, Optional

from Parser.Operators.BinaryOperatorFactory import BinaryOperatorFactory

from .IdentifierToken import IdentifierToken
from .Nodes.AstNode import ASTNode
from .Nodes.Literal import Literal
from .Nodes.Variable import Variable
from .NumberToken import NumberToken
from .Operators.ArithmeticOpType import ArithmeticOpType
from .Operators.ComparisonOpType import ComparisonOpType
from .Operators.LogicalOpType import LogicalOpType
from .Operators.OpType import OpType
from .OperatorToken import OperatorToken
from .Token import Token
from .TokenType import TokenType


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.pos: int = 0
        self.current_token: Optional[Token] = (
            self.tokens[self.pos] if self.tokens else None
        )

    def parse(self) -> ASTNode:
        return self.parse_binary_expression()

    def parse_binary_expression(self, min_precedence: int = 0) -> ASTNode:
        node = self.parse_primary()

        while self.current_token is not None and isinstance(
            self.current_token, OperatorToken
        ):
            op = self.current_token.value

            precedence = Parser.get_operator_precedence(op)

            if precedence < min_precedence:
                break

            self.consume()

            node = BinaryOperatorFactory.create(
                node, op, self.parse_binary_expression(precedence + 1)
            )

        return node

    @staticmethod
    def get_operator_precedence(op: OpType) -> int:
        if op in (ArithmeticOpType.MUL, ArithmeticOpType.DIV):
            return 4
        if op in (ArithmeticOpType.PLUS, ArithmeticOpType.MINUS):
            return 3
        if op in ComparisonOpType:
            return 2
        if op in LogicalOpType:
            return 1

        return 0

    def parse_primary(self) -> ASTNode:
        token = self.consume()

        if isinstance(token, IdentifierToken):
            return Variable(token.value)
        if isinstance(token, NumberToken):
            return Literal(token.value)
        if token.type == TokenType.LPAREN:
            expr = self.parse()
            self.consume()
            return expr

        raise ValueError('Unexpected token')

    def consume(self) -> Token:
        if self.current_token:
            token = self.current_token
            self.pos += 1
            self.current_token = (
                self.tokens[self.pos] if self.pos < len(self.tokens) else None
            )
            return token
        else:
            raise ValueError(f'Empty current token {self.current_token}')
