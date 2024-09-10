from typing import Dict, Union

from Parser.Parser import Parser
from Parser.Tokenizer import Tokenizer


class ConditionEvaluator:
    def __init__(self, condition: str) -> None:
        self.condition: str = condition

        tokens = Tokenizer(self.condition).tokenize()
        self.ast = Parser(tokens).parse()

    def evaluate(self, context: Dict[str, Union[int, str, float]]) -> bool:
        return self.ast.evaluate(context)
