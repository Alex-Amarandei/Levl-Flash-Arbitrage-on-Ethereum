from brownie import ArbContract, FlashArbitrage, accounts, config, network

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


def get_arb_contract():
    if len(ArbContract) <= 0:
        print(FontColor.UNDERLINE + "ArbContract does not exist yet" + FontColor.ENDC)
        return ArbContract.deploy({"from": get_account()})
    else:
        print(
            FontColor.UNDERLINE
            + f"ArbContract exists at {ArbContract[-1].address}"
            + FontColor.ENDC
        )
        return ArbContract[-1]


def get_flash_contract():
    if len(FlashArbitrage) <= 0:
        print(
            FontColor.UNDERLINE
            + "The FlashArbitrage Contract does not exist yet"
            + FontColor.ENDC
        )

        return FlashArbitrage.deploy(
            "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
            "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
            {"from": get_account()},
        )
    else:
        print(
            FontColor.UNDERLINE
            + f"The FlashArbitrage Contract exists at {FlashArbitrage[-1].address}"
            + FontColor.ENDC
        )
        return FlashArbitrage[-1]
