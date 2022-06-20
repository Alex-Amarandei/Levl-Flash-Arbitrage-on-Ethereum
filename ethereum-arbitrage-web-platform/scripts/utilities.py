import json

import yaml
from brownie import DataProvider, FundsManager, accounts, config, network

from scripts.address_book_manager import get_address_at
from scripts.deploy_manager import contract_router
from scripts.font_manager import green, highlight, tag, yellow
from scripts.migration_manager import migrate_builds, migrate_config

LOCAL_ENVIRONMENTS = ["development"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def get_account(index=None):
    if index == 33:
        return accounts.add(config["wallets"]["deployer"])
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
            f"{tag('UTILITIES')} {yellow(f'The {contract_name} contract does not exist yet.')}"
        )
        return contract_router(contract_name, get_account())
    else:
        print(
            f"{tag('UTILITIES')} {green(f'The {contract_name} contract is already deployed at')} {highlight(contract[-1].address)}{green('.')}"
        )
        return contract[-1]


def get_eth_price():
    data_provider_contract = get_contract("DataProvider", DataProvider)

    return data_provider_contract.getEthPrice(
        get_address_at(name=["ETHPriceFeed"], source="config"), {"from": get_account()}
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


def get_fee():
    funds_manager_contract = get_contract("FundsManager", FundsManager)
    return funds_manager_contract.fee()
