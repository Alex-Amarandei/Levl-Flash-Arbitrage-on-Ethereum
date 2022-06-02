import json

from brownie import config, interface, network

from scripts.address_book_manager import get_address_at
from scripts.colors import FontColor
from scripts.pair_handler import get_pair_address
from scripts.utilities import get_account, get_flash_contract


def add_to_order_book(token_0_address, token_1_address, expected_deviation):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)

        new_id = order_book["current_id"] + 1
        order_book["current_id"] = new_id

        new_order = dict()
        new_order["id"] = new_id
        new_order["token_0_address"] = token_0_address
        new_order["token_1_address"] = token_1_address
        new_order["expected_deviation"] = expected_deviation

        order_book["orders"].append(new_order)

        order_book_file.seek(0)

        json.dump(order_book, order_book_file, indent=4)


def remove_from_order_book(id):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        for order in order_book:
            if order["id"] == id:
                del order
                break

        order_book_file.seek(0)

        json.dump(order_book, order_book_file, indent=4)


def fund_with_gas():
    account = get_account()
    arb_contract = get_flash_contract()

    print(FontColor.OKBLUE + "\nFunding the contract with gas...\n" + FontColor.ENDC)
    tx = arb_contract.fundWithGas({"from": account, "value": 10000000000000000})
    tx.wait(1)
    print(FontColor.OKBLUE + "\nDone!\n" + FontColor.ENDC)


def execute_order(id=1):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]
        order_to_be_executed = None

        for order in order_book:
            if order["id"] == id:
                order_to_be_executed = order
                break

        uniswap_pair = interface.IUniswapV2Pair(
            get_pair_address(
                config["networks"][network.show_active()]["factory"]["uniswap"],
                order_to_be_executed["token_0_address"],
                order_to_be_executed["token_1_address"],
            )
        )

        flash_contract_address = get_address_at("FlashArbitrage")

        print(uniswap_pair.token0())

        uniswap_pair.swap(
            0,
            10,
            flash_contract_address,
            "2".encode("utf-8"),
            {
                "from": flash_contract_address,
                "gas": 4000000,
                "gas_price": 4000000000,
                "allow_revert": True,
            },
        )

        remove_from_order_book(id)


def main():
    execute_order()
