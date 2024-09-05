from dataclasses import dataclass
from typing import Any, Dict, List

from Strategy.Condition import Condition
from Strategy.Indicators.Indicator import Indicator
from Strategy.Indicators.IndicatorFactory import IndicatorFactory
from Strategy.Pair import Pair
from Strategy.Serializable import Serializable


@dataclass
class Strategy(Serializable):
    indicators: List[Indicator]
    pairs: List[Pair]
    long: Condition | None = None
    short: Condition | None = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Strategy':
        return Strategy(
            indicators=[
                IndicatorFactory.from_dict(ind) for ind in data['indicators']
            ],
            pairs=[Pair.from_dict(pair) for pair in data['pairs']],
            long=Condition.from_dict(data['long']['conditions'])
            if 'long' in data and data['long']
            else None,
            short=Condition.from_dict(data['short']['conditions'])
            if 'short' in data and data['short']
            else None,
        )
