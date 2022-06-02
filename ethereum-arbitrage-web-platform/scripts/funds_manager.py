from brownie import FundsManager

from scripts.colors import FontColor
from scripts.utilities import get_account, get_contract


def fund_with_gas(fee_in_wei):
    account = get_account()
    funds_manager_contract = get_contract("FundsManager", FundsManager)

    print(FontColor.OKBLUE + "\nFunding the contract with gas...\n" + FontColor.ENDC)

    tx = funds_manager_contract.fundWithGas({"from": account, "value": fee_in_wei})
    tx.wait(1)

    print(FontColor.OKBLUE + "\nDone!\n" + FontColor.ENDC)
