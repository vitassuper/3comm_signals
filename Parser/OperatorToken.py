from dataclasses import dataclass

from Parser.Operators.OpType import OpType
from Parser.Token import Token


@dataclass
class OperatorToken(Token):
    value: OpType
