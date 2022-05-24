import json

from brownie import FlashArbitrage, accounts, config, interface, network

from scripts.colors import FontColor

LOCAL_ENVIRONMENTS = ["development"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None):
    if (
        network.show_active() in LOCAL_ENVIRONMENTS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        if index is not None and index in range(10):
            return accounts[index]
        else:
            return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_flash_contract():
    if len(FlashArbitrage) <= 0:
        print(
            FontColor.UNDERLINE
            + "The FlashArbitrage Contract does not exist yet"
            + FontColor.ENDC
        )

        return FlashArbitrage.deploy(
            interface.IUniswapV2Router02.factory(),
            get_address_by_name("UniswapRouter"),
            get_address_by_name("SushiswapRouter"),
            {"from": get_account()},
        )
    else:
        print(
            FontColor.UNDERLINE
            + f"The FlashArbitrage Contract exists at {FlashArbitrage[-1].address}"
            + FontColor.ENDC
        )
        return FlashArbitrage[-1]


def get_address_by_name(address):
    with open("data/address_book.json", "r") as address_book_file:
        address_book = json.load(address_book_file)

        return address_book["address"][network.show_active()]
