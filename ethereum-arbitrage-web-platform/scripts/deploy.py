from brownie import ArbContract, accounts

from scripts.colors import FontColor
from scripts.utilities import get_account


def deploy_arb_contract():
    account = get_account()
    arb_contract = ArbContract.deploy({"from": account})
    print(FontColor.BOLD + "Deployed contract!\n" + FontColor.ENDC)
    return arb_contract


def main():
    deploy_arb_contract()
