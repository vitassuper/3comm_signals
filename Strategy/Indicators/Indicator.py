from abc import abstractmethod
from dataclasses import dataclass, field

from pandas import DataFrame, Series, Timedelta

from Candlestics import Candlesticks
from Strategy.Serializable import Serializable


@dataclass
class Indicator(Serializable):
    timeframe: Timedelta
    values: DataFrame | Series | None = field(default=None, init=False)

    @abstractmethod
    def calculate(self, candlesticks: Candlesticks, precision: int) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def resample_to_new_timeframe(self, timeframe: Timedelta) -> None:
        if self.values is None:
            raise ValueError(f'Indicator {self.get_name()} has no values')

        if self.timeframe != timeframe:
            self.values = self.values.resample(timeframe).ffill()
