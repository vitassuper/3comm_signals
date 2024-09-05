from dataclasses import dataclass
from typing import Any, Dict

from pandas import to_timedelta
from pandas_ta import bbands

from Candlestics import Candlesticks
from Strategy.Indicators.Indicator import Indicator


@dataclass
class BbandsIndicator(Indicator):
    length: int
    ma_type: str
    std_dev: float

    def calculate(self, candlesticks: Candlesticks, precision: int) -> None:
        candlesticks = candlesticks.recalculate_to_new_timeframe(self.timeframe)

        bbands_df = bbands(
            candlesticks['close'],
            length=self.length,
            mamode=self.ma_type,
            std=self.std_dev,
        ).round(precision)

        indicator_name = self.get_name()

        bbands_df.columns = [
            f'{indicator_name}.lower',
            f'{indicator_name}.middle',
            f'{indicator_name}.upper',
            f'{indicator_name}.width',
            f'{indicator_name}.percent',
        ]
        self.values = bbands_df

    def get_name(self) -> str:
        return 'bbands'

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BbandsIndicator':
        parameters = data.get('parameters', {})

        return BbandsIndicator(
            timeframe=to_timedelta(data['timeframe']),
            length=parameters['length'],
            ma_type=parameters['ma_type'],
            std_dev=parameters['std_dev'],
        )
