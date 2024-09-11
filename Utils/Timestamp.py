from datetime import datetime
from typing import Union


class Timestamp:
    timestamp_ms: int

    def __init__(self, timestamp_ms: int) -> None:
        self.timestamp_ms = timestamp_ms

    @staticmethod
    def now():
        return Timestamp(int(datetime.now().timestamp() * 1000))

    def clone(self) -> 'Timestamp':
        return Timestamp(self.timestamp_ms)

    def replace(self, second: int = 0, microsecond: int = 0) -> 'Timestamp':
        total_seconds = self.timestamp_ms // 1000

        # Calculate new seconds
        new_seconds = (total_seconds // 60) * 60 + second

        # Calculate new milliseconds
        new_milliseconds = microsecond // 1000

        # Recalculate timestamp in milliseconds
        self.timestamp_ms = (new_seconds * 1000) + new_milliseconds

        return self

    # TODO: temp solution
    def round_to_nearest_15_minutes(self) -> 'Timestamp':
        # Get the number of minutes since epoch
        total_minutes = self.timestamp_ms // (60 * 1000)

        # Round down to the nearest 15-minute block
        rounded_minutes = (total_minutes // 15) * 15

        # Convert back to milliseconds
        self.timestamp_ms = rounded_minutes * 60 * 1000

        return self

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
