from brownie import FundsManager

from scripts.font_manager import cyan, green, tag
from scripts.utilities import get_account, get_contract


def fund_with_gas(account, fee_in_wei):
    funds_manager_contract = get_contract("FundsManager", FundsManager)

    print(f"{tag('FUNDS')} {cyan('Funding the contract with gas...')}")

    tx = funds_manager_contract.fundWithGas({"from": account, "value": fee_in_wei})
    tx.wait(1)

    print(f"{tag('FUNDS')} {green('Done!')}")


def update_fee(fee_in_wei):
    account = get_account()
    funds_manager_contract = get_contract("FundsManager", FundsManager)

    print(f"{tag('FUNDS')} {cyan('Updating the contract fee...')}")

    tx = funds_manager_contract.updateFee(fee_in_wei, {"from": account})
    tx.wait(1)

    print(f"{tag('FUNDS')} {green('Done!')}")
