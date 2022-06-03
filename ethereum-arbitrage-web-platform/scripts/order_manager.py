import json

from web3 import Web3

from scripts.font_manager import highlight, purple, tag, underline
from scripts.funds_manager import fund_with_gas


def add_to_order_book(user, token_0_address, token_1_address, fee):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)

        new_id = order_book["current_id"] + 1
        order_book["current_id"] = new_id

        new_order = dict()
        new_order["id"] = new_id
        new_order["user_address"] = str(user)
        new_order["token_0_address"] = token_0_address
        new_order["token_1_address"] = token_1_address
        new_order["fee"] = fee

        order_book["orders"].append(new_order)

        order_book_file.seek(0)

        json.dump(order_book, order_book_file, indent=4)

        print(
            f"{tag('ORDER')} Order added successfully!\n"
            + f"{underline('ID:')} {purple(new_id)}\n"
            + f"{underline('User Address:')} {highlight(user)}\n"
            + f"{underline('Token 0 Address:')} {highlight(token_0_address)}\n"
            + f"{underline('Token 1 Address:')} {highlight(token_1_address)}\n"
            + f"{underline('Fee:')} {purple(fee)} ETH\n"
        )


def remove_from_order_book(id):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        for order in order_book:
            if order["id"] == id:
                del order
                break

        order_book_file.seek(0)

        json.dump(order_book, order_book_file, indent=4)

        print(
            f"{tag('ORDER')} Successfully removed order {purple(id)} from the order book."
        )


def place_order(user, token_0_address, token_1_address, fee):
    fund_with_gas(user, Web3.toWei(fee, "ether"))

    add_to_order_book(user, token_0_address, token_1_address, fee)
