from typing import List, Optional

from ccxt import Exchange

from Data.Candles import Candles
from Data.CandlesDataProvider import CandlesDataProvider
from helpers import (
    get_start_of_minute_one_minute_ago,
)
from sqlite import fetch_first_and_last_candles
from Utils.Timestamp import Timestamp


class CandlesDataManager:
    data_provider: CandlesDataProvider

    def __init__(self, exchange: Exchange) -> None:
        self.data_provider = CandlesDataProvider(exchange)

    def _convert_to_candles_dataframe(self, candles: List[dict]) -> Candles:
        return Candles(
            candles,
            columns=['time', 'open', 'high', 'low', 'close', 'volume'],
        )

    def fetch_candles_if_missing(
        self, symbol: str, start_timestamp: Timestamp
    ) -> None:
        first_candle, last_candle = fetch_first_and_last_candles(symbol)

        one_minute_ago_timestamp = Timestamp(
            get_start_of_minute_one_minute_ago()
        )

        if first_candle or last_candle:
            first_candle_timestamp = Timestamp(first_candle['opened_at'])
            last_candle_timestamp = Timestamp(last_candle['opened_at'])

            if first_candle_timestamp > start_timestamp:
                self.data_provider.fetch_and_store_historical_candles(
                    symbol,
                    start_timestamp,
                    first_candle_timestamp.sub_minutes(1),
                )

            if last_candle_timestamp < one_minute_ago_timestamp:
                self.data_provider.fetch_and_store_historical_candles(
                    symbol,
                    last_candle_timestamp.add_minutes(1),
                    one_minute_ago_timestamp,
                )
        else:
            self.data_provider.fetch_and_store_historical_candles(
                symbol,
                start_timestamp,
                one_minute_ago_timestamp,
            )

    def get_candles_data(
        self,
        symbol: str,
        start_timestamp: Timestamp,
        limit: Optional[int] = None,
    ) -> Candles:
        candles = self.data_provider.fetch_candles_from_storage(
            symbol, start_timestamp, limit
        )

        return self._convert_to_candles_dataframe(candles)
