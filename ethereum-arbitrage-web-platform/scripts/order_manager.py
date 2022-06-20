import json

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
            new_order["status"] = "PENDING"
            new_order["user_address"] = str(user)
            new_order["token_0_address"] = token_0_address
            new_order["token_1_address"] = token_1_address
            new_order["fee"] = fee
            new_order["hash"] = ""

            order_book["orders"].append(new_order)

            order_book["orders"] = sorted(
                order_book["orders"],
                key=lambda x: x["status"] == "PENDING",
                reverse=True,
            )

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


def update_order_book(id, all=False, hash="", status=""):
    with open("data/orders.json", "r+") as order_book_file:
        order_json = json.load(order_book_file)
        current_id = order_json["current_id"]
        order_book = order_json["orders"]

        for order in order_book:
            if not all:
                if order["id"] == id:
                    order["status"] = status
                    order["hash"] = hash
                    break
            if all:
                if order["id"] == id and order["status"] != "COMPLETED":
                    order["status"] = status
                    order["hash"] = hash

        new_order_json = {"current_id": current_id, "orders": order_book}

        order_book_file.seek(0)
        json.dump(new_order_json, order_book_file, indent=4)
        order_book_file.truncate()

        print(f"{tag('ORDER')} Successfully updated order {purple(id)}.")


def get_orders_by_address(user):
    with open("data/orders.json", "r+") as order_book_file:
        order_book = json.load(order_book_file)["orders"]

        orders = []

        for order in order_book:
            if (
                order["user_address"].lower() == user.lower()
                and order["status"] != "DELETED"
            ):
                orders.append(
                    {
                        "id": order["id"],
                        "status": order["status"],
                        "token0Address": order["token_0_address"],
                        "token1Address": order["token_1_address"],
                        "fee": order["fee"],
                        "hash": order["hash"],
                    }
                )

        return orders
