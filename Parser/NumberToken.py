from dataclasses import dataclass

from Parser.Token import Token


@dataclass
class NumberToken(Token):
    value: float
