from brownie import (
    ERC20EUR,
    ERC20RON,
    DataProvider,
    FlashArbitrage,
    FundsManager,
    accounts,
    config,
)

from scripts.address_book_manager import get_address_at
from scripts.font_manager import highlight, tag


def contract_router(contract_name, account):
    if contract_name == "FlashArbitrage":
        return deploy_flash_arbitrage_contract(account)
    elif contract_name == "FundsManager":
        return deploy_funds_manager_contract(account)
    elif contract_name == "DataProvider":
        return deploy_data_provider_contract(account)
    elif contract_name == "ERC20RON":
        return deploy_token(accounts.add(config["wallets"]["deployer"]), ERC20RON)
    elif contract_name == "ERC20EUR":
        return deploy_token(accounts.add(config["wallets"]["deployer"]), ERC20EUR)


def deploy_funds_manager_contract(account):
    funds_manager_contract = FundsManager.deploy(
        10000000000000000,
        {
            "from": account,
        },
        publish_source=True,
    )

    return funds_manager_contract


def deploy_flash_arbitrage_contract(account):
    flash_arbitrage_contract = FlashArbitrage.deploy(
        get_address_at(name=["router", "uniswap"], source="config"),
        {
            "from": account,
        },
        publish_source=True,
    )

    return flash_arbitrage_contract


def deploy_data_provider_contract(account):
    data_provider_contract = DataProvider.deploy(
        {
            "from": account,
        },
        publish_source=True,
    )

    return data_provider_contract


def deploy_token(account, token):
    initial_supply = 100000000000000000000000000
    token_contract = token.deploy(
        initial_supply,
        {"from": account},
    )

    return token_contract
