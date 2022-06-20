import os

from scripts.order_manager import (
    add_to_order_book,
    get_orders_by_address,
    update_order_book,
)


def register_order(network, user, token_0_address, token_1_address, fee):
    wd = os.getcwd()
    os.chdir("./..")
    add_to_order_book(network, user, token_0_address, token_1_address, fee),

    os.chdir(wd)


def get_orders_of(user):
    wd = os.getcwd()
    os.chdir("./..")
    orders = get_orders_by_address(user)

    os.chdir(wd)

    return orders


def update_order_status(id, all, status):
    wd = os.getcwd()
    os.chdir("./..")
    update_order_book(id=id, all=all, status=status)

    os.chdir(wd)
