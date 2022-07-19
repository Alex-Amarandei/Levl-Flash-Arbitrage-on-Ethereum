from brownie import OrderManager, network

from scripts.font_manager import cyan, green, highlight, purple, tag, underline
from scripts.utilities import ZERO_ADDRESS, get_account, get_contract, get_fee

STATUS = {"PENDING": 0, "COMPLETED": 1, "REJECTED": 2, "DELETED": 3}


def add_to_order_book(token_0_address, token_1_address):
    order_manager_contract = get_contract("OrderManager", OrderManager)

    order_manager_contract.createOrder(
        token_0_address, token_1_address, {"from": get_account(), "value": get_fee()}
    )

    new_id = order_manager_contract.currentId() - 1

    order = order_manager_contract.userOrdersById(new_id)

    print(
        f"{tag('ORDER')} Order added successfully!\n"
        + f"{underline('ID:')} {purple(new_id)}\n"
        + f"{underline('Network:')} {purple(network.show_active())}\n"
        + f"{underline('User Address:')} {highlight(order['userAddress'])}\n"
        + f"{underline('Token 0 Address:')} {highlight(order['token0Address'])}\n"
        + f"{underline('Token 1 Address:')} {highlight(order['token1Address'])}\n"
        + f"{underline('Fee:')} {purple(str(order['fee']/10**18))} ETH\n"
    )


def update_order_book(id, status, hash):
    order_manager_contract = get_contract("OrderManager", OrderManager)

    order_manager_contract.updateOrder(
        id, STATUS[status], hash, {"from": get_account()}
    )

    print(f"{tag('ORDER')} Successfully updated order {purple(id)}.")


def update_fee(fee_in_wei):
    account = get_account()
    order_manager_contract = get_contract("OrderManager", OrderManager)

    print(f"{tag('FUNDS')} {cyan('Updating the contract fee...')}")

    tx = order_manager_contract.updateFee(fee_in_wei, {"from": account})
    tx.wait(1)

    print(f"{tag('FUNDS')} {green('Done!')}")


def main():
    update_fee(10**16)
