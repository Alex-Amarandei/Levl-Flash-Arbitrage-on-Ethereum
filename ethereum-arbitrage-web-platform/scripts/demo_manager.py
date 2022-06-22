import time

from brownie import ERC20EUR, ERC20RON, interface

from scripts.address_book_manager import get_address_at
from scripts.deploy_manager import (
    deploy_data_provider_contract,
    deploy_flash_arbitrage_contract,
    deploy_order_manager_contract,
    deploy_token,
)
from scripts.migration_manager import migrate_builds, migrate_config
from scripts.utilities import get_account, get_contract


def demo_deploy_liquidity():
    token_deployer_account = get_account(33)

    # Deploy Tokens
    deploy_token(token_deployer_account, ERC20RON)
    deploy_token(token_deployer_account, ERC20EUR)

    # Get New Contracts
    erc20_ron_contract = get_contract("ERC20RON", ERC20RON)
    time.sleep(5)

    erc20_eur_contract = get_contract("ERC20EUR", ERC20EUR)
    time.sleep(5)

    # Approve Spending on Uniswap and Sushiswap
    uniswap_router_address = get_address_at(name=["router", "uniswap"], source="config")
    sushiswap_router_address = get_address_at(
        name=["router", "sushiswap"], source="config"
    )

    tx = erc20_ron_contract.approve(
        uniswap_router_address,
        100000000000000000000000000,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    tx = erc20_eur_contract.approve(
        uniswap_router_address,
        100000000000000000000000000,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    tx = erc20_ron_contract.approve(
        sushiswap_router_address,
        100000000000000000000000000,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    tx = erc20_eur_contract.approve(
        sushiswap_router_address,
        100000000000000000000000000,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    # Deploy Pair Liquidity on Uniswap and Sushiswap

    erc20_ron_address = get_address_at("ERC20RON")
    erc20_eur_address = get_address_at("ERC20EUR")

    tx = interface.IUniswapV2Router02(uniswap_router_address).addLiquidity(
        erc20_ron_address,
        erc20_eur_address,
        40000000 * 10**18,
        10000000 * 10**18,
        4000000 * 10**18,
        1000000 * 10**18,
        "0xfe292575CE771c21EfC3df89F4f16cb075d10dBC",
        int(time.time()) + 1800,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    tx = interface.IUniswapV2Router02(sushiswap_router_address).addLiquidity(
        erc20_ron_address,
        erc20_eur_address,
        50000000 * 10**18,
        10000000 * 10**18,
        5000000 * 10**18,
        1000000 * 10**18,
        "0xfe292575CE771c21EfC3df89F4f16cb075d10dBC",
        int(time.time()) + 1800,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    # Deploy DAI Liquidity on Uniswap

    tx = interface.IUniswapV2Router02(uniswap_router_address).addLiquidity(
        erc20_ron_address,
        get_address_at(name=["DAI"], source="config"),
        400000 * 10**18,
        100000 * 10**18,
        40000 * 10**18,
        10000 * 10**18,
        "0xfe292575CE771c21EfC3df89F4f16cb075d10dBC",
        int(time.time()) + 1800,
        {"from": token_deployer_account},
    )
    tx.wait(2)

    tx = interface.IUniswapV2Router02(uniswap_router_address).addLiquidity(
        erc20_eur_address,
        get_address_at(name=["DAI"], source="config"),
        100000 * 10**18,
        100000 * 10**18,
        10000 * 10**18,
        10000 * 10**18,
        "0xfe292575CE771c21EfC3df89F4f16cb075d10dBC",
        int(time.time()) + 1800,
        {"from": token_deployer_account},
    )
    tx.wait(2)


def demo_deploy_all_contracts():
    account = get_account()
    deploy_order_manager_contract(account)
    deploy_flash_arbitrage_contract(account)
    deploy_data_provider_contract(account)


def main():
    # demo_deploy_liquidity()
    # demo_deploy_all_contracts()

    # Complete with the path to the src folder in the front end
    path = "client/src/"

    migrate_config(path)
    migrate_builds(path)
