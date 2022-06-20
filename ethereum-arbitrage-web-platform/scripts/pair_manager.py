from brownie import interface

from scripts.address_book_manager import get_address_at
from scripts.utilities import get_account, highlight, tag


def get_pair_price(factory_address, token_0_address, token_1_address):
    print(f"{tag('PAIR')} Factory Address: {highlight(factory_address)}")
    print(f"{tag('PAIR')} Token 0 Address: {highlight(token_0_address)}")
    print(f"{tag('PAIR')} Token 1 Address: {highlight(token_1_address)}")

    (pair_address, switched) = get_pair_address(
        factory_address, token_0_address, token_1_address
    )

    pair_contract = interface.IUniswapV2Pair(pair_address)

    if pair_contract == "0x0000000000000000000000000000000000000000":
        return (-1, -1)

    if not switched:
        (reserve_0, reserve_1, timestamp) = pair_contract.getReserves()
    else:
        (reserve_1, reserve_0, timestamp) = pair_contract.getReserves()

    return (timestamp, reserve_1 / reserve_0)


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
    dai_address = get_address_at(name=["DAI"], source="config")
    if token == dai_address:
        return 1
    (_, price) = get_pair_price(factory, token, dai_address)

    return price
