from scripts.order_manager import get_order, remove_from_order_book
from scripts.pair_manager import get_pair_address
from scripts.utilities import ZERO_ADDRESS, get_factory_address


def main():
    order = get_order()

    uniswap_address = get_pair_address(
        get_factory_address("Uniswap"),
        order["token_0_address"],
        order["token_1_address"],
    )

    sushiswap_address = get_pair_address(
        get_factory_address("Sushiswap"),
        order["token_0_address"],
        order["token_1_address"],
    )

    if uniswap_address == ZERO_ADDRESS or sushiswap_address == ZERO_ADDRESS:
        print("FAILED")

        remove_from_order_book(order["id"])
    else:
        print("SUCCESS")
