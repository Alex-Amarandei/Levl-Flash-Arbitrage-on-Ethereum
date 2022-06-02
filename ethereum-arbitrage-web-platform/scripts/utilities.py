import json

from brownie import DataProvider, FlashArbitrage, accounts, config, interface, network

from scripts.address_book_manager import get_address_at
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
            interface.IUniswapV2Router02(get_address_at("SushiswapRouter")).factory(),
            get_address_at("UniswapRouter"),
            {"from": get_account()},
        )
    else:
        print(
            FontColor.UNDERLINE
            + f"The FlashArbitrage Contract exists at {FlashArbitrage[-1].address}"
            + FontColor.ENDC
        )
        return FlashArbitrage[-1]


def get_data_provider_contract():
    if len(DataProvider) <= 0:
        print(
            FontColor.UNDERLINE
            + "The DataProvider Contract does not exist yet"
            + FontColor.ENDC
        )

        return DataProvider.deploy(
            {"from": get_account()},
        )
    else:
        print(
            FontColor.UNDERLINE
            + f"The DataProvider Contract exists at {DataProvider[-1].address}"
            + FontColor.ENDC
        )
        return DataProvider[-1]


def get_factory_address(name):
    router_address = get_address_at(f"{name}Router")

    return interface.IUniswapV2Router02(router_address).factory()


def get_eth_price():
    data_provider_contract = get_data_provider_contract()

    return data_provider_contract.getEthPrice(
        get_address_at("ETHPriceFeed"), {"from": get_account()}
    )


def get_optimal_trade_data(
    sushiswap_reserves_0,
    sushiswap_reserves_1,
    uniswap_reserves_0,
    uniswap_reserves_1,
):
    data_provider_contract = get_data_provider_contract()

    return data_provider_contract.getTradeData(
        sushiswap_reserves_0,
        sushiswap_reserves_1,
        uniswap_reserves_0,
        uniswap_reserves_1,
        {"from": get_account()},
    )
