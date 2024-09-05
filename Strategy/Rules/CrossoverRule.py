from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple

from pandas import merge

from Strategy.Indicators.Indicator import Indicator
from Strategy.Rules.CrossoverDirection import CrossoverDirection
from Strategy.Rules.Rule import Rule


def get_indicator_name_and_field(indicator: str) -> Tuple[str, str]:
    values = indicator.split('.', 1)

    if len(values) == 2:
        return values[0], values[1]

    else:
        return values[0], values[0]


@dataclass
class CrossoverRule(Rule):
    direction: CrossoverDirection
    indicator1: str
    indicator2: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CrossoverRule':
        return CrossoverRule(
            indicator1=data['indicator1'],
            indicator2=data['indicator2'],
            direction=CrossoverDirection(data['direction']),
        )

    def evaluate_rule(
        self, indicators: List[Indicator], callback: Callable
    ) -> None:
        indicator_name1, indicator_field1 = get_indicator_name_and_field(
            self.indicator1
        )
        indicator_name2, indicator_field2 = get_indicator_name_and_field(
            self.indicator2
        )

        indicator1 = next(
            (
                indicator
                for indicator in indicators
                if indicator.get_name() == indicator_name1
            ),
            None,
        )
        indicator2 = next(
            (
                indicator
                for indicator in indicators
                if indicator.get_name() == indicator_name2
            ),
            None,
        )

        if indicator1 is None:
            raise ValueError(f'Indicator values not provided for: {indicator1}')

        if indicator2 is None:
            raise ValueError(f'Indicator values not provided for: {indicator2}')

        merged_df = merge(
            indicator1.values, indicator2.values, on='time', how='inner'
        )
        filtered_df = merged_df.dropna()

        prev_row = filtered_df.iloc[0]

        for time, row in filtered_df.iterrows():
            value1 = row[indicator_field1]
            value2 = row[indicator_field2]

            prev_value1 = prev_row[indicator_field1]
            prev_value2 = prev_row[indicator_field2]

            if self.direction == CrossoverDirection.TOP_TO_BOTTOM:
                if prev_value1 > prev_value2 and value1 <= value2:
                    callback(row, prev_row, time)
            else:
                if prev_value1 < prev_value2 and value1 >= value2:
                    callback(row, prev_row, time)

            prev_row = row
