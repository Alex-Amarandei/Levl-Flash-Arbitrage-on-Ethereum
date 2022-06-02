import pytest
from brownie import exceptions
from scripts.utilities import get_account, get_flash_contract
from web3 import Web3


def test_balance_updates_after_placing_order():
    account = get_account()
    flash_contract = get_flash_contract()

    initial_balance = flash_contract.userGasAmounts(account)
    tx = flash_contract.fundWithGas(
        {"from": account, "value": Web3.toWei(0.01, "ether")}
    )
    tx.wait(1)

    updated_balance = initial_balance + Web3.toWei(0.01, "ether")

    assert flash_contract.userGasAmounts(account) == updated_balance


def test_fail_transaction_if_amount_is_not_correct():
    account = get_account()
    flash_contract = get_flash_contract()
    initial_balance = flash_contract.userGasAmounts(account)

    with pytest.raises(exceptions.VirtualMachineError):
        flash_contract.fundWithGas(
            {"from": account, "value": Web3.toWei(0.02, "ether")}
        )

    assert flash_contract.userGasAmounts(account) == initial_balance


def main():
    test_balance_updates_after_placing_order()
