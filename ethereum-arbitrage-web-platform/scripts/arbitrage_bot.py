import json
import time

from brownie import interface
from eth_abi import encode_abi

from scripts.address_book_manager import get_address_at
from scripts.colors import FontColor
from scripts.pair_handler import get_pair_address, get_stable_price
from scripts.utilities import (
    get_account,
    get_eth_price,
    get_factory_address,
    get_flash_contract,
    get_optimal_trade_data,
)

while True:
    with open("data/orders.json", "r") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        uniswap_router_address = get_address_at("UniswapRouter")
        sushiswap_router_address = get_address_at("SushiswapRouter")

        uniswap_factory_address = get_factory_address("Uniswap")
        sushiswap_factory_address = get_factory_address("Sushiswap")

        for order in order_book:
            token_0_address = order["token_0_address"]
            token_1_address = order["token_1_address"]

            (uniswap_pair_address, switched) = get_pair_address(
                uniswap_factory_address, token_0_address, token_1_address
            )

            (sushiswap_pair_address, switched) = get_pair_address(
                sushiswap_factory_address, token_0_address, token_1_address
            )

            stable_price_0 = get_stable_price(uniswap_factory_address, token_0_address)

            stable_price_1 = get_stable_price(uniswap_factory_address, token_1_address)

            stable_price_eth = get_eth_price() / 10**18

            eth_price_0 = stable_price_0 / stable_price_eth

            eth_price_1 = stable_price_1 / stable_price_eth

            (uniswap_reserves_0, uniswap_reserves_1, _) = interface.IUniswapV2Pair(
                uniswap_pair_address
            ).getReserves({"from": get_account()})

            (sushiswap_reserves_0, sushiswap_reserves_1, _) = interface.IUniswapV2Pair(
                sushiswap_pair_address
            ).getReserves({"from": get_account()})

            (from_0_to_1, amount_to_borrow) = get_optimal_trade_data(
                sushiswap_reserves_0,
                sushiswap_reserves_1,
                uniswap_reserves_0,
                uniswap_reserves_1,
            )

            if amount_to_borrow == 0:
                print(FontColor.FAIL + "No profitable arbitrage opportunity confirmed.")
                continue

            if from_0_to_1:
                amount_after_selling = interface.IUniswapV2Router02(
                    uniswap_router_address
                ).getAmountOut(amount_to_borrow, uniswap_reserves_0, uniswap_reserves_1)

                new_uniswap_reserves_0 = uniswap_reserves_0 + amount_to_borrow
                new_uniswap_reserves_1 = uniswap_reserves_1 - amount_after_selling

                amount_to_repay = interface.IUniswapV2Router02(
                    sushiswap_router_address
                ).getAmountIn(
                    amount_to_borrow, sushiswap_reserves_1, sushiswap_reserves_0
                )

                sushiswap_price = amount_to_borrow / amount_to_repay

                difference = (
                    amount_after_selling / amount_to_borrow - 1 / sushiswap_price
                )

                if difference <= 0:
                    print(
                        FontColor.FAIL
                        + "No profitable arbitrage opportunity confirmed."
                    )
                    continue

                total_difference = difference * int(amount_to_borrow / 10**18)

                deadline = int(time.time()) + 1800

                gas_needed = 0.6 * 10**6

                gas_price = 1000001000

                gas_cost = gas_price * gas_needed / 10**18

                profit = total_difference * eth_price_1 - gas_cost

                print(f"Difference: {difference}")

                print(f"Total Difference: {total_difference}")

                print(f"Price in ETH: {eth_price_1}")

                print(f"Profit: {profit}")

                print(f"From 0 to 1: {from_0_to_1}")

                print(f"Price before: {uniswap_reserves_0 / uniswap_reserves_1}")

                print(f"Price after: {new_uniswap_reserves_0/new_uniswap_reserves_1}")

                print(f"Gas cost: {gas_cost}")

                if profit <= 0:
                    print("No profit because gas is expensive")
                    continue

                flash_contract_address = get_flash_contract().address
                print(flash_contract_address)

                interface.IUniswapV2Pair(sushiswap_pair_address).swap(
                    amount_to_borrow,
                    0,
                    flash_contract_address,
                    encode_abi(["uint256", "uint256"], [amount_to_repay, deadline]),
                    {"from": get_account(), "gas": gas_needed},
                )
            else:
                amount_after_selling = interface.IUniswapV2Router02(
                    uniswap_router_address
                ).getAmountOut(amount_to_borrow, uniswap_reserves_1, uniswap_reserves_0)

                new_uniswap_reserves_0 = uniswap_reserves_0 - amount_after_selling
                new_uniswap_reserves_1 = uniswap_reserves_1 + amount_to_borrow

                amount_to_repay = interface.IUniswapV2Router02(
                    sushiswap_router_address
                ).getAmountIn(
                    amount_to_borrow, sushiswap_reserves_0, sushiswap_reserves_1
                )

                sushiswap_price = amount_to_repay / amount_to_borrow

                difference = amount_after_selling / amount_to_borrow - sushiswap_price

                if difference <= 0:
                    print(
                        FontColor.FAIL
                        + "No profitable arbitrage opportunity confirmed."
                    )
                    continue

                total_difference = difference * int(amount_to_borrow / 10**18)

                deadline = int(time.time()) + 1800

                gas_needed = 0.6 * 10**6

                gas_price = 1000001000

                gas_cost = gas_price * gas_needed / 10**18

                profit = total_difference * eth_price_1 - gas_cost

                print(f"Difference: {difference}")

                print(f"Total Difference: {total_difference}")

                print(f"Price in ETH: {eth_price_0}")

                print(f"Profit: {profit}")

                print(f"From 0 to 1: {from_0_to_1}")

                print(f"Price before: {uniswap_reserves_0 / uniswap_reserves_1}")

                print(f"Price after: {new_uniswap_reserves_0 / new_uniswap_reserves_1}")

                print(f"Gas cost: {gas_cost}")

                if profit <= 0:
                    print("No profit because gas is expensive")
                    continue

                flash_contract_address = get_flash_contract().address
                print(flash_contract_address)

                interface.IUniswapV2Pair(sushiswap_pair_address).swap(
                    0,
                    amount_to_borrow,
                    flash_contract_address,
                    encode_abi(["uint256", "uint256"], [amount_to_repay, deadline]),
                    {"from": get_account(), "gas": gas_needed},
                )

    time.sleep(10)
