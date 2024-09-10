from datetime import datetime
from typing import Union


class Timestamp:
    timestamp_ms: int

    def __init__(self, timestamp_ms: int) -> None:
        self.timestamp_ms = timestamp_ms

    def sub_minutes(self, minutes: int) -> 'Timestamp':
        self.timestamp_ms = self.timestamp_ms - (minutes * 60_000)

        return self

    def add_minutes(self, minutes: int) -> 'Timestamp':
        self.timestamp_ms = self.timestamp_ms + (minutes * 60_000)

        return self

    def __repr__(self) -> str:
        human_readable = datetime.fromtimestamp(
            self.timestamp_ms / 1000
        ).strftime('%Y-%m-%d %H:%M:%S')

        return f'{type(self).__name__} {self.timestamp_ms} : ({human_readable})'

    def __eq__(self, other: Union[int, 'Timestamp']) -> bool:
        if isinstance(other, (int, Timestamp)):
            return self.timestamp_ms == (
                other if isinstance(other, int) else other.timestamp_ms
            )
        return NotImplemented

    def __lt__(self, other: Union[int, 'Timestamp']) -> bool:
        if isinstance(other, (int, Timestamp)):
            return self.timestamp_ms < (
                other if isinstance(other, int) else other.timestamp_ms
            )
        return NotImplemented

    def __le__(self, other: Union[int, 'Timestamp']) -> bool:
        if isinstance(other, (int, Timestamp)):
            return self.timestamp_ms <= (
                other if isinstance(other, int) else other.timestamp_ms
            )
        return NotImplemented

    def __gt__(self, other: Union[int, 'Timestamp']) -> bool:
        if isinstance(other, (int, Timestamp)):
            return self.timestamp_ms > (
                other if isinstance(other, int) else other.timestamp_ms
            )
        return NotImplemented

    def __ge__(self, other: Union[int, 'Timestamp']) -> bool:
        if isinstance(other, (int, Timestamp)):
            return self.timestamp_ms >= (
                other if isinstance(other, int) else other.timestamp_ms
            )
        return NotImplemented

    def __int__(self) -> int:
        return self.timestamp_ms
