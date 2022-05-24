import json


def add_to_order_book(token_0_address, token_1_address, expected_deviation):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)

        new_id = order_book["current_id"] + 1
        order_book["current_id"] = new_id

        new_order = dict()
        new_order["id"] = new_id
        new_order["token_0_address"] = token_0_address
        new_order["token_1_address"] = token_1_address
        new_order["expected_deviation"] = expected_deviation

        order_book["orders"].append(new_order)

        order_book_file.seek(0)

        json.dump(order_book, order_book_file, indent=4)


def remove_from_order_book(id):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        for order in order_book:
            if order["id"] == id:
                del order
                break

        order_book_file.seek(0)

        json.dump(order_book, order_book_file, indent=4)
