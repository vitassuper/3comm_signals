from typing import Any, Dict

from Strategy.Indicators.Indicator import Indicator
from Strategy.Indicators.IndicatorsMap import INDICATORS_MAP


class IndicatorFactory:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Indicator:
        indicator_name = data.get('name')

        if indicator_name not in INDICATORS_MAP:
            raise ValueError(f'Unknown indicator: {indicator_name}')

        indicator_class = INDICATORS_MAP[indicator_name]

        return indicator_class.from_dict(data)
