from typing import Dict, Type

from Strategy.Indicators.BbandsIndicator import BbandsIndicator
from Strategy.Indicators.CandlesticksIndicator import CandlesticksIndicator
from Strategy.Indicators.EmaIndicator import EmaIndicator
from Strategy.Indicators.Indicator import Indicator

INDICATORS_MAP: Dict[str, Type[Indicator]] = {
    'ema': EmaIndicator,
    'bbands': BbandsIndicator,
    'candlesticks': CandlesticksIndicator,
}
