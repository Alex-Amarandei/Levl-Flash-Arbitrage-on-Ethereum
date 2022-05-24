import time

from brownie import interface, network

from scripts.colors import FontColor
from scripts.utilities import get_account, get_address_by_name


def create_pair(
    router_address, token_0_address, token_1_address, token_0_amount, token_1_amount
):
    router = interface.IUniswapV2Router02(router_address)

    account = get_account()
    deadline = int(time.time()) + 1800

    interface.IERC20(token_0_address).approve(
        router_address,
        1000000000000000000000,
        {"from": account},
    )

    interface.IERC20(token_1_address).approve(
        router_address,
        1000000000000000000000,
        {"from": get_account()},
    )

    (amount_EUR, amount_RON, amount_lp_tokens) = router.addLiquidity(
        token_0_address,
        token_1_address,
        token_0_amount,
        token_1_amount,
        token_0_amount,
        token_1_amount,
        get_account(),
        deadline,
        {
            "from": account,
            "gas": 4000000,
            "gas_price": 4000000000,
        },
    )

    print(FontColor.OKCYAN + f"EUR in the pool: {amount_EUR}")
    print(f"RON in the pool: {amount_RON}" + FontColor.ENDC)
    print(FontColor.BOLD + f"LP Tokens received: {amount_lp_tokens}" + FontColor.ENDC)


def main():
    uniswap_router = get_address_by_name("UniswapRouter")
    sushiswap_router = get_address_by_name("SushiswapRouter")

    EUR_token = get_address_by_name("ERC20EUR")
    RON_token = get_address_by_name("ERC20RON")

    create_pair(uniswap_router, EUR_token, RON_token, 100, 500)
    create_pair(sushiswap_router, EUR_token, RON_token, 100, 400)
