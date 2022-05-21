from brownie import ArbContract, accounts

from scripts.utilities import get_account


def deploy_arb_contract():
    account = get_account()
    arb_contract = ArbContract.deploy({"from": account})
    print("Deployed contract!")
    return arb_contract


def main():
    deploy_arb_contract()
