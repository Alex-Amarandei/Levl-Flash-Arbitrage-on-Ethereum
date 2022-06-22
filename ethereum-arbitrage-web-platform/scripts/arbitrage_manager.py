import os
import sys
import time

from brownie import OrderManager, interface
from eth_abi import encode_abi

from scripts.address_book_manager import get_address_at
from scripts.font_manager import green, purple, red, tag, underline
from scripts.order_manager import update_order_book
from scripts.pair_manager import get_pair_address, get_stable_price
from scripts.utilities import (
    ZERO_ADDRESS,
    get_account,
    get_contract,
    get_eth_price,
    get_optimal_trade_data,
)


def establish_direction():
    order_manager_contract = get_contract("OrderManager", OrderManager)

    uniswap_factory_address = get_address_at(
        name=["factory", "uniswap"], source="config"
    )

    sushiswap_factory_address = get_address_at(
        name=["factory", "sushiswap"], source="config"
    )

    order_book = order_manager_contract.getOrders(ZERO_ADDRESS)

    for entry in order_book:
        order = {
            "id": entry[0],
            "fee": entry[1],
            "status": entry[2],
            "user_address": entry[3],
            "token_0_address": entry[4],
            "token_1_address": entry[5],
            "hash": entry[6],
        }

        if order["status"] != 0:
            continue

        (uniswap_pair_address, _) = get_pair_address(
            uniswap_factory_address, order["token_0_address"], order["token_1_address"]
        )

        (sushiswap_pair_address, _) = get_pair_address(
            sushiswap_factory_address,
            order["token_0_address"],
            order["token_1_address"],
        )

        (uniswap_reserves_0, uniswap_reserves_1, _,) = interface.IUniswapV2Pair(
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

        if (from_0_to_1 and amount_to_borrow > sushiswap_reserves_0) or (
            not from_0_to_1 and amount_to_borrow > sushiswap_reserves_1
        ):
            (from_0_to_1, amount_to_borrow) = get_optimal_trade_data(
                uniswap_reserves_0,
                uniswap_reserves_1,
                sushiswap_reserves_0,
                sushiswap_reserves_1,
            )

            check_arbitrage(
                "uniswap",
                "sushiswap",
                sushiswap_factory_address,
                uniswap_pair_address,
                (uniswap_reserves_0, uniswap_reserves_1),
                (sushiswap_reserves_0, sushiswap_reserves_1),
                order,
                from_0_to_1,
                amount_to_borrow,
            )

        check_arbitrage(
            "sushiswap",
            "uniswap",
            uniswap_factory_address,
            sushiswap_pair_address,
            (sushiswap_reserves_0, sushiswap_reserves_1),
            (uniswap_reserves_0, uniswap_reserves_1),
            order,
            from_0_to_1,
            amount_to_borrow,
        )


def check_arbitrage(
    borrow_dex_name,
    swap_dex_name,
    swap_dex_factory_address,
    borrow_dex_pair_address,
    borrow_dex_reserves,
    swap_dex_reserves,
    order,
    from_0_to_1,
    amount_to_borrow,
):
    try:
        (borrow_dex_reserves_0, borrow_dex_reserves_1) = borrow_dex_reserves
        (swap_dex_reserves_0, swap_dex_reserves_1) = swap_dex_reserves

        if borrow_dex_name is None:
            return

        swap_dex_router_address = get_address_at(
            name=["router", swap_dex_name], source="config"
        )

        borrow_dex_router_address = get_address_at(
            name=["router", borrow_dex_name], source="config"
        )

        stable_price_0 = get_stable_price(
            swap_dex_factory_address, order["token_0_address"]
        )

        if stable_price_0 == -1:
            update_order_book(order["id"], "REJECTED", ZERO_ADDRESS)
            return

        stable_price_1 = get_stable_price(
            swap_dex_factory_address, order["token_1_address"]
        )

        if stable_price_1 == -1:
            update_order_book(order["id"], "REJECTED", ZERO_ADDRESS)
            return

        stable_price_eth = get_eth_price() / 10**18

        eth_price_0 = stable_price_0 / stable_price_eth

        eth_price_1 = stable_price_1 / stable_price_eth

        if amount_to_borrow == 0:
            print(
                f"{tag('ARBITRAGE')} {red('No profitable arbitrage opportunity confirmed for order')} {purple(order['id'])}"
            )
            return

        if from_0_to_1:
            swap_dex_in_reserves = swap_dex_reserves_0
            swap_dex_out_reserves = swap_dex_reserves_1

            borrow_dex_in_reserves = borrow_dex_reserves_1
            borrow_dex_out_reserves = borrow_dex_reserves_0

            main_price = eth_price_0

            parameters = (amount_to_borrow, 0)
        else:
            swap_dex_in_reserves = swap_dex_reserves_1
            swap_dex_out_reserves = swap_dex_reserves_0

            borrow_dex_in_reserves = borrow_dex_reserves_0
            borrow_dex_out_reserves = borrow_dex_reserves_1

            main_price = eth_price_1

            parameters = (0, amount_to_borrow)

        amount_after_selling = interface.IUniswapV2Router02(
            swap_dex_router_address
        ).getAmountOut(amount_to_borrow, swap_dex_in_reserves, swap_dex_out_reserves)

        new_in_reserves = swap_dex_in_reserves + amount_to_borrow
        new_out_reserves = swap_dex_out_reserves - amount_after_selling

        amount_to_repay = interface.IUniswapV2Router02(
            borrow_dex_router_address
        ).getAmountIn(amount_to_borrow, borrow_dex_in_reserves, borrow_dex_out_reserves)

        difference = (amount_after_selling - amount_to_repay) / 10**18

        if difference <= 0:
            print(
                f"{tag('ARBITRAGE')} {red('No profitable arbitrage opportunity confirmed for order')} {purple(order['id'])}"
            )
            return

        difference_in_eth = difference * main_price

        gas_needed = 0.6 * 10**6

        gas_price = 1000001000

        gas_cost = gas_price * gas_needed / 10**18

        profit = difference_in_eth - gas_cost - order["fee"] / 10**18

        print(
            f"{tag('ARBITRAGE')} {underline('Amount Borrowed:')} {amount_to_borrow / 10**18}"
        )

        print(f"{tag('ARBITRAGE')} {underline('Profit In-Kind:')} {difference}")

        print(f"{tag('ARBITRAGE')} {underline('Price of ETH:')} {stable_price_eth}")

        print(f"{tag('ARBITRAGE')} {underline('Price in ETH:')} {main_price}")

        print(f"{tag('ARBITRAGE')} {underline('From 0 to 1:')} {from_0_to_1}")

        print(
            f"{tag('ARBITRAGE')} {underline('Price before:')} {swap_dex_in_reserves / swap_dex_out_reserves}"
        )

        print(
            f"{tag('ARBITRAGE')} {underline('Price after:')} {new_in_reserves/new_out_reserves}"
        )

        print(f"{tag('ARBITRAGE')} {underline('Gas cost:')} {red(gas_cost)}")

        print(
            f"{tag('ARBITRAGE')} {underline('Fee:')} {red(str(order['fee'] / 10**18))}"
        )

        print(
            f"{tag('ARBITRAGE')} {underline('Profit in ETH:')} {green(profit) if profit > 0 else red(profit)}"
        )

        print(
            f"{tag('ARBITRAGE')} {underline('Account:')} {purple(order['user_address'])}"
        )

        if profit <= 0:
            print(
                f"{tag('ARBITRAGE')} {red('Profit is negative due to gas costs and fees.')}"
            )
            return

        flash_contract_address = get_address_at("FlashArbitrage", option=swap_dex_name)

        tx = interface.IUniswapV2Pair(borrow_dex_pair_address).swap(
            parameters[0],
            parameters[1],
            flash_contract_address,
            encode_abi(
                ["uint256", "address", "uint256"],
                [
                    amount_to_repay,
                    order["user_address"],
                    int(time.time()) + 1800,
                ],
            ),
            {
                "from": get_account(),
                "gas": gas_needed,
                "allow_revert": True,
            },
        )

        update_order_book(order["id"], "COMPLETED", tx.txid)

    except Exception as err:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(red(exc_type), red(fname), red(exc_tb.tb_lineno))
        print(
            f"{tag('ARBITRAGE')} {red('Error, marking order')} {purple(order['id'])} {red('as rejected.')}"
        )
        print(red(err))
        update_order_book(order["id"], "REJECTED", ZERO_ADDRESS)


def main():
    while True:
        establish_direction()
