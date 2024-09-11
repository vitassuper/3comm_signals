from typing import List, Optional

from ccxt import Exchange
from pandas import Timedelta

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

    @staticmethod
    def _convert_to_candles_dataframe(candles: List[dict]) -> Candles:
        return Candles(
            candles,
            columns=['time', 'open', 'high', 'low', 'close', 'volume'],
        )

    def fetch_candles_if_missing(
        self,
        symbol: str,
        start_timestamp: Timestamp,
        end_timestamp: Optional[Timestamp] = None,
    ) -> None:
        first_candle, last_candle = fetch_first_and_last_candles(symbol)

        if end_timestamp is None:
            end_timestamp = Timestamp(get_start_of_minute_one_minute_ago())

        if first_candle or last_candle:
            first_candle_timestamp = Timestamp(first_candle['opened_at'])
            last_candle_timestamp = Timestamp(last_candle['opened_at'])

            if first_candle_timestamp > start_timestamp:
                self.data_provider.fetch_and_store_historical_candles(
                    symbol,
                    start_timestamp,
                    first_candle_timestamp.sub_minutes(1),
                )

            if last_candle_timestamp < end_timestamp:
                self.data_provider.fetch_and_store_historical_candles(
                    symbol,
                    last_candle_timestamp.add_minutes(1),
                    end_timestamp,
                )
        else:
            self.data_provider.fetch_and_store_historical_candles(
                symbol,
                start_timestamp,
                end_timestamp,
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

        return CandlesDataManager._convert_to_candles_dataframe(candles)

    @staticmethod
    def validate_data_completeness(candles: Candles) -> None:
        expected_interval = Timedelta(
            minutes=1
        )  # Adjust as per your candles frequency

        # Iterate through the DataFrame and check for missing candles
        for i in range(1, len(candles)):
            current_candle_time = candles.index[i]
            previous_candle_time = candles.index[i - 1]

            # Calculate the difference between the current and previous timestamps

            if current_candle_time - previous_candle_time != expected_interval:
                raise ValueError(
                    f'Missing candle between {previous_candle_time} and {current_candle_time}.'
                )
