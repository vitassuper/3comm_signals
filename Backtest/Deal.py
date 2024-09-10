from dataclasses import dataclass

from pandas import Timestamp


@dataclass
class Deal:
    open_price: float
    open_time: Timestamp
