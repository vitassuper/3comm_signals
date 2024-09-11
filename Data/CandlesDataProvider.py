from typing import List, Optional

from ccxt import Exchange

from sqlite import (
    fetch_candles,
    insert_candles,
)
from Utils.Timestamp import Timestamp


class CandlesDataProvider:
    EXCHANGE_LIMIT = 1400

    def __init__(self, exchange: Exchange) -> None:
        self.exchange: Exchange = exchange

    def fetch_and_store_historical_candles(
        self,
        symbol: str,
        start_timestamp: Timestamp,
        end_timestamp: Timestamp,
    ) -> None:
        # TODO: fix it
        start_timestamp = start_timestamp.timestamp_ms

        while start_timestamp <= end_timestamp:
            ohlcv = self.exchange.fetch_ohlcv(
                symbol,
                '1m',
                limit=self.EXCHANGE_LIMIT,
                since=start_timestamp,
            )

            if len(ohlcv):
                last_candle_time = ohlcv[-1][0]
                start_timestamp = last_candle_time + 1

                if last_candle_time >= end_timestamp:
                    ohlcv = [
                        candle for candle in ohlcv if candle[0] <= end_timestamp
                    ]

                insert_candles(symbol, ohlcv)
            else:
                break

    def fetch_candles_from_storage(
        self,
        symbol: str,
        start_timestamp: Timestamp,
        limit: Optional[int] = None,
    ) -> List[dict]:
        return fetch_candles(symbol, start_timestamp.timestamp_ms, limit)
