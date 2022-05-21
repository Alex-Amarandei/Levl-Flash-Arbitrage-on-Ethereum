from brownie import ArbContract, accounts


def place_order():
    account = accounts.load("metamask-account-1")
    arb_contract = ArbContract[-1]
    arb_contract.fundWithGas({"from": account, "value": 10000000000000000})


def main():
    place_order()
