from typing import List

from pandas import Timedelta


def count_decimal_places(num: float) -> int:
    if num == 0:
        return 0

    decimal_places = 0
    while not num.is_integer():
        num *= 10
        decimal_places += 1

    return decimal_places


def find_smallest_timeframe(timeframes: List[Timedelta]) -> Timedelta:
    return min(timeframes)
