import time

import pytest
from brownie import FundsManager, exceptions
from scripts.funds_manager import update_fee
from scripts.utilities import get_account, get_contract
from web3 import Web3


def set_initial_state(fee=0.01):
    account = get_account()
    funds_manager_contract = get_contract("FundsManager", FundsManager)
    update_fee(Web3.toWei(fee, "ether"))

    return (account, funds_manager_contract)


### Fund With Gas Tests


def test_fund_with_gas_balance_updates_after_placing_order():
    (account, funds_manager_contract) = set_initial_state()

    initial_balance = funds_manager_contract.userGasAmounts(account)
    tx = funds_manager_contract.fundWithGas(
        {"from": account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    updated_balance = initial_balance + Web3.toWei(0.01, "ether")

    assert funds_manager_contract.userGasAmounts(account) == updated_balance


def test_fund_with_gas_fail_transaction_if_amount_is_incorrect():
    (account, funds_manager_contract) = set_initial_state()

    initial_balance = funds_manager_contract.userGasAmounts(account)
    with pytest.raises(exceptions.VirtualMachineError):
        # rinkeby: ValueError
        # local: exceptions.VirtualMachineError
        funds_manager_contract.fundWithGas(
            {
                "from": account,
                "value": Web3.toWei(0.02, "ether"),
                "gas": 600000,
            }
        )

    assert funds_manager_contract.userGasAmounts(account) == initial_balance


### Refund Gas Tests


def test_refund_gas_balance_updates_after_partial_refund():
    (account, funds_manager_contract) = set_initial_state()

    tx = funds_manager_contract.fundWithGas(
        {"from": account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    initial_balance = funds_manager_contract.userGasAmounts(account)
    tx = funds_manager_contract.refundGas(False, {"from": account})
    tx.wait(1)

    updated_balance = initial_balance - Web3.toWei(0.01, "ether")

    assert funds_manager_contract.userGasAmounts(account) == updated_balance


def test_refund_gas_balance_zero_after_full_refund():
    (account, funds_manager_contract) = set_initial_state(0.02)
    tx = funds_manager_contract.fundWithGas(
        {"from": account, "value": Web3.toWei(0.02, "ether")}
    )
    tx.wait(1)

    tx = funds_manager_contract.refundGas(True, {"from": account})
    tx.wait(1)

    assert funds_manager_contract.userGasAmounts(account) == 0


def test_refund_gas_balance_zero_if_fee_is_greater_than_balance():
    (account, funds_manager_contract) = set_initial_state()

    tx = funds_manager_contract.fundWithGas(
        {"from": account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    update_fee(Web3.toWei(0.02, "ether"))

    tx = funds_manager_contract.refundGas(False, {"from": account})
    tx.wait(1)

    assert funds_manager_contract.userGasAmounts(account) == 0


### Use Gas Tests


def test_use_gas_owner_receives_fee():
    (owner_account, funds_manager_contract) = set_initial_state()

    user_account = get_account(1)

    tx = funds_manager_contract.fundWithGas(
        {"from": user_account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    initial_balance = owner_account.balance()
    tx = funds_manager_contract.useGas(user_account, {"from": owner_account})
    tx.wait(1)
    updated_balance = owner_account.balance()

    assert updated_balance <= initial_balance + Web3.toWei(0.01, "ether")


def test_use_gas_owner_receives_all_funds_if_fee_is_greater():
    (owner_account, funds_manager_contract) = set_initial_state()

    user_account = get_account(1)

    tx = funds_manager_contract.fundWithGas(
        {"from": user_account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    update_fee(Web3.toWei(0.02, "ether"))

    owner_initial_balance = owner_account.balance()
    user_funds_balance = funds_manager_contract.userGasAmounts(user_account)
    tx = funds_manager_contract.useGas(user_account, {"from": owner_account})
    tx.wait(1)
    updated_balance = owner_account.balance()

    assert updated_balance <= owner_initial_balance + user_funds_balance


def main():
    test_fund_with_gas_balance_updates_after_placing_order()
    test_fund_with_gas_fail_transaction_if_amount_is_incorrect()
    test_refund_gas_balance_updates_after_partial_refund()
    test_refund_gas_balance_zero_after_full_refund()
    test_refund_gas_balance_zero_if_fee_is_greater_than_balance()
    test_use_gas_owner_receives_fee()
    test_use_gas_owner_receives_all_funds_if_fee_is_greater()
