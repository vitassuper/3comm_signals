from typing import Any, Dict, List

from pandas import Timedelta

from helpers import find_smallest_timeframe
from Strategy.Condition import Condition
from Strategy.Indicators.Indicator import Indicator
from Strategy.Indicators.IndicatorFactory import IndicatorFactory
from Strategy.Pair import Pair
from Strategy.Serializable import Serializable


class Strategy(Serializable):
    indicators: List[Indicator]
    pairs: List[Pair]
    long: Condition | None
    short: Condition | None

    smallest_timeframe: Timedelta
    biggest_period: int

    def __init__(
        self,
        indicators: List[Indicator],
        pairs: List[Pair],
        long: Condition = None,
        short: Condition = None,
    ) -> None:
        self.long = long
        self.short = short

        self._validate()

        self.indicators = indicators
        self.pairs = pairs

        self._calculate_smallest_timeframe()
        self._calculate_biggest_period()

    def _calculate_smallest_timeframe(self) -> None:
        self.smallest_timeframe = find_smallest_timeframe(
            list(map(lambda indicator: indicator.timeframe, self.indicators))
        )

    def _calculate_biggest_period(self) -> None:
        period = 0

        for indicator in self.indicators:
            if hasattr(indicator, 'length'):
                length = indicator.length
                minutes = indicator.timeframe.total_seconds() / 60

                # -2 because pagination in Backtest
                local_period = (length - 2) * minutes

                if local_period > period:
                    period = local_period

        self.biggest_period = period

    def _validate(self) -> None:
        if self.short is None and self.long is None:
            raise ValueError(
                'Either the "short" or "long" field must be provided for the strategy.'
            )

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
