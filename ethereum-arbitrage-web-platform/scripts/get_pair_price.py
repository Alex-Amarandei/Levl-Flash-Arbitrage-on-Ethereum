import json

from brownie import config, interface, network

from scripts.colors import FontColor
from scripts.utilities import get_account


def get_price_of_pair(factory_address, token_0_address, token_1_address):
    if token_0_address > token_1_address:
        aux = token_1_address
        token_1_address = token_0_address
        token_0_address = aux

    factory = interface.IUniswapV2Factory(factory_address)
    pair_address = factory.getPair(
        token_0_address,
        token_1_address,
        {"from": get_account()},
    )

    pair_contract = interface.IUniswapV2Pair(pair_address)

    (reserve_0, reserve_1, timestamp) = pair_contract.getReserves()

    return (timestamp, reserve_0 / reserve_1)


def main():
    uniswap_factory = config["networks"][network.show_active()]["factory"]["uniswap"]
    sushiswap_factory = config["networks"][network.show_active()]["factory"][
        "sushiswap"
    ]

    order_book = json.load(open("data/orders.json", "r"))["orders"]

    for order in order_book:
        (uniswap_timestamp, uniswap_price) = get_price_of_pair(
            uniswap_factory, order["token_0_address"], order["token_1_address"]
        )

        print(
            FontColor.HEADER
            + f"\nTimestamp of last interaction with Uniswap Pair: {uniswap_timestamp}"
        )

        (sushiswap_timestamp, sushiswap_price) = get_price_of_pair(
            sushiswap_factory, order["token_0_address"], order["token_1_address"]
        )

        print(
            FontColor.HEADER
            + f"Timestamp of last interaction with Sushiswap Pair: {sushiswap_timestamp}\n"
            + FontColor.ENDC
        )

        print(FontColor.BOLD + f'Order ID: #{order["id"]}')
        print("############\n" + FontColor.ENDC)

        print(f"Uniswap Pair Price: {uniswap_price}")
        print(f"Sushiswap Pair Price: {sushiswap_price}\n")

        uni_sushi_deviation = uniswap_price / sushiswap_price * 100 - 100
        sushi_uni_deviation = sushiswap_price / uniswap_price * 100 - 100

        print(
            (FontColor.FAIL if uni_sushi_deviation < 0 else FontColor.OKGREEN)
            + f"Uniswap-to-Sushiswap Price Deviation: {uni_sushi_deviation}"
        )
        print(
            (FontColor.FAIL if sushi_uni_deviation < 0 else FontColor.OKGREEN)
            + f"Sushiswap-to-Uniswap Price Deviation: {sushi_uni_deviation}\n"
            + FontColor.ENDC
        )
