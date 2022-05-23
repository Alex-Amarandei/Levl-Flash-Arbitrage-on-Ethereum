from brownie import ArbContract, accounts, config, network

LOCAL_ENVIRONMENTS = ["development"]
FORKED_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None):
    if (
        network.show_active() in LOCAL_ENVIRONMENTS
        or network.show_active() in FORKED_ENVIRONMENTS
    ):
        if index is not None and index in range(10):
            return accounts[index]
        else:
            return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_arb_contract():
    if len(ArbContract) <= 0:
        return ArbContract.deploy({"from": get_account()})
    else:
        return ArbContract[-1]
