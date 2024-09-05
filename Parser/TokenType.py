from enum import Enum


class TokenType(Enum):
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    OPERATOR = 'OPERATOR'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    WHITESPACE = 'WHITESPACE'
    ERROR = 'ERROR'
