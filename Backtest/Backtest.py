from datetime import datetime
from typing import List

import pandas as pd
from ccxt import Exchange
from pandas import Series, Timedelta

from Backtest.DataManager import DataManager
from Backtest.Deal import Deal
from Data.Candles import Candles
from Strategy.Strategy import Strategy
from Utils.Timestamp import Timestamp


class Backtest:
    strategy: Strategy
    data_manager: DataManager

    total_deals: int
    success_deals: int
    opened_long_deals: List[Deal]
    opened_short_deals: List[Deal]
    last_long_deal: Deal | None
    last_short_deal: Deal | None

    def __init__(self, strategy: Strategy, exchange: Exchange) -> None:
        self.strategy = strategy

        self._init_stats()

        date_string = '2021-01-01'
        date_format = '%Y-%m-%d'

        dt_object = datetime.strptime(date_string, date_format)
        self.start_timestamp: Timestamp = Timestamp(
            int(dt_object.timestamp() * 1000)
        )

        self.data_manager = DataManager(strategy, exchange)

    def _init_stats(self) -> None:
        self.total_deals = 0
        self.success_deals = 0
        self.opened_long_deals = []
        self.opened_short_deals = []
        self.last_long_deal = None
        self.last_short_deal = None

    def open_new_long_deal(self, row: Series, timestamp: pd.Timestamp) -> None:
        self.total_deals += 1

        deal = Deal(row['candles.open'], timestamp)
        self.opened_long_deals.append(deal)
        self.last_long_deal = deal

        print(
            f'Open: open price: {deal.open_price}, open time: {deal.open_time}'
        )

    def open_new_short_deal(self, row: Series, timestamp: pd.Timestamp) -> None:
        self.total_deals += 1

        deal = Deal(row['candles.open'], timestamp)
        self.opened_short_deals.append(deal)
        self.last_short_deal = deal

        print(
            f'Open: open price: {deal.open_price}, open time: {deal.open_time}'
        )

    def manage_open_short_deals(
        self, row: Series, timestamp: pd.Timestamp
    ) -> None:
        for deal in self.opened_short_deals[:]:
            if self.strategy.short.exit.evaluate(
                row.to_dict() | {'entry_price': deal.open_price}
            ):
                self.opened_short_deals.remove(deal)

                if (
                    self.last_short_deal is not None
                    and deal.open_time == self.last_short_deal.open_time
                ):
                    self.last_short_deal = None

                self.success_deals += 1
                print(
                    f"Close: close price: {row['candles.high']}, close time: {timestamp} Opened at: {deal.open_time}, open price: {deal.open_price}"
                )

    def manage_open_long_deals(
        self, row: Series, timestamp: pd.Timestamp
    ) -> None:
        for deal in self.opened_long_deals[:]:
            if self.strategy.long.exit.evaluate(
                row.to_dict() | {'entry_price': deal.open_price}
            ):
                self.opened_long_deals.remove(deal)

                if (
                    self.last_long_deal is not None
                    and deal.open_time == self.last_long_deal.open_time
                ):
                    self.last_long_deal = None

                self.success_deals += 1
                print(
                    f"Close: close price: {row['candles.high']}, close time: {timestamp} Opened at: {deal.open_time}, open price: {deal.open_price}"
                )

    def run(self) -> None:
        for pair in self.strategy.pairs:
            symbol = pair.symbol

            # start_date = pd.Timestamp('2024-08-26 00:00')
            start_date = None

            data = self.data_manager.fetch_and_process_data(
                symbol, self.start_timestamp
            )

            for chunk in data:
                for timestamp, row in chunk.iterrows():
                    if start_date is not None and timestamp < start_date:
                        continue

                    if self.strategy.long and self.strategy.long.entry.evaluate(
                        row.to_dict()
                    ):
                        if (
                            self.last_long_deal is None
                            or row['candles.close']
                            <= self.last_long_deal.open_price
                            - self.last_long_deal.open_price * 0.02
                        ):
                            idx = chunk.index.get_loc(timestamp)

                            if idx + 1 < len(chunk):
                                next_row = chunk.iloc[idx + 1]
                                self.open_new_long_deal(next_row, next_row.name)

                            continue

                        print(
                            f"Can open for {timestamp}, price: {row['candles.close']} last deal was opened at {self.last_long_deal.open_time}, price open {self.last_long_deal.open_price}"
                        )

                    if (
                        self.strategy.short
                        and self.strategy.short.entry.evaluate(row.to_dict())
                    ):
                        if (
                            self.last_short_deal is None
                            or row['candles.close']
                            >= self.last_short_deal.open_price
                            + self.last_short_deal.open_price * 0.02
                        ):
                            idx = chunk.index.get_loc(timestamp)

                            if idx + 1 < len(chunk):
                                next_row = chunk.iloc[idx + 1]
                                self.open_new_short_deal(
                                    next_row, next_row.name
                                )

                            continue

                        print(
                            f"Can open for {timestamp}, price: {row['candles.close']} last deal was opened at {self.last_short_deal.open_time}, price open {self.last_short_deal.open_price}"
                        )

                    self.manage_open_long_deals(row, timestamp)
                    self.manage_open_short_deals(row, timestamp)

            self._print_stats()

    def check_missing_data(self, df1m: Candles) -> None:
        expected_interval = Timedelta(
            minutes=-1
        )  # Adjust as per your candles frequency

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

    def _print_stats(self) -> None:
        if self.opened_long_deals:
            total_open_price = sum(
                deal.open_price for deal in self.opened_long_deals
            )
            average_open_price = total_open_price / len(self.opened_long_deals)

            print(f'Long average open price: {average_open_price}')
        else:
            print('No opened long deals to calculate average.')

        if self.opened_short_deals:
            total_open_price = sum(
                deal.open_price for deal in self.opened_short_deals
            )
            average_open_price = total_open_price / len(self.opened_short_deals)

            print(f'Short average open price: {average_open_price}')
        else:
            print('No opened short deals to calculate average.')

        for deal in self.opened_long_deals:
            print(
                f'Active long deal: open price {deal.open_price} open time {deal.open_time}'
            )

        for deal in self.opened_short_deals:
            print(
                f'Active short deal: open price {deal.open_price} open time {deal.open_time}'
            )

        print(
            f'Total deals: {self.total_deals}, success deals: {self.success_deals}'
        )
