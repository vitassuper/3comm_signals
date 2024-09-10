from ccxt import Exchange
from pandas import DataFrame, concat

from Data.CandlesDataManager import CandlesDataManager
from helpers import count_decimal_places
from Strategy.Strategy import Strategy
from Utils.Timestamp import Timestamp


class DataManager:
    strategy: Strategy
    exchange: Exchange
    candles_data_manager: CandlesDataManager
    markets: dict

    def __init__(self, strategy: Strategy, exchange: Exchange) -> None:
        self.strategy = strategy
        self.exchange = exchange

        self.candles_data_manager = CandlesDataManager(exchange)
        self.markets = exchange.load_markets()

    def _get_precision(self, symbol: str) -> int:
        market = self.markets[symbol]

        return count_decimal_places(market['precision']['price'])

    def fetch_and_process_data(
        self, symbol: str, start_timestamp: Timestamp
    ) -> DataFrame:
        # Ensure all candles are fetched and up-to-date
        self.candles_data_manager.fetch_candles_if_missing(
            symbol, start_timestamp
        )

        precision = self._get_precision(symbol)
        chunk_size = 10_000

        if self.strategy.biggest_period > chunk_size:
            raise ValueError(
                'Chunk size cannot be smaller than the largest period'
            )

        while True:
            candles_chunk = self.candles_data_manager.get_candles_data(
                symbol, start_timestamp, chunk_size
            )

            # Break the loop if no data is returned
            if not len(candles_chunk):
                break

            indicator_data_frames = []

            for indicator in self.strategy.indicators:
                indicator.calculate(candles_chunk, precision)
                indicator.resample_to_new_timeframe(
                    self.strategy.smallest_timeframe
                )

                indicator_data_frames.append(indicator.values)

            yield concat(indicator_data_frames, axis=1).dropna()

            start_timestamp = start_timestamp.add_minutes(
                chunk_size - self.strategy.biggest_period
            )
