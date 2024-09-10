import re
from typing import List, Tuple

from Parser.IdentifierToken import IdentifierToken
from Parser.NumberToken import NumberToken
from Parser.Operators.ArithmeticOpType import ArithmeticOpType
from Parser.Operators.ComparisonOpType import ComparisonOpType
from Parser.Operators.LogicalOpType import LogicalOpType
from Parser.OperatorToken import OperatorToken
from Parser.Token import Token
from Parser.TokenType import TokenType


class Tokenizer:
    def __init__(self, rule: str) -> None:
        self.rule: str = rule

    @staticmethod
    def _get_token_specification() -> List[Tuple[TokenType, str]]:
        return [
            (TokenType.OPERATOR, r'\b(or|and)\b|[<>!=]=?|[+\-*/]'),
            (TokenType.NUMBER, r'\d+(\.\d*)?'),
            (
                TokenType.IDENTIFIER,
                r'[a-zA-Z_][a-zA-Z_0-9]*(\.[a-zA-Z_][a-zA-Z_0-9]*)?',
            ),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.WHITESPACE, r'[ \t]+'),
            (TokenType.ERROR, r'.'),
        ]

    @staticmethod
    def _get_token_mapping():
        return {
            TokenType.NUMBER.value: lambda val: NumberToken(
                TokenType.NUMBER, float(val)
            ),
            TokenType.IDENTIFIER.value: lambda val: IdentifierToken(
                TokenType.IDENTIFIER, val
            ),
            TokenType.OPERATOR.value: lambda val: OperatorToken(
                TokenType.OPERATOR, Tokenizer.get_operator_token_value(val)
            ),
            TokenType.LPAREN.value: lambda _: Token(TokenType.LPAREN),
            TokenType.RPAREN.value: lambda _: Token(TokenType.RPAREN),
        }

    @staticmethod
    def get_operator_token_value(
        operator: str,
    ) -> LogicalOpType | ArithmeticOpType | ComparisonOpType:
        if operator in LogicalOpType:
            return LogicalOpType(operator)

        if operator in ArithmeticOpType:
            return ArithmeticOpType(operator)

        if operator in ComparisonOpType:
            return ComparisonOpType(operator)

        raise RuntimeError(f'Unexpected operator {operator}')

    def tokenize(self) -> List[Token]:
        token_specification = Tokenizer._get_token_specification()
        token_mapping = Tokenizer._get_token_mapping()

        regex_parts = '|'.join(
            f'(?P<{pair[0].value}>{pair[1]})' for pair in token_specification
        )

        tokens = []

        for match in re.finditer(regex_parts, self.rule):
            type_ = match.lastgroup
            value = match.group(type_)

            if type_ == TokenType.WHITESPACE.value:
                continue

            if type_ == TokenType.ERROR.value:
                raise RuntimeError(f'Unexpected character {value}')

            if type_ in token_mapping:
                tokens.append(token_mapping[type_](value))

        return tokens
