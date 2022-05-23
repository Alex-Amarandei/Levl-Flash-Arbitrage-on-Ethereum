from brownie import ArbContract, accounts

from scripts.colors import FontColor
from scripts.utilities import get_account, get_arb_contract


def place_order():
    account = get_account()
    arb_contract = get_arb_contract()

    print(FontColor.OKBLUE + "\nFunding the contract with gas...\n" + FontColor.ENDC)
    tx = arb_contract.fundWithGas({"from": account, "value": 10000000000000000})
    tx.wait(1)
    print(FontColor.OKBLUE + "\nDone!\n" + FontColor.ENDC)


def main():
    place_order()
