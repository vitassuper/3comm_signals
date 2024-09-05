from typing import Dict, Union

from Parser.Nodes.AstNode import ASTNode


class Literal(ASTNode):
    def __init__(self, value: Union[int, float]) -> None:
        self.value: int | float = value

    def evaluate(
        self, context: Dict[str, Union[int, float]]
    ) -> Union[int, float]:
        return self.value
