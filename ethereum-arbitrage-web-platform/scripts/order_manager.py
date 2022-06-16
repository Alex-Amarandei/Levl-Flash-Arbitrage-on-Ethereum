import json
import os

from scripts.font_manager import highlight, purple, tag, underline


def add_to_order_book(network, user, token_0_address, token_1_address, fee):
    try:
        with open("data/orders.json", "r+") as order_book_file:
            order_book = json.load(order_book_file)

            new_id = order_book["current_id"] + 1
            order_book["current_id"] = new_id

            new_order = dict()
            new_order["id"] = new_id
            new_order["network"] = network
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
                + f"{underline('Network:')} {purple(network)}\n"
                + f"{underline('User Address:')} {highlight(user)}\n"
                + f"{underline('Token 0 Address:')} {highlight(token_0_address)}\n"
                + f"{underline('Token 1 Address:')} {highlight(token_1_address)}\n"
                + f"{underline('Fee:')} {purple(fee)} ETH\n"
            )
    except FileNotFoundError:
        print("Invalid. Retrying...")


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


def place_order(network, user, token_0_address, token_1_address, fee):
    from web3 import Web3

    from scripts.funds_manager import fund_with_gas

    fund_with_gas(user, Web3.toWei(fee, "ether"))

    add_to_order_book(network, user, token_0_address, token_1_address, fee)


def get_order(id=-1):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        if id == -1:
            return order_book[len(order_book) - 1]
        else:
            for order in order_book:
                if order["id"] == id:
                    return order
