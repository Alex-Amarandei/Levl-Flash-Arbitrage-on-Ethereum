import json
import time

from brownie import interface

from scripts.colors import FontColor
from scripts.pair_handler import get_pair_address, get_stable_price
from scripts.utilities import (
    get_account,
    get_eth_price,
    get_factory_address,
    get_optimal_trade_data,
)

while True:
    with open("data/orders.json", "r") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        uniswap_factory_address = get_factory_address("Uniswap")
        sushiswap_factory_address = get_factory_address("Sushiswap")

        for order in order_book["orders"]:
            token_0_address = order["token_0_address"]
            token_1_address = order["token_1_address"]

            uniswap_pair_address = get_pair_address(
                uniswap_factory_address, token_0_address, token_1_address
            )

            sushiswap_pair_address = get_pair_address(
                sushiswap_factory_address, token_0_address, token_1_address
            )

            stable_price_0 = get_stable_price(uniswap_factory_address, token_0_address)
            stable_price_1 = get_stable_price(uniswap_factory_address, token_1_address)
            stable_price_eth = get_eth_price()

            eth_price_0 = stable_price_0 / stable_price_eth
            eth_price_1 = stable_price_1 / stable_price_eth

            (uniswap_reserves_0, uniswap_reserves_1, _) = interface.IUniswapV2Pair(
                uniswap_pair_address
            ).getReserves({"from": get_account()})

            (sushiswap_reserves_0, sushiswap_reserves_1, _) = interface.IUniswapV2Pair(
                sushiswap_pair_address
            ).getReserves({"from": get_account()})

            (from_0_to_1, quantity) = get_optimal_trade_data(
                sushiswap_reserves_0,
                sushiswap_reserves_1,
                uniswap_reserves_0,
                uniswap_reserves_1,
            )

            if quantity == 0:
                print(FontColor.FAIL + "No profitable arbitrage opportunity confirmed.")
                continue

            if from_0_to_1:
                pass

    time.sleep(10)
