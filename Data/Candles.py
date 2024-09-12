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

        if timeframe == Timedelta(minutes=1):
            return df

        # Determine the expected start time for the first full timeframe
        first_valid_time = df.index[0] + (timeframe - (df.index[0] - df.index[0].floor(timeframe)))

        # Determine the expected start time for the last full timeframe
        last_valid_time = df.index[-1].floor(timeframe)

        if (df.index[-1] - last_valid_time) < timeframe:
            df_filtered = df[df.index < last_valid_time]
        else:
            df_filtered = df

        df_filtered = df_filtered[df_filtered.index >= first_valid_time]

        return df_filtered.resample(timeframe).apply(
            {
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum',
            }
        )
