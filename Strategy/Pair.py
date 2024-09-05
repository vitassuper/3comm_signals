from dataclasses import dataclass
from typing import Any, Dict

from Strategy.Serializable import Serializable


@dataclass
class Pair(Serializable):
    symbol: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Pair':
        return Pair(symbol=data['symbol'])
