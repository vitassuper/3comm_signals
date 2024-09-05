from dataclasses import dataclass
from typing import Any, Dict

from Strategy.ConditionEvaluator import ConditionEvaluator
from Strategy.Serializable import Serializable


@dataclass
class Condition(Serializable):
    entry: ConditionEvaluator
    exit: ConditionEvaluator | None = None

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Condition(
            entry=ConditionEvaluator(data['entry']),
            exit=ConditionEvaluator(data['exit'])
            if 'exit' in data and data['exit']
            else None,
        )
