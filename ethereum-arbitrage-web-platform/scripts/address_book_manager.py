import json

from brownie import network


def update_address_at(name, with_address):
    with open("data/address_book.json", "r+") as address_book_file:
        address_book = json.load(address_book_file)

        address_book[name][network.show_active()] = with_address

        address_book_file.seek(0)
        json.dump(address_book, address_book_file, indent=4)


def get_address_at(name):
    with open("data/address_book.json", "r") as address_book_file:
        address_book = json.load(address_book_file)

        return address_book[name][network.show_active()]
