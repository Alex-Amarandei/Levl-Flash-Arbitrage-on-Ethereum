from brownie import DataProvider, accounts, config, interface, network

from scripts.address_book_manager import get_address_at, update_address_at
from scripts.colors import FontColor
from scripts.deploy_manager import contract_router

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


def get_contract(contract_name, contract):
    if len(contract) <= 0:
        print(
            FontColor.UNDERLINE
            + f"The {contract_name} contract does not exist yet"
            + FontColor.ENDC
        )
        return contract_router(contract_name, get_account())
    else:
        print(
            FontColor.UNDERLINE
            + f"The {contract_name} contract exists at {contract[-1].address}"
            + FontColor.ENDC
        )
        return contract[-1]


def get_factory_address(name):
    router_address = get_address_at(f"{name}Router")

    return interface.IUniswapV2Router02(router_address).factory()


def get_eth_price():
    data_provider_contract = get_contract("DataProvider", DataProvider)

    return data_provider_contract.getEthPrice(
        get_address_at("ETHPriceFeed"), {"from": get_account()}
    )


def get_optimal_trade_data(
    sushiswap_reserves_0,
    sushiswap_reserves_1,
    uniswap_reserves_0,
    uniswap_reserves_1,
):
    data_provider_contract = get_contract("DataProvider", DataProvider)

    return data_provider_contract.getTradeData(
        sushiswap_reserves_0,
        sushiswap_reserves_1,
        uniswap_reserves_0,
        uniswap_reserves_1,
        {"from": get_account()},
    )


def update_info(contract_name, contract_address):
    print(FontColor.BOLD + "Deployed contract!\n" + FontColor.ENDC)

    update_address_at(contract_name, with_address=contract_address)

    print(
        FontColor.OKBLUE
        + FontColor.UNDERLINE
        + f"{contract_name} contract can be found at {contract_address} on the {network.show_active()} network."
        + FontColor.ENDC
    )
