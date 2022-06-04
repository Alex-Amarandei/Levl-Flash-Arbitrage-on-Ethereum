import pytest
from brownie import FundsManager, exceptions
from scripts.funds_manager import update_fee
from scripts.utilities import get_account, get_contract
from web3 import Web3


def test_balance_updates_after_placing_order():
    account = get_account()
    funds_manager_contract = get_contract("FundsManager", FundsManager)
    update_fee(Web3.toWei(0.01, "ether"))

    initial_balance = funds_manager_contract.userGasAmounts(account)
    tx = funds_manager_contract.fundWithGas(
        {"from": account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    updated_balance = initial_balance + Web3.toWei(0.01, "ether")

    assert funds_manager_contract.userGasAmounts(account) == updated_balance


def test_fail_transaction_if_amount_is_not_correct():
    account = get_account()
    funds_manager_contract = get_contract("FundsManager", FundsManager)
    update_fee(Web3.toWei(0.01, "ether"))

    initial_balance = funds_manager_contract.userGasAmounts(account)
    with pytest.raises(ValueError):
        # or exceptions.VirtualMachineError
        funds_manager_contract.fundWithGas(
            {
                "from": account,
                "value": Web3.toWei(0.02, "ether"),
                "gas": 600000,
            }
        )

    assert funds_manager_contract.userGasAmounts(account) == initial_balance


def main():
    test_balance_updates_after_placing_order()
    test_fail_transaction_if_amount_is_not_correct()
