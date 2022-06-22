from brownie import (
    ERC20EUR,
    ERC20RON,
    DataProvider,
    FlashArbitrage,
    OrderManager,
    accounts,
    config,
)

from scripts.address_book_manager import get_address_at


def contract_router(contract_name, account):
    if contract_name == "FlashArbitrage":
        return deploy_flash_arbitrage_contract(account)
    elif contract_name == "OrderManager":
        return deploy_order_manager_contract(account)
    elif contract_name == "DataProvider":
        return deploy_data_provider_contract(account)
    elif contract_name == "ERC20RON":
        return deploy_token(accounts.add(config["wallets"]["deployer"]), ERC20RON)
    elif contract_name == "ERC20EUR":
        return deploy_token(accounts.add(config["wallets"]["deployer"]), ERC20EUR)


def deploy_order_manager_contract(account):
    order_manager_contract = OrderManager.deploy(
        10000000000000000,
        {
            "from": account,
        },
        publish_source=True,
    )

    return order_manager_contract


def deploy_order_manager_contract(account):
    order_manager_contract = OrderManager.deploy(
        10000000000000000,
        {
            "from": account,
        },
        publish_source=True,
    )

    return order_manager_contract


def deploy_flash_arbitrage_contract(account):
    flash_arbitrage_contract_sushiswap = FlashArbitrage.deploy(
        get_address_at(name=["router", "sushiswap"], source="config"),
        {
            "from": account,
        },
        publish_source=True,
    )

    flash_arbitrage_contract_uniswap = FlashArbitrage.deploy(
        get_address_at(name=["router", "uniswap"], source="config"),
        {
            "from": account,
        },
        publish_source=True,
    )

    return {
        "uniswap": flash_arbitrage_contract_uniswap,
        "sushiswap": flash_arbitrage_contract_sushiswap,
    }


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


def deploy_all_contracts():
    account = accounts.add(config["wallets"]["from_key"])
    deploy_flash_arbitrage_contract(account)
    deploy_order_manager_contract(account)
    deploy_data_provider_contract(account)
