from dataclasses import dataclass
from typing import Any, Dict

from pandas import to_timedelta
from pandas_ta import ema

from Candlestics import Candlesticks
from Strategy.Indicators.Indicator import Indicator


@dataclass
class EmaIndicator(Indicator):
    length: int
    offset: int

    def calculate(self, candlesticks: Candlesticks, precision: int) -> None:
        candlesticks = candlesticks.recalculate_to_new_timeframe(self.timeframe)

        ema_series = ema(
            candlesticks['close'], length=self.length, offset=self.offset
        ).round(precision)

        ema_series.name = self.get_name()
        self.values = ema_series

    def get_name(self) -> str:
        return 'ema'

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'EmaIndicator':
        parameters = data.get('parameters', {})

        return EmaIndicator(
            timeframe=to_timedelta(data['timeframe']),
            length=parameters['length'],
            offset=parameters['offset'],
        )
