import re
from typing import List

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

    def tokenize(self) -> List[Token]:
        token_specification = [
            (TokenType.NUMBER, r'\d+(\.\d*)?'),
            (
                TokenType.IDENTIFIER,
                r'[a-zA-Z_][a-zA-Z_0-9]*(\.[a-zA-Z_][a-zA-Z_0-9]*)?',
            ),
            (TokenType.OPERATOR, r'\b(or|and)\b|[<>!=]=?|[+\-*/]'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.WHITESPACE, r'[ \t]+'),
            (TokenType.ERROR, r'.'),
        ]
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

            if type_ == TokenType.NUMBER.value:
                tokens.append(NumberToken(TokenType.NUMBER, float(value)))
            elif type_ == TokenType.IDENTIFIER.value:
                tokens.append(IdentifierToken(TokenType.IDENTIFIER, value))
            elif type_ == TokenType.OPERATOR.value:
                tokens.append(
                    OperatorToken(
                        TokenType.OPERATOR, self.get_operator_token_value(value)
                    )
                )
            elif type_ == TokenType.LPAREN.value:
                tokens.append(Token(TokenType.LPAREN))
            elif type_ == TokenType.RPAREN.value:
                tokens.append(Token(TokenType.RPAREN))

        return tokens

    def get_operator_token_value(
        self, operator: str
    ) -> LogicalOpType | ArithmeticOpType | ComparisonOpType:
        if operator in LogicalOpType:
            return LogicalOpType(operator)

        if operator in ArithmeticOpType:
            return ArithmeticOpType(operator)

        if operator in ComparisonOpType:
            return ComparisonOpType(operator)

        raise RuntimeError(f'Unexpected operator {operator}')
