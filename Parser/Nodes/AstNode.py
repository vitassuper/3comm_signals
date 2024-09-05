from abc import ABC, abstractmethod
from typing import Dict, Union


class ASTNode(ABC):
    @abstractmethod
    def evaluate(self, context: Dict[str, Union[int, float]]) -> bool:
        raise NotImplementedError
