from web3 import Web3

from scripts.address_book_manager import get_address_at
from scripts.deploy_manager import deploy_all_contracts
from scripts.font_manager import cyan, green, highlight, purple, red
from scripts.order_manager import add_to_order_book
from scripts.pair_manager import get_pair_address
from scripts.utilities import ZERO_ADDRESS, get_fee


def main():
    # Greetings

    print(highlight("\nHi there! Welcome to"), purple("Levl - Flash Arbitrage"))
    print(green("# # # # # # # # # # # # # # # # # # # # # #\n"))

    # If you want to run the demo, first run main() from demo_manager.py
    # Run it by typing: brownie run scripts/demo_manager.py --network rinkeby
    # You should be good for about 15-20 runs without redeploying liquidity
    ## Choose whatever network is available, we have used rinkeby as an example

    # If you chose the demo, set the value below to True

    demo = True

    if demo:
        token_0_address = get_address_at(name="ERC20RON", source="map")
        token_1_address = get_address_at(name="ERC20EUR", source="map")
    else:
        # Preparing Contracts

        ## To deploy your own version of the contracts (which is the recommended way)
        ## Uncomment the line below

        # deploy_all_contracts()

        # Gathering Input

        print(cyan("You will be asked for the token addresses."))
        print(cyan("The addresses must be valid and 42 characters long."))
        print(cyan("The pair must exist on both Uniswap and Sushiswap."))
        print(cyan("We will also do some checking, but just so you know. :)\n"))

        token_0_address = ""
        token_1_address = ""

        while True:
            token_0_address = input("Please provide the first token's address: ")
            if Web3.isAddress(token_0_address):
                break
            else:
                print(
                    red(
                        "Oops. Your address is not in the right format. Please, try again.\n"
                    )
                )

        while True:
            token_1_address = input("Please provide the second token's address: ")
            if Web3.isAddress(token_1_address):
                break
            else:
                print(
                    red(
                        "Oops. Your address is not in the right format. Please, try again.\n"
                    )
                )

        # Checking Uniswap / Sushiswap Liquidity

        if (
            get_pair_address(
                get_address_at(name=["factory", "uniswap"], source="config"),
                token_0_address,
                token_1_address,
            )
            == ZERO_ADDRESS
        ):
            print(
                red(
                    "Oops. This pair is currently not on Uniswap. Please try another one.\n"
                )
            )
            return -1

        if (
            get_pair_address(
                get_address_at(name=["factory", "sushiswap"], source="config"),
                token_0_address,
                token_1_address,
            )
            == ZERO_ADDRESS
        ):
            print(
                red(
                    "Oops. This pair is currently not on Sushiswap. Please try another one.\n"
                )
            )
            return -1

        # Placing Order

        print(highlight("Good job! We are placing your order right now.\n"))

    add_to_order_book(token_0_address, token_1_address)

    print(green("Your order was placed successfully!"))
    print(purple(f"\nYour account was debited by {get_fee() / 10**18} ETH.\n"))
    print(
        purple("Make sure you have the"),
        highlight("arbitrage_manager.py: main()"),
        purple("running."),
    )
