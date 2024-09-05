from typing import Any, Dict

from pandas import to_timedelta

from Candlestics import Candlesticks
from Strategy.Indicators.Indicator import Indicator


class CandlesticksIndicator(Indicator):
    def calculate(self, candlesticks: Candlesticks, precision: int) -> None:
        candlesticks = candlesticks.recalculate_to_new_timeframe(self.timeframe)

        indicator_name = self.get_name()

        candlesticks.columns = [
            f'{indicator_name}.open',
            f'{indicator_name}.high',
            f'{indicator_name}.low',
            f'{indicator_name}.close',
            f'{indicator_name}.volume',
        ]

        self.values = candlesticks

    def get_name(self) -> str:
        return 'candlesticks'

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CandlesticksIndicator':
        return CandlesticksIndicator(
            timeframe=to_timedelta(data['timeframe']),
        )
