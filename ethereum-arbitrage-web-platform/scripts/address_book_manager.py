import json

from brownie import config, network


def network_number_converter(network=None, number=None):
    if network is None:
        if number == 1:
            return "mainnet"
        if number == 3:
            return "ropsten"
        if number == 4:
            return "rinkeby"
    elif number is None:
        if network == "mainnet":
            return 1
        if network == "ropsten":
            return 3
        if network == "rinkeby":
            return 4


def get_address_at(name, source="map", option=""):
    if source == "map":
        with open("build/deployments/map.json", "r") as map_json_file:
            map_json = json.load(map_json_file)

            if option == "sushiswap":
                return map_json[
                    str(network_number_converter(network=network.show_active()))
                ][name][1]
            return map_json[
                str(network_number_converter(network=network.show_active()))
            ][name][0]
    else:
        if len(name) == 1:
            return config["networks"][network.show_active()][name[0]]
        elif len(name) == 2:
            return config["networks"][network.show_active()][name[0]][name[1]]
