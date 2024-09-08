from datetime import datetime, timedelta

from pandas import DataFrame, concat, Timestamp, Timedelta

from Backtest.Deal import Deal
from Candlestics import Candlesticks
from helpers import count_decimal_places, find_smallest_timeframe
from sqlite import (
    fetch_candlesticks,
    insert_candlesticks,
    fetch_last_candlestick,
)
from Strategy.Strategy import Strategy


class Backtest:
    def __init__(self, strategy: Strategy, exchange) -> None:
        self.strategy: Strategy = strategy
        self.exchange = exchange

        self.total_deals: int = 0
        self.success_deals: int = 0
        self.opened_deals = []
        self.last_deal: Deal | None = None

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

            self.store_historical_candlesticks(symbol, end_time)

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

            # start_date = Timestamp('2024-08-26 00:00')
            start_date = None

            for time, row in filtered_df.iterrows():
                if start_date is not None and time < start_date:
                    continue

                if self.strategy.long.entry.evaluate(row.to_dict()):
                    if (
                        self.last_deal is None
                        or row['candlesticks.close']
                        <= self.last_deal.open_price
                        - self.last_deal.open_price * 0.02
                    ):
                        self.total_deals += 1
                        idx = filtered_df.index.get_loc(time)

                        if idx + 1 < len(filtered_df):
                            next_row = filtered_df.iloc[idx + 1]

                            deal = Deal(
                                next_row['candlesticks.open'], next_row.name
                            )
                            self.opened_deals.append(deal)
                            self.last_deal = deal

                            print(
                                f'Open: open price: {deal.open_price}, open time: {deal.open_time}'
                            )

                            continue

                    print(
                        f"Can open for {time}, price: {row['candlesticks.close']} last deal was opened at {self.last_deal.open_time}, price open {self.last_deal.open_price}"
                    )

                for deal in self.opened_deals[:]:
                    if self.strategy.long.exit.evaluate(
                        row.to_dict() | {'entry_price': deal.open_price}
                    ):
                        self.opened_deals.remove(deal)

                        if (
                            self.last_deal is not None
                            and deal.open_time == self.last_deal.open_time
                        ):
                            self.last_deal = None

                        self.success_deals += 1
                        print(
                            f"Close: close price: {row['candlesticks.high']}, close time: {time} Opened at: {deal.open_time}, open price: {deal.open_price}"
                        )

        if self.opened_deals:
            total_open_price = sum(
                deal.open_price for deal in self.opened_deals
            )
            average_open_price = total_open_price / len(self.opened_deals)

            print(f'Average open price: {average_open_price}')
        else:
            print('No opened deals to calculate average.')

        for deal in self.opened_deals:
            print(
                f'Active deal: open price {deal.open_price} open time {deal.open_time}'
            )

        print(
            f'Total deals: {self.total_deals}, success deals: {self.success_deals}'
        )

    def check_missing_data(self, df1m):
        expected_interval = Timedelta(
            minutes=-1
        )  # Adjust as per your candlestick frequency

        # Iterate through the DataFrame and check for missing candles
        for i in range(1, len(df1m)):
            current_candle_time = df1m.index[i]
            previous_candle_time = df1m.index[i - 1]

            # Calculate the difference between the current and previous timestamps
            time_diff = current_candle_time - previous_candle_time

            if time_diff != expected_interval:
                print(
                    f'Missing candle between {previous_candle_time} and {current_candle_time}.'
                )

    # TODO: rename and refactor
    def store_historical_candlesticks(self, symbol: str, since: int) -> None:
        last_candlestick = fetch_last_candlestick(symbol)

        if last_candlestick is not None:
            since = last_candlestick['opened_at'] + 1

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
