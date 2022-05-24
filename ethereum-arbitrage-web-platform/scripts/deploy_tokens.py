from brownie import ERC20EUR, ERC20RON

from scripts.utilities import get_account


def deploy_token(contract):
    initial_supply = 1000000000000000000000
    account = get_account()
    contract.deploy(initial_supply, {"from": account})


def main():
    deploy_token(ERC20RON)
    deploy_token(ERC20EUR)
