import json

from brownie import config, interface, network

from scripts.address_book_manager import get_address_at
from scripts.colors import FontColor
from scripts.utilities import get_account


def get_pair_price(factory_address, token_0_address, token_1_address):
    print(f"factory: {factory_address}")
    print(f"token_0 {token_0_address}")
    print(f"token_1 {token_1_address}")
    (pair_address, switched) = get_pair_address(
        factory_address, token_0_address, token_1_address
    )

    pair_contract = interface.IUniswapV2Pair(pair_address)

    if not switched:
        (reserve_0, reserve_1, timestamp) = pair_contract.getReserves()
    else:
        (reserve_1, reserve_0, timestamp) = pair_contract.getReserves()

    return (timestamp, reserve_1 / reserve_0)


def get_pair_info():
    uniswap_factory = interface.IUniswapV2Router02(
        get_address_at("UniswapRouter")
    ).factory()
    sushiswap_factory = interface.IUniswapV2Router02(
        get_address_at("SushiswapRouter")
    ).factory()

    order_book = json.load(open("data/orders.json", "r"))["orders"]

    for order in order_book:
        (uniswap_timestamp, uniswap_price) = get_pair_price(
            uniswap_factory, order["token_0_address"], order["token_1_address"]
        )

        print(
            FontColor.HEADER
            + f"\nTimestamp of last interaction with Uniswap Pair: {uniswap_timestamp}"
        )

        (sushiswap_timestamp, sushiswap_price) = get_pair_price(
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

        if (
            abs(uni_sushi_deviation) < order["expected_deviation"]
            and abs(sushi_uni_deviation) < order["expected_deviation"]
        ):
            print(FontColor.FAIL + "NOT PROFITABLE" + FontColor.ENDC)
        else:
            print(FontColor.OKGREEN + "PROFITABLE" + FontColor.ENDC)


def get_pair_address(factory_address, token_0_address, token_1_address):
    switched = False

    if token_0_address > token_1_address:
        aux = token_1_address
        token_1_address = token_0_address
        token_0_address = aux
        switched = True

    factory = interface.IUniswapV2Factory(factory_address)
    return (
        factory.getPair(
            token_0_address,
            token_1_address,
            {"from": get_account()},
        ),
        switched,
    )


def get_stable_price(factory, token):
    dai = get_address_at("DAI")
    (_, price) = get_pair_price(factory, token, dai)

    return price


def main():
    get_pair_info()
