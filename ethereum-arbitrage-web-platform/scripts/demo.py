from brownie import ERC20EUR, ERC20RON
from web3 import Web3

from scripts import arbitrage_manager
from scripts.address_book_manager import get_address_at
from scripts.deploy_manager import (
    deploy_data_provider_contract,
    deploy_flash_arbitrage_contract,
    deploy_funds_manager_contract,
    deploy_token,
)
from scripts.funds_manager import update_fee
from scripts.order_manager import place_order
from scripts.utilities import get_account


def deploy_tokens(account):
    deploy_token(account, "ERC20RON", ERC20RON)
    deploy_token(account, "ERC20EUR", ERC20EUR)


def deploy_all_contracts(account):
    deploy_funds_manager_contract(account)
    deploy_data_provider_contract(account)
    deploy_flash_arbitrage_contract(account)


def add_three_mock_orders():
    update_fee(Web3.toWei(0.01, "ether"))

    place_order(
        get_account(1),
        get_address_at("ERC20RON"),
        get_address_at("ERC20EUR"),
        0.01,
    )

    update_fee(Web3.toWei(0.02, "ether"))

    place_order(
        get_account(1),
        get_address_at("ERC20EUR"),
        get_address_at("ERC20RON"),
        0.02,
    )

    update_fee(Web3.toWei(1, "ether"))

    place_order(
        get_account(2),
        get_address_at("ERC20RON"),
        get_address_at("ERC20EUR"),
        1,
    )


def run_arbitrage_bot():
    arbitrage_manager.main()


def main():
    account = get_account()

    # deploy_tokens(account)
    # deploy_all_contracts(account)
    # add_three_mock_orders()
    run_arbitrage_bot()
