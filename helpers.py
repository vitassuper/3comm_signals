from datetime import datetime, timedelta
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


def get_start_of_minute_one_minute_ago() -> int:
    now = datetime.now()

    start_of_current_minute = now.replace(second=0, microsecond=0)
    start_of_one_minute_ago = start_of_current_minute - timedelta(minutes=1)

    return int(start_of_one_minute_ago.timestamp() * 1000)


def is_list_of_lists(candles: List[any]) -> bool:
    # Check if all elements in the list are also lists
    return all(isinstance(item, list) for item in candles)
