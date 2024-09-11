import time
from datetime import datetime, timedelta

from ccxt import Exchange
from pandas import concat

from Data.CandlesDataManager import CandlesDataManager
from Strategy.Strategy import Strategy
from Utils.Timestamp import Timestamp
from helpers import count_decimal_places


class Process:
    strategy: Strategy
    candles_data_manager: CandlesDataManager

    markets: dict

    def __init__(self, strategy: Strategy, exchange: Exchange):
        self.strategy = strategy
        self.candles_data_manager = CandlesDataManager(exchange)

        self.markets = exchange.load_markets()

    # TODO: duplicates function
    def _get_precision(self, symbol: str) -> int:
        market = self.markets[symbol]

        return count_decimal_places(market['precision']['price'])

    @staticmethod
    def wait_until_next_minute():
        now = datetime.now()
        next_minute = (now + timedelta(minutes=1)).replace(
            second=0, microsecond=0
        )
        wait_time = (next_minute - now).total_seconds()
        return wait_time

    def loop(self):
        while True:
            # Calculate initial wait time
            initial_wait_time = Process.wait_until_next_minute()

            # Wait until the start of the next minute
            time.sleep(initial_wait_time)

            # Measure the time taken to execute the function
            start_time = time.time()

            self.process()

            end_time = time.time()

            # Calculate how much time was spent processing
            processing_time = end_time - start_time

            # Calculate the remaining time to wait before the next call
            remaining_wait_time = 60 - processing_time

            # Ensure we wait the correct amount of time
            if remaining_wait_time > 0:
                time.sleep(remaining_wait_time)

    def process(self):
        symbol = 'ADA/USDT'
        precision = self._get_precision(symbol)

        data_size = 10_000

        if self.strategy.biggest_period > data_size:
            raise ValueError(
                'Data size cannot be smaller than the largest period'
            )

        start_timestamp = (
            Timestamp.now()
            .replace(second=0, microsecond=0)
            .sub_minutes(data_size)
        )

        self.candles_data_manager.fetch_candles_if_missing(
            symbol,
            start_timestamp,
        )

        candles = self.candles_data_manager.get_candles_data(
            symbol, start_timestamp, data_size
        )

        if not len(candles):
            raise Exception('No candles data')

        indicator_data_frames = []

        for indicator in self.strategy.indicators:
            indicator.calculate(candles, precision)

            indicator.resample_to_new_timeframe(
                self.strategy.smallest_timeframe
            )

            indicator_data_frames.append(indicator.values)

        df = concat(indicator_data_frames, axis=1)
        df.ffill(inplace=True)

        last_row = df.iloc[-1]

        if self.strategy.long and self.strategy.long.entry.evaluate(
            last_row.to_dict()
        ):
            print(
                f'Open long deal: '
                f'time {last_row.name} - '
                f'open: {last_row["candles.open"]} - '
                f'close: {last_row["candles.close"]} - '
                f'b.upper: {last_row["bbands.upper"]} - '
                f'ema: {last_row["ema"]} - '
                f'b.middle: {last_row["bbands.middle"]}'
            )
