from typing import Dict, Type

from Strategy.Indicators.BbandsIndicator import BbandsIndicator
from Strategy.Indicators.CandlesIndicator import CandlesIndicator
from Strategy.Indicators.EmaIndicator import EmaIndicator
from Strategy.Indicators.Indicator import Indicator

INDICATORS_MAP: Dict[str, Type[Indicator]] = {
    'ema': EmaIndicator,
    'bbands': BbandsIndicator,
    'candles': CandlesIndicator,
}
