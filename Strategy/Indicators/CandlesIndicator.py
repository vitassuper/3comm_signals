from typing import Any, Dict

from pandas import to_timedelta

from Data import Candles
from Strategy.Indicators.Indicator import Indicator


class CandlesIndicator(Indicator):
    def calculate(self, candles: Candles, precision: int) -> None:
        candles = candles.recalculate_to_new_timeframe(self.timeframe)

        indicator_name = self.get_name()

        candles.columns = [
            f'{indicator_name}.open',
            f'{indicator_name}.high',
            f'{indicator_name}.low',
            f'{indicator_name}.close',
            f'{indicator_name}.volume',
        ]

        self.values = candles

    def get_name(self) -> str:
        return 'candles'

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CandlesIndicator':
        return CandlesIndicator(
            timeframe=to_timedelta(data['timeframe']),
        )
