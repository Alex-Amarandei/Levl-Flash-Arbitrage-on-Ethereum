import json

from brownie import FlashArbitrage, config, interface, network

from scripts.colors import FontColor
from scripts.utilities import get_account


def deploy_flash_contract():
    account = get_account()
    flash_contract = FlashArbitrage.deploy(
        "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
        "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
        {"from": account},
    )
    print(FontColor.BOLD + "Deployed contract!\n" + FontColor.ENDC)

    print(flash_contract.address)

    print(network.show_active())

    return flash_contract


def deploy_all():
    flash_contract = deploy_flash_contract()

    with open("data/addressBook.json", "r+") as address_book_file:
        address_book = json.load(address_book_file)

        address_book["FlashArbitrage"] = flash_contract.address

        address_book_file.seek(0)

        json.dump(address_book, address_book_file, indent=4)


def main():
    deploy_all()
