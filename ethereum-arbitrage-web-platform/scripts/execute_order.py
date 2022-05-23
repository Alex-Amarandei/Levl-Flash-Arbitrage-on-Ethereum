import json

from brownie import config, interface, network

from scripts.colors import FontColor
from scripts.pairs import get_pair_address
from scripts.utilities import get_account, get_flash_contract


def fund_with_gas():
    account = get_account()
    arb_contract = get_flash_contract()

    print(FontColor.OKBLUE + "\nFunding the contract with gas...\n" + FontColor.ENDC)
    tx = arb_contract.fundWithGas({"from": account, "value": 10000000000000000})
    tx.wait(1)
    print(FontColor.OKBLUE + "\nDone!\n" + FontColor.ENDC)


def place_order(id=1):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]
        order_to_be_executed = None

        for order in order_book:
            if order["id"] == id:
                order_to_be_executed = order
                break

        pair_address_uniswap = interface.IUniswapV2Pair(
            get_pair_address(
                config["networks"][network.show_active()]["factory"]["uniswap"],
                order_to_be_executed["token_0_address"],
                order_to_be_executed["token_1_address"],
            )
        )

        with open("data/addressBook.json", "r") as address_book_file:
            address_book = json.load(address_book_file)
            flash_contract_address = address_book["FlashArbitrage"]
            pair_address_uniswap.swap(
                0,
                1,
                flash_contract_address,
                "2".encode("utf-8"),
                {"from": flash_contract_address},
            )


def execute_order(id=1):
    fund_with_gas()
    fund_with_gas()
    fund_with_gas()
    place_order(id)


def main():
    execute_order()
