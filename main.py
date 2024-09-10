import json

import ccxt
from ccxt import Exchange
from pandas import set_option

from Backtest.Backtest import Backtest
from Strategy.Strategy import Strategy


def get_binance_exchange() -> Exchange:
    return ccxt.binance({'enableRateLimit': True})


def main() -> None:
    # TODO: temporary fix
    set_option('display.precision', 8)

    with open('strategy.json', 'r') as file:
        strategy = Strategy.from_dict(json.load(file))
        Backtest(strategy, get_binance_exchange()).run()

        # content = json.load(file)
        # tokens = Tokenizer(content['long']['conditions']['entry']).tokenize()
        # ast = Parser(tokens).parse()

        # visualize_ast(ast)
        #
        # entry_price = 20
        #
        # print(entry_price + entry_price * 0.01 - (4 * 6) + 8)
        #
        # print(ast.evaluate({'entry_price': 20}))


if __name__ == '__main__':
    main()
