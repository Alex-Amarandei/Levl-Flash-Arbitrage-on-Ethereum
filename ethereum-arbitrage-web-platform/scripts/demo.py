from scripts.deploy_manager import (
    deploy_data_provider_contract,
    deploy_flash_arbitrage_contract,
    deploy_funds_manager_contract,
)
from scripts.utilities import get_account


def main():
    account = get_account()
    # deploy_funds_manager_contract(account)
    # deploy_data_provider_contract(account)
    deploy_flash_arbitrage_contract(account)
