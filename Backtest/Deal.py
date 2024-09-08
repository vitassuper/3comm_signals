from dataclasses import dataclass
from datetime import datetime

from pandas import Timestamp


@dataclass
class Deal:
    open_price: float
    open_time: Timestamp
