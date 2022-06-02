import json

from brownie import FlashArbitrage, interface, network

from scripts.address_book_manager import get_address_at, update_address_at
from scripts.colors import FontColor
from scripts.utilities import get_account


def deploy_flash_contract():
    account = get_account()

    flash_contract = FlashArbitrage.deploy(
        interface.IUniswapV2Router02(get_address_at("UniswapRouter")).factory(),
        get_address_at("UniswapRouter"),
        get_address_at("SushiswapRouter"),
        {
            "from": account,
        },
    )
    print(FontColor.BOLD + "Deployed contract!\n" + FontColor.ENDC)

    update_address_at("FlashArbitrage", with_address=flash_contract.address)

    print(flash_contract.address)

    print(network.show_active())

    return flash_contract


def deploy_all():
    flash_contract = deploy_flash_contract()


def main():
    deploy_all()
