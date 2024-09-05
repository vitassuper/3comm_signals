from dataclasses import dataclass

from Parser.Token import Token


@dataclass
class IdentifierToken(Token):
    value: str
