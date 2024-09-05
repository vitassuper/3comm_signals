from typing import Dict, Union

from Parser.Nodes.AstNode import ASTNode


class Variable(ASTNode):
    def __init__(self, name: str) -> None:
        self.name: str = name

    def evaluate(
        self, context: Dict[str, Union[int, float]]
    ) -> Union[int, float]:
        if self.name in context:
            return context[self.name]
        raise ValueError(f'Undefined variable: {self.name}')
