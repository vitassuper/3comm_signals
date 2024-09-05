from datetime import datetime, timedelta

from pandas import DataFrame, concat

from Candlestics import Candlesticks
from helpers import count_decimal_places, find_smallest_timeframe
from sqlite import fetch_candlesticks, insert_candlesticks
from Strategy.Strategy import Strategy


class Backtest:
    def __init__(self, strategy: Strategy, exchange) -> None:
        self.strategy: Strategy = strategy
        self.exchange = exchange

        self.total_deals: int = 0
        self.success_deals: int = 0
        self.last_price: float | None = None

    def run(self) -> None:
        if self.strategy.long is None and self.strategy.short is None:
            raise ValueError(
                'Either the "short" or "long" field must be provided for the strategy.'
            )

        date_string = '2021-01-01'
        date_format = '%Y-%m-%d'

        dt_object = datetime.strptime(date_string, date_format)
        end_time = int(dt_object.timestamp() * 1000)

        markets = self.exchange.load_markets()

        smallest_timeframe = find_smallest_timeframe(
            list(map(lambda x: x.timeframe, self.strategy.indicators))
        )

        for pair in self.strategy.pairs:
            symbol = pair.symbol
            market = markets[symbol]

            precision = count_decimal_places(market['precision']['price'])

            # self.store_historical_candlesticks(symbol, end_time)

            ohlcv = fetch_candlesticks(symbol)
            df1m = Candlesticks(
                ohlcv,
                columns=['time', 'open', 'high', 'low', 'close', 'volume'],
            )

            indicator_values = []

            for indicator in self.strategy.indicators:
                indicator.calculate(df1m, precision)
                indicator.resample_to_new_timeframe(smallest_timeframe)

                indicator_values.append(indicator)

            filtered_df = concat(
                [indicator.values for indicator in indicator_values], axis=1
            ).dropna()

            for time, row in filtered_df.iterrows():
                if self.strategy.long.entry.evaluate(row.to_dict()) and (
                    self.last_price is None
                    or row['candlesticks.close']
                    <= self.last_price - self.last_price * 0.02
                ):
                    self.total_deals += 1
                    idx = filtered_df.index.get_loc(time)
                    result_df = filtered_df.iloc[idx + 1 :]
                    self.control_opened_deal(result_df)

        print(
            f'Total deals: {self.total_deals}, success deals: {self.success_deals}'
        )

    def control_opened_deal(self, indicators: DataFrame) -> None:
        open_time = indicators.index[0]
        open_price = indicators.iloc[0]['candlesticks.open']

        print(f'Open price: {open_price}, open time: {open_time}')

        self.last_price = open_price

        close_price = None

        for time, row in indicators.iterrows():
            context = row.to_dict() | {'entry_price': open_price}

            if self.strategy.long.exit.evaluate(context):
                close_price = context.get('candlesticks.high')
                self.success_deals += 1
                self.last_price = None

                print(f'Close: {close_price}, close time: {time}')

                break

    def store_historical_candlesticks(self, symbol: str, since: int) -> None:
        exchange = self.exchange
        limit = 800

        while since < exchange.milliseconds():
            ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=limit, since=since)

            if len(ohlcv):
                since = ohlcv[-1][0] + 1

                last_candle_time = ohlcv[-1][0]
                last_candle_datetime = datetime.fromtimestamp(
                    last_candle_time / 1000
                )

                one_minute_ago = datetime.now() - timedelta(minutes=1)

                if last_candle_datetime > one_minute_ago:
                    # Remove the last candle if it might not be closed
                    ohlcv = ohlcv[:-1]

                insert_candlesticks(symbol, ohlcv)
            else:
                break
