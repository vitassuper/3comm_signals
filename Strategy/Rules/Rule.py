from abc import ABC, abstractmethod
from typing import Callable, List

from Strategy.Indicators.Indicator import Indicator


class Rule(ABC):
    @abstractmethod
    def evaluate_rule(
        self, indicators: List[Indicator], callback: Callable
    ) -> None:
        pass
