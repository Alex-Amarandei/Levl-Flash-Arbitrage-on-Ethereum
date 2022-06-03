from brownie import DataProvider, FlashArbitrage, FundsManager, network

from scripts.address_book_manager import get_address_at, update_address_at
from scripts.font_manager import highlight, tag


def contract_router(contract_name, account):
    if contract_name == "FlashArbitrage":
        return deploy_flash_arbitrage_contract(account)
    elif contract_name == "FundsManager":
        return deploy_funds_manager_contract(account)
    elif contract_name == "DataProvider":
        return deploy_data_provider_contract(account)


def update_info(contract_name, contract_address):
    update_address_at(contract_name, with_address=contract_address)

    print(
        f"{tag('DEPLOY')} {contract_name} contract can be found at {highlight(contract_address)} on the {network.show_active()} network."
    )


def deploy_funds_manager_contract(account):
    funds_manager_contract = FundsManager.deploy(
        10000000000000000,
        {
            "from": account,
        },
        publish_source=True,
    )

    update_info("FundsManager", funds_manager_contract.address)
    return funds_manager_contract


def deploy_flash_arbitrage_contract(account):
    flash_arbitrage_contract = FlashArbitrage.deploy(
        get_address_at("UniswapRouter"),
        {
            "from": account,
        },
        publish_source=True,
    )

    update_info("FlashArbitrage", flash_arbitrage_contract.address)
    return flash_arbitrage_contract


def deploy_data_provider_contract(account):
    data_provider_contract = DataProvider.deploy(
        {
            "from": account,
        },
        publish_source=True,
    )

    update_info("DataProvider", data_provider_contract.address)
    return data_provider_contract


def deploy_token(account, token_name, token):
    initial_supply = 100000000000000000000000000
    token_contract = token.deploy(
        initial_supply,
        {"from": account},
    )

    update_info(token_name, token_contract.address)
    return token_contract
