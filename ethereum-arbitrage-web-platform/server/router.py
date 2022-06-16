import os

from scripts.order_manager import add_to_order_book


def register_order(network, user, token_0_address, token_1_address, fee):
    wd = os.getcwd()
    os.chdir("./..")
    add_to_order_book(
        network, user, token_0_address, token_1_address, str(int(fee) / 10**18)
    ),

    os.chdir(wd)
