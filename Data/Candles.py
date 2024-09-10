from pandas import DataFrame, Timedelta, to_datetime


class Candles(DataFrame):
    def __init__(self, *args, **kwargs) -> None:
        # Initialize the DataFrame
        super().__init__(*args, **kwargs)

        # Convert 'time' column to datetime format if it exists
        if 'time' in self.columns:
            self['time'] = to_datetime(self['time'], unit='ms')
            self.set_index('time', inplace=True)

    def recalculate_to_new_timeframe(self, timeframe: Timedelta) -> 'Candles':
        df = self.copy()

        return df.resample(timeframe).apply(
            {
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum',
            }
        )
