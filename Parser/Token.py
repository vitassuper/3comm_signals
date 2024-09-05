from dataclasses import dataclass

from Parser.TokenType import TokenType


@dataclass
class Token:
    type: TokenType
