import json
import time

from brownie import interface
from eth_abi import encode_abi

from scripts.address_book_manager import get_address_at
from scripts.font_manager import green, purple, red, tag, underline
from scripts.pair_manager import get_pair_address, get_stable_price
from scripts.utilities import (
    get_account,
    get_eth_price,
    get_factory_address,
    get_optimal_trade_data,
)


def main():
    with open("data/orders.json", "r") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        uniswap_router_address = get_address_at("UniswapRouter")
        sushiswap_router_address = get_address_at("SushiswapRouter")

        uniswap_factory_address = get_factory_address("Uniswap")
        sushiswap_factory_address = get_factory_address("Sushiswap")

        for order in order_book:
            id = order["id"]
            user_address = order["user_address"]
            token_0_address = order["token_0_address"]
            token_1_address = order["token_1_address"]
            fee = order["fee"]

            (uniswap_pair_address, _) = get_pair_address(
                uniswap_factory_address, token_0_address, token_1_address
            )

            (sushiswap_pair_address, _) = get_pair_address(
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

            (sushiswap_reserves_0, sushiswap_reserves_1, _,) = interface.IUniswapV2Pair(
                sushiswap_pair_address
            ).getReserves({"from": get_account()})

            (from_0_to_1, amount_to_borrow) = get_optimal_trade_data(
                sushiswap_reserves_0,
                sushiswap_reserves_1,
                uniswap_reserves_0,
                uniswap_reserves_1,
            )

            if amount_to_borrow == 0:
                print(
                    f"{tag('ARBITRAGE')} {red(f'No profitable arbitrage opportunity confirmed for order {purple(id)}.')}"
                )
                continue

            if from_0_to_1:
                uniswap_in_reserves = uniswap_reserves_0
                uniswap_out_reserves = uniswap_reserves_1

                sushiswap_in_reserves = sushiswap_reserves_1
                sushiswap_out_reserves = sushiswap_reserves_0

                main_price = eth_price_1

                parameters = (amount_to_borrow, 0)
            else:
                uniswap_in_reserves = uniswap_reserves_1
                uniswap_out_reserves = uniswap_reserves_0

                sushiswap_in_reserves = sushiswap_reserves_0
                sushiswap_out_reserves = sushiswap_reserves_1

                main_price = eth_price_0

                parameters = (0, amount_to_borrow)

            amount_after_selling = interface.IUniswapV2Router02(
                uniswap_router_address
            ).getAmountOut(amount_to_borrow, uniswap_in_reserves, uniswap_out_reserves)

            new_in_reserves = uniswap_in_reserves + amount_to_borrow
            new_out_reserves = uniswap_out_reserves - amount_after_selling

            amount_to_repay = interface.IUniswapV2Router02(
                sushiswap_router_address
            ).getAmountIn(
                amount_to_borrow, sushiswap_in_reserves, sushiswap_out_reserves
            )

            if from_0_to_1:
                sushiswap_price = amount_to_borrow / amount_to_repay

                difference = (
                    amount_after_selling / amount_to_borrow - 1 / sushiswap_price
                )
            else:
                sushiswap_price = amount_to_repay / amount_to_borrow

                difference = amount_after_selling / amount_to_borrow - sushiswap_price

            if difference <= 0:
                print(
                    f"{tag('ARBITRAGE')} {red(f'No profitable arbitrage opportunity confirmed for order {purple(id)}.')}"
                )
                continue

            total_difference = difference * int(amount_to_borrow / 10**18)

            deadline = int(time.time()) + 1800

            gas_needed = 0.6 * 10**6

            gas_price = 1000001000

            gas_cost = gas_price * gas_needed / 10**18

            profit = total_difference * main_price - gas_cost - fee

            print(f"{tag('ARBITRAGE')} {underline('Difference:')} {difference}")

            print(
                f"{tag('ARBITRAGE')} {underline('Total Difference:')} {total_difference}"
            )

            print(f"{tag('ARBITRAGE')} {underline('Price in ETH:')} {main_price}")

            print(f"{tag('ARBITRAGE')} {underline('From 0 to 1:')} {from_0_to_1}")

            print(
                f"{tag('ARBITRAGE')} {underline('Price before:')} {uniswap_in_reserves / uniswap_out_reserves}"
            )

            print(
                f"{tag('ARBITRAGE')} {underline('Price after:')} {new_in_reserves/new_out_reserves}"
            )

            print(f"{tag('ARBITRAGE')} {underline('Gas cost:')} {red(gas_cost)}")

            print(f"{tag('ARBITRAGE')} {underline('Fee:')} {red(fee)}")

            print(
                f"{tag('ARBITRAGE')} {underline('Profit:')} {green(profit) if profit > 0 else red(profit)}"
            )

            print(f"{tag('ARBITRAGE')} {underline('Account:')} {purple(user_address)}")

            if profit <= 0:
                print(
                    f"{tag('ARBITRAGE')} {red('Profit is negative due to gas costs and fees.')}"
                )
                continue

            flash_contract_address = get_address_at("FlashArbitrage")

            interface.IUniswapV2Pair(sushiswap_pair_address).swap(
                parameters[0],
                parameters[1],
                flash_contract_address,
                encode_abi(
                    ["uint256", "uint256", "address"],
                    [amount_to_repay, deadline, user_address],
                ),
                {
                    "from": get_account(),
                    "gas": gas_needed,
                    "allow_revert": True,
                },
            )
