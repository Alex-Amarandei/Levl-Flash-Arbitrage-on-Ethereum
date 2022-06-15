from brownie import DataProvider
from scripts.utilities import get_account, get_contract


def test_get_trade_data():
    data_provider_contract = get_contract("DataProvider", DataProvider)

    assert (True, 1167058) == data_provider_contract.getTradeData(
        10000000, 40000000, 10000000, 50000000, {"from": get_account()}
    )


def main():
    test_get_trade_data()
