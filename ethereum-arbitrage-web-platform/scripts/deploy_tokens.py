from brownie import ERC20EUR, ERC20RON

from scripts.address_book_manager import update_address_at
from scripts.utilities import get_account


def deploy_token(token):
    initial_supply = 100000000000000000000000000
    account = get_account()
    token_address = token.deploy(initial_supply, {"from": account}).address
    return token_address


def main():
    update_address_at("ERC20RON", with_address=deploy_token(ERC20RON))
    update_address_at("ERC20EUR", with_address=deploy_token(ERC20EUR))
